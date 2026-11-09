"""Sensitivity of finite-depth axis clouds to the near-identity angle cutoff."""
import numpy as np

from rhombic_prism_axis_limit_study import enumerate_depths, extract_axis, line_key


def analyze(label, u, v):
    maps, raw, states = enumerate_depths(u, v, 8)[8]
    print(f"CONFIG,{label},length=8,raw_words={raw},distinct_maps={len(maps)}")
    angle_values = []
    for M, b in maps.values():
        if np.linalg.norm(M - np.eye(3)) > 2e-7 and np.linalg.det(M) > 0:
            cosine = np.clip((np.trace(M) - 1.0) / 2.0, -1.0, 1.0)
            skew = np.array([M[2, 1] - M[1, 2], M[0, 2] - M[2, 0], M[1, 0] - M[0, 1]])
            sine = 0.5 * np.linalg.norm(skew)
            angle_values.append(float(np.degrees(np.arctan2(sine, cosine))))
    bins = [0, 5, 30, 60, 90, 120, 180.000001]
    hist = [int(np.sum((np.asarray(angle_values) >= lo) & (np.asarray(angle_values) < hi)))
            for lo, hi in zip(bins[:-1], bins[1:])]
    print(f"ANGLE_HIST,{label},bins_lt5_5to30_30to60_60to90_90to120_ge120={hist},"
          f"min_nonidentity_deg={min(angle_values):.7g}")
    for cutoff in (1.0, 2.0, 5.0, 10.0):
        axes = {}
        rotations = screws = near = translations = 0
        angles = []
        for M, b in maps.values():
            kind, result = extract_axis(M, b, min_angle_deg=cutoff)
            if kind == "ill_conditioned":
                near += 1
                continue
            if kind == "translation":
                translations += 1
                continue
            if kind == "rotation_axis":
                rotations += 1
            elif kind == "screw_axis":
                screws += 1
            else:
                continue
            a, p, pitch, angle, residual, gap = result
            axes.setdefault(line_key(a, p), (a, p))
            angles.append(angle)
        distances = np.asarray([np.linalg.norm(p) for a, p in axes.values()])
        if len(distances):
            stats = (np.median(distances), np.quantile(distances, .9),
                     np.max(distances), min(angles))
        else:
            stats = (0, 0, 0, 0)
        print(f"CUTOFF,{label},{cutoff:g},rotation_axes={rotations},"
              f"screw_axes={screws},unique_lines={len(axes)},"
              f"translations={translations},near_identity={near},"
              f"p_norm_q50_q90_max_minangle={tuple(round(float(x),7) for x in stats)}")


def main():
    analyze("symmetry_branch", 0.01, 0.0)
    analyze("generic_45", 0.01 / np.sqrt(2), 0.01 / np.sqrt(2))
    print("LIMIT: cutoff sensitivity only; not a fractal-dimension estimate.")


if __name__ == "__main__":
    main()
