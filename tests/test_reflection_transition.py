import math
import unittest

from core.reflection_transition import (
    ReflectionEvent,
    branch_probabilities,
    reflect_direction,
    reflect_event,
    surface_normal,
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


if __name__ == "__main__":
    unittest.main()
