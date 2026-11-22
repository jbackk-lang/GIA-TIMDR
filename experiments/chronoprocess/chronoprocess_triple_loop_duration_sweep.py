"""Duration-sweep experiment for time-dependent recovery of the full triple loop.

A transient frequency offset is applied to one, two, or all three loop
phases. A symmetric all-to-all Kuramoto coupling then acts continuously.
This is an explicitly proposed nonlinear extension, NOT an existing TIMDR
axiom or an implementation of the current Chronoprocess.

Recovery is defined operationally as whole-state phase coherence R >= 0.99
for at least 0.5 s after the perturbation ends. Relative phase residual is
reported separately, so common-mode shifts are not mistaken for recovery.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def simulate(k: float, duration: float, amplitude: float = 1.2,
             disturbance: str = "one", dt: float = 0.002,
             total: float = 12.0, start: float = 2.0) -> dict:
    n = round(total / dt)
    t = np.arange(n + 1) * dt
    omega = np.full(3, 2.0 * np.pi * 4.0)
    pulse = np.zeros((n + 1, 3))
    indices = {"one": (0,), "two": (0, 1), "all": (0, 1, 2)}[disturbance]
    pulse[(t >= start) & (t < start + duration), list(indices)] = amplitude
    theta = np.zeros((n + 1, 3))

    def rhs(x, p):
        return omega + p + (k / 3.0) * np.sum(
            np.sin(x[None, :] - x[:, None]), axis=1
        )

    for i in range(n):
        p1, p2 = pulse[i], pulse[i + 1]
        a = rhs(theta[i], p1)
        b = rhs(theta[i] + dt * a / 2, (p1 + p2) / 2)
        c = rhs(theta[i] + dt * b / 2, (p1 + p2) / 2)
        d = rhs(theta[i] + dt * c, p2)
        theta[i + 1] = theta[i] + dt * (a + 2*b + 2*c + d) / 6

    coherence = np.abs(np.mean(np.exp(1j * theta), axis=1))
    relative = np.angle(np.exp(1j * (theta - theta[:, [0]])))
    rel_rms = np.sqrt(np.mean(relative ** 2, axis=1))
    end = start + duration
    hold = round(0.5 / dt)
    recovery = None
    for i in np.where(t >= end)[0]:
        j = min(i + hold, len(t) - 1)
        if np.all(coherence[i:j + 1] >= 0.99):
            recovery = round(float(t[i] - end), 6)
            break
    return {
        "k": k, "duration_s": duration, "disturbance": disturbance,
        "amplitude_rad_s": amplitude, "recovery_time_s": recovery,
        "coherence_at_end": float(coherence[-1]),
        "relative_phase_rms_at_end_rad": float(rel_rms[-1]),
        "coherence_min_during_pulse": float(coherence[
            (t >= start) & (t < end)
        ].min()),
        "status": "recovered_by_threshold" if recovery is not None else "not_recovered_within_horizon",
    }


def run_sweep() -> list[dict]:
    rows = []
    for k in (0.0, 0.2, 0.4, 0.8, 1.6):
        for duration in (0.1, 0.25, 0.5, 1.0, 2.0, 4.0):
            for disturbance in ("one", "two", "all"):
                rows.append(simulate(k, duration, disturbance=disturbance))
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()
    rows = run_sweep()
    if args.json:
        args.json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    if args.csv:
        with args.csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps(rows, indent=2))
