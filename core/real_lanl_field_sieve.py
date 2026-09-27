"""Budynek LANL (3 kondygnacje) jako pole + sito (PREREG_LANL_FIELD_SIEVE_v0_2).

Pole = kanaly (podstawa, pietra 1-3) x pasma czestotliwosci (5 pasm do 160 Hz).
Krok 0 w kazdej komorce: czasteczkowosc P = udzial 5% najsilniejszych probek energii obwiedni pasma.
Hipoteza fizyczna (mapa dualnosci): uderzenia zderzaka = czasteczki -> P rosnie; zmiana masy/sztywnosci
przesuwa mody (fala), czasteczek nie tworzy.
Sito: rezonans = odchylenie komorki od pola wzorcowego (stan nieuszkodzony, mediana/MAD); oczka tylko tam,
gdzie odchylenie w gore > 1; wynik Q = suma oczek (jednostronnie -- uszkodzenie dodaje czasteczki).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_lanl_3story_bridge import load, auc, novelty, FEAT, CH  # noqa: E402

FS = 322.58
BANDS = [(5, 40), (40, 65), (65, 90), (90, 120), (120, 160)]
RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_LANL_FIELD_SIEVE_v0_2.json"


def particle_field(run):
    out = []
    for c in CH:
        x = run[c] - run[c].mean(); N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / FS)
        for lo, hi in BANDS:
            Z = np.zeros_like(X); m = (f >= lo) & (f < hi); Z[m] = 2 * X[m]
            e = np.abs(np.fft.ifft(Z)) ** 2
            k = max(1, int(0.05 * N)); out.append(float(np.sort(e)[-k:].sum() / e.sum()))
    return np.array(out)


def sieve_score(Ptr, Pte, loo=False):
    med = np.median(Ptr, 0); mad = 1.4826 * np.median(np.abs(Ptr - med), 0); mad[mad < 1e-12] = 1.0
    if loo:
        s = []
        for i in range(len(Ptr)):
            o = np.delete(Ptr, i, 0); md = np.median(o, 0); ma = 1.4826 * np.median(np.abs(o - md), 0); ma[ma < 1e-12] = 1.0
            z = (Ptr[i] - md) / ma; s.append(np.log1p(np.maximum(z - 1, 0).sum()))
        return np.array(s)
    Z = (Pte - med) / mad
    return np.log1p(np.maximum(Z - 1, 0).sum(1))


def final():
    X, st = load(); idx = np.tile(np.arange(10), 17)
    P = np.array([particle_field(r) for r in X])
    runs = [json.loads((FEAT / f"run_{i:03d}.json").read_text()) for i in range(170)]
    names = [n for n in runs[0]["f"] if n.startswith("B_")]
    B = np.array([[r["f"][n] for n in names] for r in runs])
    und = st <= 9; dam = ~und
    folds = {"A": (und & (idx % 2 == 0), und & (idx % 2 == 1)), "B": (und & (idx % 2 == 1), und & (idx % 2 == 0))}
    res = {"prereg": "PREREG_LANL_FIELD_SIEVE_v0_2.md", "auc": {}, "alarm": {"Q": {}, "B": {}}, "sev": {}}
    sev_scores = {"Q": [], "B": []}
    for fn, (tr, te) in folds.items():
        q_te, q_d = sieve_score(P[tr], P[te]), sieve_score(P[tr], P[dam])
        b_te, b_d = novelty(B[tr], B[te]), novelty(B[tr], B[dam])
        res["auc"][fn] = {"Q": auc(q_te, q_d), "B": auc(b_te, b_d)}
        thq = np.percentile(sieve_score(P[tr], None, loo=True), 95)
        thb = np.percentile(novelty(B[tr], B[tr], loo=True), 95)
        for s in range(1, 18):
            m = (te | dam) & (st == s)
            res["alarm"]["Q"].setdefault(s, []).append(float(np.mean(sieve_score(P[tr], P[m]) > thq)))
            res["alarm"]["B"].setdefault(s, []).append(float(np.mean(novelty(B[tr], B[m]) > thb)))
        sev_scores["Q"].append(q_d); sev_scores["B"].append(b_d)
    dst = st[dam]; msk = (dst >= 10) & (dst <= 14)
    for k in ("Q", "B"):
        sc = np.mean(sev_scores[k], 0)[msk]; r = spearmanr(dst[msk] - 9, sc)
        res["sev"][k] = {"rho": float(r.correlation), "p": float(r.pvalue)}
    fa = {k: float(np.mean([np.mean(res["alarm"][k][s]) for s in range(2, 10)])) for k in ("Q", "B")}
    det = {k: float(np.mean([np.mean(res["alarm"][k][s]) for s in range(10, 18)])) for k in ("Q", "B")}
    res["false_alarm_2_9"] = fa; res["detect_10_17"] = det
    res["H1"] = "SUPPORTED" if all(res["auc"][f]["Q"] >= 0.90 for f in folds) else "NOT SUPPORTED"
    res["H2"] = "SUPPORTED" if (fa["Q"] < fa["B"] and det["Q"] >= 0.8) else "NOT SUPPORTED"
    res["H3"] = "SUPPORTED" if (res["sev"]["Q"]["rho"] >= 0.5 and res["sev"]["Q"]["p"] < 0.05) else "NOT SUPPORTED"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    print(json.dumps(final(), indent=1, ensure_ascii=False))
