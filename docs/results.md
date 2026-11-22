# Experimental results and limitations

## Matched-pair results, 21 November 2026

Three separately started 60-second experiments met the sustained target at the marked RIGHT microphone. Each adaptive minute was scored against a dedicated source-only minute with zero secondary command and the same programmed changes in amplitude, phase and frequency near 200 Hz.

| Start | Board boot | Overall attenuation | Target-tone RMS reduction | Intervals ≥3 dB | Weakest one-second interval |
| --- | --- | ---: | ---: | ---: | --- |
| First | Original | 5.636460 dB | 47.74% | 60/60 | 3.209 dB at 50–51 s |
| Repeat | Original | 6.146639 dB | 50.72% | 60/60 | 5.410 dB at 49–50 s |
| After reboot | Fresh | 5.695801 dB | 48.09% | 60/60 | 4.820 dB at 0–1 s |

Each minute supplied 3,000 RIGHT I/Q windows of 20 ms. For a matched set of windows, let $E_r$ and $E_a$ be the sums of $I^2+Q^2$ over the source-only reference and adaptive recordings respectively. Overall attenuation is $10\log_{10}(E_r/E_a)$ and RMS amplitude reduction is $100(1-\sqrt{E_a/E_r})$ per cent. The same calculation over each corresponding block of 50 windows gives the one-second scores. The decision uses the unrounded scores. Each start required at least 3 dB overall and at least 54 of 60 individual seconds at or above 3 dB.

The source-only minute preceded the adaptive minute in each pair. The operator recorded laptop playback at 80%, a 5 cm distance from secondary loudspeaker to RIGHT, and fixed settings within each pair. The digital gain ceiling was 20. The first two starts shared a board boot. The third ran on the same board after a reboot, with its boot identity confirmed against the operator’s pre-run record. The source records report 3,000 adaptive commands and 300 watchdog renewals per adaptive minute, with final disarm in all six traces. The [public extracts](../evidence/README.md) support numerical replay of attenuation. The boot and controller checks come from the source records.

## Earlier experiments, 4–5 November 2026

Both runs sustained feedback while the external source changed. Both missed the attenuation criterion then in force.

| Quantity | Run A | Run B |
| --- | ---: | ---: |
| Run identifier | `3b5ff096e5a4471eb1f530e561d75fdf` | `5c7b6767b3b3456aa77a6703db0f94d9` |
| Correction rate | 0.08 | 0.16 |
| Digital gain ceiling | 64 | 96 |
| 60-second active duration | 60.00344489 s | 60.00347264 s |
| Conservative reference RMS | 63,552.2261 | 73,206.4231 |
| Active RMS | 48,889.8967 | 56,648.3452 |
| RMS amplitude reduction | 23.0713% | 22.6183% |
| Mean power attenuation | 2.2782 dB | 2.2272 dB |
| One-second intervals reaching 3 dB | 28 / 60 | 22 / 60 |
| Control drift | 0.9006 dB | 0.6763 dB |
| Applied commands replayed in 60-second span | 3,000 | 3,000 |
| Watchdog renewals verified in 60-second span | 300 | 300 |
| Recorded final disarm | Confirmed | Confirmed |
| Full sustained attenuation criterion | Not met | Not met |

RMS values use the digital I/Q scale. Absolute values are not acoustic SPL. Each experiment also included a preceding ten-second check: Run A achieved 37.4288% RMS reduction / 4.0725 dB; Run B achieved 35.0946% / 3.7544 dB. Both ten-second checks met their own extension criterion. These checks used a different reference factor from the subsequent 60-second spans and should not be compared as though the scoring were identical.

Across the ten-second and sixty-second spans combined, each experiment contains 3,500 feedback commands and 350 watchdog renewals. Counts of 3,000 / 300 refer specifically to the sixty-second span.

### 4–5 November source programme

The acoustic source ran for approximately 100 seconds per experiment. The following nominal events occurred inside each continuous sixty-second active interval:

| Time from source start | Programmed change |
| --- | --- |
| 38 s | Amplitude factor 0.8; phase step +30 degrees |
| 53 s | Frequency changes to 200.1 Hz |
| 68 s | Amplitude factor 1.0; phase step −30 degrees |
| 83 s | Frequency returns to 200.0 Hz |

The retained timing metadata places the active interval at source-relative 28.5477–88.5511 s for Run A and 28.5586–88.5621 s for Run B. The offline replay checks that the nominal events lie within those intervals. Their physical acoustic waveform is not independently established by the event schedule alone.

### 4–5 November scoring

Let $z_k=I_k+jQ_k$ be the complex measured target component. Its squared magnitude is $I_k^2+Q_k^2$. Power is averaged before conversion to decibels.

```math
P_{\mathrm{active}} = \frac{1}{N} \sum_{k=1}^{N} (I_k^2 + Q_k^2)
```

Here $N$ is the number of active I/Q windows: 3,000 in a sixty-second span.

For the sixty-second span, the reference is 64% of the smaller power in the two bracketing five-second zero-drive controls:

```math
P_{\mathrm{ref}} = 0.64 \min(P_{\mathrm{before}}, P_{\mathrm{after}})
```

This reduces the reference amplitude to 80% of the smaller bracket RMS and accounts conservatively for the programmed source-amplitude reduction. The ten-second check uses a power factor of 1.0.

```math
A_{\mathrm{dB}} = 10 \log_{10} \left(\frac{P_{\mathrm{ref}}}{P_{\mathrm{active}}}\right)
```

```math
R_{\mathrm{RMS}} = 100 \left(1 - \sqrt{\frac{P_{\mathrm{active}}}{P_{\mathrm{ref}}}}\right)
```

The full sustained criterion requires all three conditions:

1. At least 3 dB attenuation from the mean active power.
2. At least 54 of the 60 one-second intervals individually reaching 3 dB against the same reference.
3. Absolute drift between the bracketing controls no greater than 1.5 dB.

Both experiments met the control-drift condition and missed the two attenuation conditions. An average of per-second decibel values is not the formal mean score.

## Limits on interpretation

- Attenuation is local and tone-specific. The digital RIGHT I/Q measurements describe the tracked component at one position. Spatial extent, broadband benefit and perceived loudness reduction have not been established.
- On 4–5 November, two different settings were each run once. The background differed, so the figures do not establish improvement or equivalence between the settings.
- The 4–5 November analyses recorded frequent gain-ceiling operation and a nearby residual component. A nearby component also appeared before laptop playback; its physical origin remains unconfirmed.
- All three 21 November pairs used the same apparatus and marked position. Separate scoring and one reboot establish within-bench repeatability. Independent laboratory replication and calibrated sound-pressure measurements remain open.
- A source-only comparator measures the effect of enabling adaptive control. Estimating an advantage over a fixed command requires a fixed-command trial under matched conditions. The common reference-first order leaves possible time effects unseparated. Differences in reference method and drive settings limit direct comparisons between dates.
- Complete end-to-end latency, full electrical timing, calibrated SPL and analogue fault containment remain separate qualification tasks.
- The earlier approximately 73% short-duration figure belongs to a different fixed-tone experiment and geometry. Its original records are outside this selected public evidence set; it is not a sixty-second sustained result.

## Historical preflight stop, 5 November

The subsequent 0.32-rate / 128-count controller revision passed its reported offline cases, but its physical attempt stopped during preflight before the amplifier-ON prompt or playback. The exact timeout cause was not established by the returned archive. That revision has no new physical attenuation result.

The three scored 21 November starts form a later campaign with a matched source-only reference for each adaptive minute.

[Replay these measurements](../evidence/README.md) · [Provenance](provenance.md)
