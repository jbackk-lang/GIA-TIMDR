# 54A.7 — Causal META-inspired dynamics

Source: docs/theory/TIMDR_EventGraph_Branch_Construction.md defines S=(Lambda,tau,rho,J) and M_k=(S_k-S_(k-1))/(b_k-b_(k-1)). State from a completed window must not be used to predict that window.

This experiment is NOT full META-TIMDR: byte data do not provide independently measured graph edges or positions, hence geometric J is unavailable. Lambda/tau/rho here are byte-value proxies, not the source-defined event observables. Bias mapping is exploratory.

Protocol: 4 deterministic synthetic datasets, 32768 bytes each; 64-byte completed windows; predictors lag 1/3/256; causal error smoothing; one gzip level 9 stream for all residuals; all round trips verified. Sizes exclude codec identifier.

| Data | gzip | static | adaptive | META proxy |
|---|---:|---:|---:|---:|
| random | 32796 | 32796 | 32796 | 32796 |
| periodic | 170 | 395 | 172 | 172 |
| drift | 167 | 167 | 170 | 320 |
| correlated | 6655 | 9334 | 6655 | 6655 |

Conclusion: no compression gain; substantial degradation on drift. Next: use real event streams with separately observed topology and geometry, freeze calibration, compare against equally informed adaptive baseline.
