# core/stress_test_sieve.py
"""
stress_test_sieve.py -- audyt odpornosci "sita" (timdr_formalism.pipeline)
i piatki metryk zbudowanych 2026-09-15 (trefoil_ms_bridge, winding_
crossing_ms_bridge, persistent_homology_ms_bridge, phase_winding_oam_
ms_bridge), na propozycje uzytkownika: nakarmic sito sygnalami
adwersarialnymi i zobaczyc efekt przepelnienia.

TO NIE JEST test hipotezy o TIMDR (jak PREREG_*/RESULT_* wczesniej) --
to test odpornosci WLASNEGO KODU, w duchu audytow z wczesniejszej czesci
sesji (test_operators_wiring.py, phase diagram SG-Coupling, ktore
znalazly realny blad przepelnienia R_phase[S]).

Trzy czesci:
  A) Kalibracja sita pod czystym zerem -- empiryczny odsetek falszywie
     pozytywnych "passed" przy TRZECH generatorach o identycznym
     rozkladzie (prawdziwie zerowy efekt), porownany z wartoscia
     teoretyczna alpha*(1-alpha).
  B) Bateria sygnalow adwersarialnych przez wszystkie 5 metric_fn --
     zera, stale, ekstremalne amplitudy, NaN/Inf, bardzo krotkie okna,
     skok pojedynczy, fala prostokatna.
  C) Zdegenerowany metric_fn (stala/NaN/losowy niezwiazany z danymi)
     wprost przez pipeline.run_controls -- co sito z tym robi.
"""
from __future__ import annotations

import os
import sys
import time
import warnings
from typing import Callable, List, Dict

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import run_controls, mann_whitney_test  # noqa: E402

from core.trefoil_ms_bridge import metric_fn as torsion_metric  # noqa: E402
from core.winding_crossing_ms_bridge import (  # noqa: E402
    winding_metric_fn, crossing_metric_fn,
)
from core.persistent_homology_ms_bridge import h1_total_persistence_fn  # noqa: E402
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa: E402

METRICS: Dict[str, Callable[[np.ndarray], float]] = {
    "torsion_max|tau|": torsion_metric,
    "winding_number": winding_metric_fn,
    "crossing_number": crossing_metric_fn,
    "h1_persistence": h1_total_persistence_fn,
    "phase_winding": phase_winding_fn,
}

# ---------------------------------------------------------------------
# A) Kalibracja sita pod czystym zerem (prawdziwie zerowy efekt)
# ---------------------------------------------------------------------


def calibration_under_true_null(n_trials: int = 200, window_size: int = 64) -> Dict:
    """TRZY generatory o IDENTYCZNYM rozkladzie (biale, ten sam sigma) --
    genuine zerowy efekt z konstrukcji. `passed` powinno wychodzic z
    czestoscia ok. alpha*(1-alpha)=0.0475, NIE 0 i NIE duzo wiecej."""
    def null_gen(window_size: int, seed) -> np.ndarray:
        rng = np.random.default_rng(seed)
        return rng.normal(0.0, 1.0, window_size)

    metric = winding_metric_fn  # dowolna z 5, uzyta jako reprezentatywna
    n_passed = 0
    outer_rng = np.random.default_rng(12345)
    for i in range(n_trials):
        seed = int(outer_rng.integers(0, 2**31 - 1))
        result = run_controls(
            metric_fn=metric,
            positive_injector=null_gen,
            negative_generator_a=null_gen,
            negative_generator_b=null_gen,
            n_windows=30,
            window_size=window_size,
            seed=seed,
            alpha=0.05,
        )
        if result.passed:
            n_passed += 1
    empirical_rate = n_passed / n_trials
    theoretical_rate = 0.05 * (1 - 0.05)
    return {
        "n_trials": n_trials,
        "n_passed": n_passed,
        "empirical_rate": empirical_rate,
        "theoretical_rate": theoretical_rate,
    }


# ---------------------------------------------------------------------
# B) Bateria sygnalow adwersarialnych
# ---------------------------------------------------------------------


