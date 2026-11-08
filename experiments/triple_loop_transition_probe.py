"""Whole triple-loop transition probe for the proposed three-channel model.

This tests the algebraic cycle/holonomy in the *proposed* three-loop model.
It does not assert that the model is an established GIA-TIMDR axiom, and it
does not call cycle closure "self-repair".
"""
from __future__ import annotations

import json
import numpy as np

P = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
I3 = np.eye(3, dtype=complex)
MINUS_I3 = -I3


def apply_full_loop(state: np.ndarray, holonomy: np.ndarray) -> np.ndarray:
    state = np.asarray(state, dtype=complex)
    if state.shape != (3,):
        raise ValueError("state must contain all three loop amplitudes")
    return holonomy @ state


def run_probe() -> dict:
    initial = np.array([1.0 + 0j, 0.7 * np.exp(0.4j), 0.45 * np.exp(-0.8j)])
    # Perturb one loop, but keep the entire three-loop state as the object
    # being transported and measured.
    disturbed = initial.copy()
    disturbed[0] *= 0.25 * np.exp(1.1j)

    scenarios = {}
    for name, holonomy in (("orientable_control_HI", I3),
                           ("triple_cycle_HP", P),
                           ("global_inversion_HminusI", MINUS_I3)):
        state = disturbed.copy()
        snapshots = []
        for count in range(1, 7):
            state = apply_full_loop(state, holonomy)
            snapshots.append({
                "completed_loops": count,
                "state_distance_from_disturbed": float(np.linalg.norm(state - disturbed)),
                "state_distance_from_initial": float(np.linalg.norm(state - initial)),
                "norm": float(np.linalg.norm(state)),
            })
        scenarios[name] = snapshots

    # The full three-channel state returns after three P-holonomy traversals.
    p3_error = float(np.linalg.norm(np.linalg.matrix_power(P, 3) - I3))
    # The original disturbance is not erased by topological cycle closure.
    after_three = np.linalg.matrix_power(P, 3) @ disturbed
    residual_disturbance = float(np.linalg.norm(after_three - initial))
    return {
        "status": "algebraic_triple_loop_probe_not_self_repair_validation",
        "object_under_test": "single coupled three-component state Psi",
        "initial_state": [[float(z.real), float(z.imag)] for z in initial],
        "disturbed_state": [[float(z.real), float(z.imag)] for z in disturbed],
        "P_cubed_identity_error": p3_error,
        "residual_disturbance_after_three_full_loops": residual_disturbance,
        "scenarios": scenarios,
        "interpretation": [
            "P^3=I establishes algebraic channel-cycle closure for the chosen H=P model.",
            "The disturbance remains after three loops; cycle closure is not self-repair.",
            "H=I and H=-I are distinct control hypotheses, not consequences of Mobius topology.",
            "No information-theoretic recovery is tested by this finite-dimensional state transport.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2, sort_keys=True))
