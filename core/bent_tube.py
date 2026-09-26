"""bent_tube.py -- rura zgieta i skrecona: sygnal dwuskalowy (idea J. Kielicha, 2026-09-27).

Wolna czesc sygnalu (pasmo niskie, np. linie wirnika) -> OS rury: C(t) = (v t, Re z_L, Im z_L) -- os wygina sie
poprzecznie (krzywizna kappa_a) i skreca (torsja tau_a); jej predkosc |C'(t)| rozciaga / sciska rure wzdluz.
Szybka czesc (pasmo wysokie, np. dzwonienie uderzen) -> promien A_H(t) i kat phi_H(t) wokol zgietej osi:
X(t, theta) = C(t) + A_H(t) (cos theta N(t) + sin theta B(t)), (N, B) -- ramka Freneta osi.
Wzory: docs/theory/TIMDR_Analytic_Tube.md par. 6.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def band_analytic(x: np.ndarray, fs: float, lo: float, hi: float) -> np.ndarray:
    x = np.asarray(x, float) - np.mean(x); N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / fs)
    Z = np.zeros_like(X); m = (f >= lo) & (f < hi); Z[m] = 2 * X[m]
    return np.fft.ifft(Z)


@dataclass
class BentTube:
    t: np.ndarray
    axis: np.ndarray        # C(t), (N, 3)
    speed: np.ndarray       # |C'(t)| -- rozciaganie wzdluzne
    kappa: np.ndarray       # krzywizna osi -- zgiecie poprzeczne
    tau: np.ndarray         # torsja osi -- skret
    A: np.ndarray           # promien rury (obwiednia czesci szybkiej)
    phi: np.ndarray         # kat na obwodzie (faza czesci szybkiej)


def bent_tube(x: np.ndarray, fs: float, slow=(0.5, 200.0), fast=(1000.0, None), v: float = 1.0) -> BentTube:
    hi_fast = fast[1] if fast[1] is not None else fs / 2
    zL = band_analytic(x, fs, *slow); zH = band_analytic(x, fs, fast[0], hi_fast)
    t = np.arange(len(x)) / fs; C = np.stack([v * t, zL.real, zL.imag], 1); dt = 1 / fs
    d1 = np.gradient(C, dt, axis=0); d2 = np.gradient(d1, dt, axis=0); d3 = np.gradient(d2, dt, axis=0)
    c = np.cross(d1, d2); nc = np.linalg.norm(c, axis=1); sp = np.linalg.norm(d1, axis=1)
    kappa = nc / sp ** 3; tau = np.einsum("ij,ij->i", c, d3) / np.where(nc > 0, nc ** 2, np.nan)
    return BentTube(t, C, sp, kappa, tau, np.abs(zH), np.unwrap(np.angle(zH)))


def tube_surface(bt: BentTube, n_theta: int = 16, step: int = 1) -> np.ndarray:
    """Punkty powierzchni rury wokol zgietej osi (ramka Freneta), ksztalt (N/step, n_theta, 3) -- do wizualizacji."""
    C = bt.axis[::step]; T = np.gradient(C, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
    Nv = np.gradient(T, axis=0); n = np.linalg.norm(Nv, axis=1, keepdims=True); Nv = np.where(n > 1e-12, Nv / np.maximum(n, 1e-12), [0, 1, 0])
    B = np.cross(T, Nv); th = np.linspace(0, 2 * np.pi, n_theta, endpoint=False)
    A = bt.A[::step][:, None, None]
    return C[:, None, :] + A * (np.cos(th)[None, :, None] * Nv[:, None, :] + np.sin(th)[None, :, None] * B[:, None, :])


def bend_features(bt: BentTube, cut: float = 0.1) -> dict:
    """Cechy rury zgietej (bez brzegow): zgiecie, skret, rozciaganie wzdluzne, oddech promienia."""
    s = slice(int(cut * len(bt.t)), -int(cut * len(bt.t)) or None)
    r = np.hypot(bt.axis[s, 1], bt.axis[s, 2])
    return {"bend_radius": float(np.median(r)), "kappa": float(np.median(bt.kappa[s])), "tau": float(np.median(bt.tau[s])),
            "stretch": float(bt.speed[s].std() / bt.speed[s].mean()), "breath": float(bt.A[s].std() / bt.A[s].mean())}
