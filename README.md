# DE10-Nano active noise cancellation

Independent engineering and research into adaptive control of low-frequency sound, combining FPGA signal processing, embedded Linux and acoustic experiments.

**Three 60-second runs on three distinct board boots reduced the tracked tone near 200 Hz by 7.55, 9.03 and 10.14 dB at the marked RIGHT microphone.** The best minute on 24 November 2026 gave a **68.9% reduction in target-tone RMS**. Across the three minutes, all **180/180 one-second intervals** exceeded 3 dB.

<p align="center">
  <img src="docs/images/anc-bench-2026-11-07.jpg" alt="Experimental bench with two microphones, the secondary loudspeaker and amplifier, and the DE10-Nano beside the laptop." width="75%">
</p>

*Bench photograph, 7 November 2026. The laptop generates the external test tone. The Audio Mini acquires both MAX4466 microphones. RIGHT supplies the feedback error. The photograph predates both matched-pair series.*

## Experimental results

On 24 November the laptop played the same near-200 Hz programme in each source-only minute and its paired adaptive minute. A change of 30° in source phase took 20 ms. The secondary loudspeaker was 5 cm from the RIGHT microphone. Playback level, geometry and controller settings were fixed within each pair.

| 24 November start | Overall attenuation | Target-tone RMS reduction | Seconds ≥3 dB | Weakest second |
| --- | ---: | ---: | ---: | ---: |
| 1 | 7.55 dB | 58.07% | 60/60 | 5.57 dB |
| 2 | 9.03 dB | 64.64% | 60/60 | 6.91 dB |
| 3 | 10.14 dB | 68.87% | 60/60 | 8.22 dB |

The sustained target was first met on 21 November. With abrupt source phase changes, three starts across two boots measured **5.64, 6.15 and 5.70 dB** and all 180 seconds exceeded 3 dB. The microphone ground was repaired between the two series. The 4–5 November runs measured 2.28 and 2.23 dB using an earlier reference method. [Results, comparison plot and scoring](docs/results.md)

## System and engineering work

The platform uses a Terasic DE10-Nano, Audio Mini codec, two MAX4466 microphone modules, an amplifier and a secondary loudspeaker. FPGA logic measures the tone and generates the secondary signal; an embedded C controller on the ARM/Linux side adjusts it. Acquisition uses both microphones; the demonstrated controller uses RIGHT feedback.

The work spans FPGA audio acquisition, coherent I/Q measurement, embedded control, Linux audio integration, acoustic-path calibration and reproducible experiment design. [System architecture](docs/system-overview.md)

## Measurement scope

The measurements establish repeatable attenuation of the tracked tone at one microphone position on this bench. Broadband attenuation, spatial coverage and perceived loudness remain unmeasured. Each source-only minute preceded its adaptive minute, and the measured reference level varied across starts. An adaptive-versus-fixed-command comparison and replication on another bench remain open.

## Explore the evidence

- [Results, reference calculation and measurement scope](docs/results.md)
- [Measurement data and offline verification](evidence/README.md)
- [Source identities and publication scope](docs/provenance.md)
- [Licence and attribution](NOTICE.md)

```sh
python tools/verify_results.py
python tools/verify_tim035.py
```

Both commands run offline with Python 3.10 or later and the standard library. The first replays the 4–5 November experiments. The second scores the six matched pairs from 21 and 24 November using the published RIGHT I/Q measurements.

Project: **Neil Thomson**. Independent adviser: **Bruce W. Thomson**.

Released under the [GNU General Public License, version 3](LICENSE). See [NOTICE.md](NOTICE.md) for scope and attribution.
