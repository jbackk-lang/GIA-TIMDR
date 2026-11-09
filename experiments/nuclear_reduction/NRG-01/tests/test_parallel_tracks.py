import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from analyze_decay_graph import analyze
from analyze_helix_handedness import analyze as analyze_helix, signed_torsion


class ParallelTrackTests(unittest.TestCase):
    def test_three_way_branch_is_detected(self):
        data = {
            "schema": "test",
            "nodes": [
                {"id": "A", "z": 10, "n": 10, "stability_status": "decay_mode_listed",
                 "decay_modes": [{"mode": "A"}, {"mode": "B-"}, {"mode": "EC"}]},
                {"id": "B", "z": 8, "n": 8, "stability_status": "no_decay_mode_listed_not_assumed_stable", "decay_modes": []},
                {"id": "C", "z": 11, "n": 9, "stability_status": "no_decay_mode_listed_not_assumed_stable", "decay_modes": []},
                {"id": "D", "z": 9, "n": 11, "stability_status": "no_decay_mode_listed_not_assumed_stable", "decay_modes": []},
            ],
            "edges": [
                {"source": "A", "target": "B", "mode": "A", "branching_percent": 50},
                {"source": "A", "target": "C", "mode": "B-", "branching_percent": 30},
                {"source": "A", "target": "D", "mode": "EC", "branching_percent": 20},
            ],
            "unresolved_edges": [],
        }
        result = analyze(data)
        self.assertEqual(result["branchpoints"][0]["outdegree"], 3)
        self.assertEqual(result["graph_counts"]["nodes"], 4)

    def test_signed_twist_survives_and_absolute_value_would_collapse(self):
        result = analyze_helix()
        self.assertTrue(result["magnitude_equal"])
        self.assertTrue(result["sign_opposite"])
        self.assertGreater(result["signed_torsion_right"], 0)
        self.assertLess(result["signed_torsion_left"], 0)

    def test_analytic_torsion_formula(self):
        self.assertAlmostEqual(signed_torsion(1.0, 0.5), 0.4)
        self.assertAlmostEqual(signed_torsion(1.0, -0.5), -0.4)


if __name__ == "__main__":
    unittest.main()
