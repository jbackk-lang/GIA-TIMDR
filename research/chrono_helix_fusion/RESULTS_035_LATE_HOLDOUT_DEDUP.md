# RESULTS 035 — Late-time holdout and exact duplicate detection

Executed on real CWRU_CHF.zip. Fixed hypothesis: positive locally adjusted correlation between log inter-event interval and following peak log amplitude. Threshold .995; peak distance 32 samples. Holdout starts at sample 245760 (120×2048), beyond prior stage 034 analysis. Require 40 windows of late data.

**Critical data-quality finding:** numerical drive-end acceleration arrays in `98.mat` and `99.mat` have identical SHA-256 hashes. They are exact duplicates; `99.mat` was excluded. Thus previous analyses treating all 16 files as independent actually had only 15 unique waveforms. Earlier statistical claims must be re-audited.

| File | Early adjusted r | Late adjusted r | Late peaks |
|---|---:|---:|---:|
| 100.mat | −0.0238375 | +0.0026170 | 649 |
| 98.mat | +0.0371714 | −0.0579299 | 533 |

Late mean adjusted correlation **−0.0276564** (1/2 positive); exact recording-level sign-flip two-sided **p=1.0**, one-sided positive **p=0.75**. With only two unique eligible long recordings, the test has very low power and is not external replication. Nevertheless, it does not support a stable positive effect.

No new physical memory or CHF-specific advantage established. Reproduce: `python chf_stage_035.py CWRU_CHF.zip` (requires stage 034 and 033 modules). Local artifacts: `chf_stage_035.py`, `CHF_AFTER_EVENT_035.json`, `RESULTS_035_LATE_HOLDOUT_DEDUP.md`.

**Next priority:** deduplicate and recompute the prior key p-values with 15 independent numerical recordings before any new discovery claim.