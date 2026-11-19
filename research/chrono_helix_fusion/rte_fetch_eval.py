"""Fetch small authentic RTE voltage/current transient files and inspect them.

RTE's DATA_u / DATA_i are *fault-selected* transients without healthy labels.
This is ingestion/feature extraction, NOT classification performance.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
import numpy as np
from benchmark import extract
from bridges import vector

BASE = "https://dfrdb.rte-france.com/"
SHA = {
    "DATA_u.npz": "204647569416d7f8010d4607058c9610db1407ad6a2f81cc0647f8c427d07209",
    "DATA_i.npz": "7a103da040f1e56e12bb1a3cb03c0c02cb0afbec0d811736fa685e5c7a025aa3",
}

def get(url):
    with urlopen(Request(url, headers={"User-Agent": "CHF-research/0.1"}), timeout=90) as r:
        return r.read()

def resolve(html, filename):
    # Parse actual hrefs from publisher page, never assume /DATA_u.npz exists.
    hrefs = re.findall(r'href\\s*=\\s*["\\\']([^"\\\']+)["\\\']', html, flags=re.I)
    links = [urljoin(BASE, h) for h in hrefs if filename.lower() in h.lower()]
    if not links:
        raise RuntimeError(f"No published download link found for {filename}")
    return links[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("rte_pilot"))
    ap.add_argument("--max-pairs", type=int, default=50)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    html = get(BASE).decode("utf-8", errors="replace")
    arrays, sources = {}, {}
    for name in SHA:
        url = resolve(html, name)
        raw = get(url)
        digest = hashlib.sha256(raw).hexdigest()
        if digest != SHA[name]:
            raise RuntimeError(f"SHA256 mismatch for {name}: {digest}")
        path = args.out / name
        path.write_bytes(raw)
        with np.load(path, allow_pickle=False) as z:
            key = Path(name).stem
            if key not in z:
                raise ValueError(f"{name} missing array {key}; keys={z.files}")
            arrays[key] = z[key]
        sources[name] = {"url": url, "sha256": digest, "shape": list(arrays[key].shape)}
    u, i = arrays["DATA_u"], arrays["DATA_i"]
    if u.shape != i.shape or u.ndim != 2:
        raise ValueError(f"Unexpected paired shapes {u.shape} {i.shape}")
    n = min(args.max_pairs, len(u))
    if n <= 0:
        raise ValueError("No pairs")
    out = []
    for j in range(n):
        row = {"pair_id": j}
        for name, x in (("voltage", u[j]), ("current", i[j])):
            x = np.asarray(x, float)
            if len(x) < 64 or not np.isfinite(x).all():
                raise ValueError(f"Bad signal at {j}: {name}")
            parts = extract(x, fs=6400)
            row[name] = {"fft_stats": parts[0], "chrono": parts[1],
                         "helix": parts[2], "branches": parts[3],
                         "trinode": parts[4], "lagged_bridges": vector(x, fs=6400)}
        out.append(row)
    report = {"status": "real_data_descriptive_only", "source": BASE,
              "sources": sources, "n_pairs_analyzed": n,
              "sampling_hz": 6400, "window_samples": int(u.shape[1]),
              "no_labels": True,
              "warning": "All RTE DATA_u/i are selected transients; no normal class or AUROC. Pairs may originate from shared events.",
              "features": out}
    (args.out / "report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k!="features"}, indent=2))

if __name__ == "__main__":
    main()
