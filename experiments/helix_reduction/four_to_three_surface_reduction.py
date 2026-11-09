#!/usr/bin/env python3
"""Four-to-three helix reduction on a sphere or egg-shaped surface.

This is an explicit geometric *model*, not a claim that the physical TIMDR
object has already been identified. One selected strand is cut at two
parameters; the intervening arc is excised and its endpoints are rejoined
by a surface bridge. The remaining three strands are redistributed to
120-degree azimuthal spacing.

The same parameterization supports a sphere (epsilon=0, axial_scale=1)
and an asymmetric egg (epsilon>0). No measured coordinates are invented.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np


def surface(theta, phi, radius=1.0, axial_scale=1.0, egg=0.0):
    """Axisymmetric surface S(theta,phi); egg in (-1,1), 0 is a sphere
    when axial_scale=1. Positive egg makes the upper hemisphere fuller."""
    if radius <= 0 or axial_scale <= 0 or not (-1.0 < egg < 1.0):
        raise ValueError("radius, axial_scale must be positive and |egg| < 1")
    radial = radius * np.sin(theta) * (1.0 + egg * np.cos(theta))
    z = radius * axial_scale * np.cos(theta)
    return np.stack((radial * np.cos(phi), radial * np.sin(phi), z), axis=-1)


def helix_strand(u, index, count=4, theta0=np.pi / 2, amplitude=0.22,
                 turns=1, radius=1.0, axial_scale=1.0, egg=0.0):
    theta = theta0 + amplitude * np.sin(2.0 * u)
    phi = turns * u + 2.0 * np.pi * index / count
    return surface(theta, phi, radius, axial_scale, egg)


def wrapped_delta(a, b):
    return (b - a + np.pi) % (2.0 * np.pi) - np.pi


def surface_bridge(theta_a, phi_a, theta_b, phi_b, samples=101,
                   radius=1.0, axial_scale=1.0, egg=0.0):
    """A transparent bridge candidate, linear in surface parameters.
    It is not called a geodesic; geodesic minimization is a later refinement."""
    q = np.linspace(0.0, 1.0, samples)
    theta = theta_a + q * (theta_b - theta_a)
    phi = phi_a + q * wrapped_delta(phi_a, phi_b)
    return surface(theta, phi, radius, axial_scale, egg)


def polyline_length(points):
    return float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())


def surface_metric(theta, radius=1.0, axial_scale=1.0, egg=0.0, h=1e-6):
    """First fundamental form coefficients E,F,G from numerical tangents."""
    p = surface(theta, 0.0, radius, axial_scale, egg)
    pt = (surface(theta + h, 0.0, radius, axial_scale, egg) -
          surface(theta - h, 0.0, radius, axial_scale, egg)) / (2*h)
    pp = (surface(theta, h, radius, axial_scale, egg) -
          surface(theta, -h, radius, axial_scale, egg)) / (2*h)
    return float(pt @ pt), float(pt @ pp), float(pp @ pp)


def signed_torsion(points):
    """Periodic finite-difference Frenet torsion; NaN where ill-conditioned."""
    p = np.asarray(points, dtype=float)
    d1 = (np.roll(p, -1, axis=0) - np.roll(p, 1, axis=0)) / 2.0
    d2 = np.roll(p, -1, axis=0) - 2.0*p + np.roll(p, 1, axis=0)
    d3 = (np.roll(p, -2, axis=0) - 2*np.roll(p, -1, axis=0)
          + 2*np.roll(p, 1, axis=0) - np.roll(p, 2, axis=0)) / 2.0
    cross = np.cross(d1, d2)
    den = np.sum(cross*cross, axis=1)
    num = np.sum(cross*d3, axis=1)
    out = np.full(len(p), np.nan)
    good = den > 1e-12
    out[good] = num[good] / den[good]
    return out


def run_model(shape="sphere", samples=720, cut_start=0.15, cut_end=1.1,
              radius=1.0):
    if not (0.0 <= cut_start < cut_end <= 2*np.pi):
        raise ValueError("require 0 <= cut_start < cut_end <= 2*pi")
    egg = 0.0 if shape == "sphere" else 0.28
    axial = 1.0 if shape == "sphere" else 1.08
    u = np.linspace(0.0, 2*np.pi, samples, endpoint=False)
    old = [helix_strand(u, i, radius=radius, axial_scale=axial, egg=egg)
           for i in range(4)]

    # Selected strand #4: cut out the interval and join its two cut sites.
    cut_mask = (u >= cut_start) & (u <= cut_end)
    retained = old[3][~cut_mask]
    ua = cut_start
    ub = cut_end
    theta_a = np.pi/2 + 0.22*np.sin(2*ua)
    theta_b = np.pi/2 + 0.22*np.sin(2*ub)
    phi_a = ua + 3*np.pi/2
    phi_b = ub + 3*np.pi/2
    bridge = surface_bridge(theta_a, phi_a, theta_b, phi_b,
                            radius=radius, axial_scale=axial, egg=egg)

    # Three survivors relax to equal angular phase spacing (120 degrees).
    new = [helix_strand(u, i, count=3, radius=radius,
                        axial_scale=axial, egg=egg) for i in range(3)]
    theta = np.pi/2 + 0.22*np.sin(2*u)
    E, F, G = surface_metric(theta, radius, axial, egg)
    # At fixed theta, the local parallel metric is ds^2 = G dphi^2.
    old_gap = np.sqrt(max(G, 0.0)) * (2*np.pi/4)
    new_gap = np.sqrt(max(G, 0.0)) * (2*np.pi/3)

    torsions = [signed_torsion(p) for p in old[:3]]
    result = {
        "schema": "gia-timdr-four-to-three-surface-reduction-v0.1",
        "shape": shape,
        "surface_parameters": {"radius": radius, "axial_scale": axial, "egg": egg},
        "operation": {
            "selected_strand": 4,
            "cut_interval_parameter": [cut_start, cut_end],
            "cut_endpoint_a": surface(theta_a, phi_a, radius, axial, egg).tolist(),
            "cut_endpoint_b": surface(theta_b, phi_b, radius, axial, egg).tolist(),
            "removed_sample_count": int(cut_mask.sum()),
            "retained_selected_strand_sample_count": int(len(retained)),
            "bridge_length": polyline_length(bridge),
            "bridge_type": "surface-parameter interpolation; not yet a geodesic",
        },
        "before": {
            "strand_count": 4,
            "azimuth_gap_radians": 2*np.pi/4,
            "mean_adjacent_parallel_spacing": float(np.mean(old_gap)),
            "survivor_lengths": [polyline_length(p) for p in old[:3]],
        },
        "after": {
            "strand_count": 3,
            "azimuth_gap_radians": 2*np.pi/3,
            "mean_adjacent_parallel_spacing": float(np.mean(new_gap)),
            "survivor_lengths": [polyline_length(p) for p in new],
        },
        "surface_metric_midpoint": {"E": E, "F": F, "G": G},
        "signed_torsion_survivors": [
            {"mean": float(np.nanmean(t)), "min": float(np.nanmin(t)),
             "max": float(np.nanmax(t))} for t in torsions
        ],
        "interpretation_limits": [
            "The 4-to-3 operation is a specified cut-and-rejoin model, not a proof of physical identity.",
            "The bridge is not geodesically optimized.",
            "The three surviving strands are rephased uniformly; full elastic relaxation is not yet solved.",
            "The model does not identify physical cardinal points without an independent rule.",
            "Torsion values depend on the chosen embedding and parameterization; compare signed values only under the same orientation convention."
        ],
    }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shape", choices=("sphere", "egg"), default="sphere")
    ap.add_argument("--samples", type=int, default=720)
    ap.add_argument("--cut-start", type=float, default=0.15)
    ap.add_argument("--cut-end", type=float, default=1.1)
    ap.add_argument("--radius", type=float, default=1.0)
    ap.add_argument("--out", type=Path, default=Path("four_to_three_reduction.json"))
    args = ap.parse_args()
    if args.samples < 32:
        ap.error("--samples must be at least 32")
    result = run_model(args.shape, args.samples, args.cut_start, args.cut_end, args.radius)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print(json.dumps({
        "shape": result["shape"],
        "bridge_length": result["operation"]["bridge_length"],
        "before_spacing": result["before"]["mean_adjacent_parallel_spacing"],
        "after_spacing": result["after"]["mean_adjacent_parallel_spacing"],
        "torsion": result["signed_torsion_survivors"],
        "output": str(args.out)
    }, indent=2))


if __name__ == "__main__":
    main()
