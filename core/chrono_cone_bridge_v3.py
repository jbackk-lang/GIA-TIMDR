# core/chrono_cone_bridge_v3.py
"""
chrono_cone_bridge_v3.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_CHRONO_CONE_MS_BRIDGE_v0.3.md) hipotezy uzytkownika
o "sile odsrodkowej": utrzymujace sie w czasie krecenie (nagromadzony,
NIE modulo-2*pi kat theta_v2 z core/chrono_cone_bridge_v2.py) samo z
siebie wzmacnia promien r(t), niezaleznie od tego, czy sama anomalia
|x-mean|/std rosnie.

r_total(t) = r_anomalia(t) * (1 + k * theta_unwrapped(t)**2)

theta_unwrapped(t) to DOKLADNIE core.chrono_cone_bridge_v2.trend_referenced_phase
-- BEZ ZMIAN, reuzywane, NIE redefiniowane (theta_v2 juz jest
"nagromadzona"/odwinieta, nie modulo 2*pi -- audyt PREREG SS1). r_anomalia(t)
to DOKLADNIE core.chrono_cone_bridge.anomaly_radius -- BEZ ZMIAN.

Jedna nowa zmienna wzgledem v0.2 (protokol "jedna zmienna na raz"): TYLKO
wzor na promien. theta(t) niezmieniona.

Odrzucona alternatywa (PREREG SS3): r_total = r_anomalia + k*omega(t)**2
gdzie omega=dtheta/dt (chwilowa predkosc katowa, blizej doslownego
F=m*omega^2*r) -- odrzucona, bo traci "akumulacje w czasie" (uzytkownik:
"wpadajace w czasie w obrot"), ktora jest sednem hipotezy.

Metafora "spin fotonu na elektronie" wspomniana przez uzytkownika jest
TU WYLACZNIE INSPIRACJA JEZYKOWA, NIE rownowaznikiem fizycznym budowanym
w te matematyke -- analogicznie do TIMDR_Gravity_Speculative.md (skill
punkt 9): analogia, nie rownowaznosc.
"""
from __future__ import annotations

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
    anomaly_radius,
    make_growing_amplitude,
    make_white_noise,
    make_constant_amplitude,
)
from core.chrono_cone_bridge_v2 import (  # noqa: E402
    trend_referenced_phase,
    chrono_pendulum_ratio,
)

try:
    from scipy import stats as _scipy_stats

    _HAS_SCIPY = True
except Exception:  # pragma: no cover -- Device Guard scenariusz, patrz pipeline.py
    _scipy_stats = None
    _HAS_SCIPY = False


# ---------------------------------------------------------------------
# PREREG SS3 -- kalibracja k (zamrozona METODA, PRZED realnymi danymi;
# wykonana WYLACZNIE na kontroli syntetycznej POZYTYWNEJ -- reuzywany
# 1:1 make_growing_amplitude z core/chrono_cone_bridge.py)
# ---------------------------------------------------------------------

A_MAX = 10.0  # PREREG: czynnik odsrodkowy (1+k*theta^2) nie ma przekraczac
              # ~10x (rzad wielkosci) na SZCZYCIE |theta| kontroli pozytywnej
CALIB_N = 30       # jak SYN_N_WINDOWS w v1/v2
CALIB_SEED = 1000  # ROZLACZNY z seedami testowymi (0..N-1) -- konwencja
                   # z punktu 22 skilla (kalibracja z tla/kontroli, nie z
                   # tych samych probek co test)

# Unia WSZYSTKICH rozmiarow okien uzywanych w calej rodzinie testow
# (syntetyczne 128/256, lozyska 256/512, sejsmika 512/1024, BTC 48) --
# k skalibrowane dla kazdego PRZED dotknieciem realnych danych.
ALL_WINDOW_SIZES = (48, 128, 256, 512, 1024)