def adversarial_signals() -> Dict[str, np.ndarray]:
    t = np.arange(300, dtype=float)
    sig: Dict[str, np.ndarray] = {}
    sig["zeros_300"] = np.zeros(300)
    sig["constant_nonzero_300"] = np.full(300, 5.0)
    sig["huge_amplitude_1e150"] = np.sin(t) * 1e150
    sig["tiny_amplitude_1e-150"] = np.sin(t) * 1e-150
    sig["nan_injected"] = np.sin(t).copy()
    sig["nan_injected"][150] = np.nan
    sig["inf_injected"] = np.sin(t).copy()
    sig["inf_injected"][150] = np.inf
    spike = np.zeros(300)
    spike[150] = 1e20
    sig["single_huge_spike"] = spike
    sig["square_wave"] = np.sign(np.sin(t))
    sig["very_short_n4"] = np.array([1.0, 2.0, 1.0, 2.0])
    sig["very_short_n3"] = np.array([1.0, -1.0, 1.0])
    sig["very_long_n5000"] = np.sin(np.arange(5000, dtype=float) * 0.1)
    sig["all_nan"] = np.full(300, np.nan)
    return sig


def run_adversarial_battery() -> List[Dict]:
    rows = []
    signals = adversarial_signals()
    for sig_name, sig in signals.items():
        for metric_name, metric in METRICS.items():
            t0 = time.time()
            status = "OK"
            value = None
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                try:
                    value = metric(sig)
                except Exception as e:  # noqa: BLE001
                    status = f"EXCEPTION: {type(e).__name__}: {e}"
                dt = time.time() - t0
                n_warn = len(caught)
            finite = np.isfinite(value) if isinstance(value, (int, float)) else None
            rows.append({
                "signal": sig_name,
                "metric": metric_name,
                "status": status,
                "value": value,
                "finite": finite,
                "time_s": round(dt, 4),
                "n_warnings": n_warn,
            })
    return rows


# ---------------------------------------------------------------------
# C) Zdegenerowany metric_fn wprost przez pipeline
# ---------------------------------------------------------------------


def degenerate_metric_through_pipeline() -> List[Dict]:
    def gen(window_size: int, seed) -> np.ndarray:
        rng = np.random.default_rng(seed)
        return rng.normal(0.0, 1.0, window_size)

    def gen2(window_size: int, seed) -> np.ndarray:
        rng = np.random.default_rng(seed)
        return rng.normal(0.5, 1.0, window_size)  # lekko przesuniete od gen

    constant_metric = lambda x: 42.0  # noqa: E731
    always_nan_metric = lambda x: float("nan")  # noqa: E731

    rng = np.random.default_rng(0)
    def random_unrelated_metric(x: np.ndarray) -> float:
        return float(rng.normal())

    rows = []
    for name, metric in (
        ("stala_42", constant_metric),
        ("zawsze_nan", always_nan_metric),
        ("losowa_niezwiazana_z_danymi", random_unrelated_metric),
    ):
        try:
            result = run_controls(
                metric_fn=metric,
                positive_injector=gen2,
                negative_generator_a=gen,
                negative_generator_b=gen,
                n_windows=30,
                window_size=64,
                seed=0,
                alpha=0.05,
            )
            rows.append({
                "metric": name,
                "status": "OK",
                "passed": result.passed,
                "pos_p": result.positive.pvalue,
                "neg_p": result.negative.pvalue,
                "reason": result.reason,
            })
        except Exception as e:  # noqa: BLE001
            rows.append({
                "metric": name,
                "status": f"EXCEPTION: {type(e).__name__}: {e}",
                "passed": None, "pos_p": None, "neg_p": None, "reason": None,
            })
    return rows


if __name__ == "__main__":
    print("=== A) Kalibracja sita pod czystym zerem (200 przebiegow) ===")
    calib = calibration_under_true_null()
    print(f"n_trials={calib['n_trials']}  n_passed={calib['n_passed']}  "
          f"empiryczny odsetek={calib['empirical_rate']:.4f}  "
          f"teoretyczny alpha*(1-alpha)={calib['theoretical_rate']:.4f}")

    print("\n=== B) Bateria sygnalow adwersarialnych (5 metryk x 12 sygnalow) ===")
    rows = run_adversarial_battery()
    for r in rows:
        val_str = f"{r['value']:.4g}" if isinstance(r['value'], (int, float)) and r['value'] is not None else str(r['value'])
        print(f"{r['signal']:<24} {r['metric']:<18} {r['status']:<12} "
              f"val={val_str:<12} finite={str(r['finite']):<6} "
              f"t={r['time_s']:.3f}s  warn={r['n_warnings']}")

    print("\n=== C) Zdegenerowany metric_fn przez pipeline ===")
    deg_rows = degenerate_metric_through_pipeline()
    for r in deg_rows:
        print(r)
