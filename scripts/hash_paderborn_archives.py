#!/usr/bin/env python3
"""Produce a reproducible SHA-256 manifest for Paderborn archive files.

Read-only. Does not download or publish the archive contents.
Usage: python scripts/hash_paderborn_archives.py /path/to/raw > manifest.json
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

BEARINGS = ("K002", "K003", "K004", "K005", "K006",
            "KA04", "KA15", "KA16", "KA22", "KA30",
            "KI04", "KI14", "KI16", "KI18", "KI21")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def manifest(folder: Path) -> dict:
    files = []
    missing = []
    for bearing in BEARINGS:
        path = folder / (bearing + ".rar")
        if not path.is_file():
            missing.append(path.name)
        else:
            files.append({"name": path.name, "size_bytes": path.stat().st_size,
                          "sha256": digest(path)})
    return {"schema_version": 1, "dataset": "Paderborn bearing recordings",
            "files": files, "missing": missing, "complete": not missing}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    result = manifest(args.directory)
    print(json.dumps(result, indent=2))
    if args.require_complete and not result["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
