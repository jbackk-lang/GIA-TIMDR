import sys
import unittest
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
MODULE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(MODULE_DIR))
import minimal_coupling_probe as probe


class MinimalCouplingProbeTests(unittest.TestCase):
    def test_same_input_same_initial_state_same_response(self):
        from core.geometric_resonance_operator import build_ring_matrices
        M, K, G = build_ring_matrices(3, [1]*3, [0.3]*3, gamma=0.2)
        u = np.sin(np.linspace(0, 4*np.pi, 300))
        a = probe.simulate(u, 0.005, M, K, G)
        b = probe.simulate(u, 0.005, M, K, G)
        np.testing.assert_allclose(a, b, atol=1e-13)

    def test_history_state_changes_response_to_same_input(self):
        result = probe.run_probe()
        self.assertTrue(result["input"]["same_test_signal_both_arms"])
        self.assertGreater(result["history"]["state_norm_before_test"], 0)
        self.assertGreater(result["response"]["rms_difference"], 1e-8)

    def test_zero_input_zero_state_stays_zero(self):
        from core.geometric_resonance_operator import build_ring_matrices
        M, K, G = build_ring_matrices(3, [1]*3, [0.3]*3, gamma=0.2)
        out = probe.simulate(np.zeros(100), 0.01, M, K, G)
        np.testing.assert_allclose(out, 0.0, atol=1e-14)


if __name__ == "__main__":
    unittest.main()
