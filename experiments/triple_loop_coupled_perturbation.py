"""Whole-state perturbation study for the proposed three-loop J(Lambda).

This is a falsification-oriented linear-operator probe, not a claim of
physical phase-transition recovery. It applies the same 3x3 operator to the
entire coupled state and compares perturbed trajectories with an unperturbed
reference trajectory.
"""
from __future__ import annotations

import json
import numpy as np


def operator_j(lam: float) -> np.ndarray:
    return np.array([[0.0, 1.0, -lam],
                     [-lam, 0.0, 1.0],
                     [1.0, -lam, 0.0]], dtype=float)


def spectral_radius(lam: float) -> float:
    return float(np.max(np.abs(np.linalg.eigvals(operator_j(lam)))))


def run_case(lam: float, disturbed_indices: tuple[int, ...],
             steps: int = 24, stabilize: bool = False) -> dict:
    j = operator_j(lam)
    rho = spectral_radius(lam)
    a = j / rho if stabilize else j
    initial = np.array([1.0, 0.7, -0.35], dtype=float)
    perturbed = initial.copy()
    for idx in disturbed_indices:
        perturbed[idx] += (0.8 if idx % 2 == 0 else -0.55)

    ref = initial.copy()
    state = perturbed.copy()
    distances = []
    norms = []
    for _ in range(steps):
        ref = a @ ref
        state = a @ state
        distances.append(float(np.linalg.norm(state - ref)))
        norms.append(float(np.linalg.norm(state)))

    return {
        "lambda": lam,
        "spectral_radius_original_J": rho,
        "operator": "J/rho(J)" if stabilize else "J",
        "disturbed_loop_indices_1_based": [i + 1 for i in disturbed_indices],
        "initial_perturbation_norm": float(np.linalg.norm(perturbed - initial)),
        "final_distance_from_unperturbed_trajectory": distances[-1],
        "distance_trace": distances,
        "state_norm_trace": norms,
    }


def run_probe() -> dict:
    cases = []
    for lam in (0.0, 0.2, 0.5, 1.0):
        for label, indices in (
            ("one_loop", (0,)),
            ("two_loops", (0, 1)),
            ("all_three_loops", (0, 1, 2)),
        ):
            cases.append({
                "disturbance": label,
                "raw": run_case(lam, indices, stabilize=False),
                "spectrally_normalized": run_case(lam, indices, stabilize=True),
            })
    return {
        "status": "linear_operator_perturbation_test_not_phase_transition_or_information_recovery",
        "state": "single coupled three-loop vector",
        "steps": 24,
        "cases": cases,
        "interpretation": [
            "For a linear time-invariant operator, the difference between perturbed and reference trajectories evolves under the same operator.",
            "If spectral radius exceeds one, perturbation differences can grow; if equal to one, they need not decay.",
            "Dividing J by its spectral radius bounds modal growth but does not selectively restore the original state; it scales both reference and perturbation.",
            "No nonlinear phase-transition dynamics or independent information decoder is specified by the current proposal.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2, sort_keys=True))
