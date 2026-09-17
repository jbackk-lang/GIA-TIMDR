# tests/test_zero_mode_topology_bridge.py
"""
Testy syntetyczne dla core/zero_mode_topology_bridge.py (most M/S<->G
#1) -- punkt 3 planu uzytkownika (2026-09-17): sygnaly z/bez trybu
zerowego, sygnaly z wysokim/niskim G_i, sprawdzenie ze MC_{M/S<->G}
reaguje zgodnie z definicja. Uzywa istniejacego pipeline'u
anty-numerologicznego (run_controls, Mann-Whitney + rozmiar efektu) tam,
gdzie to naturalne (G_i), i bezposrednich asercji tam, gdzie kierunek
efektu jest jednoznaczny z definicji wzoru (Z0, MC binarny/ciagly).
Zero realnych danych, zero pre-rejestrowanych progow theta0/thetaG (to
przychodzi w PREREG_MOBIUS_COHERENCE_BRIDGES.md, OSOBNO, przed realnymi
danymi) -- tu sprawdzamy WYLACZNIE "czy operator robi to, co mowi".
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TIMDR-Math-Formalism"))

from timdr_formalism.pipeline import run_controls, effect_size_label  # noqa: E402

from core.zero_mode_topology_bridge import (  # noqa: E402
    zero_mode_fraction,
    calibrate_gi_ranges,
    g_i,
    mc_ms_g_continuous,
    mc_ms_g_binary,
)
from core.trefoil_ms_bridge import (  # noqa: E402
    make_positive_injector as make_winding_rich_signal,
    make_negative_a as make_white_noise,
)

SEED = 0
N_WINDOWS = 30
WINDOW_SIZE = 300  # rezim "gesty" juz zwalidowany w winding/crossing/phase_winding (punkt 19 skilla)
ALPHA = 0.05


# ---------------------------------------------------------------------
# Z0 -- sygnaly z trybem zerowym (DC) vs bez (srednia zero)
# ---------------------------------------------------------------------


def make_dc_signal(window_size: int, seed) -> np.ndarray:
    """Pozytywna: silny tryb zerowy (offset stalej >> szum)."""
    rng = np.random.default_rng(seed)
    return 5.0 + rng.normal(0.0, 1.0, window_size)


def make_zero_mean_noise_a(window_size: int, seed) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, 1.0, window_size)


def make_zero_mean_noise_b(window_size: int, seed) -> np.ndarray:
    # inna skala (sigma=0.4) -- Z0 jest niezmiennicze wzgledem skali
    # (mu i Eac skaluja sie tak samo), wiec oczekujemy braku roznicy
    # wzgledem noise_a mimo innej amplitudy
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, 0.4, window_size)


def test_z0_separates_dc_from_zero_mean():
    result = run_controls(
        metric_fn=zero_mode_fraction,
        positive_injector=make_dc_signal,
        negative_generator_a=make_zero_mean_noise_a,
        negative_generator_b=make_zero_mean_noise_b,
        n_windows=N_WINDOWS,
        window_size=WINDOW_SIZE,
        seed=SEED,
        alpha=ALPHA,
    )
    assert result.passed, result.reason
    assert result.positive.median_test > result.positive.median_background


def test_z0_is_scale_invariant():
    rng = np.random.default_rng(42)
    x = rng.normal(0.0, 1.0, 300) + 2.0
    z0_a = zero_mode_fraction(x)
    z0_b = zero_mode_fraction(3.0 * x)  # przeskalowany sygnal (mu i Eac skaluja sie x^2/x^2)
    assert z0_a == pytest.approx(z0_b, rel=1e-9)


def test_z0_small_for_pure_zero_mean_noise():
    rng = np.random.default_rng(7)
    x = rng.normal(0.0, 1.0, 500)
    assert zero_mode_fraction(x) < 1.0  # rzadu 1/N, znacznie ponizej typowej wartosci DC ~25


def test_z0_large_for_strong_dc():
    rng = np.random.default_rng(7)
    x = 10.0 + rng.normal(0.0, 1.0, 500)
    assert zero_mode_fraction(x) > 50.0


def test_z0_empty_signal_returns_zero():
    assert zero_mode_fraction(np.array([])) == 0.0


# ---------------------------------------------------------------------
# G_i -- sygnaly z wysokim/niskim skretem geometrycznym (winding/crossing/phase)
# ---------------------------------------------------------------------

# Kalibracja zakresow G_i z MIESZANEGO tla (kontrola pozytywna + negatywna
# generowane tym samym mechanizmem co ponizszy test run_controls, ale
# OSOBNYM zestawem seedow 1000+ -- nie tymi samymi oknami, na ktorych
# G_i jest pozniej raportowane w tescie).
_CALIB_SEEDS = range(1000, 1040)
_CALIB_SIGNALS = (
    [make_winding_rich_signal(0.1)(WINDOW_SIZE, s) for s in _CALIB_SEEDS]
    + [make_white_noise(1.0)(WINDOW_SIZE, s) for s in _CALIB_SEEDS]
)
_GI_RANGES = calibrate_gi_ranges(_CALIB_SIGNALS)


def _gi_metric(signal_1d: np.ndarray) -> float:
    return g_i(signal_1d, _GI_RANGES)


def test_gi_does_not_cleanly_separate_periodic_from_white_noise_synthetic():
    """UCZCIWY WYNIK NEGATYWNY, oczekiwany a priori: G_i dziedziczy z
    winding_number/crossing_number/phase_winding dokladnie ten sam,
    juz udokumentowany efekt co w punkcie 19 skilla / RESULT_TOPOLOGICAL_
    BRIDGE_MS_SCOPE.md -- na TEJ konstrukcji syntetycznej (dwie
    niewspolmierne czestotliwosci + szum vs czysty szum bialy) embedding
    opozniajacy sprawia, ze SZUM ma WIEKSZA lokalna/globalna zlozonosc
    geometryczna niz sygnal periodyczny (przeciwnie do naiwnej intuicji
    "szum = brak skretu"). Zweryfikowane bezposrednio (patrz komentarz
    kalibracji nizej): srednie W/C/P dla bialego szumu WIEKSZE niz dla
    sygnalu periodycznego przy tych samych oknach.

    Test run_controls tutaj CELOWO nie wymaga result.passed -- zamiast
    tego dokumentuje ten znany brak separacji jako STWIERDZONY FAKT, nie
    ukrywa go. Zgodnie z ustalonym w punkcie 19 wnioskiem: te trzy
    metryki maja tresc empiryczna na REALNYCH danych (lozyska 82%), NIE
    na tej konkretnej, naiwnej konstrukcji syntetycznej -- test_realny
    (core/real_zero_mode_topology_bridge.py) jest wiec WLASCIWYM
    miejscem walidacji G_i, nie ten plik."""
    result = run_controls(
        metric_fn=_gi_metric,
        positive_injector=make_winding_rich_signal(0.1),
        negative_generator_a=make_white_noise(1.0),
        negative_generator_b=make_white_noise(1.0),
        n_windows=N_WINDOWS,
        window_size=WINDOW_SIZE,
        seed=SEED,
        alpha=ALPHA,
    )
    # Uczciwie zaraportowany wynik negatywny -- NIE assert result.passed.
    assert result.passed is False
    assert "za mało czuła" in result.reason or "fałszywy alarm" in result.reason


def test_gi_bounded_in_unit_interval():
    for s in _CALIB_SIGNALS[:10]:
        v = g_i(s, _GI_RANGES)
        assert 0.0 <= v <= 1.0


def test_gi_deterministic_for_same_signal():
    s = _CALIB_SIGNALS[0]
    vals = [g_i(s, _GI_RANGES) for _ in range(5)]
    assert len(set(vals)) == 1


def test_gi_is_mean_of_three_normalized_components():
    from core.zero_mode_topology_bridge import compute_wcp, _minmax01
    s = _CALIB_SIGNALS[3]
    w, c, p = compute_wcp(s)
    expected = (
        _minmax01(w, _GI_RANGES.w_min, _GI_RANGES.w_max)
        + _minmax01(c, _GI_RANGES.c_min, _GI_RANGES.c_max)
        + _minmax01(p, _GI_RANGES.p_min, _GI_RANGES.p_max)
    ) / 3.0
    assert g_i(s, _GI_RANGES) == pytest.approx(expected)


# ---------------------------------------------------------------------
# MC_{M/S<->G} -- operator zlozony, prawda tabelaryczna
# ---------------------------------------------------------------------


def test_mc_continuous_monotonic_in_expected_direction():
    # mniejsze Z0 (blizej 0) i wieksze Gi -> wiekszy MC ciagly
    low = mc_ms_g_continuous(z0=0.9, gi=0.1, w1=0.5, w3=0.5, gref=1.0)
    high = mc_ms_g_continuous(z0=0.05, gi=0.9, w1=0.5, w3=0.5, gref=1.0)
    assert high > low


def test_mc_continuous_matches_closed_form():
    v = mc_ms_g_continuous(z0=0.2, gi=0.6, w1=0.5, w3=0.5, gref=1.0)
    assert v == pytest.approx(0.5 * (1 - 0.2) + 0.5 * (0.6 / 1.0))


def test_mc_binary_truth_table():
    theta0, thetaG = 0.3, 0.5
    # (Z0 maly, Gi duze) -> True -- jedyny kwadrant Mobius-podobny
    assert mc_ms_g_binary(z0=0.1, gi=0.8, theta0=theta0, thetaG=thetaG) is True
    # (Z0 duzy, Gi duze) -> False
    assert mc_ms_g_binary(z0=0.5, gi=0.8, theta0=theta0, thetaG=thetaG) is False
    # (Z0 maly, Gi male) -> False
    assert mc_ms_g_binary(z0=0.1, gi=0.2, theta0=theta0, thetaG=thetaG) is False
    # (Z0 duzy, Gi male) -> False
    assert mc_ms_g_binary(z0=0.5, gi=0.2, theta0=theta0, thetaG=thetaG) is False


def test_mc_binary_boundary_is_strict():
    # graniczne wartosci NIE spelniaja warunku (nierownosci ostre z definicji)
    assert mc_ms_g_binary(z0=0.3, gi=0.5, theta0=0.3, thetaG=0.5) is False
