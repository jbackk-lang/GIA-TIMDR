#!/usr/bin/env python3
"""Validate Paderborn learning-curve NPZ metadata without loading full raw arrays."""
import argparse
import json
from pathlib import Path
import numpy as np

BEARINGS = ("K002", "K003", "K004", "K005", "K006", "KA04", "KA15", "KA16",
            "KA22", "KA30", "KI04", "KI14", "KI16", "KI18", "KI21")
CONDS = ("N15_M07_F10", "N09_M07_F10", "N15_M01_F10", "N15_M07_F04")
EXPECTED = {"raw": (80, 64000), "tok": (80, 15, 230),
            "cond": (80,), "meas": (80,)}


def validate(directory: Path) -> dict:
    result = {"path": str(directory), "checked": 0, "errors": []}
    for bearing in BEARINGS:
        path = directory / (bearing + ".npz")
        if not path.is_file():
            result["errors"].append(f"{bearing}: missing NPZ")
            continue
        try:
            with np.load(path, allow_pickle=False) as z:
                for key, shape in EXPECTED.items():
                    if key not in z.files:
                        result["errors"].append(f"{bearing}: missing {key}")
                    elif z[key].shape != shape:
                        result["errors"].append(f"{bearing}: {key} shape {z[key].shape}, expected {shape}")
                if "cond" in z.files and z["cond"].shape == (80,):
                    observed = [str(c) for c in z["cond"]]
                    if sorted(observed) != sorted([c for c in CONDS for _ in range(20)]):
                        result["errors"].append(f"{bearing}: unexpected operating conditions")
                if "meas" in z.files and z["meas"].shape == (80,):
                    observed = [int(n) for n in z["meas"]]
                    if sorted(observed) != sorted(list(range(1, 21)) * 4):
                        result["errors"].append(f"{bearing}: unexpected measurement indices")
            result["checked"] += 1
        except (OSError, ValueError, KeyError, TypeError) as exc:
            result["errors"].append(f"{bearing}: unreadable NPZ ({type(exc).__name__}: {exc})")
    result["valid"] = result["checked"] == len(BEARINGS) and not result["errors"]
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    args = p.parse_args()
    result = validate(args.directory)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
