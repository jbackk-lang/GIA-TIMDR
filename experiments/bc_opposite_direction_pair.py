"""Oppositely directed BC screw strands from one tetrahedral seed.

This is an exact-rational geometry experiment. It compares forward and
inverse iterates of the same BC screw isometry, launched from distinct
vertices of the same regular tetrahedron. It does not claim a physical
interaction or a knot/link classification.
"""
from __future__ import annotations

import sys
from pathlib import Path
from fractions import Fraction as Q

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.boerdijk_coxeter_tetrahelix import (
    INITIAL_VERTICES, SCREW_ROTATION, SCREW_TRANSLATION,
    _dot, _sub, _cross,
)


def transpose(A):
    return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))


def mv(A, p):
    return tuple(sum((A[i][j] * p[j] for j in range(3)), Q(0))
                 for i in range(3))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def screw(p):
    return add(mv(transpose(SCREW_ROTATION), p), SCREW_TRANSLATION)


def inverse_screw(p):
    # Given row-vector convention p' = p R + t, inverse is (p'-t) R^T.
    return mv(SCREW_ROTATION, sub(p, SCREW_TRANSLATION))


def orbit(seed, step, count):
    out = [seed]
    for _ in range(count):
        out.append(step(out[-1]))
    return tuple(out)


def main():
    # Axis direction u=(2,1,0)/sqrt(5); a point on the axis is (0,0,-2/5).
    # The perpendicular radius squared is computed exactly.
    axis_point = (Q(0), Q(0), Q(-2, 5))
    axis_dir = (Q(2), Q(1), Q(0))
    norm_sq = _dot(axis_dir, axis_dir)

    def radius_sq(p):
        v = sub(p, axis_point)
        projection_sq = _dot(v, axis_dir) ** 2 / norm_sq
        return _dot(v, v) - projection_sq

    def axial_coordinate(p):
        return _dot(sub(p, axis_point), axis_dir)

    # Two strands share one tetrahedral launch configuration but start at
    # different vertices and move in opposite screw directions.
    a0, b0 = INITIAL_VERTICES[0], INITIAL_VERTICES[1]
    forward = orbit(a0, screw, 64)
    backward = orbit(b0, inverse_screw, 64)

    assert all(radius_sq(p) == radius_sq(a0) for p in forward)
    assert all(radius_sq(p) == radius_sq(b0) for p in backward)
    assert radius_sq(a0) == radius_sq(b0)

    # Exact point-collision check on finite sampled pieces.
    collisions = [(i, j) for i, p in enumerate(forward)
                  for j, q in enumerate(backward) if p == q]
    assert not collisions

    # The signed axial increments must be equal and opposite.
    da = axial_coordinate(forward[1]) - axial_coordinate(forward[0])
    db = axial_coordinate(backward[1]) - axial_coordinate(backward[0])
    assert da == -db
    assert da != 0

    # Both strands are on the same cylinder, with opposite axial motion.
    # The phase offset is read from their exact initial radial vectors.
    ra = sub(a0, axis_point)
    rb = sub(b0, axis_point)
    ra_perp = sub(ra, tuple(axis_dir[k] * _dot(ra, axis_dir) / norm_sq
                            for k in range(3)))
    rb_perp = sub(rb, tuple(axis_dir[k] * _dot(rb, axis_dir) / norm_sq
                            for k in range(3)))
    cross_norm_sq = _dot(_cross(ra_perp, rb_perp), _cross(ra_perp, rb_perp))
    dot_radial = _dot(ra_perp, rb_perp)
    assert cross_norm_sq != 0

    print("PASS: 65 exact points generated on each oppositely directed strand.")
    print(f"radius_squared_A = {radius_sq(a0)}")
    print(f"radius_squared_B = {radius_sq(b0)}")
    print(f"axial_step_forward = {da}")
    print(f"axial_step_backward = {db}")
    print(f"radial_dot_product = {dot_radial}")
    print(f"radial_cross_norm_squared = {cross_norm_sq}")
    print("sampled_exact_point_collisions = 0")
    print("RESULT: two distinct, coaxial, equal-radius screw orbits with opposite axial advance.")
    print("LIMIT: infinite/open strands have no classical linking number; no knot/link claim is made.")


if __name__ == "__main__":
    main()
