# RESULTS 032 — Event-order memory and permutation controls

Executed on 16 real CWRU vibration recordings in `CWRU_CHF.zip`. Per recording, analyze up to 120 windows of 2048 samples, identify absolute-amplitude peaks above the recording's 99.5th percentile, with minimum spacing 32 samples. Measure (1) lag-one correlation between successive log inter-peak intervals and (2) correlation between log interval and log amplitude of the following peak.

Nulls: 2000 within-recording random permutations per measure; aggregate inference via 20,000 sign flips over the 16 recording-level correlation coefficients. All tests exploratory and two-sided.

| Measure | Recording mean Pearson r | Aggregate two-sided p | Positive recordings |
|---|---:|---:|---:|
| Successive log inter-event intervals | -0.0316393 | 0.129444 | 5/16 |
| Log interval vs next-event log amplitude | +0.0359536 | 0.086796 | 11/16 |

**Conclusion:** Neither measure supplies persuasive evidence of event-order memory. The interval-amplitude association is small and exploratory. Shuffling destroys local nonstationarity and does not control mechanical periodicity; no correction for testing two hypotheses; recordings from one dataset are not independent external replication. This experiment does not establish novel physical information, echo, beating, or incremental CHF performance.

Reproduce: `python chf_stage_032.py CWRU_CHF.zip`. Machine-readable full results: `CHF_AFTER_EVENT_032.json`.