# timdr_formalism/envelope_demodulation.py
"""
envelope_demodulation.py -- domenowo-agnostyczny rdzen przetwarzania
sygnalu gałęzi M/S czytany przez most M/S->K: filtr pasmowy FFT-domenowy,
obwiednia Hilberta, wybor pasma rezonansu przez kurtoze, widmo
obwiedni z wyszukiwaniem piku przy zadanej czestotliwosci.

Wydzielone 1:1 (bez zmiany logiki, tylko usuniecie stalych
specyficznych dla lozysk CWRU -- te zostaja jako parametry wywolania)
z GIA-TIMDR (core/chrono_modal_geometry_bridge.py,
core/modal_band_energy_bridge.py v0.2), gdzie powstalo w ramach
PREREG_MODAL_BAND_ENERGY_BRIDGE_v0.2.md -- patrz tamtejsze
PREREG/RESULT po kontekst historyczny (diagnostyka lozysk CWRU, wynik
POTWIERDZONY na trzech typach uszkodzenia, IR/OR z wyrazna
specyficznoscia pasmowa, B bez niej -- zgodnie z literatura).

Standardowa "envelope spectrum analysis" z diagnostyki maszyn
wirujacych: sygnal -> filtr wokol pasma rezonansu (wybranego przez
maksimum kurtozy na sygnale referencyjnym/zdrowym) -> obwiednia
Hilberta -> widmo (FFT) tej obwiedni -> wysokosc piku przy
czestotliwosci diagnostycznej. Uzyteczne wszedzie tam, gdzie
periodyczne uderzenia/impulsy (defekt lozyska, zabu zebatego, itp.)
wzbudzaja rezonans strukturalny wyzszej czestotliwosci niz sama
czestotliwosc defektu.
"""
from __future__ import annotations

from typing import Dict, Sequence, Tuple

import numpy as np


def _finite_1d(values: np.ndarray, name: str) -> np.ndarray:
    """Convert to a finite, non-empty one-dimensional float array."""
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size == 0:
        raise ValueError(f"{name} musi byc niepustym wektorem 1D")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} musi zawierac wylacznie skonczone wartosci")
    return arr


def _validate_band(fs: float, f_lo: float, f_hi: float) -> tuple[float, float, float]:
    fs, f_lo, f_hi = float(fs), float(f_lo), float(f_hi)
    if not np.all(np.isfinite([fs, f_lo, f_hi])):
        raise ValueError("fs i granice pasma musza byc skonczone")
    if fs <= 0:
        raise ValueError("fs musi byc > 0")
    if f_lo < 0 or f_hi <= f_lo or f_hi > fs / 2:
        raise ValueError("wymagane 0 <= f_lo < f_hi <= czestotliwosc Nyquista")
    return fs, f_lo, f_hi


# ---------------------------------------------------------------------
# Filtr pasmowy FFT-domenowy + obwiednia Hilberta
# ---------------------------------------------------------------------


def bandpass_fft(signal: np.ndarray, fs: float, f_lo: float, f_hi: float) -> np.ndarray:
    """Maskowanie w dziedzinie czestotliwosci (zera poza pasmem),
    odwrotna FFT -- unika wyboru rzedu filtru IIR/FIR."""
    x = _finite_1d(signal, "signal")
    fs, f_lo, f_hi = _validate_band(fs, f_lo, f_hi)
    n = len(x)
    spectrum = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    mask = (freqs >= f_lo) & (freqs <= f_hi)
    spectrum_masked = spectrum * mask
    return np.fft.irfft(spectrum_masked, n=n)


