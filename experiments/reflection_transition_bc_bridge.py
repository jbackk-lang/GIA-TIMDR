"""Reproducible bridge check: generic surface reflection <-> exact BC recurrence.

Run from the repository root:
    python experiments/reflection_transition_bc_bridge.py

This checks geometry only. It does not infer a physical probability law.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.boerdijk_coxeter_tetrahelix import (
    INITIAL_VERTICES,
    generate_vertices,
    squared_distance,
)
from core.reflection_transition import (
    reflect_direction,
    reflect_tetrahedron_step,
    tetrahedron_face_reflection_candidates,
)


def main() -> None:
    exact = generate_vertices(40)
    floating = tuple(tuple(float(x) for x in p) for p in exact)

    # Compare the new generic operator against the exact Fraction recurrence.
    max_error = 0.0
    for i in range(len(floating) - 4):
        predicted = reflect_tetrahedron_step(floating[i:i + 4])
        expected = floating[i + 4]
        max_error = max(
            max_error,
            *(abs(predicted[k] - expected[k]) for k in range(3)),
        )
    assert max_error < 1e-12, max_error

    # The regular tetrahedron has four geometrically valid face-reflection
    # candidates. They are distinct but preserve all six edge lengths.
    initial = tuple(tuple(float(x) for x in p) for p in INITIAL_VERTICES)
    branches = tetrahedron_face_reflection_candidates(initial)
    assert len(branches) == 4
    branch_points = [branches[i][i] for i in range(4)]
    assert len({tuple(round(x, 12) for x in p) for p in branch_points}) == 4
    for tetra in branches:
        edge_squares = {
            round(sum((tetra[i][k] - tetra[j][k]) ** 2 for k in range(3)), 10)
            for i in range(4) for j in range(i + 1, 4)
        }
        assert edge_squares == {8.0}, edge_squares

    # Check the point-reflection/vector-reflection identity for one BC step.
    old, a, b, c, nxt = floating[:5]
    center = tuple((a[k] + b[k] + c[k]) / 3 for k in range(3))
    incoming = tuple(old[k] - center[k] for k in range(3))
    outgoing = tuple(nxt[k] - center[k] for k in range(3))
    normal = (
        (b[1]-a[1])*(c[2]-a[2]) - (b[2]-a[2])*(c[1]-a[1]),
        (b[2]-a[2])*(c[0]-a[0]) - (b[0]-a[0])*(c[2]-a[2]),
        (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]),
    )
    reflected = reflect_direction(incoming, normal)
    assert max(abs(reflected[k] - outgoing[k]) for k in range(3)) < 1e-12

    print("PASS: 36/36 BC steps agree with the exact Fraction reference (<1e-12).")
    print("PASS: four distinct face-reflection candidates preserve all six edges.")
    print("PASS: point reflection and vector reflection agree for the BC face.")
    print("NOTE: geometry does not select a probability distribution among branches.")
    print(f"Exact reference has {len(exact)} vertices; max float adapter error={max_error:.3e}.")


if __name__ == "__main__":
    main()
