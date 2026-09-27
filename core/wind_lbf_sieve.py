"""wind_lbf_sieve.py -- sito w osi katowej (zegar: tachometr) vs sito przy stalej predkosci, turbina Fraunhofer LBF.
Na plik: segmenty 60 s; drgania lozyska -> decymacja x2 (37 kHz) -> pasma nosne 1-16 kHz -> obwiednie ->
(a) os katowa z tachometru -> mapa rezonansu w rzedach -> sito QO (oczka per hipoteza);
(b) stala predkosc = srednia z tachometru w segmencie -> mapa w Hz -> sito Q przy rzedzie * srednia predkosc.
Wynik pliku = mediana z segmentow."""
from __future__ import annotations
import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.wind_lbf_io import load, tach_speed, dec, MULT  # noqa: E402
from core.modal_speed_tracking import order_resonance_map, order_sieve  # noqa: E402

BANDS = [(1000.0 * i, 1000.0 * (i + 1)) for i in range(1, 9)]   # po decymacji x4 (18,5 kHz)
SEG_S, MAXSEG, MIN_REV, HYP = 60.0, 3, 10.0, {"BPFO": MULT["BPFO"], "BPFI": MULT["BPFI"], "BSF2": 2 * MULT["BSF"]}


def resonance_map_hz(x, fs, bands, amin=0.2, amax=60.0):
    """Mapa rezonansu w Hz z dolna granica 0,2 Hz (czestotliwosci uszkodzen tej turbiny to ~1-4 Hz)."""
    N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / fs)
    a = np.fft.rfftfreq(N, 1 / fs); am = (a >= amin) & (a <= amax); w = np.hanning(N); rows = []
    for lo, hi in bands:
        Z = np.zeros_like(X); m = (f >= lo) & (f < hi); Z[m] = 2 * X[m]
        e = np.abs(np.fft.ifft(Z)); e = e - e.mean(); E = np.abs(np.fft.rfft(e * w))[am]; rows.append(E / (np.median(E) + 1e-12))
    return np.array(rows), a[am]


def hz_sieve(Rz, al, fr, orders, tol=0.03):
    out = {}
    for k, o in orders.items():
        fc = o * fr; b1 = np.where((al >= (1 - tol) * fc) & (al <= (1 + tol) * fc))[0]
        j = b1[np.argmax(Rz[:, b1].max(0))]; v = np.clip(Rz[:, j] - 1, 0, None)
        w = v / v.sum() if v.sum() > 0 else np.full(len(v), 1 / len(v)); S = w @ Rz; a = 0.0
        for h in (1, 2):
            band = (al >= (1 - tol) * h * fc) & (al <= (1 + tol) * h * fc); a += float(S[band].max())
        out[f"QH_{k}"] = float(np.log(a))
    return out


def file_features(cls, name, channel="brng_f_y"):
    fs, c, tach, ft = load(cls, name, (channel,)); x = dec(c[channel], 4); fs2 = fs / 4
    tt, fr = tach_speed(tach, ft); n = int(SEG_S * fs2); rows = []
    starts = list(range(0, len(x) - n + 1, n))[:MAXSEG] or [0]      # krotszy plik: jeden segment = caly plik
    for s0 in starts:
        seg = x[s0:s0 + n]; t = (s0 + np.arange(len(seg))) / fs2
        m = (tt >= t[0]) & (tt <= t[-1])
        if m.sum() < 100:
            continue
        frt = np.interp(t, tt[m], fr[m]); th = np.concatenate([[0.0], np.cumsum((frt[1:] + frt[:-1]) / 2) / fs2])
        if th[-1] < MIN_REV:          # za malo obrotow w segmencie (wirnik prawie stoi) -- segment pomijany
            continue
        Ro, o = order_resonance_map(seg, fs2, th, BANDS, spr=64, omin=0.5, omax=30.0)
        f = order_sieve(Ro, o, HYP)
        Rz, al = resonance_map_hz(seg, fs2, BANDS)
        f.update(hz_sieve(Rz, al, float(np.median(fr[m])), HYP)); f["fr_med"] = float(np.median(fr[m]))
        rows.append(f)
    if not rows:
        return None, 0
    return {k: float(np.median([r[k] for r in rows])) for k in rows[0]}, len(rows)


def segment_rows(cls, name, maxseg=5, channel="brng_f_y"):
    """Ocena: wiersz na segment 60 s (do maxseg), z cechami QO/QH oraz klasycznymi (kurtoza, RMS)."""
    from scipy.stats import kurtosis
    fs, c, tach, ft = load(cls, name, (channel,)); x = dec(c[channel], 4); fs2 = fs / 4
    tt, fr = tach_speed(tach, ft); n = int(SEG_S * fs2); rows = []
    starts = list(range(0, len(x) - n + 1, n))[:maxseg] or [0]
    for i, s0 in enumerate(starts):
        seg = x[s0:s0 + n]; t = (s0 + np.arange(len(seg))) / fs2
        m = (tt >= t[0]) & (tt <= t[-1])
        if m.sum() < 100:
            continue
        frt = np.interp(t, tt[m], fr[m]); th = np.concatenate([[0.0], np.cumsum((frt[1:] + frt[:-1]) / 2) / fs2])
        if th[-1] < MIN_REV:
            continue
        Ro, o = order_resonance_map(seg, fs2, th, BANDS, spr=64, omin=0.5, omax=30.0)
        f = order_sieve(Ro, o, HYP); Rz, al = resonance_map_hz(seg, fs2, BANDS)
        f.update(hz_sieve(Rz, al, float(np.median(fr[m])), HYP))
        f.update({"KURT": float(kurtosis(seg)), "RMS": float(seg.std()), "fr_med": float(np.median(fr[m])),
                  "rev": float(th[-1]), "cls": cls, "file": name, "seg": i})
        rows.append(f)
    return rows
