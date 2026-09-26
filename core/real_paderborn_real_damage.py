"""real_paderborn_real_damage.py -- PREREG_PADERBORN_REAL_DAMAGE_v0.1 (test A: topologia; test B: pole/rezonans/sito).
  python core/real_paderborn_real_damage.py gate
  python core/real_paderborn_real_damage.py extract <od> <do>      (0..300)
  python core/real_paderborn_real_damage.py evaluate"""
from __future__ import annotations
import hashlib, json, sys
from io import BytesIO
from pathlib import Path
import numpy as np
from scipy.signal import decimate, hilbert
from scipy.stats import kurtosis, rankdata, mannwhitneyu
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.winding_crossing_ms_bridge import winding_metric_fn, crossing_metric_fn  # noqa: E402
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa: E402
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1, spectral_entropy  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent
RAW = _REPO.parent / "TIMDR-AI-Core" / "data" / "paderborn_candidate" / "raw"
FEAT = _REPO.parent / "DATA" / "paderborn_real_damage_v0_1"
RESULT = _REPO / "docs" / "geometry" / "RESULT_PADERBORN_REAL_DAMAGE_v0.1.json"
BEARINGS = {0: ["K002", "K003", "K004", "K005", "K006"], 1: ["KA04", "KA15", "KA16", "KA22", "KA30"],
            2: ["KI04", "KI14", "KI16", "KI18", "KI21"]}
CONDS = ("N15_M07_F10", "N09_M07_F10", "N15_M01_F10", "N15_M07_F04")
FS, SEGN, FR, HOP, SUB, NSUB, SEED = 16000, 32768, 4096, 2048, 512, 8, 20260926
MULT = {"BPFO": 3.054, "BPFI": 4.946, "BSF": 1.997}
FREQS = np.fft.rfftfreq(FR, 1 / FS); BAND = (FREQS >= 5) & (FREQS <= 500); FB = FREQS[BAND]


def measurements():
    out = []
    for cls, ids in BEARINGS.items():
        for b in ids:
            for c in CONDS:
                for n in range(1, 6):
                    out.append({"bearing": b, "cls": cls, "cond": c, "member": f"{b}/{c}_{b}_{n}.mat"})
    return out


def rpm(cond):
    return 1500.0 if cond.startswith("N15") else 900.0


def env_feats(x, r):
    e = np.abs(hilbert(x)); e = e - e.mean()
    E = np.abs(np.fft.rfft(e * np.hanning(len(e)))); f = np.fft.rfftfreq(len(e), 1 / FS); med = np.median(E[1:])
    out = {}
    for k, m in MULT.items():
        a = 0.0
        for h in (1, 2):
            fc = h * m * r / 60; band = (f >= 0.97 * fc) & (f <= 1.03 * fc); a += float(E[band].max())
        out[f"B_env_{k}"] = float(np.log(a / med))
    return out


def ab_feats(x, r):
    sd = float(x.std())
    f = {"B_std": sd, "B_kurt": float(kurtosis(x)), "B_crest": float(np.abs(x).max() / sd), "B_sent": spectral_entropy(x)}
    f.update(env_feats(x, r))
    subs = [x[i * SUB:(i + 1) * SUB] for i in range(NSUB)]
    f["T_wind"] = float(np.median([winding_metric_fn(s) for s in subs]))
    f["T_cross"] = float(np.median([crossing_metric_fn(s) for s in subs]))
    f["T_phase"] = float(np.median([phase_winding_fn(s) for s in subs]))
    return f


def field(x):
    e = np.abs(hilbert(x)); e = e - e.mean(); w = np.hanning(FR)
    frames = [np.abs(np.fft.rfft(e[s:s + FR] * w))[BAND] for s in range(0, len(e) - FR + 1, HOP)]
    F = np.array(frames)
    return ((rankdata(F.ravel()) - 1) / (F.size - 1)).reshape(F.shape)


