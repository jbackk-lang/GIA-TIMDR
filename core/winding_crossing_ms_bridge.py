# core/winding_crossing_ms_bridge.py
"""
winding_crossing_ms_bridge.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_WINDING_CROSSING_MS_BRIDGE.md) syntetycznej kontroli
pozytywnej/negatywnej dla mostu "sygnal 1D (M/S) -> ten sam embedding
opozniajacy co w trefoil_ms_bridge.py -> rzut PCA 3D->2D -> winding
number LUB crossing number -> pipeline anty-numerologiczny".

Bezposrednia kontynuacja core/trefoil_ms_bridge.py (RESULT: 0/10,
ODRZUCONY -- diagnoza: potrojne roznicowanie torsji wzmacnia szum).
Embedding i generatory kontroli sa CELOWO reuzyte 1:1 z tamtego modulu
(import, nie kopia) -- jedyna zmieniona rzecz to krok "trajektoria ->
skalar": zero lub jedno roznicowanie zamiast trzech.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow.
"""
from __future__ import annotations

import os
import sys
from typing import List, Dict, Tuple

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    run_controls,
    ControlResult,
    effect_size_label,
)
from core.trefoil_ms_bridge import (  # noqa: E402
    LAG,
    make_positive_injector,
    make_negative_a,
    make_negative_b,
    WINDOW_SIZES,
    SIGMAS,
    N_WINDOWS,
    SEED,
    ALPHA,
)

# ---------------------------------------------------------------------
# 1. Embedding (identyczny z trefoil_ms_bridge.metric_fn, wydzielony) +
#    2. Rzut PCA 3D -> 2D (zamrozone, sekcja 1-2 pre-rejestracji)
# ---------------------------------------------------------------------


def _embed_3d(signal_1d: np.ndarray, lag: int = LAG) -> "np.ndarray | None":
    x = np.asarray(signal_1d, dtype=float)
    std = float(x.std())
    if std < 1e-12:
        return None
    xn = (x - float(x.mean())) / std
    n = len(xn) - 2 * lag
    if n < 4:
        return None
    return np.stack([xn[:n], xn[lag:lag + n], xn[2 * lag:2 * lag + n]], axis=1)


def project_pca_2d(pts3d: np.ndarray) -> "np.ndarray | None":
    """PCA: centruj, wez 2 wektory wlasne o najwiekszych wartosciach
    wlasnych macierzy kowariancji, rzutuj. Deterministyczne (np.linalg.eigh
    dla macierzy symetrycznej), zero roznicowania czasowego."""
    centered = pts3d - pts3d.mean(axis=0)
    cov = np.cov(centered, rowvar=False)
    if not np.all(np.isfinite(cov)):
        return None
    eigvals, eigvecs = np.linalg.eigh(cov)  # rosnaco
    top2 = eigvecs[:, -2:]  # dwa najwieksze
    return centered @ top2  # (n, 2)


# ---------------------------------------------------------------------
# 3. Metryka A: winding/turning number
# ---------------------------------------------------------------------


def winding_metric_fn(signal_1d: np.ndarray) -> float:
    pts3d = _embed_3d(signal_1d)
    if pts3d is None:
        return 0.0
    pts2d = project_pca_2d(pts3d)
    if pts2d is None or len(pts2d) < 3:
        return 0.0
    centered = pts2d - pts2d.mean(axis=0)
    theta = np.arctan2(centered[:, 1], centered[:, 0])
    theta_unwrapped = np.unwrap(theta)
    return float(abs(theta_unwrapped[-1] - theta_unwrapped[0]) / (2 * np.pi))


# ---------------------------------------------------------------------
# 4. Metryka B: crossing number (niesasiadujace odcinki, orientacja)
# ---------------------------------------------------------------------


