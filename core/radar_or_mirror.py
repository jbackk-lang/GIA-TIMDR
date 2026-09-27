"""Open Radar v0.3 -- most K<->G "lustro" i "cien" (stereoskopia pol lustrzanych).

Odbicie: ruch zapisany jest w fazie nosnej, znak skretu I/Q = kierunek predkosci radialnej wzgledem radaru.
Pole w ukladzie linii ciala (kotwica K) ma dwie lustrzane polowki: +d (szybciej niz cialo) i -d (wolniej).
Stereoskopia: S = (E+ + E-)/2 -- czesc wspolna (znosi sie przy nalozeniu obrazow), A = (E+ - E-)/2 -- "cien"
(czesc antysymetryczna, zostaje po zniesieniu). E = log mocy pasma. Rytm (samokorekta): alfa* = argmax sumy
modulacji obu polowek (1x + 2x) w 0,5-9,5 Hz, na calym sladzie (regula wykonalnosci: N_cyk >= 10 wymaga > 2 s).
Cechy przy alfa*: koherencja lustra |S+-|^2/(S++ S--), faza lustra cos(arg S+-) (+1 w fazie, -1 w przeciwfazie),
udzial cienia R = P_A / (P_A + P_S); dla pasm bliskich (100-2100 Hz) i dalekich (2100-6100 Hz).
Odniesienie klasyczne na tym samym calym sladzie: diagram predkosci kadencji (CVD) + rozrzut Dopplera.
"""
import json, os
import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import csd, welch

DATA = os.path.join(os.path.dirname(__file__), '..', '..', 'DATA', 'open_radar')
EDGES = np.arange(-8000, 8001, 100.0); CEN = 0.5 * (EDGES[1:] + EDGES[:-1])
FSM = 20.0                                  # klatki / s (siatka 50 ms)
BANDS = [(100 + 500 * k, 600 + 500 * k) for k in range(12)]
NEAR = range(0, 4); FAR = range(4, 12)
ALPHA = (0.5, 9.5)
NPER = 64                                   # 3,2 s; koherencja tylko przy >= 3 segmentach (n >= 2*NPER)


def uniform(P, ts):
    """Klatki na rowna siatke 50 ms (ts w ms); brakujace klatki -- interpolacja liniowa log-mocy. Zwraca L, udzial luk."""
    k = np.round((ts - ts[0]) / 50.0).astype(int)
    k, u = np.unique(k, return_index=True); L = np.log(P[u].astype(float) + 1e-12)
    grid = np.arange(k[-1] + 1)
    out = np.stack([np.interp(grid, k, L[:, j]) for j in range(L.shape[1])], 1)
    return out, 1 - len(k) / len(grid)


def band_log(L, lo, hi, sign):
    m = (sign * CEN >= lo) & (sign * CEN < hi)
    return np.log(np.exp(L[:, m]).sum(1) + 1e-12)


def _detr(x):
    t = np.arange(len(x)); return x - np.polyval(np.polyfit(t, x, 1), t)


