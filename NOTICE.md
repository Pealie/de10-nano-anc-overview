# Licence, attribution and publication scope

## Licence

This overview retains the source project's **GNU General Public License, version 3**. The complete licence is provided in [LICENSE](LICENSE). Unless a file states otherwise, the original overview text, diagram, verification scripts, selected project records, results figure and bench photograph are distributed under that licence. The verification scripts use the identifier `GPL-3.0-only`.

The Free Software Foundation copyright line in the licence text identifies the author of that licence document; it does not identify the author of the engineering project.

This licence choice applies to the material included here. It does not relicense excluded vendor source, commercial hardware, manuals, published research or the entire private development archive. The source project's separately identified MIT-licensed FPGA package is not included in this overview. Third-party names and trade marks identify equipment and carry no implication of endorsement.

## Attribution

- Project and overview: Neil Thomson.
- Independent adviser: Bruce W. Thomson.
- Bench photograph: supplied by Neil Thomson; taken 7 November 2026. The overview uses a resized 640 × 480 pixel JPEG; the original source identity and transformation are recorded in [docs/provenance.md](docs/provenance.md).
- Original measurement records and review reports: selected from Neil Thomson's `Pealie/active_noise_cancellation` project at the source identities recorded in [docs/provenance.md](docs/provenance.md).
- The [24 November results figure](docs/images/tim035-three-boots.png) reproduces the three-start comparison from the project’s dated evidence record.
- The 4–5 November verifier implements the source project’s `tim035_right_sustain_score.py` and `tim035_right_iq_score.py` algorithms. The matched-pair verifier recomputes attenuation from selected RIGHT I/Q records for 21 and 24 November. Both use Python’s standard library and retain the project licence.

No third-party driver, vendor RTL, hardware manual, live controller, launcher, programming image or account credential is included.

## Evidence status

The public records support attenuation replay for all three experimental series. The 4–5 November logs also support replay of applied commands, watchdog renewals and final disarm. The 21 and 24 November extracts contain the paired measurements used for acoustic scoring. Independent acoustic replication and product qualification remain open.

Hashes identify retained bytes and support comparison with source records. A hash does not establish that a physical measurement was accurate. The scope and limitations in [docs/results.md](docs/results.md) form part of the interpretation of the published figures.
