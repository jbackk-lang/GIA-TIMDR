"""Cloud-safe tests for the read-only Paderborn inventory utility."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_paderborn_data.py"


class PaderbornInventoryTests(unittest.TestCase):
    def inventory(self, raw, lc, features):
        run = subprocess.run(
            [sys.executable, str(SCRIPT), "--raw", str(raw), "--lc", str(lc),
             "--features", str(features)],
            capture_output=True, text=True, check=True)
        return json.loads(run.stdout)

    def test_empty_directories_request_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            result = self.inventory(p / "raw", p / "lc", p / "features")
            self.assertEqual(result["raw_archives"]["present"], 0)
            self.assertEqual(result["learning_curves_inputs"]["present"], 0)
            self.assertIn("Locate or re-download", result["recommendation"])

    def test_complete_processed_data_is_sufficient_for_attempt(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            lc = p / "lc"
            lc.mkdir()
            for b in ("K002", "K003", "K004", "K005", "K006",
                      "KA04", "KA15", "KA16", "KA22", "KA30",
                      "KI04", "KI14", "KI16", "KI18", "KI21"):
                (lc / (b + ".npz")).touch()
            (lc / "rs_feats_all.json").touch()
            result = self.inventory(p / "raw", lc, p / "features")
            self.assertEqual(result["learning_curves_inputs"]["present"], 16)
            self.assertIn("can attempt original experiment", result["recommendation"])

    def test_raw_archives_allow_regeneration(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            raw = p / "raw"
            raw.mkdir()
            for b in ("K002", "K003", "K004", "K005", "K006",
                      "KA04", "KA15", "KA16", "KA22", "KA30",
                      "KI04", "KI14", "KI16", "KI18", "KI21"):
                (raw / (b + ".rar")).touch()
            result = self.inventory(raw, p / "lc", p / "features")
            self.assertEqual(result["raw_archives"]["present"], 15)
            self.assertIn("regenerate", result["recommendation"])


if __name__ == "__main__":
    unittest.main()
