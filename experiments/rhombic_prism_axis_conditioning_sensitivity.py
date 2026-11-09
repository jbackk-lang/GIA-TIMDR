"""Sensitivity of finite-depth axis clouds to the near-identity angle cutoff."""
import numpy as np

from rhombic_prism_axis_limit_study import enumerate_depths, extract_axis, line_key


def analyze(label, u, v):
    maps, raw, states = enumerate_depths(u, v, 8)[8]
    print(f"CONFIG,{label},length=8,raw_words={raw},distinct_maps={len(maps)}")
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
