# core/chrono_cone_bridge_v2.py
"""
chrono_cone_bridge_v2.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_CHRONO_CONE_MS_BRIDGE_v0.2.md) hipotezy uzytkownika:
w v0.1 (core/chrono_cone_bridge.py) theta(t) rosla MONOTONICZNIE o 2*pi
miedzy kolejnymi SZCZYTAMI, niezaleznie od tego, czy sygnal akurat
wznosil sie czy opadal (kolo zamachowe). v0.2 zmienia WYLACZNIE regule
kierunku: miedzy kolejnymi EKSTREMAMI (szczyt LUB dolina) faza rosnie o
+2*pi jesli sygnal WZNOSI SIE do nastepnego ekstremum, i o -2*pi jesli
OPADA -- symetryczny cykl dolina->szczyt->dolina wraca (dokladnie, nie
tylko mod 2*pi) do tej samej wartosci fazy, zamiast robic pelny obrot
+4*pi jak zrobilby v0.1.

WAZNE (PREREG SS1, przeczytane PRZED napisaniem tego pliku): funkcja
chrono_cone_ratio/chrono_pendulum_ratio uzywa theta WYLACZNIE jako
bramki istnienia (czy sa >=2 ekstrema) -- sama WARTOSC liczbowa ratio
jest funkcja WYLACZNIE r(t), nie zalezy od kierunku theta. Zmiana
kierunku moze wiec zmienic wynik testu na realnych danych WYLACZNIE
posrednio, przez zmiane skladu zbioru okien przechodzacych bramke
(v0.2 liczy TEZ doliny, nie tylko szczyty -- bramka jest z natury
bardziej permisywna). Zeby dac hipotezie uczciwa szanse zadzialac przez
sam mechanizm rotacji (nie tylko efekt bramki), plik definiuje TEZ
`chrono_pendulum_net_turn` -- metryke, ktora FAKTYCZNIE uzywa wartosci
theta, jawnie oznaczona jako eksploracyjna/dodatkowa (PREREG SS5).

r(t) i z(t)=t: BEZ ZMIAN wzgledem v0.1 (ten sam anomaly_radius,
identyczny Chronoproces jako os z) -- importowane z chrono_cone_bridge.py,
NIE redefiniowane tutaj.

Zadna funkcja v0.1 (core/chrono_cone_bridge.py) nie jest nadpisywana
przez ten plik -- v0.1 pozostaje udokumentowanym, uczciwym wynikiem
negatywnym.
"""
from __future__ import annotations

import csv
import os
import sys
import time
from typing import Callable, Dict, List, Optional

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    mann_whitney_test,
    effect_size_label,
    TestResult,
)
from core.chrono_cone_bridge import (  # noqa: E402
    SMOOTH_WINDOW,
    EDGE_FRACTION,
    OMEGA,
    _moving_average,
    _find_peaks,
    anomaly_radius,
    make_growing_amplitude,
    make_white_noise,
    make_constant_amplitude,
    peak_referenced_phase as peak_referenced_phase_v1,
)

# ---------------------------------------------------------------------
# PREREG SS3 -- doliny (lustrzane odbicie _find_peaks z v0.1)
# ---------------------------------------------------------------------


def _find_troughs(xs: np.ndarray) -> np.ndarray:
    """Scisle lokalne minima, wylacznie punkty wewnetrzne -- lustrzane
    odbicie core.chrono_cone_bridge._find_peaks."""
    if len(xs) < 3:
        return np.array([], dtype=int)
    mask = (xs[1:-1] < xs[:-2]) & (xs[1:-1] < xs[2:])
    return np.nonzero(mask)[0] + 1


def _find_extrema(xs: np.ndarray) -> np.ndarray:
    """Wszystkie ekstrema (szczyty + doliny), posortowane wg indeksu."""
    peaks = _find_peaks(xs)
    troughs = _find_troughs(xs)
    if len(peaks) == 0:
        return np.sort(troughs)
    if len(troughs) == 0:
        return np.sort(peaks)
    return np.sort(np.concatenate([peaks, troughs]))


# ---------------------------------------------------------------------
# PREREG SS3 -- theta_v2(t): kierunek segmentu zalezny od trendu
# (Opcja A wybrana, Opcja B odrzucona -- patrz PREREG SS3)
# ---------------------------------------------------------------------


