# core/real_modal_band_energy_bridge.py
"""
real_modal_band_energy_bridge.py -- test na realnych danych CWRU dla
modal_band_energy_bridge v0.1 (patrz
docs/geometry/PREREG_MODAL_BAND_ENERGY_BRIDGE_v0.1.md SS5-SS6).
URUCHAMIANE WYLACZNIE po przejsciu kontroli syntetycznych
(core/modal_band_energy_bridge.py) -- PASSED na wszystkich trzech
window_size (500,1000,2000), patrz raport z uruchomienia.

Trzy pary DOPASOWANE (IR->BPFI, OR->BPFO, B->BSF), jednostronne,
korekta Bonferroniego na 3. Szesc par NIEDOPASOWANYCH, dwustronne,
opisowe (nie klasyfikujace).
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
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from core.modal_band_energy_bridge import all_band_energies  # noqa: E402
from core.chrono_modal_geometry_bridge import BAND_NAMES, FS_RAW_HZ  # noqa: E402
from timdr_formalism.pipeline import mann_whitney_test, effect_size_label  # noqa: E402

DATA_DIR = os.path.join(
    os.path.dirname(_REPO_ROOT),  # TIMDR-Industrial-Predict jest siostrzanym repo obok GIA-TIMDR, nie zagniezdzonym
    "TIMDR-Industrial-Predict",
    "data",
    "cwru_bearing",
    "b4_raw",
    "source_mirror",
    "Data",
    "1797 RPM",
)

FILES = {
    "Normal": "1797_Normal.npz",
    "IR_21": "1797_IR_21_DE12.npz",
    "OR@6_21": "1797_OR@6_21_DE12.npz",
    "B_21": "1797_B_21_DE12.npz",
}

MATCHED_PAIRS = {  # SS3.2 PREREG: plik -> pasmo dopasowane, przewidywanie kierunku
    "IR_21": "BPFI",
    "OR@6_21": "BPFO",
    "B_21": "BSF",
}

WINDOW_SAMPLES = 12000  # 1.0s @ 12kHz
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05
BONFERRONI_N = 3


def load_de(filename: str) -> np.ndarray:
    path = os.path.join(DATA_DIR, filename)
    with np.load(path, allow_pickle=False) as archive:
        de = archive["DE"]
    return np.asarray(de, dtype=float).reshape(-1)


def segment_windows(signal: np.ndarray, n_windows: int, seed: int) -> List[np.ndarray]:
    n = len(signal)
    n_blocks = n // WINDOW_SAMPLES
    if n_blocks == 0:
        return []
    rng = np.random.default_rng(seed)
    k = min(n_windows, n_blocks)
    block_idx = rng.choice(n_blocks, size=k, replace=False)
    return [signal[i * WINDOW_SAMPLES : (i + 1) * WINDOW_SAMPLES] for i in block_idx]


def energies_for_file(filename: str, seed: int = SEED) -> Dict[str, np.ndarray]:
    de = load_de(filename)
    windows = segment_windows(de, N_WINDOWS, seed)
    per_band = {name: [] for name in BAND_NAMES}
    for w in windows:
        e = all_band_energies(w, fs=FS_RAW_HZ)
        for name in BAND_NAMES:
            per_band[name].append(e[name])
    return {name: np.array(vals) for name, vals in per_band.items()}


def run_real_test() -> Dict:
    print("Wczytywanie i liczenie energii pasm (moze chwile potrwac)...")
    all_energies = {label: energies_for_file(fname) for label, fname in FILES.items()}

    results = {"matched": {}, "unmatched": {}, "stability": {}}

    for fault_label, matched_band in MATCHED_PAIRS.items():
        test_vals = all_energies[fault_label][matched_band]
        bg_vals = all_energies["Normal"][matched_band]
        t = mann_whitney_test(test_vals, bg_vals, alternative="greater")
        alpha_corr = ALPHA / BONFERRONI_N
        supported = t.pvalue < alpha_corr
        results["matched"][f"{fault_label}->{matched_band}"] = {
            "p": t.pvalue,
            "r": t.effect_size_r,
            "median_fault": t.median_test,
            "median_normal": t.median_background,
            "supported": supported,
        }

        # SS6 PREREG: stabilnosc -- podzial pol-na-pol
        n_half_t = len(test_vals) // 2
        n_half_b = len(bg_vals) // 2
        t1 = mann_whitney_test(test_vals[:n_half_t], bg_vals[:n_half_b], alternative="greater")
        t2 = mann_whitney_test(test_vals[n_half_t:], bg_vals[n_half_b:], alternative="greater")
        stable = (t1.median_test > t1.median_background) == (t2.median_test > t2.median_background)
        results["stability"][f"{fault_label}->{matched_band}"] = {
            "half1_p": t1.pvalue,
            "half1_dir_up": t1.median_test > t1.median_background,
            "half2_p": t2.pvalue,
            "half2_dir_up": t2.median_test > t2.median_background,
            "stable": stable,
        }

        for other_band in BAND_NAMES:
            if other_band == matched_band:
                continue
            tv = all_energies[fault_label][other_band]
            bv = all_energies["Normal"][other_band]
            tt = mann_whitney_test(tv, bv, alternative="two-sided")
            results["unmatched"][f"{fault_label}->{other_band}"] = {
                "p": tt.pvalue,
                "r": tt.effect_size_r,
                "median_fault": tt.median_test,
                "median_normal": tt.median_background,
            }

    return results


def format_report(results: Dict) -> str:
    lines = ["## Wynik realny: modal_band_energy_bridge v0.1", ""]
    lines.append(f"Korekta Bonferroniego: alpha_corr = {ALPHA/BONFERRONI_N:.4f}")
    lines.append("")
    lines.append("### Pary DOPASOWANE (test glowny, jednostronny \"greater\")")
    for key, r in results["matched"].items():
        lines.append(
            f"{key}: p={r['p']:.4g} r={r['r']:.3f} ({effect_size_label(r['r'])}) "
            f"mediana(fault)={r['median_fault']:.4g} mediana(normal)={r['median_normal']:.4g} "
            f"SUPPORTED={r['supported']}"
        )
    lines.append("")
    lines.append("### Stabilnosc (podzial pol-na-pol)")
    for key, s in results["stability"].items():
        lines.append(
            f"{key}: polowa1 p={s['half1_p']:.4g} kierunek_gora={s['half1_dir_up']}, "
            f"polowa2 p={s['half2_p']:.4g} kierunek_gora={s['half2_dir_up']}, STABLE={s['stable']}"
        )
    lines.append("")
    lines.append("### Pary NIEDOPASOWANE (opisowe, dwustronne)")
    for key, r in results["unmatched"].items():
        lines.append(
            f"{key}: p={r['p']:.4g} r={r['r']:.3f} "
            f"mediana(fault)={r['median_fault']:.4g} mediana(normal)={r['median_normal']:.4g}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    results = run_real_test()
    print(format_report(results))
    print(f"Czas: {time.time()-t0:.2f}s")
