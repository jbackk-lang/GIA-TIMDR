import unittest
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.boerdijk_coxeter_tetrahelix import (
    SCREW_ROTATION,
    SCREW_TRANSLATION,
    generate_vertices,
    screw_step,
    squared_distance,
    tetrahedron_centroid,
)


class BoerdijkCoxeterExactTests(unittest.TestCase):
    def test_every_consecutive_edge_has_exact_same_length(self):
        vertices = generate_vertices(40)
        self.assertTrue(all(squared_distance(a, b) == Q(8)
                            for a, b in zip(vertices, vertices[1:])))

    def test_each_tetrahedron_is_regular(self):
        vertices = generate_vertices(24)
        for i in range(len(vertices) - 3):
            tetra = vertices[i:i + 4]
            edge_sq = {
                squared_distance(tetra[a], tetra[b])
                for a in range(4) for b in range(a + 1, 4)
            }
            self.assertEqual(edge_sq, {Q(8)})

    def test_one_exact_screw_map_predicts_all_vertices(self):
        vertices = generate_vertices(60)
        for current, following in zip(vertices, vertices[1:]):
            self.assertEqual(screw_step(current), following)

    def test_screw_map_is_a_proper_rigid_rotation_plus_translation(self):
        r = SCREW_ROTATION
        # R^T R = I for the row-vector convention.
        for i in range(3):
            for j in range(3):
                value = sum((r[k][i] * r[k][j] for k in range(3)), Q(0))
                self.assertEqual(value, Q(1) if i == j else Q(0))
        det = (
            r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
            - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
            + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
        )
        self.assertEqual(det, Q(1))
        self.assertEqual(SCREW_TRANSLATION, (Q(-2, 3),) * 3)

    def test_the_same_screw_map_advances_tetrahedron_centroids(self):
        vertices = generate_vertices(20)
        centroids = [
            tetrahedron_centroid(vertices[i:i + 4])
            for i in range(len(vertices) - 3)
        ]
        for current, following in zip(centroids, centroids[1:]):
            self.assertEqual(screw_step(current), following)

    def test_minimum_count_and_degenerate_plane_are_rejected(self):
        with self.assertRaises(ValueError):
            generate_vertices(3)
        from core.boerdijk_coxeter_tetrahelix import reflect_point_in_plane
        with self.assertRaises(ValueError):
            reflect_point_in_plane((Q(0), Q(0), Q(1)),
                                   (Q(0), Q(0), Q(0)),
                                   (Q(1), Q(0), Q(0)),
                                   (Q(2), Q(0), Q(0)))


if __name__ == "__main__":
    unittest.main()
