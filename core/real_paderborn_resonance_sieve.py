"""real_paderborn_resonance_sieve.py -- pole pasm nosnych, mapa rezonansu, sito samokorygujace (oczka = rezonans).
Faza rozwoju: pomiary 1-5 (juz ogladane). Ocena: pomiary 6-10 (po zamrozeniu PREREG_PADERBORN_RESONANCE_SIEVE_v0.1).
  python core/real_paderborn_resonance_sieve.py extract <set: dev|eval> <od> <do>
  python core/real_paderborn_resonance_sieve.py score <set>"""
from __future__ import annotations
import json, sys
from io import BytesIO
from pathlib import Path
import numpy as np
from scipy.signal import decimate
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_paderborn_real_damage import (BEARINGS, CONDS, RAW, MULT, rpm, ab_feats, SEGN)  # noqa: E402
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent
OUT = _REPO.parent / "DATA" / "paderborn_resonance_sieve_v0_1"
RESULT = _REPO / "docs" / "geometry" / "RESULT_PADERBORN_RESONANCE_SIEVE_v0.1.json"
FS2, N2 = 32000, 64000                      # decymacja x2, 2 s
BANDS = [(1000.0 * i, 1000.0 * (i + 1)) for i in range(1, 16)]   # 15 pasm nosnych 1-16 kHz
AMIN, AMAX = 5.0, 500.0
SETS = {"dev": range(1, 6), "eval": range(6, 11), "rep": range(11, 16), "res": range(16, 21)}


def measurements(which):
    return [{"bearing": b, "cls": c, "cond": cd, "member": f"{b}/{cd}_{b}_{n}.mat"}
            for c, ids in BEARINGS.items() for b in ids for cd in CONDS for n in SETS[which]]


def resonance_map(x):
    """Pole -> mapa rezonansu Rz[b, alfa]: widmo obwiedni pasma b, znormalizowane mediana (tlo = 1)."""
    N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / FS2)
    alpha = np.fft.rfftfreq(N, 1 / FS2); am = (alpha >= AMIN) & (alpha <= AMAX); w = np.hanning(N)
    rows = []
    for lo, hi in BANDS:
        Z = np.zeros_like(X); m = (f >= lo) & (f < hi); Z[m] = 2 * X[m]
        e = np.abs(np.fft.ifft(Z)); e = e - e.mean()
        E = np.abs(np.fft.rfft(e * w))[am]; rows.append(E / (np.median(E) + 1e-12))
    return np.array(rows), alpha[am]


def sieve(Rz, al):
    """Sito samokorygujace: przejscie 1 -- oczka wg najsilniejszego rezonansu pasma; alfa* = dominujaca modulacja;
    przejscie 2 -- oczka przestawione wg rezonansu pasm przy alfa*."""
    def norm(v):
        v = np.clip(v, 0, None); s = v.sum()
        return v / s if s > 0 else np.full_like(v, 1 / len(v))
    w1 = norm(Rz.max(1) - 1); S1 = w1 @ Rz; a_star = al[np.argmax(S1)]
    w2 = norm(Rz[:, np.argmin(np.abs(al - a_star))] - 1); S2 = w2 @ Rz
    return S2, w2, a_star


def mean_curvature_graph(Z, dx, dy):
    """Krzywizna srednia wykresu z = Z(x, y) (slad operatora ksztaltu Weingartena dla powierzchni-wykresu)."""
    zy, zx = np.gradient(Z, dy, dx); zyy, zyx = np.gradient(zy, dy, dx); zxy, zxx = np.gradient(zx, dy, dx)
    return ((1 + zy ** 2) * zxx - 2 * zx * zy * zxy + (1 + zx ** 2) * zyy) / (2 * (1 + zx ** 2 + zy ** 2) ** 1.5)


def geo_feats(Rz, al, w, r):
    """Most G: powierzchnia L = log Rz nad (pasmo [kHz], alfa [Hz]); na grzbiecie uszkodzenia:
    -H wazone oczkami sita (ostrosc grzbietu) i rozciaglosc grzbietu przez pasma nosne."""
    L = np.log(Rz + 1e-12); H = mean_curvature_graph(L, al[1] - al[0], 1.0); f = {}
    S = w @ Rz
    for k in ("BPFO", "BPFI"):
        hs, ex = [], []
        for h in (1, 2):
            fc = h * MULT[k] * r / 60; band = np.where((al >= 0.97 * fc) & (al <= 1.03 * fc))[0]
            j = band[np.argmax(S[band])]; hs.append(float(-(w @ H[:, j]))); ex.append(float((Rz[:, j] > 3).mean()))
        f[f"G_curv_{k}"] = float(np.mean(hs)); f[f"G_ext_{k}"] = float(np.mean(ex))
    return f