def trend_referenced_phase(
    x: np.ndarray, smooth_window: int = SMOOTH_WINDOW
) -> Optional[np.ndarray]:
    """theta_v2(t), PREREG SS3. Miedzy kolejnymi ekstremami (szczyt LUB
    dolina) faza rosnie o +2*pi (wznoszenie) lub maleje o -2*pi
    (opadanie) -- stala "predkosc katowa" w obrebie segmentu
    (rampa liniowa 2*pi/span), znak WYLACZNIE z kierunku trendu,
    niezaleznie od tempa/amplitudy zmiany (Opcja A).

    Zwraca None jesli <2 ekstrema (dowolnego typu) -- theta
    NIEZDEFINIOWANA, jak w v0.1 (jawnie obslugiwany przypadek, nie
    blad)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    xs = _moving_average(x, smooth_window)
    extrema = _find_extrema(xs)
    if len(extrema) < 2:
        return None

    theta = np.zeros(n, dtype=float)
    theta[: extrema[0]] = 0.0
    cum = 0.0
    for k in range(len(extrema) - 1):
        e0, e1 = int(extrema[k]), int(extrema[k + 1])
        span = e1 - e0
        if span <= 0:
            continue
        direction = 1.0 if xs[e1] > xs[e0] else -1.0
        t_local = np.arange(e0, e1 + 1) - e0
        theta[e0 : e1 + 1] = cum + direction * 2 * np.pi * (t_local / span)
        cum += direction * 2 * np.pi
    theta[extrema[-1] :] = cum
    return theta


# ---------------------------------------------------------------------
# PREREG SS4 -- r(t), z(t): BEZ ZMIAN, reuzywane z v0.1 (anomaly_radius)
# ---------------------------------------------------------------------


def chrono_pendulum_curve(
    x: np.ndarray, smooth_window: int = SMOOTH_WINDOW
) -> Optional[np.ndarray]:
    """(r*cos theta_v2, r*sin theta_v2, t) -- analogiczne do
    chrono_cone_curve, ale z theta_v2 (trend_referenced_phase)."""
    theta = trend_referenced_phase(x, smooth_window)
    if theta is None:
        return None
    r = anomaly_radius(x)
    t = np.arange(len(x), dtype=float)
    return np.stack([r * np.cos(theta), r * np.sin(theta), t], axis=1)


# ---------------------------------------------------------------------
# PREREG SS5 -- metryki
# ---------------------------------------------------------------------


def chrono_pendulum_ratio(
    x: np.ndarray,
    smooth_window: int = SMOOTH_WINDOW,
    edge_fraction: float = EDGE_FRACTION,
) -> float:
    """Metryka PRIMARNA (PREREG SS5) -- IDENTYCZNY wzor co
    chrono_cone_ratio (v0.1), gated na theta_v2 (>=2 ekstrema
    DOWOLNEGO typu, roznica od v0.1 ktory wymagal >=2 SZCZYTOW).
    Wartosc liczbowa NIE zalezy od theta poza brama istnienia (patrz
    modul docstring / PREREG SS1)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    theta = trend_referenced_phase(x, smooth_window)
    if theta is None:
        return float("nan")
    r = anomaly_radius(x)
    n_edge = max(2, round(edge_fraction * n))
    r_start = float(np.mean(r[:n_edge]))
    r_end = float(np.mean(r[-n_edge:]))
    if r_start < 1e-9:
        return float("nan")
    return r_end / r_start


def chrono_pendulum_net_turn(
    x: np.ndarray, smooth_window: int = SMOOTH_WINDOW
) -> float:
    """Metryka SEKUNDARNA, jawnie eksploracyjna (PREREG SS5) -- liczba
    NETTO pelnych obrotow zakumulowanych w oknie:
    (theta_v2[-1]-theta_v2[0])/(2*pi). W odroznieniu od ratio, ta
    wielkosc FAKTYCZNIE zalezy od wartosci theta. NIE uzywana do
    klasyfikacji SUPPORTED/NOT_SUPPORTED (PREREG SS7) -- raportowana
    obok, jako niezalezna proba dania hipotezie rotacji uczciwej
    szansy."""
    theta = trend_referenced_phase(x, smooth_window)
    if theta is None:
        return float("nan")
    return float((theta[-1] - theta[0]) / (2 * np.pi))


# ---------------------------------------------------------------------
# PREREG SS6 -- kontrole syntetyczne. Generatory REUZYWANE 1:1 z v0.1
# (make_growing_amplitude/make_white_noise/make_constant_amplitude,
# core/chrono_cone_bridge.py) -- NIE definiowane od nowa.
# ---------------------------------------------------------------------

