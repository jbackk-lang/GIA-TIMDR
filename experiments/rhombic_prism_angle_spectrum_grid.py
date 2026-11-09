"""Grid study of the finite-depth rotation-angle spectrum (reduced words <= 8)."""
import numpy as np

from rhombic_prism_axis_limit_study import enumerate_depths

RADII = (0.10, 0.30, 0.60, 0.80)
DIRECTIONS_DEG = (0.0, 22.5, 45.0)


def spectrum(r, phi_deg):
    phi = np.deg2rad(phi_deg)
    u, v = r * np.cos(phi), r * np.sin(phi)
    maps, raw, states = enumerate_depths(float(u), float(v), 8)[8]
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
    a = np.sort(np.asarray(angles))
    # Collapse numerical multiplicities only for the geometric gap diagnostic.
    unique = np.unique(np.round(a, 7))
    gaps = np.diff(unique)
    order = np.argsort(gaps)[::-1][:5]
    largest = [(float(unique[i]), float(unique[i+1]), float(gaps[i]))
               for i in order]
    below5 = a[a < 5.0]
    above5 = a[a >= 5.0]
    gap5 = (float(above5.min() - below5.max())
            if len(below5) and len(above5) else float("nan"))
    print(f"GRID,r={r:.3f},phi={phi_deg:.1f},u={u:.8g},v={v:.8g},"
          f"maps={len(maps)},angles={len(a)},unique_angles={len(unique)},"
          f"count_lt5={len(below5)},count_ge5={len(above5)},"
          f"max_lt5={below5.max() if len(below5) else float('nan'):.7g},"
          f"min_ge5={above5.min() if len(above5) else float('nan'):.7g},"
          f"gap_at5={gap5:.7g},largest_gaps={largest}")


def main():
    for r in RADII:
        for phi in DIRECTIONS_DEG:
            spectrum(r, phi)
    print("LIMIT: finite-depth angle spectrum only; not a theorem about all group elements.")


if __name__ == "__main__":
    main()
