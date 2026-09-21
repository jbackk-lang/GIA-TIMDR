# core/chrono_cone_bridge.py
"""
chrono_cone_bridge.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_CHRONO_CONE_MS_BRIDGE_v0.1.md) konstrukcji
"chrono_cone_ratio": szosty kandydat w rodzinie mostow M/S<->topologia/G
(po torsji, winding/crossing, homologii perzystentnej, phase_winding
OAM -- punkt 19 skilla), ale konstrukcyjnie inny -- pierwszy, ktory
jawnie przechodzi przez formalizm Chronoprocesu Xi=(T,x,Gamma,phi)
(docs/theory/TIMDR_Chronoprocess.md) zamiast embeddingu opozniajacego
Takensa.

RDZEN POMYSLU (propozycja uzytkownika, sparafrazowana w PREREG):
SZCZYT (lokalne maksimum) sygnalu M/S generuje SKRET/faze theta(t),
SZUM/ANOMALIA (istniejacy obiekt M/S, |x-mean|/std) daje promien r(t),
brakujaca trzecia os to CZAS z=t (Chronoproces, NAJPROSTSZE mozliwe
uproszczenie -- rodzina jednoelementowa {gamma}, NIE pelna kongruencja
Gamma:TxI->R^3 z chronocongruence.py -- patrz PREREG SS4). Krzywa 3D
(r*cos(theta), r*sin(theta), t) -- fizycznie normalne (nie-anomalne)
obroty maja dawac ksztalty lejowate (stozkowe); metryka
`chrono_cone_ratio` = stosunek promienia w ostatnim vs pierwszym
`edge_fraction` oknie, INSPIROWANA koncepcyjnie `funnel_ratio`/
`phasespace_funnel_ratio` z NIEPOWIAZANEGO projektu TIMDR-fusion-tools
(plazma tokamaka TCABR) -- NAZWANA INACZEJ celowo (patrz PREREG SS1,
audyt nazw PRZED uzyciem), kod NIE jest laczony ani kopiowany, wynik
z tamtego repo NIE jest zakladany jako przenoszacy sie tutaj.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow kontroli
syntetycznych ani realnych danych -- wszystkie stale (SMOOTH_WINDOW,
EDGE_FRACTION, siatki okien, generatory kontrolne) sa przeniesione 1:1
z zamrozonej pre-rejestracji.
"""
from __future__ import annotations

import csv
import os
import sys
import time
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    mann_whitney_test,
    rank_biserial_effect_size,
    effect_size_label,
    TestResult,
)

# ---------------------------------------------------------------------
# Stale zamrozone w PREREG_CHRONO_CONE_MS_BRIDGE_v0.1.md SS2-6
# ---------------------------------------------------------------------

SMOOTH_WINDOW = 5          # SS2 -- musi byc << okres oscylacji (~15 probek)
EDGE_FRACTION = 0.2        # SS5 -- 20% pierwszych/ostatnich probek okna
OMEGA = 2 * np.pi / 15.0   # SS6 -- okres ~15 probek, wspolny dla (a)/(b)/(c)

# ---------------------------------------------------------------------
# SS2. theta(t) -- peak-referenced phase
# ---------------------------------------------------------------------


def _moving_average(x: np.ndarray, window: int) -> np.ndarray:
    """Wygladzenie centrowane, padding metoda 'edge', dlugosc wyjscia
    == dlugosc wejscia. `window` musi byc nieparzyste."""
    n = len(x)
    if window <= 1:
        return x.astype(float).copy()
    assert window % 2 == 1, "smooth_window musi byc nieparzyste"
    half = window // 2
    xpad = np.pad(x.astype(float), (half, half), mode="edge")
    kernel = np.ones(window) / window
    sm = np.convolve(xpad, kernel, mode="valid")
    return sm[:n]


def _find_peaks(xs: np.ndarray) -> np.ndarray:
    """Scisle lokalne maksima, wylacznie punkty wewnetrzne (bez
    zawijania na brzegach okna) -- wektoryzowane."""
    if len(xs) < 3:
        return np.array([], dtype=int)
    mask = (xs[1:-1] > xs[:-2]) & (xs[1:-1] > xs[2:])
    return np.nonzero(mask)[0] + 1


