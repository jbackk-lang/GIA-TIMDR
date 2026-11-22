"""Compatibility launcher for the GitHub traffic window.

The implementation lives in scripts/github_traffic_window.py.
"""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).resolve().parent / "scripts" / "github_traffic_window.py"),
        run_name="__main__",
    )
