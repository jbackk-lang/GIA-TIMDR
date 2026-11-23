# RESULTS 029 — AR(2) damped-oscillator proxy vs AR(8), held-out next-sample prediction

Executed 2026-11-19 on local real CWRU_CHF.zip: 16 recordings, 48 matched event/control pairs, inherited event selection and RMS matching from stage 025.

For each pair locate maximum absolute acceleration peak in event/control window, extract **320 continuous samples** following the peak (crossing window boundaries), normalize by pre-peak local SD, subtract mean of first 160 samples. Fit ridge AR(2) and AR(8) on samples 0–159, validate one-step predictions on samples 160–319 using observed lagged values. AR(2) stable complex characteristic roots serve as a *damped-oscillator proxy*; this is not a physically identified echo.

Recording-level paired differences and two-sided sign-flip tests (20,000 flips over 16 recordings), recording-level bootstrap CIs:

| Measure (event − control) | Mean | p | 95% bootstrap CI |
|---|---:|---:|---|
| log MSE(AR2)/MSE(AR8) | −0.0081456 | 0.83226 | [−0.08258,0.06597] |
| log MSE(AR2)/MSE(persistence) | +0.0431413 | 0.34078 | [−0.03757,0.12864] |
| fraction stable complex AR2 roots | 0 | 1.0 | [0,0] |
| log MSE(AR8)/MSE(persistence) | +0.0512869 | 0.42073 | [−0.05814,0.17261] |

Both event and control AR2 fits had stable complex roots in 100% of analyzed segments. AR8 improves on AR2 in both groups (mean log AR2/AR8 MSE ~0.725 events, ~0.733 controls), without a distinctive event-specific effect.

**Interpretation:** no evidence of event-specific oscillator predictability or extra memory beyond conventional AR models in these simple metrics. Limitations: one-step forecast with observed recent samples is not long-horizon memory; peak amplitudes not matched; exploratory 4 outcomes and no multiplicity adjustment; no CHF features or independent dataset; complex roots do not prove a physical echo.

Local executable: `chf_stage_029.py`. Local JSON: `CHF_AFTER_EVENT_029.json`.
