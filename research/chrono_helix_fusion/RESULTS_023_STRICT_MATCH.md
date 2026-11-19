# RESULTS 023 — Strict pre-event RMS matching

Executed 2026-11-19 on 16 real CWRU recordings (50 windows of 2048 samples). Five highest crest-factor events among first 42 windows per recording. Unique controls assigned by minimum-cost matching in log RMS plus small temporal penalty; retain only pairs with pre-event log RMS difference <=0.01.

**Real data:** 78/80 pairs retained; median log RMS gap 0.000821. Direct *directional paired statistic* = 25/78 = **0.3205**: in 53/78 pairs next-window RMS after the event was lower than after the matched control. This statistic is NOT the leave-one-recording-out model AUROC from stages 019–022; a trained model may exploit a negative association.

**IAAFT null:** 12 independent whole-record surrogate sets, 12 iterations each, seed 20261121; event detection and matching repeated. Mean directional statistic 0.5126, range 0.4340–0.7255. Two-sided Monte Carlo p for |statistic−0.5| = **2/13 = 0.1538**; one-sided positive p = 1.0. Surrogates retained only 47–63 pairs (mean 54.3), and their median log RMS gaps ranged ~0.0015–0.0031.

**Conclusion:** Negative post-event RMS direction persists with strict pre-event RMS matching, but not statistically established against this small surrogate ensemble. Crucial confound: real and surrogate samples differ substantially in number and composition of matched events. Whole-record IAAFT disrupts known transient and nonstationary structure. No demonstrated new signal memory, helix effect or CHF advantage.

Next: ensure comparable event/pair counts and matching quality across nulls; account for local nonstationarity; only then assess phase and CHF descriptors.

Reproduce using conversation artifact `chf_stage_023.py` with `CWRU_CHF.zip` and `chf_stage_021.py`. Machine-readable output: `CHF_AFTER_EVENT_023.json`.
