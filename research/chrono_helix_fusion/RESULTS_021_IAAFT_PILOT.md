# RESULTS 021 — IAAFT pilot (real CWRU vs surrogate signals)

Executed on 2026-11-19 using local CWRU_CHF.zip: 16 recordings, 50 windows of 2048 samples. For each recording: original and 8 independently generated whole-record IAAFT surrogate datasets (6 iterations), with exact rank-order amplitude distribution and approximate global Fourier magnitude. On each dataset reselect top 5 crest-factor events among first 42 windows and match 5 controls by log RMS and time. Use next-window log RMS, leave-one-recording-out logistic regression and training-only scaling.

Original mean per-recording AUROC **0.6375**. Surrogate AUROCs: 0.5225, 0.3375, 0.5700, 0.5600, 0.4925, 0.5100, 0.4675, 0.5200. Null mean **0.4975**, empirical 95% quantile interval [0.3603, 0.5682]. One-sided Monte Carlo p=(1+0)/(8+1)=**0.1111**; insufficient surrogate count for a small p-value. Original median log RMS matching gap 0.00478.

**Interpretation:** original predictive performance exceeds all eight surrogates, but this is not statistically conclusive and does not establish new physics or CHF. IAAFT disrupts familiar transient/nonstationary dynamics as well as any hypothetical hidden memory. Six iterations may not converge PSD matching; no PSD-error diagnostics yet. Only classical RMS tested, not helix or CHF features. Small exploratory pilot; preregistration, more surrogates, convergence checks, local-stationary null and independent data needed.

Reproduce with `python research/chrono_helix_fusion/chf_stage_021.py CWRU_CHF.zip`; code and complete JSON supplied in the conversation.
