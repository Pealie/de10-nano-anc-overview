# Selected evidence and offline replay

This directory contains the original ten-second and sixty-second numeric records for the two completed 4–5 November 2026 experiments, together with their retained review reports. The raw `.csv` files are mixed record logs, not ordinary spreadsheets with one uniform row schema.

| Run | Original numeric records | Retained source review |
| --- | --- | --- |
| A | [stage10.csv](2026-11-05/3b5ff096e5a4471eb1f530e561d75fdf/stage10.csv), [stage60.csv](2026-11-05/3b5ff096e5a4471eb1f530e561d75fdf/stage60.csv) | [review.json](2026-11-05/3b5ff096e5a4471eb1f530e561d75fdf/review.json) |
| B | [stage10.csv](2026-11-05/5c7b6767b3b3456aa77a6703db0f94d9/stage10.csv), [stage60.csv](2026-11-05/5c7b6767b3b3456aa77a6703db0f94d9/stage60.csv) | [review.json](2026-11-05/5c7b6767b3b3456aa77a6703db0f94d9/review.json) |

[manifest.json](manifest.json) records file hashes, source identities, controller parameters and the selected source-start timestamps needed for chronology checks. The four numeric files are byte-for-byte extractions from the verified original archives. No hardware launchers or deployment binaries are included.

## Recompute

From the repository root:

```sh
python tools/verify_results.py
```

Python 3.10 or later is sufficient. No package installation, network connection or hardware access is required. A verification failure returns a non-zero exit code.

The verifier checks:

- Published file SHA-256 hashes against the manifest.
- Window inventory, sequence, peak bounds and monotonic recorded time.
- Each requested and applied feedback command using the matching run's correction rate and gain ceiling, recorded quantisation and complex calibration coefficient.
- Command acknowledgements, active duration, watchdog cadence and recorded lease renewals.
- RMS/power arithmetic, control drift and one-second acceptance counts for both spans.
- Continuity between the two spans and the nominal source-event positions inside the sixty-second active interval.
- The native completion/disarm markers and agreement with the retained review metrics.

The verifier has no code path for hardware access. Checks establish consistency of the retained records; they cannot independently prove the physical sound field, clock calibration, electrical safety or authenticity of the original acquisition.

## Record format

| Prefix | Contents |
| --- | --- |
| `Q1,ADAPTIVE` | Span identity, initial acknowledgement, recorded arm/disarm times and cleanup flag |
| `W` | Labelled I/Q window, sequence number, peak values and monotonic timestamp |
| `C` | Requested and applied drive phase/gain, acknowledgement bracket and timestamp |
| `H` | Watchdog renewal index, timestamp, lease values and acknowledgement |
| `TIM035_Q1_DONE_TIM6_DISARMED` | Native completion marker |

`SHAM` and `PRE` together form the five-second pre-control bracket; `PRE` supplies the initial feedback estimate. `ACTIVE` contains 50 windows per second. `POST` forms the five-second post-control bracket.

## Publication boundaries

The complete original archives, WAV, build logs and controller binaries are retained in the private research record. This selection preserves the numeric records needed for the public replay and identifies the original archives by hash. Only the source-start timestamp has been selected from each board record; host and board inventory files have not been copied.

The word “independent” in the retained source reports describes separate software recomputation. It does not claim independent laboratory replication or external human peer review. The reports also retain the parameters and proposed next trial as recorded at that time; those proposals are historical, not new experimental results.

[Scoring and limitations](../docs/results.md) · [Provenance](../docs/provenance.md)
