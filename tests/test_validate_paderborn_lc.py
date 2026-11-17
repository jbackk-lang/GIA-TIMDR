"""Cloud-safe tests for NPZ input validation."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_paderborn_lc.py"


class ValidatorTests(unittest.TestCase):
    def run_validator(self, directory):
        return subprocess.run([sys.executable, str(SCRIPT), str(directory)],
                              capture_output=True, text=True)

    def test_missing_files_fail(self):
        with tempfile.TemporaryDirectory() as d:
            result = self.run_validator(d)
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing NPZ", result.stdout)

    def test_corrupted_npz_fails(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "K002.npz").write_bytes(b"not an npz")
            result = self.run_validator(d)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unreadable NPZ", result.stdout)

    def test_duplicate_condition_measurement_pair_fails(self):
        import numpy as np
        with tempfile.TemporaryDirectory() as d:
            conds = ("N15_M07_F10", "N09_M07_F10", "N15_M01_F10", "N15_M07_F04")
            cond = np.array([c for c in conds for _ in range(20)])
            meas = np.tile(np.arange(1, 21), 4)
            meas[0], meas[21] = meas[21], meas[0]
            np.savez_compressed(
                Path(d) / "K002.npz",
                raw=np.broadcast_to(np.zeros((1, 64000), np.float32), (80, 64000)),
                tok=np.broadcast_to(np.zeros((1, 15, 230), np.float32), (80, 15, 230)),
                cond=cond, meas=meas)
            result = self.run_validator(d)
            self.assertEqual(result.returncode, 1)
            self.assertIn("duplicate or missing condition/measurement pairs", result.stdout)

    def test_wrong_shape_fails(self):
        import numpy as np
        with tempfile.TemporaryDirectory() as d:
            np.savez(Path(d) / "K002.npz", raw=np.zeros((1, 2), dtype=np.float32))
            result = self.run_validator(d)
            self.assertEqual(result.returncode, 1)
            self.assertIn("raw shape", result.stdout)


if __name__ == "__main__":
    unittest.main()
