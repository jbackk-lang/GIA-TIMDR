import math
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hc01_tube as tube


class HC01TubeTests(unittest.TestCase):
    def test_local_curvature_radius(self):
        x = tube.characterize(1.0, 1.0)
        self.assertAlmostEqual(x["local_radius_of_curvature"], 2.0)

    def test_mirror_symmetry_of_tube_radius(self):
        right = tube.characterize(1.0, 0.3)
        left = tube.characterize(1.0, -0.3)
        self.assertAlmostEqual(right["centerline_tube_radius_estimate"],
                               left["centerline_tube_radius_estimate"], places=9)
        self.assertEqual(len(right["doubly_critical_roots"]),
                         len(left["doubly_critical_roots"]))

    def test_doubly_critical_equation(self):
        x = tube.characterize(1.0, 0.2)
        self.assertTrue(x["doubly_critical_roots"])
        for root in x["doubly_critical_roots"]:
            d = root["delta"]
            residual = math.sin(d) + 0.2**2*d
            self.assertLess(abs(residual), 1e-9)

    def test_global_bound_never_exceeds_local_bound_in_reach(self):
        for eta in (0.1, 0.2, 0.3, 0.4, 0.6, 1.0):
            x = tube.characterize(1.0, eta)
            self.assertLessEqual(x["centerline_tube_radius_estimate"],
                                 x["local_radius_of_curvature"] + 1e-12)

    def test_invalid_radius(self):
        with self.assertRaises(ValueError):
            tube.characterize(0.0, 1.0)


if __name__ == "__main__":
    unittest.main()
