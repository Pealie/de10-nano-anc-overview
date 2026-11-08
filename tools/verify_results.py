#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Neil Thomson
"""Offline replay of the selected TIM035 records; Python standard library only.

Adapted from tim035_right_sustain_score.py and tim035_right_iq_score.py
at the run-specific source identities in evidence/manifest.json.
Reads local evidence only. Contains no hardware or network operations.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TURN = 2**32
CALIBRATION = complex(-302.87207031250017, 1879.4453125)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def local_file(name: str) -> Path:
    path = (ROOT / name).resolve()
    require(path.is_relative_to(ROOT), f"path leaves repository: {name}")
    return path


def quantise(drive: complex) -> tuple[int, int, complex]:
    gain = round(abs(drive))
    if gain == 0:
        return 0, 0, 0j
    phase = round((cmath.phase(drive) % math.tau) / math.tau * TURN) % TURN
    return phase, gain, cmath.rect(gain, math.tau * phase / TURN)


def requested(last: complex, error: complex, rate: float, cap: int):
    target = last - rate * error / CALIBRATION
    if abs(target) > cap:
        target *= cap / abs(target)
    move = target - last
    for limit in (8.0, 7.499999):
        bounded = target if abs(move) <= limit else last + move * limit / abs(move)
        phase, gain, drive = quantise(bounded)
        if gain <= cap and abs(drive - last) <= 8.000001:
            return phase, gain
    raise ValueError("feedback step cannot be quantised within recorded bounds")


def mean_power(values: list[complex]) -> float:
    require(bool(values), "empty measurement period")
    return math.fsum(z.real * z.real + z.imag * z.imag for z in values) / len(values)


def compare(actual, expected, label: str) -> None:
    if isinstance(expected, bool) or isinstance(expected, int):
        require(actual == expected, f"{label}: {actual!r} != {expected!r}")
    elif isinstance(expected, float):
        require(math.isclose(actual, expected, rel_tol=2e-12, abs_tol=2e-9),
                f"{label}: {actual!r} != {expected!r}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{label}: list length")
        for index, (left, right) in enumerate(zip(actual, expected)):
            compare(left, right, f"{label}[{index}]")
    else:
        require(actual == expected, f"{label}: unequal values")


def assess_span(path: Path, seconds: int, rate: float, cap: int) -> dict:
    require(seconds in (10, 60), "unsupported span")
    count = seconds * 50
    lines = path.read_text(encoding="ascii").splitlines()
    require(lines[-1:] == ["TIM035_Q1_DONE_TIM6_DISARMED"], "native disarm marker")
    header = lines[0].split(",")
    require(len(header) == 11 and header[:2] == ["Q1", "ADAPTIVE"]
            and header[9] == "1", "native identity or cleanup flag")
    ack = int(header[2])
    arm, disarm = int(header[6]), int(header[7])
    duration = (disarm - arm) / 1e9
    require(seconds - 0.002 < duration < seconds + 0.030, "active duration")
    windows = [line.split(",") for line in lines if line.startswith("W,")]
    commands = [line.split(",") for line in lines if line.startswith("C,")]
    renewals = [line.split(",") for line in lines if line.startswith("H,")]
    require(len(windows) == count + 550, "window inventory")
    require(len(commands) == count, "feedback command inventory")
    require(len(renewals) == count // 10, "watchdog renewal inventory")
    require(len(lines) == len(windows) + len(commands) + len(renewals) + 2,
            "unexpected record type")

    for index, window in enumerate(windows):
        require(len(window) == 10, "window field count")
        require(max(int(window[7]), int(window[8])) <= 262144, "microphone peak")
        if index:
            require(int(window[2]) == (int(windows[index - 1][2]) + 1) % TURN,
                    "window sequence")
            require(int(window[9]) > int(windows[index - 1][9]), "window time")

    def values(labels):
        return [complex(int(w[3]), int(w[4])) for w in windows if w[1] in labels]

    before = values(("SHAM", "PRE"))
    initial = values(("PRE",))
    active = values(("ACTIVE",))
    after = values(("POST",))
    require((len(before), len(initial), len(active), len(after))
            == (250, 100, count, 250), "period inventory")

    last = 0j
    for index, command in enumerate(commands):
        require(len(command) == 10 and int(command[1]) == index
                and int(command[4]) == (ack + index + 1) % TURN,
                "feedback index or acknowledgement")
        lower, upper = int(command[2]), int(command[3])
        require(index * 960 <= lower < upper <= index * 960 + 48
                and upper - lower <= 24, "feedback acknowledgement bracket")
        error = sum(initial) / 100 if index == 0 else active[index - 1]
        phase, gain = requested(last, error, rate, cap)
        distance = abs((int(command[5]) - phase + TURN // 2) % TURN - TURN // 2)
        require(int(command[6]) == int(command[8]) == gain
                and int(command[5]) == int(command[7]) and distance <= 1,
                f"applied command differs from replay at command {index}")
        require(arm <= int(command[9]) < disarm, "command outside active span")
        last = cmath.rect(int(command[8]), math.tau * int(command[7]) / TURN)

    previous = arm
    for index, renewal in enumerate(renewals):
        require(len(renewal) == 6 and int(renewal[1]) == index, "watchdog index")
        stamp, before_lease, after_lease, got_ack = map(int, renewal[2:])
        require(previous < stamp < disarm and stamp - previous < 300_000_000,
                "watchdog cadence")
        require(16_000_000 <= before_lease <= 98_304_000
                and 97_000_000 <= after_lease <= 98_304_000,
                "watchdog lease")
        require(got_ack == (ack + (index + 1) * 10) % TURN, "watchdog acknowledgement")
        previous = stamp

    pre_power, post_power = mean_power(before), mean_power(after)
    factor = 0.64 if seconds == 60 else 1.0
    reference = min(pre_power, post_power) * factor
    active_power = mean_power(active)
    require(reference > 0 and active_power > 0, "non-positive measured power")
    per_second = [mean_power(active[k:k + 50]) for k in range(0, count, 50)]
    qualifying = sum(power <= reference * 10 ** (-0.3) for power in per_second)
    drift = 10 * math.log10(post_power / pre_power)
    reduction = 10 * math.log10(reference / active_power)
    controls = abs(drift) <= 1.5
    accepted = controls and reduction >= 3 and (seconds == 10 or qualifying >= 54)
    return {
        "seconds": seconds,
        "active_seconds": duration,
        "initial_ack": ack,
        "final_ack": (ack + count) % TURN,
        "feedback_commands_replayed": count,
        "watchdog_renewals_verified": len(renewals),
        "before_5s_rms": math.sqrt(pre_power),
        "after_5s_rms": math.sqrt(post_power),
        "control_drift_db": drift,
        "controls_within_1_5_db": controls,
        "conservative_reference_rms": math.sqrt(reference),
        "active_rms": math.sqrt(active_power),
        "reduction_db": reduction,
        "rms_reduction_percent": 100 * (1 - math.sqrt(active_power / reference)),
        "seconds_at_least_3db_reduction": qualifying,
        "fraction_seconds_at_least_3db_reduction": qualifying / seconds,
        "per_second_rms": [math.sqrt(p) for p in per_second],
        "extension_eligible": seconds == 10 and reduction >= 3,
        "attenuation_demonstrated": accepted,
        "source_level_conservative_power_factor": factor,
        "all_recorded_live_checks_passed": True,
    }


def verify() -> dict:
    manifest = json.loads(local_file("evidence/manifest.json").read_text())
    require(manifest["schema_version"] == 1, "unsupported manifest version")
    expected_acceptance = {
        "control_drift_abs_db_max": 1.5,
        "mean_reduction_db_min": 3,
        "seconds_meeting_3db_min": 54,
        "total_seconds": 60,
        "conservative_reference_power_factor": 0.64,
    }
    require(manifest["sustained_acceptance"] == expected_acceptance,
            "manifest acceptance differs from the recorded criteria")
    require(manifest["calibration_complex"] == [CALIBRATION.real, CALIBRATION.imag],
            "manifest calibration differs from the source scorers")
    for name, expected_hash in manifest["published_file_sha256"].items():
        actual_hash = hashlib.sha256(local_file(name).read_bytes()).hexdigest()
        require(actual_hash == expected_hash.lower(), f"SHA-256 mismatch: {name}")

    summary = []
    for run in manifest["runs"]:
        review = json.loads(local_file(run["files"]["review"]).read_text())
        require(review["source_commit"] == run["source_commit"], "source identity")
        require(review["archive_sha256"].lower() == run["original_archive_sha256"],
                "archive identity")
        stages = {}
        for seconds in (10, 60):
            name = f"stage{seconds}"
            path = local_file(run["files"][name])
            require(hashlib.sha256(path.read_bytes()).hexdigest()
                    == review["target_member_sha256"][f"{name}.csv"].lower(),
                    f"{run['label']} {name}: original member hash")
            result = assess_span(path, seconds, run["correction_rate"], run["max_gain"])
            expected = review["recomputed"][name]
            require(result.keys() == expected.keys(), "review metric inventory")
            for key in expected:
                compare(result[key], expected[key], f"{run['label']} {name} {key}")
            stages[name] = result
        require(stages["stage10"]["extension_eligible"], "10-second extension criterion")
        require(stages["stage10"]["final_ack"] == stages["stage60"]["initial_ack"],
                "acknowledgement continuity between spans")
        header = local_file(run["files"]["stage60"]).read_text().splitlines()[0].split(",")
        start = (int(header[6]) - run["source_go_monotonic_ns"]) / 1e9
        end = (int(header[7]) - run["source_go_monotonic_ns"]) / 1e9
        require(26 <= start <= 33 and end < 99
                and all(start + 2 < t < end - 2 for t in (38, 53, 68, 83)),
                "nominal source events outside active span")
        compare([start, end], review["recomputed"]["active_source_relative_seconds"],
                f"{run['label']} source-relative interval")
        accepted = stages["stage60"]["attenuation_demonstrated"]
        compare(accepted, review["recomputed"]["sustained_local_200hz_iq_attenuation_demonstrated"],
                "sustained acceptance")
        summary.append({
            "run": run["label"],
            "rms_reduction_percent": stages["stage60"]["rms_reduction_percent"],
            "mean_attenuation_db": stages["stage60"]["reduction_db"],
            "one_second_intervals_reaching_3db": stages["stage60"]["seconds_at_least_3db_reduction"],
            "feedback_commands_replayed_total": sum(x["feedback_commands_replayed"] for x in stages.values()),
            "watchdog_renewals_verified_total": sum(x["watchdog_renewals_verified"] for x in stages.values()),
            "recorded_disarm_checks_passed": True,
            "sustained_attenuation_criterion_met": accepted,
        })
    return {"verification": "PASS", "scope": "offline consistency of selected records", "runs": summary}


def main() -> int:
    try:
        print(json.dumps(verify(), indent=2))
        return 0
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        print(f"Verification FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
