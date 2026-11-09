import math
import unittest

from core.reflection_transition import (
    ReflectionEvent,
    branch_probabilities,
    reflect_direction,
    reflect_event,
    surface_normal,
    reflect_tetrahedron_step,
)


class ReflectionTransitionTests(unittest.TestCase):
    def test_surface_normal_from_tangents(self):
        self.assertEqual(surface_normal((1, 0, 0), (0, 1, 0)), (0.0, 0.0, 1.0))

    def test_specular_reflection_preserves_speed_and_reverses_normal_component(self):
        incoming = (1.0, -2.0, 3.0)
        normal = (0.0, 1.0, 0.0)
        outgoing = reflect_direction(incoming, normal)
        self.assertEqual(outgoing, (1.0, 2.0, 3.0))
        self.assertAlmostEqual(sum(x*x for x in incoming), sum(x*x for x in outgoing))

    def test_reflection_angles_are_equal(self):
        event = ReflectionEvent(
            time=1.25, position=(0.0, 0.0, 0.0),
            incoming=(1.0, -1.0, 0.0), normal=(0.0, 1.0, 0.0),
        )
        result = reflect_event(event)
        self.assertAlmostEqual(result.incidence_angle_rad, math.pi / 4)
        self.assertAlmostEqual(result.reflection_angle_rad, math.pi / 4)

    def test_normal_scaling_does_not_change_reflection(self):
        a = reflect_direction((1.0, -2.0, 0.0), (0.0, 1.0, 0.0))
        b = reflect_direction((1.0, -2.0, 0.0), (0.0, 7.0, 0.0))
        self.assertEqual(a, b)

    def test_tangent_degeneracy_is_rejected(self):
        with self.assertRaises(ValueError):
            surface_normal((1, 0, 0), (2, 0, 0))

    def test_zero_normal_is_rejected(self):
        with self.assertRaises(ValueError):
            reflect_direction((1, 0, 0), (0, 0, 0))

    def test_uniform_branch_kernel_at_beta_zero(self):
        self.assertEqual(branch_probabilities((2.0, 3.0, 4.0), beta=0), (1/3, 1/3, 1/3))

    def test_softmax_prefers_lower_cost_and_normalizes(self):
        p = branch_probabilities((0.0, 1.0, 2.0), beta=1.0)
        self.assertGreater(p[0], p[1])
        self.assertGreater(p[1], p[2])
        self.assertAlmostEqual(sum(p), 1.0)

    def test_empty_or_invalid_branch_model_is_rejected(self):
        with self.assertRaises(ValueError):
            branch_probabilities(())
        with self.assertRaises(ValueError):
            branch_probabilities((1.0, 2.0), beta=-1.0)


class BoerdijkCoxeterBridgeTests(unittest.TestCase):
    def test_reflection_operator_reproduces_exact_bc_recurrence(self):
        from core.boerdijk_coxeter_tetrahelix import generate_vertices

        exact_vertices = generate_vertices(40)
        float_vertices = tuple(tuple(float(x) for x in p) for p in exact_vertices)
        for i in range(len(float_vertices) - 4):
            predicted = reflect_tetrahedron_step(float_vertices[i:i + 4])
            expected = float_vertices[i + 4]
            for x, y in zip(predicted, expected):
                self.assertAlmostEqual(x, y, places=12)

    def test_bc_bridge_preserves_all_six_regular_tetrahedron_edges(self):
        from core.boerdijk_coxeter_tetrahelix import generate_vertices

        vertices = tuple(tuple(float(x) for x in p) for p in generate_vertices(32))
        target_sq = 8.0
        for i in range(len(vertices) - 3):
            tetra = vertices[i:i + 4]
            for a in range(4):
                for b in range(a + 1, 4):
                    d2 = sum((tetra[a][k] - tetra[b][k]) ** 2 for k in range(3))
                    self.assertAlmostEqual(d2, target_sq, places=11)

    def test_bc_face_reflection_is_specular_about_face_normal(self):
        from core.boerdijk_coxeter_tetrahelix import generate_vertices

        v = tuple(tuple(float(x) for x in p) for p in generate_vertices(6))
        old, a, b, c, nxt = v[:5]
        face_center = tuple((a[k] + b[k] + c[k]) / 3.0 for k in range(3))
        incoming = tuple(old[k] - face_center[k] for k in range(3))
        outgoing = tuple(nxt[k] - face_center[k] for k in range(3))
        normal = tuple(
            (b[1]-a[1])*(c[2]-a[2]) - (b[2]-a[2])*(c[1]-a[1]),
            (b[2]-a[2])*(c[0]-a[0]) - (b[0]-a[0])*(c[2]-a[2]),
            (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]),
        )
        reflected = reflect_direction(incoming, normal)
        for x, y in zip(reflected, outgoing):
            self.assertAlmostEqual(x, y, places=12)


if __name__ == "__main__":
    unittest.main()
