"""modal_self_repair.py -- samonaprawiajacy sie model modalny: most K <-> Chronoproces.

Wzory: docs/theory/TIMDR_Modal_Self_Repair.md. Modalnosci = rury pasm nosnych (promien A_b(t), faza, skret) z
rury analitycznej; model = przewidywane czestotliwosci modalne f_k(s) = m_k * s * f_r0 (s -- wspolczynnik predkosci,
nominalnie 1). Petla samonaprawy: model przewiduje -> rury pokazuja, gdzie jest rezonans -> blad przestraja s ->
powtorz. Wynik: naprawiony model s^, wielkosc naprawy |s^-1|, jakosc synchronizacji przed i po.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence

import numpy as np

AMIN, AMAX = 5.0, 500.0


def resonance_map(x: np.ndarray, fs: float, bands: Sequence[tuple]):
    """Mapa rezonansu wiazki rur: widmo oddechu (obwiedni) kazdej rury, tlo (mediana) = 1."""
    N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / fs)
    alpha = np.fft.rfftfreq(N, 1 / fs); am = (alpha >= AMIN) & (alpha <= AMAX); w = np.hanning(N); rows = []
    for lo, hi in bands:
        Z = np.zeros_like(X); m = (f >= lo) & (f < hi); Z[m] = 2 * X[m]
        e = np.abs(np.fft.ifft(Z)); e = e - e.mean()
        E = np.abs(np.fft.rfft(e * w))[am]; rows.append(E / (np.median(E) + 1e-12))
    return np.array(rows), alpha[am]


def _peak(al: np.ndarray, S: np.ndarray, fc: float, delta: float):
    """Szczyt S w oknie fc*(1 +- delta) z interpolacja paraboliczna: (czestotliwosc, wysokosc)."""
    idx = np.where((al >= (1 - delta) * fc) & (al <= (1 + delta) * fc))[0]
    if len(idx) == 0:
        return fc, 0.0
    j = idx[np.argmax(S[idx])]
    if 0 < j < len(S) - 1:
        a, b, c = S[j - 1], S[j], S[j + 1]; den = a - 2 * b + c
        off = 0.5 * (a - c) / den if den != 0 else 0.0
        off = float(np.clip(off, -0.5, 0.5))
    else:
        off = 0.0
    return float(al[j] + off * (al[1] - al[0])), float(S[j])


def lock_quality(Rz: np.ndarray, al: np.ndarray, freqs: Sequence[float], delta: float = 0.01) -> float:
    """Jakosc synchronizacji modelu z modalnosciami: srednia (po harmonicznych) wysokosc rezonansu
    najsilniej rezonujacej rury przy przewidywanej czestotliwosci (tlo = 1)."""
    return float(np.mean([Rz[:, (al >= (1 - delta) * f) & (al <= (1 + delta) * f)].max() for f in freqs]))


@dataclass
class RepairResult:
    s: float                       # naprawiony wspolczynnik predkosci
    repair: float                  # |s - 1|
    hypothesis: str                # hipoteza, do ktorej model sie zsynchronizowal
    quality_before: float
    quality_after: float
    trajectory: List[float] = field(default_factory=list)


def repair_model(x: np.ndarray, fs: float, rpm0: float, multipliers: Dict[str, float], bands: Sequence[tuple],
                 harmonics: int = 4, delta: float = 0.03, gain: float = 0.7, s_max: float = 0.06,
                 iters: int = 25, tol: float = 1e-5) -> RepairResult:
    Rz, al = resonance_map(np.asarray(x, float) - np.mean(x), fs, bands)
    fr0 = rpm0 / 60.0
    # wybor hipotezy: najsilniejszy rezonans modelu nominalnego (szerokie okno delta)
    def score(k, s, d):
        return lock_quality(Rz, al, [h * multipliers[k] * s * fr0 for h in range(1, harmonics + 1)], d)
    k = max(multipliers, key=lambda q: score(q, 1.0, delta))
    s = 1.0; traj = [s]; q0 = score(k, 1.0, 0.01)
    for _ in range(iters):
        # oczka sita dla biezacego modelu: rury rezonujace przy przewidywanej czestotliwosci
        f1 = multipliers[k] * s * fr0
        col = (al >= (1 - 0.01) * f1) & (al <= (1 + 0.01) * f1)
        v = np.clip(Rz[:, col].max(1) - 1, 0, None); w = v / v.sum() if v.sum() > 0 else np.full(len(v), 1 / len(v))
        S = w @ Rz; est, wt = [], []
        for h in range(1, harmonics + 1):
            fh, ph = _peak(al, S, h * f1, delta / h)
            est.append(fh / (h * multipliers[k] * fr0)); wt.append(max(ph - 1, 0))
        if sum(wt) == 0:
            break
        target = float(np.average(est, weights=wt))
        s_new = float(np.clip(s + gain * (target - s), 1 - s_max, 1 + s_max))
        traj.append(s_new)
        if abs(s_new - s) < tol:
            s = s_new; break
        s = s_new
    return RepairResult(s, abs(s - 1), k, q0, score(k, s, 0.01), traj)
