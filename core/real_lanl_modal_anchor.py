"""Budynek LANL: kotwica modalna z galezi K -> sito w rezimie fali (PREREG_LANL_MODAL_ANCHOR_v0_3).

Kotwica (K): dwa mody z widma ruchu wzglednego pieter 3 i 2 (tam siedzi zderzak): fa w 45-62 Hz, fb w 64-80 Hz,
wyznaczane w kazdym pomiarze (samokorekta kotwicy). Uderzenia zderzaka sa nieliniowe -> tony 2fa, 2fb, fa+fb.
Rezim fali (czeste uderzenia): czytamy linie K przy kotwicy, a nie blyski. H = log(moc przy {2fa, 2fb, fa+fb}) -
log(moc przy {fa, fb}). Sito czasteczkowosci z v0.2 (Q_P) pokrywa rezim czasteczki; wynik laczny = max z obu
(z-score wzgledem stanu nieuszkodzonego). D = gestosc zdarzen w pasmie 90-160 Hz ruchu wzglednego.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.signal import welch
from scipy.stats import spearmanr
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_lanl_3story_bridge import load, auc, novelty, FEAT  # noqa: E402
from core.real_lanl_field_sieve import particle_field, sieve_score  # noqa: E402
from core.transition_params import event_density, band_envelope  # noqa: E402

FS = 322.58
RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_LANL_MODAL_ANCHOR_v0_3.json"


def anchored_lines(run):
    rel = run[4] - run[3]
    f, P = welch(rel - rel.mean(), FS, nperseg=2048)
    def pk(lo, hi):
        m = (f >= lo) & (f <= hi); return f[m][np.argmax(P[m])]
    def pw(c):
        m = np.abs(f - c) <= 1.5; return P[m].max() if m.any() else np.nan
    fa, fb = pk(45, 62), pk(64, 80)
    num = np.nansum([pw(2 * fa), pw(2 * fb), pw(fa + fb)]); den = pw(fa) + pw(fb)
    D = event_density(band_envelope(rel, FS, 90, 160), FS)["D"]
    return float(np.log(num / den)), float(fa), float(fb), float(D)


def zscore(tr, te):
    med = np.median(tr); mad = 1.4826 * np.median(np.abs(tr - med)) + 1e-12
    return (te - med) / mad


def final():
    X, st = load(); idx = np.tile(np.arange(10), 17)
    A = np.array([anchored_lines(r) for r in X]); H, D = A[:, 0], A[:, 3]
    P = np.array([particle_field(r) for r in X])
    runs = [json.loads((FEAT / f"run_{i:03d}.json").read_text()) for i in range(170)]
    B = np.array([[r["f"][n] for n in runs[0]["f"] if n.startswith("B_")] for r in runs])
    und = st <= 9; dam = ~und
    folds = {"A": (und & (idx % 2 == 0), und & (idx % 2 == 1)), "B": (und & (idx % 2 == 1), und & (idx % 2 == 0))}
    res = {"prereg": "PREREG_LANL_MODAL_ANCHOR_v0_3.md", "auc": {}, "alarm": {"C": {}, "B": {}}}
    sevH, sevC = [], []
    for fn, (tr, te) in folds.items():
        def comb(mask):
            zq = zscore(sieve_score(P[tr], None, loo=True), sieve_score(P[tr], P[mask]))
            zh = zscore(H[tr], H[mask]); return np.maximum(zq, zh)
        def comb_loo():
            q = sieve_score(P[tr], None, loo=True); zq = zscore(q, q)
            h = H[tr]; zh = np.array([zscore(np.delete(h, i), h[i]) for i in range(len(h))]); return np.maximum(zq, zh)
        res["auc"][fn] = {"H": auc(H[te], H[dam]), "C": auc(comb(te), comb(dam)), "B": auc(novelty(B[tr], B[te]), novelty(B[tr], B[dam]))}
        thc = np.percentile(comb_loo(), 95); thb = np.percentile(novelty(B[tr], B[tr], loo=True), 95)
        for s in range(1, 18):
            m = (te | dam) & (st == s)
            res["alarm"]["C"].setdefault(s, []).append(float(np.mean(comb(m) > thc)))
            res["alarm"]["B"].setdefault(s, []).append(float(np.mean(novelty(B[tr], B[m]) > thb)))
        sevC.append(comb(dam))
    dst = st[dam]; msk = (dst >= 10) & (dst <= 14); sv = dst[msk] - 9
    rH = spearmanr(sv, H[dam][msk]); rD = spearmanr(sv, D[dam][msk]); rC = spearmanr(sv, np.mean(sevC, 0)[msk])
    res["sev"] = {"H": [float(rH.correlation), float(rH.pvalue)], "D": [float(rD.correlation), float(rD.pvalue)],
                  "C": [float(rC.correlation), float(rC.pvalue)]}
    res["D_median_by_state"] = {int(s): float(np.median(D[st == s])) for s in range(1, 18)}
    res["H_median_by_state"] = {int(s): float(np.median(H[st == s])) for s in range(1, 18)}
    fa = {k: float(np.mean([np.mean(res["alarm"][k][s]) for s in range(2, 10)])) for k in ("C", "B")}
    det = {k: float(np.mean([np.mean(res["alarm"][k][s]) for s in range(10, 18)])) for k in ("C", "B")}
    res["false_alarm_2_9"] = fa; res["detect_10_17"] = det
    res["H1"] = "SUPPORTED" if (rH.correlation >= 0.5 and rH.pvalue < 0.05) else "NOT SUPPORTED"
    res["H2"] = "SUPPORTED" if (all(res["auc"][f]["C"] >= 0.95 for f in folds) and fa["C"] <= fa["B"]) else "NOT SUPPORTED"
    res["H3"] = "SUPPORTED" if (rD.correlation >= 0.5 and rD.pvalue < 0.05) else "NOT SUPPORTED"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = final(); print(json.dumps({k: r[k] for k in ("auc", "sev", "false_alarm_2_9", "detect_10_17", "D_median_by_state", "H_median_by_state", "H1", "H2", "H3")}, indent=1))
