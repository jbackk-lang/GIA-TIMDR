"""Deterministic reflection and optional branch kernel for TIMDR.

This module keeps three operations separate:
1. geometric surface normal,
2. deterministic specular reflection,
3. optional probability distribution over an explicitly supplied branch set.

It does not claim that reflection creates a fractal or that a probability
kernel is a physical law. All coordinates use a caller-declared convention.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, sqrt
from typing import Sequence

Vector = tuple[float, float, float]


def _dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def _cross(a: Vector, b: Vector) -> Vector:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _norm(v: Vector) -> float:
    return sqrt(_dot(v, v))


def _unit(v: Vector, *, name: str) -> Vector:
    n = _norm(v)
    if not isfinite(n) or n <= 1e-14:
        raise ValueError(f"{name} must be finite and non-zero")
    return tuple(x / n for x in v)  # type: ignore[return-value]


def surface_normal(du: Vector, dv: Vector) -> Vector:
    """Unit normal from two tangent vectors of a regular parameterized surface."""
    return _unit(_cross(du, dv), name="surface tangent cross product")


def reflect_direction(incoming: Vector, normal: Vector) -> Vector:
    """Specular reflection u_out = u_in - 2(u_in·n)n.

    The normal is normalized internally. The magnitude of incoming is
    preserved; incoming need not be a unit vector.
    """
    n = _unit(normal, name="normal")
    if not all(isfinite(x) for x in incoming):
        raise ValueError("incoming direction must be finite")
    projection = _dot(incoming, n)
    out = tuple(incoming[i] - 2.0 * projection * n[i] for i in range(3))
    return out  # type: ignore[return-value]


@dataclass(frozen=True)
class ReflectionEvent:
    time: float
    position: Vector
    incoming: Vector
    normal: Vector

    def __post_init__(self) -> None:
        if not isfinite(self.time):
            raise ValueError("event time must be finite")
        if not all(isfinite(x) for x in self.position):
            raise ValueError("event position must be finite")
        _unit(self.incoming, name="incoming direction")
        _unit(self.normal, name="normal")


@dataclass(frozen=True)
class ReflectionResult:
    time: float
    position: Vector
    incoming: Vector
    normal: Vector
    outgoing: Vector
    incidence_angle_rad: float
    reflection_angle_rad: float


def reflect_event(event: ReflectionEvent) -> ReflectionResult:
    """Apply the deterministic reflection law at one event."""
    incoming = _unit(event.incoming, name="incoming direction")
    normal = _unit(event.normal, name="normal")
    outgoing = _unit(reflect_direction(incoming, normal), name="outgoing direction")
    # Unsigned angles measured from the normal line.
    from math import acos
    ci = min(1.0, max(0.0, abs(_dot(incoming, normal))))
    cr = min(1.0, max(0.0, abs(_dot(outgoing, normal))))
    return ReflectionResult(
        time=event.time,
        position=event.position,
        incoming=incoming,
        normal=normal,
        outgoing=outgoing,
        incidence_angle_rad=acos(ci),
        reflection_angle_rad=acos(cr),
    )


def branch_probabilities(costs: Sequence[float], beta: float = 1.0) -> tuple[float, ...]:
    """Optional normalized softmax kernel over a non-empty candidate set.

    This is a mathematical model family only. The caller must justify costs
    and beta from data or a preregistered hypothesis. Lower cost gets higher
    probability. Empty candidate sets are invalid rather than normalized.
    """
    if not costs:
        raise ValueError("at least one admissible branch is required")
    if not isfinite(beta) or beta < 0:
        raise ValueError("beta must be finite and non-negative")
    if any(not isfinite(float(c)) for c in costs):
        raise ValueError("all branch costs must be finite")
    if beta == 0:
        p = 1.0 / len(costs)
        return tuple(p for _ in costs)
    logits = tuple(-beta * float(c) for c in costs)
    shift = max(logits)
    weights = tuple(exp(x - shift) for x in logits)
    total = sum(weights)
    return tuple(w / total for w in weights)


def reflect_point_in_plane(point: Vector, plane_point: Vector, normal: Vector) -> Vector:
    """Reflect a point across a plane specified by one point and its normal."""
    n = _unit(normal, name="plane normal")
    if not all(isfinite(x) for x in point + plane_point):
        raise ValueError("point and plane point must be finite")
    offset = tuple(point[i] - plane_point[i] for i in range(3))
    reflected_offset = reflect_direction(offset, n)
    return tuple(plane_point[i] + reflected_offset[i] for i in range(3))  # type: ignore[return-value]


def reflect_tetrahedron_step(vertices: Sequence[Vector]) -> Vector:
    """BC bridge: reflect the oldest vertex across the face of the other three.

    Input order is (oldest, face_a, face_b, face_c). The result is the
    next vertex in the face-reflected tetrahedral chain. This is a floating
    point adapter for the exact Fraction reference in
    core.boerdijk_coxeter_tetrahelix; use that module for exact arithmetic.
    """
    if len(vertices) != 4:
        raise ValueError("exactly four tetrahedron vertices are required")
    point, a, b, c = vertices
    normal = _cross(
        tuple(b[i] - a[i] for i in range(3)),
        tuple(c[i] - a[i] for i in range(3)),
    )
    return reflect_point_in_plane(point, a, normal)
