"""real_lanl_3story_bridge.py -- PREREG_LANL_3STORY_v0.1.
  python core/real_lanl_3story_bridge.py extract <start> <stop>   (indeksy pomiarow 0..170)
  python core/real_lanl_3story_bridge.py evaluate
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.stats import kurtosis, mannwhitneyu, spearmanr

_REPO = Path(__file__).resolve().parent.parent
for _p in (_REPO, _REPO / "TIMDR-Geometry-Formalism"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
from timdr_geometry.spectral_family import channel_correlation_matrix, spectrum_from_correlation, spectral_concentration  # noqa
from core.winding_crossing_ms_bridge import winding_metric_fn, crossing_metric_fn  # noqa
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa

DATA = Path(os.environ.get("LANL_DATA", _REPO.parent / "DATA" / "lanl_3story"))
FEAT = DATA / "_features_v0_1"
RESULT = _REPO / "docs" / "geometry" / "RESULT_LANL_3STORY_v0.1.json"
CH = (1, 2, 3, 4)  # 0-based: kanaly 2-5
AR_P, SEG, NSEG, K, SEED = 5, 512, 4, 3, 20260926


def load():
    d = loadmat(DATA / "data3SS.mat")
    return np.transpose(d["dataset"], (2, 1, 0)).astype(float), d["states"].ravel().astype(int)  # (170,5,8192)


def ar_coefs(x, p=AR_P):
    x = (x - x.mean()) / x.std()
    A = np.stack([x[p - i - 1:len(x) - i - 1] for i in range(p)], axis=1)
    return np.linalg.lstsq(A, x[p:], rcond=None)[0]


def features(run):
    f = {}
    chans = [run[c] for c in CH]
    f["T_conc"] = spectral_concentration(spectrum_from_correlation(channel_correlation_matrix([c - c.mean() for c in chans])))
    for i, x in zip(CH, chans):
        n = i + 1
        for j, a in enumerate(ar_coefs(x)):
            f[f"B_ar{j+1}_{n}"] = float(a)
        xc = x - x.mean()
        f[f"B_kurt_{n}"] = float(kurtosis(xc)); f[f"B_crest_{n}"] = float(np.abs(xc).max() / xc.std())
        segs = [xc[s * SEG:(s + 1) * SEG] for s in range(NSEG)]
        f[f"T_wind_{n}"] = float(np.median([winding_metric_fn(s) for s in segs]))
        f[f"T_cross_{n}"] = float(np.median([crossing_metric_fn(s) for s in segs]))
        f[f"T_phase_{n}"] = float(np.median([phase_winding_fn(s) for s in segs]))
    return f


def extract(a, b):
    X, st = load(); FEAT.mkdir(exist_ok=True)
    for i in range(a, b):
        (FEAT / f"run_{i:03d}.json").write_text(json.dumps({"state": int(st[i]), "f": features(X[i])}))
    print("ok", a, b)


def _std_fit(X):
    med = np.median(X, 0); mad = 1.4826 * np.median(np.abs(X - med), 0); mad[mad < 1e-12] = 1.0
    return med, mad


def novelty(Xtr, Xte, loo=False):
    med, mad = _std_fit(Xtr); A = (Xtr - med) / mad; B = (Xte - med) / mad
    D = np.sqrt(((B[:, None, :] - A[None, :, :]) ** 2).sum(-1))
    if loo:
        np.fill_diagonal(D, np.inf)
    return np.sort(D, 1)[:, :K].mean(1)


def auc(neg, pos):
    u = mannwhitneyu(pos, neg, alternative="two-sided").statistic
    return float(u / (len(pos) * len(neg)))


def evaluate():
    runs = [json.loads((FEAT / f"run_{i:03d}.json").read_text()) for i in range(170)]
    st = np.array([r["state"] for r in runs]); idx = np.tile(np.arange(10), 17)
    names = list(runs[0]["f"]); sets = {"B": [n for n in names if n.startswith("B_")], "T": [n for n in names if n.startswith("T_")]}
    sets["BT"] = sets["B"] + sets["T"]
    M = {s: np.array([[r["f"][n] for n in cols] for r in runs]) for s, cols in sets.items()}
    und = st <= 9; dam = ~und
    folds = {"A": (und & (idx % 2 == 0), und & (idx % 2 == 1)), "B": (und & (idx % 2 == 1), und & (idx % 2 == 0))}
    res = {"prereg": "PREREG_LANL_3STORY_v0.1.md", "n_features": {s: len(c) for s, c in sets.items()}}
    rng = np.random.default_rng(SEED)
    # kontrole (fold A, BT)
    tr, te = folds["A"]; X, _ = load()
    clean = X[te]; spiked = clean.copy()
    for r in spiked:
        pos = rng.choice(np.arange(100, 8000), 5, replace=False); r[3, pos] += 5 * r[3].std()
    Fc = np.array([[features(r)[n] for n in sets["BT"]] for r in clean]); Fs = np.array([[features(r)[n] for n in sets["BT"]] for r in spiked])
    pos_auc = auc(novelty(M["BT"][tr], Fc), novelty(M["BT"][tr], Fs))
    sc = novelty(M["BT"][tr], M["BT"][te | dam]); lab = dam[te | dam]; perm = rng.permutation(lab)
    neg_auc = auc(sc[~perm], sc[perm])
    res["controls"] = {"positive_auc": pos_auc, "negative_auc": neg_auc, "passed": pos_auc >= 0.8 and 0.35 <= neg_auc <= 0.65}
    # H-glowna
    aucs, scores_dam, alarms = {}, {s: [] for s in sets}, {}
    for fn, (tr, te) in folds.items():
        aucs[fn] = {}
        for s in sets:
            sc_te = novelty(M[s][tr], M[s][te]); sc_d = novelty(M[s][tr], M[s][dam])
            aucs[fn][s] = auc(sc_te, sc_d); scores_dam[s].append(sc_d)
            thr = np.percentile(novelty(M[s][tr], M[s][tr], loo=True), 95)
            for state in range(1, 18):
                m = (te | dam) & (st == state)
                alarms.setdefault(s, {}).setdefault(state, []).append(float(np.mean(novelty(M[s][tr], M[s][m]) > thr)))
    gains = [aucs[f]["BT"] - aucs[f]["B"] for f in folds]; ceil = [aucs[f]["B"] > 0.97 for f in folds]
    verdict = ("INCONCLUSIVE (sufit)" if all(ceil) else "SUPPORTED" if all(g >= 0.03 for g in gains)
               else "NOT SUPPORTED" if all(g < 0.03 for g in gains) else "MIESZANY")
    res["H_main"] = {"auc": aucs, "gain_BT_minus_B": gains, "ceiling": ceil, "verdict": verdict}
    # H-ciezkosc
    dst = st[dam]; sev = {}
    for s in sets:
        sc = np.mean(scores_dam[s], 0); m = (dst >= 10) & (dst <= 14)
        r = spearmanr(sc[m], dst[m] - 9)
        sev[s] = {"rho": float(r.statistic), "p": float(r.pvalue), "SUPPORTED": bool(r.statistic >= 0.5 and r.pvalue < 0.05)}
    res["H_severity"] = sev
    res["alarm_rate_per_state"] = {s: {k: float(np.mean(v)) for k, v in d.items()} for s, d in alarms.items()}
    if not res["controls"]["passed"]:
        res["overall"] = "INCONCLUSIVE (kontrole)"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(int(sys.argv[2]), int(sys.argv[3]))
    else:
        r = evaluate(); print(json.dumps({k: v for k, v in r.items() if k != "alarm_rate_per_state"}, indent=1))
        for s, d in r["alarm_rate_per_state"].items():
            print(s, " ".join(f"{k}:{v:.2f}" for k, v in d.items()))
