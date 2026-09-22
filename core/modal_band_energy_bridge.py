# core/modal_band_energy_bridge.py
"""
modal_band_energy_bridge.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_MODAL_BAND_ENERGY_BRIDGE_v0.1.md) prostego mostu
M/S->K: energia obwiedni Hilberta w pasmach charakterystycznych
lozyska (BPFO/BPFI/BSF), BEZ galezi G -- swiadomy powrot do metody z
ugruntowana literatura diagnostyki lozysk ("envelope spectrum
analysis"), po trzech kolejnych konstrukcjach geometrycznych
(chrono_cone/sphere/modal_geometry -- odrzucone lub niestabilne).

Reuzywa bandpass_fft/hilbert_envelope z chrono_modal_geometry_bridge.py
(ten sam kod, bez zmian) -- tu bez zanurzania w zadna trajektorie,
tylko srednia obwiedni jako pojedyncza liczba na okno na pasmo.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow kontroli
syntetycznych -- wszystkie stale sa przeniesione 1:1 z zamrozonej
pre-rejestracji.
"""
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from core.chrono_modal_geometry_bridge import (  # noqa: E402
    bandpass_fft,
    hilbert_envelope,
    CHAR_FREQS,
    band_edges,
    BAND_NAMES,
    FS_RAW_HZ,
)
from timdr_formalism.pipeline import (  # noqa: E402
    mann_whitney_test,
    effect_size_label,
    TestResult,
)
from timdr_formalism.envelope_demodulation import (  # noqa: E402
    kurtosis_excess as _kurtosis_excess,
    select_resonance_band as _select_resonance_band_generic,
    envelope_spectrum_peak,
)

# ---------------------------------------------------------------------
# SS3.1 PREREG: metryka -- srednia obwiedni Hilberta w pasmie
# ---------------------------------------------------------------------


def band_energy(signal: np.ndarray, fs: float, f_lo: float, f_hi: float) -> float:
    """energy_s = mean(|hilbert(bandpass_fft(signal, fs, f_lo, f_hi))|)."""
    filtered = bandpass_fft(signal, fs, f_lo, f_hi)
    envelope = hilbert_envelope(filtered)
    return float(np.mean(envelope))


def all_band_energies(signal: np.ndarray, fs: float = FS_RAW_HZ) -> Dict[str, float]:
    """energy_BPFO, energy_BPFI, energy_BSF dla jednego okna."""
    out = {}
    for name in BAND_NAMES:
        f_lo, f_hi = band_edges(CHAR_FREQS[name])
        out[name] = band_energy(signal, fs, f_lo, f_hi)
    return out


# ---------------------------------------------------------------------
# SS4 PREREG: generatory syntetyczne (zamrozone PRZED implementacja)
# ---------------------------------------------------------------------

SYN_FS = 1000.0
SYN_F_LO, SYN_F_HI = 90.0, 110.0   # pasmo testowe
SYN_F_OFFBAND = 300.0              # kontrola specyficznosci -- daleko poza pasmem
SYN_NOISE_STD = 1.0
SYN_SIGNAL_AMP = 3.0                # amplituda oscylacji wzgledem szumu


def make_inband_signal(window_size: int, seed: Optional[int]) -> np.ndarray:
    """(a) POZYTYWNA -- bialy szum + oscylacja W PASMIE testowym."""
    rng = np.random.default_rng(seed)
    t = np.arange(window_size, dtype=float)
    noise = rng.normal(0.0, SYN_NOISE_STD, window_size)
    signal = SYN_SIGNAL_AMP * np.sin(2 * np.pi * 100.0 * t / SYN_FS)
    return noise + signal


def make_white_noise_only(window_size: int, seed: Optional[int]) -> np.ndarray:
    """(b) NEGATYWNA -- czysty bialy szum, bez struktury."""
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, SYN_NOISE_STD, window_size)


def make_offband_signal(window_size: int, seed: Optional[int]) -> np.ndarray:
    """(c) SPECYFICZNOSC -- bialy szum + oscylacja POZA pasmem testowym."""
    rng = np.random.default_rng(seed)
    t = np.arange(window_size, dtype=float)
    noise = rng.normal(0.0, SYN_NOISE_STD, window_size)
    signal = SYN_SIGNAL_AMP * np.sin(2 * np.pi * SYN_F_OFFBAND * t / SYN_FS)
    return noise + signal


# ---------------------------------------------------------------------
# Bramka kontrolna (SS4 PREREG)
# ---------------------------------------------------------------------

