"""real_paderborn_tube.py -- czy geometria rury analitycznej dodaje informacje ponad sito Q?
Rozwoj: pomiary 1-15 (juz ogladane). Ocena (po zamrozeniu): pomiary 16-20 (ostatnia rezerwa).
Cechy rury (per hipoteza k = BPFO/BPFI, wazone oczkami sita w_k):
  TW_k  -- widmo SKRETU rury (czestotliwosc chwilowa pasma) przy 1x i 2x k: czy spirala 'szarpie' z czestotliwoscia
           uszkodzenia (modulacja FM), a nie tylko promien 'oddycha' (AM, to czyta Q);
  M_k   -- glebokosc oddechu rury: std(A)/mean(A);
  KA_k  -- kurtoza promienia (ostrosc impulsow oddechu).
  python core/real_paderborn_tube.py extract <set> <od> <do>   (set: dev=1-5, dev2=6-10, dev3=11-15, final=16-20)
  python core/real_paderborn_tube.py score <set>"""
from __future__ import annotations
import json, sys
from io import BytesIO
from pathlib import Path
import numpy as np
from scipy.signal import decimate
from scipy.stats import kurtosis
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_paderborn_real_damage import BEARINGS, CONDS, RAW, MULT, rpm  # noqa: E402
from core.real_paderborn_resonance_sieve import resonance_map, rs_feats, BANDS, FS2, N2, AMIN, AMAX  # noqa: E402
from core.analytic_tube import band_tubes  # noqa: E402
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent
OUT = _REPO.parent / "DATA" / "paderborn_tube_v0_1"
SETS = {"dev": range(1, 6), "dev2": range(6, 11), "dev3": range(11, 16), "final": range(16, 21)}


def measurements(which):
    return [{"bearing": b, "cls": c, "cond": cd, "member": f"{b}/{cd}_{b}_{n}.mat"}
            for c, ids in BEARINGS.items() for b in ids for cd in CONDS for n in SETS[which]]


def spec_norm(y):
    y = y - y.mean(); E = np.abs(np.fft.rfft(y * np.hanning(len(y)))); f = np.fft.rfftfreq(len(y), 1 / FS2)
    m = (f >= AMIN) & (f <= AMAX); return f[m], E[m] / (np.median(E[m]) + 1e-12)


def tube_feats(x, r):
    Rz, al = resonance_map(x)
    A, P = band_tubes(x, FS2, BANDS)
    om = np.gradient(P, 1 / FS2, axis=1)
    cut = slice(len(x) // 20, -len(x) // 20)   # brzegi Hilberta
    out = {}
    for k in ("BPFO", "BPFI"):
        fc = MULT[k] * r / 60; b1 = np.where((al >= 0.97 * fc) & (al <= 1.03 * fc))[0]
        j = b1[np.argmax(Rz[:, b1].max(0))]; v = np.clip(Rz[:, j] - 1, 0, None)
        w = v / v.sum() if v.sum() > 0 else np.full(len(v), 1 / len(v))
        tw = 0.0; M = 0.0; KA = 0.0
        for b in range(len(BANDS)):
            f, S = spec_norm(om[b, cut]); a = 0.0
            for h in (1, 2):
                band = (f >= 0.97 * h * fc) & (f <= 1.03 * h * fc); a += float(S[band].max())
            tw += w[b] * a; Ab = A[b, cut]; M += w[b] * float(Ab.std() / Ab.mean()); KA += w[b] * float(kurtosis(Ab))
        out[f"TW_{k}"] = float(np.log(tw)); out[f"M_{k}"] = M; out[f"KA_{k}"] = KA
    return out


def extract(which, lo, hi):
    from unrar.cffi import rarfile
    from scipy.io import loadmat
    d = OUT / which; d.mkdir(parents=True, exist_ok=True); ms = measurements(which); cache = {}
    for i in range(lo, hi):
        m = ms[i]
        rf = cache.setdefault(m["bearing"], rarfile.RarFile(str(RAW / f"{m['bearing']}.rar")))
        mat = loadmat(BytesIO(rf.read(m["member"])), squeeze_me=True, struct_as_record=False)
        s = mat[[x for x in mat if not x.startswith("__")][0]]
        v = np.asarray({e.Name: e.Data for e in s.Y}["vibration_1"], float)
        x2 = decimate(v, 2, ftype="fir", zero_phase=True)[:N2]; x2 = x2 - x2.mean()
        f = {k: val for k, val in rs_feats(x2, rpm(m["cond"])).items() if k.startswith("Q_")}
        f.update(tube_feats(x2, rpm(m["cond"])))
        (d / f"{i:03d}.json").write_text(json.dumps({**m, "f": f}))
    print("ok", which, lo, hi)


def score(which, seed=20260926):
    ms = [json.loads((OUT / which / f"{i:03d}.json").read_text()) for i in range(300)]
    y = np.array([m["cls"] for m in ms]); cond = np.array([m["cond"] for m in ms]); bear = np.array([m["bearing"] for m in ms])
    names = list(ms[0]["f"]); Q = [n for n in names if n.startswith("Q_")]; TU = [n for n in names if n[:2] in ("TW", "M_", "KA")]
    sets = {"Q": Q, "TUBE": TU, "Q+TUBE": Q + TU, "Q+TW": Q + [n for n in TU if n.startswith("TW")]}
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
        Z = stdz(M["Q+TUBE"]); neg.append(macro_f1(y[te], lda_predict(lda_fit(Z[tr], rng.permutation(y[tr])), Z[te])))
    return {"f1": f1, "mean": {s: float(np.mean(v)) for s, v in f1.items()}, "neg_mean": float(np.mean(neg))}


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        r = score(sys.argv[2]); [print(s, round(r["mean"][s], 3), [round(x, 2) for x in v]) for s, v in r["f1"].items()]; print("neg", round(r["neg_mean"], 3))
