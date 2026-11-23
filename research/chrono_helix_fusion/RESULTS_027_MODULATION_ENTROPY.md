# RESULTS 027 — Modulation rhythm and independent spectral entropy

Executed on actual CWRU_CHF.zip, 16 recordings × 50 windows of 2048 samples; 48 event/control pairs selected exactly as stage 025 (three pairs per recording). Features measured in the **next** window after selected crest-factor events and RMS-matched controls.

Three preregistration-free exploratory paired measures:
1. Envelope cyclic concentration: largest envelope power spectral bin / sum of bins 4–256, mean event-control **−0.0018944**, recording-level sign-flip two-sided **p=0.5358**, recording bootstrap 95% CI [−0.0075244, 0.0029784].
2. Raw spectral entropy: normalized Shannon entropy of windowed acceleration power spectrum, difference **+0.0042306**, **p=0.2503**, CI [−0.0024054, 0.0110466].
3. Envelope dominant-frequency persistence: exp(−|change in envelope peak FFT bin from prior window|/8), difference **+0.0102026**, **p=0.6552**, CI [−0.0274795, 0.0536802].

Test: 20,000 sign flips at **recording level** (16 independent units), not 48 independent pairs; recording bootstrap for CI. Seed 20261119.

**Interpretation:** no persuasive evidence for any of these three effects. The stage 025 increase in envelope autocorrelation does not imply a matching increase in single-bin envelope concentration or persistent modulation frequency. These proxies are not a full cyclic spectral analysis; harmonics and known bearing mechanics remain alternative explanations. No multiplicity correction, no independent dataset, no proof of echo, beating, novel memory, or CHF advantage.

Artifacts: `chf_stage_027.py`, `CHF_AFTER_EVENT_027.json`. Reproduce: `python chf_stage_027.py CWRU_CHF.zip` (requires stage 025 module).
