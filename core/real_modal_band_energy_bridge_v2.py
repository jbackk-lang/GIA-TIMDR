# core/real_modal_band_energy_bridge_v2.py
"""
real_modal_band_energy_bridge_v2.py -- test na realnych danych CWRU
dla modal_band_energy_bridge v0.2 (pelna demodulacja: pasmo rezonansu
przez kurtoze na Normal, widmo obwiedni, szukanie piku przy BPFO/
BPFI/BSF). Patrz docs/geometry/PREREG_MODAL_BAND_ENERGY_BRIDGE_v0.2.md
SS4. URUCHAMIANE po przejsciu kontroli syntetycznych v0.2 (PASSED na
wszystkich trzech window_size, patrz raport).
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

from core.modal_band_energy_bridge import select_resonance_band, envelope_spectrum_peak  # noqa: E402
from core.real_modal_band_energy_bridge import (  # noqa: E402
    load_de, segment_windows, FILES, MATCHED_PAIRS, WINDOW_SAMPLES, N_WINDOWS, SEED, ALPHA, BONFERRONI_N,
)
from core.chrono_modal_geometry_bridge import BAND_NAMES, CHAR_FREQS, FS_RAW_HZ  # noqa: E402
from timdr_formalism.pipeline import mann_whitney_test, effect_size_label  # noqa: E402


def run_real_test_v2() -> Dict:
    print("Wybor pasma rezonansu z Normal (kurtoza)...")
    de_normal_full = load_de(FILES["Normal"])
    resonance_band, best_kurt = select_resonance_band(de_normal_full, FS_RAW_HZ)
    print(f"Wybrane pasmo rezonansu: {resonance_band} Hz (kurtoza nadmiarowa={best_kurt:.3f})")

    print("Liczenie widma obwiedni per okno per plik (moze chwile potrwac)...")
    all_peaks = {}
    for label, fname in FILES.items():
        de = load_de(fname)
        windows = segment_windows(de, N_WINDOWS, SEED)
        per_band = {name: [] for name in BAND_NAMES}
        for w in windows:
            peaks = envelope_spectrum_peak(w, FS_RAW_HZ, resonance_band, CHAR_FREQS)
            for name in BAND_NAMES:
                per_band[name].append(peaks[name])
        all_peaks[label] = {name: np.array(vals) for name, vals in per_band.items()}

    results = {"resonance_band": resonance_band, "resonance_kurtosis": best_kurt, "matched": {}, "unmatched": {}, "stability": {}}

    for fault_label, matched_band in MATCHED_PAIRS.items():
        test_vals = all_peaks[fault_label][matched_band]
        bg_vals = all_peaks["Normal"][matched_band]
        t = mann_whitney_test(test_vals, bg_vals, alternative="greater")
        alpha_corr = ALPHA / BONFERRONI_N
        supported = t.pvalue < alpha_corr
        results["matched"][f"{fault_label}->{matched_band}"] = {
            "p": t.pvalue, "r": t.effect_size_r,
            "median_fault": t.median_test, "median_normal": t.median_background,
            "supported": supported,
        }

        n_half_t = len(test_vals) // 2
        n_half_b = len(bg_vals) // 2
        t1 = mann_whitney_test(test_vals[:n_half_t], bg_vals[:n_half_b], alternative="greater")
        t2 = mann_whitney_test(test_vals[n_half_t:], bg_vals[n_half_b:], alternative="greater")
        stable = (t1.median_test > t1.median_background) == (t2.median_test > t2.median_background)
        results["stability"][f"{fault_label}->{matched_band}"] = {
            "half1_p": t1.pvalue, "half1_dir_up": t1.median_test > t1.median_background,
            "half2_p": t2.pvalue, "half2_dir_up": t2.median_test > t2.median_background,
            "stable": stable,
        }

        for other_band in BAND_NAMES:
            if other_band == matched_band:
                continue
            tv = all_peaks[fault_label][other_band]
            bv = all_peaks["Normal"][other_band]
            tt = mann_whitney_test(tv, bv, alternative="two-sided")
            results["unmatched"][f"{fault_label}->{other_band}"] = {
                "p": tt.pvalue, "r": tt.effect_size_r,
                "median_fault": tt.median_test, "median_normal": tt.median_background,
            }

    return results


def format_report_v2(results: Dict) -> str:
    lines = ["## Wynik realny: modal_band_energy_bridge v0.2 (pelna demodulacja)", ""]
    lines.append(f"Pasmo rezonansu (z Normal, kurtoza={results['resonance_kurtosis']:.3f}): {results['resonance_band']} Hz")
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
    results = run_real_test_v2()
    print(format_report_v2(results))
    print(f"Czas: {time.time()-t0:.2f}s")
