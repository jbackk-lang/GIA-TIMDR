# core/real_btc_noise_robustness_bridge.py
"""
real_btc_noise_robustness_bridge.py -- implementacja PRE-REJESTROWANEJ
(patrz docs/geometry/PREREG_REAL_BTC_NOISE_ROBUSTNESS.md) kontroli
pozytywnej/negatywnej dla mostu M/S<->topologia/K na REALNYCH zwrotach
godzinowych BTC/USD, + syntetyczny szum addytywny rosnacej mocy.

Trzeci most na realnych danych (po lozyskach CWRU i sejsmice Ridgecrest).
Region pozytywny (wysoka zmiennosc) i negatywny (niska zmiennosc)
zdefiniowane jako bloki 24h -- okna metryki NIGDY nie przecinaja
granicy bloku ani nie sklejaja dwoch roznych blokow (lekcja z mostu
sejsmicznego: jednorodnosc regionu pozytywnego).

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow.
"""
from __future__ import annotations

import csv
import os
import sys
import time
from typing import Callable, Dict, List

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
_DATA_FILE = os.path.join(
    os.path.dirname(_REPO_ROOT), "deliverable_timdr_finanse", "data", "btcusd_1h.csv"
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

BLOCK_SIZE = 24  # 24h blok, zamrozone


def load_log_returns() -> np.ndarray:
    closes = []
    with open(_DATA_FILE, "r") as f:
        r = csv.DictReader(f)
        for row in r:
            closes.append(float(row["close"]))
    closes = np.array(closes, dtype=float)
    return np.diff(np.log(closes))


def split_blocks_by_regime(logret: np.ndarray, block_size: int = BLOCK_SIZE):
    """Zwraca (high_vol_blocks, low_vol_blocks) -- listy 1D-array po
    block_size probek kazdy, podzial medianowy po std bloku."""
    n_blocks = len(logret) // block_size
    blocks = [logret[i * block_size:(i + 1) * block_size] for i in range(n_blocks)]
    stds = np.array([b.std() for b in blocks])
    median = np.median(stds)
    high = [b for b, s in zip(blocks, stds) if s >= median]
    low = [b for b, s in zip(blocks, stds) if s < median]
    return high, low


# ---------------------------------------------------------------------
# Generator: okno WEWNATRZ jednego bloku (nigdy nie przecina granicy) + szum
# ---------------------------------------------------------------------


def make_regime_injector(
    blocks: List[np.ndarray], sigma_frac: float, window_size: int
) -> Callable[[int, "int | None"], np.ndarray]:
    n_blocks = len(blocks)
    sub_per_block = BLOCK_SIZE // window_size  # 1 (window=24) albo 2 (window=12)
    n_avail = n_blocks * sub_per_block

    def _gen(_window_size_ignored: int, seed) -> np.ndarray:
        s = int(seed) if seed is not None else 0
        block_idx = (s // sub_per_block) % n_blocks if sub_per_block > 1 else s % n_blocks
        sub_idx = s % sub_per_block
        block = blocks[block_idx]
        seg = block[sub_idx * window_size:(sub_idx + 1) * window_size].copy()
        if sigma_frac > 0:
            rng = np.random.default_rng(s)
            noise_std = sigma_frac * float(seg.std())
            seg = seg + rng.normal(0.0, noise_std, window_size)
        return seg

    _gen.n_avail = n_avail  # type: ignore[attr-defined]
    return _gen


# ---------------------------------------------------------------------
# Siatka (zamrozona)
# ---------------------------------------------------------------------

WINDOW_SIZES = (12, 24)
SIGMAS = (0.0, 0.1, 0.3, 0.5, 1.0)
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05


def run_grid() -> List[Dict]:
    logret = load_log_returns()
    high_blocks, low_blocks = split_blocks_by_regime(logret)
    rows: List[Dict] = []
    for window_size in WINDOW_SIZES:
        pos_gen_probe = make_regime_injector(high_blocks, 0.0, window_size)
        neg_gen_probe = make_regime_injector(low_blocks, 0.0, window_size)
        n_avail_pos = pos_gen_probe.n_avail  # type: ignore[attr-defined]
        n_avail_neg = neg_gen_probe.n_avail  # type: ignore[attr-defined]
        for sigma in SIGMAS:
            for metric_name, metric in METRICS.items():
                result: ControlResult = run_controls(
                    metric_fn=metric,
                    positive_injector=make_regime_injector(high_blocks, sigma, window_size),
                    negative_generator_a=make_regime_injector(low_blocks, sigma, window_size),
                    negative_generator_b=make_regime_injector(low_blocks, sigma, window_size),
                    n_windows=N_WINDOWS,
                    window_size=window_size,
                    seed=SEED,
                    alpha=ALPHA,
                )
                rows.append({
                    "metric": metric_name,
                    "window_size": window_size,
                    "sigma": sigma,
                    "n_avail_pos": n_avail_pos,
                    "n_avail_neg": n_avail_neg,
                    "reuse_needed": N_WINDOWS > min(n_avail_pos, n_avail_neg),
                    "passed": result.passed,
                    "reason": result.reason,
                    "pos_p": result.positive.pvalue,
                    "pos_r": result.positive.effect_size_r,
                    "pos_r_label": effect_size_label(result.positive.effect_size_r),
                    "neg_p": result.negative.pvalue,
                    "neg_r": result.negative.effect_size_r,
                })
    return rows, len(high_blocks), len(low_blocks)


def format_report(rows: List[Dict]) -> str:
    lines = []
    lines.append(
        f"{'metryka':>18} {'okno':>5} {'sigma':>6} {'passed':>7} "
        f"{'pos_p':>10} {'pos_r':>8} {'pos_r_lbl':>10} {'neg_p':>10} {'neg_r':>8} {'reuse':>6}"
    )
    for r in rows:
        lines.append(
            f"{r['metric']:>18} {r['window_size']:>5} {r['sigma']:>6.2f} "
            f"{str(r['passed']):>7} {r['pos_p']:>10.4g} {r['pos_r']:>8.3f} "
            f"{r['pos_r_label']:>10} {r['neg_p']:>10.4g} {r['neg_r']:>8.3f} "
            f"{('TAK' if r['reuse_needed'] else ''):>6}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    rows, n_high, n_low = run_grid()
    dt = time.time() - t0
    print(f"n_blocks_high_vol={n_high}  n_blocks_low_vol={n_low}")
    print(format_report(rows))
    n_pass = sum(1 for r in rows if r["passed"])
    print(
        f"\nPRZESZLO: {n_pass}/{len(rows)} komorek siatki "
        f"({len(METRICS)} metryk x {len(WINDOW_SIZES)} okna x "
        f"{len(SIGMAS)} poziomow szumu). Czas: {dt:.1f}s"
    )
