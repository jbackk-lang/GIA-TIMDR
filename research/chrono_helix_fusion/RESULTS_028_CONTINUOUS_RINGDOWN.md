# RESULTS 028 — Continuous peak-triggered ringdown

Executed on 16 real CWRU recordings in `CWRU_CHF.zip`, 48 matched event/control pairs inherited from stage 025. Rather than treating windows as isolated, locate maximum absolute peak in each event/control window and extract the **256 samples immediately after that peak from the continuous recording**, crossing window boundaries where needed. Normalize each segment by local pre-peak 256-sample RMS.

Two paired measures: (1) log ratio of late (samples 128–255) to early (8–71) Hilbert-envelope squared energy; (2) maximum spectral power-bin fraction (excluding first four FFT bins) as a crude ringing concentration. Sign-flip tests at recording level (16 clusters), 20,000 random flips; recording-level bootstrap CIs.

Results:
- Late/early log envelope energy: paired mean difference **+0.0144021**, two-sided **p=0.86691**, 95% recording bootstrap CI **[−0.15500, +0.16374]**; 12/16 recording-level differences positive.
- Spectral peak concentration: paired mean difference **−0.0018655**, two-sided **p=0.83086**, 95% CI **[−0.02008, +0.01561]**; 9/16 positive.

**Conclusion:** No detectable event-specific ringdown effect by these metrics. This is NOT a definitive echo or beating test: no delay estimation, no matched peak amplitudes, potential selection/regression-to-mean bias, only one dataset, no held-out replication, no CHF incremental prediction analysis. Future test: physical impulse-response modeling, local baseline matching, compare damped sinusoidal fits against AR and stationary surrogates.

Reproducible script: `chf_stage_028.py`, machine-readable result: `CHF_AFTER_EVENT_028.json` (conversation artifacts).