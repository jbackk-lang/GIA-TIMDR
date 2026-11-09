"""Spatial organization of screw axes in the rhombic-prism reflection family.

For every distinct even-length affine isometry, extract its screw axis as a
line in R^3. A line is represented by its closest point p to the origin and
an unoriented unit direction a (Pluecker coordinates can be formed as
(a, p x a)). Compare axis sets at word lengths 2, 4, 6.

This is a finite-word geometric diagnostic, not a fractal-dimension proof.
"""
from collections import Counter
import numpy as np

from rhombic_prism_mobility_screw_coupling import IDENTITY, build_generators, compose

def enumerate_maps(u, v, length, decimals=11):
    gens, _, _ = build_generators(u, v)
    layer = [((), (IDENTITY, np.zeros(3)))]
    for _ in range(length):
        nxt = []
        for word, tr in layer:
            for i, gen in enumerate(gens):
                if word and word[-1] == i:
                    continue
                nxt.append((word + (i,), compose(gen, tr)))
        layer = nxt
    unique = {}
    for word, (M, b) in layer:
        key = tuple(np.round(np.r_[M.ravel(), b], decimals))
        unique.setdefault(key, (word, M, b))
    return list(unique.values()), len(layer)

def screw_axis(M, b, tol=2e-7, min_angle_deg=0.1):
    # Even word length gives a proper orthogonal linear part. Near-identity
    # rotations have axes extremely far away and are ill-conditioned in float.
    if np.linalg.det(M) < 0.0 or np.linalg.norm(M - IDENTITY) < tol:
        return None
    cosine = np.clip((np.trace(M)-1.0)/2.0, -1.0, 1.0)
    angle_deg = float(np.degrees(np.arccos(cosine)))
    if angle_deg < min_angle_deg:
        return "ill_conditioned", angle_deg
    vals, vecs = np.linalg.eig(M)
    k = int(np.argmin(np.abs(vals - 1.0)))
    if abs(vals[k] - 1.0) > 1e-5:
        return None
    a = np.real(vecs[:, k])
    a /= np.linalg.norm(a)
    pitch = float(a @ b)
    if abs(pitch) < tol:
        return None
    # Fix unoriented direction convention; pitch changes with orientation.
    if a[2] < -1e-10 or (abs(a[2]) <= 1e-10 and
                         (a[1] < -1e-10 or (abs(a[1]) <= 1e-10 and a[0] < 0))):
        a = -a
        pitch = -pitch
    # Closest point p on the axis: (I-M)p = b - pitch*a and p.a=0.
    A = IDENTITY - M
    rhs = b - pitch*a
    p = np.linalg.lstsq(A + np.outer(a, a), rhs, rcond=None)[0]
    p -= a * float(a @ p)
    residual = float(np.linalg.norm(A @ p - rhs))
    if residual > 2e-5:
        return None
    return a, p, pitch, angle_deg

def line_key(a, p, decimals=7):
    return tuple(np.round(np.r_[a, p], decimals))

def extract_axes(u, v, length):
    maps, raw = enumerate_maps(u, v, length)
    axes = {}
    kinds = Counter()
    for word, M, b in maps:
        if np.linalg.norm(M - IDENTITY) < 2e-7:
            kinds["translation" if np.linalg.norm(b) > 2e-7 else "identity"] += 1
            continue
        if np.linalg.det(M) < 0:
            kinds["improper"] += 1
            continue
        sig = screw_axis(M, b)
        if sig is None:
            kinds["rotation"] += 1
            continue
        if sig[0] == "ill_conditioned":
            kinds["ill_conditioned_screw"] += 1
            continue
        kinds["screw"] += 1
        a, p, pitch, angle_deg = sig
        axes.setdefault(line_key(a, p), (a, p, []))[2].append(pitch)
    return list(axes.values()), len(maps), raw, kinds

def box_counts(points, dimensions, scales):
    if len(points) == 0:
        return []
    x = np.asarray(points, dtype=float)
    lo = x.min(axis=0)
    span = np.maximum(x.max(axis=0)-lo, 1e-12)
    y = (x-lo)/span
    out = []
    for eps in scales:
        cells = np.floor(y/eps).astype(int)
        out.append((eps, len({tuple(row) for row in cells})))
    return out

def summarize(label, u, v, lengths=(2,4,6)):
    print(f"CONFIG,{label},u={u:.9g},v={v:.9g}")
    for n in lengths:
        axes, distinct, raw, kinds = extract_axes(u, v, n)
        if axes:
            dirs = np.array([x[0] for x in axes])
            offsets = np.array([x[1] for x in axes])
            pluecker = np.array([np.r_[x[0], np.cross(x[1], x[0])] for x in axes])
            eig = np.linalg.eigvalsh(np.cov(pluecker.T)) if len(axes)>1 else np.zeros(6)
            scales = (0.5,0.25,0.125,0.0625,0.03125)
            counts = box_counts(pluecker, 6, scales)
            pnorm = np.linalg.norm(offsets, axis=1)
            print(f"AXES,{label},{n},raw={raw},distinct_maps={distinct},"
                  f"screw_maps={kinds['screw']},ill_conditioned_screws={kinds['ill_conditioned_screw']},"
                  f"unique_axis_lines={len(axes)},"
                  f"p_norm_minmax=({pnorm.min():.8g},{pnorm.max():.8g}),"
                  f"pluecker_cov_eigs={np.round(eig,8).tolist()},"
                  f"box_counts={counts}")
        else:
            print(f"AXES,{label},{n},raw={raw},distinct_maps={distinct},"
                  f"screw_maps={kinds['screw']},ill_conditioned_screws={kinds['ill_conditioned_screw']},unique_axis_lines=0")

def main():
    eps = 1e-2
    summarize("center", 0.0, 0.0)
    for name, theta in (("special_0",0.0),("special_60",np.pi/3),
                        ("special_120",2*np.pi/3),
                        ("generic_30",np.pi/6),("generic_45",np.pi/4),
                        ("generic_90",np.pi/2)):
        summarize(name, eps*np.cos(theta), eps*np.sin(theta))
    # Exact reduced-word count for five involutive generators, no adjacent
    # equal letters: 5*4^(n-1), not 4^n.
    for n in (2,4,6,8):
        print(f"WORD_COUNT,length={n},count={5*4**(n-1)}")

if __name__ == "__main__":
    main()
