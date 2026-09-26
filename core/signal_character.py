"""signal_character.py -- krok 0 drogowskazow: czy sygnal jest MODALNY (sam jest widmem: wyrazne linie)
czy POLOWY (informacja w widmie pola: modulacje pasm nosnych). Hipoteza robocza, progi wstepne (2026-09-27).

L = udzial mocy w waskich liniach widma (bin > 10x lokalnej mediany widma, okno 1% pasma).
M = mediana po pasmach nosnych (1 kHz, od 1 kHz) sily najsilniejszej modulacji obwiedni (5-500 Hz, tlo = 1).
Etykieta: 'modalny' gdy L >= 0.5; 'polowy' gdy L < 0.5 i M >= 8; inaczej 'nieokreslony'.
"""
from __future__ import annotations

import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import welch

L_MODAL, M_FIELD = 0.5, 8.0


def line_fraction(x: np.ndarray, fs: float) -> float:
    f, P = welch(np.asarray(x, float) - np.mean(x), fs, nperseg=min(len(x), 8192))
    base = median_filter(P, size=max(5, len(P) // 100) | 1, mode="nearest")
    return float(P[P > 10 * base].sum() / P.sum())


def modulation_strength(x: np.ndarray, fs: float, n_seg: float = 2.0) -> float:
    x = np.asarray(x, float)[: int(n_seg * fs)]; x = x - x.mean(); N = len(x)
    X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / fs); a = np.fft.rfftfreq(N, 1 / fs); am = (a >= 5) & (a <= 500)
    w = np.hanning(N); vals = []; lo = 1000.0
    while lo + 1000 <= min(16000.0, fs / 2):
        Z = np.zeros_like(X); m = (f >= lo) & (f < lo + 1000); Z[m] = 2 * X[m]
        e = np.abs(np.fft.ifft(Z)); e = e - e.mean(); E = np.abs(np.fft.rfft(e * w))[am]
        vals.append(E.max() / (np.median(E) + 1e-12)); lo += 1000
    return float(np.median(vals)) if vals else float("nan")


def signal_character(x: np.ndarray, fs: float) -> dict:
    L = line_fraction(x, fs); M = modulation_strength(x, fs)
    label = "modalny" if L >= L_MODAL else ("polowy" if M >= M_FIELD else "nieokreslony")
    return {"L": L, "M": M, "typ": label}