SYN_WINDOW_SIZES = (500, 1000, 2000)
SYN_N_WINDOWS = 30
SYN_SEED = 0
SYN_ALPHA = 0.05
MIN_VALID_FRAC = 0.5


@dataclass
class BandEnergyControlResult:
    __test__ = False
    positive: Optional[TestResult]
    specificity: Optional[TestResult]
    n_valid_a: int
    n_valid_b: int
    n_valid_c: int
    n_total: int
    passed: bool
    inconclusive: bool
    reason: str


def run_band_energy_controls(
    window_size: int, n_windows: int = SYN_N_WINDOWS, seed: int = SYN_SEED, alpha: float = SYN_ALPHA
) -> BandEnergyControlResult:
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)

    def _energies(gen, seed_offset=0):
        return np.array(
            [
                band_energy(gen(window_size, int(s) + seed_offset), SYN_FS, SYN_F_LO, SYN_F_HI)
                for s in seeds
            ]
        )

    a_vals = _energies(make_inband_signal)
    b_vals = _energies(make_white_noise_only, seed_offset=1)
    c_vals = _energies(make_offband_signal, seed_offset=2)

    a_v, b_v, c_v = (
        a_vals[~np.isnan(a_vals)],
        b_vals[~np.isnan(b_vals)],
        c_vals[~np.isnan(c_vals)],
    )
    n_total = n_windows
    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_total)))

    if len(a_v) < min_needed or len(b_v) < min_needed or len(c_v) < min_needed:
        return BandEnergyControlResult(
            positive=None,
            specificity=None,
            n_valid_a=len(a_v),
            n_valid_b=len(b_v),
            n_valid_c=len(c_v),
            n_total=n_total,
            passed=False,
            inconclusive=True,
            reason=f"Za duzo NaN: a={len(a_v)}, b={len(b_v)}, c={len(c_v)}, prog={min_needed}.",
        )

    positive = mann_whitney_test(a_v, b_v, alternative="two-sided")
    specificity = mann_whitney_test(c_v, b_v, alternative="two-sided")

    pos_ok = positive.pvalue < alpha and positive.median_test > positive.median_background
    spec_ok = specificity.pvalue >= alpha  # brak roznicy = brak przecieku

    passed = pos_ok and spec_ok
    if passed:
        reason = "Kontrola pozytywna wykryla podniesiona energie w pasmie, kontrola specyficznosci nie pokazala przecieku spoza pasma."
    elif not pos_ok and not spec_ok:
        reason = "Kontrola pozytywna NIE wykryla efektu I wystapil przeciek spoza pasma."
    elif not pos_ok:
        reason = "Kontrola pozytywna nie wykryla podniesienia energii w pasmie testowym."
    else:
        reason = "Wystapil przeciek: sygnal spoza pasma podnosi energie w pasmie testowym -- filtr nie izoluje czysto."

    return BandEnergyControlResult(
        positive=positive,
        specificity=specificity,
        n_valid_a=len(a_v),
        n_valid_b=len(b_v),
        n_valid_c=len(c_v),
        n_total=n_total,
        passed=passed,
        inconclusive=False,
        reason=reason,
    )


def run_synthetic_controls() -> List[Dict]:
    rows = []
    for window_size in SYN_WINDOW_SIZES:
        result = run_band_energy_controls(window_size=window_size)
        rows.append({"window_size": window_size, "result": result})
    return rows


