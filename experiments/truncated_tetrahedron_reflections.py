"""Exact reflection geometry of a tetrahedron truncated by a parallel cut.

The original regular tetrahedron has vertices (1,1,1), (1,-1,-1),
(-1,1,-1), (-1,-1,1). A vertex is truncated at fraction q along each
incident edge. The resulting five face planes are:
  base: x+y+z=-1
  cut:  x+y+z=3-4q
  sides: x-y-z=-1, -x+y-z=-1, -x-y+z=-1

All calculations use Fraction arithmetic. q is a geometric parameter in (0,1).
"""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations

I = tuple(tuple(Q(int(i == j)) for j in range(3)) for i in range(3))
ZERO = (Q(0), Q(0), Q(0))
A_VERTEX = (Q(1), Q(1), Q(1))
B_VERTICES = (
    (Q(1), Q(-1), Q(-1)),
    (Q(-1), Q(1), Q(-1)),
    (Q(-1), Q(-1), Q(1)),
)
SIDE_NORMALS = (
    (Q(1), Q(-1), Q(-1)),
    (Q(-1), Q(1), Q(-1)),
    (Q(-1), Q(-1), Q(1)),
)

def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))

def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )

def mv(M, x):
    return tuple(sum((M[i][j] * x[j] for j in range(3)), Q(0)) for i in range(3))

def mm(M, N):
    return tuple(
        tuple(sum((M[i][k] * N[k][j] for k in range(3)), Q(0)) for j in range(3))
        for i in range(3)
    )

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def compose(after, before):
    """Affine composition after(before(x)); maps are (matrix, translation)."""
    M, b = after
    N, d = before
    return mm(M, N), add(mv(M, d), b)

def reflect(normal, offset):
    """Reflection in n.x = c."""
    nn = dot(normal, normal)
    M = tuple(
        tuple(Q(int(i == j)) - 2 * normal[i] * normal[j] / nn for j in range(3))
        for i in range(3)
    )
    b = tuple(2 * offset * normal[i] / nn for i in range(3))
    return M, b

def generators(q):
    assert 0 < q < 1
    return (
        reflect((Q(1), Q(1), Q(1)), Q(-1)),
        reflect((Q(1), Q(1), Q(1)), Q(3) - 4 * q),
        *(reflect(n, Q(-1)) for n in SIDE_NORMALS),
    )

def identity_map(T):
    return T == (I, ZERO)

def axis_vector(M):
    """Exact nonzero vector in ker(M-I), for a nonidentity 3D rotation."""
    rows = [tuple(M[i][j] - I[i][j] for j in range(3)) for i in range(3)]
    for i, j in combinations(range(3), 2):
        u = cross(rows[i], rows[j])
        if u != ZERO:
            return u
    raise AssertionError("nonidentity proper rotation has no recovered axis")

def isometry_type(T):
    M, b = T
    if M == I:
        return "identity" if b == ZERO else "translation"
    u = axis_vector(M)
    return "screw" if dot(u, b) != 0 else "rotation"

def enumerate_words(q, max_length=8):
    G = generators(q)
    layer = [((), (I, ZERO))]
    stats = {}
    maps_by_length = {}
    words_by_length = {}
    for length in range(1, max_length + 1):
        next_layer = []
        unique = {}
        for word, T in layer:
            for i, generator in enumerate(G):
                if word and word[-1] == i:
                    continue
                new_word = word + (i,)
                new_T = compose(generator, T)
                next_layer.append((new_word, new_T))
                unique.setdefault(new_T, new_word)
        stats[length] = (len(next_layer), len(unique))
        maps_by_length[length] = unique
        words_by_length[length] = next_layer
        layer = next_layer
    return stats, maps_by_length, words_by_length

def resonance_roots(length):
    """Find q in (0,1) where an even-word screw pitch becomes zero.

    The rotation matrix is independent of q; the translation vector is affine
    in q. Evaluate at q=0 and q=1 to recover the exact linear pitch function.
    Counts are reduced words, not unique affine maps.
    """
    G0 = (
        reflect((Q(1), Q(1), Q(1)), Q(-1)),
        reflect((Q(1), Q(1), Q(1)), Q(3)),
        *(reflect(n, Q(-1)) for n in SIDE_NORMALS),
    )
    G1 = (
        reflect((Q(1), Q(1), Q(1)), Q(-1)),
        reflect((Q(1), Q(1), Q(1)), Q(-1)),
        *(reflect(n, Q(-1)) for n in SIDE_NORMALS),
    )
    layer = [((), (I, ZERO), (I, ZERO))]
    roots = Counter()
    parameter_independent_rotations = 0
    for _ in range(1, length + 1):
        next_layer = []
        for word, T0, T1 in layer:
            for i in range(5):
                if word and word[-1] == i:
                    continue
                next_layer.append((
                    word + (i,),
                    compose(G0[i], T0),
                    compose(G1[i], T1),
                ))
        layer = next_layer
    for word, T0, T1 in layer:
        M, b0 = T0
        _, b1 = T1
        if M == I:
            continue
        u = axis_vector(M)
        p0, p1 = dot(u, b0), dot(u, b1)
        if p0 == 0 and p1 == 0:
            parameter_independent_rotations += 1
        elif p0 != p1:
            q0 = -p0 / (p1 - p0)
            if 0 < q0 < 1:
                roots[q0] += 1
    return roots, parameter_independent_rotations