def hilbert_envelope(signal: np.ndarray) -> np.ndarray:
    """|sygnal analityczny| przez FFT (rownowazne scipy.signal.hilbert,
    bez zaleznosci od scipy.signal dla tej jednej operacji)."""
    x = _finite_1d(signal, "signal")
    n = len(x)
    spectrum = np.fft.fft(x)
    h = np.zeros(n)
    if n % 2 == 0:
        h[0] = h[n // 2] = 1
        h[1 : n // 2] = 2
    else:
        h[0] = 1
        h[1 : (n + 1) // 2] = 2
    analytic = np.fft.ifft(spectrum * h)
    return np.abs(analytic)


def decimate_simple(signal: np.ndarray, factor: int) -> np.ndarray:
    """Decymacja z filtrem antyaliasingowym (usrednianie w oknie
    `factor`, potem co-`factor`-ta probka) -- wystarczajace gdy sygnal
    wejsciowy jest juz gladki (np. obwiednia)."""
    x = _finite_1d(signal, "signal")
    if isinstance(factor, bool) or not isinstance(factor, (int, np.integer)) or factor < 1:
        raise ValueError("factor musi byc dodatnia liczba calkowita")
    if factor > x.size:
        raise ValueError("factor nie moze przekraczac dlugosci sygnalu")
    n_out = len(x) // factor
    trimmed = x[: n_out * factor]
    return trimmed.reshape(n_out, factor).mean(axis=1)


# ---------------------------------------------------------------------
# Kurtoza i wybor pasma rezonansu
# ---------------------------------------------------------------------


def kurtosis_excess(signal: np.ndarray) -> float:
    """Kurtoza nadmiarowa (Fisher, 0=Gauss) bez zaleznosci od
    scipy.stats.kurtosis -- prosta implementacja numpy."""
    values = _finite_1d(signal, "signal")
    x = values - np.mean(values)
    m2 = np.mean(x ** 2)
    if m2 < 1e-18:
        return 0.0
    m4 = np.mean(x ** 4)
    return float(m4 / (m2 ** 2) - 3.0)


def select_resonance_band(
    reference_signal: np.ndarray, fs: float, candidate_bands: Sequence[Tuple[float, float]]
) -> Tuple[Tuple[float, float], float]:
    """Pasmo z maksymalna kurtoza sposrod `candidate_bands`, wybrane
    z sygnalu referencyjnego (np. stan zdrowy/baseline) PRZED
    jakimkolwiek porownaniem miedzy grupami -- rezonans strukturalny
    jest wlasciwoscia czujnika/obudowy, nie samego uszkodzenia, wiec
    wybor z sygnalu referencyjnego nie jest podgladaniem roznicy
    miedzy grupami. Zwraca (pasmo, kurtoza_nadmiarowa_najlepszego)."""
    _finite_1d(reference_signal, "reference_signal")
    if not candidate_bands:
        raise ValueError("candidate_bands nie moze byc puste")
    best_band = None
    best_kurt = -np.inf
    for f_lo, f_hi in candidate_bands:
        filtered = bandpass_fft(reference_signal, fs, f_lo, f_hi)
        k = kurtosis_excess(filtered)
        if k > best_kurt:
            best_kurt = k
            best_band = (f_lo, f_hi)
    return best_band, best_kurt


# ---------------------------------------------------------------------
# Widmo obwiedni i wyszukiwanie piku
# ---------------------------------------------------------------------


def envelope_spectrum(signal: np.ndarray, fs: float, resonance_band: Tuple[float, float]) -> Tuple[np.ndarray, np.ndarray]:
    """Filtr wokol pasma rezonansu -> obwiednia -> widmo amplitudowe
    obwiedni (po usunieciu skladowej DC). Zwraca (freqs, spectrum)."""
    x = _finite_1d(signal, "signal")
    f_lo, f_hi = resonance_band
    x_res = bandpass_fft(x, fs, f_lo, f_hi)
    envelope = hilbert_envelope(x_res)
    envelope_centered = envelope - np.mean(envelope)
    n = len(envelope_centered)
    spectrum = np.abs(np.fft.rfft(envelope_centered)) / n
    # Jednostronne widmo amplitudowe: biny wewnetrzne reprezentuja
    # pary +/-f i wymagaja podwojenia; DC oraz Nyquist (dla parzystego n)
    # nie maja partnera i pozostaja bez skalowania.
    if n % 2 == 0:
        spectrum[1:-1] *= 2.0
    else:
        spectrum[1:] *= 2.0
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    return freqs, spectrum


def envelope_spectrum_peak(
    signal: np.ndarray,
    fs: float,
    resonance_band: Tuple[float, float],
    target_freqs: Dict[str, float],
    window_hz: float = 2.0,
) -> Dict[str, float]:
    """Wysokosc piku widma obwiedni w oknie +-window_hz wokol kazdej z
    `target_freqs`. `window_hz` domyslnie 2.0 Hz -- rozsadne dla okien
    rzedu 1s (rozdzielczosc FFT=1Hz) i czestotliwosci diagnostycznych
    niecalkowitych; dostosuj dla innych dlugosci okna/zastosowan."""
    if not np.isfinite(window_hz) or window_hz < 0:
        raise ValueError("window_hz musi byc skonczone i >= 0")
    for name, target in target_freqs.items():
        if not np.isfinite(target) or target < 0:
            raise ValueError(f"target_freqs[{name!r}] musi byc skonczona i >= 0")
    freqs, spectrum = envelope_spectrum(signal, fs, resonance_band)
    out = {}
    for name, target in target_freqs.items():
        mask = (freqs >= target - window_hz) & (freqs <= target + window_hz)
        out[name] = float(np.max(spectrum[mask])) if np.any(mask) else float("nan")
    return out


__all__ = [
    "bandpass_fft",
    "hilbert_envelope",
    "decimate_simple",
    "kurtosis_excess",
    "select_resonance_band",
    "envelope_spectrum",
    "envelope_spectrum_peak",
]
