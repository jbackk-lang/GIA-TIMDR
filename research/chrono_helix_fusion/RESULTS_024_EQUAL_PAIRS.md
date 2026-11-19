# RESULTS 024 — Equal-count matched controls versus IAAFT

2026-11-19. Actual local execution on `CWRU_CHF.zip` (16 CWRU recordings, first 50 windows × 2048 samples). For each recording, select 5 strongest crest-factor events among first 42 windows, optimally match controls by pre-event log RMS with small time penalty, then retain **exactly 3 closest matched pairs**. The same procedure is repeated on each of 12 whole-record IAAFT surrogate datasets (12 iterations, seed 20261122). This fixes the unequal number of matched pairs identified in RESULTS_023.

**Statistic:** fraction of matched pairs where RMS in the *next* window is greater after the event than after the control. This is a simple directional fraction, **not AUROC** and not a CHF measure.

| Measure | Result |
|---|---:|
| Recordings | 16 |
| Matched pairs per dataset | 48 |
| Real fraction positive | 0.3125 (15/48) |
| Real fraction negative | 0.6875 (33/48) |
| IAAFT mean fraction positive | 0.44618 |
| IAAFT range | [0.3125, 0.54167] |
| One-sided Monte Carlo p for low fraction | 0.15385 (2/13) |
| Two-sided p relative to 0.5 | 0.15385 |
| Real median absolute pre-event log RMS gap | 0.0004374 |
| Real 90th-percentile gap | 0.0014290 |

**Conclusion:** Equalizing pair count does not eliminate the negative direction of next-window RMS after selected impulses, but the 12-surrogate ensemble does not provide convincing statistical evidence. IAAFT may disrupt familiar transients/nonstationarity. Matching quality can still differ even when pair counts agree. No proof of physical memory, novel information, or CHF superiority.

Reproduce: `python chf_stage_024.py CWRU_CHF.zip`; requires `chf_stage_021.py`, numpy, scipy, scikit-learn. Complete code and JSON were generated and verified locally. Next: compare matching-gap distributions, larger surrogate ensemble, locally stationary controls and preregistered external dataset.
