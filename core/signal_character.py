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
P_PARTICLE = 0.3   # szum gaussowski daje ok. 0,20; ton ok. 0,05


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


def particle_index(x: np.ndarray, fs: float, top: float = 0.05, hp: float = 1000.0) -> float:
    """Czasteczkowosc: udzial energii obwiedni w najsilniejszych 5% chwil. Liczone powyzej 1 kHz (jesli fs pozwala),
    bo uderzenia pobudzaja rezonanse wysokoczestotliwosciowe, a linie wirnika leza nizej."""
    x = np.asarray(x, float) - np.mean(x); N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / fs)
    Z = np.zeros_like(X); m = (f >= (hp if fs / 2 > 2 * hp else 0.0)); Z[m] = 2 * X[m]
    e2 = np.abs(np.fft.ifft(Z)) ** 2; k = max(1, int(top * N))
    return float(np.sort(e2)[-k:].sum() / e2.sum())


def duality(L: float, P: float, M: float) -> str:
    """Mapa dualnosci (analogia z Gaborem: dt*df >= 1/4pi, nie twierdzenie o fizyce kwantowej)."""
    wave, particle, rhythm = L >= L_MODAL, P >= P_PARTICLE, (M >= M_FIELD)
    if particle and rhythm:
        return "mieszany (fala + pakiet)" if wave else "pakiet falowy"
    if particle:
        return "czasteczkowy"
    if wave:
        return "falowy"
    return "polowy (modulowany szum)" if rhythm else "szumowy"


def signal_character(x: np.ndarray, fs: float) -> dict:
    L = line_fraction(x, fs); M = modulation_strength(x, fs); P = particle_index(x, fs)
    label = "modalny" if L >= L_MODAL else ("polowy" if M >= M_FIELD else "nieokreslony")
    return {"L": L, "M": M, "P": P, "typ": label, "dualnosc": duality(L, P, M)}
