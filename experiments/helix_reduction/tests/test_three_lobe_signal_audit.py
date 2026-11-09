import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC))
from three_lobe_signal_audit import analyze_three_lobes


class ThreeLobeSignalAuditTests(unittest.TestCase):
    def test_canonical_plus_minus_plus_word(self):
        r = analyze_three_lobes(samples_per_lobe=128)
        self.assertEqual(r["lobe_sign_word"], [1, -1, 1])
        self.assertTrue(r["signal_level_conclusions"]["alternating_sign_word_recovered"])

    def test_absolute_value_erases_middle_polarity(self):
        r = analyze_three_lobes(samples_per_lobe=128)
        self.assertEqual(r["absolute_value_sign_word"], [1, 1, 1])
        self.assertTrue(r["signal_level_conclusions"]["absolute_value_erases_middle_negative_polarity"])

    def test_palindromic_word_does_not_encode_traversal_direction(self):
        r = analyze_three_lobes(samples_per_lobe=128)
        self.assertTrue(r["word_is_palindromic"])
        self.assertFalse(r["signal_level_conclusions"]["sign_word_alone_detects_traversal_direction"])
        self.assertEqual(r["traversal_orientation_forward"], -r["traversal_orientation_reverse"])

    def test_three_internal_zero_crossings_and_four_boundaries(self):
        r = analyze_three_lobes(samples_per_lobe=128)
        self.assertEqual(len(r["zero_crossings"]), 4)
        self.assertEqual([x["slope_sign"] for x in r["zero_crossings"]], [1, -1, 1, -1])

    def test_phase_shift_by_pi_flips_polarities(self):
        r = analyze_three_lobes(samples_per_lobe=128, phase=3.141592653589793)
        self.assertEqual(r["lobe_sign_word"], [-1, 1, -1])


    def test_three_halfwaves_close_position_but_not_tangent(self):
        r = analyze_three_lobes(samples_per_lobe=128)
        c = r["closure"]
        self.assertTrue(c["position_closes_C0"])
        self.assertFalse(c["tangent_closes_C1"])
        self.assertFalse(c["smooth_scalar_loop"])
        self.assertAlmostEqual(c["start_slope"], -c["end_slope"])

    def test_no_claim_of_spatial_strands(self):
        r = analyze_three_lobes(samples_per_lobe=128)
        self.assertFalse(r["signal_level_conclusions"]["three_lobes_are_three_spatial_strands"])
        self.assertIn("spatial embedding", r["topology_warning"])


if __name__ == "__main__":
    unittest.main()
