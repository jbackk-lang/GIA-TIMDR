# core/real_chrono_membrane_bridge_v0_2.py
"""
real_chrono_membrane_bridge_v0_2.py -- test v0.2 (PREREG SS1-4,
docs/geometry/PREREG_CHRONO_MEMBRANE_BEARING_v0.2.md) ODWROCONEGO
kierunku (normal > fault w `spectral_concentration`, patrz v0.1 SS7
"co zostaje otwarte") na CZASOWO ODOSOBNIONEJ drugiej polowie kazdego
z trzech plikow CWRU.

Konstrukcja (channel_correlation_matrix, spectrum_from_correlation,
spectral_concentration, membrane_window_metrics) jest 1:1 z
core/chrono_membrane_bridge.py, BEZ ZMIAN -- ten plik tylko dzieli
kazde nagranie na dwie nienachodzace sie polowy (pierwsza=kalibracja,
NIE rozstrzygajaca; druga=test, JEDYNA czesc liczaca sie jako wynik) i
uruchamia Manna-Whitneya osobno na kazdej polowie.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow na drugiej
polowie -- wszystkie stale (WINDOW_SIZES, N_WINDOWS, SEED_CALIBRATION,
SEED_TEST) sa przeniesione 1:1 z zamrozonej PREREG SS3.
"""
from __future__ import annotations

