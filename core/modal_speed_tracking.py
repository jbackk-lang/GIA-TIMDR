"""modal_speed_tracking.py -- samonaprawa modelu w czasie: sledzenie predkosci z samych drgan + os katowa.

Rozszerzenie `modal_self_repair.py` na zmienna predkosc (turbiny wiatrowe). Model (rzedy: np. BPFO = 3,05 obrotu)
jest staly; naprawiana jest OS CZASU: z drgan sledzimy predkosc f_r(t) (grzebien harmonicznych rzedu odniesienia,
kazda ramka startuje z poprzedniego oszacowania -- samonaprawa krok po kroku), potem obwiednie rur pasm przeliczamy
na os katowa (rzedy), gdzie uszkodzenie ma stala czestotliwosc. Tachometr NIE jest wejsciem -- sluzy tylko do oceny.
Wzory: docs/theory/TIMDR_Modal_Self_Repair.md, par. 6.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence

import numpy as np
from scipy.signal import stft


@dataclass
class SpeedTrack:
    t: np.ndarray        # czasy srodkow ramek [s]
    fr: np.ndarray       # sledzona czestotliwosc obrotowa [Hz]
    score: np.ndarray    # sila grzebienia (tlo ~ 1)


def track_speed(x: np.ndarray, fs: float, f_lo: float, f_hi: float, ref_orders: Sequence[float] = (1, 2, 3),
                frame_s: float = 2.0, hop_s: float = 0.25, max_step: float = 0.05, grid_step: float = 0.002,
                decim_to: float = 2000.0) -> SpeedTrack:
    """Sledzi f_r(t): dla kazdej ramki wybiera f maksymalizujace sume widma przy k*f (k w ref_orders).
    Pierwsza ramka: przeszukanie [f_lo, f_hi]; kolejne: +-max_step wokol poprzedniego oszacowania."""
    x = np.asarray(x, float) - np.mean(x)
    q = max(1, int(fs // decim_to)); xd = x[::q] if q == 1 else _lowpass_decimate(x, q); fsd = fs / q
    nper = int(frame_s * fsd); f, tt, Z = stft(xd, fsd, nperseg=nper, noverlap=nper - int(hop_s * fsd), padded=False, boundary=None)
    P = np.abs(Z); P = P / (np.median(P, axis=0, keepdims=True) + 1e-12)
    out, sc, prev = [], [], None
    for j in range(P.shape[1]):
        lo, hi = (f_lo, f_hi) if prev is None else (prev * (1 - max_step), prev * (1 + max_step))
        cand = np.arange(max(lo, f_lo), min(hi, f_hi) + grid_step, grid_step * (prev or 1.0))
        s = np.zeros(len(cand))
        for k in ref_orders:
            s += np.interp(k * cand, f, P[:, j])
        i = int(np.argmax(s)); prev = float(cand[i]); out.append(prev); sc.append(float(s[i] / len(ref_orders)))
    return SpeedTrack(tt, np.array(out), np.array(sc))


def _lowpass_decimate(x, q):
    from scipy.signal import decimate
    y = x
    while q > 1:
        step = min(q, 8)
        while q % step:
            step -= 1
        y = decimate(y, step, ftype="fir", zero_phase=True); q //= step
    return y


def shaft_phase(track: SpeedTrack, n: int, fs: float) -> np.ndarray:
    """Kat walu theta(t) [obroty] = calka f_r dt (f_r interpolowane liniowo miedzy srodkami ramek)."""
    t = np.arange(n) / fs; fr = np.interp(t, track.t, track.fr)
    return np.concatenate([[0.0], np.cumsum((fr[1:] + fr[:-1]) / 2) / fs])


def order_resonance_map(x: np.ndarray, fs: float, theta: np.ndarray, bands: Sequence[tuple], spr: int = 64,
                        omin: float = 0.5, omax: float = 20.0):
    """Mapa rezonansu wiazki rur w dziedzinie rzedow: obwiednia kazdego pasma nosnego (Hz) przeliczona na
    rowne kroki kata (spr probek na obrot); widmo -> rzedy; tlo (mediana) = 1."""
    x = np.asarray(x, float) - np.mean(x); N = len(x); X = np.fft.fft(x); f = np.fft.fftfreq(N, 1 / fs)
    th_u = np.arange(theta[0], theta[-1], 1.0 / spr); rows = []
    orders = np.fft.rfftfreq(len(th_u), 1.0 / spr); m = (orders >= omin) & (orders <= omax); w = np.hanning(len(th_u))
    for lo, hi in bands:
        Zb = np.zeros_like(X); sel = (f >= lo) & (f < hi); Zb[sel] = 2 * X[sel]
        e = np.abs(np.fft.ifft(Zb)); eu = np.interp(th_u, theta, e); eu = eu - eu.mean()
        E = np.abs(np.fft.rfft(eu * w))[m]; rows.append(E / (np.median(E) + 1e-12))
    return np.array(rows), orders[m]


def order_sieve(Rz: np.ndarray, orders: np.ndarray, fault_orders: Dict[str, float], tol: float = 0.03) -> Dict[str, float]:
    """Sito samokorygujace w dziedzinie rzedow (jak cechy Q): oczka = rezonans rur przy rzedzie uszkodzenia."""
    out = {}
    for k, o in fault_orders.items():
        b1 = np.where((orders >= (1 - tol) * o) & (orders <= (1 + tol) * o))[0]
        j = b1[np.argmax(Rz[:, b1].max(0))]; v = np.clip(Rz[:, j] - 1, 0, None)
        w = v / v.sum() if v.sum() > 0 else np.full(len(v), 1 / len(v)); S = w @ Rz; a = 0.0
        for h in (1, 2):
            band = (orders >= (1 - tol) * h * o) & (orders <= (1 + tol) * h * o); a += float(S[band].max())
        out[f"QO_{k}"] = float(np.log(a))
    return out


def track_speed_viterbi(x: np.ndarray, fs: float, f_lo: float, f_hi: float, ref_orders: Sequence[float] = (1, 2, 3),
                        frame_s: float = 8.0, hop_s: float = 1.0, max_step: float = 0.05, penalty: float = 20.0,
                        n_grid: int = 600) -> SpeedTrack:
    """Sledzenie predkosci jako globalna sciezka (Viterbi) przez mape grzebienia: kazda ramka ocenia kandydatow f
    (srednia widma przy k*f), przejscie miedzy ramkami ograniczone do +-max_step i karane penalty*|dlog f|.
    Samonaprawa calej sciezki naraz zamiast krok po kroku (odporna na slabe linie)."""
    x = np.asarray(x, float) - np.mean(x)
    nper = int(frame_s * fs); f, tt, Z = stft(x, fs, nperseg=nper, noverlap=nper - int(hop_s * fs), padded=False, boundary=None)
    P = np.abs(Z); P = P / (np.median(P, axis=0, keepdims=True) + 1e-12)
    cand = np.exp(np.linspace(np.log(f_lo), np.log(f_hi), n_grid)); lc = np.log(cand)
    S = np.stack([np.mean([np.interp(k * cand, f, P[:, j]) for k in ref_orders], axis=0) for j in range(P.shape[1])])
    dl = np.abs(lc[:, None] - lc[None, :]); allowed = dl <= np.log(1 + max_step)
    cost = np.where(allowed, penalty * dl, np.inf)
    acc = np.log(S[0] + 1e-12); back = np.zeros((len(tt), n_grid), int)
    for j in range(1, len(tt)):
        tot = acc[None, :] - cost          # [nowy, stary]
        back[j] = np.argmax(tot, axis=1); acc = tot[np.arange(n_grid), back[j]] + np.log(S[j] + 1e-12)
    path = np.zeros(len(tt), int); path[-1] = int(np.argmax(acc))
    for j in range(len(tt) - 1, 0, -1):
        path[j - 1] = back[j, path[j]]
    return SpeedTrack(tt, cand[path], S[np.arange(len(tt)), path])
