"""Turbina LBF: gondola/wieza jako zgieta rura (orbita) -- niewywazenie wirnika.

Rura: z(t) = x(t) + i y(t) z akcelerometru szczytu wiezy (plaszczyzna pozioma). Oba kierunki drgan = jeden
sygnal zespolony, wiec rura ma naturalna os i kat: promien = wychylenie orbity, kat = kierunek, skret = obieg.
Niewywazenie = sila odsrodkowa wirujaca z wirnikiem -> orbita obiega w tym samym kierunku co wirnik (winding +1
na obrot). Zegar: tachometr (jak w v0.1 turbiny) -> os katowa wirnika, widmo w rzedach.
Odpowiednik klasyczny: pelne widmo (full spectrum) i orbity z rotordynamiki; bazowo -- amplituda 1x w kazdym
kanale osobno (order tracking, bez kierunku).
"""
import numpy as np
from scipy.interpolate import interp1d
import wind_lbf_io as io

Q = 100                  # 2960 Hz -> 29,6 Hz
SPR = 64                 # probek na obrot po resamplingu katowym
ORD = (0.5, 3.5)


def shaft_angle(tach, ft):
    up = np.where((tach[1:] >= 2.0) & (tach[:-1] < 2.0))[0]
    return up / ft, np.arange(len(up)) / io.TACH_PPR          # czas impulsow, obroty


def order_resample(x, fs, tt, rev):
    t = np.arange(len(x)) / fs
    r0, r1 = rev[0], rev[-1]
    rg = np.arange(np.ceil(r0 * SPR), np.floor(r1 * SPR)) / SPR
    tq = interp1d(rev, tt)(rg)
    return interp1d(t, x, bounds_error=False, fill_value=0.0)(tq), rg


def orbit_features(cls, name, ch=('top_l_x', 'top_l_y')):
    fs, C, tach, ft = io.load(cls, name, channels=ch)
    x = io.dec(C[ch[0]].astype(float), Q); y = io.dec(C[ch[1]].astype(float), Q); fsd = fs / 25 / Q
    tt, rev = shaft_angle(tach, ft)
    if len(rev) < 20 * io.TACH_PPR:
        return None
    xo, rg = order_resample(x - x.mean(), fsd, tt, rev); yo, _ = order_resample(y - y.mean(), fsd, tt, rev)
    n = len(xo); w = np.hanning(n)
    Z = np.fft.fftshift(np.fft.fft((xo + 1j * yo) * w)) / w.sum()           # pelne widmo (rzedy +/-)
    o = np.fft.fftshift(np.fft.fftfreq(n, 1 / SPR))
    X = np.fft.rfft(xo * w) / w.sum(); Y = np.fft.rfft(yo * w) / w.sum(); oo = np.fft.rfftfreq(n, 1 / SPR)
    def pk(S, f, c):
        m = np.abs(f - c) <= 0.02; return float(np.abs(S[m]).max())
    def bg(S, f, c):
        m = (np.abs(f - c) > 0.05) & (np.abs(f - c) < 0.3); return float(np.median(np.abs(S[m])))
    speed = float(np.median(1 / (io.TACH_PPR * np.diff(tt))))
    out = {'cls': cls, 'name': name, 'speed': speed, 'n_rev': float(rev[-1] - rev[0])}
    for k in (1.0, 1.5, 2.0, 2.5):                                          # 1.5, 2.5 = kontrola dnia
        out[f'X{k}'] = np.log(pk(X, oo, k) / bg(X, oo, k)); out[f'Y{k}'] = np.log(pk(Y, oo, k) / bg(Y, oo, k))
        fwd, bwd = pk(Z, o, k), pk(Z, o, -k)
        out[f'F{k}'] = np.log(fwd / bg(Z, o, k)); out[f'B{k}'] = np.log(bwd / bg(Z, o, -k))
        out[f'D{k}'] = np.log(fwd / bwd)                                     # kierunek obiegu (winding)
    return {k: (float(v) if not isinstance(v, str) else v) for k, v in out.items()}