MIN_VALID_FRAC = 0.5  # jak v0.1


class ChronoPendulumControlResult:
    __test__ = False

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
        net_turn_c_median: float,
        net_turn_c_mad: float,
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
        self.net_turn_c_median = net_turn_c_median
        self.net_turn_c_mad = net_turn_c_mad


def run_chrono_pendulum_controls(
    positive_injector: Callable[[int, Optional[int]], np.ndarray],
    negative_generator_a: Callable[[int, Optional[int]], np.ndarray],
    negative_generator_b: Callable[[int, Optional[int]], np.ndarray],
    n_windows: int,
    window_size: int,
    seed: int = 0,
    alpha: float = 0.05,
    edge_fraction: float = EDGE_FRACTION,
    smooth_window: int = SMOOTH_WINDOW,
) -> ChronoPendulumControlResult:
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)

    def _values(gen, seed_offset=0):
        return np.array(
            [
                chrono_pendulum_ratio(
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

    # Sanity-check PREREG SS6(c): net_turn na kontroli (c) powinien byc
    # bliski 0 (wahadlo), nie rosnacy bez ograniczen jak w v0.1.
    net_turns_c = np.array(
        [
            chrono_pendulum_net_turn(
                negative_generator_b(window_size, int(s) + 1),
                smooth_window=smooth_window,
            )
            for s in seeds
        ]
    )
    net_turns_c_valid = net_turns_c[~np.isnan(net_turns_c)]
    net_turn_c_median = (
        float(np.median(net_turns_c_valid)) if len(net_turns_c_valid) else float("nan")
    )
    net_turn_c_mad = (
        float(np.median(np.abs(net_turns_c_valid - net_turn_c_median)))
        if len(net_turns_c_valid)
        else float("nan")
    )

    n_total = n_windows
    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_total)))

    if (
        len(pos_valid) < min_needed
        or len(neg_a_valid) < min_needed
        or len(neg_b_valid) < min_needed
    ):
        return ChronoPendulumControlResult(
            positive=None,
            negative=None,
            n_valid_pos=len(pos_valid),
            n_valid_neg_a=len(neg_a_valid),
            n_valid_neg_b=len(neg_b_valid),
            n_total=n_total,
            passed=False,
            inconclusive=True,
            reason=(
                f"Za duzo NaN w co najmniej jednej grupie: "
                f"pos={len(pos_valid)}/{n_total}, neg_a={len(neg_a_valid)}/{n_total}, "
                f"neg_b={len(neg_b_valid)}/{n_total}, prog={min_needed}."
            ),
            net_turn_c_median=net_turn_c_median,
            net_turn_c_mad=net_turn_c_mad,
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
        reason = "Kontrola pozytywna NIE wykryla efektu I kontrola negatywna dala falszywy alarm."
    elif not pos_ok:
        reason = "Kontrola pozytywna nie wykryla wzrostu amplitudy."
    else:
        reason = "Kontrola negatywna dala istotna roznice (b vs c)."

    return ChronoPendulumControlResult(
        positive=positive,
        negative=negative,
        n_valid_pos=len(pos_valid),
        n_valid_neg_a=len(neg_a_valid),
        n_valid_neg_b=len(neg_b_valid),
        n_total=n_total,
        passed=passed,
        inconclusive=False,
        reason=reason,
        net_turn_c_median=net_turn_c_median,
        net_turn_c_mad=net_turn_c_mad,
    )


SYN_WINDOW_SIZES = (128, 256)  # identyczne z v0.1
SYN_N_WINDOWS = 30
SYN_SEED = 0
SYN_ALPHA = 0.05


def run_synthetic_controls() -> List[Dict]:
    rows = []
    for window_size in SYN_WINDOW_SIZES:
        result = run_chrono_pendulum_controls(
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
    lines = ["## Kontrole syntetyczne chrono_pendulum_ratio (v0.2)", ""]
    for row in rows:
        w = row["window_size"]
        r: ChronoPendulumControlResult = row["result"]
        lines.append(f"### window_size={w}")
        lines.append(
            f"n_valid: pos={r.n_valid_pos}/{r.n_total}, "
            f"neg_a={r.n_valid_neg_a}/{r.n_total}, neg_b={r.n_valid_neg_b}/{r.n_total}"
        )
        lines.append(
            f"sanity net_turn(c) [wahadlo, oczekiwane bliskie 0]: "
            f"mediana={r.net_turn_c_median:.4f} MAD={r.net_turn_c_mad:.4f}"
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
