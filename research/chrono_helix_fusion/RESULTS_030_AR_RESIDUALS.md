# RESULTS 030 — AR(8) residual structure after strong impulses

Executed on 2026-11-19 using the real local CWRU_CHF.zip, 16 recordings, 48 crest-factor-event versus pre-event-RMS-matched-control pairs (three per recording, inherited from stage 025).

For each event/control, extract 320 continuous samples after the local peak. Fit ridge AR(8) on the first 160 samples, and compute one-step held-out prediction residuals on samples 160–319 using observed recent samples. Analyze residual autocorrelation squared mean over lags 1..20; squared-residual autocorrelation squared mean over lags 1..20; and absolute residual skewness. Compare event minus control; 20,000 paired sign flips at recording level and recording-level bootstrap CIs.

| Measure | Event-control mean | Two-sided p | 95% bootstrap CI | Positive recordings |
|---|---:|---:|---|---:|
| AR8 residual autocorrelation energy | +0.00379525 | 0.56752 | [−0.008548, +0.016731] | 8/16 |
| AR8 residual squared-autocorrelation energy | +0.00513475 | 0.21134 | [−0.000774, +0.012563] | 10/16 |
| AR8 residual absolute skewness | −0.0507059 | 0.12809 | [−0.114444, +0.006223] | 2/16 |

**Interpretation:** no statistically persuasive event-specific AR residual structure under these exploratory metrics. Absolute residual skewness is lower after events in 14/16 recordings, but effect-size sign-flip p=0.128 and bootstrap interval crosses zero; not a validated effect. Three outcomes tested without multiple-comparison adjustment. One-step AR residual whiteness does not test long-term memory. The event peak magnitude is not matched, and this is a single bearing dataset. No novel echo, CHF, or new physics claim.

Reproducible code: `chf_stage_030.py`. Machine-readable results: `CHF_AFTER_EVENT_030.json`. Execute `python chf_stage_030.py CWRU_CHF.zip` with stage 025 and stage 029 modules present.

Next: independent confirmation of asymmetry effect using different recordings or alternate datasets, plus amplitude-matched controls; do not tune to this result on the same sample.
