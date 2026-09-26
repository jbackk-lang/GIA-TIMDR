"""real_paderborn_current_orbit.py -- PREREG_PADERBORN_CURRENT_ORBIT_v0.1.
  python core/real_paderborn_current_orbit.py gate
  python core/real_paderborn_current_orbit.py extract <od> <do>     (indeks w liscie 192 pomiarow train+calibration)
  python core/real_paderborn_current_orbit.py evaluate
Holdout zamrozonego podzialu AI-Core nie jest nigdy otwierany."""
from __future__ import annotations
import json, os, sys
from io import BytesIO
from pathlib import Path
import numpy as np
from scipy.signal import decimate
from scipy.stats import kurtosis

_REPO = Path(__file__).resolve().parent.parent
for _p in (_REPO, _REPO / "TIMDR-Geometry-Formalism"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
from core.winding_crossing_ms_bridge import winding_metric_fn, crossing_metric_fn, _cross2  # noqa
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1, spectral_entropy  # noqa

AICORE = Path(os.environ.get("AICORE", _REPO.parent / "TIMDR-AI-Core"))
SPLIT = AICORE / "prereg" / "PADERBORN_MS_REPLICATION_v0.1.json"
FEAT = _REPO.parent / "DATA" / "paderborn_current_orbit_v0_1"
RESULT = _REPO / "docs" / "geometry" / "RESULT_PADERBORN_CURRENT_ORBIT_v0.1.json"
CLASSES = {"K001": 0, "KA01": 1, "KI01": 2}
CONDS = ("N15_M07_F10", "N09_M07_F10", "N15_M01_F10", "N15_M07_F04")
W, NWIN, SEED = 512, 4, 20260926


def members():
    d = json.loads(SPLIT.read_text(encoding="utf-8"))
    return d["split"]["members"]["train"] + d["split"]["members"]["calibration"]  # holdout celowo pominiety


def orbit_winding(a, b):
    th = np.unwrap(np.arctan2(b - b.mean(), a - a.mean()))
    return float(abs(th[-1] - th[0]) / (2 * np.pi))


def orbit_crossing(a, b):
    pts = np.stack([a, b], 1)
    P, Q = pts[:-1], pts[1:]; AB = Q - P; m = len(P)
    Pi, Qi, Pj, Qj = P[:, None], Q[:, None], P[None], Q[None]; ABi, ABj = AB[:, None], AB[None]
    o1 = _cross2(ABi, Pj - Pi); o2 = _cross2(ABi, Qj - Pi); o3 = _cross2(ABj, Pi - Pj); o4 = _cross2(ABj, Qi - Pj)
    x = (np.sign(o1) != np.sign(o2)) & (np.sign(o3) != np.sign(o4)) & (o1 != 0) & (o2 != 0) & (o3 != 0) & (o4 != 0)
    ii, jj = np.meshgrid(np.arange(m), np.arange(m), indexing="ij")
    return float(np.sum(x & (jj >= ii + 2)))


def window_features(i1, i2):
    i1 = i1 - i1.mean(); i2 = i2 - i2.mean()
    a = i1; b = (i1 + 2 * i2) / np.sqrt(3)
    mod = np.sqrt(a ** 2 + b ** 2)
    ev = np.linalg.eigvalsh(np.cov(np.stack([a, b])))
    f = {"B_mod_cv": float(mod.std() / mod.mean()), "B_mod_kurt": float(kurtosis(mod)),
         "B_mod_sent": spectral_entropy(mod - mod.mean()), "B_axis_ratio": float(np.sqrt(max(ev[0], 0) / ev[1]))}
    for n, x in (("1", i1), ("2", i2)):
        sd = float(x.std())
        f[f"B_rms_{n}"] = sd; f[f"B_kurt_{n}"] = float(kurtosis(x)); f[f"B_crest_{n}"] = float(np.abs(x).max() / sd)
        f[f"B_sent_{n}"] = spectral_entropy(x)
        f[f"T1_wind_{n}"] = winding_metric_fn(x); f[f"T1_cross_{n}"] = crossing_metric_fn(x); f[f"T1_phase_{n}"] = phase_winding_fn(x)
    f["TO_wind"] = orbit_winding(a, b); f["TO_cross"] = orbit_crossing(a, b)
    return f


def dec(x):
    return decimate(decimate(np.asarray(x, float), 4, ftype="fir", zero_phase=True), 4, ftype="fir", zero_phase=True)


def extract(lo, hi):
    from unrar.cffi import rarfile
    from scipy.io import loadmat
    FEAT.mkdir(parents=True, exist_ok=True)
    mem = members(); cache = {}
    for k in range(lo, hi):
        m = mem[k]
        rf = cache.setdefault(m["archive"], rarfile.RarFile(str(AICORE / "data/paderborn_candidate/raw" / m["archive"])))
        mat = loadmat(BytesIO(rf.read(m["member"])), squeeze_me=True, struct_as_record=False)
        s = mat[[x for x in mat if not x.startswith("__")][0]]
        ch = {e.Name: e.Data for e in s.Y}
        i1, i2 = dec(ch["phase_current_1"]), dec(ch["phase_current_2"])
        name = Path(m["member"]).stem
        feats = [window_features(i1[j * W:(j + 1) * W], i2[j * W:(j + 1) * W]) for j in range(NWIN)]
        (FEAT / f"{k:03d}.json").write_text(json.dumps({"member": m["member"], "cond": name[:11], "cls": CLASSES[m["archive"][:4]],
                                                         "features": feats}))
    print("ok", lo, hi)


def synth(unbal, n, rng, fs=4000, f0=50.0):
    out = []
    for _ in range(n):
        t = np.arange(W) / fs; ph = rng.uniform(0, 2 * np.pi)
        pos = [np.cos(2 * np.pi * f0 * t + ph - k * 2 * np.pi / 3) for k in range(3)]
        neg = [unbal * np.cos(2 * np.pi * f0 * t + ph + k * 2 * np.pi / 3) for k in range(3)]
        i1 = pos[0] + neg[0] + 0.05 * rng.standard_normal(W); i2 = pos[1] + neg[1] + 0.05 * rng.standard_normal(W)
        out.append(window_features(i1, i2))
    return out


def gate():
    rng = np.random.default_rng(SEED)
    c0, c1 = synth(0.0, 100, rng), synth(0.10, 100, rng)
    names = list(c0[0]); X = np.array([[f[n] for n in names] for f in c0 + c1]); y = np.r_[np.zeros(100, int), np.ones(100, int)]
    tr = np.r_[np.arange(50), np.arange(100, 150)]; te = np.r_[np.arange(50, 100), np.arange(150, 200)]
    f1 = macro_f1(y[te], lda_predict(lda_fit(X[tr], y[tr]), X[te]))
    wind = float(np.median([f["TO_wind"] for f in c0]))
    return {"synthetic_f1": f1, "balanced_orbit_winding_median": wind, "passed": f1 >= 0.9 and abs(wind - 6.4) <= 0.2}


def evaluate():
    recs = [json.loads((FEAT / f"{k:03d}.json").read_text()) for k in range(192)]
    rows = [(r["cond"], r["cls"], f) for r in recs for f in r["features"]]
    names = list(rows[0][2]); B = [n for n in names if n.startswith("B_")]
    TO = [n for n in names if n.startswith("TO_")]; T1 = [n for n in names if n.startswith("T1_")]
    sets = {"B": B, "T_orbit": TO, "T_1D": T1, "T": TO + T1, "BT": B + TO + T1, "B+T_orbit": B + TO}
    cond = np.array([r[0] for r in rows]); y = np.array([r[1] for r in rows])
    res = {"prereg": "PREREG_PADERBORN_CURRENT_ORBIT_v0.1.md", "n_windows": len(rows),
           "per_condition_counts": {c: int(np.sum(cond == c)) for c in CONDS}, "gate": gate()}

    def Xn(cols):
        X = np.array([[r[2][n] for n in cols] for r in rows], float)
        for c in CONDS:
            m = cond == c; X[m] = (X[m] - X[m].mean(0)) / (X[m].std(0) + 1e-12)
        return X
    rng = np.random.default_rng(SEED); f1 = {s: [] for s in sets}; neg = []
    for c in CONDS:
        tr, te = cond != c, cond == c
        for s, cols in sets.items():
            X = Xn(cols); f1[s].append(macro_f1(y[te], lda_predict(lda_fit(X[tr], y[tr]), X[te])))
        X = Xn(sets["BT"]); neg.append(macro_f1(y[te], lda_predict(lda_fit(X[tr], rng.permutation(y[tr])), X[te])))
    res["negative_control"] = {"f1": neg, "mean": float(np.mean(neg)), "passed": float(np.mean(neg)) <= 0.45}
    res["f1_per_fold"] = {s: dict(zip(CONDS, v)) for s, v in f1.items()}
    res["f1_mean"] = {s: float(np.mean(v)) for s, v in f1.items()}
    d = np.array(f1["BT"]) - np.array(f1["B"])
    if sum(v >= 0.97 for v in f1["B"]) >= 3:
        h1 = "INCONCLUSIVE (sufit)"
    elif d.mean() >= 0.05 and (d > 0).sum() >= 3:
        h1 = "SUPPORTED"
    elif d.mean() <= 0:
        h1 = "NOT SUPPORTED"
    else:
        h1 = "MIESZANY"
    to, t1 = res["f1_mean"]["T_orbit"], res["f1_mean"]["T_1D"]
    h2 = "SUPPORTED" if to >= t1 + 0.05 else ("NOT SUPPORTED" if to <= t1 else "MIESZANY")
    res["H1"] = {"delta_BT_minus_B": d.tolist(), "mean_delta": float(d.mean()), "verdict": h1}
    res["H2"] = {"T_orbit": to, "T_1D": t1, "verdict": h2}
    res["gate_passed"] = res["gate"]["passed"] and res["negative_control"]["passed"]
    if not res["gate_passed"]:
        res["overall"] = "INCONCLUSIVE (kontrole)"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "gate":
        print(gate())
    elif sys.argv[1] == "extract":
        extract(int(sys.argv[2]), int(sys.argv[3]))
    else:
        r = evaluate(); print(json.dumps({k: r[k] for k in ("per_condition_counts", "gate", "negative_control", "f1_mean", "H1", "H2", "gate_passed")}, indent=1))
        for s, v in r["f1_per_fold"].items(): print(s, {k: round(x, 3) for k, x in v.items()})
