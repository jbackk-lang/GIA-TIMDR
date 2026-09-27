"""Cechy migawek PRONOSTIA: klasyczne (RMS, kurtoza) + TIMDR (P, D, sito z kotwica Q, linie K walu)."""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.stats import kurtosis
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import pronostia_io as pio  # noqa: E402
from core.transition_params import event_density, band_envelope  # noqa: E402

BAND = (1000.0, 12000.0)
NPAD = 16384
CACHE = pio.DATA / "_features_v0_1"


def snap_features(x, fr):
    x = x - x.mean()
    env = band_envelope(x, pio.FS, *BAND)
    e2 = env ** 2; k = max(1, int(0.05 * len(e2)))
    P = float(np.sort(e2)[-k:].sum() / e2.sum())
    d = event_density(env, pio.FS)
    E = np.abs(np.fft.rfft((env - env.mean()) * np.hanning(len(env)), NPAD)); fa = np.fft.rfftfreq(NPAD, 1 / pio.FS)
    base = np.median(E[(fa > 20) & (fa < 1000)]) + 1e-12
    def pk(c, tol=0.03):
        m = np.abs(fa - c) <= max(tol * c, 1.6); return E[m].max() / base
    Q = {h: float(np.log(pk(m * fr) + pk(2 * m * fr))) for h, m in pio.MULT.items() if h != "FTF"}
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), NPAD)); fx = np.fft.rfftfreq(NPAD, 1 / pio.FS)
    bx = np.median(X[(fx > 10) & (fx < 500)]) + 1e-12
    K = float(np.log((X[np.abs(fx - fr) <= 1.6].max() + X[np.abs(fx - 2 * fr) <= 1.6].max()) / bx))
    return {"rms": float(np.sqrt(np.mean(x ** 2))), "kurt": float(kurtosis(x)), "P": P, "D": d["D"], "eta": d["eta"],
            "Q_BPFO": Q["BPFO"], "Q_BPFI": Q["BPFI"], "Q_BSF": Q["BSF"], "Q": max(Q.values()), "K": K}


def extract(b, budget=165):
    t0 = time.time(); out = CACHE / f"{b}.json"; CACHE.mkdir(exist_ok=True)
    rows = json.loads(out.read_text()) if out.exists() else []
    done = {r["file"] for r in rows}; fr = pio.fr(b)
    for f in pio.snapshots(b):
        if f in done:
            continue
        h, v = pio.read(b, f)
        rows.append({"file": f, "h": snap_features(h, fr), "v": snap_features(v, fr)})
        if time.time() - t0 > budget:
            break
    rows.sort(key=lambda r: r["file"]); out.write_text(json.dumps(rows))
    return len(rows), len(pio.snapshots(b))


if __name__ == "__main__":
    for b in sys.argv[1:]:
        print(b, extract(b))
