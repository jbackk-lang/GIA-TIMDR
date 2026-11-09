"""Finite-depth study of all rotation/screw axes in the rhombic-prism family.

Unlike the first screw-only diagnostic, this includes zero-pitch rotation axes.
Translations have no finite axis. Near-identity rotations are reported separately
because their axis locations are ill-conditioned.

This is a finite-depth diagnostic, not a proof of an infinite-depth limit or
fractal dimension.
"""
from collections import Counter
import numpy as np

from rhombic_prism_mobility_screw_coupling import IDENTITY, build_generators, compose

MAP_DECIMALS = 10
STATE_DECIMALS = 12
LINE_DECIMALS = 7
MIN_ANGLE_DEG = 1.0
TOL = 2e-7


def key_map(M, b, decimals):
    return tuple(np.round(np.r_[M.ravel(), b], decimals))


def enumerate_depths(u, v, max_length=8):
    """Dynamic enumeration, retaining last generator to preserve reduced words."""
    gens, _, _ = build_generators(u, v)
    # State key: (last generator, rounded affine map); value: representative (M,b).
    states = {(-1, key_map(IDENTITY, np.zeros(3), STATE_DECIMALS)):
              (IDENTITY, np.zeros(3))}
    snapshots = {}
    raw_count = 1
    for length in range(1, max_length + 1):
        nxt = {}
        for (last, _), (M, b) in states.items():
            for i, gen in enumerate(gens):
                if i == last:
                    continue
                Q, q = compose(gen, (M, b))
                nxt[(i, key_map(Q, q, STATE_DECIMALS))] = (Q, q)
        states = nxt
        raw_count *= 5 if length == 1 else 4
        if length % 2 == 0:
            # Keep the distinct map set, not the last-letter states.
            maps = {}
            for (_, _), (M, b) in states.items():
                maps.setdefault(key_map(M, b, MAP_DECIMALS), (M, b))
            snapshots[length] = (maps, raw_count, len(states))
    return snapshots


def canonical_axis(a, p, pitch):
    # An unoriented line has two equivalent direction representatives.
    if (a[2] < -1e-10 or
        (abs(a[2]) <= 1e-10 and
         (a[1] < -1e-10 or (abs(a[1]) <= 1e-10 and a[0] < 0)))):
        a, pitch = -a, -pitch
    return a, p, pitch


def extract_axis(M, b, min_angle_deg=MIN_ANGLE_DEG):
    if np.linalg.det(M) < 0:
        return "improper", None
    if np.linalg.norm(M - IDENTITY) < TOL:
        return ("translation" if np.linalg.norm(b) > TOL else "identity"), None

    cosine = np.clip((np.trace(M) - 1.0) / 2.0, -1.0, 1.0)
    skew = np.array([M[2, 1] - M[1, 2],
                     M[0, 2] - M[2, 0],
                     M[1, 0] - M[0, 1]])
    sine = 0.5 * np.linalg.norm(skew)
    angle = float(np.degrees(np.arctan2(sine, cosine)))
    if angle < min_angle_deg:
        return "ill_conditioned", angle

    # The right singular vector for the smallest singular value is the
    # rotation-axis direction, including the zero-pitch/fixed-line case.
    _, singular, vh = np.linalg.svd(M - IDENTITY)
    a = vh[-1].copy()
    a /= np.linalg.norm(a)
    pitch = float(a @ b)
    a, p_pitch, pitch = canonical_axis(a, np.zeros(3), pitch)

    A = IDENTITY - M
    rhs = b - pitch * a
    p = np.linalg.lstsq(A + np.outer(a, a), rhs, rcond=None)[0]
    p -= a * float(a @ p)
    residual = float(np.linalg.norm(A @ p - rhs))
    if residual > 2e-5:
        return "bad_residual", residual

    kind = "rotation_axis" if abs(pitch) <= 1e-7 else "screw_axis"
    return kind, (a, p, pitch, angle, residual, singular[-2])


def line_key(a, p, decimals=LINE_DECIMALS):
    return tuple(np.round(np.r_[a, p], decimals))


