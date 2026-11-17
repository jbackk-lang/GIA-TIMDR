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

    def test_wrong_shape_fails(self):
        import numpy as np
        with tempfile.TemporaryDirectory() as d:
            np.savez(Path(d) / "K002.npz", raw=np.zeros((1, 2), dtype=np.float32))
            result = self.run_validator(d)
            self.assertEqual(result.returncode, 1)
            self.assertIn("raw shape", result.stdout)


if __name__ == "__main__":
    unittest.main()
