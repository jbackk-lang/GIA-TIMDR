# core/real_chrono_membrane_bridge_independent.py
"""
real_chrono_membrane_bridge_independent.py -- NIEZALEZNY test
potwierdzajacy hipotezy `spectral_concentration: normal > fault`
(zamrozonej i potwierdzonej dwukrotnie na 1797 RPM -- v0.1
docs/geometry/RESULT_CHRONO_MEMBRANE_BEARING_v0.1.md SS3.1 (obserwacja
post-hoc) i v0.2 docs/geometry/RESULT_CHRONO_MEMBRANE_BEARING_v0.2.md
(formalne SUPPORTED na czasowo odosobnionej drugiej polowie)) na
PRAWDZIWIE swiezych danych.

KONSTRUKCJA (channel_correlation_matrix, spectrum_from_correlation,
spectral_concentration, membrane_window_metrics) jest 1:1 z
core/chrono_membrane_bridge.py, BEZ ZMIAN. Rozmiary okna, N_WINDOWS,
ALPHA, MIN_VALID_PER_GROUP i kryterium SUPPORTED/NOT_SUPPORTED sa 1:1
przeniesione z core/real_chrono_membrane_bridge_v0_2.py -- ZAMROZONA
metodologia, TA sesja jej NIE zmienia.

CO JEST TU NAPRAWDE NOWE (jedyna zmiana wzgledem v0.1/v0.2):
  1. Dwa RPM nigdy wczesniej nie testowane lokalnie: 1730, 1750 (v0.1/
     v0.2 uzywaly WYLACZNIE 1797 RPM).
  2. Typy uszkodzenia inne niz jedyne dotad testowane IR/OR@6 -- tutaj
     B (kulka), IR, OR@3, OR@6 (wsrod uszkodzen ROZNE pozycje zegara).
  3. Rozmiary uszkodzenia inne niz jedyne dotad testowane 21 mils --
     tutaj 7, 14, 21 mils.
  4. Pliki NPZ pochodza z zupelnie innego archiwum
     (CWRU_Bearing_NumPy_4LUM, dostarczonego przez uzytkownika), NIE z
     lokalnego mirrora TIMDR-Industrial-Predict uzywanego w v0.1/v0.2.

Pliki WYBRANE PRZED uruchomieniem testu (patrz docstring `SELECTED_FILES`
nizej dla pelnego uzasadnienia) -- zaden plik nie zostal dobrany ani
odrzucony po zobaczeniu jakiegokolwiek wyniku tej sesji.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow -- wszystkie
stale (WINDOW_SIZES, N_WINDOWS, SEED, ALPHA, kryterium SUPPORTED) sa
przeniesione 1:1 z juz zamrozonej metodologii v0.1/v0.2.
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
for _p in (_REPO_ROOT, _MATH_FORMALISM, _GEOMETRY_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import mann_whitney_test, effect_size_label  # noqa: E402
from timdr_geometry.b4_bearing_data_gate import load_synchronous_cwru_channels  # noqa: E402
from core.chrono_membrane_bridge import membrane_window_metrics  # noqa: E402

# ---------------------------------------------------------------------
# Stale zamrozone 1:1 z real_chrono_membrane_bridge_v0_2.py
# ---------------------------------------------------------------------

WINDOW_SIZES = (128, 256, 512)
N_WINDOWS = 30
SEED_POS = 0
SEED_NEG = 1
ALPHA = 0.05
MIN_VALID_PER_GROUP = 10

# ---------------------------------------------------------------------
# Dane -- ekstrahowane WYBIORCZO z CWRU_Bearing_NumPy_4LUM-main.zip
# (dostarczonego przez uzytkownika) do /tmp/cwru_fresh/, NIE do repo
# (236MB archiwum, zbyt duze zeby kopiowac). Tylko te 8 plikow.
# ---------------------------------------------------------------------

_DATA_DIR = "/tmp/cwru_fresh"

# Wybor PRZED zobaczeniem jakiegokolwiek wyniku tej sesji, wg Contents.md
# archiwum (kolumny DE/FE/BA checkmark):
#
# NORMAL (N=2, DE+FE -- BA=X w Contents.md dla obu plikow Normal,
# dokladnie jak 1797_Normal.npz w v0.1/v0.2):
#   1730_Normal_0_DE12.npz  (1730 RPM -- NOWE RPM)
#   1750_Normal_0_DE12.npz  (1750 RPM -- NOWE RPM)
#
# FAULT (N=3 w plikach zrodlowych DE+FE+BA, ale primarny test tej sesji
# uzywa TYLKO N=2 (DE,FE) -- dokladnie tak jak v0.1/v0.2 primary, zeby
# normal i fault byly porownywane na tym samym podzbiorze kanalow;
# BA jest dostepne w kazdym z tych 6 plikow i moglaby zasilic osobny
# test sekundarny/diagnostyczny analogiczny do v0.1 SS4, tu pominiety
# dla prostoty -- odnotowane wprost, nie ukryte), zroznicowany
# swiadomie PRZED wynikiem: 3 pliki na kazde z dwoch RPM, kazdy inny
# typ uszkodzenia (B=kulka, IR=biezniA wewnetrzna, OR@3/OR@6=biezniA
# zewnetrzna w innej pozycji zegara), kazdy inny rozmiar defektu
# (7/14/21 mils), zeby zaden pojedynczy typ/rozmiar nie zdominowal
# polaczonej proby fault:
#   1730_IR_7_DE12.npz      (IR,    7 mils, 1730 RPM)
#   1730_B_14_DE12.npz      (B,     14 mils, 1730 RPM)
#   1730_OR@6_21_DE12.npz   (OR@6,  21 mils, 1730 RPM)
#   1750_IR_14_DE12.npz     (IR,    14 mils, 1750 RPM)
#   1750_B_21_DE12.npz      (B,     21 mils, 1750 RPM)
#   1750_OR@3_7_DE12.npz    (OR@3,  7 mils, 1750 RPM)
#
# Zaden z tych 8 plikow / kombinacji RPM+typ+rozmiar nie zostal
# uzyty w v0.1/v0.2 (ktore uzywaly WYLACZNIE 1797 RPM, IR_21, OR@6_21).

NORMAL_FILES = [
    os.path.join(_DATA_DIR, "1730_Normal_0_DE12.npz"),
    os.path.join(_DATA_DIR, "1750_Normal_0_DE12.npz"),
]

FAULT_FILES = {
    "1730_IR_7": os.path.join(_DATA_DIR, "1730_IR_7_DE12.npz"),
    "1730_B_14": os.path.join(_DATA_DIR, "1730_B_14_DE12.npz"),
    "1730_OR6_21": os.path.join(_DATA_DIR, "1730_OR@6_21_DE12.npz"),
    "1750_IR_14": os.path.join(_DATA_DIR, "1750_IR_14_DE12.npz"),
    "1750_B_21": os.path.join(_DATA_DIR, "1750_B_21_DE12.npz"),
    "1750_OR3_7": os.path.join(_DATA_DIR, "1750_OR@3_7_DE12.npz"),
}


# ---------------------------------------------------------------------
# Segmentacja -- identyczna logika co real_chrono_membrane_bridge{,_v0_2}.py
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
    seed_pos: int = SEED_POS,
    seed_neg: int = SEED_NEG,
) -> Dict:
    """pos=normal, neg=fault -- tak, ze r>0 odpowiada wprost hipotezie
    tej sesji (normal > fault), zgodnie z konwencja v0.2."""
    pos_windows = _sample_windows(pos_pool, n_windows, seed_pos)
    neg_windows = _sample_windows(neg_pool, n_windows, seed_neg)

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
    supported = result.pvalue < ALPHA and abs(result.effect_size_r) >= 0.3 and result.effect_size_r > 0
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
# Wczytanie danych i budowa polaczonych puli (normal z obu RPM razem,
# fault ze wszystkich 6 wybranych plikow razem) -- N=2 (DE, FE), tak jak
# primarny test v0.1/v0.2
# =======================================================================


def load_pools(window_size: int):
    normal_signals_list = [
        load_synchronous_cwru_channels(f, required_channels=("DE", "FE")).signals
        for f in NORMAL_FILES
    ]
    fault_signals_list = {
        name: load_synchronous_cwru_channels(f, required_channels=("DE", "FE")).signals
        for name, f in FAULT_FILES.items()
    }

    normal_pool: List[List[np.ndarray]] = []
    normal_avail_per_file = {}
    for f, sig in zip(NORMAL_FILES, normal_signals_list):
        pool = _segment_pool(sig, ["DE", "FE"], window_size)
        normal_avail_per_file[os.path.basename(f)] = len(pool)
        normal_pool.extend(pool)

    fault_pool_per_type: Dict[str, List[List[np.ndarray]]] = {}
    fault_avail_per_file = {}
    for name, sig in fault_signals_list.items():
        pool = _segment_pool(sig, ["DE", "FE"], window_size)
        fault_avail_per_file[name] = len(pool)
        fault_pool_per_type[name] = pool

    fault_pool_combined: List[List[np.ndarray]] = []
    for pool in fault_pool_per_type.values():
        fault_pool_combined.extend(pool)

    return normal_pool, fault_pool_combined, fault_pool_per_type, normal_avail_per_file, fault_avail_per_file


# =======================================================================
# Test GLOWNY: normal (polaczone 1730+1750) vs fault (polaczone
# wszystkie 6 wybranych plikow), spectral_concentration, per okno
# =======================================================================


def run_main_test() -> List[Dict]:
    rows = []
    for window_size in WINDOW_SIZES:
        normal_pool, fault_pool_combined, _, normal_avail, fault_avail = load_pools(window_size)
        row = run_group_test(normal_pool, fault_pool_combined, "spectral_concentration")
        row.update({
            "window_size": window_size,
            "metric": "spectral_concentration",
            "n_avail_normal": len(normal_pool),
            "n_avail_fault": len(fault_pool_combined),
            "normal_avail_per_file": normal_avail,
            "fault_avail_per_file": fault_avail,
        })
        rows.append(row)
    return rows


# =======================================================================
# Test DODATKOWY, diagnostyczny (nie decyduje o SUPPORTED/NOT_SUPPORTED
# glownego wyniku): normal (polaczone) vs KAZDY typ uszkodzenia osobno
# =======================================================================


def run_per_type_test() -> List[Dict]:
    rows = []
    for window_size in WINDOW_SIZES:
        normal_pool, _, fault_pool_per_type, normal_avail, fault_avail = load_pools(window_size)
        for fault_name, fault_pool in fault_pool_per_type.items():
            row = run_group_test(normal_pool, fault_pool, "spectral_concentration")
            row.update({
                "window_size": window_size,
                "fault": fault_name,
                "metric": "spectral_concentration",
                "n_avail_normal": len(normal_pool),
                "n_avail_fault": len(fault_pool),
            })
            rows.append(row)
    return rows


# =======================================================================
# Stabilnosc znaku
# =======================================================================


def sign_stability_report(rows: List[Dict], label_key: str = None) -> str:
    lines = ["## Stabilnosc znaku efektu (spectral_concentration, normal vs fault polaczone)", ""]
    if label_key is None:
        signs = [(row["window_size"], row.get("r")) for row in rows]
        signs.sort()
        r_strs = ", ".join(f"w={w}:r={r:+.3f}" if r is not None else f"w={w}:n/a" for w, r in signs)
        valid_r = [r for _, r in signs if r is not None]
        stable = len({np.sign(r) for r in valid_r if r != 0}) <= 1 if valid_r else None
        all_positive = all(r > 0 for r in valid_r) if valid_r else None
        lines.append(f"GLOWNY (normal vs fault polaczone): {r_strs}  ->  ZNAK STABILNY={stable}, WSZYSTKIE r>0={all_positive}")
    else:
        labels = sorted({row[label_key] for row in rows})
        for lbl in labels:
            signs = [(row["window_size"], row.get("r")) for row in rows if row[label_key] == lbl]
            signs.sort()
            r_strs = ", ".join(f"w={w}:r={r:+.3f}" if r is not None else f"w={w}:n/a" for w, r in signs)
            valid_r = [r for _, r in signs if r is not None]
            stable = len({np.sign(r) for r in valid_r if r != 0}) <= 1 if valid_r else None
            all_positive = all(r > 0 for r in valid_r) if valid_r else None
            lines.append(f"{lbl}: {r_strs}  ->  ZNAK STABILNY={stable}, WSZYSTKIE r>0={all_positive}")
    return "\n".join(lines)


def format_report(rows: List[Dict], group_keys: List[str]) -> str:
    lines = []
    for row in rows:
        p_str = f"{row['p']:.4g}" if row['p'] is not None else "n/a"
        r_str = f"{row['r']:.3f}" if row['r'] is not None else "n/a"
        r_lbl = row.get('r_label', 'n/a')
        key_str = " ".join(f"{row[k]}" for k in group_keys)
        lines.append(
            f"{key_str:>15} okno={row['window_size']:>4} "
            f"status={row['status']:>14} p={p_str:>10} r={r_str:>7} ({r_lbl:>7}) "
            f"n_valid_normal={row['n_valid_pos']:>3} n_valid_fault={row['n_valid_neg']:>3} "
            f"n_avail_normal={row['n_avail_normal']:>5} n_avail_fault={row['n_avail_fault']:>5}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    main_rows = run_main_test()
    per_type_rows = run_per_type_test()
    dt = time.time() - t0

    print("=== TEST GLOWNY: normal (1730+1750 polaczone) vs fault (6 plikow polaczone) ===")
    print(format_report(main_rows, []))
    print()
    print(sign_stability_report(main_rows))
    print()
    print("=== TEST DODATKOWY (diagnostyczny): normal vs KAZDY typ uszkodzenia osobno ===")
    print(format_report(per_type_rows, ["fault"]))
    print()
    print(sign_stability_report(per_type_rows, label_key="fault"))

    print(f"\nCzas: {dt:.1f}s")
