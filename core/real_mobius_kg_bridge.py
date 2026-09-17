# core/real_mobius_kg_bridge.py
"""
real_mobius_kg_bridge.py -- implementacja PRE-REJESTROWANEJ
(docs/geometry/PREREG_MOBIUS_COHERENCE_BRIDGES.md, zadanie #64) kontroli
pozytywnej/negatywnej dla kandydujacego (NIE ustalonego) mostu G<->K
(core/mobius_kg_bridge.py, MC_{K<->G}(k,n)=T(k,n)*(omega_{k,n}/omega_ref))
na TRZECH realnych domenach: lozyska CWRU, sejsmika Ridgecrest, BTC/USD.

Zero nowych danych/generatorow/siatek -- wszystko reuzyte 1:1 z trzech
istniejacych mostow M/S<->topologia/K (core/real_{bearing,seismic,btc}_
noise_robustness_bridge.py). Jedyny nowy element: ekstrakcja omega1
(pierwsza istotna czestotliwosc, juz zweryfikowany most Fouriera M/S<->K
z TIMDR-Time-Formalism), kalibracja omega_ref z tla (seedy 1000-1029,
mediana, PRZED porownaniem pozytywna/negatywna), i binarny wskaznik
"czy najblizszy punkt kratownicy Mobiusa jest dopuszczalny".

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow -- wszystkie
wybory sa przeniesione 1:1 z zamrozonej pre-rejestracji.
"""
from __future__ import annotations

import math
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
from timdr_time.fourier_bridge import fft_modalities  # noqa: E402
from core.mobius_kg_bridge import is_allowed, omega_kn, nearest_lattice_point  # noqa: E402

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

# ---------------------------------------------------------------------
# Siatka kratownicy Mobiusa (zamrozona, identyczna z tests/test_mobius_kg_bridge.py)
# ---------------------------------------------------------------------

K_RANGE = range(-6, 7)
N_RANGE = range(1, 8)

# Czestotliwosc probkowania per domena. Lozyska: 1797 RPM, kanal DE, 12 kHz
# (TIMDR-Industrial-Predict/README.md). Sejsmika: 100 Hz (stala FS z mostu
# realnego sejsmicznego). BTC: BRAK fizycznej jednostki czasu -- fs=1.0
# przyjete UMOWNIE (dt=1 probka), zastrzezenie explicite w PREREG SS7.1,
# wynik na tej domenie traktowany jako najslabszy dowodowo.
BEARING_FS = 12000.0
SEISMIC_FS_HZ = SEISMIC_FS
BTC_FS = 1.0

CALIB_SEEDS = range(1000, 1030)


def dominant_omega1(window: np.ndarray, fs: float) -> float:
    """omega1 = 2*pi*f1, f1 = czestotliwosc modalnosci o najwiekszej
    amplitudzie z fft_modalities (most Fouriera M/S<->K, juz zweryfikowany
    10/10 testow -- zero nowej transformaty). include_dc=False (DC nie
    jest 'czestotliwoscia', patrz docstring fft_modalities)."""
    modalities, _ = fft_modalities(window, dt=1.0 / fs, include_dc=False)
    if not modalities:
        return 0.0
    f1 = max(modalities, key=lambda m: m.A).f
    return 2.0 * math.pi * f1


def make_mc_k_g_indicator(fs: float, omega_ref: float) -> Callable[[np.ndarray], float]:
    """Zwraca metric_fn(window)->1.0/0.0: 1.0 jesli najblizszy punkt
    kratownicy (k,n) (w K_RANGE x N_RANGE, wzgledem omega1/omega_ref) jest
    dopuszczalny na Mobiusie, 0.0 w przeciwnym razie."""
    def _metric(window: np.ndarray) -> float:
        omega1 = dominant_omega1(window, fs)
        x = omega1 / omega_ref
        k, n = nearest_lattice_point(x, K_RANGE, N_RANGE)
        return 1.0 if is_allowed(k, n) else 0.0
    return _metric


def calibrate_omega_ref(
    neg_generator_factory: Callable[[float, int], Callable], window_size: int, fs: float
) -> float:
    """omega_ref := mediana(omega1) na 30 oknach klasy negatywnej (tlo),
    sigma=0.0, seedy 1000-1029 (rozlaczne od puli testowej 0-29) --
    zamrozone w PREREG SS5, liczone RAZ przed run_controls."""
    gen = neg_generator_factory(0.0, window_size)
    vals = []
    for seed in CALIB_SEEDS:
        window = gen(window_size, seed)
        vals.append(dominant_omega1(window, fs))
    return float(np.median(vals))


# ---------------------------------------------------------------------
# Definicje trzech domen (zero nowych danych/generatorow -- importy powyzej)
# ---------------------------------------------------------------------

SIGMAS = (0.0, 0.1, 0.3, 0.5, 1.0)
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05


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
        "pos_factory": lambda sigma, ws, b=high: make_regime_injector(b, sigma, ws),
        "neg_factory": lambda sigma, ws, b=low: make_regime_injector(b, sigma, ws),
    }]


def run_grid() -> List[Dict]:
    rows: List[Dict] = []
    for spec in _bearing_domains() + _seismic_domains() + _btc_domains():
        fs = spec["fs"]
        for window_size in spec["window_sizes"]:
            omega_ref = calibrate_omega_ref(spec["neg_factory"], window_size, fs)
            metric = make_mc_k_g_indicator(fs, omega_ref)
            for sigma in SIGMAS:
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
                    "window_size": window_size,
                    "sigma": sigma,
                    "omega_ref": omega_ref,
                    "passed": result.passed,
                    "reason": result.reason,
                    "pos_p": result.positive.pvalue,
                    "pos_r": result.positive.effect_size_r,
                    "pos_r_label": effect_size_label(result.positive.effect_size_r),
                    "pos_frac_test": result.positive.median_test,
                    "pos_frac_bg": result.positive.median_background,
                    "neg_p": result.negative.pvalue,
                    "neg_r": result.negative.effect_size_r,
                })
    return rows


def format_report(rows: List[Dict]) -> str:
    lines = []
    lines.append(
        f"{'domena':>9} {'case':>13} {'okno':>5} {'sigma':>6} {'omega_ref':>10} "
        f"{'passed':>7} {'pos_p':>10} {'pos_r':>8} {'pos_r_lbl':>10} "
        f"{'frac_test':>9} {'frac_bg':>8} {'neg_p':>10} {'neg_r':>8}"
    )
    for r in rows:
        lines.append(
            f"{r['domain']:>9} {r['case']:>13} {r['window_size']:>5} "
            f"{r['sigma']:>6.2f} {r['omega_ref']:>10.4f} {str(r['passed']):>7} "
            f"{r['pos_p']:>10.4g} {r['pos_r']:>8.3f} {r['pos_r_label']:>10} "
            f"{r['pos_frac_test']:>9.3f} {r['pos_frac_bg']:>8.3f} "
            f"{r['neg_p']:>10.4g} {r['neg_r']:>8.3f}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    rows = run_grid()
    dt = time.time() - t0
    print(format_report(rows))
    n_pass = sum(1 for r in rows if r["passed"])
    by_domain: Dict[str, List[Dict]] = {}
    for r in rows:
        by_domain.setdefault(r["domain"], []).append(r)
    print(f"\nPRZESZLO OGOLEM: {n_pass}/{len(rows)}")
    for dom, drows in by_domain.items():
        dp = sum(1 for r in drows if r["passed"])
        print(f"  {dom}: {dp}/{len(drows)}")
    print(f"Czas: {dt:.1f}s")
