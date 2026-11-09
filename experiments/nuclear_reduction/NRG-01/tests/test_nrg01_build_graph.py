import unittest
from nrg01_build_graph import daughter_for, parse_nuclide, graph_metrics


class NRG01Tests(unittest.TestCase):
    def test_seed_identity(self):
        self.assertEqual(parse_nuclide("238u"), (92, 146, "U"))
        self.assertEqual(parse_nuclide("232Th"), (90, 142, "Th"))
        self.assertEqual(parse_nuclide("237np"), (93, 144, "Np"))

    def test_alpha_balance(self):
        self.assertEqual(daughter_for(92, 146, "A"), (90, 144))

    def test_beta_minus_balance(self):
        self.assertEqual(daughter_for(55, 82, "B-"), (56, 81))

    def test_electron_capture_balance(self):
        self.assertEqual(daughter_for(93, 144, "EC"), (92, 145))

    def test_unknown_channels_are_not_guessed(self):
        self.assertIsNone(daughter_for(92, 146, "SF"))
        self.assertIsNone(daughter_for(92, 146, "IT"))

    def test_graph_metrics_distinguish_unresolved(self):
        nodes = {"A": {}, "B": {}}
        edges = [{"source": "A", "target": "B"}]
        unresolved = [{"parent": "B", "mode": "SF"}]
        m = graph_metrics(nodes, edges, unresolved)
        self.assertEqual(m["node_count"], 2)
        self.assertEqual(m["resolved_edge_count"], 1)
        self.assertEqual(m["unresolved_edge_count"], 1)


if __name__ == "__main__":
    unittest.main()
