import sys
import unittest
from pathlib import Path
import numpy as np

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC))
from four_to_three_surface_reduction import run_model, surface, surface_metric


class FourToThreeSurfaceReductionTests(unittest.TestCase):
    def test_sphere_is_spherical(self):
        p = surface(np.array([0.4, 1.2]), np.array([0.3, 2.1]))
        self.assertTrue(np.allclose(np.linalg.norm(p, axis=1), 1.0, atol=1e-10))

    def test_egg_is_asymmetric_and_finite(self):
        p_north = surface(np.pi/3, 0.0, egg=0.28, axial_scale=1.08)
        p_south = surface(2*np.pi/3, 0.0, egg=0.28, axial_scale=1.08)
        self.assertTrue(np.all(np.isfinite(p_north)))
        self.assertFalse(np.isclose(np.linalg.norm(p_north[:2]),
                                    np.linalg.norm(p_south[:2])))

    def test_four_to_three_phase_spacing(self):
        sphere = run_model("sphere", samples=360)
        self.assertEqual(sphere["before"]["strand_count"], 4)
        self.assertEqual(sphere["after"]["strand_count"], 3)
        self.assertAlmostEqual(sphere["before"]["azimuth_gap_radians"], np.pi/2)
        self.assertAlmostEqual(sphere["after"]["azimuth_gap_radians"], 2*np.pi/3)
        self.assertGreater(sphere["operation"]["bridge_length"], 0)

    def test_egg_changes_local_metric_and_spacing(self):
        sphere = run_model("sphere", samples=360)
        egg = run_model("egg", samples=360)
        self.assertNotAlmostEqual(
            sphere["after"]["max_adjacent_parallel_spacing"],
            egg["after"]["max_adjacent_parallel_spacing"], places=4
        )
        self.assertNotAlmostEqual(
            sphere["after"]["min_adjacent_parallel_spacing"],
            egg["after"]["min_adjacent_parallel_spacing"], places=4
        )

    def test_signed_torsion_is_computed(self):
        result = run_model("sphere", samples=720)
        for profile in result["signed_torsion_survivors"]:
            self.assertTrue(np.isfinite(profile["mean"]))
            self.assertTrue(np.isfinite(profile["min"]))
            self.assertTrue(np.isfinite(profile["max"]))

    def test_surface_metric_positive_semidefinite(self):
        E, F, G = surface_metric(np.pi/2, egg=0.2)
        self.assertGreaterEqual(E, 0)
        self.assertGreaterEqual(G, 0)
        self.assertGreaterEqual(E*G-F*F, -1e-8)


if __name__ == "__main__":
    unittest.main()