def box_counts(points, scales=(2.0, 1.0, 0.5, 0.25, 0.125, 0.0625)):
    if len(points) == 0:
        return []
    x = np.asarray(points)
    return [(eps, len({tuple(row) for row in np.floor(x / eps).astype(np.int64)}))
            for eps in scales]


def nearest_distance_summary(current, previous):
    if len(current) == 0 or len(previous) == 0:
        return "n/a"
    A = np.asarray(current)
    B = np.asarray(previous)
    mins = np.full(len(A), np.inf)
    # Chunked direct distances; Pluecker coordinates (a, p x a).
    for start in range(0, len(A), 128):
        block = A[start:start + 128]
        d2 = ((block[:, None, :] - B[None, :, :]) ** 2).sum(axis=2)
        mins[start:start + len(block)] = np.sqrt(d2.min(axis=1))
    return (f"min={mins.min():.6g},median={np.median(mins):.6g},"
            f"q90={np.quantile(mins,0.9):.6g},"
            f"within_1e-2={np.mean(mins<1e-2):.5f},"
            f"within_1e-1={np.mean(mins<1e-1):.5f}")


def analyze(label, u, v):
    print(f"CONFIG,{label},u={u:.9g},v={v:.9g}")
    snapshots = enumerate_depths(u, v, 8)
    previous_plucker = None
    for length in (2, 4, 6, 8):
        maps, raw, states = snapshots[length]
        axes = {}
        kinds = Counter()
        pitches = []
        angles = []
        residuals = []
        pnorms = []
        for M, b in maps.values():
            kind, result = extract_axis(M, b)
            kinds[kind] += 1
            if kind not in ("rotation_axis", "screw_axis"):
                continue
            a, p, pitch, angle, residual, gap = result
            axes.setdefault(line_key(a, p), (a, p, pitch))
            pitches.append(abs(pitch))
            angles.append(angle)
            residuals.append(residual)
            pnorms.append(float(np.linalg.norm(p)))

        plucker = []
        for a, p, _ in axes.values():
            plucker.append(np.r_[a, np.cross(p, a)])
        counts = box_counts(plucker)
        if len(plucker):
            pnorm = np.asarray([np.linalg.norm(x[1]) for x in axes.values()])
            print(
                f"DEPTH,{label},{length},raw_words={raw},last_letter_states={states},"
                f"distinct_maps={len(maps)},rotation_axes={kinds['rotation_axis']},"
                f"screw_axes={kinds['screw_axis']},unique_lines={len(axes)},"
                f"translations={kinds['translation']},near_identity={kinds['ill_conditioned']},"
                f"bad_residual={kinds['bad_residual']},"
                f"axis_distance_q50_q90_max=({np.median(pnorm):.7g},"
                f"{np.quantile(pnorm,0.9):.7g},{pnorm.max():.7g}),"
                f"pitch_abs_q50_q90_max=({np.median(pitches):.7g},"
                f"{np.quantile(pitches,0.9):.7g},{max(pitches):.7g}),"
                f"angle_deg_min_q50=({min(angles):.7g},{np.median(angles):.7g}),"
                f"max_axis_residual={max(residuals):.3g},"
                f"plucker_box_counts={counts}"
            )
        else:
            print(f"DEPTH,{label},{length},raw_words={raw},distinct_maps={len(maps)},"
                  f"unique_lines=0,kinds={dict(kinds)}")

        if previous_plucker is not None:
            print(f"DEPTH_OVERLAP,{label},{length}_vs_{length-2},"
                  f"{nearest_distance_summary(plucker, previous_plucker)}")
        previous_plucker = plucker


def main():
    # Center, a symmetry-locus point, and a generic off-symmetry point.
    # All lie strictly inside u^2+v^2<1.
    analyze("center", 0.0, 0.0)
    analyze("symmetry_branch", 0.01, 0.0)
    analyze("generic_45", 0.01 / np.sqrt(2), 0.01 / np.sqrt(2))
    print("LIMIT: finite depths only; no infinite-group or fractal claim.")


if __name__ == "__main__":
    main()
