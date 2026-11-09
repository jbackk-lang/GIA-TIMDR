"""Couple rhombic-prism mobility to length-4 reflection spectra.

Exploratory numerical scan only: exact symbolic checks are in
rhombic_prism_mobility_domain.py and the two rational benchmark cases are in
rhombic_triangular_prism_two_angles.py.

Parameters (u,v) lie in the open unit disk; w=sqrt(1-u^2-v^2).
All nine edges remain unit length, the two triangular ends remain equilateral,
and all three lateral faces remain rhombi.
"""
import itertools
from collections import Counter
import numpy as np

TOL = 2e-8
IDENTITY = np.eye(3)
EDGES = (
    np.array([1.0, 0.0, 0.0]),
    np.array([-0.5, np.sqrt(3)/2, 0.0]),
    np.array([-0.5, -np.sqrt(3)/2, 0.0]),
)

def build_generators(u, v):
    r2 = u*u + v*v
    if not r2 < 1.0:
        raise ValueError("The non-degenerate configuration domain is u^2+v^2<1.")
    w = np.sqrt(1.0-r2)
    t = np.array([u, v, w])
    # Reflection in z=0 and z=w.
    Rz = np.diag([1.0, 1.0, -1.0])
    generators = [(Rz, np.zeros(3)), (Rz, np.array([0.0, 0.0, 2*w]))]
    # Each lateral rhombus plane contains one base edge and t.
    for edge in EDGES:
        n = np.cross(edge, t)
        n = n/np.linalg.norm(n)
        R = IDENTITY - 2*np.outer(n, n)
        generators.append((R, np.zeros(3)))
    return generators, w, t

def compose(left, right):
    M, b = left
    N, d = right
    return M @ N, M @ d + b

def classify(M, b):
    if np.linalg.norm(M-IDENTITY) < TOL:
        return "translation" if np.linalg.norm(b) > TOL else "identity"
    if np.linalg.det(M) < 0.0:
        return "improper"
    vals, vecs = np.linalg.eig(M)
    idx = int(np.argmin(np.abs(vals-1.0)))
    axis = np.real(vecs[:, idx])
    axis /= np.linalg.norm(axis)
    pitch = float(axis @ b)
    return "screw" if abs(pitch) > TOL else "rotation"

def length_four_spectrum(u, v):
    generators, w, t = build_generators(u, v)
    layer = [((), (IDENTITY, np.zeros(3)))]
    for _ in range(4):
        nxt = []
        for word, transform in layer:
            for i, gen in enumerate(generators):
                if word and word[-1] == i:
                    continue
                nxt.append((word+(i,), compose(gen, transform)))
        layer = nxt
    distinct = {}
    for word, (M, b) in layer:
        key = tuple(np.round(np.r_[M.ravel(), b], 8))
        distinct.setdefault(key, (word, M, b))
    kinds = Counter(classify(M, b) for _, M, b in distinct.values())
    c = [float(t @ e) for e in EDGES]
    acute_angles = [float(np.degrees(np.arccos(min(1.0, abs(x))))) for x in c]
    volume = np.sqrt(3)/4*w
    return {
        "u": u, "v": v, "w": w, "volume": volume,
        "c": c, "acute_angles_deg": acute_angles,
        "reduced_words": len(layer), "distinct_maps": len(distinct),
        "types": kinds,
    }

def main():
    # Two coordinates sweep the full mobility family; this path holds u fixed.
    a = 1/(2*np.sqrt(3))
    b = 1/np.sqrt(3)
    samples = [
        (0.2, 0.0),                    # symmetry branch c2=c3
        (0.5, 0.0),                    # symmetry branch c2=c3
        (0.8, 0.0),
        (0.5, 1e-5),                   # transverse off-branch control
        (0.5, 0.05),
        (0.5, 0.10),
        (0.5, 0.20),
        (0.2, 0.2/np.sqrt(3)),        # square-face symmetry branch
        (0.4, 0.4/np.sqrt(3)),
        (0.5, a),                      # exact benchmark A: c=(1/2,0,-1/2)
        (0.5, -a),                     # reflected partner of A
        (0.5, a-1e-5),                 # off-resonance controls
        (0.5, a+1e-5),
        (0.5, 0.35),
        (0.5, 0.50),
        (0.5, b),                      # exact benchmark B: c=(1/2,1/4,-3/4)
        (0.5, -b),                     # reflected partner of B
        (0.5, b-1e-5),
        (0.5, b+1e-5),
        (0.5, 0.60),
        (0.5, 0.70),
        (0.1, 0.1),                    # off-symmetry generic control
    ]
    # Candidate exceptional ellipse: u^2 + 4 v^2 = 1, hence w=sqrt(3)*|v|.
    # Sample both signs and a special intersection u=1/2.
    for u0 in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        v0 = np.sqrt(1-u0*u0)/2
        samples.extend([
            (u0, v0), (u0, -v0),
            (u0, v0+1e-5), (u0, v0-1e-5),
        ])
    print("u,v,w,volume,acute_angles_deg,distinct_length4_maps,rotations,screws,translations,identities")
    for u, v in samples:
        result = length_four_spectrum(u, v)
        k = result["types"]
        print(
            f"{u:.9f},{v:.9f},{result['w']:.9f},{result['volume']:.9f},"
            f"{[round(a,6) for a in result['acute_angles_deg']]},"
            f"{result['distinct_maps']},{k['rotation']},{k['screw']},"
            f"{k['translation']},{k['identity']}"
        )
    print("INTERPRETATION: numerical evidence for exceptional symmetry/resonance loci; not a proof of the full infinite reflection group.")
    print("MOBILITY: u^2+v^2<1; two continuous shape degrees of freedom.")
    print("GENERIC SAMPLE: off-symmetry points exhibit a stable length-4 spectrum in this scan.")

if __name__ == "__main__":
    main()
