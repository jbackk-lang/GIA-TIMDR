import unittest
from phase_field_preservation import run


class PhaseFieldPreservationTests(unittest.TestCase):
    def test_quadrature_representation_preserves_chirality(self):
        r = run()["results_by_chirality"]
        self.assertAlmostEqual(r["1"]["quadrature_winding"], 1.0, places=6)
        self.assertAlmostEqual(r["-1"]["quadrature_winding"], -1.0, places=6)

    def test_scalar_angle_control_loses_winding(self):
        r = run()["results_by_chirality"]
        self.assertAlmostEqual(r["1"]["scalar_angle_winding"], 0.0, places=6)
        self.assertAlmostEqual(r["-1"]["scalar_angle_winding"], 0.0, places=6)

    def test_chirality_sign_survives_sampling_and_noise_sweep(self):
        sweep = run()["robustness_sweep"]
        self.assertEqual(len(sweep), 50)
        for row in sweep:
            self.assertAlmostEqual(row["winding"], float(row["chirality"]), places=6)

    def test_phase_reconstruction_is_accurate(self):
        r = run()["results_by_chirality"]
        for result in r.values():
            self.assertLess(result["quadrature_phase_mae_deg"], 2.0)
            self.assertLess(result["quadrature_phase_p95_deg"], 5.0)


if __name__ == "__main__":
    unittest.main()
