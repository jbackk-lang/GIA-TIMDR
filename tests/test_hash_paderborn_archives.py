"""Tests for reproducible, read-only Paderborn SHA-256 manifests."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "hash_paderborn_archives.py"


class ArchiveManifestTests(unittest.TestCase):
    def test_missing_archives_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            run = subprocess.run([sys.executable, str(SCRIPT), d, "--require-complete"],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            manifest = json.loads(run.stdout)
            self.assertEqual(len(manifest["missing"]), 15)
            self.assertFalse(manifest["complete"])

    def test_hash_and_size_are_correct(self):
        with tempfile.TemporaryDirectory() as d:
            payload = b"synthetic test fixture, not Paderborn data"
            (Path(d) / "K002.rar").write_bytes(payload)
            run = subprocess.run([sys.executable, str(SCRIPT), d],
                                 capture_output=True, text=True, check=True)
            manifest = json.loads(run.stdout)
            self.assertEqual(manifest["files"][0]["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(manifest["files"][0]["size_bytes"], len(payload))
            self.assertEqual(len(manifest["missing"]), 14)


if __name__ == "__main__":
    unittest.main()
