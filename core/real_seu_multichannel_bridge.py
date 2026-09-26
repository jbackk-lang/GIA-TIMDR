"""real_seu_multichannel_bridge.py -- PREREG_SEU_MULTICHANNEL_DIAGNOSTIC_v0.1.

Kroki (kazdy osobno, bo powloka ma limit czasu):
  python core/real_seu_multichannel_bridge.py gate
  python core/real_seu_multichannel_bridge.py extract <plik bez .csv>   (x10)
  python core/real_seu_multichannel_bridge.py evaluate

Dane: SEU_DATA (domyslnie ../DATA/seu_bearingset). Stale ponizej sa zamrozone w PREREG.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
from scipy.stats import kurtosis, mannwhitneyu, spearmanr

_REPO = Path(__file__).resolve().parent.parent
for _p in (_REPO, _REPO / "TIMDR-Geometry-Formalism"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from timdr_geometry.spectral_family import (  # noqa: E402
    channel_correlation_matrix, spectrum_from_correlation, spectral_concentration, run_synthetic_controls)
from core.winding_crossing_ms_bridge import winding_metric_fn, crossing_metric_fn  # noqa: E402
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa: E402

DATA = Path(os.environ.get("SEU_DATA", _REPO.parent / "DATA" / "seu_bearingset"))
FEAT_DIR = DATA / "_features_v0_1"
RESULT = _REPO / "docs" / "geometry" / "RESULT_SEU_MULTICHANNEL_DIAGNOSTIC_v0.1.json"
CLASSES = ("health", "ball", "inner", "outer", "comb")
CONDS = ("20_0", "30_2")
CHANNELS = (1, 2, 3)          # indeksy 0-based kolumn = kanaly 2,3,4 zrodla
W = 512
N_WIN = 100
SHRINK = 0.1
PERM_SEED = 20260926
ALPHA_H1 = 0.05 / 8


def load(name: str) -> np.ndarray:
    rows = []
    with open(DATA / f"{name}.csv", encoding="latin-1") as f:
        started = False
        for line in f:
            if not started:
                if line.strip() == "Data":
                    started = True
                continue
            parts = [x for x in line.replace(",", "\t").split("\t") if x.strip()]
            if len(parts) >= 8:
                rows.append([float(x) for x in parts[:8]])
    return np.asarray(rows, dtype=float)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def spectral_entropy(x: np.ndarray) -> float:
    p = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    p = p[1:]
    p = p / p.sum()
    p = p[p > 0]
    return float(-(p * np.log(p)).sum() / np.log(len(x) // 2))


def window_features(win: np.ndarray) -> dict:
    win = win - win.mean(axis=0)
    chans = [win[:, c] for c in range(win.shape[1])]
    f = {"T_conc": spectral_concentration(spectrum_from_correlation(channel_correlation_matrix(chans)))}
    C = np.corrcoef(np.stack(chans))
    f["X_mean_abs_r"] = float(np.mean(np.abs(C[np.triu_indices(3, 1)])))
    for i, x in enumerate(chans, start=2):
        sd = float(x.std())
        f[f"T_wind_{i}"] = winding_metric_fn(x)
        f[f"T_cross_{i}"] = crossing_metric_fn(x)
        f[f"T_phase_{i}"] = phase_winding_fn(x)
        f[f"B_std_{i}"] = sd
        f[f"B_kurt_{i}"] = float(kurtosis(x))
        f[f"B_crest_{i}"] = float(np.max(np.abs(x)) / sd)
        f[f"B_sent_{i}"] = spectral_entropy(x)
    return f


def extract(name: str) -> None:
    X = load(name)
    starts = np.round(np.linspace(0, len(X) - W, N_WIN)).astype(int)
    feats = [window_features(X[s:s + W][:, CHANNELS]) for s in starts]
    FEAT_DIR.mkdir(exist_ok=True)
    out = {"file": f"{name}.csv", "sha256": sha256(DATA / f"{name}.csv"), "n_rows": int(len(X)),
           "starts": starts.tolist(), "features": feats}
    (FEAT_DIR / f"{name}.json").write_text(json.dumps(out), encoding="utf-8")
    print(name, len(X), "rows,", len(feats), "windows")


def gate() -> dict:
    rows = run_synthetic_controls()
    return {"cells": [{"n_channels": r["n_channels"], "window": r["window_size"], "passed": bool(r["result"].passed)}
                      for r in rows], "passed": all(r["result"].passed for r in rows)}


# ---------------- klasyfikacja ----------------
def lda_fit(X, y):
    mu, sd = X.mean(0), X.std(0)
    sd[sd < 1e-12] = 1.0
    Z = (X - mu) / sd
    ks = np.unique(y)
    means = np.stack([Z[y == k].mean(0) for k in ks])
    R = np.concatenate([Z[y == k] - means[i] for i, k in enumerate(ks)])
    S = R.T @ R / max(len(R) - len(ks), 1)
    p = S.shape[0]
    S = (1 - SHRINK) * S + SHRINK * (np.trace(S) / p) * np.eye(p)
    Si = np.linalg.inv(S)
    return dict(mu=mu, sd=sd, ks=ks, means=means, Si=Si)


def lda_predict(m, X):
    Z = (X - m["mu"]) / m["sd"]
    A = Z @ m["Si"] @ m["means"].T - 0.5 * np.einsum("ij,jk,ik->i", m["means"], m["Si"], m["means"])
    return m["ks"][np.argmax(A, axis=1)]


def macro_f1(y, yp):
    out = []
    for k in np.unique(y):
        tp = np.sum((yp == k) & (y == k)); fp = np.sum((yp == k) & (y != k)); fn = np.sum((yp != k) & (y == k))
        out.append(0.0 if tp == 0 else 2 * tp / (2 * tp + fp + fn))
    return float(np.mean(out))


def rank_biserial(a, b):
    u = mannwhitneyu(a, b, alternative="two-sided")
    return float(u.pvalue), float(2 * u.statistic / (len(a) * len(b)) - 1)


def evaluate() -> dict:
    data = {}
    for c in CLASSES:
        for cond in CONDS:
            data[(c, cond)] = json.loads((FEAT_DIR / f"{c}_{cond}.json").read_text(encoding="utf-8"))
    names = list(data[("health", "20_0")]["features"][0].keys())
    sets = {"B": [n for n in names if n.startswith("B_")], "T": [n for n in names if n.startswith("T_")]}
    sets["BT"] = sets["B"] + sets["T"]

    def mat(cond, cols, idx=slice(None)):
        X, y = [], []
        for ci, c in enumerate(CLASSES):
            fs = data[(c, cond)]["features"][idx]
            X += [[f[n] for n in cols] for f in fs]; y += [ci] * len(fs)
        return np.asarray(X, float), np.asarray(y)

    res = {"prereg": "PREREG_SEU_MULTICHANNEL_DIAGNOSTIC_v0.1.md",
           "files": {f"{c}_{d}": {"sha256": data[(c, d)]["sha256"], "n_rows": data[(c, d)]["n_rows"]} for c, d in data}}
    g = gate(); res["gate_synthetic"] = g
    # kontrola negatywna
    rng = np.random.default_rng(PERM_SEED); neg = {}
    for a, b in (("20_0", "30_2"), ("30_2", "20_0")):
        Xa, ya = mat(a, sets["BT"]); Xb, yb = mat(b, sets["BT"])
        neg[f"{a}->{b}"] = macro_f1(yb, lda_predict(lda_fit(Xa, rng.permutation(ya)), Xb))
    res["negative_control"] = {"macro_f1": neg, "passed": all(v <= 0.35 for v in neg.values())}
    res["gate_passed"] = g["passed"] and res["negative_control"]["passed"]
    # H1
    cells = []
    for cond in CONDS:
        h = [f["T_conc"] for f in data[("health", cond)]["features"]]
        for c in CLASSES[1:]:
            x = [f["T_conc"] for f in data[(c, cond)]["features"]]
            p, r = rank_biserial(h, x)
            cells.append({"cond": cond, "fault": c, "p": p, "r": r, "med_health": float(np.median(h)),
                          "med_fault": float(np.median(x)), "sig": p < ALPHA_H1})
    sup = sum(c["sig"] and c["r"] >= 0.3 for c in cells); opp = sum(c["sig"] and c["r"] <= -0.3 for c in cells)
    res["H1"] = {"cells": cells, "n_supported_cells": sup, "n_opposite_cells": opp,
                 "verdict": "SUPPORTED" if sup >= 6 else ("ODWROTNY" if opp >= 6 else "NOT SUPPORTED")}
    topo = []
    for n in [k for k in sets["T"] if k != "T_conc"]:
        for cond in CONDS:
            h = [f[n] for f in data[("health", cond)]["features"]]
            for c in CLASSES[1:]:
                p, r = rank_biserial(h, [f[n] for f in data[(c, cond)]["features"]])
                topo.append({"feature": n, "cond": cond, "fault": c, "p": p, "r": r})
    res["H1_topology_descriptive"] = {"n_cells": len(topo), "n_sig_abs_r_ge_0.3": sum(t["p"] < ALPHA_H1 and abs(t["r"]) >= 0.3 for t in topo),
                                      "cells": topo}
    # H2
    h2 = {}
    for a, b in (("20_0", "30_2"), ("30_2", "20_0")):
        h2[f"{a}->{b}"] = {}
        for s, cols in sets.items():
            Xa, ya = mat(a, cols); Xb, yb = mat(b, cols)
            h2[f"{a}->{b}"][s] = macro_f1(yb, lda_predict(lda_fit(Xa, ya), Xb))
    gains = [v["BT"] - v["B"] for v in h2.values()]
    res["H2"] = {"macro_f1": h2, "gain_BT_minus_B": gains,
                 "verdict": "SUPPORTED" if all(x >= 0.05 for x in gains) else ("NOT SUPPORTED" if all(x < 0.05 for x in gains) else "MIESZANY"),
                 "T_better_than_B_both": all(v["T"] > v["B"] for v in h2.values())}
    ceil = {}
    for cond in CONDS:
        ceil[cond] = {}
        for s, cols in sets.items():
            Xa, ya = mat(cond, cols, slice(0, 50)); Xb, yb = mat(cond, cols, slice(50, 100))
            ceil[cond][s] = macro_f1(yb, lda_predict(lda_fit(Xa, ya), Xb))
    res["within_condition_ceiling"] = ceil
    allf = [f for d in data.values() for f in d["features"]]
    rho = spearmanr([f["T_conc"] for f in allf], [f["X_mean_abs_r"] for f in allf])
    res["conc_vs_mean_abs_r_spearman"] = float(rho.statistic)
    if not res["gate_passed"]:
        res["overall"] = "INCONCLUSIVE (bramka)"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "gate":
        print(json.dumps(gate()))
    elif cmd == "extract":
        extract(sys.argv[2])
    elif cmd == "evaluate":
        r = evaluate()
        print(json.dumps({k: r[k] for k in ("gate_passed", "negative_control", "H2", "within_condition_ceiling",
                                            "conc_vs_mean_abs_r_spearman")}, indent=1))
        print(json.dumps({k: v for k, v in r["H1"].items() if k != "cells"}), r["H1_topology_descriptive"]["n_sig_abs_r_ge_0.3"])
        for c in r["H1"]["cells"]:
            print(c)