def peak_referenced_phase(
    x: np.ndarray, smooth_window: int = SMOOTH_WINDOW
) -> Optional[np.ndarray]:
    """theta(t), SS2 pre-rejestracji. Zwraca None jesli < 2 szczyty
    (theta NIEZDEFINIOWANA dla tego okna -- jawnie obslugiwany
    przypadek, nie blad)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    xs = _moving_average(x, smooth_window)
    peaks = _find_peaks(xs)
    if len(peaks) < 2:
        return None

    theta = np.zeros(n, dtype=float)
    theta[: peaks[0]] = 0.0
    for k in range(len(peaks) - 1):
        p0, p1 = int(peaks[k]), int(peaks[k + 1])
        span = p1 - p0
        if span <= 0:
            continue
        t_local = np.arange(p0, p1 + 1) - p0
        theta[p0 : p1 + 1] = 2 * np.pi * k + 2 * np.pi * (t_local / span)
    theta[peaks[-1] :] = 2 * np.pi * (len(peaks) - 1)
    return theta


# ---------------------------------------------------------------------
# SS3. r(t) -- promien z anomalii (ciagla wersja anomalia_flags())
# ---------------------------------------------------------------------


def anomaly_radius(x: np.ndarray) -> np.ndarray:
    """r(t) = |x(t)-mean(x)|/std(x) -- ciagla wersja
    timdr_formalism.chronosignal.anomalia_flags() (ktora progowala
    ta sama wielkosc na k=2.0). Przy std==0: r(t)=0 wszedzie, zgodnie
    z konwencja anomalia_flags() dla sygnalu stalego."""
    x = np.asarray(x, dtype=float)
    m, sd = float(x.mean()), float(x.std())
    if sd == 0.0:
        return np.zeros_like(x)
    return np.abs(x - m) / sd


# ---------------------------------------------------------------------
# SS4-5. z(t)=t (Chronoproces, uproszczenie jednoelementowe), krzywa 3D,
# metryka chrono_cone_ratio
# ---------------------------------------------------------------------


def chrono_cone_curve(
    x: np.ndarray, smooth_window: int = SMOOTH_WINDOW
) -> Optional[np.ndarray]:
    """(r*cos theta, r*sin theta, t) -- None jesli theta niezdefiniowana.
    z(t)=t jest NAJPROSTSZYM mozliwym rzutem G Chronoprocesu (rodzina
    jednoelementowa {gamma}, patrz PREREG SS4) -- NIE pelna kongruencja
    Gamma:TxI->R^3 z timdr_geometry/chronocongruence.py."""
    theta = peak_referenced_phase(x, smooth_window)
    if theta is None:
        return None
    r = anomaly_radius(x)
    t = np.arange(len(x), dtype=float)
    return np.stack([r * np.cos(theta), r * np.sin(theta), t], axis=1)


def chrono_cone_ratio(
    x: np.ndarray,
    smooth_window: int = SMOOTH_WINDOW,
    edge_fraction: float = EDGE_FRACTION,
) -> float:
    """Metryka SS5 pre-rejestracji. NaN jesli theta niezdefiniowana LUB
    r_start ~ 0 (nie 0.0 lub 1.0 -- NaN jest trzecim, jawnie odrebnym
    wynikiem 'niezdefiniowane', patrz PREREG SS5)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    theta = peak_referenced_phase(x, smooth_window)
    if theta is None:
        return float("nan")
    r = anomaly_radius(x)
    n_edge = max(2, round(edge_fraction * n))
    r_start = float(np.mean(r[:n_edge]))
    r_end = float(np.mean(r[-n_edge:]))
    if r_start < 1e-9:
        return float("nan")
    return r_end / r_start


# ---------------------------------------------------------------------
# SS6. Generatory kontrolne syntetyczne (zamrozone)
# ---------------------------------------------------------------------

GROWTH_RATE = 0.05   # (a) pozytywna: amplituda = 1 + GROWTH_RATE*t
NOISE_STD_OSC = 0.15  # (a)/(c) poziom szumu addytywnego na oscylacji
WHITE_NOISE_SCALE = 1.0  # (b) skala czystego szumu bialego


