# RESULTS 033 — Local adjustment of event interval–amplitude association

Executed on 16 real CWRU vibration recordings in `CWRU_CHF.zip`, each truncated to 120 × 2048 samples. Event definition matches stage 032: peaks in absolute acceleration above each recording's 99.5th percentile, separated by at least 32 samples. Correlate log inter-event interval with log amplitude of the subsequent peak.

Local adjustment: regress both variables on an intercept, log RMS in the current 16,384-sample block, log count of detected peaks in that block, and normalized block position; compute correlation between residuals. Use 1,000 amplitude-order permutations within each block for per-recording null diagnostics. Aggregate 16 recording-level correlations with 20,000 sign flips. Seed 20261120.

| Statistic | Raw | Locally adjusted |
|---|---:|---:|
| Mean recording correlation | +0.035954 | +0.040877 |
| Two-sided recording-level sign-flip p | 0.084596 | 0.047198 |
| Positive recording-level correlations | 11/16 | 12/16 |

Within-block shuffle diagnostics: median per-recording p=0.2737; only 3/16 recordings individually have p<0.05. Thus the weak aggregate signal is not a consistently strong within-recording result.

**Interpretation:** exploratory small positive association, not a validated discovery. p=0.0472 is uncorrected for many prior analyses and the selected hypothesis; blockwise covariates are estimated from the same data; residualization and peak thresholding can introduce selection artifacts. Shuffling within blocks does not reproduce all mechanical dependencies. Independent external recordings and pre-specified tests are required. No evidence of novel memory, echo, beating, or CHF incremental value.

Code: `chf_stage_033.py`. JSON: `CHF_AFTER_EVENT_033.json`.