def sieve_feats(R, theta, r):
    m = R > theta; fill = float(m.mean())
    if not m.any():
        return [fill, 250.0, 0.0]
    fpass = np.broadcast_to(FB, R.shape)[m]
    df = FB[1] - FB[0]; near = np.zeros_like(fpass, bool)
    for k in ("BPFO", "BPFI"):
        for h in (1, 2):
            fc = h * MULT[k] * r / 60; tol = max(0.03 * fc, df)
            near |= np.abs(fpass - fc) <= tol
    return [fill, float(fpass.mean()), float(near.mean())]


def extract(lo, hi):
    from unrar.cffi import rarfile
    from scipy.io import loadmat
    FEAT.mkdir(parents=True, exist_ok=True); ms = measurements(); cache = {}
    for k in range(lo, hi):
        m = ms[k]
        rf = cache.setdefault(m["bearing"], rarfile.RarFile(str(RAW / f"{m['bearing']}.rar")))
        mat = loadmat(BytesIO(rf.read(m["member"])), squeeze_me=True, struct_as_record=False)
        s = mat[[x for x in mat if not x.startswith("__")][0]]; ch = {e.Name: e.Data for e in s.Y}
        sig = {n: decimate(np.asarray(ch[n], float), 4, ftype="fir", zero_phase=True)[:SEGN] for n in
               ("vibration_1", "phase_current_1", "phase_current_2")}
        sig = {n: v - v.mean() for n, v in sig.items()}
        f = ab_feats(sig["vibration_1"], rpm(m["cond"]))
        P = np.stack([field(sig[n]) for n in ("vibration_1", "phase_current_1", "phase_current_2")]).astype(np.float32)
        np.savez_compressed(FEAT / f"{k:03d}.npz", P=P)
        (FEAT / f"{k:03d}.json").write_text(json.dumps({**m, "f": f}))
    print("ok", lo, hi)


def gate():
    rng = np.random.default_rng(SEED); rows = []
    for c in (0, 1):
        for _ in range(60):
            x = rng.standard_normal(SEGN)
            if c:
                x[::64] += 6.0
            rows.append((c, ab_feats(x, 1500.0)))
    names = list(rows[0][1]); X = np.array([[f[n] for n in names] for _, f in rows]); y = np.array([c for c, _ in rows])
    X = (X - X.mean(0)) / (X.std(0) + 1e-12); tr = np.r_[np.arange(30), np.arange(60, 90)]; te = np.r_[np.arange(30, 60), np.arange(90, 120)]
    f1_topo = macro_f1(y[te], lda_predict(lda_fit(X[tr], y[tr]), X[te]))
    t = np.arange(SEGN) / FS; R = {0: [], 1: []}
    for c in (0, 1):
        for _ in range(20):
            fm = (80, 80, 80) if c else (60, 80, 110)
            chans = [(1 + 0.5 * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28))) * np.sin(2 * np.pi * 1000 * t + rng.uniform(0, 6.28))
                     + 0.3 * rng.standard_normal(SEGN) for f in fm]
            R[c].append(np.prod([field(x) for x in chans], axis=0))
    theta = np.percentile(np.concatenate([r.ravel() for r in R[0]]), 95)
    fill = {c: [float((r > theta).mean()) for r in R[c]] for c in (0, 1)}
    auc = float(mannwhitneyu(fill[1], fill[0]).statistic / 400)
    return {"topology_f1": f1_topo, "sieve_auc": auc, "passed": f1_topo >= 0.9 and auc >= 0.9}


