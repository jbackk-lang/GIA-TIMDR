"""Radar jako rura (idea J. Kielicha: zwinac pole widma Dopplera z powrotem w sygnal i badac go jak w rurze).

Zwiniecie: klatka = widmo Dopplera (pole) -> odwrotna FFT -> z(t) = I + iQ w czasie wolnym (1008 impulsow).
Z oknem akwizycji: uzywamy srodka (okno > 0,5 max, ok. 12 ms) i dzielimy przez okno.
Rura: promien A = |z|, kat phi = arg z, skret = dphi/dt. Po demodulacji Dopplerem ciala:
  os (wolna czesc, |f| < 300 Hz)   -> C(t) = (t, Re z_L, Im z_L): zgiecie (krzywizna) i skret osi (torsja),
  szybka czesc (|f| >= 1 kHz)      -> promien A_H(t) wokol osi: blyski (czasteczkowosc), rytm blyskow, drgania skretu.
Clutter zerowego Dopplera (+-2 biny) usuwany przed zwinieciem.
"""
import numpy as np
from analytic_tube import helix_curvature_torsion

AX_HZ, FAST_HZ = 300.0, 1000.0
LAG_MS = (1.5, 8.0)


def fold_frames(spec, prf, wp):
    """(F,N) widma -> slownik skladowych rury dla kazdej klatki (tylko srodek okna)."""
    F, N = spec.shape
    f = (np.arange(N) - N // 2) * prf / N
    P = np.abs(spec) ** 2
    Pm = P.copy(); Pm[:, N // 2 - 2: N // 2 + 3] = 0
    kb = np.argmax(Pm, 1)
    ce = np.where(wp > 0.5 * wp.max())[0]; w = wp[ce]
    t = np.arange(N) / prf
    out = []
    for i in range(F):
        s = spec[i].copy(); s[N // 2 - 2: N // 2 + 3] = 0          # bez cluttera
        fb = f[kb[i]]
        rel = f - fb
        rel = (rel + prf / 2) % prf - prf / 2                        # Doppler wzgledem ciala (kolowo)
        def fold(mask):
            z = np.fft.ifft(np.fft.ifftshift(np.where(mask, s, 0)))
            return (z * np.exp(-2j * np.pi * fb * t))[ce] / w
        out.append((fold(np.abs(rel) < AX_HZ), fold(np.abs(rel) >= FAST_HZ), fold(np.ones(N, bool))))
    return out, 1.0 / prf


def tube_feats(zL, zH, zA, dt):
    eA = np.abs(zA) ** 2; eH = np.abs(zH) ** 2
    thick = float(np.log((eH.sum() + 1e-30) / (eA.sum() + 1e-30)))           # grubosc szybkiej rury
    k = max(1, int(round(0.05 * len(eH))))
    particle = float(np.sort(eH)[-k:].sum() / (eH.sum() + 1e-30))           # blyski promienia
    a = np.abs(zH) - np.abs(zH).mean()
    ac = np.correlate(a, a, 'full')[len(a) - 1:]; ac = ac / (ac[0] + 1e-30)
    l0, l1 = int(LAG_MS[0] * 1e-3 / dt), int(LAG_MS[1] * 1e-3 / dt)
    rhythm = float(ac[l0:l1].max())                                          # rytm blyskow (oddech rury)
    ph = np.unwrap(np.angle(zH)); om = np.diff(ph) / dt
    twist = float(np.log(np.median(np.abs(om - np.median(om))) + 1))         # drgania skretu
    C = np.stack([np.arange(len(zL)) * dt * 1e3, zL.real / (np.abs(zL).mean() + 1e-12), zL.imag / (np.abs(zL).mean() + 1e-12)], 1)
    kap, tau = helix_curvature_torsion(C, dt * 1e3)
    m = slice(len(kap) // 10, len(kap) - len(kap) // 10)
    bend = float(np.log(np.median(kap[m]) + 1e-12)); tors = float(np.log(np.median(np.abs(tau[m])) + 1e-12))
    return [thick, particle, rhythm, twist, bend, tors]


TUBE_NAMES = ['T_thick', 'T_particle', 'T_rhythm', 'T_twist', 'T_bend', 'T_torsion']


def track_tube(t, wp):
    fr, dt = fold_frames(t['spec'], float(t['prf']), wp)
    V = np.array([tube_feats(zL, zH, zA, dt) for zL, zH, zA in fr])
    return [float(v) for v in np.r_[np.nanmedian(V, 0), np.nanpercentile(V, 90, 0)]]
