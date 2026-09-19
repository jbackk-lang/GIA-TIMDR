# core/real_ms_k_zero_mode_bridge.py
"""
real_ms_k_zero_mode_bridge.py -- implementacja PRE-REJESTROWANEJ
(docs/geometry/PREREG_MS_K_BRIDGE_2.md, zadanie #69) kontroli
pozytywnej/negatywnej dla kandydujacego (NIE ustalonego) mostu
MC_{M/S<->K} #2 (tlumienie trybu zerowego Z0 vs pierwsza istotna
czestotliwosc omega1) na TRZECH realnych domenach: lozyska CWRU,
sejsmika Ridgecrest, BTC/USD.

Zero nowej ekstrakcji -- reuzyte 1:1 dominant_omega1/calibrate_omega_ref
z core/real_mobius_kg_bridge.py (most MC_K<->G) i zero_mode_fraction z
core/zero_mode_topology_bridge.py (most MC_M/S<->G #1). Jedyny nowy
kod to KOMBINACJA tych dwoch juz istniejacych, juz zweryfikowanych
wielkosci.

Z0_norm = Z0/(Z0+1) -- naprawa PROAKTYWNA (nie po zobaczeniu wyniku TEGO
mostu) znanego, nienaprawionego zniekstalcenia z mostu macierzystego
MC_M/S<->G #1 (Z0 nieograniczone psuje (1-Z0) w wersji ciaglej) --
decyzja podjeta w PREREG, PRZED dotknieciem danych tego mostu.

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
_TIME_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Time-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM, _TIME_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    run_controls,
    ControlResult,
    effect_size_label,
)
from core.real_mobius_kg_bridge import dominant_omega1, calibrate_omega_ref  # noqa: E402
from core.zero_mode_topology_bridge import zero_mode_fraction  # noqa: E402

from core.real_bearing_noise_robustness_bridge import (  # noqa: E402
    load_real_signals as load_bearing_signals,
    DEFECT_FILES as BEARING_DEFECT_FILES,
    make_real_window_injector,
)
from core.real_seismic_noise_robustness_bridge import (  # noqa: E402
    load_station,
    STATIONS,
    EVENT_IDX,
    FS as SEISMIC_FS,
    make_region_injector,
)
from core.real_btc_noise_robustness_bridge import (  # noqa: E402
    load_log_returns,
    split_blocks_by_regime,
    make_regime_injector,
)

EPS = 1e-9
CALIB_SEEDS = range(1000, 1030)
SIGMAS = (0.0, 0.1, 0.3, 0.5, 1.0)
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05
W1 = 0.5
W2 = 0.5

BEARING_FS = 12000.0
SEISMIC_FS_HZ = SEISMIC_FS
BTC_FS = 1.0


def z0_norm(window: np.ndarray) -> float:
    """Z0_norm = Z0/(Z0+1) in [0,1) -- naprawa proaktywna, patrz naglowek
    modulu. Zamrozone w PREREG_MS_K_BRIDGE_2.md SS6, PRZED danymi."""
    z0 = zero_mode_fraction(window)
    return z0 / (z0 + 1.0)


def mc_continuous(window: np.ndarray, fs: float, omega_ref: float) -> float:
    omega1 = dominant_omega1(window, fs)
    return W1 * (1.0 - z0_norm(window)) + W2 * (omega1 / omega_ref)


def mc_binary(window: np.ndarray, fs: float, omega_ref: float, theta0: float) -> float:
    z0 = zero_mode_fraction(window)
    omega1 = dominant_omega1(window, fs)
    return 1.0 if (z0 < theta0 and omega1 > omega_ref) else 0.0


def calibrate_theta0(
    pos_factory: Callable[[float, int], Callable],
    neg_factory: Callable[[float, int], Callable],
    calib_window_size: int,
) -> float:
    """theta0 := mediana(Z0) na MIESZANEJ puli 30 okien pozytywnych + 30
    negatywnych, seedy 1000-1029, sigma=0.0 -- dziedziczona konwencja
    kalibracji Z0/theta0 z MC_M/S<->G #1 (PREREG SS5), bez zmian."""
    pos_gen = pos_factory(0.0, calib_window_size)
    neg_gen = neg_factory(0.0, calib_window_size)
    pool = [pos_gen(calib_window_size, s) for s in CALIB_SEEDS] + \
           [neg_gen(calib_window_size, s) for s in CALIB_SEEDS]
    z0_vals = [zero_mode_fraction(w) for w in pool]
    return float(np.median(z0_vals))


def _bearing_domains():
    signals = load_bearing_signals()
    normal_sig = signals["normal"]
    out = []
    for defect_name in BEARING_DEFECT_FILES:
        defect_sig = signals[defect_name]
        out.append({
            "domain": "lozyska",
            "case": defect_name,
            "fs": BEARING_FS,
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
            "fs": SEISMIC_FS_HZ,
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
        "fs": BTC_FS,
        "window_sizes": (12, 24),
        "calib_window_size": 12,
        "pos_factory": lambda sigma, ws, b=high: make_regime_injector(b, sigma, ws),
        "neg_factory": lambda sigma, ws, b=low: make_regime_injector(b, sigma, ws),
    }]


def run_grid() -> List[Dict]:
    rows: List[Dict] = []
    for spec in _bearing_domains() + _seismic_domains() + _btc_domains():
        fs = spec["fs"]
        omega_ref = calibrate_omega_ref(spec["neg_factory"], spec["calib_window_size"], fs)
        theta0 = calibrate_theta0(spec["pos_factory"], spec["neg_factory"], spec["calib_window_size"])

        metrics = {
            "MC_continuous": lambda w, fs=fs, oref=omega_ref: mc_continuous(w, fs, oref),
            "MC_binary": lambda w, fs=fs, oref=omega_ref, t0=theta0: mc_binary(w, fs, oref, t0),
        }

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
                        "omega_ref": omega_ref,
                        "theta0": theta0,
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

    main_rows = [r for r in rows if r["metric"] == "MC_continuous"]
    bin_rows = [r for r in rows if r["metric"] == "MC_binary"]
    print(f"\nMC_continuous (GLOWNY TEST): {sum(1 for r in main_rows if r['passed'])}/{len(main_rows)}")
    print(f"MC_binary (DODATKOWY, diagnostyczny): {sum(1 for r in bin_rows if r['passed'])}/{len(bin_rows)}")

    by_key: Dict[str, List[Dict]] = {}
    for r in rows:
        by_key.setdefault(f"{r['domain']}/{r['metric']}", []).append(r)
    for key, krows in sorted(by_key.items()):
        kp = sum(1 for r in krows if r["passed"])
        print(f"  {key}: {kp}/{len(krows)}")
    print(f"Czas: {dt:.1f}s")
