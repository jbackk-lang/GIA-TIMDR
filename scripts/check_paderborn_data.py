#!/usr/bin/env python3
"""Read-only inventory of Paderborn raw and derived data for GIA-TIMDR.

Usage: python scripts/check_paderborn_data.py [--raw PATH] [--lc PATH] [--features PATH]
Never downloads, modifies, or deletes data.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path

BEARINGS = ("K002", "K003", "K004", "K005", "K006",
            "KA04", "KA15", "KA16", "KA22", "KA30",
            "KI04", "KI14", "KI16", "KI18", "KI21")
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW = ROOT.parent / "TIMDR-AI-Core" / "data" / "paderborn_candidate" / "raw"
DEFAULT_LC = Path(os.environ.get("LC_DATA", str(ROOT.parent / "DATA" / "paderborn_lc_v0_1")))
DEFAULT_FEATURES = ROOT.parent / "DATA" / "paderborn_resonance_sieve_v0_1"


def inspect(directory: Path, names: list[str]) -> dict:
    present = [name for name in names if (directory / name).is_file()]
    missing = [name for name in names if name not in present]
    return {"path": str(directory), "directory_exists": directory.is_dir(),
            "expected": len(names), "present": len(present), "missing": missing}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--lc", type=Path, default=DEFAULT_LC)
    parser.add_argument("--features", type=Path, default=DEFAULT_FEATURES)
    args = parser.parse_args()
    raw = inspect(args.raw, [b + ".rar" for b in BEARINGS])
    lc = inspect(args.lc, [b + ".npz" for b in BEARINGS] + ["rs_feats_all.json"])
    feature_dirs = {name: inspect(args.features / name, [f"{i:03d}.json" for i in range(300)])
                    for name in ("dev", "eval", "rep", "res")}
    result = {"raw_archives": raw, "learning_curves_inputs": lc,
              "resonance_feature_json": feature_dirs,
              "recommendation": (
                  "Learning-curve inputs available; can attempt original experiment."
                  if lc["present"] == lc["expected"]
                  else "Raw archives available; regenerate learning-curve inputs using existing extraction scripts."
                  if raw["present"] == raw["expected"]
                  else "Locate or re-download missing public Paderborn archives; do not treat old results as a fresh holdout."
              )}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
