"""transition_params.py -- parametry przejsc miedzy galeziami TIMDR (2026-09-27).

N_cyk  -- liczba cykli rytmu w oknie (sygnal -> pole): ile "szczelin" ma sito; ostry grzebien wymaga wielu cykli.
L_koh  -- dlugosc koherencji rytmu w cyklach (rura -> zegar): f0 / szerokosc linii; gdy L_koh < N_cyk trzeba
          wyprostowac rure (zmienic zegar na katowy/zdarzeniowy).
D      -- gestosc zdarzen ~ czestosc x czas wygaszania (mierzona wypelnieniem obwiedni) (pole -> rura -> META: rho = f * tau):
          D << 1 czasteczka, D ~ 1 pakiet, D >> 1 fala.
kotwica -- skad znana jest czestotliwosc hipotezy: 'stala' (kinematyka), 'sledzona' (tachometr/rzedy), 'wolna' (argmax).
Wzory i reguly: docs/theory/TIMDR_Parametry_Przejsc.md.
"""
from __future__ import annotations
import numpy as np

REGIME_LO, REGIME_HI = 0.3, 3.0


def n_cycles(window_s: float, f_rhythm: float) -> float:
    return float(window_s * f_rhythm)


def band_envelope(x, fs, lo, hi):
    x = np.asarray(x, float) - np.mean(x); X = np.fft.fft(x); f = np.fft.fftfreq(len(x), 1 / fs)
    Z = np.zeros_like(X); m = (f >= lo) & (f < hi); Z[m] = 2 * X[m]
    return np.abs(np.fft.ifft(Z))


def event_density(env, fs, k=5.0):
    """Gestosc zdarzen D bez progu: wypelnienie obwiedni eta = (E e)^2 / E(e^2) (dla ciagu impulsow o wypelnieniu
    delta: eta ~ delta; dla gasnacych impulsow: eta ~ 2 r tau), D = eta / (1 - eta).
    D << 1: rzadkie blyski (czasteczka); D ~ 1: pakiet; D >> 1: rura wypelniona (fala / szum, szum gaussowski D ~ 3,7).
    Pomocniczo: czestosc zdarzen r (maksima > mediana + k*MAD) i tau (autokorelacja obwiedni < 1/e)."""
    e = np.asarray(env, float)
    eta = float(e.mean() ** 2 / (np.mean(e ** 2) + 1e-30))
    a = e - e.mean()
    ac = np.fft.irfft(np.abs(np.fft.rfft(a, 2 * len(a))) ** 2)[: len(a)]; ac = ac / (ac[0] + 1e-30)
    lag = int(np.argmax(ac < np.exp(-1))) if np.any(ac < np.exp(-1)) else len(a)
    med = np.median(e); mad = 1.4826 * np.median(np.abs(e - med)) + 1e-30
    pk = np.where((e[1:-1] > e[:-2]) & (e[1:-1] >= e[2:]) & (e[1:-1] > med + k * mad))[0] + 1
    ev, last = 0, -np.inf
    for p in pk:
        if p - last >= 3 * max(lag, 1):
            ev += 1; last = p
    return {"D": eta / max(1 - eta, 1e-9), "eta": eta, "rate": float(ev / (len(e) / fs)), "tau": float(max(lag, 1) / fs)}


def coherence_cycles(x, fs, f0, rel_band=0.2):
    """L_koh ~ f0 / FWHM linii przy f0 (widmo z oknem Hanna). Nierozdzielona linia -> dolna granica = N_cyk."""
    x = np.asarray(x, float) - np.mean(x); n = len(x)
    S = np.abs(np.fft.rfft(x * np.hanning(n), 8 * n)) ** 2; f = np.fft.rfftfreq(8 * n, 1 / fs)
    m = np.abs(f - f0) <= rel_band * f0
    if not m.any():
        return float("nan")
    i0 = np.where(m)[0][np.argmax(S[m])]; half = S[i0] / 2
    lo = i0
    while lo > 0 and S[lo] > half:
        lo -= 1
    hi = i0
    while hi < len(S) - 1 and S[hi] > half:
        hi += 1
    fwhm = max(f[hi] - f[lo], 2.0 * fs / n)          # rozdzielczosc okna Hanna ~ 2/T
    return float(f[i0] / fwhm)


def regime(D: float) -> str:
    return "czasteczka" if D < REGIME_LO else ("fala" if D > REGIME_HI else "pakiet")


def feasibility(N_cyk: float, L_koh: float, D: float, anchor: str) -> dict:
    """Regula wykonalnosci: ktora droga i czy sito ma szanse -- liczona PRZED testem."""
    path, ok = [], True
    if N_cyk < 10:
        path.append("za malo cykli w oknie (N_cyk < 10): grzebien rozmyty"); ok = False
    if np.isfinite(L_koh) and L_koh < N_cyk:
        path.append("koherencja krotsza niz okno: wyprostowac rure (zegar katowy/zdarzeniowy)")
    if anchor == "wolna":
        path.append("brak kotwicy: samokorekta bez punktu startu"); ok = False
    reg = regime(D)
    path.append({"czasteczka": "miara czasteczkowosci P (blyski)", "pakiet": "sito z kotwica (grzebien Q)",
                 "fala": "linie galezi K (harmoniczne kotwicy)"}[reg])
    return {"reżim": reg, "droga": path, "sito_ma_szanse": ok}
