"""Multi-length test of screw-spectrum unfolding near the central configuration.

Uses the corrected affine face planes. Lengths 2, 4 and 6 are checked with
stable 11-decimal deduplication at epsilon=1e-2. Length 8 is deliberately
reported as a precision-sensitivity diagnostic, not as an invariant count:
floating-point composition accumulates error at that depth.
"""
from collections import Counter
import numpy as np

from rhombic_prism_mobility_screw_coupling import (
    IDENTITY, build_generators, compose
)

def enumerate_maps(u, v, length, decimals=11):
    generators, _, _ = build_generators(u, v)
    layer = [((), (IDENTITY, np.zeros(3)))]
    for _ in range(length):
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

def classify(M, b):
    if np.linalg.norm(M - IDENTITY) < 1e-7:
        return "translation" if np.linalg.norm(b) > 1e-7 else "identity", None, None
    if np.linalg.det(M) < 0:
        return "improper", None, None
    vals, vecs = np.linalg.eig(M)
    axis = np.real(vecs[:, np.argmin(np.abs(vals - 1.0))])
    axis /= np.linalg.norm(axis)
    pitch = float(axis @ b)
    if axis[2] < -1e-9 or (abs(axis[2]) < 1e-9 and axis[0] < 0):
        axis, pitch = -axis, -pitch
    return ("screw" if abs(pitch) > 1e-7 else "rotation"), axis, pitch

def summarize(u, v, length, decimals=11):
    maps, raw = enumerate_maps(u, v, length, decimals)
    kinds = Counter()
    screws = []
    for _, M, b in maps:
        kind, axis, pitch = classify(M, b)
        kinds[kind] += 1
        if kind == "screw":
            screws.append((axis, pitch))
    return len(maps), raw, kinds, screws

def axis_angle(a, b):
    return np.degrees(np.arccos(np.clip(abs(float(a @ b)), -1.0, 1.0)))

def main():
    eps = 1e-2
    center = {}
    for length in (2, 4, 6):
        center[length] = summarize(0.0, 0.0, length)
    assert [(center[n][0], center[n][2]["screw"]) for n in (2,4,6)] == [
        (14, 0), (65, 24), (175, 84)
    ]

    # Three exact perpendicular-face branches: theta=0,60,120 degrees.
    # Three generic directions are controls, not points on these branches.
    cases = {
        "line_0": 0.0,
        "line_60": np.pi/3,
        "line_120": 2*np.pi/3,
        "generic_30": np.pi/6,
        "generic_45": np.pi/4,
        "generic_90": np.pi/2,
    }
    expected = {
        "line_0": {2:(18,0), 4:(245,84), 6:(3045,1848)},
        "line_60": {2:(18,0), 4:(245,84), 6:(3045,1848)},
        "line_120": {2:(18,0), 4:(245,84), 6:(3045,1848)},
        "generic_30": {2:(20,0), 4:(320,120), 6:(5078,3400)},
        "generic_45": {2:(20,0), 4:(320,120), 6:(5102,3480)},
        "generic_90": {2:(20,0), 4:(320,120), 6:(5078,3400)},
    }
    print("epsilon=0.01; dedup_decimals=11")
    print("case,length,distinct_maps,screws,rotations,translations,identities")
    for name, theta in cases.items():
        u, v = eps*np.cos(theta), eps*np.sin(theta)
        for length in (2, 4, 6):
            n, raw, kinds, screws = summarize(u, v, length)
            assert (n, kinds["screw"]) == expected[name][length]
            print(f"{name},{length},{n},{kinds['screw']},{kinds['rotation']},"
                  f"{kinds['translation']},{kinds['identity']}")

    # At length 4, compare screw axes and pitches with the central spectrum.
    _, _, _, central_screws = center[4]
    for name, theta in cases.items():
        u, v = eps*np.cos(theta), eps*np.sin(theta)
        _, _, _, nearby = summarize(u, v, 4)
        nearest_shifts = [
            min(axis_angle(axis, old_axis) for old_axis, _ in central_screws)
            for axis, _ in nearby
        ]
        pitch_values = sorted(set(round(abs(p), 6) for _, p in nearby))
        print(f"axis_pitch,{name},max_nearest_axis_shift_deg="
              f"{max(nearest_shifts):.6f},abs_pitch_values={pitch_values}")

    # Length 8 is included as a diagnostic, but floating point accumulation
    # makes the distinct-map count precision-sensitive off the center.
    print("length8_precision_diagnostic:case,decimals,distinct_maps")
    for name, theta in (("center", 0.0), ("line_0", 0.0),
                        ("generic_30", np.pi/6), ("generic_45", np.pi/4)):
        u, v = (0.0, 0.0) if name == "center" else (
            eps*np.cos(theta), eps*np.sin(theta))
        for decimals in (7, 9, 11, 13):
            n, _, _, _ = summarize(u, v, 8, decimals)
            print(f"length8_precision_diagnostic:{name},{decimals},{n}")
    print("PASS: length 2/4/6 spectra and screw counts reproduce at all six directions.")
    print("LIMIT: length-8 off-center map counts are precision-sensitive and are not asserted.")

if __name__ == "__main__":
    main()
