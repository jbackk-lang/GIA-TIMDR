# core/real_seismic_noise_robustness_bridge.py
"""
real_seismic_noise_robustness_bridge.py -- implementacja PRE-REJESTROWANEJ
(patrz docs/geometry/PREREG_REAL_SEISMIC_NOISE_ROBUSTNESS.md) kontroli
pozytywnej/negatywnej dla mostu M/S<->topologia/K na REALNYM sejsmogramie
mainshocku Ridgecrest 2019 (stacje CLC, RIO), + syntetyczny szum
addytywny rosnacej mocy.

Drugi most na realnych danych po core/real_bearing_noise_robustness_
bridge.py (lozyska CWRU). W ODROZNIENIU od tamtego, ten most wrocil do
STANDARDOWEJ kolejnosci dokumentacji (PREREG przed uruchomieniem, nie
po fakcie).

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow -- wszystkie
wybory (event_idx, rozmiary okien, siatka szumu, definicja generatora)
sa przeniesione 1:1 z zamrozonej pre-rejestracji.
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from typing import Callable, Dict, List

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
_DATA_DIR = os.path.join(
    os.path.dirname(_REPO_ROOT),
    "TIMDR-Earthquake-Core", "data", "ridgecrest_2019", "real_waveform_CLC_RIO",
)
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    run_controls,
    ControlResult,
    effect_size_label,
)

from core.trefoil_ms_bridge import metric_fn as torsion_metric  # noqa: E402
from core.winding_crossing_ms_bridge import (  # noqa: E402
    winding_metric_fn,
    crossing_metric_fn,
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
# 0. event_idx -- zamrozony, obliczony z realnego czasu mainshocku
# ---------------------------------------------------------------------

FS = 100.0
STARTTIME = datetime(2019, 7, 6, 3, 18, 52, 998000)
MAINSHOCK = datetime(2019, 7, 6, 3, 19, 53, 40000)
EVENT_IDX = round((MAINSHOCK - STARTTIME).total_seconds() * FS)  # 6004

STATIONS = {
    "CLC": "CLC_HHZ.csv",
    "RIO": "RIO_HHZ.csv",
}


def load_station(name: str) -> np.ndarray:
    path = os.path.join(_DATA_DIR, STATIONS[name])
    amps = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            _t, a = line.split(",")
            amps.append(float(a))
    return np.array(amps, dtype=float)


# ---------------------------------------------------------------------
# 1. Generator: okno regionu (tlo / koda) + szum (identyczne z mostem
#    lozyskowym)
# ---------------------------------------------------------------------


def make_region_injector(
    region: np.ndarray, sigma_frac: float, window_size: int
) -> Callable[[int, "int | None"], np.ndarray]:
    n_avail = len(region) // window_size
    if n_avail < 1:
        raise ValueError(f"window_size={window_size} > dlugosc regionu={len(region)}")
    segments = [
        region[i * window_size : (i + 1) * window_size] for i in range(n_avail)
    ]

    def _gen(_window_size_ignored: int, seed) -> np.ndarray:
        s = int(seed) if seed is not None else 0
        idx = s % n_avail
        seg = segments[idx].copy()
        if sigma_frac > 0:
            rng = np.random.default_rng(s)
            noise_std = sigma_frac * float(seg.std())
            seg = seg + rng.normal(0.0, noise_std, window_size)
        return seg

    return _gen


# ---------------------------------------------------------------------
# 2. Siatka (zamrozona)
# ---------------------------------------------------------------------

WINDOW_SIZES = (64, 128)
SIGMAS = (0.0, 0.1, 0.3, 0.5, 1.0)
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05


def run_grid_for_station(station_name: str) -> List[Dict]:
    full = load_station(station_name)
    background = full[:EVENT_IDX]
    coda = full[EVENT_IDX:]
    rows: List[Dict] = []
    for window_size in WINDOW_SIZES:
        n_avail_bg = len(background) // window_size
        n_avail_coda = len(coda) // window_size
        for sigma in SIGMAS:
            for metric_name, metric in METRICS.items():
                result: ControlResult = run_controls(
                    metric_fn=metric,
                    positive_injector=make_region_injector(coda, sigma, window_size),
                    negative_generator_a=make_region_injector(background, sigma, window_size),
                    negative_generator_b=make_region_injector(background, sigma, window_size),
                    n_windows=N_WINDOWS,
                    window_size=window_size,
                    seed=SEED,
                    alpha=ALPHA,
                )
                rows.append({
                    "station": station_name,
                    "metric": metric_name,
                    "window_size": window_size,
                    "sigma": sigma,
                    "n_avail_bg": n_avail_bg,
                    "n_avail_coda": n_avail_coda,
                    "reuse_needed": N_WINDOWS > min(n_avail_bg, n_avail_coda),
                    "passed": result.passed,
                    "reason": result.reason,
                    "pos_p": result.positive.pvalue,
                    "pos_r": result.positive.effect_size_r,
                    "pos_r_label": effect_size_label(result.positive.effect_size_r),
                    "neg_p": result.negative.pvalue,
                    "neg_r": result.negative.effect_size_r,
                })
    return rows


def format_report(rows: List[Dict]) -> str:
    lines = []
    lines.append(
        f"{'stacja':>7} {'metryka':>18} {'okno':>5} {'sigma':>6} {'passed':>7} "
        f"{'pos_p':>10} {'pos_r':>8} {'pos_r_lbl':>10} {'neg_p':>10} {'neg_r':>8} {'reuse':>6}"
    )
    for r in rows:
        lines.append(
            f"{r['station']:>7} {r['metric']:>18} {r['window_size']:>5} "
            f"{r['sigma']:>6.2f} {str(r['passed']):>7} {r['pos_p']:>10.4g} "
            f"{r['pos_r']:>8.3f} {r['pos_r_label']:>10} {r['neg_p']:>10.4g} "
            f"{r['neg_r']:>8.3f} {('TAK' if r['reuse_needed'] else ''):>6}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print(f"EVENT_IDX={EVENT_IDX} (t_event={EVENT_IDX/FS:.2f}s)")
    t0 = time.time()
    all_rows: List[Dict] = []
    for station_name in STATIONS:
        all_rows.extend(run_grid_for_station(station_name))
    dt = time.time() - t0

    print(format_report(all_rows))
    n_pass = sum(1 for r in all_rows if r["passed"])
    print(
        f"\nPRZESZLO: {n_pass}/{len(all_rows)} komorek siatki "
        f"({len(STATIONS)} stacje x {len(METRICS)} metryk x "
        f"{len(WINDOW_SIZES)} okna x {len(SIGMAS)} poziomow szumu). "
        f"Czas: {dt:.1f}s"
    )
