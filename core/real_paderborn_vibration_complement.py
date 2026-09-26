"""real_paderborn_vibration_complement.py -- PREREG_PADERBORN_VIBRATION_COMPLEMENT_v0.1.
  python core/real_paderborn_vibration_complement.py extract <od> <do>   (0..192)
  python core/real_paderborn_vibration_complement.py evaluate"""
from __future__ import annotations
import json, sys
from io import BytesIO
from pathlib import Path
import numpy as np
from scipy.signal import decimate
from scipy.stats import kurtosis
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.winding_crossing_ms_bridge import winding_metric_fn, crossing_metric_fn  # noqa: E402
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa: E402
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1, spectral_entropy  # noqa: E402
from core.real_paderborn_current_orbit import AICORE, SPLIT, CLASSES, CONDS  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent
FEAT = _REPO.parent / "DATA" / "paderborn_vibration_complement_v0_1"
RESULT = _REPO / "docs" / "geometry" / "RESULT_PADERBORN_VIBRATION_COMPLEMENT_v0.1.json"
W, NWIN, SEED = 512, 8, 20260926


def members():
    d = json.loads(SPLIT.read_text(encoding="utf-8"))["split"]["members"]
    return [dict(m, split="train") for m in d["train"]] + [dict(m, split="calibration") for m in d["calibration"]]


def feats(x):
    x = x - x.mean(); sd = float(x.std())
    return {"B_std": sd, "B_kurt": float(kurtosis(x)), "B_crest": float(np.abs(x).max() / sd), "B_sent": spectral_entropy(x),
            "T_wind": winding_metric_fn(x), "T_cross": crossing_metric_fn(x), "T_phase": phase_winding_fn(x)}


def extract(lo, hi):
    from unrar.cffi import rarfile
    from scipy.io import loadmat
    FEAT.mkdir(parents=True, exist_ok=True); mem = members(); cache = {}
    for k in range(lo, hi):
        m = mem[k]
        rf = cache.setdefault(m["archive"], rarfile.RarFile(str(AICORE / "data/paderborn_candidate/raw" / m["archive"])))
        mat = loadmat(BytesIO(rf.read(m["member"])), squeeze_me=True, struct_as_record=False)
        s = mat[[x for x in mat if not x.startswith("__")][0]]
        v = decimate(np.asarray({e.Name: e.Data for e in s.Y}["vibration_1"], float), 4, ftype="fir", zero_phase=True)
        name = Path(m["member"]).stem
        (FEAT / f"{k:03d}.json").write_text(json.dumps({"member": m["member"], "split": m["split"], "cond": name[:11],
                                                         "cls": CLASSES[m["archive"][:4]],
                                                         "features": [feats(v[j * W:(j + 1) * W]) for j in range(NWIN)]}))
    print("ok", lo, hi)


def positive_control():
    rng = np.random.default_rng(SEED); rows = []
    for c in (0, 1):
        for _ in range(100):
            x = rng.standard_normal(W)
            if c:
                x[::64] += 6.0
            rows.append((c, feats(x)))
    names = list(rows[0][1]); X = np.array([[f[n] for n in names] for _, f in rows]); y = np.array([c for c, _ in rows])
    X = (X - X.mean(0)) / (X.std(0) + 1e-12)
    tr = np.r_[np.arange(50), np.arange(100, 150)]; te = np.r_[np.arange(50, 100), np.arange(150, 200)]
    return macro_f1(y[te], lda_predict(lda_fit(X[tr], y[tr]), X[te]))


def evaluate():
    recs = [json.loads((FEAT / f"{k:03d}.json").read_text()) for k in range(192)]
    rows = [(r["cond"], r["split"], r["cls"], f) for r in recs for f in r["features"]]
    names = list(rows[0][3]); B = [n for n in names if n.startswith("B_")]; T = [n for n in names if n.startswith("T_")]
    sets = {"B": B, "T": T, "BT": B + T}
    cond = np.array([r[0] for r in rows]); spl = np.array([r[1] for r in rows]); y = np.array([r[2] for r in rows])

    def Xn(cols):
        X = np.array([[r[3][n] for n in cols] for r in rows], float)
        for c in CONDS:
            m = cond == c; X[m] = (X[m] - X[m].mean(0)) / (X[m].std(0) + 1e-12)
        return X
    Xs = {s: Xn(c) for s, c in sets.items()}
    rng = np.random.default_rng(SEED); within = {s: {} for s in sets}; neg = []
    for c in CONDS:
        tr = (cond == c) & (spl == "train"); te = (cond == c) & (spl == "calibration")
        for s in sets:
            within[s][c] = macro_f1(y[te], lda_predict(lda_fit(Xs[s][tr], y[tr]), Xs[s][te]))
        neg.append(macro_f1(y[te], lda_predict(lda_fit(Xs["BT"][tr], rng.permutation(y[tr])), Xs["BT"][te])))
    loco = {s: {} for s in sets}
    for c in CONDS:
        tr, te = cond != c, cond == c
        for s in sets:
            loco[s][c] = macro_f1(y[te], lda_predict(lda_fit(Xs[s][tr], y[tr]), Xs[s][te]))
    g = np.array([within["BT"][c] - within["B"][c] for c in CONDS])
    if sum(within["B"][c] >= 0.97 for c in CONDS) >= 3:
        v = "INCONCLUSIVE (sufit)"
    elif g.mean() >= 0.05 and (g > 0).sum() >= 3:
        v = "SUPPORTED"
    elif g.mean() <= 0:
        v = "NOT SUPPORTED"
    else:
        v = "MIESZANY"
    pos = positive_control()
    res = {"prereg": "PREREG_PADERBORN_VIBRATION_COMPLEMENT_v0.1.md", "n_windows": len(rows),
           "positive_control_f1": pos, "negative_control_mean_f1": float(np.mean(neg)),
           "controls_passed": pos >= 0.9 and float(np.mean(neg)) <= 0.45,
           "within_condition_f1": within, "gain_per_condition": dict(zip(CONDS, g.tolist())), "mean_gain": float(g.mean()),
           "loco_f1_descriptive": loco}
    res["verdict"] = v if res["controls_passed"] else "INCONCLUSIVE (kontrole)"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print(json.dumps(evaluate(), indent=1))
