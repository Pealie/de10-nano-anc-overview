# DE10-Nano active noise cancellation

Independent engineering and research into adaptive control of low-frequency sound, combining FPGA signal processing, embedded Linux and acoustic experiments.

**Demonstrated:** two continuous 60-second adaptive-feedback runs while an external tone changed in level, phase and frequency around 200 Hz. Local target-tone RMS amplitude fell by **23.07%** and **22.62%** against the conservative reference.

**Next milestone:** at least 3 dB mean attenuation, with 54 of 60 one-second intervals reaching 3 dB.

*Evidence snapshot: 5 November 2026. Overview prepared: 8 November 2026.*

<p align="center">
  <img src="docs/images/anc-bench-2026-11-07.jpg" alt="Experimental bench with two microphones, the secondary loudspeaker and amplifier, and the DE10-Nano beside the laptop." width="75%">
</p>

*Bench photograph, 7 November 2026. The laptop supplies the acoustic disturbance. Both MAX4466 microphones feed the Audio Mini; the RIGHT microphone supplies the feedback error. The photograph shows the later bench arrangement, recorded two days after the reported runs.*

## Experimental results

| Physical experiment | Active feedback | Target-tone RMS reduction | Mean attenuation | One-second intervals reaching 3 dB |
| --- | ---: | ---: | ---: | ---: |
| Run A: correction rate 0.08, gain ceiling 64 | 60.003 s | 23.07% | 2.28 dB | 28 / 60 |
| Run B: correction rate 0.16, gain ceiling 96 | 60.003 s | 22.62% | 2.23 dB | 22 / 60 |

Both runs maintained feedback throughout the programmed source changes and ended disarmed. Separate software replays checked the applied feedback commands and watchdog renewals. The selected original measurements and offline replay are included here.

The sustained target requires **at least 3 dB mean attenuation and 54 of 60 one-second intervals reaching 3 dB**, with the control measurements within the permitted drift. Three decibels corresponds to approximately 29% RMS amplitude reduction. These criteria govern the next physical comparison.

## System and engineering work

The platform uses a Terasic DE10-Nano, Audio Mini codec, two MAX4466 microphone modules, an amplifier and a secondary loudspeaker. FPGA logic measures the tone and generates the secondary signal; an embedded C controller on the ARM/Linux side adjusts it. Acquisition uses both microphones; the demonstrated controller uses RIGHT feedback.

The work spans FPGA audio acquisition, coherent I/Q measurement, embedded control, Linux audio integration, acoustic-path calibration and reproducible experiment design. [System architecture](docs/system-overview.md)

## Measurement scope and next experiment

The reported percentages quantify target-tone RMS amplitude reduction at the RIGHT microphone position. Assessments of perceived loudness, spatial coverage and broadband performance require dedicated measurements. Qualification priorities include timing, calibrated acoustic output, repeatability and wider operating conditions.

The next experiment covers diagnosis of the recorded preflight stop, verification of progress reporting and timeout handling, and a bounded attenuation comparison against the stated criteria.

## Explore the evidence

- [Results, reference calculation and measurement scope](docs/results.md)
- [Original data and offline verification](evidence/README.md)
- [Source identities and publication scope](docs/provenance.md)
- [Licence and attribution](NOTICE.md)

```sh
python tools/verify_results.py
```

The verifier runs offline on local evidence files using Python 3.10 or later and the standard library. This overview presents experimental results, supporting evidence and engineering documentation.

Project: **Neil Thomson**. Independent adviser: **Bruce W. Thomson**.

Released under the [GNU General Public License, version 3](LICENSE). See [NOTICE.md](NOTICE.md) for scope and attribution.
