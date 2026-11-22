"""Central-point orbit and screw-geometry diagnostics for the rhombic-prism reflections.

Run from the repository root:
    python experiments/rhombic_prism_center_orbit_geometry.py

Uses existing generators. Finite-depth diagnostics do not establish a physical
vortex, fractal dimension, or a closed-form limit.
"""
import numpy as np
from rhombic_prism_mobility_screw_coupling import build_generators, compose, IDENTITY
from rhombic_prism_axis_limit_study import extract_axis

def center(u, v):
    w = np.sqrt(1.0 - u*u - v*v)
    return np.array([(1.0+u)/2.0, np.sqrt(3.0)/6.0+v/2.0, w/2.0])

def audit(u, v, max_depth=5, decimals=10):
    gens, w, _ = build_generators(u, v)
    O = center(u, v)
    # Two horizontal reflections produce an exact vertical translation.
    trans = compose(gens[1], gens[0])
    assert np.allclose(trans[0], IDENTITY, atol=1e-12)
    assert np.allclose(trans[1], [0, 0, 2*w], atol=1e-12)
    states = [((), (IDENTITY, np.zeros(3)))]
    cumulative_points = {tuple(np.round(O, decimals))}
    print(f"CONFIG,u={u:.9g},v={v:.9g},w={w:.9g},center={O.tolist()}")
    for depth in range(1, max_depth+1):
        next_states = []
        for word, transform in states:
            for i, gen in enumerate(gens):
                if word and i == word[-1]:
                    continue
                g = compose(gen, transform)
                next_states.append((word + (i,), g))
        states = next_states
        positions = np.array([g[0] @ O + g[1] for _, g in states])
        cumulative_points.update(tuple(np.round(p, decimals)) for p in positions)
        displacements = np.array(list(cumulative_points)) - O
        max_radius = float(np.max(np.linalg.norm(displacements, axis=1)))
        # Reflection generators fix O only in special circumstances.
        print(f"DEPTH,{depth},distinct_center_positions={len(cumulative_points)},"
              f"max_center_distance={max_radius:.9g},nw={depth*w:.9g}")
        # Only proper isometries have rotation/screw axes.
        if depth % 2 == 0:
            checked = 0
            max_error = 0.0
            for _, (M, b) in states:
                kind, result = extract_axis(M, b, min_angle_deg=1.0)
                if kind not in ("rotation_axis", "screw_axis"):
                    continue
                a, p, h, angle, _, _ = result
                rho = np.linalg.norm(np.cross(O-p, a))
                predicted = 4*rho*rho*np.sin(np.deg2rad(angle)/2)**2 + h*h
                actual = float(np.dot(M@O+b-O, M@O+b-O))
                max_error = max(max_error, abs(predicted-actual))
                checked += 1
            print(f"SCREW_IDENTITY,{depth},checked={checked},max_abs_error={max_error:.6g}")

def main():
    for u, v in ((0.0,0.0),(0.01,0.0),(0.2,0.1),
                 (0.4/np.sqrt(2),0.4/np.sqrt(2))):
        audit(u,v)
    print("LIMIT: finite-depth orbit data; no physical-dynamics claim.")

if __name__ == "__main__":
    main()
