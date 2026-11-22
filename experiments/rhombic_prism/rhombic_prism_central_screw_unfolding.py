"""Probe the screw-motion spectrum near the central square-prism configuration.

This is a finite-word experiment: all reduced words of length four in the five
correct affine face reflections are enumerated. It does not classify the full
infinite reflection group.
"""
import itertools
from collections import Counter
import numpy as np

from rhombic_prism_mobility_screw_coupling import (
    IDENTITY, build_generators, compose, TOL
)

def maps_at(u, v, decimals=9):
    generators, _, _ = build_generators(u, v)
    layer = [((), (IDENTITY, np.zeros(3)))]
    for _ in range(4):
        nxt = []
        for word, transform in layer:
            for i, gen in enumerate(generators):
                if word and word[-1] == i:
                    continue
                nxt.append((word + (i,), compose(gen, transform)))
        layer = nxt
    distinct = {}
    for word, (M, b) in layer:
        key = tuple(np.round(np.r_[M.ravel(), b], decimals))
        distinct.setdefault(key, (word, M, b))
    return list(distinct.values()), len(layer)

def screw_signature(M, b):
    if np.linalg.det(M) < 0:
        return None
    if np.linalg.norm(M - IDENTITY) < 1e-7:
        return None
    vals, vecs = np.linalg.eig(M)
    axis = np.real(vecs[:, np.argmin(np.abs(vals - 1.0))])
    axis /= np.linalg.norm(axis)
    pitch = float(axis @ b)
    if abs(pitch) < 1e-7:
        return None
    # An unoriented axis and its signed pitch are normalized consistently.
    if axis[2] < -1e-9 or (abs(axis[2]) < 1e-9 and axis[0] < 0):
        axis = -axis
        pitch = -pitch
    return axis, pitch

def signatures(u, v):
    maps, raw_count = maps_at(u, v)
    screws = []
    kinds = Counter()
    for word, M, b in maps:
        if np.linalg.norm(M - IDENTITY) < 1e-7:
            kinds["translation" if np.linalg.norm(b) > 1e-7 else "identity"] += 1
        elif np.linalg.det(M) < 0:
            kinds["improper"] += 1
        else:
            sig = screw_signature(M, b)
            if sig is None:
                kinds["rotation"] += 1
            else:
                kinds["screw"] += 1
                screws.append(sig)
    return len(maps), raw_count, kinds, screws

def axis_angle(a, b):
    return float(np.degrees(np.arccos(np.clip(abs(float(a @ b)), -1.0, 1.0))))

def main():
    eps = 1e-3
    center_n, raw, center_kinds, center_screws = signatures(0.0, 0.0)
    assert raw == 320 and center_n == 65
    assert center_kinds["screw"] == 24

    print("epsilon=0.001; reduced words=320 at every configuration")
    print("angle_deg,distinct_maps,screws,rotations,translations,identities,pitch_abs_values,max_axis_shift_deg")
    directions = (0, np.pi/6, np.pi/4, 0.37, np.pi/3, np.pi/2)
    for theta in directions:
        u, v = eps*np.cos(theta), eps*np.sin(theta)
        n, raw, kinds, screws = signatures(u, v)
        assert raw == 320
        assert len(screws) in (84, 120)
        pitches = sorted(set(round(abs(p), 6) for _, p in screws))
        shifts = [
            min(axis_angle(axis, old_axis) for old_axis, _ in center_screws)
            for axis, _ in screws
        ]
        print(
            f"{np.degrees(theta):.6f},{n},{kinds['screw']},{kinds['rotation']},"
            f"{kinds['translation']},{kinds['identity']},{pitches},"
            f"{max(shifts):.6f}"
        )
    center_pitches = sorted(set(round(abs(p), 6) for _, p in center_screws))
    assert center_pitches == [1.5, 2.0]
    print(f"center: distinct_maps={center_n}; screws={center_kinds['screw']}; pitch_abs_values={center_pitches}")
    print("INTERPRETATION: central degeneracy splits into more distinct length-four screw maps under perturbation.")
    print("LIMIT: finite length-four spectrum only; not a proof of a phase transition in the full group.")

if __name__ == "__main__":
    main()
