"""Coupled Chronoprocess phase-recovery candidate: preregistered toy model.

Three phases evolve on one shared time carrier T. A finite interval of
frequency detuning is applied to one, two, or all three loops. A symmetric
Kuramoto-type coupling is then tested as an *additional candidate law*;
it is not part of the existing Chronoprocess implementation or K axioms.

The experiment distinguishes relative-phase recovery from common-mode
phase shifts. It does not test cryptographic payload recovery.
"""
from __future__ import annotations

import json
import numpy as np


def simulate(
    coupling: float,
    disturbed_loops: tuple[int, ...],
    detune_fraction: float = 0.05,
    detune_start: float = 2.0,
    detune_duration: float = 2.0,
    total_duration: float = 12.0,
    sample_rate: float = 500.0,
    base_frequency: float = 4.0,
) -> dict:
    if coupling < 0:
        raise ValueError("coupling must be >= 0 for this recovery hypothesis")
    if not disturbed_loops or any(i not in (0, 1, 2) for i in disturbed_loops):
        raise ValueError("disturbed_loops must contain indices 0, 1, or 2")
    if detune_fraction <= 0 or detune_duration <= 0:
        raise ValueError("detune_fraction and detune_duration must be > 0")

    dt = 1.0 / sample_rate
    n = int(round(total_duration * sample_rate))
    t = np.arange(n + 1, dtype=float) * dt
    theta = np.zeros((n + 1, 3), dtype=float)
    omega0 = np.full(3, 2.0 * np.pi * base_frequency)
    start_i = int(round(detune_start * sample_rate))
    end_i = int(round((detune_start + detune_duration) * sample_rate))

    def rhs(state: np.ndarray, step: int) -> np.ndarray:
        omega = omega0.copy()
        if start_i <= step < end_i:
            omega[list(disturbed_loops)] *= (1.0 + detune_fraction)
        coupling_term = coupling / 3.0 * np.sum(
            np.sin(state[np.newaxis, :] - state[:, np.newaxis]), axis=1
        )
        return omega + coupling_term

    for i in range(n):
        state = theta[i]
        k1 = rhs(state, i)
        k2 = rhs(state + 0.5 * dt * k1, i)
        k3 = rhs(state + 0.5 * dt * k2, i)
        k4 = rhs(state + dt * k3, i)
        theta[i + 1] = state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

    relative = np.angle(np.exp(1j * (theta - theta[:, :1])))
    order = np.abs(np.mean(np.exp(1j * theta), axis=1))
    post_start = detune_start + detune_duration
    post = t >= post_start
    recovery_indices = np.flatnonzero(post & (order >= 0.99))
    recovery_time = (
        float(t[recovery_indices[0]] - post_start)
        if recovery_indices.size else None
    )
    return {
        "coupling": float(coupling),
        "disturbed_loops_1_based": [i + 1 for i in disturbed_loops],
        "detune_fraction": float(detune_fraction),
        "detune_duration": float(detune_duration),
        "post_disturbance_mean_order_parameter": float(np.mean(order[post])),
        "post_disturbance_final_order_parameter": float(order[-1]),
        "post_disturbance_mean_abs_relative_phase_rad": float(
            np.mean(np.abs(relative[post]))
        ),
        "time_to_order_parameter_0_99_seconds": recovery_time,
        "time": t.tolist(),
        "order_parameter": order.tolist(),
        "relative_phase_rad": relative.tolist(),
    }


def run_probe() -> dict:
    cases = {}
    for coupling in (0.0, 0.2, 0.8, 1.6):
        for name, loops in (
            ("one_loop", (0,)),
            ("two_loops", (0, 1)),
            ("all_three_common_mode", (0, 1, 2)),
        ):
            cases[f"K={coupling}:{name}"] = simulate(coupling, loops)
    return {
        "status": "candidate_coupled_phase_law_test_not_empirical_validation",
        "equation": "dtheta_i/dt = omega_i(t) + K/3 * sum_j sin(theta_j-theta_i)",
        "shared_time_carrier": "T",
        "state": "whole three-loop phase vector",
        "integration": "fixed-step fourth-order Runge-Kutta",
        "recovery_metric": "Kuramoto order parameter R >= 0.99 after detuning ends",
        "cases": cases,
        "limitations": [
            "The Kuramoto-type coupling is an explicit new candidate law, not existing TIMDR code or an established axiom.",
            "Identical natural frequencies and symmetric all-to-all coupling are idealized assumptions.",
            "Common-mode detuning changes absolute phase but not relative coherence.",
            "Phase coherence recovery is not proof of waveform, payload, or information recovery.",
            "Numerical results require convergence checks at finer time steps before being treated as robust.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2, sort_keys=True))
