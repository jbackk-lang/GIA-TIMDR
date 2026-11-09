#!/usr/bin/env python3
"""Verify phase/chirality preservation when transforming a helical signal to a field.

Uses the same core interpolation choice as Synoptyk-v3 (scipy.griddata,
method='cubic', nearest fill outside the convex hull). This is a synthetic
representation test, not a physical helix model.
"""
from __future__ import annotations

import json
import numpy as np
from scipy.interpolate import griddata


def wrap_phase(x: np.ndarray) -> np.ndarray:
    return (x + np.pi) % (2.0 * np.pi) - np.pi


def winding_number(phase: np.ndarray, loop: np.ndarray) -> float:
    values = phase[loop[:, 1], loop[:, 0]]
    increments = wrap_phase(np.roll(values, -1) - values)
    return float(increments.sum() / (2.0 * np.pi))


def square_loop(lo: int = 20, hi: int = 60) -> np.ndarray:
    x = np.arange(lo, hi + 1)
    y = np.arange(lo, hi + 1)
    return np.concatenate([
        np.column_stack([x, np.full_like(x, lo)]),
        np.column_stack([np.full_like(y[1:], hi), y[1:]]),
        np.column_stack([x[-2::-1], np.full_like(x[-2::-1], hi)]),
        np.column_stack([np.full_like(y[-2:0:-1], lo), y[-2:0:-1]]),
    ])


def interpolate(values: np.ndarray, points: np.ndarray,
                gx: np.ndarray, gy: np.ndarray) -> np.ndarray:
    out = griddata(points, values.ravel(), (gx, gy), method="cubic")
    if np.isnan(out).any():
        nearest = griddata(points, values.ravel(), (gx, gy), method="nearest")
        out = np.where(np.isnan(out), nearest, out)
    return out


def robustness_case(chirality: int, n: int, noise: float) -> dict:
    xs = np.linspace(-1.0, 1.0, n)
    X, Y = np.meshgrid(xs, xs)
    points = np.column_stack([X.ravel(), Y.ravel()])
    dense = np.linspace(-1.0, 1.0, 81)
    GX, GY = np.meshgrid(dense, dense)
    true_phase = chirality * np.arctan2(Y, X)
    rng = np.random.default_rng(123)
    c = np.cos(true_phase) + rng.normal(0.0, noise, true_phase.shape)
    s = np.sin(true_phase) + rng.normal(0.0, noise, true_phase.shape)
    ci = interpolate(c, points, GX, GY)
    si = interpolate(s, points, GX, GY)
    phase = np.arctan2(si, ci)
    norm = np.hypot(ci, si)
    loop = square_loop()
    mask = ((GX**2 + GY**2 > 0.15**2) &
            (GX**2 + GY**2 < 0.85**2) & (norm > 0.1))
    error = np.abs(wrap_phase(
        phase[mask] - chirality * np.arctan2(GY[mask], GX[mask])
    ))
    return {
        "winding": winding_number(phase, loop),
        "phase_mae_deg": float(np.degrees(error).mean()),
        "phase_p95_deg": float(np.degrees(np.quantile(error, 0.95))),
    }


def run() -> dict:
    # Sparse samples and dense output grid, matching Synoptyk-v3's
    # scattered-points -> regular-grid architecture.
    xs = np.linspace(-1.0, 1.0, 9)
    ys = np.linspace(-1.0, 1.0, 9)
    X, Y = np.meshgrid(xs, ys)
    points = np.column_stack([X.ravel(), Y.ravel()])
    dense = np.linspace(-1.0, 1.0, 81)
    GX, GY = np.meshgrid(dense, dense)
    loop = square_loop()
    mask = ((GX**2 + GY**2 > 0.15**2) &
            (GX**2 + GY**2 < 0.85**2))

    results = {}
    for chirality in (1, -1):
        true_phase = chirality * np.arctan2(Y, X)

        # Correct circular representation: interpolate both quadratures.
        c = interpolate(np.cos(true_phase), points, GX, GY)
        s = interpolate(np.sin(true_phase), points, GX, GY)
        magnitude = np.hypot(c, s)
        phase_from_pair = np.arctan2(s, c)
        valid = mask & (magnitude > 0.1)
        phase_error = np.abs(wrap_phase(
            phase_from_pair[valid] -
            chirality * np.arctan2(GY[valid], GX[valid])
        ))

        # Deliberately incorrect control: interpolate wrapped angle as scalar.
        phase_scalar = interpolate(true_phase, points, GX, GY)
        results[str(chirality)] = {
            "quadrature_winding": winding_number(phase_from_pair, loop),
            "scalar_angle_winding": winding_number(phase_scalar, loop),
            "quadrature_phase_mae_deg": float(np.degrees(phase_error).mean()),
            "quadrature_phase_p95_deg": float(np.degrees(np.quantile(phase_error, 0.95))),
            "field_norm_min_valid": float(magnitude[valid].min()),
            "field_norm_median_valid": float(np.median(magnitude[valid])),
        }

    robustness = [
        {"chirality": q, "source_grid_n": n, "noise_std": noise,
         **robustness_case(q, n, noise)}
        for q in (1, -1) for n in (5, 7, 9, 13, 17)
        for noise in (0.0, 0.05, 0.1, 0.2, 0.35)
    ]
    return {
        "schema": "gia-timdr-phase-field-preservation-v1",
        "status": "synthetic_representation_test_not_physical_validation",
        "interpolator": "scipy.interpolate.griddata(method='cubic') + nearest fill",
        "source_grid": "9x9",
        "output_grid": "81x81",
        "results_by_chirality": results,
        "robustness_sweep": robustness,
        "interpretation": [
            "Interpolating (cos(phi), sin(phi)) preserves circular phase through the branch cut in this test.",
            "Interpolating wrapped phi as an ordinary scalar destroys the measured winding in this test.",
            "The sign of winding distinguishes the two chiralities (+1 versus -1).",
            "This validates a representation choice for a synthetic field, not physical signal-to-helix coupling.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
