# RESULTS 034 — Sensitivity of interval–amplitude association to peak detection

Executed on the real local `CWRU_CHF.zip` (16 recordings, up to 120×2048 samples each), with code `chf_stage_034.py`. Based on stage 033, measure correlation of log inter-peak interval with log subsequent-peak amplitude, adjusted by residualization against local block log RMS, local detected-peak count, and normalized block position (16,384-sample blocks).

**Sensitivity grid:** threshold quantiles {0.990,0.995,0.997} × minimum peak distances {16,32,64} samples. 100,000 sign-flip draws at recording level; same 16 recordings reused for all conditions.

| Threshold | Distance | Mean adjusted r | Positive recordings | Raw two-sided p | Bonferroni p (×9) |
|---|---:|---:|---:|---:|---:|
| .990 | 16 | .033842 | 6/16 | .330897 | 1 |
| .990 | 32 | .047141 | 9/16 | .168198 | 1 |
| .990 | 64 | .060722 | 10/16 | .073269 | .659423 |
| .995 | 16 | .020616 | 8/16 | .349017 | 1 |
| .995 | 32 | .040877 | 12/16 | .049560 | .446036 |
| .995 | 64 | .051541 | 12/16 | .016730 | .150568 |
| .997 | 16 | .019614 | 7/16 | .413356 | 1 |
| .997 | 32 | .036473 | 10/16 | .120589 | 1 |
| .997 | 64 | .036808 | 11/16 | .146139 | 1 |

**Interpretation:** all nine mean correlations are positive but small, and their strength and p-values depend on peak-detection parameters. **No test remains significant after correction for nine comparisons**; correction also ignores earlier exploratory analyses, so it is optimistic. This is NOT independent replication: same 16 recordings used in stages 032–034. Selection bias and known mechanical processes remain plausible explanations. No established signal memory or novel CHF information.

Next: pre-specify one fixed configuration and validate on a genuinely different bearing dataset, or shift to out-of-sample incremental prediction over a strong mechanical baseline.

Artifacts in conversation: `chf_stage_034.py` and `CHF_AFTER_EVENT_034.json`.