def _cross2(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    return u[..., 0] * v[..., 1] - u[..., 1] * v[..., 0]


def crossing_metric_fn(signal_1d: np.ndarray) -> float:
    """Wektoryzowana wersja (numpy broadcasting zamiast podwojnej petli
    Python) -- MATEMATYCZNIE identyczny test orientacji (znak iloczynu
    wektorowego), tylko policzony dla wszystkich par odcinkow naraz.
    Zmiana wylacznie wydajnosciowa, zdecydowana PRZED uruchomieniem na
    pelnej siatce (pierwsza, czysto-Pythonowa wersja przekroczyla limit
    czasu przy n=300, m^2~90000 par x 900 wywolan siatki) -- definicja
    metryki (sekcja 4 pre-rejestracji) jest niezmieniona."""
    pts3d = _embed_3d(signal_1d)
    if pts3d is None:
        return 0.0
    pts2d = project_pca_2d(pts3d)
    if pts2d is None or len(pts2d) < 4:
        return 0.0

    P = pts2d[:-1]
    Q = pts2d[1:]
    AB = Q - P
    m = len(P)

    Pi = P[:, None, :]
    Qi = Q[:, None, :]
    Pj = P[None, :, :]
    Qj = Q[None, :, :]
    ABi = AB[:, None, :]
    ABj = AB[None, :, :]

    o1 = _cross2(ABi, Pj - Pi)
    o2 = _cross2(ABi, Qj - Pi)
    o3 = _cross2(ABj, Pi - Pj)
    o4 = _cross2(ABj, Qi - Pj)

    intersect = (
        (np.sign(o1) != np.sign(o2))
        & (np.sign(o3) != np.sign(o4))
        & (o1 != 0) & (o2 != 0) & (o3 != 0) & (o4 != 0)
    )
    idx_i, idx_j = np.meshgrid(np.arange(m), np.arange(m), indexing="ij")
    mask = idx_j >= idx_i + 2  # niesasiadujace odcinki, bez podwojnego liczenia
    return float(np.sum(intersect & mask))


# ---------------------------------------------------------------------
# 5-6. Siatka: dwie metryki x 2 okna x 5 poziomow szumu (zamrozone)
# ---------------------------------------------------------------------


def run_grid_for(metric_fn, metric_name: str) -> List[Dict]:
    rows: List[Dict] = []
    for window_size in WINDOW_SIZES:
        for sigma in SIGMAS:
            result: ControlResult = run_controls(
                metric_fn=metric_fn,
                positive_injector=make_positive_injector(sigma),
                negative_generator_a=make_negative_a(sigma),
                negative_generator_b=make_negative_b(sigma),
                n_windows=N_WINDOWS,
                window_size=window_size,
                seed=SEED,
                alpha=ALPHA,
            )
            rows.append({
                "metric": metric_name,
                "window_size": window_size,
                "sigma": sigma,
                "degenerate_neg_a": sigma == 0.0,
                "passed": result.passed,
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
        f"{'metryka':>9} {'okno':>5} {'sigma':>6} {'passed':>7} {'pos_p':>10} "
        f"{'pos_r':>8} {'pos_r_lbl':>10} {'neg_p':>10} {'neg_r':>8} {'degen':>6}"
    )
    for r in rows:
        lines.append(
            f"{r['metric']:>9} {r['window_size']:>5} {r['sigma']:>6.2f} "
            f"{str(r['passed']):>7} {r['pos_p']:>10.4g} {r['pos_r']:>8.3f} "
            f"{r['pos_r_label']:>10} {r['neg_p']:>10.4g} {r['neg_r']:>8.3f} "
            f"{'TAK' if r['degenerate_neg_a'] else '':>6}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    all_rows = run_grid_for(winding_metric_fn, "winding") + run_grid_for(crossing_metric_fn, "crossing")
    print(format_report(all_rows))
    n_pass = sum(1 for r in all_rows if r["passed"])
    print(f"\nPRZESZLO: {n_pass}/{len(all_rows)} komorek siatki "
          f"(2 metryki x {len(WINDOW_SIZES)} okna x {len(SIGMAS)} poziomow szumu).")
