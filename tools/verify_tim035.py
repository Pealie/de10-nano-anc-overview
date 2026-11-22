#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Recompute the 21 November matched-pair attenuation from published RIGHT I/Q."""

import csv
import hashlib
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = Path("evidence/2026-11-21")
RUN_IDS = (
    "2a3d336d810f4917b68e6c830faac093",
    "4fff25db6f384751b9da13c8f4964387",
    "e42f6d3387874e65865781801ea7e9a5",
)
SECONDS = 60
WINDOWS_PER_SECOND = 50
THRESHOLD_DB = 3.0
REQUIRED_SECONDS = 54


def score(raw):
    rows = csv.reader(raw.decode("ascii").splitlines(), strict=True)
    if next(rows, None) != ["window", "ref_i", "ref_q", "adaptive_i", "adaptive_q"]:
        raise ValueError("unexpected CSV header")

    reference = [0] * SECONDS
    adaptive = [0] * SECONDS
    count = 0
    for row in rows:
        index, ref_i, ref_q, adaptive_i, adaptive_q = map(int, row)
        if index != count or index >= SECONDS * WINDOWS_PER_SECOND:
            raise ValueError(f"unexpected window {index} at row {count + 2}")
        second = index // WINDOWS_PER_SECOND
        reference[second] += ref_i**2 + ref_q**2
        adaptive[second] += adaptive_i**2 + adaptive_q**2
        count += 1
    if count != SECONDS * WINDOWS_PER_SECOND:
        raise ValueError(f"expected {SECONDS * WINDOWS_PER_SECOND} windows, found {count}")
    if min(reference) <= 0 or min(adaptive) <= 0:
        raise ValueError("one-second interval has zero energy")

    reference_total = sum(reference)
    adaptive_total = sum(adaptive)
    overall = 10 * math.log10(reference_total / adaptive_total)
    seconds_db = [10 * math.log10(r / a) for r, a in zip(reference, adaptive)]
    qualifying = sum(db >= THRESHOLD_DB for db in seconds_db)
    minimum = min(seconds_db)
    return {
        "attenuation_db": overall,
        "rms_reduction_percent": round(100 * (1 - math.sqrt(adaptive_total / reference_total)), 2),
        "qualifying_seconds": qualifying,
        "minimum_second_db": round(minimum, 3),
        "minimum_second_start": seconds_db.index(minimum),
        "accepted": overall >= THRESHOLD_DB and qualifying >= REQUIRED_SECONDS,
    }


def verify():
    manifest = json.loads((ROOT / EVIDENCE / "manifest.json").read_text(encoding="utf-8"))
    if manifest["acceptance"] != {
        "attenuation_db_min": THRESHOLD_DB,
        "seconds_meeting_3db_min": REQUIRED_SECONDS,
        "total_seconds": SECONDS,
        "windows_per_second": WINDOWS_PER_SECOND,
    }:
        raise ValueError("manifest differs from the matched-pair acceptance criteria")
    if tuple(run["run"] for run in manifest["runs"]) != RUN_IDS:
        raise ValueError("manifest differs from the three archived run identities")

    for run in manifest["runs"]:
        path = EVIDENCE / (run["run"] + ".csv")
        if run["path"] != path.as_posix():
            raise ValueError(f"unexpected measurement path for {run['run']}")
        raw = (ROOT / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != run["sha256"]:
            raise ValueError(f"SHA-256 mismatch for {path}")

        result = score(raw)
        expected = run["expected"]
        for name, value in result.items():
            if name == "attenuation_db":
                matches = math.isclose(value, expected[name], rel_tol=0.0, abs_tol=1e-10)
            else:
                matches = value == expected[name]
            if not matches:
                raise ValueError(f"{path}: {name} recomputed {value}, recorded {expected[name]}")

        start = result["minimum_second_start"]
        verdict = "PASS" if result["accepted"] else "FAIL"
        print(f"{run['label']}: {result['attenuation_db']:.6f} dB, "
              f"{result['rms_reduction_percent']:.2f}% RMS reduction, "
              f"{result['qualifying_seconds']}/{SECONDS} qualifying intervals, "
              f"minimum {result['minimum_second_db']:.3f} dB at {start}-{start + 1} s, "
              f"acceptance {verdict}")


if __name__ == "__main__":
    try:
        verify()
    except (OSError, csv.Error, ValueError, KeyError, TypeError, OverflowError) as error:
        sys.exit(f"Verification failed: {error}")
