# core/real_chrono_cone_bridge.py
"""
real_chrono_cone_bridge.py -- test glowny (PREREG SS8-9,
docs/geometry/PREREG_CHRONO_CONE_MS_BRIDGE_v0.1.md) metryki
`chrono_cone_ratio` (core/chrono_cone_bridge.py) na TRZECH realnych
domenach uzywanych juz przez wszystkie poprzednie mosty M/S<->topologia/
G tego repo: lozyska CWRU, sejsmika Ridgecrest 2019, BTC/USD.

Uruchamiane WYLACZNIE po tym, jak core/chrono_cone_bridge.py::
run_synthetic_controls() przeszlo (PASSED=True dla obu window_size) --
zgodnie z bramka kontrolna protokolu (skill SS3/SS9).

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow -- wszystkie
stale (rozmiary okien, BLOCK_SIZE=48 dla BTC, siatka SIGMAS) sa
przeniesione 1:1 z PREREG SS8, zamrozonej PRZED uruchomieniem tego pliku.
"""
from __future__ import annotations

import csv
import os
import sys
import time
from datetime import datetime
from typing import Callable, Dict, List, Optional

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
_SIBLING_ROOT = os.path.dirname(_REPO_ROOT)
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import mann_whitney_test, effect_size_label  # noqa: E402
from core.chrono_cone_bridge import chrono_cone_ratio  # noqa: E402

SIGMAS = (0.0, 0.1, 0.3, 0.5, 1.0)
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05
MIN_VALID_PER_GROUP = 10  # PREREG SS9: INCONCLUSIVE jesli < 10 wazne obserwacje


# ---------------------------------------------------------------------
# Generator wspolny: okno realnego segmentu + szum addytywny (identyczna
# konstrukcja co w trzech poprzednich mostach real_*_noise_robustness)
# ---------------------------------------------------------------------


def make_segment_injector(
    pool: List[np.ndarray], sigma_frac: float
) -> Callable[[int, Optional[int]], np.ndarray]:
    n_avail = len(pool)

    def _gen(_window_size_ignored: int, seed) -> np.ndarray:
        s = int(seed) if seed is not None else 0
        idx = s % n_avail
        seg = pool[idx].copy()
        if sigma_frac > 0:
            rng = np.random.default_rng(s)
            noise_std = sigma_frac * float(seg.std())
            seg = seg + rng.normal(0.0, noise_std, len(seg))
        return seg

    return _gen


def _valid(values: np.ndarray) -> np.ndarray:
    return values[~np.isnan(values)]


