"""Compare the support of finite-depth rotation-angle spectra under D3 reflection."""
import numpy as np
from rhombic_prism_axis_limit_study import enumerate_depths

RADII = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
ANGLES = (0.0, 10.0, 20.0)


def spectrum_support(r, phi_deg):
    phi = np.deg2rad(phi_deg)
    u, v = r*np.cos(phi), r*np.sin(phi)
    maps, raw, states = enumerate_depths(float(u), float(v), 8)[8]
    values = []
    for M, b in maps.values():
        if np.linalg.det(M) <= 0 or np.linalg.norm(M-np.eye(3)) <= 2e-7:
            continue
        cosine = np.clip((np.trace(M)-1.0)/2.0, -1.0, 1.0)
        skew = np.array([M[2,1]-M[1,2], M[0,2]-M[2,0], M[1,0]-M[0,1]])
        sine = 0.5*np.linalg.norm(skew)
        values.append(float(np.degrees(np.arctan2(sine, cosine))))
    return np.unique(np.round(values, 7))


def main():
    failures = 0
    for r in RADII:
        for phi in ANGLES:
            left = spectrum_support(r, phi)
            right = spectrum_support(r, 60.0-phi)
            same = left.shape == right.shape and np.array_equal(left, right)
            max_delta = float(np.max(np.abs(left-right))) if left.shape == right.shape and len(left) else float("inf")
            print(f"D3_SUPPORT,r={r:.1f},phi={phi:.1f},mirror={60-phi:.1f},"
                  f"unique_angles=({len(left)},{len(right)}),"
                  f"same_support={same},max_delta={max_delta:.9g}")
            failures += int(not same)
    print(f"D3_SUPPORT_SUMMARY,pairs={len(RADII)*len(ANGLES)},failures={failures}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