def evaluate():
    ms = [json.loads((FEAT / f"{k:03d}.json").read_text()) for k in range(300)]
    P = np.stack([np.load(FEAT / f"{k:03d}.npz")["P"] for k in range(300)]).astype(float)  # (300,3,T,F)
    R3 = P.prod(axis=1); Rv = P[:, 0]
    y = np.array([m["cls"] for m in ms]); cond = np.array([m["cond"] for m in ms]); bear = np.array([m["bearing"] for m in ms])
    names = list(ms[0]["f"]); Bn = [n for n in names if n.startswith("B_")]; Tn = [n for n in names if n.startswith("T_")]
    FB_ = np.array([[m["f"][n] for n in Bn] for m in ms]); FT_ = np.array([[m["f"][n] for n in Tn] for m in ms])
    rng = np.random.default_rng(SEED)
    res = {"prereg": "PREREG_PADERBORN_REAL_DAMAGE_v0.1.md", "gate": gate(),
           "archives_sha256": {b: hashlib.sha256((RAW / f"{b}.rar").read_bytes()).hexdigest() for ids in BEARINGS.values() for b in ids}}

    def stdz(X):
        X = X.copy()
        for c in CONDS:
            m = cond == c; X[m] = (X[m] - X[m].mean(0)) / (X[m].std(0) + 1e-12)
        return X
    sets_f1 = {s: [] for s in ("B", "T", "BT", "S3", "Sv", "B+S3")}; neg = []
    for k in range(5):
        test_b = {BEARINGS[c][k] for c in BEARINGS}; te = np.isin(bear, list(test_b)); tr = ~te
        S3 = np.zeros((300, 3)); Sv = np.zeros((300, 3))
        for c in CONDS:
            hm = tr & (y == 0) & (cond == c); cm = cond == c
            th3 = np.percentile(R3[hm].ravel(), 95); thv = np.percentile(Rv[hm].ravel(), 95)
            for i in np.where(cm)[0]:
                S3[i] = sieve_feats(R3[i], th3, rpm(c)); Sv[i] = sieve_feats(Rv[i], thv, rpm(c))
        X = {"B": FB_, "T": FT_, "BT": np.hstack([FB_, FT_]), "S3": S3, "Sv": Sv, "B+S3": np.hstack([FB_, S3])}
        for s, M in X.items():
            Z = stdz(M); sets_f1[s].append(macro_f1(y[te], lda_predict(lda_fit(Z[tr], y[tr]), Z[te])))
        for s in ("BT", "B+S3"):
            Z = stdz(X[s]); neg.append(macro_f1(y[te], lda_predict(lda_fit(Z[tr], rng.permutation(y[tr])), Z[te])))

    def verdict(a, b, need_ceiling=True):
        d = np.array(sets_f1[a]) - np.array(sets_f1[b])
        if need_ceiling and sum(v >= 0.97 for v in sets_f1[b]) >= 4:
            return d.tolist(), "INCONCLUSIVE (sufit)"
        if d.mean() >= 0.05 and (d > 0).sum() >= 4:
            return d.tolist(), "SUPPORTED"
        return d.tolist(), ("NOT SUPPORTED" if d.mean() <= 0 else "MIESZANY")
    res["f1_per_fold"] = sets_f1; res["f1_mean"] = {s: float(np.mean(v)) for s, v in sets_f1.items()}
    res["negative_control_mean_f1"] = float(np.mean(neg))
    res["A"] = dict(zip(("delta", "verdict"), verdict("BT", "B")))
    res["S1"] = dict(zip(("delta", "verdict"), verdict("S3", "Sv", need_ceiling=False)))
    res["S2"] = dict(zip(("delta", "verdict"), verdict("B+S3", "B")))
    res["controls_passed"] = res["gate"]["passed"] and res["negative_control_mean_f1"] <= 0.45
    if not res["controls_passed"]:
        for h in ("A", "S1", "S2"):
            res[h]["verdict"] = "INCONCLUSIVE (kontrole)"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "gate":
        print(gate())
    elif sys.argv[1] == "extract":
        extract(int(sys.argv[2]), int(sys.argv[3]))
    else:
        r = evaluate(); print(json.dumps({k: v for k, v in r.items() if k != "archives_sha256"}, indent=1))
