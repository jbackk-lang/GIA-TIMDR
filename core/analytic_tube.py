"""analytic_tube.py -- rura analityczna: zwiniecie sygnalu (i pola pasm) w rure, most M/S <-> G.

Wzory: docs/theory/TIMDR_Analytic_Tube.md. Sygnal x(t) -> sygnal analityczny z = x + i*H[x] = A*exp(i*phi).
Krzywa Gamma(t) = (v*t, A cos phi, A sin phi) lezy na powierzchni obrotowej (rurze) o promieniu A(t) wokol osi t:
promien rury = obwiednia, kat na obwodzie = faza, tempo skretu = czestotliwosc chwilowa. Powrot: x = A cos phi.
v [jednostki/s] to jawny parametr konstrukcji (predkosc wzdluz osi), jak r_0 w TIMDR_Geometry_From_EventGraph.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

import numpy as np
from scipy.signal import hilbert


@dataclass
class AnalyticTube:
    t: np.ndarray        # czas [s]
    A: np.ndarray        # promien rury = obwiednia
    phi: np.ndarray      # kat na obwodzie = faza (rozwinieta)
    omega: np.ndarray    # tempo skretu = czestotliwosc katowa chwilowa [rad/s]
    curve: np.ndarray    # spirala Gamma(t), ksztalt (N, 3)
    v: float


def tube_from_signal(x: Sequence[float], fs: float, v: float = 1.0) -> AnalyticTube:
    x = np.asarray(x, float)
    z = hilbert(x); A = np.abs(z); phi = np.unwrap(np.angle(z)); t = np.arange(len(x)) / fs
    omega = np.gradient(phi, 1 / fs)
    curve = np.stack([v * t, A * np.cos(phi), A * np.sin(phi)], axis=1)
    return AnalyticTube(t, A, phi, omega, curve, v)


def reconstruct(A: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """Powrot z rury do sygnalu: x = A cos phi."""
    return A * np.cos(phi)


def winding_turns(phi: np.ndarray) -> float:
    """Liczba okrazen spirali wokol rury (ta sama definicja co phase_winding_fn)."""
    return float(abs(phi[-1] - phi[0]) / (2 * np.pi))


def revolution_curvatures(A: np.ndarray, du: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Krzywizny rury jako powierzchni obrotowej o profilu r(u) = A, u = v t (normalna do wnetrza):
    kappa_meridian = -r''/(1+r'^2)^(3/2), kappa_parallel = 1/(r sqrt(1+r'^2)), H = srednia, K = iloczyn."""
    r1 = np.gradient(A, du); r2 = np.gradient(r1, du); g = 1 + r1 ** 2
    km = -r2 / g ** 1.5; kp = 1 / (A * np.sqrt(g))
    return km, kp, (km + kp) / 2, km * kp


def helix_curvature_torsion(curve: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
    """Krzywizna i skret (Frenet) spirali Gamma(t) z roznic skonczonych."""
    d1 = np.gradient(curve, dt, axis=0); d2 = np.gradient(d1, dt, axis=0); d3 = np.gradient(d2, dt, axis=0)
    c = np.cross(d1, d2); nc = np.linalg.norm(c, axis=1)
    kappa = nc / np.linalg.norm(d1, axis=1) ** 3
    tau = np.einsum("ij,ij->i", c, d3) / np.where(nc > 0, nc ** 2, np.nan)
    return kappa, tau


def band_tubes(x: Sequence[float], fs: float, bands: List[Tuple[float, float]]) -> Tuple[np.ndarray, np.ndarray]:
    """Zwiniecie pola pasm: dla kazdego pasma nosnego wlasna rura (promien A_b(t), faza phi_b(t)).
    Sygnal analityczny pasma liczony przez maske widma (jak w sicie rezonansowym)."""
    x = np.asarray(x, float); N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / fs); A, P = [], []
    for lo, hi in bands:
        Z = np.zeros_like(X); m = (f >= lo) & (f < hi); Z[m] = 2 * X[m]; z = np.fft.ifft(Z)
        A.append(np.abs(z)); P.append(np.unwrap(np.angle(z)))
    return np.array(A), np.array(P)


def breathing_spectrum(A: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    """Widmo 'oddychania' rury: widmo zmian promienia (= widmo obwiedni). To czyta sito rezonansowe."""
    a = A - A.mean(); E = np.abs(np.fft.rfft(a * np.hanning(len(a))))
    return np.fft.rfftfreq(len(a), 1 / fs), E
