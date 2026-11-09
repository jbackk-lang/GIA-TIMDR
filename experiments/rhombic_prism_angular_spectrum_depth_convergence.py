"""Compare finite-depth rotation-angle distributions at word lengths 4, 6 and 8."""
import numpy as np

from rhombic_prism_axis_limit_study import enumerate_depths


CONFIGS = (
    ("center", 0.0, 0.0),
    ("axis_r03", 0.3, 0.0),
    ("sector_r03_phi30", 0.3*np.cos(np.pi/6), 0.3*np.sin(np.pi/6)),
    ("sector_r06_phi30", 0.6*np.cos(np.pi/6), 0.6*np.sin(np.pi/6)),
    ("sector_r08_phi30", 0.8*np.cos(np.pi/6), 0.8*np.sin(np.pi/6)),
    ("generic_r04_phi20", 0.4*np.cos(np.deg2rad(20)), 0.4*np.sin(np.deg2rad(20))),
)


def angles_for(maps):
    values = []
    for M, b in maps.values():
        if np.linalg.det(M) <= 0 or np.linalg.norm(M-np.eye(3)) <= 2e-7:
            continue
        cosine = np.clip((np.trace(M)-1.0)/2.0, -1.0, 1.0)
        skew = np.array([M[2,1]-M[1,2], M[0,2]-M[2,0], M[1,0]-M[0,1]])
        sine = 0.5*np.linalg.norm(skew)
        values.append(float(np.degrees(np.arctan2(sine, cosine))))
    return np.sort(np.asarray(values))


def wasserstein_1d(a, b):
    q = np.linspace(0.0, 1.0, 1001)
    return float(np.mean(np.abs(np.quantile(a, q)-np.quantile(b, q))))


def main():
    for label, u, v in CONFIGS:
        snapshots = enumerate_depths(float(u), float(v), 8)
        distributions = {}
        for depth in (4, 6, 8):
            maps, raw, states = snapshots[depth]
            a = angles_for(maps)
            distributions[depth] = a
            quantiles = np.quantile(a, [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
            print(f"DEPTH_SPECTRUM,{label},{depth},raw={raw},maps={len(maps)},"
                  f"angles={len(a)},unique_angles={len(np.unique(np.round(a,7)))},"
                  f"count_lt1={int(np.sum(a<1))},count_lt5={int(np.sum(a<5))},"
                  f"count_lt10={int(np.sum(a<10))},"
                  f"quantiles={np.round(quantiles,7).tolist()}")
        print(f"DEPTH_DISTANCE,{label},4_to_6={wasserstein_1d(distributions[4], distributions[6]):.9g},"
              f"6_to_8={wasserstein_1d(distributions[6], distributions[8]):.9g}")
    print("LIMIT: empirical finite-depth distributions only; Wasserstein convergence is not a proof of group-limit convergence.")


if __name__ == "__main__":
    main()
