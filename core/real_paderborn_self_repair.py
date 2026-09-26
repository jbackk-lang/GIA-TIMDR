"""real_paderborn_self_repair.py -- rozwoj: czy samonaprawa modelu modalnego pomaga situ i czy sama niesie informacje?
Pomiary 1-15 (juz ogladane); rezerwa 16-20 nietknieta.
Cechy: Q (sito, model nominalny), QR (sito przy naprawionej predkosci), REP (s-1, |s-1|, Q przed, Q po, log przyrostu,
hipoteza zsynchronizowana).
  python core/real_paderborn_self_repair.py extract <set> <od> <do> ; score <set>"""
from __future__ import annotations
import json, sys
from io import BytesIO
from pathlib import Path
import numpy as np
from scipy.signal import decimate
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_paderborn_real_damage import BEARINGS, CONDS, RAW, rpm  # noqa: E402
from core.real_paderborn_resonance_sieve import rs_feats, BANDS, FS2, N2  # noqa: E402
from core.real_paderborn_tube import measurements  # noqa: E402
from core.modal_self_repair import repair_model  # noqa: E402
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent
OUT = _REPO.parent / "DATA" / "paderborn_self_repair_v0_1"
MULT = {"BPFO": 3.054, "BPFI": 4.946}


def feats(x, r0):
    f = {k: v for k, v in rs_feats(x, r0).items() if k.startswith("Q_")}
    rr = repair_model(x, FS2, r0, MULT, BANDS)
    f.update({"QR" + k[1:]: v for k, v in rs_feats(x, r0 * rr.s).items() if k.startswith("Q_")})
    f.update({"REP_s": rr.s - 1, "REP_abs": rr.repair, "REP_qb": float(np.log(rr.quality_before)),
              "REP_qa": float(np.log(rr.quality_after)), "REP_gain": float(np.log(rr.quality_after / rr.quality_before)),
              "REP_hyp": 1.0 if rr.hypothesis == "BPFO" else 0.0})
    return f


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
        (d / f"{i:03d}.json").write_text(json.dumps({**m, "f": feats(x2, rpm(m["cond"]))}))
    print("ok", which, lo, hi)


def score(which, seed=20260926):
    ms = [json.loads((OUT / which / f"{i:03d}.json").read_text()) for i in range(300)]
    y = np.array([m["cls"] for m in ms]); cond = np.array([m["cond"] for m in ms]); bear = np.array([m["bearing"] for m in ms])
    n = list(ms[0]["f"]); Q = [k for k in n if k.startswith("Q_")]; QR = [k for k in n if k.startswith("QR_")]
    REP = [k for k in n if k.startswith("REP")]
    sets = {"Q": Q, "QR": QR, "REP": REP, "Q+REP": Q + REP, "QR+REP": QR + REP}
    M = {s: np.array([[m["f"][k] for k in c] for m in ms]) for s, c in sets.items()}
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
        Z = stdz(M["QR+REP"]); neg.append(macro_f1(y[te], lda_predict(lda_fit(Z[tr], rng.permutation(y[tr])), Z[te])))
    s_by = {c: float(np.median([m["f"]["REP_s"] for m in ms if m["cls"] == c])) for c in (0, 1, 2)}
    return {"f1": f1, "mean": {s: float(np.mean(v)) for s, v in f1.items()}, "neg_mean": float(np.mean(neg)),
            "median_repair_by_class": s_by}


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        r = score(sys.argv[2]); [print(s, round(r["mean"][s], 3), [round(x, 2) for x in v]) for s, v in r["f1"].items()]
        print("neg", round(r["neg_mean"], 3), "mediana s-1 (zdrowe/OR/IR):", {k: round(v, 4) for k, v in r["median_repair_by_class"].items()})