def rs_feats(x, r, keep=None):
    Rz, al = resonance_map(x); S, w, a_star = sieve(Rz, al); f = {}
    f.update(geo_feats(Rz, al, w, r))
    for k, m in MULT.items():
        a = 0.0
        for h in (1, 2):
            fc = h * m * r / 60; band = (al >= 0.97 * fc) & (al <= 1.03 * fc); a += float(S[band].max())
        f[f"R_{k}"] = float(np.log(a))
    # wariant 3: osobne oczka sita dla kazdej hipotezy uszkodzenia (rezonans przy BPFO / BPFI ustawia oczka)
    for k in ("BPFO", "BPFI"):
        fc = MULT[k] * r / 60; b1 = np.where((al >= 0.97 * fc) & (al <= 1.03 * fc))[0]
        j = b1[np.argmax(Rz[:, b1].max(0))]; v = np.clip(Rz[:, j] - 1, 0, None)
        wk = v / v.sum() if v.sum() > 0 else np.full(len(v), 1 / len(v)); Sk = wk @ Rz; a = 0.0
        for h in (1, 2):
            band = (al >= 0.97 * h * fc) & (al <= 1.03 * h * fc); a += float(Sk[band].max())
        f[f"Q_{k}"] = float(np.log(a)); q = wk[wk > 0]; f[f"Q_went_{k}"] = float(-(q * np.log(q)).sum() / np.log(len(wk)))
    p = w[w > 0]; f["R_w_entropy"] = float(-(p * np.log(p)).sum() / np.log(len(w)))
    return f


def kurt_feats(x, r):
    """Baseline typu kurtogram (uproszczony): pasmo o najwiekszej kurtozie widmowej K = E|z|^4/(E|z|^2)^2 - 2
    sposrod tych samych 15 pasm; widmo obwiedni tego pasma przy BPFO/BPFI/BSF (1x + 2x) + wartosc K."""
    N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / FS2)
    alpha = np.fft.rfftfreq(N, 1 / FS2); am = (alpha >= AMIN) & (alpha <= AMAX); best = (-np.inf, None)
    for lo, hi in BANDS:
        Z = np.zeros_like(X); m = (f >= lo) & (f < hi); Z[m] = 2 * X[m]; z = np.fft.ifft(Z); p2 = np.abs(z) ** 2
        K = float(np.mean(p2 ** 2) / np.mean(p2) ** 2 - 2)
        if K > best[0]:
            best = (K, np.abs(z))
    e = best[1] - best[1].mean(); E = np.abs(np.fft.rfft(e * np.hanning(N)))[am]; E = E / (np.median(E) + 1e-12)
    al = alpha[am]; out = {"K_max": best[0]}
    for k, mlt in MULT.items():
        a = 0.0
        for h in (1, 2):
            fc = h * mlt * r / 60; band = (al >= 0.97 * fc) & (al <= 1.03 * fc); a += float(E[band].max())
        out[f"K_{k}"] = float(np.log(a))
    return out


def extract(which, lo, hi):
    from unrar.cffi import rarfile
    from scipy.io import loadmat
    d = OUT / which; d.mkdir(parents=True, exist_ok=True); ms = measurements(which); cache = {}
    for k in range(lo, hi):
        m = ms[k]
        rf = cache.setdefault(m["bearing"], rarfile.RarFile(str(RAW / f"{m['bearing']}.rar")))
        mat = loadmat(BytesIO(rf.read(m["member"])), squeeze_me=True, struct_as_record=False)
        s = mat[[x for x in mat if not x.startswith("__")][0]]
        v = np.asarray({e.Name: e.Data for e in s.Y}["vibration_1"], float)
        x2 = decimate(v, 2, ftype="fir", zero_phase=True)[:N2]; x2 = x2 - x2.mean()
        f = rs_feats(x2, rpm(m["cond"]))
        if which in ("eval", "rep", "res"):
            x4 = decimate(v, 4, ftype="fir", zero_phase=True)[:SEGN]; f.update(ab_feats(x4 - x4.mean(), rpm(m["cond"])))
        if which in ("rep", "res"):
            f.update(kurt_feats(x2, rpm(m["cond"])))
        (d / f"{k:03d}.json").write_text(json.dumps({**m, "f": f}))
    print("ok", which, lo, hi)


