"""Cechy dla radaru Open Radar: sito rezonansowe w czasie wolnym (TIMDR) + klasyczne odniesienia.

Kazda klatka to zespolone widmo Dopplera (1008 binow, 0 Hz w srodku). Odwrotna FFT daje
sygnal I/Q w czasie wolnym (1008 impulsow, ok. 30 ms, z oknem) -- to jest gotowa rura
analityczna z = I + iQ.

TIMDR (drogowskazy):
  pole       = czas wolny x pasmo Dopplera (pasma nosne po 2 kHz),
  rezonans   = widmo obwiedni kazdego pasma (blyski lopat -> okresowe impulsy),
  sito       = oczka z mapy rezonansu Rz[pasmo, alfa] (mediana = 1),
  samokorekta= czestosc blyskow alfa* nieznana -> model sam ja wybiera (szuka 1x+2x).
Odniesienia: cepstrum JEM (grzebien linii w widmie Dopplera), rozrzut Dopplera,
diagram predkosci kadencji (CVD), kinematyka trackera (kontrola akwizycji).
"""
import numpy as np

C = 3e8
BAND_HZ = 2000.0
ALPHA = (100.0, 2500.0)
NFFT_ENV = 4096


def slow_time(spec):
    """(F,N) zespolone widma -> (F,N) sygnal w czasie wolnym + profil okna."""
    z = np.fft.ifft(np.fft.ifftshift(spec, axes=1), axis=1)
    return z


def central(win_prof, lo=0.5):
    """Indeksy czasu wolnego, gdzie okno > lo * max."""
    return np.where(win_prof > lo * win_prof.max())[0]