def calibrate_k(
    window_size: int,
    target_amplification: float = A_MAX,
    n_calib: int = CALIB_N,
    calib_seed: int = CALIB_SEED,
    smooth_window: int = SMOOTH_WINDOW,
) -> float:
    """PREREG SS3: k(window_size) = A_MAX / M(window_size), gdzie
    M(window_size) = mediana (po n_calib niezaleznych realizacjach
    kontroli POZYTYWNEJ, rosnaca amplituda) z max_t theta_unwrapped(t)**2
    w oknie. Mechaniczna, deterministyczna procedura -- BEZ dotykania
    realnych danych ani zgadywania stalej."""
    rng = np.random.default_rng(calib_seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_calib)
    maxes = []
    for s in seeds:
        x = make_growing_amplitude(window_size, int(s))
        theta = trend_referenced_phase(x, smooth_window)
        if theta is None:
            continue
        maxes.append(float(np.max(theta**2)))
    if not maxes:
        return float("nan")
    M = float(np.median(maxes))
    if M <= 0:
        return float("nan")
    return target_amplification / M


# Zamrozona tabela k, wyliczona RAZ (deterministyczny seed) -- patrz
# docs/geometry/PREREG_CHRONO_CONE_MS_BRIDGE_v0.3.md SS3 dla wartosci
# liczbowych wpisanych do dokumentu PRZED uruchomieniem na realnych
# danych.
K_TABLE: Dict[int, float] = {w: calibrate_k(w) for w in ALL_WINDOW_SIZES}


def _k_for(n: int) -> float:
    k = K_TABLE.get(n)
    if k is None or (isinstance(k, float) and np.isnan(k)):
        # Rozmiar okna spoza z gory znanej siatki -- ta sama, zamrozona
        # metoda kalibracji zastosowana "w locie", NIE nowa/inna metoda.
        k = calibrate_k(n)
    return k


# ---------------------------------------------------------------------
# PREREG SS2 -- r_total(t), krzywa, metryka chrono_centrifugal_ratio
# ---------------------------------------------------------------------


def centrifugal_radius(
    x: np.ndarray, smooth_window: int = SMOOTH_WINDOW, k: Optional[float] = None
) -> Optional[np.ndarray]:
    """r_total(t) = r_anomalia(t) * (1 + k*theta_unwrapped(t)**2). None
    jesli theta niezdefiniowana (<2 ekstrema), identycznie jak v1/v2."""
    x = np.asarray(x, dtype=float)
    theta = trend_referenced_phase(x, smooth_window)
    if theta is None:
        return None
    r = anomaly_radius(x)
    kk = k if k is not None else _k_for(len(x))
    return r * (1.0 + kk * theta**2)


def chrono_centrifugal_curve(
    x: np.ndarray, smooth_window: int = SMOOTH_WINDOW, k: Optional[float] = None
) -> Optional[np.ndarray]:
    theta = trend_referenced_phase(x, smooth_window)
    if theta is None:
        return None
    rt = centrifugal_radius(x, smooth_window, k)
    t = np.arange(len(x), dtype=float)
    return np.stack([rt * np.cos(theta), rt * np.sin(theta), t], axis=1)