def format_synthetic_report(rows: List[Dict]) -> str:
    lines = ["## Kontrole syntetyczne modal_band_energy_bridge v0.1", ""]
    for row in rows:
        w = row["window_size"]
        r: BandEnergyControlResult = row["result"]
        lines.append(f"### window_size={w}")
        if r.inconclusive:
            lines.append(f"INCONCLUSIVE: {r.reason}")
        else:
            p, s = r.positive, r.specificity
            lines.append(
                f"pozytywna (a vs b): p={p.pvalue:.4g} r={p.effect_size_r:.3f} ({effect_size_label(p.effect_size_r)}) "
                f"mediana(a)={p.median_test:.4g} mediana(b)={p.median_background:.4g}"
            )
            lines.append(
                f"specyficznosc (c vs b): p={s.pvalue:.4g} r={s.effect_size_r:.3f} "
                f"mediana(c)={s.median_test:.4g} mediana(b)={s.median_background:.4g}"
            )
            lines.append(f"PASSED={r.passed} -- {r.reason}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------
# v0.2 (PREREG_MODAL_BAND_ENERGY_BRIDGE_v0.2.md) -- pelna demodulacja:
# wybor pasma rezonansu przez kurtoze + widmo obwiedni. v0.1 (powyzej)
# ZAMKNIETY jako blad metodologiczny (RESULT v0.1), kod zachowany bez
# zmian jako udokumentowana historia.
# ---------------------------------------------------------------------

CANDIDATE_RESONANCE_BANDS = [
    (500.0, 1000.0), (1000.0, 1500.0), (1500.0, 2000.0), (2000.0, 2500.0),
    (2500.0, 3000.0), (3000.0, 3500.0), (3500.0, 4000.0), (4000.0, 4500.0),
    (4500.0, 5000.0),
]
ENVELOPE_PEAK_WINDOW_HZ = 2.0  # SS2 PREREG v0.2


# _kurtosis_excess, envelope_spectrum_peak: WYDZIELONE do
# timdr_formalism.envelope_demodulation (2026-09-22), importowane wyzej
# (patrz import blok) -- NIE redefiniowane tutaj.


def select_resonance_band(reference_signal: np.ndarray, fs: float) -> tuple:
    """SS1 PREREG v0.2: cienki wrapper nad generyczna
    `timdr_formalism.envelope_demodulation.select_resonance_band`,
    zamrazajacy `CANDIDATE_RESONANCE_BANDS` (specyficzne dla lozysk
    CWRU, 500-5000Hz) jako liste kandydatow tego mostu."""
    return _select_resonance_band_generic(reference_signal, fs, CANDIDATE_RESONANCE_BANDS)


# ---------------------------------------------------------------------
# v0.2 kontrole syntetyczne (SS3 PREREG v0.2)
# ---------------------------------------------------------------------

SYN_V2_FS = 5000.0
SYN_V2_F_TARGET = 100.0
SYN_V2_F_RES = 1200.0
SYN_V2_TAU = 0.001
SYN_V2_NOISE_STD = 1.0
SYN_V2_IMPULSE_AMP = 5.0


def _impulse_train(window_size: int, fs: float, f_target: float, f_res: float, tau: float, amp: float) -> np.ndarray:
    t = np.arange(window_size) / fs
    period_samples = fs / f_target
    signal = np.zeros(window_size)
    n_impulses = int(window_size / period_samples) + 2
    for k in range(n_impulses):
        t0 = k * period_samples / fs
        local_t = t - t0
        mask = local_t >= 0
        signal[mask] += amp * np.exp(-local_t[mask] / tau) * np.sin(2 * np.pi * f_res * local_t[mask])
    return signal


def make_impulse_train_signal(window_size: int, seed: Optional[int]) -> np.ndarray:
    """(a) POZYTYWNA v0.2 -- powtarzajace sie tlumione impulsy przy
    f_target w okresie T=1/f_target, na tle szumu (SS3 PREREG v0.2)."""
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, SYN_V2_NOISE_STD, window_size)
    impulses = _impulse_train(window_size, SYN_V2_FS, SYN_V2_F_TARGET, SYN_V2_F_RES, SYN_V2_TAU, SYN_V2_IMPULSE_AMP)
    return noise + impulses


def make_broadband_noise_v2(window_size: int, seed: Optional[int]) -> np.ndarray:
    """(b) NEGATYWNA v0.2 -- czysty szerokopasmowy szum, bez
    periodycznosci ani rezonansu."""
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, SYN_V2_NOISE_STD, window_size)


@dataclass
class DemodControlResult:
    __test__ = False
    test: Optional[TestResult]
    resonance_band: tuple
    n_valid_a: int
    n_valid_b: int
    n_total: int
    passed: bool
    inconclusive: bool
    reason: str


