# core/real_zero_mode_topology_bridge.py
"""
real_zero_mode_topology_bridge.py -- implementacja PRE-REJESTROWANEJ
(docs/geometry/PREREG_MOBIUS_COHERENCE_BRIDGES.md, zadanie #64) kontroli
pozytywnej/negatywnej dla kandydujacego (NIE ustalonego) mostu M/S<->G #1
(core/zero_mode_topology_bridge.py: Z0, G_i, MC_{M/S<->G} ciagly/binarny)
na TRZECH realnych domenach: lozyska CWRU, sejsmika Ridgecrest, BTC/USD.

Zero nowych danych/generatorow/siatek -- reuzyte 1:1 z trzech istniejacych
mostow M/S<->topologia/K. GiRanges/theta0/thetaG kalibrowane z MIESZANEJ
puli 30 okien pozytywnych + 30 negatywnych (seedy 1000-1029, sigma=0.0,
window_size = MNIEJSZA wartosc z WINDOW_SIZES danej domeny) -- zamrozone
w PREREG SS6, PRZED uruchomieniem run_controls na glownej siatce.

Raportowane SA WSZYSTKIE cztery metryki osobno (Z0, G_i, MC_continuous,
MC_binary-jako-0/1) -- nie tylko MC_continuous -- bo formula MC_continuous
uzywa (1-Z0), a Z0 NIE jest ograniczone do [0,1] z definicji (moze byc
>>1 dla sygnalow zdominowanych skladowa stala, patrz test_z0_large_for_
strong_dc w tests/), co jest ZNANYM, ODZIEDZICZONYM zniekstalceniem
formuly MC_continuous na realnych danych o duzym Z0 -- NIE naprawianym
tutaj (naprawa po zobaczeniu wyniku lamalaby dyscypline anty-numerologii),
tylko jawnie odnotowanym w wynikach.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow.
"""
from __future__ import annotations

import os
import sys
import time
from typing import Callable, Dict, List

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    run_controls,
    ControlResult,
    effect_size_label,
)
from core.zero_mode_topology_bridge import (  # noqa: E402
    zero_mode_fraction,
    calibrate_gi_ranges,
    g_i,
    mc_ms_g_continuous,
    mc_ms_g_binary,
    GiRanges,
)

from core.real_bearing_noise_robustness_bridge import (  # noqa: E402
    load_real_signals as load_bearing_signals,
    DEFECT_FILES as BEARING_DEFECT_FILES,
    make_real_window_injector,
)
from core.real_seismic_noise_robustness_bridge import (  # noqa: E402
    load_station,
    STATIONS,
    EVENT_IDX,
    make_region_injector,
)
from core.real_btc_noise_robustness_bridge import (  # noqa: E402
    load_log_returns,
    split_blocks_by_regime,
    make_regime_injector,
)

CALIB_SEEDS = range(1000, 1030)
SIGMAS = (0.0, 0.1, 0.3, 0.5, 1.0)
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05
W1 = 0.5
W3 = 0.5
GREF = 1.0


def calibrate_domain(
    pos_factory: Callable[[float, int], Callable],
    neg_factory: Callable[[float, int], Callable],
    calib_window_size: int,
):
    """GiRanges + theta0 (mediana Z0) + thetaG (mediana Gi) z MIESZANEJ
    puli 30+30 okien (pozytywne+negatywne), sigma=0.0, seedy 1000-1029,
    window_size = mniejsza wartosc z WINDOW_SIZES danej domeny -- 1:1
    z PREREG SS6."""
    pos_gen = pos_factory(0.0, calib_window_size)
    neg_gen = neg_factory(0.0, calib_window_size)
    pool = [pos_gen(calib_window_size, s) for s in CALIB_SEEDS] + \
           [neg_gen(calib_window_size, s) for s in CALIB_SEEDS]
    ranges = calibrate_gi_ranges(pool)
    z0_vals = [zero_mode_fraction(w) for w in pool]
    gi_vals = [g_i(w, ranges) for w in pool]
    theta0 = float(np.median(z0_vals))
    thetaG = float(np.median(gi_vals))
    return ranges, theta0, thetaG


def make_metric_fns(ranges: GiRanges, theta0: float, thetaG: float) -> Dict[str, Callable]:
    def _z0(w):
        return zero_mode_fraction(w)

    def _gi(w):
        return g_i(w, ranges)

    def _mc_cont(w):
        return mc_ms_g_continuous(zero_mode_fraction(w), g_i(w, ranges), W1, W3, GREF)

    def _mc_bin(w):
        return 1.0 if mc_ms_g_binary(zero_mode_fraction(w), g_i(w, ranges), theta0, thetaG) else 0.0

    return {"Z0": _z0, "Gi": _gi, "MC_continuous": _mc_cont, "MC_binary": _mc_bin}


