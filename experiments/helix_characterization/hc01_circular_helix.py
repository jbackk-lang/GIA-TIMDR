#!/usr/bin/env python3
"""HC-01 analytic/numeric characterization of a circular helix.

Run:
  python experiments/helix_characterization/hc01_circular_helix.py --out-dir results/hc01
Requires NumPy. No reduction rule or critical angle is assumed.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import numpy as np


def analytic(a: float, h: float) -> dict[str, float]:
    if a <= 0:
        raise ValueError("radius a must be positive")
    den = a*a + h*h
    return {
        "kappa": a/den,
        "tau_fs": h/den,
        "tau_over_kappa": h/a,
        "pitch": 2*np.pi*h,
        "length_per_turn": 2*np.pi*np.sqrt(den),
        "tangent_angle_rad": float(np.arctan2(h, a)),
        "dimensionless_kappa": a*a/den,
        "dimensionless_tau": a*h/den,
        "integrated_torsion_per_turn": 2*np.pi*h/np.sqrt(den),
    }


def numeric(a: float, h: float, samples: int) -> dict[str, float]:
    t = np.linspace(0.0, 4*np.pi, samples)
    points = np.column_stack((a*np.cos(t), a*np.sin(t), h*t))
    d1 = np.gradient(points, t, axis=0, edge_order=2)
    d2 = np.gradient(d1, t, axis=0, edge_order=2)
    d3 = np.gradient(d2, t, axis=0, edge_order=2)
    cross = np.cross(d1, d2)
    cross_norm = np.linalg.norm(cross, axis=1)
    speed = np.linalg.norm(d1, axis=1)
    kappa = cross_norm / speed**3
    tau = np.einsum("ij,ij->i", cross, d3) / cross_norm**2
    # Exclude edge points affected by one-sided finite differences.
    core = slice(8, -8)
    return {
        "numeric_kappa_median": float(np.median(kappa[core])),
        "numeric_tau_fs_median": float(np.median(tau[core])),
    }


def run() -> dict:
    rows = []
    for eta in np.linspace(-4.0, 4.0, 17):
        a, h = 1.0, float(eta)
        exact = analytic(a, h)
        for n in (256, 512, 1024, 2048):
            est = numeric(a, h, n)
            rows.append({
                "eta_h_over_a": float(eta),
                "samples": n,
                **exact,
                **est,
                "abs_kappa_error": abs(est["numeric_kappa_median"]-exact["kappa"]),
                "abs_tau_error": abs(est["numeric_tau_fs_median"]-exact["tau_fs"]),
            })
    # Dense dimensionless sweep locates extrema without presupposing their position.
    grid = np.linspace(-10.0, 10.0, 200001)
    tau_hat = grid/(1.0+grid**2)
    i = int(np.argmax(np.abs(tau_hat)))
    return {
        "schema": "gia-timdr-hc01-circular-helix-characterization-v0.1",
        "model": "r(t)=(a*cos(t), a*sin(t), h*t), a=1",
        "method": "analytic Frenet invariants; numeric derivatives by numpy.gradient; median over interior samples",
        "sweep_rows": rows,
        "dimensionless_abs_torsion_maximum": {
            "eta": float(grid[i]),
            "abs_dimensionless_tau": float(abs(tau_hat[i])),
            "dimensionless_kappa_at_extremum": float(1/(1+grid[i]**2)),
            "tangent_angle_deg": float(np.degrees(np.arctan(grid[i]))),
        },
        "interpretation_limits": [
            "This is a mathematical characterization of the standard circular helix only.",
            "An extremum of dimensionless torsion is not evidence of instability or reduction.",
            "The model has an open axial coordinate; it is not a closed knot.",
            "Numerical torsion uses third derivatives and must be assessed for convergence and noise sensitivity."
        ]
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, default=Path("results/hc01"))
    args = ap.parse_args()
    result = run()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir/"hc01_sweep.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(result["sweep_rows"][0]))
        writer.writeheader()
        writer.writerows(result["sweep_rows"])
    (args.out_dir/"hc01_summary.json").write_text(
        json.dumps({k:v for k,v in result.items() if k != "sweep_rows"},
                   indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(result["dimensionless_abs_torsion_maximum"], indent=2))


if __name__ == "__main__":
    main()
