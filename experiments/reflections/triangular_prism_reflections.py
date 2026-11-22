"""Exact reflection geometry of a regular triangular prism with square sides.

The prism has unit equilateral triangular ends and unit-height square sides.
Its five face planes generate the product of the affine A2 reflection group
in the triangular plane and the infinite dihedral group along the prism axis.
Exact arithmetic uses SymPy and sqrt(3).
"""
import sympy as s
from itertools import combinations
from collections import Counter

r3 = s.sqrt(3)
I = s.eye(3)
O = s.zeros(3, 1)

# Equilateral triangle vertices (0,0), (1,0), (1/2,sqrt(3)/2).
# Side-plane equations, extruded vertically:
# bottom edge y=0; diagonal edge sqrt(3)x+y=sqrt(3);
# diagonal edge sqrt(3)x-y=0.
planes = [
    (s.Matrix([0, 0, 1]), 0),       # lower triangle: z=0
    (s.Matrix([0, 0, 1]), 1),       # upper triangle: z=1
    (s.Matrix([0, 1, 0]), 0),       # square side 1
    (s.Matrix([r3, 1, 0]), r3),     # square side 2
    (s.Matrix([r3, -1, 0]), 0),     # square side 3
]

def reflection(normal, offset):
    n = s.Matrix(normal)
    M = I - 2 * (n * n.T) / n.dot(n)
    b = 2 * offset * n / n.dot(n)
    return M.applyfunc(s.simplify), b.applyfunc(s.simplify)

def compose(A, B):
    """A after B."""
    M, b = A
    N, d = B
    return ((M*N).applyfunc(s.simplify), (M*d+b).applyfunc(s.simplify))

def equal(A, B):
    return all(s.simplify(x-y) == 0 for x, y in zip(tuple(A[0])+tuple(A[1]), tuple(B[0])+tuple(B[1])))

def power(T, n):
    out = (I, O)
    for _ in range(n):
        out = compose(T, out)
    return out

def main():
    G = [reflection(n, c) for n, c in planes]
    for S in G:
        assert equal(compose(S, S), (I, O))

    pair_types = Counter()
    rotation_cosines = Counter()
    pair_products = {}
    for i, j in combinations(range(5), 2):
        T = compose(G[i], G[j])
        M, b = T
        if M == I:
            kind = "translation" if b != O else "identity"
        else:
            kind = "rotation"
            cosine = s.simplify((s.trace(M)-1)/2)
            rotation_cosines[str(cosine)] += 1
        pair_types[kind] += 1
        pair_products[(i, j)] = T

    assert pair_types == Counter({"rotation": 9, "translation": 1}), pair_types
    assert rotation_cosines == Counter({"-1": 6, "-1/2": 3}), rotation_cosines

    # The three vertical side reflections form the affine A2 Coxeter group:
    # every pair product is a 120-degree rotation of order 3.
    for i, j in ((2, 3), (2, 4), (3, 4)):
        assert equal(power(pair_products[(i, j)], 3), (I, O))

    # The two horizontal reflections generate an axial translation by 2.
    axial = pair_products[(0, 1)]
    assert axial[0] == I
    assert axial[1] == s.Matrix([0, 0, -2])

    # Horizontal reflections commute with all vertical side reflections.
    for i in (0, 1):
        for j in (2, 3, 4):
            assert equal(compose(G[i], G[j]), compose(G[j], G[i]))

    # Therefore the full group is a direct product:
    # affine A2 (triangular tiling in xy) x infinite dihedral (z).
    # Its translation subgroup has rank 3. All generators preserve the
    # horizontal/vertical splitting, so no screw component is generated.
    print("PASS: exact regular triangular prism reflection experiment.")
    print("faces=5 (2 equilateral triangles + 3 squares)")
    print(f"pair_products={dict(pair_types)}")
    print(f"rotation_cosines={dict(rotation_cosines)}")
    print("side-side: 3 rotations by 120 degrees, each of order 3")
    print("end-side: 6 rotations by 180 degrees, each of order 2")
    print("end-end: translation by 2 units along prism axis")
    print("side_reflection_group=affine_A2 (equilateral triangular tiling)")
    print("axial_reflection_group=infinite_dihedral")
    print("full_group=affine_A2 x infinite_dihedral")
    print("translation_subgroup_rank=3")
    print("screw_motions=none; nonzero_screw_pitch_resonances=none")
    print("LIMIT: this is the ideal prism with square sides (height equals triangle side).")

if __name__ == "__main__":
    main()