def _bearing_domains():
    signals = load_bearing_signals()
    normal_sig = signals["normal"]
    out = []
    for defect_name in BEARING_DEFECT_FILES:
        defect_sig = signals[defect_name]
        out.append({
            "domain": "lozyska",
            "case": defect_name,
            "window_sizes": (32, 64),
            "calib_window_size": 32,
            "pos_factory": lambda sigma, ws, sig=defect_sig: make_real_window_injector(sig, sigma, ws),
            "neg_factory": lambda sigma, ws, sig=normal_sig: make_real_window_injector(sig, sigma, ws),
        })
    return out


def _seismic_domains():
    out = []
    for station in STATIONS:
        full = load_station(station)
        background = full[:EVENT_IDX]
        coda = full[EVENT_IDX:]
        out.append({
            "domain": "sejsmika",
            "case": station,
            "window_sizes": (64, 128),
            "calib_window_size": 64,
            "pos_factory": lambda sigma, ws, reg=coda: make_region_injector(reg, sigma, ws),
            "neg_factory": lambda sigma, ws, reg=background: make_region_injector(reg, sigma, ws),
        })
    return out


def _btc_domains():
    logret = load_log_returns()
    high, low = split_blocks_by_regime(logret)
    return [{
        "domain": "BTC",
        "case": "high_vs_low_vol",
        "window_sizes": (12, 24),
        "calib_window_size": 12,
        "pos_factory": lambda sigma, ws, b=high: make_regime_injector(b, sigma, ws),
        "neg_factory": lambda sigma, ws, b=low: make_regime_injector(b, sigma, ws),
    }]


def run_grid() -> List[Dict]:
    rows: List[Dict] = []
    for spec in _bearing_domains() + _seismic_domains() + _btc_domains():
        ranges, theta0, thetaG = calibrate_domain(
            spec["pos_factory"], spec["neg_factory"], spec["calib_window_size"]
        )
        metrics = make_metric_fns(ranges, theta0, thetaG)
        for window_size in spec["window_sizes"]:
            for sigma in SIGMAS:
                for metric_name, metric in metrics.items():
                    result: ControlResult = run_controls(
                        metric_fn=metric,
                        positive_injector=spec["pos_factory"](sigma, window_size),
                        negative_generator_a=spec["neg_factory"](sigma, window_size),
                        negative_generator_b=spec["neg_factory"](sigma, window_size),
                        n_windows=N_WINDOWS,
                        window_size=window_size,
                        seed=SEED,
                        alpha=ALPHA,
                    )
                    rows.append({
                        "domain": spec["domain"],
                        "case": spec["case"],
                        "metric": metric_name,
                        "window_size": window_size,
                        "sigma": sigma,
                        "theta0": theta0,
                        "thetaG": thetaG,
                        "passed": result.passed,
                        "reason": result.reason,
                        "pos_p": result.positive.pvalue,
                        "pos_r": result.positive.effect_size_r,
                        "pos_r_label": effect_size_label(result.positive.effect_size_r),
                        "med_test": result.positive.median_test,
                        "med_bg": result.positive.median_background,
                        "neg_p": result.negative.pvalue,
                        "neg_r": result.negative.effect_size_r,
                    })
    return rows


def format_report(rows: List[Dict]) -> str:
    lines = []
    lines.append(
        f"{'domena':>9} {'case':>13} {'metryka':>14} {'okno':>5} {'sigma':>6} "
        f"{'passed':>7} {'pos_p':>10} {'pos_r':>8} {'pos_r_lbl':>10} "
        f"{'med_test':>9} {'med_bg':>9} {'neg_p':>10} {'neg_r':>8}"
    )
    for r in rows:
        lines.append(
            f"{r['domain']:>9} {r['case']:>13} {r['metric']:>14} {r['window_size']:>5} "
            f"{r['sigma']:>6.2f} {str(r['passed']):>7} {r['pos_p']:>10.4g} "
            f"{r['pos_r']:>8.3f} {r['pos_r_label']:>10} {r['med_test']:>9.4g} "
            f"{r['med_bg']:>9.4g} {r['neg_p']:>10.4g} {r['neg_r']:>8.3f}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    rows = run_grid()
    dt = time.time() - t0
    print(format_report(rows))
    print(f"\nPRZESZLO OGOLEM: {sum(1 for r in rows if r['passed'])}/{len(rows)}")
    by_key: Dict[str, List[Dict]] = {}
    for r in rows:
        by_key.setdefault(f"{r['domain']}/{r['metric']}", []).append(r)
    for key, krows in sorted(by_key.items()):
        kp = sum(1 for r in krows if r["passed"])
        print(f"  {key}: {kp}/{len(krows)}")
    print(f"Czas: {dt:.1f}s")
