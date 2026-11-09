#!/usr/bin/env python3
"""Minimal abstract signal -> G-ring -> response probe.

This is an engineering coupling test, NOT a calibrated physical helix model.
The input is a normalized scalar signal mapped to one ring node through an
explicit gain. The time-domain state is (x, v); prior excitation can leave
a residual state that changes the response to an identical probe.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from core.geometric_resonance_operator import build_ring_matrices


def rk4_step(state, force, dt, M, K, Gamma):
    n = len(M)
    x, v = state[:n], state[n:]

    def rhs(s):
        sx, sv = s[:n], s[n:]
        acc = np.linalg.solve(M, force - Gamma @ sv - K @ sx)
        return np.concatenate((sv, acc))

    k1 = rhs(state)
    k2 = rhs(state + 0.5 * dt * k1)
    k3 = rhs(state + 0.5 * dt * k2)
    k4 = rhs(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def simulate(signal, dt, M, K, Gamma, node=0, gain=1.0, initial_state=None):
    signal = np.asarray(signal, dtype=float)
    n = M.shape[0]
    if signal.ndim != 1 or not np.all(np.isfinite(signal)):
        raise ValueError("signal must be a finite 1D array")
    if dt <= 0 or not 0 <= node < n:
        raise ValueError("dt must be positive and node must be in range")
    state = np.zeros(2*n) if initial_state is None else np.asarray(initial_state, float).copy()
    if state.shape != (2*n,):
        raise ValueError("initial_state must contain x and v for every node")
    states = np.zeros((len(signal), 2*n))
    for i, sample in enumerate(signal):
        force = np.zeros(n)
        force[node] = gain * sample
        state = rk4_step(state, force, dt, M, K, Gamma)
        states[i] = state
    return states


def run_probe():
    n = 3
    kappa = np.array([1.0, 1.0, 1.0])
    tau = np.array([0.35, 0.35, 0.35])
    M, K, Gamma = build_ring_matrices(n, kappa, tau, gamma=0.18, k_scale=2.0, kc_scale=1.0)
    dt = 0.005
    t = np.arange(0, 12, dt)
    # Same final test input in both arms.
    test = 0.2 * np.sin(2*np.pi*0.45*t[:800]) * np.hanning(800)
    # Preconditioning history: a bounded pulse, followed by a finite quiet interval.
    history = np.zeros(1200)
    history[100:300] = np.sin(2*np.pi*0.45*np.arange(200)*dt)
    history_state = simulate(history, dt, M, K, Gamma)[-1]
    baseline_state = np.zeros(2*n)
    # Compare identical test signal with zero state and history-conditioned state.
    y0 = simulate(test, dt, M, K, Gamma, initial_state=baseline_state)
    yh = simulate(test, dt, M, K, Gamma, initial_state=history_state)
    # Response observable is displacement at the driven node.
    d0 = y0[:, 0]
    dh = yh[:, 0]
    diff = dh - d0
    return {
        "schema": "gia-timdr-abstract-signal-helix-response-probe-v0.1",
        "status": "synthetic_model_demonstration_not_physical_validation",
        "model": "M x_ddot + Gamma x_dot + K x = B u(t), B injects normalized scalar input at node 0",
        "geometry": {"n_nodes": n, "kappa": kappa.tolist(), "tau_unsigned_model_input": tau.tolist()},
        "input": {"dt": dt, "test_samples": len(test), "same_test_signal_both_arms": True, "gain": 1.0},
        "history": {"preconditioning_samples": len(history), "quiet_gap_samples": 0,
                    "state_norm_before_test": float(np.linalg.norm(history_state))},
        "response": {
            "baseline_rms": float(np.sqrt(np.mean(d0*d0))),
            "history_conditioned_rms": float(np.sqrt(np.mean(dh*dh))),
            "rms_difference": float(np.sqrt(np.mean(diff*diff))),
            "max_abs_difference": float(np.max(np.abs(diff))),
        },
        "interpretation": [
            "A nonzero difference shows state-dependent response in this chosen linear oscillator model.",
            "It does not establish a physical information-to-helix coupling law.",
            "The gain and normalized input-to-force mapping are model assumptions, not calibrated units.",
            "Residual mechanical state is not evidence of persistent information memory or self-repair.",
            "The current G matrix uses absolute torsion; this probe does not test chirality."
        ]
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("results/helix_signal_response/minimal_probe.json"))
    args = ap.parse_args()
    result = run_probe()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(result["response"], indent=2))


if __name__ == "__main__":
    main()
