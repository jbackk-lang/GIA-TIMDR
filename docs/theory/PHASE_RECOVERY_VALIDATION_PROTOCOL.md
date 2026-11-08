# Phase-transition recovery — independent validation protocol

**Status:** preregistration / engineering probe. No self-repair of information is claimed.

## Question
What exactly recovers in the existing TIMDR modal self-repair implementation after a controlled disturbance: estimated frequency scale, phase alignment, signal waveform, or encoded information?

## Source-grounded implementation boundary
- `core/modal_self_repair.py` estimates a scalar frequency scale `s` from resonance peaks and updates it iteratively.
- It does not update an explicit phase-offset parameter.
- `TIMDR-Modal-Formalism/timdr_modal/phase_sync.py` computes an affine time map between constant-frequency modalities; it does not implement coupled oscillator dynamics or an adaptive phase-recovery loop.
- Therefore, frequency re-lock must not be reported as recovery of phase, waveform, or information.

## Probe A — pure phase step
Generate a narrowband carrier with a known instantaneous phase. At a fixed time apply a constant phase step while leaving instantaneous frequency unchanged. Measure:
1. phase error relative to the undisturbed reference;
2. frequency-estimation error;
3. whether the existing scalar-`s` repair changes the phase error.

Expected interpretation: this is a negative control for the current frequency-only repair model. A constant phase step is not a frequency-scale error; if the code has no phase state, it cannot claim to repair that offset.

## Probe B — temporary frequency detuning and return
Generate a carrier with nominal frequency, a bounded interval of known detuning, then return to nominal. Measure frequency estimate and phase residual in pre-disturbance, disturbed, and post-disturbance windows. Report phase residual separately from frequency error: after frequency returns to nominal, accumulated phase offset may remain.

## Probe C — information preservation
Keep a separate known payload bit sequence and its cryptographic digest outside the signal-estimation loop. Verify the payload digest before and after analysis. This checks only that the experiment pipeline did not mutate the stored payload; it does not demonstrate reconstruction of lost/corrupted information.

## Controls
- No-repair baseline.
- Existing TIMDR scalar frequency repair.
- Oracle reference using the known injected frequency/phase, reported only as an upper bound.
- Fixed random seeds and disjoint generation seeds.
- Sweep phase-step size and detuning duration/amplitude.
- Report raw traces and all parameters; do not tune after viewing the final test set.

## Metrics
- RMS frequency error.
- Circular phase error (radians), both immediately after disturbance and after recovery.
- Time to return below a preregistered phase/frequency tolerance.
- Payload digest equality (binary pass/fail, not a model accuracy metric).

## Decision rule
A positive result for frequency tracking is not evidence of phase self-repair. A positive phase result is not evidence of information recovery. Claims must be limited to the metric actually improved. If phase offset remains after frequency returns, record that as residual phase memory rather than silently calling it recovery.

## Next formal step
If a phase-adaptive mechanism is proposed, specify its state variables, update rule, stability conditions, lock-loss detection, and a control against false locking before implementation. Do not modify the K axioms merely to accommodate a desired result.
