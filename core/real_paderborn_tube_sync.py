"""real_paderborn_tube_sync.py -- synchronicznosc oddechu wiazki rur (rezonans jako nalozenie pol).
Dla hipotezy k: czestotliwosc f* = szczyt przesianego widma sita w pasmie +-3% wokol k; dla kazdego pasma b zespolona
amplituda oddechu C_b = sum_t (A_b - mean) exp(-i 2 pi f* t).
  PLV_k = |mean_b C_b/|C_b||             -- czy rury oddychaja w tej samej fazie (wszystkie pasma);
  COH_k = |sum_b w_b C_b| / sum_b w_b|C_b| -- zgodnosc fazy w pasmach przepuszczonych przez sito.
Rozwoj: pomiary 1-15; ocena (po zamrozeniu): 16-20.
  python core/real_paderborn_tube_sync.py extract <set> <od> <do> ; score <set>"""
from __future__ import annotations
import json, sys
from io import BytesIO
from pathlib import Path
import numpy as np
from scipy.signal import decimate
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_paderborn_real_damage import BEARINGS, CONDS, RAW, MULT, rpm  # noqa: E402
from core.real_paderborn_resonance_sieve import resonance_map, rs_feats, BANDS, FS2, N2  # noqa: E402
from core.analytic_tube import band_tubes  # noqa: E402
from core.real_paderborn_tube import measurements, SETS  # noqa: E402
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent
OUT = _REPO.parent / "DATA" / "paderborn_tube_sync_v0_1"


def sync_feats(x, r):
    Rz, al = resonance_map(x); A, _ = band_tubes(x, FS2, BANDS)
    cut = slice(len(x) // 20, -len(x) // 20); Ac = A[:, cut]; Ac = Ac - Ac.mean(1, keepdims=True)
    t = np.arange(Ac.shape[1]) / FS2; out = {}
    for k in ("BPFO", "BPFI"):
        fc = MULT[k] * r / 60; b1 = np.where((al >= 0.97 * fc) & (al <= 1.03 * fc))[0]
        j = b1[np.argmax(Rz[:, b1].max(0))]; v = np.clip(Rz[:, j] - 1, 0, None)
        w = v / v.sum() if v.sum() > 0 else np.full(len(v), 1 / len(v))
        S = w @ Rz; fstar = al[b1[np.argmax(S[b1])]]
        plv, coh = [], []
        for h in (1, 2):
            C = Ac @ np.exp(-2j * np.pi * h * fstar * t)
            u = C / (np.abs(C) + 1e-12); plv.append(float(np.abs(u.mean())))
            coh.append(float(np.abs((w * C).sum()) / ((w * np.abs(C)).sum() + 1e-12)))
        out[f"PLV_{k}"] = float(np.mean(plv)); out[f"COH_{k}"] = float(np.mean(coh))
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
        f.update(sync_feats(x2, rpm(m["cond"])))
        (d / f"{i:03d}.json").write_text(json.dumps({**m, "f": f}))
    print("ok", which, lo, hi)


def score(which, seed=20260926):
    ms = [json.loads((OUT / which / f"{i:03d}.json").read_text()) for i in range(300)]
    y = np.array([m["cls"] for m in ms]); cond = np.array([m["cond"] for m in ms]); bear = np.array([m["bearing"] for m in ms])
    names = list(ms[0]["f"]); Q = [n for n in names if n.startswith("Q_")]; SY = [n for n in names if n[:3] in ("PLV", "COH")]
    sets = {"Q": Q, "SYNC": SY, "Q+SYNC": Q + SY}
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
        Z = stdz(M["Q+SYNC"]); neg.append(macro_f1(y[te], lda_predict(lda_fit(Z[tr], rng.permutation(y[tr])), Z[te])))
    return {"f1": f1, "mean": {s: float(np.mean(v)) for s, v in f1.items()}, "neg_mean": float(np.mean(neg))}


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        r = score(sys.argv[2]); [print(s, round(r["mean"][s], 3), [round(x, 2) for x in v]) for s, v in r["f1"].items()]; print("neg", round(r["neg_mean"], 3))
