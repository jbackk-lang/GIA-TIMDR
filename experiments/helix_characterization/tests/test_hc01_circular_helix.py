import math
import unittest
from pathlib import Path
import sys

MODULE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_DIR))
import hc01_circular_helix as hc


class HC01AnalyticTests(unittest.TestCase):
    def test_zero_pitch_is_circle(self):
        x = hc.analytic(2.0, 0.0)
        self.assertAlmostEqual(x["kappa"], 0.5)
        self.assertAlmostEqual(x["tau_fs"], 0.0)
        self.assertAlmostEqual(x["pitch"], 0.0)

    def test_mirror_changes_signed_torsion_only(self):
        right = hc.analytic(1.0, 0.75)
        left = hc.analytic(1.0, -0.75)
        self.assertAlmostEqual(right["kappa"], left["kappa"])
        self.assertAlmostEqual(right["tau_fs"], -left["tau_fs"])
        self.assertAlmostEqual(right["length_per_turn"], left["length_per_turn"])
        self.assertAlmostEqual(right["dimensionless_tau"], -left["dimensionless_tau"])

    def test_uniform_scaling(self):
        base = hc.analytic(1.0, 0.6)
        scaled = hc.analytic(3.0, 1.8)
        self.assertAlmostEqual(scaled["kappa"], base["kappa"]/3.0)
        self.assertAlmostEqual(scaled["tau_fs"], base["tau_fs"]/3.0)
        self.assertAlmostEqual(scaled["length_per_turn"], base["length_per_turn"]*3.0)
        self.assertAlmostEqual(scaled["dimensionless_kappa"], base["dimensionless_kappa"])
        self.assertAlmostEqual(scaled["dimensionless_tau"], base["dimensionless_tau"])

    def test_dimensionless_torsion_extremum_is_half(self):
        for eta in (-1.0, 1.0):
            x = hc.analytic(1.0, eta)
            self.assertAlmostEqual(abs(x["dimensionless_tau"]), 0.5)
            self.assertAlmostEqual(x["dimensionless_kappa"], 0.5)

    def test_invalid_radius_rejected(self):
        with self.assertRaises(ValueError):
            hc.analytic(0.0, 1.0)


if __name__ == "__main__":
    unittest.main()
