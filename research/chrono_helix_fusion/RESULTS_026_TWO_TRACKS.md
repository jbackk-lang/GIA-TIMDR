# RESULTS 026 — Two tracks: beat consistency and independent time asymmetry

Executed 2026-11-19 on CWRU_CHF.zip: 16 recordings, 48 matched event/control pairs from stage 025. Measurements in next window. 20,000 recording-level sign-flip permutations and 20,000 recording bootstrap replicates.

| Metric | Mean paired difference | Two-sided p | Bootstrap 95% CI |
|---|---:|---:|---|
| Pair of spectral peaks spaced by envelope peak bin | -0.003137 | 0.81336 | [-0.02901,0.02173] |
| Envelope spectrum peak prominence | -0.17667 | 0.56897 | [-0.74517,0.40995] |
| Normalized increment skewness (independent time-asymmetry line) | +0.005560 | 0.57217 | [-0.01257,0.02472] |

**Conclusion:** None of these metrics provides persuasive evidence for a special post-impulse effect. Earlier envelope autocorrelation enhancement does not establish physical beating of two nearby modes. Increment skewness is a classical, incomplete measure of time irreversibility; no effect here.

**Limitations:** exploratory tests, no multiplicity correction, short 2048-sample spectral resolution, harmonic spectral peaks can mimic a two-frequency match, event/control pairs reused from stage 025, no external replication, no full CHF representation.

Reproduction: `python chf_stage_026.py CWRU_CHF.zip` with stage 025 script, scipy and numpy. Script and full JSON provided as downloadable conversation artifacts. Next: cyclostationarity and locally windowed envelope spectra against classical baselines, and independently predictive information before/after events.