def run_demod_controls(
    window_size: int, n_windows: int = SYN_N_WINDOWS, seed: int = SYN_SEED, alpha: float = SYN_ALPHA
) -> DemodControlResult:
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)

    # Pasmo rezonansu w syntetyce: wybrane z JEDNEGO reprezentatywnego
    # sygnalu pozytywnego (w realnym pipeline z Normal -- tu nie ma
    # oddzielnego "zdrowego" sygnalu, wiec uzywamy pierwszego seeda
    # kontroli pozytywnej jako referencji, odnotowane jako roznica wobec
    # SS1 PREREG v0.2).
    reference = make_impulse_train_signal(window_size, int(seeds[0]))
    # kandydaci syntetyczni dopasowani do SYN_V2_FS zakresu (skalowane
    # analogicznie do CANDIDATE_RESONANCE_BANDS, ale w zakresie < Nyquista=2500Hz)
    candidate_bands_syn = [(f_lo * SYN_V2_FS / FS_RAW_HZ, f_hi * SYN_V2_FS / FS_RAW_HZ) for f_lo, f_hi in CANDIDATE_RESONANCE_BANDS]
    best_band, best_kurt = None, -np.inf
    for f_lo, f_hi in candidate_bands_syn:
        if f_hi >= SYN_V2_FS / 2:
            continue
        filtered = bandpass_fft(reference, SYN_V2_FS, f_lo, f_hi)
        k = _kurtosis_excess(filtered)
        if k > best_kurt:
            best_kurt = k
            best_band = (f_lo, f_hi)

    target_freqs = {"f_target": SYN_V2_F_TARGET}

    def _peaks(gen, seed_offset=0):
        vals = []
        for s in seeds:
            sig = gen(window_size, int(s) + seed_offset)
            p = envelope_spectrum_peak(sig, SYN_V2_FS, best_band, target_freqs)
            vals.append(p["f_target"])
        return np.array(vals)

    a_vals = _peaks(make_impulse_train_signal)
    b_vals = _peaks(make_broadband_noise_v2, seed_offset=1)

    a_v = a_vals[~np.isnan(a_vals)]
    b_v = b_vals[~np.isnan(b_vals)]
    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_windows)))

    if len(a_v) < min_needed or len(b_v) < min_needed:
        return DemodControlResult(
            test=None, resonance_band=best_band, n_valid_a=len(a_v), n_valid_b=len(b_v),
            n_total=n_windows, passed=False, inconclusive=True,
            reason=f"Za duzo NaN: a={len(a_v)}, b={len(b_v)}, prog={min_needed}.",
        )

    t = mann_whitney_test(a_v, b_v, alternative="two-sided")
    passed = t.pvalue < alpha and abs(t.effect_size_r) >= 0.3 and t.median_test > t.median_background

    if passed:
        reason = "Impulsy periodyczne przy f_target dajq istotnie wyzszy pik w widmie obwiedni niz szum -- demodulacja dziala."
    else:
        reason = "Brak wykrywalnego piku w widmie obwiedni dla sygnalu impulsowego -- mechanizm demodulacji nie dziala jak przewidziano."

    return DemodControlResult(
        test=t, resonance_band=best_band, n_valid_a=len(a_v), n_valid_b=len(b_v),
        n_total=n_windows, passed=passed, inconclusive=False, reason=reason,
    )


def run_synthetic_controls_v2() -> List[Dict]:
    rows = []
    for window_size in SYN_WINDOW_SIZES_V2:
        result = run_demod_controls(window_size=window_size)
        rows.append({"window_size": window_size, "result": result})
    return rows


SYN_WINDOW_SIZES_V2 = (2500, 5000, 10000)


def format_synthetic_report_v2(rows: List[Dict]) -> str:
    lines = ["## Kontrole syntetyczne modal_band_energy_bridge v0.2 (pelna demodulacja)", ""]
    for row in rows:
        w = row["window_size"]
        r: DemodControlResult = row["result"]
        lines.append(f"### window_size={w}")
        lines.append(f"pasmo rezonansu wybrane: {r.resonance_band}")
        if r.inconclusive:
            lines.append(f"INCONCLUSIVE: {r.reason}")
        else:
            t = r.test
            lines.append(
                f"n_valid: a={r.n_valid_a}/{r.n_total}, b={r.n_valid_b}/{r.n_total}"
            )
            lines.append(
                f"pik widma obwiedni przy f_target (a vs b): p={t.pvalue:.4g} r={t.effect_size_r:.3f} "
                f"({effect_size_label(t.effect_size_r)}) mediana(a)={t.median_test:.4g} mediana(b)={t.median_background:.4g}"
            )
            lines.append(f"PASSED={r.passed} -- {r.reason}")
        lines.append("")
    return "\n".join(lines)


__all__ = [
    "band_energy",
    "all_band_energies",
    "make_inband_signal",
    "make_white_noise_only",
    "make_offband_signal",
    "run_band_energy_controls",
    "run_synthetic_controls",
    "format_synthetic_report",
    "select_resonance_band",
    "envelope_spectrum_peak",
    "CANDIDATE_RESONANCE_BANDS",
    "ENVELOPE_PEAK_WINDOW_HZ",
    "run_demod_controls",
    "run_synthetic_controls_v2",
    "format_synthetic_report_v2",
]


if __name__ == "__main__":
    t0 = time.time()
    rows = run_synthetic_controls()
    print(format_synthetic_report(rows))
    print(f"Czas: {time.time()-t0:.2f}s")
