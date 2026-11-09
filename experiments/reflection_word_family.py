"""Exact classification of words in the four fixed face reflections.

Run:
    python experiments/reflection_word_family.py

All affine maps are represented exactly over fractions.Fraction.
A word (i,j,...) means apply reflection i, then j, and so on.
Adjacent equal generators are cancelled because s_i^2 = identity.
"""
from __future__ import annotations

import sys
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.boerdijk_coxeter_tetrahelix import INITIAL_VERTICES


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def matmul(A, B):
    return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), Q(0))
                       for j in range(3)) for i in range(3))


def matvec(A, v):
    return tuple(sum((A[i][k] * v[k] for k in range(3)), Q(0))
                 for i in range(3))


def det(A):
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


IDENTITY = tuple(tuple(Q(int(i == j)) for j in range(3)) for i in range(3))
ZERO = (Q(0), Q(0), Q(0))


def fixed_face_reflections():
    generators = []
    for omitted in range(4):
        face = [INITIAL_VERTICES[j] for j in range(4) if j != omitted]
        a, b, c = face
        n = cross(sub(b, a), sub(c, a))
        nn = dot(n, n)
        A = tuple(tuple(Q(int(i == j)) - 2 * n[i] * n[j] / nn
                         for j in range(3)) for i in range(3))
        na = dot(n, a)
        offset = tuple(2 * na * n[i] / nn for i in range(3))
        generators.append((A, offset))
    return tuple(generators)


def compose(after, before):
    """Affine composition: apply before, then after."""
    A, b = after
    C, d = before
    return (
        matmul(A, C),
        tuple(x + y for x, y in zip(matvec(A, d), b)),
    )


def axis_vector(A):
    rows = [tuple(A[i][j] - Q(int(i == j)) for j in range(3))
            for i in range(3)]
    for i in range(3):
        for j in range(i + 1, 3):
            v = cross(rows[i], rows[j])
            if dot(v, v) != 0:
                return v
    return None


def classify_isometry(transform):
    A, b = transform
    orientation = det(A)
    if orientation == -1:
        return "orientation_reversing", None, None
    trace = sum((A[i][i] for i in range(3)), Q(0))
    cosine = (trace - 1) / 2
    if A == IDENTITY:
        return ("identity" if b == ZERO else "translation"), cosine, None
    axis = axis_vector(A)
    if axis is None:
        raise AssertionError("non-identity proper isometry has no rotation axis")
    axial_shift_sq = dot(b, axis) ** 2 / dot(axis, axis)
    kind = "rotation" if axial_shift_sq == 0 else "screw"
    return kind, cosine, axial_shift_sq


def enumerate_words(max_length=6):
    generators = fixed_face_reflections()
    layers = {}
    previous = [((), (IDENTITY, ZERO))]
    for length in range(1, max_length + 1):
        current = []
        for word, transform in previous:
            for i, generator in enumerate(generators):
                if word and word[-1] == i:
                    continue
                current.append((word + (i,), compose(generator, transform)))
        layers[length] = current
        previous = current
    return layers


def main():
    layers = enumerate_words(6)
    expected_words = {1: 4, 2: 12, 3: 36, 4: 108, 5: 324, 6: 972}
    expected_types = {
        1: {"orientation_reversing": 4},
        2: {"rotation": 12},
        3: {"orientation_reversing": 36},
        4: {"rotation": 84, "screw": 24},
        5: {"orientation_reversing": 324},
        6: {"rotation": 516, "screw": 456},
    }
    for length, entries in layers.items():
        maps = [transform for _, transform in entries]
        assert len(entries) == expected_words[length]
        assert len(set(maps)) == len(maps), f"map collision at length {length}"
        counts = Counter(classify_isometry(t)[0] for t in maps)
        if length in expected_types:
            assert dict(counts) == expected_types[length], (length, counts)
        print(f"length {length}: {len(entries)} reduced words, "
              f"{len(set(maps))} distinct affine maps, {dict(counts)}")

    screws4 = []
    for word, transform in layers[4]:
        kind, cosine, shift_sq = classify_isometry(transform)
        if kind == "screw":
            screws4.append((word, cosine, shift_sq))
    assert len(screws4) == 24
    assert {cosine for _, cosine, _ in screws4} == {Q(-79, 81)}
    assert {shift_sq for _, _, shift_sq in screws4} == {Q(64, 5)}
    print("length-4 screw family: 24 words using all four distinct face generators")
    print("exact screw invariants: cos(rotation)=-79/81; axial_shift^2=64/5")
    print("length-2 family: 12 pure rotations with cos(rotation)=-7/9")
    # Finite-order rotation test via Niven's theorem. All matrix traces
    # are rational, so a rational angle multiple of pi can only have
    # cosine 0, +/-1/2, or +/-1.
    niven_values = {Q(0), Q(1, 2), Q(-1, 2), Q(1), Q(-1)}
    for length in (2, 4, 6, 8):
        cosines = Counter()
        finite_order = 0
        screw_count = 0
        for _, transform in layers[length]:
            kind, cosine, _ = classify_isometry(transform)
            if kind == "rotation":
                cosines[cosine] += 1
                finite_order += int(cosine in niven_values)
            elif kind == "screw":
                screw_count += 1
        assert finite_order == 0, (length, finite_order, cosines)
        print(f"even length {length}: rotation cosine spectrum={dict(sorted(cosines.items()))}; "
              f"finite-order rotations={finite_order}; screws={screw_count}")
    print("PASS: exact word-family classification through length 8; no finite-order pure rotations found.")
    print("LIMIT: these are fixed-face affine maps; BC uses a moving-face vertex recurrence. No knot classification is implied.")


if __name__ == "__main__":
    main()
