"""Exact rational construction of the Boerdijk-Coxeter tetrahelix.

This is a reference geometry, not an assertion that it is identical to a
TIMDR helix. Coordinates use a regular tetrahedron with vertices
(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1), so every edge has
squared length 8.

The next vertex is obtained by reflecting the oldest of the last four
vertices through the plane of the other three. All recurrence arithmetic is
exact (fractions.Fraction).

For this coordinate convention the vertex-to-vertex screw map is
    p_next = p @ R + t
with the exact rational R and t below. Its screw rotation angle has
cos(theta) = -2/3. This is distinct from the regular tetrahedron's
interior dihedral angle, whose cosine is +1/3.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Sequence

Q = Fraction
Vector = tuple[Q, Q, Q]

INITIAL_VERTICES: tuple[Vector, ...] = (
    (Q(1), Q(1), Q(1)),
    (Q(1), Q(-1), Q(-1)),
    (Q(-1), Q(1), Q(-1)),
    (Q(-1), Q(-1), Q(1)),
)

SCREW_ROTATION: tuple[Vector, ...] = (
    (Q(2, 3), Q(2, 3), Q(-1, 3)),
    (Q(2, 3), Q(-1, 3), Q(2, 3)),
    (Q(1, 3), Q(-2, 3), Q(-2, 3)),
)
SCREW_TRANSLATION: Vector = (Q(-2, 3), Q(-2, 3), Q(-2, 3))


def _sub(a: Vector, b: Vector) -> Vector:
    return tuple(x - y for x, y in zip(a, b))  # type: ignore[return-value]


def _add(a: Vector, b: Vector) -> Vector:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def _scale(s: Q, v: Vector) -> Vector:
    return tuple(s * x for x in v)  # type: ignore[return-value]


def _dot(a: Vector, b: Vector) -> Q:
    return sum((x * y for x, y in zip(a, b)), Q(0))


def _cross(a: Vector, b: Vector) -> Vector:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def reflect_point_in_plane(point: Vector, a: Vector, b: Vector, c: Vector) -> Vector:
    """Reflect point in the plane through a,b,c using exact rational arithmetic."""
    normal = _cross(_sub(b, a), _sub(c, a))
    norm_sq = _dot(normal, normal)
    if norm_sq == 0:
        raise ValueError("plane-defining points must not be collinear")
    signed_factor = Q(2) * _dot(_sub(point, a), normal) / norm_sq
    return _sub(point, _scale(signed_factor, normal))


def generate_vertices(count: int) -> tuple[Vector, ...]:
    """Generate count consecutive vertices; at least four are required."""
    if count < 4:
        raise ValueError("count must be at least 4")
    vertices = list(INITIAL_VERTICES)
    while len(vertices) < count:
        # Reflect the oldest vertex of the current tetrahedron through the
        # opposite face; this appends a congruent tetrahedron to the chain.
        vertices.append(
            reflect_point_in_plane(vertices[-4], vertices[-3], vertices[-2], vertices[-1])
        )
    return tuple(vertices)


def screw_step(point: Vector) -> Vector:
    """Apply the exact fixed screw map, using row-vector coordinates."""
    rotated = tuple(
        sum((point[i] * SCREW_ROTATION[i][j] for i in range(3)), Q(0))
        for j in range(3)
    )
    return _add(rotated, SCREW_TRANSLATION)  # type: ignore[arg-type]


def tetrahedron_centroid(vertices: Sequence[Vector]) -> Vector:
    """Return the exact centroid of four vertices."""
    if len(vertices) != 4:
        raise ValueError("a tetrahedron requires exactly four vertices")
    return tuple(
        sum((v[j] for v in vertices), Q(0)) / 4 for j in range(3)
    )  # type: ignore[return-value]


def squared_distance(a: Vector, b: Vector) -> Q:
    delta = _sub(a, b)
    return _dot(delta, delta)


def screw_parameters() -> dict[str, str]:
    """Exact invariant parameters for this coordinate convention.

    Axis direction is (2,1,0)/sqrt(5), axis point is (0,0,-2/5),
    vertex radius is 3*sqrt(6)/5, and signed axial advance per vertex is
    -2/sqrt(5). The rotation angle obeys cos(theta)=-2/3.
    """
    return {
        "axis_direction": "(2,1,0)/sqrt(5)",
        "axis_point": "(0,0,-2/5)",
        "vertex_radius": "3*sqrt(6)/5",
        "axial_advance_per_vertex": "-2/sqrt(5)",
        "screw_rotation_angle": "acos(-2/3)",
        "tetrahedron_interior_dihedral_angle": "acos(1/3)",
    }
