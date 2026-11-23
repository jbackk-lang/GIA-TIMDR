# RESULTS 019 — Matched controls for post-event signal decoding

Executed 2026-11-19 on 16 CWRU recordings, 50 windows of 2048 samples each. For each recording, select 5 highest crest-factor events from first 42 windows; match 5 controls without replacement on log RMS and temporal proximity. Fixed 80 matched pairs for lags 1, 2, 3, 5. Median absolute log RMS gap = 0.005; median time gap = 2 windows. Predict from subsequent window using leave-one-recording-out logistic regression with training-only StandardScaler.

Mean AUROC across recordings:

| Lag | RMS | FFT | Envelope | Phase | All |
|---|---:|---:|---:|---:|---:|
| 1 | 0.638 | 0.370 | 0.503 | 0.613 | 0.603 |
| 2 | 0.605 | 0.463 | 0.560 | 0.518 | 0.548 |
| 3 | 0.470 | 0.395 | 0.418 | 0.523 | 0.510 |
| 5 | 0.345 | 0.610 | 0.465 | 0.588 | 0.590 |

Bootstrap 95% CI, 4000 resamples of recordings: lag1 RMS [0.568,0.708], phase [0.538,0.685], all [0.525,0.685]. Lag2 RMS [0.505,0.705]. Lag5 RMS [0.286,0.404], suggesting possible reversed association rather than lasting memory.

**Conclusion:** The classical subsequent-window RMS performs best at lags 1 and 2 after approximate matching. No established additional value from phase or combined descriptors. Exploratory tests, multiple comparisons, imperfect matching, no causal identification, no independent replication, and no full CHF helix descriptors. AUCs are descriptive, not discovery evidence.

Reproduction: run `chf_stage_019.py` with `CWRU_CHF.zip` and `chf_stage_016.py`; full script and JSON are attached in the conversation. Next: locally stationary surrogates, stronger matching, preregistered lag1 confirmation.
