# Provenance and publication scope

## Snapshot identity

- Overview date: **8 November 2026**, Europe/London.
- Experimental close-out: **5 November 2026**, covering the 4–5 November session.
- Authoritative development repository: `Pealie/active_noise_cancellation` (private).
- Research milestone: `c14634648633aa681fce9d8195fe0e75c904c58c`.
- Photograph source revision: `4ee3f48f5b7e90a78feb532ce30c4b6e7a3b0c30`.

The private source identifiers support provenance for authorised readers. Every file needed by this overview's offline verifier is included in this repository; public verification does not require access to the private repository.

## Selected material

| Public material | Source and treatment |
| --- | --- |
| Four `stage10.csv` / `stage60.csv` files | Byte-for-byte extraction from each original return archive's `target.zip`; member hashes match the retained source reviews |
| Two `review.json` files | Byte-for-byte copies of the run-specific `TIM035_RIGHT_SUSTAIN_*_REVIEW.json` files at the research milestone |
| `docs/images/anc-bench-2026-11-07.jpg` | Resized JPEG derivative, 640 × 480 pixels, from the photograph source revision; original source Git blob `eb806ec35bec3011225e5ceea18a1a52d649ed14` |
| `LICENSE` | Byte-for-byte copy of the source root licence; source Git blob `f288702d2fa16d3cdf0035b15a9fcbc552cd88e7` |
| Overview, architecture, results and explanatory text | Newly composed from the dated source records; selective summary rather than a copy of the development README |
| `tools/verify_results.py` | New standard-library implementation of the matching source scoring and command-replay algorithms; compares all span metrics against the retained reports |
| Run source-start timestamps | Selected fields from each archived `target.zip/board.json`; complete board inventory files are excluded |

The source reports are preserved as historical records, including their verdicts and proposed next settings. A proposed experiment in one report does not establish that it subsequently succeeded.

## Photograph derivative

On 8 November 2026, the overview photograph was reduced from **1536 × 1152** to **640 × 480 pixels**, retaining the complete frame at approximately 41.7% of each original dimension. The derivative was produced directly from the original source image. ImageMagick 7.1.1-43 applied Lanczos downsampling and progressive JPEG encoding at quality 90 with 4:2:0 sampling. EXIF metadata was removed; the source ICC colour profile was preserved. No crop or scene alteration was applied.

The file size fell from **624,231** to **90,570 bytes**. The original remains identified by the pinned source revision and Git blob above. The derivative's SHA-256 and transformation details are recorded in [evidence/manifest.json](../evidence/manifest.json).

## Original archive identities

**Run A**

- Run: `3b5ff096e5a4471eb1f530e561d75fdf`.
- Source commit: `fda45dee428c29ec1c013ddbe4ab27414e30d705`.
- Original archive: `TIM035_RIGHT_SUSTAIN_3b5ff096e5a4471eb1f530e561d75fdf.zip`.
- Archive bytes: 754,650.
- Archive SHA-256: `8c6db4e0ef800e4e345e49a21280e530b73c6861d40c3c81c024a2cdfda5832b`.
- Controller settings: correction rate 0.08; gain ceiling 64.

**Run B**

- Run: `5c7b6767b3b3456aa77a6703db0f94d9`.
- Source commit: `1b487fe62c1ecef2e7a2e0dba12bf10baf28cf9c`.
- Original archive: `TIM035_RIGHT_SUSTAIN_5c7b6767b3b3456aa77a6703db0f94d9.zip`.
- Archive bytes: 756,058.
- Archive SHA-256: `a55b6cb8a5c0493066d3f73d439ce372fcd720243540c76d8b7543af6248bbf9`.
- Controller settings: correction rate 0.16; gain ceiling 96.

The complete original archives remain in the private engineering record. Their hashes are identities, not publicly downloadable evidence in this overview. The extracted measurements needed for the selected replay are available here.

## Replay source identities

At each experiment's source commit, the original scoring paths are:

- `tools/tim035_right_sustain_score.py`.
- `tools/tim035_right_iq_score.py`.

The sustained scorer uses the matching run's settings. The shared I/Q scorer has source Git blob `2f70bcfa5edf0ba9d613f16a549660fba7cade56`. The Run A sustained scorer has blob `3be36a8715e9867cb4c8dd64464af7cacfb013ab`; the Run B version has blob `0283cdeb58c5d4e5c2591195c27e3870d0c74f1a`.

The new verifier substitutes Python standard-library arithmetic for NumPy. It checks the original member hashes, replays every command and watchdog renewal, then compares the resulting metrics with the retained reports using stated numerical tolerances. This is a computational consistency check, not an independent acoustic experiment.

## Hashes, privacy and maintenance

[evidence/manifest.json](../evidence/manifest.json) records SHA-256 hashes for the published files other than the manifest itself. Self-exclusion avoids a recursive hash. The Git commit identifies the complete publication, including the manifest. Hashes protect against unnoticed changes within the selected snapshot; they are not an external signature or proof of measurement accuracy.

The publication excludes credentials, host configuration, controller binaries, programming images, raw audio recordings, the complete board inventories and the development Git history. The published photograph is a resized JPEG derivative with EXIF metadata removed and its original ICC colour profile retained. Numeric logs and retained review reports were reviewed for private contact details and credentials before publication.

Future updates should add dated evidence and revise the README, results and manifest together. Existing raw records and their original verdicts remain preserved. [Update procedure](../CONTRIBUTING.md)