def main():
    q = Q(1, 2)
    G = generators(q)

    # Check the actual five-faced truncated tetrahedron.
    cut_vertices = tuple(
        tuple(A_VERTEX[k] + q * (B[k] - A_VERTEX[k]) for k in range(3))
        for B in B_VERTICES
    )
    assert cut_vertices == (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    )
    assert all(sum(v) == -1 for v in B_VERTICES)
    assert all(sum(v) == 1 for v in cut_vertices)
    for n, omitted in zip(SIDE_NORMALS, B_VERTICES):
        assert dot(n, A_VERTEX) == -1
        assert all(dot(n, v) == -1 for v in B_VERTICES if v != omitted)
        assert all(dot(n, p) == -1 for p, v in zip(cut_vertices, B_VERTICES) if v != omitted)

    # Every face reflection is an exact involutive Euclidean isometry.
    for S in G:
        assert compose(S, S) == (I, ZERO)
        M, _ = S
        assert mm(tuple(zip(*M)), M) == I

    # One parallel pair produces a translation; the other nine pairs rotate.
    pair_types = Counter()
    rotation_cosines = set()
    parallel_translation = None
    for i, j in combinations(range(5), 2):
        T = compose(G[i], G[j])
        kind = isometry_type(T)
        pair_types[kind] += 1
        if kind == "rotation":
            rotation_cosines.add((sum((T[0][k][k] for k in range(3)), Q(0)) - 1) / 2)
        elif kind == "translation":
            parallel_translation = T[1]
    assert pair_types == Counter({"rotation": 9, "translation": 1})
    assert rotation_cosines == {Q(-7, 9)}
    assert parallel_translation == (Q(-4, 3), Q(-4, 3), Q(-4, 3))

    stats, maps, _ = enumerate_words(q, 8)
    expected = {
        1: (5, 5), 2: (20, 20), 3: (80, 80), 4: (320, 320),
        5: (1280, 1280), 6: (5120, 5102), 7: (20480, 20372),
        8: (81920, 81242),
    }
    assert stats == expected, stats

    even_types = {}
    for length in (2, 4, 6, 8):
        counts = Counter(isometry_type(T) for T in maps[length])
        even_types[length] = dict(counts)

    roots6, fixed6 = resonance_roots(6)
    roots8, fixed8 = resonance_roots(8)
    assert dict(sorted(roots6.items())) == {
        Q(1, 4): 72, Q(1, 3): 108, Q(1, 2): 36
    }
    assert fixed6 == 1572
    assert len(roots8) == 25
    assert fixed8 == 11724

    print("PASS: exact truncated-tetrahedron geometry at q=1/2.")
    print("faces=5 (two parallel triangles + three quadrilaterals)")
    print("cut vertices=(1,0,0),(0,1,0),(0,0,1)")
    print("face-pair products: 9 rotations with cos(theta)=-7/9; 1 translation")
    print("parallel-face translation vector=(-4/3,-4/3,-4/3); length=4/sqrt(3)")
    for n, (words, distinct) in stats.items():
        print(f"length_{n}: reduced_words={words}; distinct_affine_maps={distinct}; collisions={words-distinct}")
    for n, counts in even_types.items():
        print(f"even_length_{n}_isometry_types={counts}")
    print(f"length_6_zero_pitch_resonances={dict(sorted(roots6.items()))}")
    print(f"length_8_zero_pitch_resonance_count={len(roots8)} distinct rational q values")
    print(f"length_8_zero_pitch_resonances={dict(sorted(roots8.items()))}")
    print(f"parameter_independent_pure_rotations: length6={fixed6}; length8={fixed8}")
    print("RESULT: truncation depth changes screw pitch; exact rational depths create zero-pitch resonances.")
    print("LIMIT: finite word search does not prove global closure, knotting, or physical interaction.")

if __name__ == "__main__":
    main()