def run_group_test(
    pos_pool: List[np.ndarray],
    neg_pool: List[np.ndarray],
    sigma: float,
    n_windows: int = N_WINDOWS,
    seed: int = SEED,
) -> Dict:
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)
    pos_gen = make_segment_injector(pos_pool, sigma)
    neg_gen = make_segment_injector(neg_pool, sigma)
    pos_vals = np.array([chrono_cone_ratio(pos_gen(0, int(s))) for s in seeds])
    neg_vals = np.array([chrono_cone_ratio(neg_gen(0, int(s))) for s in seeds])
    pos_valid = _valid(pos_vals)
    neg_valid = _valid(neg_vals)

    row = {
        "sigma": sigma,
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
# 1. Lozyska CWRU
# =======================================================================

_BEARING_DIR = os.path.join(_SIBLING_ROOT, "TIMDR-Industrial-Predict", "data", "cwru_bearing")
BEARING_WINDOW_SIZES = (256, 512)
BEARING_NORMAL_FILE = "normal_1797_de_first1536.csv"
BEARING_DEFECT_FILES = {
    "ir_0021": "ir_0021_1797_de_first1536.csv",
    "or6_0021": "or6_0021_1797_de_first1536.csv",
    "b_0021": "b_0021_1797_de_first1536.csv",
}


def _load_row_csv(path: str) -> np.ndarray:
    with open(path, "r") as f:
        line = f.read().strip()
    return np.array([float(v) for v in line.split(",") if v != ""], dtype=float)


def _segment_pool(signal: np.ndarray, window_size: int) -> List[np.ndarray]:
    n_avail = len(signal) // window_size
    return [signal[i * window_size:(i + 1) * window_size] for i in range(n_avail)]


def run_bearing() -> List[Dict]:
    normal = _load_row_csv(os.path.join(_BEARING_DIR, BEARING_NORMAL_FILE))
    rows = []
    for defect_name, fname in BEARING_DEFECT_FILES.items():
        defect = _load_row_csv(os.path.join(_BEARING_DIR, fname))
        for window_size in BEARING_WINDOW_SIZES:
            normal_pool = _segment_pool(normal, window_size)
            defect_pool = _segment_pool(defect, window_size)
            for sigma in SIGMAS:
                row = run_group_test(defect_pool, normal_pool, sigma)
                row.update({"domain": "bearing", "case": defect_name, "window_size": window_size,
                            "n_avail_pos": len(defect_pool), "n_avail_neg": len(normal_pool)})
                rows.append(row)
    return rows


# =======================================================================
# 2. Sejsmika Ridgecrest 2019
# =======================================================================

_SEISMIC_DIR = os.path.join(_SIBLING_ROOT, "TIMDR-Earthquake-Core", "data",
                             "ridgecrest_2019", "real_waveform_CLC_RIO")
SEISMIC_WINDOW_SIZES = (512, 1024)
FS = 100.0
STARTTIME = datetime(2019, 7, 6, 3, 18, 52, 998000)
MAINSHOCK = datetime(2019, 7, 6, 3, 19, 53, 40000)
EVENT_IDX = round((MAINSHOCK - STARTTIME).total_seconds() * FS)  # 6004
STATIONS = {"CLC": "CLC_HHZ.csv", "RIO": "RIO_HHZ.csv"}


def _load_station(name: str) -> np.ndarray:
    path = os.path.join(_SEISMIC_DIR, STATIONS[name])
    amps = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            _t, a = line.split(",")
            amps.append(float(a))
    return np.array(amps, dtype=float)


def run_seismic() -> List[Dict]:
    rows = []
    for station in STATIONS:
        full = _load_station(station)
        background = full[:EVENT_IDX]
        coda = full[EVENT_IDX:]
        for window_size in SEISMIC_WINDOW_SIZES:
            bg_pool = _segment_pool(background, window_size)
            coda_pool = _segment_pool(coda, window_size)
            for sigma in SIGMAS:
                row = run_group_test(coda_pool, bg_pool, sigma)
                row.update({"domain": "seismic", "case": station, "window_size": window_size,
                            "n_avail_pos": len(coda_pool), "n_avail_neg": len(bg_pool)})
                rows.append(row)
    return rows


# =======================================================================
# 3. BTC/USD -- BLOCK_SIZE=48h (odstepstwo od poprzedniego mostu,
#    uzasadnione i zamrozone w PREREG SS8.3)
# =======================================================================

_BTC_FILE = os.path.join(_SIBLING_ROOT, "deliverable_timdr_finanse", "data", "btcusd_1h.csv")
BTC_BLOCK_SIZE = 48
BTC_WINDOW_SIZES = (48,)


def _load_log_returns() -> np.ndarray:
    closes = []
    with open(_BTC_FILE, "r") as f:
        r = csv.DictReader(f)
        for row in r:
            closes.append(float(row["close"]))
    closes = np.array(closes, dtype=float)
    return np.diff(np.log(closes))


def _split_blocks_by_regime(logret: np.ndarray, block_size: int):
    n_blocks = len(logret) // block_size
    blocks = [logret[i * block_size:(i + 1) * block_size] for i in range(n_blocks)]
    stds = np.array([b.std() for b in blocks])
    median = np.median(stds)
    high = [b for b, s in zip(blocks, stds) if s >= median]
    low = [b for b, s in zip(blocks, stds) if s < median]
    return high, low


def run_btc() -> List[Dict]:
    logret = _load_log_returns()
    high_blocks, low_blocks = _split_blocks_by_regime(logret, BTC_BLOCK_SIZE)
    rows = []
    for window_size in BTC_WINDOW_SIZES:
        assert window_size == BTC_BLOCK_SIZE
        for sigma in SIGMAS:
            row = run_group_test(high_blocks, low_blocks, sigma)
            row.update({"domain": "btc", "case": "high_vs_low_vol", "window_size": window_size,
                        "n_avail_pos": len(high_blocks), "n_avail_neg": len(low_blocks)})
            rows.append(row)
    return rows, len(high_blocks), len(low_blocks)


# =======================================================================
# Raport
# =======================================================================


def format_report(rows: List[Dict]) -> str:
    lines = [
        f"{'domain':>8} {'case':>10} {'okno':>5} {'sigma':>6} {'status':>14} "
        f"{'p':>10} {'r':>7} {'r_lbl':>8} {'n_valid_pos':>12} {'n_valid_neg':>12}"
    ]
    for row in rows:
        p_str = f"{row['p']:.4g}" if row['p'] is not None else "n/a"
        r_str = f"{row['r']:.3f}" if row['r'] is not None else "n/a"
        r_lbl = row.get('r_label', 'n/a')
        lines.append(
            f"{row['domain']:>8} {row['case']:>10} {row['window_size']:>5} "
            f"{row['sigma']:>6.2f} {row['status']:>14} {p_str:>10} {r_str:>7} "
            f"{r_lbl:>8} {row['n_valid_pos']:>12} {row['n_valid_neg']:>12}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    bearing_rows = run_bearing()
    seismic_rows = run_seismic()
    btc_rows, n_high, n_low = run_btc()
    dt = time.time() - t0

    all_rows = bearing_rows + seismic_rows + btc_rows
    print(f"EVENT_IDX(seismic)={EVENT_IDX}  n_blocks_high_vol(btc)={n_high}  n_blocks_low_vol(btc)={n_low}")
    print(format_report(all_rows))

    for domain in ("bearing", "seismic", "btc"):
        drows = [r for r in all_rows if r["domain"] == domain]
        n_sup = sum(1 for r in drows if r["status"] == "SUPPORTED")
        n_notsup = sum(1 for r in drows if r["status"] == "NOT_SUPPORTED")
        n_inc = sum(1 for r in drows if r["status"] == "INCONCLUSIVE")
        print(f"\n{domain}: SUPPORTED={n_sup} NOT_SUPPORTED={n_notsup} INCONCLUSIVE={n_inc} / {len(drows)}")

    # sigma=0.0 (najczystszy wiersz, konwencja poprzednich mostow) osobno
    print("\n--- sigma=0.0 (najczystszy wiersz) ---")
    for row in all_rows:
        if row["sigma"] == 0.0:
            print(row)

    print(f"\nCzas: {dt:.1f}s")
