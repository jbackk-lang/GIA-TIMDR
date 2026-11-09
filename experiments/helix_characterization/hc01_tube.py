#!/usr/bin/env python3
"""HC-01-TUBE: numerical reach estimate for a circular helix.

The estimate combines the local curvature-radius bound with the first
non-trivial doubly-critical self-distance of the infinite circular helix.
It is a geometric centerline result, not a physical material-tube model.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np


def _bisect(f, lo: float, hi: float, iterations: int = 80) -> float:
    flo, fhi = f(lo), f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        raise ValueError("root is not bracketed")
    for _ in range(iterations):
        mid = (lo + hi) / 2
        fm = f(mid)
        if abs(fm) < 1e-14 or hi - lo < 1e-13:
            return mid
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def doubly_critical_pairs(a: float, h: float, turns: int = 8,
                          scan_steps: int = 20000) -> list[dict[str, float]]:
    if a <= 0 or h == 0:
        return []
    eta2 = (h/a)**2
    # For points separated by delta on the same circular helix, the
    # doubly-critical condition is sin(delta) + eta^2*delta = 0.
    f = lambda d: math.sin(d) + eta2*d
    end = turns * 2 * math.pi
    xs = np.linspace(1e-5, end, scan_steps + 1)
    roots = []
    last_x, last_y = float(xs[0]), f(float(xs[0]))
    for x0 in xs[1:]:
        x = float(x0)
        y = f(x)
        if last_y * y < 0:
            root = _bisect(f, last_x, x)
            if root > 1e-4 and (not roots or abs(root-roots[-1]["delta"]) > 1e-6):
                chord2 = 2*a*a*(1-math.cos(root)) + h*h*root*root
                roots.append({
                    "delta": root,
                    "centerline_distance": math.sqrt(max(0.0, chord2)),
                    "half_distance": 0.5*math.sqrt(max(0.0, chord2)),
                })
        last_x, last_y = x, y
    return roots


def characterize(a: float, h: float) -> dict:
    if a <= 0:
        raise ValueError("a must be positive")
    kappa = a/(a*a+h*h)
    local_radius = 1.0/kappa
    roots = doubly_critical_pairs(a, h)
    first_bottleneck = min(roots, key=lambda x: x["half_distance"]) if roots else None
    global_bound = first_bottleneck["half_distance"] if first_bottleneck else None
    reach_estimate = min(local_radius, global_bound) if global_bound is not None else local_radius
    limiting = "global_doubly_critical_distance" if global_bound is not None and global_bound < local_radius else "local_curvature"
    return {
        "a": a,
        "h": h,
        "eta_h_over_a": h/a,
        "curvature": kappa,
        "local_radius_of_curvature": local_radius,
        "doubly_critical_roots": roots,
        "global_half_self_distance_bound": global_bound,
        "centerline_tube_radius_estimate": reach_estimate,
        "limiting_mechanism": limiting,
        "notes": [
            "For h=0 the parametrization retraces a circle and is treated as a limiting case, not an embedded infinite helix.",
            "The global search is numerical and bounded to the requested number of turns.",
            "A physical tube may have additional constraints from material thickness, deformation, or boundary conditions."
        ]
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("results/hc01_tube/hc01_tube_sweep.json"))
    ap.add_argument("--turns", type=int, default=8)
    args = ap.parse_args()
    rows = []
    for eta in np.linspace(-1.0, 1.0, 41):
        if abs(eta) < 1e-12:
            continue
        rows.append(characterize(1.0, float(eta)))
    payload = {
        "schema": "gia-timdr-hc01-tube-v0.1",
        "method": "local curvature radius plus numerically detected doubly-critical centerline distances",
        "search_turns": args.turns,
        "sweep": rows,
        "caveat": "Numerical geometric estimate for the ideal circular helix; not a measured material property or a reduction criterion."
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({
        "points": len(rows),
        "examples": [characterize(1.0, x) for x in (0.2, 0.3, 0.4, 0.6, 1.0)]
    }, indent=2))


if __name__ == "__main__":
    main()
