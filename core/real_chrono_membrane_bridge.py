# core/real_chrono_membrane_bridge.py
"""
real_chrono_membrane_bridge.py -- test glowny (PREREG SS6-7,
docs/geometry/PREREG_CHRONO_MEMBRANE_BEARING_v0.1.md) metryk
`spectral_concentration`/`participation_ratio`/`membrane_spectral_ratio`
(core/chrono_membrane_bridge.py) na WIELOKANALOWYCH realnych danych
lozysk CWRU (DE/FE/BA, wspolna os czasu wewnatrz jednego pliku NPZ,
ladowane przez TIMDR-Geometry-Formalism/timdr_geometry/
b4_bearing_data_gate.py::load_synchronous_cwru_channels -- BEZ zmian w
tym module, tylko konsumpcja gotowego, audytowanego loadera).

Uruchamiane WYLACZNIE po tym, jak core/chrono_membrane_bridge.py::
run_synthetic_controls() przeszlo (PASSED=True dla wszystkich komorek
N_CHANNELS x window_size) -- zgodnie z bramka kontrolna PREREG SS5/SS8.

Test PRIMARNY (PREREG SS6.1): N=2 (DE,FE), normal (1797_Normal.npz) vs
IR (1797_IR_21_DE12.npz) i vs OR@6 (1797_OR@6_21_DE12.npz), oddzielnie,
NIE mieszane. Test SEKUNDARNY (PREREG SS6.2), czysto diagnostyczny: N=3
(DE,FE,BA), IR vs OR@6 (fault vs fault, normal nie ma kanalu BA lokalnie
-- patrz docs/geometry/B4_BEARING_DATA_FREEZE.md).

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow -- wszystkie
stale (WINDOW_SIZES, N_WINDOWS, SEED) sa przeniesione 1:1 z PREREG SS6,
zamrozonej PRZED uruchomieniem tego pliku.
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
SEED = 0
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
# Segmentacja: nieprzecinajace sie okna, wspolne dla wszystkich kanalow
# jednego pliku (ta sama liczba probek na kazdym kanale -- gwarantowane
# przez load_synchronous_cwru_channels)
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
    seed: int = SEED,
) -> Dict:
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
    supported = result.pvalue < ALPHA and abs(result.effect_size_r) >= 0.3
    row.update({
        "status": "SUPPORTED" if supported else "NOT_SUPPORTED",
        "p": result.pvalue,
        "r": result.effect_size_r,
        "r_label": effect_size_label(result.effect_size_r),
        "median_pos": result.median_test,
        "median_neg": result.median_background,
    })
    return row


# =======================================================================
# 1. Test PRIMARNY: N=2 (DE,FE), normal vs fault (PREREG SS6.1)
# =======================================================================


def run_primary() -> List[Dict]:
    normal = load_synchronous_cwru_channels(NORMAL_FILE, required_channels=("DE", "FE"))
    faults = {
        "IR_21": load_synchronous_cwru_channels(IR_FILE, required_channels=("DE", "FE")),
        "OR6_21": load_synchronous_cwru_channels(OR6_FILE, required_channels=("DE", "FE")),
    }
    rows = []
    for fault_name, fault_data in faults.items():
        for window_size in WINDOW_SIZES:
            normal_pool = _segment_pool(normal.signals, ["DE", "FE"], window_size)
            fault_pool = _segment_pool(fault_data.signals, ["DE", "FE"], window_size)
            for metric_key in ("spectral_concentration", "participation_ratio", "membrane_spectral_ratio"):
                row = run_group_test(fault_pool, normal_pool, metric_key)
                row.update({
                    "fault": fault_name, "window_size": window_size, "metric": metric_key,
                    "n_avail_fault": len(fault_pool), "n_avail_normal": len(normal_pool),
                })
                rows.append(row)
    return rows


# =======================================================================
# 2. Test SEKUNDARNY, diagnostyczny: N=3 (DE,FE,BA), IR vs OR@6 (PREREG SS6.2)
# =======================================================================


def run_secondary() -> List[Dict]:
    ir = load_synchronous_cwru_channels(IR_FILE, required_channels=("DE", "FE", "BA"))
    or6 = load_synchronous_cwru_channels(OR6_FILE, required_channels=("DE", "FE", "BA"))
    rows = []
    for window_size in WINDOW_SIZES:
        ir_pool = _segment_pool(ir.signals, ["DE", "FE", "BA"], window_size)
        or6_pool = _segment_pool(or6.signals, ["DE", "FE", "BA"], window_size)
        for metric_key in ("spectral_concentration", "participation_ratio", "membrane_spectral_ratio"):
            row = run_group_test(ir_pool, or6_pool, metric_key)
            row.update({
                "window_size": window_size, "metric": metric_key,
                "n_avail_ir": len(ir_pool), "n_avail_or6": len(or6_pool),
            })
            rows.append(row)
    return rows


# =======================================================================
# 3. Stabilnosc znaku (PREREG SS6.1/SS7)
# =======================================================================


def sign_stability_report(primary_rows: List[Dict]) -> str:
    lines = ["## Stabilnosc znaku efektu (spectral_concentration, primarna metryka)", ""]
    for fault_name in ("IR_21", "OR6_21"):
        signs = []
        for row in primary_rows:
            if row["fault"] == fault_name and row["metric"] == "spectral_concentration":
                r = row.get("r")
                signs.append((row["window_size"], r))
        signs.sort()
        r_strs = ", ".join(f"w={w}:r={r:+.3f}" if r is not None else f"w={w}:n/a" for w, r in signs)
        valid_r = [r for _, r in signs if r is not None]
        stable = len({np.sign(r) for r in valid_r if r != 0}) <= 1 if valid_r else None
        lines.append(f"{fault_name}: {r_strs}  ->  ZNAK STABILNY={stable}")
    return "\n".join(lines)


# =======================================================================
# Raport
# =======================================================================


def format_report(rows: List[Dict], group_keys: List[str]) -> str:
    lines = []
    for row in rows:
        p_str = f"{row['p']:.4g}" if row['p'] is not None else "n/a"
        r_str = f"{row['r']:.3f}" if row['r'] is not None else "n/a"
        r_lbl = row.get('r_label', 'n/a')
        key_str = " ".join(f"{row[k]}" for k in group_keys)
        lines.append(
            f"{key_str:>30} okno={row['window_size']:>4} metryka={row['metric']:>24} "
            f"status={row['status']:>14} p={p_str:>10} r={r_str:>7} ({r_lbl:>7}) "
            f"n_valid_pos={row['n_valid_pos']:>3} n_valid_neg={row['n_valid_neg']:>3}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    primary_rows = run_primary()
    secondary_rows = run_secondary()
    dt = time.time() - t0

    print("=== TEST PRIMARNY: N=2 (DE,FE), normal vs fault ===")
    print(format_report(primary_rows, ["fault"]))
    print()
    print(sign_stability_report(primary_rows))
    print()
    print("=== TEST SEKUNDARNY (diagnostyczny): N=3 (DE,FE,BA), IR vs OR@6 ===")
    print(format_report(secondary_rows, []))

    print(f"\nCzas: {dt:.1f}s")
