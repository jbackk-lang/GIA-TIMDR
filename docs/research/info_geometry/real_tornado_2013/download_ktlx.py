#!/usr/bin/env python3
"""Download and verify real KTLX Level II files listed in manifest.json."""
import hashlib
import json
import pathlib
import urllib.request

root = pathlib.Path(__file__).resolve().parent
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
out = root / "data"
out.mkdir(exist_ok=True)
for item in manifest["files"]:
    target = out / item["name"]
    if not target.exists() or target.stat().st_size != item["bytes"]:
        print("Downloading", item["name"], flush=True)
        urllib.request.urlretrieve(item["url"], target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if digest != item["sha256"] or target.stat().st_size != item["bytes"]:
        raise RuntimeError("Integrity check failed: " + item["name"])
    print("OK", item["name"])
print("All files verified.")