def make_growing_amplitude(window_size: int, seed: Optional[int]) -> np.ndarray:
    """(a) POZYTYWNA -- amplituda rosnaca w czasie, PREREG SS6a."""
    rng = np.random.default_rng(seed)
    t = np.arange(window_size, dtype=float)
    amp = 1.0 + GROWTH_RATE * t
    return amp * np.sin(OMEGA * t) + rng.normal(0.0, NOISE_STD_OSC, window_size)


def make_white_noise(window_size: int, seed: Optional[int]) -> np.ndarray:
    """(b) NEGATYWNA A -- czysty szum bialy, PREREG SS6b."""
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, WHITE_NOISE_SCALE, window_size)


def make_constant_amplitude(window_size: int, seed: Optional[int]) -> np.ndarray:
    """(c) NEGATYWNA B -- stacjonarna oscylacja, STALA amplituda,
    PREREG SS6c."""
    rng = np.random.default_rng(seed)
    t = np.arange(window_size, dtype=float)
    return np.sin(OMEGA * t) + rng.normal(0.0, NOISE_STD_OSC, window_size)


# ---------------------------------------------------------------------
# Bramka kontrolna z obsluga NaN (PREREG SS6, "Obsluga NaN") -- WLASNY
# wrapper, NIE pipeline.run_controls() bezposrednio, bo run_controls()
# zaklada, ze metric_fn zawsze zwraca wartosc uzywalna w Mann-Whitney;
# tutaj NaN jest legalnym, oczekiwanym wynikiem metryki (za malo
# szczytow), wiec trzeba go jawnie odfiltrowac PRZED testem i
# zaraportowac n_valid osobno.
# ---------------------------------------------------------------------


class ChronoConeControlResult:
    __test__ = False  # nie jest klasa testow pytest

    def __init__(
        self,
        positive: Optional[TestResult],
        negative: Optional[TestResult],
        n_valid_pos: int,
        n_valid_neg_a: int,
        n_valid_neg_b: int,
        n_total: int,
        passed: bool,
        inconclusive: bool,
        reason: str,
    ):
        self.positive = positive
        self.negative = negative
        self.n_valid_pos = n_valid_pos
        self.n_valid_neg_a = n_valid_neg_a
        self.n_valid_neg_b = n_valid_neg_b
        self.n_total = n_total
        self.passed = passed
        self.inconclusive = inconclusive
        self.reason = reason


MIN_VALID_FRAC = 0.5  # PREREG SS6: >50% NaN w ktorejkolwiek grupie -> inconclusive