import os
import sys
import time
from typing import Dict, List

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
_GEOMETRY_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Geometry-Formalism")
_SIBLING_ROOT = os.path.dirname(_REPO_ROOT)
for _p in (_REPO_ROOT, _MATH_FORMALISM, _GEOMETRY_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import mann_whitney_test, effect_size_label  # noqa: E402
from timdr_geometry.b4_bearing_data_gate import load_synchronous_cwru_channels  # noqa: E402
from core.chrono_membrane_bridge import membrane_window_metrics  # noqa: E402

WINDOW_SIZES = (128, 256, 512)
N_WINDOWS = 30
SEED_CALIBRATION = 0
SEED_TEST = 100
ALPHA = 0.05
MIN_VALID_PER_GROUP = 10

_BEARING_DIR = os.path.join(
    _SIBLING_ROOT, "TIMDR-Industrial-Predict", "data", "cwru_bearing",
    "b4_raw", "source_mirror", "Data", "1797 RPM",
)
NORMAL_FILE = os.path.join(_BEARING_DIR, "1797_Normal.npz")
IR_FILE = os.path.join(_BEARING_DIR, "1797_IR_21_DE12.npz")
OR6_FILE = os.path.join(_BEARING_DIR, "1797_OR@6_21_DE12.npz")


# ---------------------------------------------------------------------
# PREREG SS3.2: podzial kazdego kanalu na dwie nienachodzace sie polowy
# ---------------------------------------------------------------------


def split_signals_in_half(signals: Dict[str, np.ndarray]) -> tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """Zwraca (first_half, second_half) -- podzial PRZED segmentacja na
    okna, wiec zadne okno nie przecina granicy polowy."""
    lengths = {len(v) for v in signals.values()}
    if len(lengths) != 1:
        raise ValueError("kanaly musza miec identyczna dlugosc")
    n = lengths.pop()
    half = n // 2
    first = {ch: sig[:half] for ch, sig in signals.items()}
    second = {ch: sig[half:] for ch, sig in signals.items()}
    return first, second


# ---------------------------------------------------------------------
# Segmentacja: nieprzecinajace sie okna (identyczna logika co
# core/real_chrono_membrane_bridge.py::_segment_pool, przeniesiona 1:1)
# ---------------------------------------------------------------------


def _segment_pool(signals: Dict[str, np.ndarray], channels: List[str], window_size: int) -> List[List[np.ndarray]]:
    n = len(signals[channels[0]])
    n_avail = n // window_size
    pool = []
    for i in range(n_avail):
        seg = [signals[ch][i * window_size:(i + 1) * window_size] for ch in channels]
        pool.append(seg)
    return pool


def _sample_windows(pool: List[List[np.ndarray]], n_windows: int, seed: int) -> List[List[np.ndarray]]:
    rng = np.random.default_rng(seed)
    n_avail = len(pool)
    if n_avail >= n_windows:
        idx = rng.choice(n_avail, size=n_windows, replace=False)
    else:
        idx = rng.integers(0, n_avail, size=n_windows)  # reuzycie, odnotowane w raporcie
    return [pool[i] for i in idx]


def _valid(values: np.ndarray) -> np.ndarray:
    return values[~np.isnan(values)]


def run_group_test(
    pos_pool: List[List[np.ndarray]],
    neg_pool: List[List[np.ndarray]],
    metric_key: str,
    n_windows: int = N_WINDOWS,
    seed: int = SEED_CALIBRATION,
) -> Dict:
    """pos = normal (PREREG SS3.4 -- odwrocone wzgledem v0.1, zeby r>0
    odpowiadalo wprost przewidywaniu normal>fault tej sesji)."""
    pos_windows = _sample_windows(pos_pool, n_windows, seed)
    neg_windows = _sample_windows(neg_pool, n_windows, seed + 1)

    pos_vals = np.array([membrane_window_metrics(w)[metric_key] for w in pos_windows])
    neg_vals = np.array([membrane_window_metrics(w)[metric_key] for w in neg_windows])
    pos_valid = _valid(pos_vals)
    neg_valid = _valid(neg_vals)

    row = {
        "n_valid_pos": len(pos_valid),
        "n_valid_neg": len(neg_valid),
        "n_total": n_windows,
    }
    if len(pos_valid) < MIN_VALID_PER_GROUP or len(neg_valid) < MIN_VALID_PER_GROUP:
        row.update({"status": "INCONCLUSIVE", "p": None, "r": None,
                     "median_pos": None, "median_neg": None})
        return row

    result = mann_whitney_test(pos_valid, neg_valid)
    confirmed = result.pvalue < ALPHA and abs(result.effect_size_r) >= 0.3 and result.effect_size_r > 0
    row.update({
        "status": "SUPPORTED" if confirmed else "NOT_SUPPORTED",
        "p": result.pvalue,
        "r": result.effect_size_r,
        "r_label": effect_size_label(result.effect_size_r),
        "median_pos": result.median_test,
        "median_neg": result.median_background,
    })
    return row


# =======================================================================
# Test PRIMARNY (v0.2): N=2 (DE,FE), normal vs fault, PIERWSZA (kalibracja)
# i DRUGA (test, rozstrzygajaca) polowa kazdego pliku osobno
# =======================================================================


def run_split_half(seed: int, half_name: str) -> List[Dict]:
    normal_full = load_synchronous_cwru_channels(NORMAL_FILE, required_channels=("DE", "FE"))
    faults_full = {
        "IR_21": load_synchronous_cwru_channels(IR_FILE, required_channels=("DE", "FE")),
        "OR6_21": load_synchronous_cwru_channels(OR6_FILE, required_channels=("DE", "FE")),
    }

    normal_first, normal_second = split_signals_in_half(normal_full.signals)
    normal_half_signals = normal_first if half_name == "calibration" else normal_second

    rows = []
    for fault_name, fault_data in faults_full.items():
        fault_first, fault_second = split_signals_in_half(fault_data.signals)
        fault_half_signals = fault_first if half_name == "calibration" else fault_second

        for window_size in WINDOW_SIZES:
            normal_pool = _segment_pool(normal_half_signals, ["DE", "FE"], window_size)
            fault_pool = _segment_pool(fault_half_signals, ["DE", "FE"], window_size)
            row = run_group_test(normal_pool, fault_pool, "spectral_concentration", seed=seed)
            row.update({
                "half": half_name, "fault": fault_name, "window_size": window_size,
                "metric": "spectral_concentration",
                "n_avail_normal": len(normal_pool), "n_avail_fault": len(fault_pool),
            })
            rows.append(row)
    return rows


def sign_stability_report(rows: List[Dict], half_name: str) -> str:
    lines = [f"## Stabilnosc znaku efektu -- polowa={half_name}", ""]
    for fault_name in ("IR_21", "OR6_21"):
        signs = []
        for row in rows:
            if row["half"] == half_name and row["fault"] == fault_name:
                signs.append((row["window_size"], row.get("r")))
        signs.sort()
        r_strs = ", ".join(f"w={w}:r={r:+.3f}" if r is not None else f"w={w}:n/a" for w, r in signs)
        valid_r = [r for _, r in signs if r is not None]
        stable_positive = all(r > 0 for r in valid_r) if valid_r else None
        lines.append(f"{fault_name}: {r_strs}  ->  WSZYSTKIE r>0 (normal>fault, stabilny)={stable_positive}")
    return "\n".join(lines)


def format_report(rows: List[Dict]) -> str:
    lines = []
    for row in rows:
        p_str = f"{row['p']:.4g}" if row['p'] is not None else "n/a"
        r_str = f"{row['r']:.3f}" if row['r'] is not None else "n/a"
        r_lbl = row.get('r_label', 'n/a')
        lines.append(
            f"polowa={row['half']:>11} fault={row['fault']:>7} okno={row['window_size']:>4} "
            f"status={row['status']:>14} p={p_str:>10} r={r_str:>7} ({r_lbl:>7}) "
            f"n_valid_normal={row['n_valid_pos']:>3} n_valid_fault={row['n_valid_neg']:>3} "
            f"n_avail_normal={row['n_avail_normal']:>4} n_avail_fault={row['n_avail_fault']:>4}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    calibration_rows = run_split_half(seed=SEED_CALIBRATION, half_name="calibration")
    test_rows = run_split_half(seed=SEED_TEST, half_name="test")
    dt = time.time() - t0

    print("=== PIERWSZA POLOWA (KALIBRACJA -- NIE rozstrzygajaca, patrz PREREG SS1/SS4) ===")
    print(format_report(calibration_rows))
    print()
    print(sign_stability_report(calibration_rows, "calibration"))
    print()
    print("=== DRUGA POLOWA (TEST -- JEDYNA czesc rozstrzygajaca, PREREG SS4) ===")
    print(format_report(test_rows))
    print()
    print(sign_stability_report(test_rows, "test"))

    print(f"\nCzas: {dt:.1f}s")
