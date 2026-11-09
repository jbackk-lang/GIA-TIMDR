#!/usr/bin/env python3
"""Signed handedness checks for ideal helices; analytic geometry only."""
import argparse
import json
import math
from pathlib import Path


def signed_torsion(radius: float, pitch_per_radian: float) -> float:
    # r(t)=(R cos t, R sin t, h t); tau = h/(R^2+h^2)
    return pitch_per_radian / (radius * radius + pitch_per_radian * pitch_per_radian)


def analyze(radius=1.0, pitch=0.5):
    right = signed_torsion(radius, abs(pitch))
    left = signed_torsion(radius, -abs(pitch))
    return {
        "schema": "gia-timdr-helix-handedness-v0.1",
        "method": "analytic ideal circular helix",
        "convention": {
            "axis": "+z",
            "parameter": "increasing t",
            "ambient_orientation": "right-handed xyz",
            "signed_pitch": "z(t)=h*t; sign(h) defines axial handedness",
        },
        "radius": radius,
        "pitch_per_radian_right": abs(pitch),
        "signed_torsion_right": right,
        "signed_torsion_left": left,
        "magnitude_equal": math.isclose(abs(right), abs(left), rel_tol=1e-12),
        "sign_opposite": math.isclose(right, -left, rel_tol=1e-12),
        "reduction_invariant_payload": {
            "must_preserve": ["signed_torsion", "signed_pitch", "axis_orientation", "phase", "cardinal_event_order"],
            "forbidden_projection": "abs(torsion) alone; it collapses left/right distinction",
        },
        "limits": [
            "This is a synthetic geometric control, not a measured TIMDR helix.",
            "Geometric handedness is not particle-antiparticle identity.",
            "At zero curvature the Frenet torsion is undefined; use a stable alternative frame or mark it undefined.",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--radius", type=float, default=1.0)
    p.add_argument("--pitch", type=float, default=0.5)
    p.add_argument("--out", type=Path, default=Path("helix_handedness.json"))
    a = p.parse_args()
    if a.radius <= 0 or a.pitch == 0:
        raise SystemExit("radius must be positive and pitch nonzero")
    result = analyze(a.radius, a.pitch)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("signed_torsion_right", "signed_torsion_left", "magnitude_equal", "sign_opposite")}, indent=2))
    print(f"Wrote {a.out}")


if __name__ == "__main__":
    main()
