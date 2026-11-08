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


## Whole triple-loop requirement (user clarification, 2026-11-08)

The phase-transition object under study is the **entire three-loop state** `Psi=(psi1,psi2,psi3)^T), including inter-loop relations and the full traversal. Single-channel phase-step tests are auxiliary controls only; they cannot stand in for a complete triple-loop transition.

The proposed three-loop extension defines a candidate holonomy `H=P`, where `P` cyclically permutes the three channels and `P^3=I`. The new probe `experiments/triple_loop_transition_probe.py` tests one through six complete traversals and compares `H=I`, `H=P`, and `H=-I` as distinct model hypotheses.

Important result of the algebraic control: after three `P)-traversals the state returns to the *disturbed* state, not the original undisturbed state. Thus `P^3=I` proves cycle closure for the chosen holonomy, **not self-repair** and not recovery of lost information. A repair claim requires an independently specified coupled recovery dynamic and a reference criterion that cannot be rewritten by the repair process itself.


## Coupled three-loop perturbation test

Added `experiments/triple_loop_coupled_perturbation.py` and `tests/test_triple_loop_coupled_perturbation.py`. The probe applies the proposed full matrix `J(Λ)` to one coupled vector `Ψ∈R³`, comparing an undisturbed reference trajectory with disturbances injected into one, two, or all three components. It samples Λ = 0, 0.2, 0.5, 1.0 and also tests the spectrally normalized operator `J/ρ(J)`.

The linearity gives a decisive diagnostic: the difference δΨ between perturbed and reference trajectories obeys δΨₙ₊₁=JδΨₙ (or the normalized operator), so the operator has no mechanism to identify and remove the disturbance. Spectral normalization scales both trajectories and does not reconstruct the reference state. This is not evidence against every possible nonlinear transition mechanism; it shows that the currently specified linear operator alone does not establish self-repair.

The model extension states that for real Λ≠0, ρ(J)>1; at Λ=0, ρ(J)=1. Thus the original J is not a contraction for real Λ. Any recovery mechanism needs additional, independently justified dynamics and must be tested against matched controls.
