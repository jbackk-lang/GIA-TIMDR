#!/usr/bin/env python3
"""Numerical audit of three consecutive sinusoid lobes (+,-,+).

The experiment tests only signal-level facts: lobe signs, zero crossings,
extrema, loss under absolute value, and orientation under time reversal.
It deliberately does NOT claim that a three-lobe signal alone defines a
3D knot; a spatial embedding and node/over-under data are additional inputs.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np


def analyze_three_lobes(samples_per_lobe: int = 512, amplitude: float = 1.0,
                        omega: float = 1.0, phase: float = 0.0) -> dict:
    if samples_per_lobe < 16:
        raise ValueError("samples_per_lobe must be >= 16")
    if amplitude <= 0 or omega <= 0:
        raise ValueError("amplitude and omega must be positive")
    # Three half-periods, starting at a zero crossing.
    t = np.linspace(0.0, 3.0*np.pi/omega, 3*samples_per_lobe+1)
    x = amplitude*np.sin(omega*t + phase)
    # phase is restricted to a zero-starting signal for this canonical audit
    if abs(np.sin(phase)) > 1e-10:
        raise ValueError("canonical three-lobe audit requires phase = k*pi")

    edges = np.array([0.0, np.pi/omega, 2*np.pi/omega, 3*np.pi/omega])
    lobe_signs = []
    extrema = []
    zero_crossings = []
    for i in range(3):
        mask = (t >= edges[i]) & (t <= edges[i+1])
        segment_t, segment_x = t[mask], x[mask]
        peak_idx = int(np.argmax(np.abs(segment_x)))
        extrema.append({
            "time": float(segment_t[peak_idx]),
            "value": float(segment_x[peak_idx]),
            "sign": int(np.sign(segment_x[peak_idx]))
        })
        lobe_signs.append(int(np.sign(np.mean(segment_x[1:-1]))))
    # Zero crossings are the shared boundaries, including both endpoints.
    zero_crossings = [
        {"time": float(e), "slope_sign": int(np.sign(amplitude*omega*np.cos(omega*e+phase)))}
        for e in edges
    ]
    reversed_signs = list(reversed(lobe_signs))
    # Reverse traversal: signal polarity stays attached to samples, but the
    # traversal orientation changes sign. For +,-,+ this word is palindromic.
    abs_signs = [int(np.sign(np.mean(np.abs(x[(t >= edges[i]) & (t <= edges[i+1])][1:-1])))
                      ) for i in range(3)]
    derivative_orientation_forward = 1
    derivative_orientation_reverse = -1
    return {
        "schema": "gia-timdr-three-lobe-signal-audit-v0.1",
        "parameters": {"samples_per_lobe": samples_per_lobe, "amplitude": amplitude,
                       "omega": omega, "phase": phase},
        "lobe_sign_word": lobe_signs,
        "expected_word": [1, -1, 1],
        "lobe_extrema": extrema,
        "zero_crossings": zero_crossings,
        "absolute_value_sign_word": abs_signs,
        "reverse_traversal_lobe_word": reversed_signs,
        "word_is_palindromic": lobe_signs == reversed_signs,
        "traversal_orientation_forward": derivative_orientation_forward,
        "traversal_orientation_reverse": derivative_orientation_reverse,
        "signal_level_conclusions": {
            "alternating_sign_word_recovered": lobe_signs == [1, -1, 1],
            "absolute_value_erases_middle_negative_polarity": abs_signs == [1, 1, 1],
            "sign_word_alone_detects_traversal_direction": lobe_signs != reversed_signs,
            "three_lobes_are_three_spatial_strands": False
        },
        "topology_warning": (
            "The signal word (+,-,+) does not specify a spatial embedding, "
            "crossing data, node connectivity, or a knot/link invariant."
        )
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples-per-lobe", type=int, default=512)
    ap.add_argument("--amplitude", type=float, default=1.0)
    ap.add_argument("--omega", type=float, default=1.0)
    ap.add_argument("--phase", type=float, default=0.0)
    ap.add_argument("--out", type=Path, default=Path("three_lobe_audit.json"))
    a = ap.parse_args()
    result = analyze_three_lobes(a.samples_per_lobe, a.amplitude, a.omega, a.phase)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["signal_level_conclusions"], indent=2))


if __name__ == "__main__":
    main()
