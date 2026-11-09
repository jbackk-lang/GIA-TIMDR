"""Audit cumulative screw/rotation-axis geometry at even reduced-word depths.

The cumulative set through depth n includes proper isometries represented by
all even reduced words of lengths <= n. This avoids comparing non-nested exact
word-length shells. Lines are represented by normalized Pluecker coordinates
(a, p x a), with a a canonically oriented unit direction and p the closest
point on the line to the origin.

This is a finite-depth diagnostic only. Box occupancy is not a Hausdorff
dimension estimate, and nearest-neighbour stabilization is not a proof of
Hausdorff convergence of the infinite axis set.
"""
from collections import Counter
import numpy as np

from rhombic_prism_axis_limit_study import enumerate_depths, extract_axis, line_key

CONFIGS = (
    ("center", 0.0, 0.0),
    ("near_center_symmetry", 0.01, 0.0),
    ("generic_moderate", 0.20, 0.10),
    ("generic_diagonal", 0.40 / np.sqrt(2), 0.40 / np.sqrt(2)),
)
DEPTHS = (2, 4, 6, 8)
ANGLE_CUTOFFS = (0.5, 1.0, 2.0, 5.0)
BOX_SCALES = (0.5, 0.25, 0.125, 0.0625)


def plucker(a, p):
    # The line direction is unoriented; canonical_axis in extract_axis fixes it.
    return np.r_[a, np.cross(p, a)]


def axis_records(maps, cutoff):
    lines = {}
    kinds = Counter()
    angle_values = []
    pitches = []
    residuals = []
    for M, b in maps.values():
        kind, result = extract_axis(M, b, min_angle_deg=cutoff)
        kinds[kind] += 1
        if kind not in ("rotation_axis", "screw_axis"):
            continue
        a, p, pitch, angle, residual, gap = result
        key = line_key(a, p)
        lines.setdefault(key, (plucker(a, p), a, p, pitch, angle))
        angle_values.append(angle)
        pitches.append(abs(pitch))
        residuals.append(residual)
    return list(lines.values()), kinds, angle_values, pitches, residuals


def directed_nearest(A, B, chunk=128):
    """For each row of A, compute its nearest Euclidean distance to B."""
    if len(A) == 0 or len(B) == 0:
        return np.array([], dtype=float)
    result = np.full(len(A), np.inf)
    B2 = np.sum(B * B, axis=1)
    for start in range(0, len(A), chunk):
        X = A[start:start + chunk]
        d2 = np.sum(X * X, axis=1)[:, None] + B2[None, :] - 2.0 * X @ B.T
        np.maximum(d2, 0.0, out=d2)
        result[start:start + len(X)] = np.sqrt(np.min(d2, axis=1))
    return result


def distance_summary(A, B):
    ab = directed_nearest(A, B)
    ba = directed_nearest(B, A)
    if len(ab) == 0 or len(ba) == 0:
        return "n/a"
    return (
        f"new_to_old_q50_q90_max=({np.median(ab):.6g},"
        f"{np.quantile(ab,.9):.6g},{ab.max():.6g}),"
        f"old_to_new_q50_q90_max=({np.median(ba):.6g},"
        f"{np.quantile(ba,.9):.6g},{ba.max():.6g})"
    )


def fixed_box_counts(points_by_depth):
    all_points = [p for group in points_by_depth.values() for p in group]
    if not all_points:
        return {}
    X = np.asarray(all_points)
    lo, hi = X.min(axis=0), X.max(axis=0)
    span = np.maximum(hi - lo, 1e-12)
    out = {}
    for depth, points in points_by_depth.items():
        if not points:
            out[depth] = []
            continue
        Y = (np.asarray(points) - lo) / span
        counts = []
        for eps in BOX_SCALES:
            cells = np.floor(Y / eps).astype(np.int64)
            counts.append((eps, len({tuple(row) for row in cells})))
        out[depth] = counts
    return out


def analyze(label, u, v):
    snapshots = enumerate_depths(float(u), float(v), max(DEPTHS))
    cumulative = {}
    running = {}
    for depth in DEPTHS:
        exact_maps, raw, states = snapshots[depth]
        running.update(exact_maps)
        cumulative[depth] = dict(running)
    print(f"CONFIG,{label},u={u:.9g},v={v:.9g},w={np.sqrt(1-u*u-v*v):.9g}")
    print("WORD_COUNTS,exact_and_cumulative_even_lengths")
    for depth in DEPTHS:
        print(f"WORDS,{depth},raw_exact={5*4**(depth-1)},"
              f"unique_exact_maps={len(snapshots[depth][0])},"
              f"cumulative_unique_maps={len(cumulative[depth])}")

    point_sets = {}
    records_by_depth = {}
    for depth in DEPTHS:
        records, kinds, angles, pitches, residuals = axis_records(cumulative[depth], 1.0)
        records_by_depth[depth] = records
        point_sets[depth] = [x[0] for x in records]
        pnorms = [np.linalg.norm(x[2]) for x in records]
        print(
            f"AXIS_CLOUD,{label},{depth},maps={len(cumulative[depth])},"
            f"proper_axes={len(records)},rotation_maps={kinds['rotation_axis']},"
            f"screw_maps={kinds['screw_axis']},translations={kinds['translation']},"
            f"near_identity={kinds['ill_conditioned']},bad_residual={kinds['bad_residual']},"
            f"axis_distance_q50_q90_max={tuple(round(float(x),7) for x in "
            f"(np.median(pnorms),np.quantile(pnorms,.9),max(pnorms)) if pnorms else (0,0,0))},"
            f"pitch_abs_q50_q90_max={tuple(round(float(x),7) for x in "
            f"(np.median(pitches),np.quantile(pitches,.9),max(pitches)) if pitches else (0,0,0))},"
            f"angle_min_median={tuple(round(float(x),7) for x in "
            f"(min(angles),np.median(angles)) if angles else (0,0))},"
            f"max_axis_residual={max(residuals) if residuals else 0:.3g}"
        )
        if depth != DEPTHS[0]:
            prev = DEPTHS[DEPTHS.index(depth)-1]
            print(f"AXIS_SET_DISTANCE,{label},{prev}_to_{depth},"
                  f"{distance_summary(np.asarray(point_sets[depth]), np.asarray(point_sets[prev]))}")

    box = fixed_box_counts(point_sets)
    for depth in DEPTHS:
        print(f"PLUCKER_BOX_OCCUPANCY,{label},{depth},{box[depth]}")

    # Cutoff sensitivity at the deepest cumulative set.
    deepest = cumulative[DEPTHS[-1]]
    for cutoff in ANGLE_CUTOFFS:
        records, kinds, angles, pitches, residuals = axis_records(deepest, cutoff)
        print(f"CUTOFF_SENSITIVITY,{label},{cutoff},unique_lines={len(records)},"
              f"rotation_maps={kinds['rotation_axis']},screw_maps={kinds['screw_axis']},"
              f"near_identity={kinds['ill_conditioned']},bad_residual={kinds['bad_residual']}")


def main():
    for label, u, v in CONFIGS:
        analyze(label, u, v)
    print("LIMIT: finite cumulative word depths; Pluecker occupancy and nearest-neighbour diagnostics are not proofs of fractality or infinite-depth convergence.")


if __name__ == "__main__":
    main()