def load(which):
    ms = [json.loads((OUT / which / f"{k:03d}.json").read_text()) for k in range(300)]
    if which == "dev":  # cechy B i T z v0.1 (te same pomiary 1-5, ta sama kolejnosc)
        old = _REPO.parent / "DATA" / "paderborn_real_damage_v0_1"
        for k, m in enumerate(ms):
            o = json.loads((old / f"{k:03d}.json").read_text()); assert o["member"] == m["member"]; m["f"].update(o["f"])
    return ms


def score(which, seed=20260926):
    ms = load(which); y = np.array([m["cls"] for m in ms]); cond = np.array([m["cond"] for m in ms])
    bear = np.array([m["bearing"] for m in ms]); names = list(ms[0]["f"])
    sets = {"B": [n for n in names if n.startswith("B_")], "R": [n for n in names if n.startswith("R_")]}
    sets["G"] = [n for n in names if n.startswith("G_")]; sets["Q"] = [n for n in names if n.startswith("Q_")]
    sets["ENV"] = [n for n in names if n.startswith("B_env")]
    if any(n.startswith("K_") for n in names):
        sets["KURT"] = [n for n in names if n.startswith("K_")]
    sets["B+Q"] = sets["B"] + sets["Q"]; sets["B+Q+G"] = sets["B"] + sets["Q"] + sets["G"]
    sets["B+R"] = sets["B"] + sets["R"]; sets["B+G"] = sets["B"] + sets["G"]; sets["B+R+G"] = sets["B"] + sets["R"] + sets["G"]
    M = {s: np.array([[m["f"][n] for n in c] for m in ms]) for s, c in sets.items()}
    def stdz(X):
        X = X.copy()
        for c in CONDS:
            q = cond == c; X[q] = (X[q] - X[q].mean(0)) / (X[q].std(0) + 1e-12)
        return X
    f1 = {s: [] for s in sets}; neg = []; rng = np.random.default_rng(seed)
    for k in range(5):
        te = np.isin(bear, [BEARINGS[c][k] for c in BEARINGS]); tr = ~te
        for s in sets:
            Z = stdz(M[s]); f1[s].append(macro_f1(y[te], lda_predict(lda_fit(Z[tr], y[tr]), Z[te])))
        Z = stdz(M["B+R+G"]); neg.append(macro_f1(y[te], lda_predict(lda_fit(Z[tr], rng.permutation(y[tr])), Z[te])))
    return {"f1": f1, "mean": {s: float(np.mean(v)) for s, v in f1.items()}, "neg_mean": float(np.mean(neg))}


def final():
    """Jednorazowa ocena na pomiarach 6-10 wg PREREG_PADERBORN_RESONANCE_SIEVE_v0.1."""
    r = score("eval"); f = r["f1"]
    def crit(a, b):
        d = np.array(f[a]) - np.array(f[b])
        v = "SUPPORTED" if d.mean() >= 0.05 and (d > 0).sum() >= 3 else ("NOT SUPPORTED" if d.mean() <= 0 else "MIESZANY")
        return {"delta": d.tolist(), "mean_delta": float(d.mean()), "verdict": v}
    r["H1_Q_vs_B"] = crit("Q", "B"); r["H2_Q_vs_ENV"] = crit("Q", "ENV")
    r["controls_passed"] = r["neg_mean"] <= 0.45
    if not r["controls_passed"]:
        r["H1_Q_vs_B"]["verdict"] = r["H2_Q_vs_ENV"]["verdict"] = "INCONCLUSIVE (kontrole)"
    r["prereg"] = "PREREG_PADERBORN_RESONANCE_SIEVE_v0.1.md"
    RESULT.write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
    return r


