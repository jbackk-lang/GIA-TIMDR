import json
import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
from audit_three_strand_correspondence import audit


class ThreeStrandAuditTests(unittest.TestCase):
    def fixture(self):
        return {
            "schema": "fixture",
            "seeds": ["seedA", "seedB", "seedC"],
            "nodes": [
                {"id": "A0", "a": 10, "z": 5}, {"id": "A1", "a": 9, "z": 4},
                {"id": "A2", "a": 8, "z": 3}, {"id": "A3", "a": 8, "z": 4},
                {"id": "B0", "a": 20, "z": 10}, {"id": "B1", "a": 19, "z": 9},
                {"id": "C0", "a": 30, "z": 15}, {"id": "C1", "a": 29, "z": 14},
            ],
            "edges": [
                {"source": "A0", "target": "A1", "mode": "A"},
                {"source": "A1", "target": "A2", "mode": "A"},
                {"source": "A1", "target": "A3", "mode": "B-"},
                {"source": "B0", "target": "B1", "mode": "A"},
                {"source": "C0", "target": "C1", "mode": "B-"},
            ],
            "unresolved_edges": [],
        }

    def test_components_are_not_assigned_by_data_to_strands(self):
        r = audit(self.fixture())
        self.assertEqual(r["counts"]["weak_components"], 3)
        self.assertEqual(r["three_strand_mapping"]["candidate_count"], 6)
        self.assertFalse(r["three_strand_mapping"]["ranking_possible_from_current_data"])
        self.assertFalse(r["cardinal_point_correspondence"]["identifiable"])
        self.assertFalse(r["handedness_preservation"]["cross_domain_invariant_testable"])

    def test_branching_prevents_smooth_unbranched_strand_equivalence(self):
        r = audit(self.fixture())
        self.assertTrue(r["directed_graph"]["each_component_has_internal_branching"] is False)
        # One component branches, so strict smooth-strand compatibility is not established.
        self.assertIsNone(r["three_strand_mapping"]["strict_smooth_strand_compatibility"])

    def test_cycle_detection_and_branchpoint_count(self):
        r = audit(self.fixture())
        self.assertTrue(r["directed_graph"]["all_components_are_dags"])
        self.assertEqual(len(r["directed_graph"]["three_way_branchpoints"]), 0)


if __name__ == "__main__":
    unittest.main()
