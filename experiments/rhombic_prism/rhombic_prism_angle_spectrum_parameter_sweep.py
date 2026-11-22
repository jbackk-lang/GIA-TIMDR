"""Check whether the length-eight angular gap persists away from the center."""
import numpy as np

from rhombic_prism_axis_limit_study import enumerate_depths


def angle_histogram(label, u, v):
    maps, raw, states = enumerate_depths(u, v, 8)[8]
    angles = []
    for M, b in maps.values():
        if np.linalg.det(M) <= 0 or np.linalg.norm(M - np.eye(3)) <= 2e-7:
            continue
        cosine = np.clip((np.trace(M) - 1.0) / 2.0, -1.0, 1.0)
        skew = np.array([M[2, 1] - M[1, 2],
                         M[0, 2] - M[2, 0],
                         M[1, 0] - M[0, 1]])
        sine = 0.5 * np.linalg.norm(skew)
        angles.append(float(np.degrees(np.arctan2(sine, cosine))))
    a = np.asarray(angles)
    bins = [0, 1, 5, 15, 30, 60, 90, 110, 119, 120, 150, 180.000001]
    hist = [int(np.sum((a >= lo) & (a < hi))) for lo, hi in zip(bins[:-1], bins[1:])]
    below5 = a[a < 5]
    above5 = a[a >= 5]
    gap = float(above5.min() - below5.max()) if len(below5) and len(above5) else float("nan")
    print(f"ANGLE_SWEEP,{label},u={u:.7g},v={v:.7g},raw={raw},"
          f"distinct_maps={len(maps)},angle_count={len(a)},hist={hist},"
          f"max_below5={below5.max() if len(below5) else float('nan'):.7g},"
          f"min_above5={above5.min() if len(above5) else float('nan'):.7g},"
          f"observed_gap={gap:.7g}")


def main():
    # Larger deformations test whether the near-central angular gap is robust.
    angle_histogram("symmetry_r03", 0.3, 0.0)
    angle_histogram("generic45_r03", 0.3 / np.sqrt(2), 0.3 / np.sqrt(2))
    angle_histogram("generic45_r06", 0.6 / np.sqrt(2), 0.6 / np.sqrt(2))
    print("LIMIT: finite-depth angular spectrum; no claim about all words.")


if __name__ == "__main__":
    main()
