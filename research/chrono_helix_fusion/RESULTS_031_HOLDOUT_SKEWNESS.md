# RESULTS 031 — Held-out time-window check of AR8 residual asymmetry

Executed on the real `CWRU_CHF.zip` dataset, 16 recordings. The metric was selected in advance from stage 030: event minus control **absolute skewness of held-out AR(8) one-step prediction residuals**.

**Holdout:** only windows **42–57** (16 windows per recording), previously not used in event/control selection in stage 030. Two highest crest-factor windows per recording; match to two distinct controls using standardized differences in **log peak amplitude AND log RMS**. For each event/control, take 320 continuous samples after the local maximum, fit AR8 on first 160 and compute absolute residual skewness on last 160.

**Results:** 32 pairs across 16 recordings; recording-level paired mean **+0.0374450**, *opposite sign* to stage 030 (**−0.0507059**); two-sided recording sign-flip p **0.330747** (100,000 random sign flips); one-sided negative p **0.834312**; recording bootstrap 95% CI **[−0.0190095,+0.1072941]**; only 5/16 recording-level differences negative. Median absolute log peak amplitude matching gap **0.040188**; median standardized matching cost **0.8833**.

**Interpretation:** the previously suggested lower AR8 residual asymmetry after impulses does **not replicate** in unused time windows. Do not claim memory, new physics, or robust anomaly. Caveats: same 16 recordings and bearing conditions (not independent external replication); matching peak and RMS is imperfect and selection on crest factor makes overlap difficult; 2 pairs/recording; project-wide exploratory hypothesis selection.

Reproduce with `python chf_stage_031.py CWRU_CHF.zip` alongside `chf_stage_029.py` and `chf_stage_030.py`. Local machine-readable output `CHF_AFTER_EVENT_031.json`.