def final_rep():
    """Replikacja na pomiarach 11-15 wg PREREG_PADERBORN_RESONANCE_SIEVE_REPLICATION_v0.2 (sito Q bez zmian)."""
    r = score("rep"); f = r["f1"]
    def crit(a, b):
        d = np.array(f[a]) - np.array(f[b])
        v = "SUPPORTED" if d.mean() >= 0.05 and (d > 0).sum() >= 3 else ("NOT SUPPORTED" if d.mean() <= 0 else "MIESZANY")
        return {"delta": d.tolist(), "mean_delta": float(d.mean()), "verdict": v}
    r["H1_Q_vs_B"] = crit("Q", "B"); r["H2_Q_vs_ENV"] = crit("Q", "ENV"); r["H3_Q_vs_KURT"] = crit("Q", "KURT")
    r["controls_passed"] = r["neg_mean"] <= 0.45
    if not r["controls_passed"]:
        for h in ("H1_Q_vs_B", "H2_Q_vs_ENV", "H3_Q_vs_KURT"):
            r[h]["verdict"] = "INCONCLUSIVE (kontrole)"
    r["prereg"] = "PREREG_PADERBORN_RESONANCE_SIEVE_REPLICATION_v0.2.md"
    (RESULT.parent / "RESULT_PADERBORN_RESONANCE_SIEVE_REPLICATION_v0.2.json").write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
    return r


def final_res():
    """Trzecie potwierdzenie na pomiarach 16-20 wg PREREG_PADERBORN_RESONANCE_SIEVE_CONFIRM_v0.3 (sito Q bez zmian)."""
    r = score("res"); f = r["f1"]
    def crit(a, b):
        d = np.array(f[a]) - np.array(f[b])
        v = "SUPPORTED" if d.mean() >= 0.05 and (d > 0).sum() >= 3 else ("NOT SUPPORTED" if d.mean() <= 0 else "MIESZANY")
        return {"delta": d.tolist(), "mean_delta": float(d.mean()), "verdict": v}
    r["H1_Q_vs_B"] = crit("Q", "B"); r["H2_Q_vs_ENV"] = crit("Q", "ENV"); r["H3_Q_vs_KURT"] = crit("Q", "KURT")
    # laczne: 15 foldow z trzech prob (6-10, 11-15, 16-20)
    pooled = {}
    prev = [json.loads((RESULT.parent / n).read_text(encoding="utf-8")) for n in
            ("RESULT_PADERBORN_RESONANCE_SIEVE_v0.1.json", "RESULT_PADERBORN_RESONANCE_SIEVE_REPLICATION_v0.2.json")]
    for h, (a, b) in {"Q_vs_B": ("Q", "B"), "Q_vs_ENV": ("Q", "ENV")}.items():
        d = np.concatenate([np.array(p["f1"][a]) - np.array(p["f1"][b]) for p in prev] + [np.array(f[a]) - np.array(f[b])])
        v = "SUPPORTED" if d.mean() >= 0.05 and (d > 0).sum() >= 9 else ("NOT SUPPORTED" if d.mean() <= 0 else "MIESZANY")
        pooled[h] = {"mean_delta": float(d.mean()), "n_pos": int((d > 0).sum()), "n": int(len(d)), "verdict": v}
    r["pooled_15_folds"] = pooled
    r["controls_passed"] = r["neg_mean"] <= 0.45
    if not r["controls_passed"]:
        for h in ("H1_Q_vs_B", "H2_Q_vs_ENV", "H3_Q_vs_KURT"):
            r[h]["verdict"] = "INCONCLUSIVE (kontrole)"
    r["prereg"] = "PREREG_PADERBORN_RESONANCE_SIEVE_CONFIRM_v0.3.md"
    (RESULT.parent / "RESULT_PADERBORN_RESONANCE_SIEVE_CONFIRM_v0.3.json").write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
    return r


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif sys.argv[1] == "final_rep":
        r = final_rep(); print(json.dumps({k: r[k] for k in ("mean", "H1_Q_vs_B", "H2_Q_vs_ENV", "H3_Q_vs_KURT", "neg_mean", "controls_passed")}, indent=1))
    elif sys.argv[1] == "final_res":
        r = final_res(); print(json.dumps({k: r[k] for k in ("mean", "H1_Q_vs_B", "H2_Q_vs_ENV", "H3_Q_vs_KURT", "pooled_15_folds", "neg_mean", "controls_passed")}, indent=1))
    elif sys.argv[1] == "final":
        r = final(); print(json.dumps({k: r[k] for k in ("mean", "H1_Q_vs_B", "H2_Q_vs_ENV", "neg_mean", "controls_passed")}, indent=1))
    else:
        print(json.dumps(score(sys.argv[2]), indent=1))