def chrono_centrifugal_ratio(
    x: np.ndarray,
    smooth_window: int = SMOOTH_WINDOW,
    edge_fraction: float = EDGE_FRACTION,
    k: Optional[float] = None,
) -> float:
    """Metryka PRIMARNA v0.3 -- identyczna konstrukcja brzeg/brzeg co
    chrono_cone_ratio/chrono_pendulum_ratio, ale na r_total zamiast
    r_anomalia."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    rt = centrifugal_radius(x, smooth_window, k)
    if rt is None:
        return float("nan")
    n_edge = max(2, round(edge_fraction * n))
    r_start = float(np.mean(rt[:n_edge]))
    r_end = float(np.mean(rt[-n_edge:]))
    if r_start < 1e-9:
        return float("nan")
    return r_end / r_start


# ---------------------------------------------------------------------
# PREREG SS5 Kontrola #0 (RYZYKO, uruchamiana PIERWSZA) -- czy sam czlon
# odsrodkowy generuje falszywy "lej" z czystego szumu bialego?
# Test PAROWY (te same realizacje szumu, dwie metryki) -- Wilcoxon
# signed-rank, NIE Mann-Whitney (dane sparowane, nie niezalezne;
# uzasadnienie w PREREG SS5).
# ---------------------------------------------------------------------


class NoiseRiskControlResult:
    __test__ = False

    def __init__(self, window_size, n_valid, inconclusive, reason,
                 p=None, r_eff=None, median_pendulum=None, median_centrifugal=None,
                 iqr_pendulum=None, iqr_centrifugal=None, spread_inflation=None,
                 false_signal=None):
        self.window_size = window_size
        self.n_valid = n_valid
        self.inconclusive = inconclusive
        self.reason = reason
        self.p = p
        self.r_eff = r_eff
        self.median_pendulum = median_pendulum
        self.median_centrifugal = median_centrifugal
        self.iqr_pendulum = iqr_pendulum
        self.iqr_centrifugal = iqr_centrifugal
        self.spread_inflation = spread_inflation
        self.false_signal = false_signal


MIN_VALID_FRAC = 0.5  # jak v0.1/v0.2


def _matched_pairs_rank_biserial(diffs: np.ndarray) -> float:
    """Rozmiar efektu dla Wilcoxona signed-rank, niezalezny od scipy
    (uzywa scipy.stats.rankdata, dostepnego wraz z wilcoxon)."""
    nz = diffs[diffs != 0]
    if len(nz) == 0:
        return 0.0
    ranks = _scipy_stats.rankdata(np.abs(nz))
    w_pos = float(ranks[nz > 0].sum())
    w_neg = float(ranks[nz < 0].sum())
    denom = w_pos + w_neg
    if denom == 0:
        return 0.0
    return (w_pos - w_neg) / denom


def run_noise_risk_control(
    window_size: int,
    n_windows: int = 30,
    seed: int = 0,
    alpha: float = 0.05,
    smooth_window: int = SMOOTH_WINDOW,
    edge_fraction: float = EDGE_FRACTION,
) -> NoiseRiskControlResult:
    if not _HAS_SCIPY:
        raise RuntimeError(
            "run_noise_risk_control wymaga scipy (Wilcoxon signed-rank); "
            "niedostepne w tym srodowisku."
        )
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)

    pendulum_vals: List[float] = []
    centrifugal_vals: List[float] = []
    for s in seeds:
        x = make_white_noise(window_size, int(s))
        rv2 = chrono_pendulum_ratio(x, smooth_window=smooth_window, edge_fraction=edge_fraction)
        rv3 = chrono_centrifugal_ratio(x, smooth_window=smooth_window, edge_fraction=edge_fraction)
        if not (np.isnan(rv2) or np.isnan(rv3)):
            pendulum_vals.append(rv2)
            centrifugal_vals.append(rv3)

    n_valid = len(pendulum_vals)
    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_windows)))
    if n_valid < min_needed:
        return NoiseRiskControlResult(
            window_size=window_size, n_valid=n_valid, inconclusive=True,
            reason=f"Za malo sparowanych, waznych obserwacji ({n_valid}/{n_windows}, prog={min_needed}).",
        )

    pendulum_arr = np.array(pendulum_vals)
    centrifugal_arr = np.array(centrifugal_vals)
    diffs = centrifugal_arr - pendulum_arr

    if np.all(diffs == 0):
        p = 1.0
        r_eff = 0.0
    else:
        stat, p = _scipy_stats.wilcoxon(centrifugal_arr, pendulum_arr, alternative="two-sided")
        r_eff = _matched_pairs_rank_biserial(diffs)

    median_pendulum = float(np.median(pendulum_arr))
    median_centrifugal = float(np.median(centrifugal_arr))
    q75p, q25p = np.percentile(pendulum_arr, [75, 25])
    q75c, q25c = np.percentile(centrifugal_arr, [75, 25])
    iqr_pendulum = float(q75p - q25p)
    iqr_centrifugal = float(q75c - q25c)
    spread_inflation = (
        abs(iqr_centrifugal) / abs(iqr_pendulum) if iqr_pendulum != 0 else float("inf")
    )
    false_signal = bool(p < alpha and abs(r_eff) >= 0.3)

    return NoiseRiskControlResult(
        window_size=window_size, n_valid=n_valid, inconclusive=False,
        reason="OK", p=float(p), r_eff=float(r_eff),
        median_pendulum=median_pendulum, median_centrifugal=median_centrifugal,
        iqr_pendulum=iqr_pendulum, iqr_centrifugal=iqr_centrifugal,
        spread_inflation=spread_inflation, false_signal=false_signal,
    )


def run_all_noise_risk_controls(window_sizes=ALL_WINDOW_SIZES) -> List[NoiseRiskControlResult]:
    return [run_noise_risk_control(w) for w in window_sizes]


# ---------------------------------------------------------------------
# PREREG SS5 Kontrola #1 (STRUKTURALNA, jak w v1/v2) -- (a) rosnaca
# amplituda vs (b) szum bialy vs (c) stala amplituda, na NOWEJ metryce.
# ---------------------------------------------------------------------


class ChronoCentrifugalControlResult:
    __test__ = False

    def __init__(self, positive, negative, n_valid_pos, n_valid_neg_a, n_valid_neg_b,
                 n_total, passed, inconclusive, reason):
        self.positive = positive
        self.negative = negative
        self.n_valid_pos = n_valid_pos
        self.n_valid_neg_a = n_valid_neg_a
        self.n_valid_neg_b = n_valid_neg_b
        self.n_total = n_total
        self.passed = passed
        self.inconclusive = inconclusive
        self.reason = reason


def run_chrono_centrifugal_controls(
    positive_injector: Callable[[int, Optional[int]], np.ndarray],
    negative_generator_a: Callable[[int, Optional[int]], np.ndarray],
    negative_generator_b: Callable[[int, Optional[int]], np.ndarray],
    n_windows: int,
    window_size: int,
    seed: int = 0,
    alpha: float = 0.05,
    edge_fraction: float = EDGE_FRACTION,
    smooth_window: int = SMOOTH_WINDOW,
) -> ChronoCentrifugalControlResult:
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)

    def _values(gen, seed_offset=0):
        return np.array([
            chrono_centrifugal_ratio(
                gen(window_size, int(s) + seed_offset),
                smooth_window=smooth_window, edge_fraction=edge_fraction,
            ) for s in seeds
        ])

    pos_all = _values(positive_injector)
    neg_a_all = _values(negative_generator_a)
    neg_b_all = _values(negative_generator_b, seed_offset=1)

    pos_valid = pos_all[~np.isnan(pos_all)]
    neg_a_valid = neg_a_all[~np.isnan(neg_a_all)]
    neg_b_valid = neg_b_all[~np.isnan(neg_b_all)]

    n_total = n_windows
    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_total)))

    if (len(pos_valid) < min_needed or len(neg_a_valid) < min_needed or len(neg_b_valid) < min_needed):
        return ChronoCentrifugalControlResult(
            positive=None, negative=None, n_valid_pos=len(pos_valid),
            n_valid_neg_a=len(neg_a_valid), n_valid_neg_b=len(neg_b_valid),
            n_total=n_total, passed=False, inconclusive=True,
            reason=(f"Za duzo NaN: pos={len(pos_valid)}/{n_total}, "
                    f"neg_a={len(neg_a_valid)}/{n_total}, neg_b={len(neg_b_valid)}/{n_total}, "
                    f"prog={min_needed}."),
        )

    positive = mann_whitney_test(pos_valid, neg_a_valid)
    negative = mann_whitney_test(neg_a_valid, neg_b_valid)
    pos_ok = positive.pvalue < alpha
    neg_ok = negative.pvalue >= alpha
    passed = pos_ok and neg_ok

    if passed:
        reason = "Kontrola pozytywna istotna, kontrola negatywna bez falszywego alarmu."
    elif not pos_ok and not neg_ok:
        reason = "Kontrola pozytywna NIE wykryla efektu I kontrola negatywna dala falszywy alarm."
    elif not pos_ok:
        reason = "Kontrola pozytywna nie wykryla wzrostu amplitudy."
    else:
        reason = "Kontrola negatywna dala istotna roznice (b vs c)."

    return ChronoCentrifugalControlResult(
        positive=positive, negative=negative, n_valid_pos=len(pos_valid),
        n_valid_neg_a=len(neg_a_valid), n_valid_neg_b=len(neg_b_valid),
        n_total=n_total, passed=passed, inconclusive=False, reason=reason,
    )


SYN_WINDOW_SIZES = (128, 256)  # identyczne z v0.1/v0.2
SYN_N_WINDOWS = 30
SYN_SEED = 0
SYN_ALPHA = 0.05


def run_synthetic_controls() -> List[Dict]:
    rows = []
    for window_size in SYN_WINDOW_SIZES:
        result = run_chrono_centrifugal_controls(
            positive_injector=make_growing_amplitude,
            negative_generator_a=make_white_noise,
            negative_generator_b=make_constant_amplitude,
            n_windows=SYN_N_WINDOWS, window_size=window_size,
            seed=SYN_SEED, alpha=SYN_ALPHA,
        )
        rows.append({"window_size": window_size, "result": result})
    return rows


def format_risk_report(results: List[NoiseRiskControlResult]) -> str:
    lines = ["## Kontrola #0 (RYZYKO) -- czlon odsrodkowy na czystym szumie", ""]
    for r in results:
        lines.append(f"### window_size={r.window_size}  k={K_TABLE.get(r.window_size, float('nan')):.6g}")
        if r.inconclusive:
            lines.append(f"INCONCLUSIVE: {r.reason}")
        else:
            lines.append(
                f"n_valid={r.n_valid} p={r.p:.4g} r_eff={r.r_eff:.3f} "
                f"mediana(pendulum)={r.median_pendulum:.4g} mediana(centrifugal)={r.median_centrifugal:.4g} "
                f"IQR(pendulum)={r.iqr_pendulum:.4g} IQR(centrifugal)={r.iqr_centrifugal:.4g} "
                f"spread_inflation={r.spread_inflation:.3f} "
                f"FALSE_SIGNAL={r.false_signal}"
            )
        lines.append("")
    return "\n".join(lines)


def format_synthetic_report(rows: List[Dict]) -> str:
    lines = ["## Kontrole strukturalne chrono_centrifugal_ratio (v0.3)", ""]
    for row in rows:
        w = row["window_size"]
        r: ChronoCentrifugalControlResult = row["result"]
        lines.append(f"### window_size={w}  k={K_TABLE.get(w, float('nan')):.6g}")
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
    print("K_TABLE:", K_TABLE)
    risk_results = run_all_noise_risk_controls()
    print(format_risk_report(risk_results))
    any_false_signal = any(r.false_signal for r in risk_results if not r.inconclusive)
    print(f"ANY_FALSE_SIGNAL (kontrola #0)={any_false_signal}")
    if not any_false_signal:
        rows = run_synthetic_controls()
        print(format_synthetic_report(rows))
    else:
        print("STOP: kontrola #0 (ryzyko falszywego sygnalu z szumu) NIE przeszla -- "
              "nie uruchamiam kontroli strukturalnej ani realnych danych.")
    print(f"Czas: {time.time()-t0:.2f}s")