def mirror_feats(P, ts):
    L, gap = uniform(P, ts); n = len(L)
    if n < 16:
        return None, {'n': n, 'gap': gap}
    nper = min(NPER, n); few = n < 2 * NPER
    Ep = np.stack([_detr(band_log(L, lo, hi, +1)) for lo, hi in BANDS])
    Em = np.stack([_detr(band_log(L, lo, hi, -1)) for lo, hi in BANDS])
    f, Ppp = welch(Ep, FSM, nperseg=nper); _, Pmm = welch(Em, FSM, nperseg=nper)
    _, Ppm = csd(Ep, Em, FSM, nperseg=nper)
    _, PS = welch((Ep + Em) / 2, FSM, nperseg=nper); _, PA = welch((Ep - Em) / 2, FSM, nperseg=nper)
    sel = np.where((f >= ALPHA[0]) & (f <= ALPHA[1]))[0]
    norm = lambda X: X / (median_filter(X, size=(1, 9), mode='nearest') + 1e-30)   # lokalne tlo (bez nachylenia 1/f)
    sc = (norm(Ppp) + norm(Pmm)).sum(0)
    j2 = np.array([np.argmin(np.abs(f - 2 * f[j])) for j in sel])
    tot = sc[sel] + np.where(f[j2] <= FSM / 2, sc[j2], 0)
    j = sel[np.argmax(tot)]; a = f[j]
    out = {'alpha': float(a), 'Q': float(np.log(tot.max() / (2 * len(BANDS)))), 'n': n, 'gap': gap,
           'N_cyk': float(n / FSM * a)}
    for name, grp in (('near', NEAR), ('far', FAR)):
        g = list(grp); w = (Ppp[g, j] + Pmm[g, j]); w = w / (w.sum() + 1e-30)
        coh = np.abs(Ppm[g, j]) ** 2 / (Ppp[g, j] * Pmm[g, j] + 1e-30)
        if few:                                  # 1-2 segmenty: koherencja trywialnie ~1 -> brak danych
            coh = np.full(len(g), np.nan)
        cph = np.real(Ppm[g, j]) / (np.abs(Ppm[g, j]) + 1e-30)
        R = PA[g, j] / (PA[g, j] + PS[g, j] + 1e-30)
        out[f'coh_{name}'] = float((w * coh).sum()); out[f'cos_{name}'] = float((w * cph).sum())
        out[f'R_{name}'] = float((w * R).sum())
    # cien w calym pasmie rytmu (bez kotwicy): udzial A w modulacji 0,5-9,5 Hz
    out['R_all'] = float(PA[:, sel].sum() / (PA[:, sel].sum() + PS[:, sel].sum() + 1e-30))
    vec = [out[k] for k in ('coh_near', 'cos_near', 'R_near', 'coh_far', 'cos_far', 'R_far', 'R_all', 'Q', 'alpha')]
    return vec, out


def cvd_full(P, ts):
    """Klasyka na calym sladzie: CVD (FFT po klatkach log-mocy kazdego binu +-6 kHz), szczyt kadencji i jego sila;
    rozrzut Dopplera (odch. std. wokol ciala, entropia, szerokosc -20 dB; mediany po klatkach)."""
    L, _ = uniform(P, ts); n = len(L)
    m = np.abs(CEN) <= 6000
    if n < 16:
        return [np.nan] * 5
    nper = min(NPER, n)
    f, C = welch(np.apply_along_axis(_detr, 0, L[:, m]).T, FSM, nperseg=nper)
    sel = (f >= ALPHA[0]) & (f <= ALPHA[1]); C = C / (median_filter(C, size=(1, 9), mode='nearest') + 1e-30)
    c = C[:, sel].sum(0)
    cad = float(f[sel][np.argmax(c)]); strength = float(np.log(c.max() / (np.median(c) + 1e-30)))
    Pl = np.exp(L[:, m]); c0 = CEN[m]; p = Pl / Pl.sum(1, keepdims=True)
    sd = np.sqrt((p * c0 ** 2).sum(1)); ent = -(p * np.log(p + 1e-30)).sum(1) / np.log(m.sum())
    bw = (Pl > 0.01 * Pl.max(1, keepdims=True)).sum(1) * 100.0
    return [cad, strength, float(np.log(np.median(sd) + 1)), float(np.median(ent)), float(np.log(np.median(bw) + 1))]


def extract(part):
    d = os.path.join(DATA, f'full_{part}'); rows = []
    for fn in sorted(os.listdir(d)):
        z = np.load(os.path.join(d, fn)); P, ts = z['P'], z['ts'].astype(float)
        vec, info = mirror_feats(P, ts)
        if vec is None:
            vec = [np.nan] * 9
        rows.append({'track': fn[:-4], 'cls': str(z['cls']), 'bw': float(z['bw']), 'M': vec, 'C': cvd_full(P, ts),
                     'info': info})
    return rows


if __name__ == '__main__':
    import sys
    part = sys.argv[1]
    json.dump(extract(part), open(os.path.join(DATA, f'feat_mirror_v0_3_{part}.json'), 'w'))
