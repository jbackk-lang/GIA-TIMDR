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


## Chronoprocess time-history probe

Source audit of `TIMDR-Time-Formalism/timdr_time/chronoprocess.py` and `docs/theory/TIMDR_Chronoprocess.md` confirms that the current Chronoprocess uses one ordered carrier `T), but deliberately keeps M/S, G, and K as independent projections. In K, modalities have constant `(f, phi, A)`; `phase_sync.py` implements an affine local/global time map, not coupled phase dynamics. Therefore the current Chronoprocess does not itself implement a three-loop repair mechanism.

Added `experiments/chronoprocess_triple_loop_time_history.py`: three loop clocks share T; temporary frequency detuning is integrated over time; frequencies then return to nominal. One-, two-, and three-loop detunings are compared using whole-state relative phase and coherence.

Key distinction built into this test:
- Detuning one or two loops creates a lasting relative-phase offset after the frequencies return.
- Equal detuning of all three loops is a common-mode phase shift: absolute phase changes, but relative three-loop coherence remains. This is not recovery; the loops simply experienced the same accumulated shift.
- The test demonstrates time-history dependence and phase memory, not autonomous self-repair or information reconstruction.

A true Chronoprocess-based recovery model would require a separately specified coupling/evolution law across the three projections. It must not be smuggled into the current `Chronoprocess` class, whose documented contract is orchestration only.


## Candidate time-coupled recovery law — preregistered engineering probe

A new *candidate* K-branch evolution law is tested in `experiments/chronoprocess_coupled_phase_recovery.py`:

`dθᵢ/dt = ωᵢ(t) + (K/3) Σⱼ sin(θⱼ−θᵢ)`.

This is a symmetric Kuramoto-type coupling added for falsification testing. It is NOT present in the current `phase_sync.py`, current Chronoprocess, or established K axioms. It must remain clearly labelled as a candidate until independently justified.

Design:
- Shared time carrier `T), with the complete three-phase state `(θ₁,θ₂,θ₃)`.
- A finite frequency detuning window is imposed on one loop, two loops, or all three loops.
- Coupling strengths `K∈{0,0.2,0.8,1.6}` are compared.
- The primary metric is the Kuramoto order parameter `R=|Σ exp(iθᵢ)|/3`; recovery time is the first post-disturbance time at which `R≥0.99`.
- Controls include `K=0` (no coupling) and equal detuning of all loops (common-mode control).

Preliminary reference run (RK4, 500 Hz, base frequency 4 Hz, +5% detuning for 2 s) showed:
- `K=0`, differential detuning: persistent phase offset; post-window mean R ≈ 0.443.
- `K=0.8`, differential detuning: post-window mean R ≈ 0.984; threshold crossing R≥0.99 at ≈2.17 s after detuning ends.
- `K=1.6`, differential detuning: post-window mean R ≈ 0.999; threshold crossing at ≈0.656 s.
- Equal detuning of all three loops preserves relative coherence even at `K=0`; this is a common-mode control, not self-repair.

Interpretation is deliberately narrow: the candidate coupling law can restore *relative phase coherence* in this idealized model, and stronger coupling shortens recovery time in the sampled conditions. This is not yet evidence that the original TIMDR Chronoprocess self-repairs, nor that waveform or encoded information is reconstructed.

Required next validation before stronger claims: run the committed tests in the user's full multi-repository environment; repeat at finer time steps (250/500/1000/2000 Hz) for convergence; sweep detuning duration/amplitude and frequency mismatch; test asymmetric and missing coupling links; compare against randomized-phase and no-coupling controls; pre-register a held-out parameter grid. Any extension to real information recovery must carry an independent payload and digest through the process.


### Numerical step-size check (local independent rerun)

For the `K=1.6`, one-loop detuning case, with total duration 8 s and the same 2 s detuning interval, the independently rerun RK4 integration gave:

| Sample rate | Post-window mean R | First R≥0.99 |
|---:|---:|---:|
| 250 Hz | 0.993910 | 0.656 s |
| 500 Hz | 0.993925 | 0.656 s |
| 1000 Hz | 0.993933 | 0.656 s |
| 2000 Hz | 0.993937 | 0.656 s |

The recovery-threshold time is stable to the reported precision across this step-size sweep. This is a numerical convergence check for this specific idealized case, not an empirical validation of TIMDR or a proof of information recovery.


## Duration-window sweep for the full triple loop

Added `experiments/chronoprocess_triple_loop_duration_sweep.py` and its tests. It integrates one coupled three-phase state with a transient frequency pulse applied to one, two, or all three loops. Coupling strengths are K={0, 0.2, 0.4, 0.8, 1.6}; pulse durations are {0.1, 0.25, 0.5, 1, 2, 4} seconds. Recovery is operationally defined as whole-state Kuramoto coherence R≥0.99 maintained for 0.5 seconds after the pulse ends. Relative phase residual is reported independently.

Exploratory result from a local double-precision RK4 simulation (dt=0.002 s, intrinsic frequency 4 Hz, pulse amplitude 1.2 rad/s): with K=0.2, final coherence after a 1 s single-loop pulse is about 0.9955; with K=0.8 it is about 1.0000. For a 2 s pulse, K=0.2 ends around 0.9490, while K=0.8 ends around 1.0000. With K=0 and a 2 s single-loop pulse, the system does not meet the recovery threshold within the 12 s horizon. An equal common-mode pulse on all three loops leaves relative coherence unchanged even at K=0; this is a control, not repair.

Interpretation boundary: these are results of the newly proposed all-to-all Kuramoto model. The model contains explicit coupling and time evolution not present in the current TIMDR K axioms or Chronoprocess implementation. The experiment demonstrates that a time-dependent coupling model can exhibit relaxation of relative phase errors. It does **not** establish that the original TIMDR equations or Helix-Lock already possess this property, nor that information payload is reconstructed.

A next validation should sweep pulse amplitude and initial phase configuration, use non-identical intrinsic frequencies, compare against a PLL and uncoupled controls, test multiple random initial states, and add a payload-integrity/reconstruction experiment kept independent of phase coherence.