def run_chrono_cone_controls(
    positive_injector: Callable[[int, Optional[int]], np.ndarray],
    negative_generator_a: Callable[[int, Optional[int]], np.ndarray],
    negative_generator_b: Callable[[int, Optional[int]], np.ndarray],
    n_windows: int,
    window_size: int,
    seed: int = 0,
    alpha: float = 0.05,
    edge_fraction: float = EDGE_FRACTION,
    smooth_window: int = SMOOTH_WINDOW,
) -> ChronoConeControlResult:
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)

    def _values(gen, seed_offset=0):
        return np.array(
            [
                chrono_cone_ratio(
                    gen(window_size, int(s) + seed_offset),
                    smooth_window=smooth_window,
                    edge_fraction=edge_fraction,
                )
                for s in seeds
            ]
        )

    pos_all = _values(positive_injector)
    neg_a_all = _values(negative_generator_a)
    neg_b_all = _values(negative_generator_b, seed_offset=1)

    pos_valid = pos_all[~np.isnan(pos_all)]
    neg_a_valid = neg_a_all[~np.isnan(neg_a_all)]
    neg_b_valid = neg_b_all[~np.isnan(neg_b_all)]

    n_total = n_windows
    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_total)))

    if (
        len(pos_valid) < min_needed
        or len(neg_a_valid) < min_needed
        or len(neg_b_valid) < min_needed
    ):
        return ChronoConeControlResult(
            positive=None,
            negative=None,
            n_valid_pos=len(pos_valid),
            n_valid_neg_a=len(neg_a_valid),
            n_valid_neg_b=len(neg_b_valid),
            n_total=n_total,
            passed=False,
            inconclusive=True,
            reason=(
                f"Za duzo NaN (theta niezdefiniowana, <2 szczyty) w co "
                f"najmniej jednej grupie: pos={len(pos_valid)}/{n_total}, "
                f"neg_a={len(neg_a_valid)}/{n_total}, "
                f"neg_b={len(neg_b_valid)}/{n_total}, prog={min_needed}. "
                f"NIEROZSTRZYGNIETE z powodu mocy, nie brak efektu."
            ),
        )

    positive = mann_whitney_test(pos_valid, neg_a_valid)
    negative = mann_whitney_test(neg_a_valid, neg_b_valid)

    pos_ok = positive.pvalue < alpha
    neg_ok = negative.pvalue >= alpha
    passed = pos_ok and neg_ok

    if passed:
        reason = (
            "Kontrola pozytywna (rosnaca amplituda vs szum bialy) wykryla "
            "istotna roznice, kontrola negatywna (szum bialy vs stala "
            "amplituda) nie dala falszywego alarmu."
        )
    elif not pos_ok and not neg_ok:
        reason = "Kontrola pozytywna NIE wykryla efektu I kontrola negatywna dala falszywy alarm -- mechanika zepsuta."
    elif not pos_ok:
        reason = "Kontrola pozytywna nie wykryla wzrostu amplitudy -- metryka za malo czula."
    else:
        reason = "Kontrola negatywna (szum bialy vs stala amplituda) dala istotna roznice -- same w sobie warte odnotowania (PREREG SS6)."

    return ChronoConeControlResult(
        positive=positive,
        negative=negative,
        n_valid_pos=len(pos_valid),
        n_valid_neg_a=len(neg_a_valid),
        n_valid_neg_b=len(neg_b_valid),
        n_total=n_total,
        passed=passed,
        inconclusive=False,
        reason=reason,
    )


# ---------------------------------------------------------------------
# SS7. Siatka syntetyczna (zamrozona)
# ---------------------------------------------------------------------

SYN_WINDOW_SIZES = (128, 256)
SYN_N_WINDOWS = 30
SYN_SEED = 0
SYN_ALPHA = 0.05


def run_synthetic_controls() -> List[Dict]:
    rows = []
    for window_size in SYN_WINDOW_SIZES:
        result = run_chrono_cone_controls(
            positive_injector=make_growing_amplitude,
            negative_generator_a=make_white_noise,
            negative_generator_b=make_constant_amplitude,
            n_windows=SYN_N_WINDOWS,
            window_size=window_size,
            seed=SYN_SEED,
            alpha=SYN_ALPHA,
        )
        rows.append({"window_size": window_size, "result": result})
    return rows


def format_synthetic_report(rows: List[Dict]) -> str:
    lines = ["## Kontrole syntetyczne chrono_cone_ratio", ""]
    for row in rows:
        w = row["window_size"]
        r: ChronoConeControlResult = row["result"]
        lines.append(f"### window_size={w}")
        lines.append(
            f"n_valid: pos={r.n_valid_pos}/{r.n_total}, "
            f"neg_a={r.n_valid_neg_a}/{r.n_total}, neg_b={r.n_valid_neg_b}/{r.n_total}"
        )
        if r.inconclusive:
            lines.append(f"INCONCLUSIVE: {r.reason}")
        else:
            lines.append(
                f"pozytywna: p={r.positive.pvalue:.4g} r={r.positive.effect_size_r:.3f} "
                f"({effect_size_label(r.positive.effect_size_r)}) "
                f"mediana(a)={r.positive.median_test:.4g} mediana(b)={r.positive.median_background:.4g}"
            )
            lines.append(
                f"negatywna: p={r.negative.pvalue:.4g} r={r.negative.effect_size_r:.3f} "
                f"mediana(b)={r.negative.median_test:.4g} mediana(c)={r.negative.median_background:.4g}"
            )
            lines.append(f"PASSED={r.passed} -- {r.reason}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    rows = run_synthetic_controls()
    print(format_synthetic_report(rows))
    print(f"Czas: {time.time()-t0:.2f}s")
