"""Exact multi-branch reflection-tree and two-face subgroup experiment.

Run from the repository root:
    python experiments/reflection_branch_tree.py

All geometry in this experiment uses fractions.Fraction. No probabilities
or scale contractions are imposed.
"""
from __future__ import annotations

import sys
from pathlib import Path
from fractions import Fraction as Q

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.boerdijk_coxeter_tetrahelix import (
    INITIAL_VERTICES,
    _cross,
    _dot,
    _sub,
    reflect_point_in_plane,
)


def canonical(tetra):
    return tuple(sorted(tetra))


def reflect_across_opposite_face(tetra, index):
    face = [tetra[j] for j in range(4) if j != index]
    moved = reflect_point_in_plane(tetra[index], *face)
    result = list(tetra)
    result[index] = moved
    return tuple(result)


def children(tetra):
    return tuple(reflect_across_opposite_face(tetra, i) for i in range(4))


def centroid(tetra):
    return tuple(sum((p[k] for p in tetra), Q(0)) / 4 for k in range(3))


def squared_distance_to_line(point, a, b):
    direction = _sub(b, a)
    offset = _sub(point, a)
    cross = _cross(offset, direction)
    return _dot(cross, cross) / _dot(direction, direction)


def reflect_tetrahedron_in_fixed_plane(tetra, face_index):
    face = [INITIAL_VERTICES[j] for j in range(4) if j != face_index]
    return tuple(reflect_point_in_plane(p, *face) for p in tetra)


def branch_tree(max_depth=7):
    initial = tuple(INITIAL_VERTICES)
    frontier = {canonical(initial): initial}
    seen = set(frontier)
    counts = [1]
    centers_seen = set()
    center_counts = []
    for depth in range(max_depth + 1):
        layer_centers = {centroid(t) for t in frontier.values()}
        overlap = len(layer_centers & centers_seen)
        assert overlap == 0, (depth, overlap)
        centers_seen.update(layer_centers)
        center_counts.append(len(layer_centers))
        assert len(layer_centers) == len(frontier)
        if depth == max_depth:
            break
        next_frontier = {}
        for tetra in frontier.values():
            for child in children(tetra):
                key = canonical(child)
                if key not in seen:
                    next_frontier[key] = child
        frontier = next_frontier
        seen.update(frontier)
        counts.append(len(frontier))
    expected = [1] + [4 * (3 ** (d - 1)) for d in range(1, max_depth + 1)]
    assert counts == expected, (counts, expected)
    return counts, center_counts, len(seen)


def two_face_rotation(iterations=24):
    # Face 0 and face 1 intersect along the edge joining vertices 2 and 3.
    tetra = tuple(INITIAL_VERTICES)
    axis_a, axis_b = INITIAL_VERTICES[2], INITIAL_VERTICES[3]
    centers = []
    distances = []
    for step in range(iterations):
        centers.append(centroid(tetra))
        distances.append(squared_distance_to_line(centers[-1], axis_a, axis_b))
        plane_index = step % 2
        tetra = reflect_tetrahedron_in_fixed_plane(tetra, plane_index)

    assert len(set(centers)) == iterations
    assert set(distances) == {Q(1)}

    face_normals = []
    for i in (0, 1):
        face = [INITIAL_VERTICES[j] for j in range(4) if j != i]
        face_normals.append(_cross(_sub(face[1], face[0]), _sub(face[2], face[0])))
    n0, n1 = face_normals
    cosine_between_normals = _dot(n0, n1) ** 2 / (_dot(n0, n0) * _dot(n1, n1))
    # Product of two plane reflections is a rotation by twice the acute
    # angle between planes: cos(phi) = 2 cos(alpha)^2 - 1.
    cos_rotation = 2 * cosine_between_normals - 1
    assert cos_rotation == Q(-7, 9)
    return cos_rotation, distances[0], len(set(centers))


def main():
    counts, center_counts, total = branch_tree(7)
    cos_rotation, radius_sq, orbit_count = two_face_rotation(24)
    print(f"PASS: exact branch counts by depth 0..7: {counts}")
    print(f"PASS: distinct tetrahedra through depth 7: {total}")
    print(f"PASS: distinct centroids by depth: {center_counts}")
    print("PASS: no repeated tetrahedron or centroid across tested depths.")
    print(f"PASS: alternating two-face reflections: {orbit_count} distinct centers.")
    print(f"PASS: squared distance to common edge axis is invariant: {radius_sq}.")
    print(f"RESULT: cos(rotation angle) = {cos_rotation} = -7/9.")
    print("THEOREM: this angle is an irrational multiple of 2*pi; the orbit")
    print("         of any off-axis point is dense on its circle.")
    print("LIMIT: this is an isometric reflection orbit, not a fractal proof.")


if __name__ == "__main__":
    main()