def band_edges(prf, n):
    fmax = prf / 2
    nb = int(2 * fmax // BAND_HZ)
    e = -fmax + BAND_HZ * np.arange(nb + 1)
    return e


def resonance_frames(spec, prf, win_prof):
    """Mapa rezonansu Rz[klatka, pasmo, alfa] i os alfa."""
    F, N = spec.shape
    f = (np.arange(N) - N // 2) * prf / N
    ce = central(win_prof)
    w = win_prof[ce]
    edges = band_edges(prf, N)
    fa = np.fft.rfftfreq(NFFT_ENV, 1 / prf)
    sel = (fa >= ALPHA[0]) & (fa <= ALPHA[1])
    out = []
    for b in range(len(edges) - 1):
        m = (f >= edges[b]) & (f < edges[b + 1])
        sb = np.where(m[None, :], spec, 0)
        zb = np.fft.ifft(np.fft.ifftshift(sb, axes=1), axis=1)[:, ce] / w  # kompensacja okna
        env = np.abs(zb)
        env = env - env.mean(1, keepdims=True)
        E = np.abs(np.fft.rfft(env * np.hanning(len(ce)), NFFT_ENV, axis=1)) ** 2
        E = E[:, sel]
        out.append(E / (np.median(E, 1, keepdims=True) + 1e-30))
    return np.stack(out, 1), fa[sel]


def sieve_frame_feats(Rz, fa):
    """Samokorygujace sito: alfa* = argmax sumy oczek (1x + 2x); Q, entropia oczek, alfa*."""
    F, B, A = Rz.shape
    ex = np.maximum(Rz - 1, 0)
    score = ex.sum(1)                                   # (F, A) suma po pasmach
    # harmoniczna 2x: indeks najblizszy 2*alfa
    j2 = np.searchsorted(fa, 2 * fa)
    ok = j2 < A
    s2 = np.zeros_like(score)
    s2[:, ok] = score[:, j2[ok]]
    tot = score + s2
    j = np.argmax(tot, 1)
    Q = np.log1p(tot[np.arange(F), j])
    wts = ex[np.arange(F), :, j]                        # oczka (F, B)
    p = wts / (wts.sum(1, keepdims=True) + 1e-12)
    ent = -(p * np.log(p + 1e-12)).sum(1) / np.log(B)
    return Q, ent, fa[j]


def jem_cepstrum(spec, prf):
    """Klasyczny detektor grzebienia JEM: max cepstrum w zakresie odstepow 100-2500 Hz."""
    F, N = spec.shape
    lp = np.log(np.abs(spec) ** 2 + 1e-12)
    cep = np.abs(np.fft.irfft(lp - lp.mean(1, keepdims=True), axis=1))[:, : N // 2]
    df = prf / N
    q = np.arange(N // 2)                       # quefrency w probkach widma; odstep = N/q binow
    spacing = np.where(q > 0, N / np.maximum(q, 1) * df, np.inf)
    rng = (spacing >= ALPHA[0]) & (spacing <= ALPHA[1])
    base = np.median(cep[:, rng], 1)
    return np.log(cep[:, rng].max(1) / (base + 1e-12))


def doppler_stats(spec, prf):
    """Rozrzut Dopplera wokol piku (bez binu zerowego +-2), entropia widmowa, szerokosc -20 dB."""
    F, N = spec.shape
    P = np.abs(spec) ** 2
    f = (np.arange(N) - N // 2) * prf / N
    P = P.copy(); P[:, N // 2 - 2: N // 2 + 3] = np.median(P, 1, keepdims=True)
    p = P / P.sum(1, keepdims=True)
    mu = (p * f).sum(1)
    sd = np.sqrt((p * (f - mu[:, None]) ** 2).sum(1))
    ent = -(p * np.log(p + 1e-30)).sum(1) / np.log(N)
    bw20 = (P > P.max(1, keepdims=True) * 0.01).sum(1) * prf / N
    return np.log(sd + 1), ent, np.log(bw20 + 1)


def cvd_feats(spec, chunk_starts, frames, chunk=10):
    """Diagram predkosci kadencji na kawalkach 10 klatek (0,5 s): udzial mocy kadencji > 0."""
    vals = []
    P = np.abs(spec) ** 2
    pos = 0
    for s in chunk_starts:
        n = min(chunk, len(frames) - pos)
        if n < chunk:
            break
        blk = np.log(P[pos:pos + chunk] + 1e-12)
        pos += chunk
        C_ = np.abs(np.fft.rfft(blk - blk.mean(0), axis=0)) ** 2   # (6, N)
        tot = C_.sum()
        vals.append(C_[1:].sum() / (tot + 1e-30) if tot > 0 else np.nan)
    return np.array(vals)


# ---------------- v0.1: pole = klatki (20 Hz) x pasma Dopplera wzgledem ciala ----------------
# Rozwoj: sito w czasie wolnym (wyzej) odpadlo -- okno 30 ms (efektywnie ok. 12 ms) daje rozdzielczosc
# ok. 80 Hz, alfa* przyklejalo sie do dolnej granicy 100 Hz (artefakt okna), a Q bylo odwrotne.
# Rytm ruchu (konczyny, pedaly, blyski wirnika zaliasowane do 20 Hz) zyje w skali klatek.

OFF_BAND = 500.0
OFF_MAX = 6000.0
CAD = (0.5, 9.5)
NFFT_CAD = 128
FRAME_HZ = 20.0


def body_align(spec, prf):
    """Przesuwa kazda klatke tak, by pik ciala (bez binu zerowego +-2) byl w srodku. Zwraca moc i os Hz."""
    F, N = spec.shape
    P = np.abs(spec) ** 2
    Pm = P.copy(); Pm[:, N // 2 - 2: N // 2 + 3] = 0
    k = np.argmax(Pm, 1)
    if F >= 5:
        from scipy.signal import medfilt
        k = medfilt(k.astype(float), 5).astype(int)
    A = np.stack([np.roll(P[i], N // 2 - k[i]) for i in range(F)])
    f = (np.arange(N) - N // 2) * prf / N
    return A, f


def band_field(A, f):
    """Pole e[t, b]: log energii w pasmach 500 Hz wzgledem ciala (-6..+6 kHz)."""
    edges = np.arange(-OFF_MAX, OFF_MAX + 1, OFF_BAND)
    cols = [A[:, (f >= edges[b]) & (f < edges[b + 1])].sum(1) for b in range(len(edges) - 1)]
    E = np.stack(cols, 1)
    return np.log(E + 1e-12), 0.5 * (edges[:-1] + edges[1:])


def cadence_spectrum(x):
    """Widmo rytmu po czasie (kolumny = sygnaly), usuniety trend liniowy, okno Hanna."""
    n = x.shape[0]
    t = np.arange(n)
    X = x - np.polyval(np.polyfit(t, x, 1), t[:, None]) if x.ndim == 1 else x - (np.outer(t - t.mean(), ((t - t.mean())[:, None] * (x - x.mean(0))).sum(0) / ((t - t.mean()) ** 2).sum()) + x.mean(0))
    S = np.abs(np.fft.rfft(X * np.hanning(n)[:, None], NFFT_CAD, axis=0)) ** 2
    fa = np.fft.rfftfreq(NFFT_CAD, 1 / FRAME_HZ)
    sel = (fa >= CAD[0]) & (fa <= CAD[1])
    return S[sel], fa[sel]


def chunk_sieve(A, f):
    """TIMDR: mapa rezonansu Rz[alfa, pasmo] (mediana=1), samokorygujace oczka, alfa*."""
    el, off = band_field(A, f)
    S, fa = cadence_spectrum(el)
    Rz = S / (np.median(S, 0, keepdims=True) + 1e-30)
    ex = np.maximum(Rz - 1, 0)
    score = ex.sum(1)
    j2 = np.searchsorted(fa, 2 * fa); ok = j2 < len(fa)
    tot = score.copy(); tot[ok] += score[j2[ok]]
    j = int(np.argmax(tot))
    w = ex[j]
    p = w / (w.sum() + 1e-12)
    ent = float(-(p * np.log(p + 1e-12)).sum() / np.log(len(p)))
    return {'Q': float(np.log1p(tot[j])), 'mesh': 1 - ent, 'alpha': float(fa[j]),
            'mesh_off': float((p * np.abs(off)).sum() / 1000.0)}


def chunk_character(A, f):
    """Krok 0 na polu: L = udzial mocy w pasmie ciala (+-250 Hz), P = udzial energii pozacialowej
    w 5% najsilniejszych klatek (blyski = czasteczkowy), M = mediana po pasmach max Rz."""
    body = np.abs(f) < 250
    Lf = float(A[:, body].sum() / A.sum())
    offp = A[:, np.abs(f) >= OFF_BAND].sum(1)
    k = max(1, int(round(0.05 * len(offp))))
    Pf = float(np.sort(offp)[-k:].sum() / (offp.sum() + 1e-30))
    el, _ = band_field(A, f)
    S, _ = cadence_spectrum(el)
    Mf = float(np.median((S / (np.median(S, 0, keepdims=True) + 1e-30)).max(0)))
    return {'L': Lf, 'P': Pf, 'M': Mf}


def chunk_cvd(A):
    """Klasyczny CVD: log-moc (wyrownana do ciala) -> FFT po czasie w kazdym binie -> profil kadencji."""
    S, fa = cadence_spectrum(np.log(A + 1e-12))
    prof = S.sum(1)
    j = int(np.argmax(prof))
    return {'cvd_peak': float(np.log(prof[j] / (np.median(prof) + 1e-30))), 'cvd_alpha': float(fa[j])}


def window_profile(dev_tracks):
    acc = None
    for _, t in dev_tracks:
        a = np.abs(slow_time(t['spec'])).mean(0)
        acc = a if acc is None else acc + a
    return acc / acc.max()
