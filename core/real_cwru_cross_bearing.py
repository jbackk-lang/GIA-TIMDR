"""real_cwru_cross_bearing.py -- PREREG_CWRU_CROSS_BEARING_ENVELOPE_v0.1.
  python core/real_cwru_cross_bearing.py extract <RPM>
  python core/real_cwru_cross_bearing.py evaluate"""
from __future__ import annotations
import io, json, os, sys, zipfile
from pathlib import Path
import numpy as np
from scipy.signal import hilbert
from scipy.stats import kurtosis
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.winding_crossing_ms_bridge import winding_metric_fn, crossing_metric_fn  # noqa: E402
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa: E402
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1, spectral_entropy  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent
ZIP = Path(os.environ.get("CWRU_ZIP", _REPO.parent.parent / "CWRU_Bearing_NumPy_4LUM-main.zip"))
FEAT = _REPO.parent / "DATA" / "cwru_cross_bearing_v0_1"
RESULT = _REPO / "docs" / "geometry" / "RESULT_CWRU_CROSS_BEARING_ENVELOPE_v0.1.json"
RPMS = (1797, 1772, 1750, 1730); CLASSES = ("IR", "B", "OR@6"); TRAIN_SIZES = (7, 14); TEST_SIZE = 21
FS, SEG, NSEG, SUB, NSUB, SEED = 12000, 4096, 16, 512, 4, 20260926
MULT = {"BPFI": 5.4152, "BPFO": 3.5848, "BSF": 4.7135}


def env_feats(x, rpm):
    e = np.abs(hilbert(x)); e = e - e.mean()
    E = np.abs(np.fft.rfft(e * np.hanning(len(e)))); fr = np.fft.rfftfreq(len(e), 1 / FS); med = np.median(E[1:])
    out = {}
    for k, m in MULT.items():
        a = 0.0
        for h in (1, 2):
            f = h * m * rpm / 60; band = (fr >= 0.97 * f) & (fr <= 1.03 * f); a += float(E[band].max())
        out[f"B_env_{k}"] = float(np.log(a / med))
    return out


def seg_feats(x, rpm):
    x = x - x.mean(); sd = float(x.std())
    f = {"B_std": sd, "B_kurt": float(kurtosis(x)), "B_crest": float(np.abs(x).max() / sd), "B_sent": spectral_entropy(x)}
    f.update(env_feats(x, rpm))
    subs = [x[i * SUB:(i + 1) * SUB] for i in range(NSUB)]
    f["T_wind"] = float(np.median([winding_metric_fn(s) for s in subs]))
    f["T_cross"] = float(np.median([crossing_metric_fn(s) for s in subs]))
    f["T_phase"] = float(np.median([phase_winding_fn(s) for s in subs]))
    return f


def extract(rpm):
    z = zipfile.ZipFile(ZIP); FEAT.mkdir(parents=True, exist_ok=True); out = []
    for c in CLASSES:
        for size in TRAIN_SIZES + (TEST_SIZE,):
            name = f"{rpm}_{c}_{size}_DE12.npz"
            x = np.load(io.BytesIO(z.read(f"CWRU_Bearing_NumPy_4LUM-main/ORIGINAL_Data/{rpm} RPM/{name}")))["DE"].ravel().astype(float)
            for s in range(NSEG):
                out.append({"file": name, "cls": CLASSES.index(c), "size": size, "f": seg_feats(x[s * SEG:(s + 1) * SEG], rpm)})
    (FEAT / f"{rpm}.json").write_text(json.dumps(out)); print(rpm, len(out))


def positive_control():
    rng = np.random.default_rng(SEED); rows = []
    for c in (0, 1):
        for _ in range(100):
            x = rng.standard_normal(SEG)
            if c:
                x[::64] += 6.0
            rows.append((c, seg_feats(x, 1797)))
    names = list(rows[0][1]); X = np.array([[f[n] for n in names] for _, f in rows]); y = np.array([c for c, _ in rows])
    X = (X - X.mean(0)) / (X.std(0) + 1e-12)
    tr = np.r_[np.arange(50), np.arange(100, 150)]; te = np.r_[np.arange(50, 100), np.arange(150, 200)]
    return macro_f1(y[te], lda_predict(lda_fit(X[tr], y[tr]), X[te]))


def evaluate():
    names = None; res = {"prereg": "PREREG_CWRU_CROSS_BEARING_ENVELOPE_v0.1.md"}
    f1 = {}; neg = []; rng = np.random.default_rng(SEED)
    for rpm in RPMS:
        rows = json.loads((FEAT / f"{rpm}.json").read_text()); names = names or list(rows[0]["f"])
        sets = {"B": [n for n in names if n.startswith("B_")], "T": [n for n in names if n.startswith("T_")],
                "ENV": [n for n in names if n.startswith("B_env")]}
        sets["BT"] = sets["B"] + sets["T"]
        y = np.array([r["cls"] for r in rows]); te = np.array([r["size"] == TEST_SIZE for r in rows]); tr = ~te
        f1[rpm] = {}
        for s, cols in sets.items():
            X = np.array([[r["f"][n] for n in cols] for r in rows]); X = (X - X.mean(0)) / (X.std(0) + 1e-12)
            f1[rpm][s] = macro_f1(y[te], lda_predict(lda_fit(X[tr], y[tr]), X[te]))
            if s == "BT":
                neg.append(macro_f1(y[te], lda_predict(lda_fit(X[tr], rng.permutation(y[tr])), X[te])))
    g = np.array([f1[r]["BT"] - f1[r]["B"] for r in RPMS])
    if sum(f1[r]["B"] >= 0.97 for r in RPMS) >= 3:
        v = "INCONCLUSIVE (sufit)"
    elif g.mean() >= 0.05 and (g > 0).sum() >= 3:
        v = "SUPPORTED"
    elif g.mean() <= 0:
        v = "NOT SUPPORTED"
    else:
        v = "MIESZANY"
    pos = positive_control()
    res.update({"f1": f1, "gain": dict(zip(map(str, RPMS), g.tolist())), "mean_gain": float(g.mean()),
                "negative_control_mean_f1": float(np.mean(neg)), "positive_control_f1": pos})
    res["controls_passed"] = pos >= 0.9 and float(np.mean(neg)) <= 0.45
    res["verdict"] = v if res["controls_passed"] else "INCONCLUSIVE (kontrole)"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(int(sys.argv[2]))
    else:
        print(json.dumps(evaluate(), indent=1))
