"""Hell Bridge Test Arena (stalowy most kratownicowy, Norwegia, 2020): kotwica modalna K + ksztalt modu (rodzina Gamma).
PREREG_HBTA_MODAL_ANCHOR_v0_1. Rejestracje 'Noise mode' (szum 1-100 Hz z wibratora, P2, pionowo), 59 kanalow z, 100 Hz.

Konstrukcja wg drogowskazow: wymuszenie szumem -> rezim pola/fali -> droga przez linie K przy kotwicy.
Kotwice: 8 czestotliwosci wlasnych wyznaczonych RAZ z rejestracji uczacej UDS_01 (6.86 ... 32.32 Hz).
W kazdym oknie 60 s kotwica sie samokoryguje: szczyt widma wielokanalowego w +-4% (interpolacja paraboliczna).
Cechy TIMDR (16): wzgledne przesuniecie czestotliwosci kotwicy + (1 - MAC) ksztaltu modu w 59 kanalach wzgledem uczenia.
Odniesienie klasyczne: AR(5) na kanalach z (295 wspolczynnikow) -> PCA 10 (uczone na UDS_01).
Detektor jak LANL v0.1: srednia odleglosc do k = 3 najblizszych okien uczacych po standaryzacji mediana/MAD.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.signal import welch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_lanl_3story_bridge import novelty, auc  # noqa: E402

H5 = Path(__file__).resolve().parent.parent.parent / "DATA" / "hell_bridge" / "data_100Hz.h5"
FS, WIN = 100.0, 6000
ANCH = [6.86, 7.42, 9.40, 12.79, 17.26, 24.12, 30.08, 32.32]
TRAIN = "MVS_P2_UDS_NM_Z_01"; UND_TEST = "MVS_P2_UDS_NM_Z_02"
DAMAGED = [f"MVS_P2_DS{i}_NM_Z_01" for i in range(1, 9)]
RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_HBTA_MODAL_ANCHOR_v0_1.json"


def load(name):
    import h5py
    with h5py.File(H5, "r") as f:
        g = f[name]; acc = g["acceleration"]; names = sorted(acc.keys())
        X = np.array([acc[n]["z"][:] for n in names]); T = int(g.attrs["temperature"])
    return X, T


def windows(X):
    return [X[:, s:s + WIN] for s in range(0, X.shape[1] - WIN + 1, WIN)]


def anchor_feats(W):
    f, P = welch(W - W.mean(1, keepdims=True), FS, nperseg=2048)
    S = (P / np.median(P, 1, keepdims=True)).mean(0)
    fr, shapes = [], []
    for a in ANCH:
        m = np.where(np.abs(f - a) <= 0.04 * a)[0]; j = m[np.argmax(S[m])]
        if 0 < j < len(S) - 1:
            y0, y1, y2 = np.log(S[j - 1:j + 2]); d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
        else:
            d = 0.0
        fr.append(f[j] + d * (f[1] - f[0]))
        v = np.sqrt(P[:, j]); shapes.append(v / (np.linalg.norm(v) + 1e-12))
    return np.array(fr), np.array(shapes)


def ar_coefs(x, p=5):
    x = (x - x.mean()) / (x.std() + 1e-12)
    A = np.stack([x[p - i - 1:len(x) - i - 1] for i in range(p)], 1)
    return np.linalg.lstsq(A, x[p:], rcond=None)[0]


def record_features(name):
    X, T = load(name); rows = []
    for W in windows(X):
        fr, sh = anchor_feats(W); ar = np.concatenate([ar_coefs(c) for c in W])
        rows.append({"f": fr, "shape": sh, "ar": ar})
    return rows, T


def final():
    tr, Ttr = record_features(TRAIN)
    f0 = np.median([r["f"] for r in tr], 0); sh0 = np.mean([r["shape"] for r in tr], 0)
    sh0 = sh0 / np.linalg.norm(sh0, axis=1, keepdims=True)
    def timdr(rows):
        out = []
        for r in rows:
            mac = [float(np.dot(r["shape"][k], sh0[k]) ** 2) for k in range(len(ANCH))]
            out.append(np.r_[(r["f"] - f0) / f0, 1 - np.array(mac)])
        return np.array(out)
    Atr = np.array([r["ar"] for r in tr]); mu = Atr.mean(0); U, s, Vt = np.linalg.svd(Atr - mu, full_matrices=False); V = Vt[:10].T
    ar = lambda rows: (np.array([r["ar"] for r in rows]) - mu) @ V
    Ttr_f, Atr_f = timdr(tr), ar(tr)
    und, Tund = record_features(UND_TEST)
    res = {"prereg": "PREREG_HBTA_MODAL_ANCHOR_v0_1.md", "n_train_windows": len(tr), "temp": {TRAIN: Ttr, UND_TEST: Tund},
           "anchors_train_median_hz": f0.tolist(), "auc": {}, "alarm": {}}
    sc = {"T": (lambda R: novelty(Ttr_f, timdr(R))), "AR": (lambda R: novelty(Atr_f, ar(R)))}
    thr = {"T": np.percentile(novelty(Ttr_f, Ttr_f, loo=True), 95), "AR": np.percentile(novelty(Atr_f, Atr_f, loo=True), 95)}
    s_und = {k: fn(und) for k, fn in sc.items()}
    res["alarm"]["UDS_02"] = {k: float(np.mean(s_und[k] > thr[k])) for k in sc}
    shifts = {}
    for name in DAMAGED:
        R, T = record_features(name); ds = name.split("_")[2]; res["temp"][name] = T
        res["auc"][ds] = {k: auc(s_und[k], fn(R)) for k, fn in sc.items()}
        res["alarm"][ds] = {k: float(np.mean(fn(R) > thr[k])) for k, fn in sc.items()}
        shifts[ds] = (np.median([r["f"] for r in R], 0) - f0).tolist()
    res["freq_shift_hz"] = shifts
    mean = lambda k, ds: float(np.mean([res["auc"][d][k] for d in ds]))
    allds = [f"DS{i}" for i in range(1, 9)]
    res["mean_auc"] = {k: mean(k, allds) for k in sc}
    res["H1"] = "SUPPORTED" if res["mean_auc"]["T"] >= 0.90 else "NOT SUPPORTED"
    res["H2"] = "SUPPORTED" if res["mean_auc"]["T"] >= res["mean_auc"]["AR"] - 0.02 else "NOT SUPPORTED"
    easy, hard = ["DS1", "DS2", "DS8"], ["DS3", "DS4", "DS5", "DS6", "DS7"]
    res["H3"] = {"easy": mean("T", easy), "hard": mean("T", hard),
                 "verdict": "SUPPORTED" if mean("T", easy) > mean("T", hard) else "NOT SUPPORTED"}
    res["H4"] = "SUPPORTED" if res["alarm"]["UDS_02"]["T"] <= 0.2 else "NOT SUPPORTED"
    RESULT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = final(); print(json.dumps({k: r[k] for k in ("temp", "auc", "alarm", "mean_auc", "H1", "H2", "H3", "H4")}, indent=1))
