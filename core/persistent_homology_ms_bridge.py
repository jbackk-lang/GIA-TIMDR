# core/persistent_homology_ms_bridge.py
"""
persistent_homology_ms_bridge.py -- implementacja PRE-REJESTROWANEJ
(patrz docs/geometry/PREREG_PERSISTENT_HOMOLOGY_MS_BRIDGE.md)
syntetycznej kontroli pozytywnej/negatywnej dla mostu "sygnal 1D (M/S)
-> ten sam embedding opozniajacy co w trefoil_ms_bridge.py -> filtracja
Vietorisa-Ripsa (ripser) -> calkowita persystencja H1 -> pipeline
anty-numerologiczny".

Trzecia i ostatnia z trojki kandydatow po odrzuceniu torsji
Freneta-Serreta (RESULT_TREFOIL_MS_BRIDGE.md, 0/10) oraz winding/
crossing number (RESULT_WINDING_CROSSING_MS_BRIDGE.md, 0/20). Nowa
zaleznosc: `ripser` (nie byla wczesniej czescia stosu tego ekosystemu,
zainstalowana jawnie na potrzeby tego testu).

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow.
"""
from __future__ import annotations

import os
import sys
from typing import List, Dict

import numpy as np
from ripser import ripser

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
# 2. Embedding (identyczny, bez rzutu 2D -- sekcja 2 pre-rejestracji)
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


# ---------------------------------------------------------------------
# 3. Metryka: calkowita persystencja H1 (zamrozona)
# ---------------------------------------------------------------------


def h1_total_persistence_fn(signal_1d: np.ndarray) -> float:
    pts = _embed_3d(signal_1d)
    if pts is None or len(pts) < 5:
        return 0.0
    result = ripser(pts, maxdim=1)
    dgm1 = result["dgms"][1]
    if len(dgm1) == 0:
        return 0.0
    finite = dgm1[np.isfinite(dgm1[:, 1])]
    if len(finite) == 0:
        return 0.0
    return float(np.sum(finite[:, 1] - finite[:, 0]))


# ---------------------------------------------------------------------
# 4. Siatka (identyczna z poprzednimi dwoma mostami)
# ---------------------------------------------------------------------


def run_grid() -> List[Dict]:
    rows: List[Dict] = []
    for window_size in WINDOW_SIZES:
        for sigma in SIGMAS:
            result: ControlResult = run_controls(
                metric_fn=h1_total_persistence_fn,
                positive_injector=make_positive_injector(sigma),
                negative_generator_a=make_negative_a(sigma),
                negative_generator_b=make_negative_b(sigma),
                n_windows=N_WINDOWS,
                window_size=window_size,
                seed=SEED,
                alpha=ALPHA,
            )
            rows.append({
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
        f"{'okno':>5} {'sigma':>6} {'passed':>7} {'pos_p':>10} {'pos_r':>8} "
        f"{'pos_r_lbl':>10} {'neg_p':>10} {'neg_r':>8} {'degen':>6}"
    )
    for r in rows:
        lines.append(
            f"{r['window_size']:>5} {r['sigma']:>6.2f} {str(r['passed']):>7} "
            f"{r['pos_p']:>10.4g} {r['pos_r']:>8.3f} {r['pos_r_label']:>10} "
            f"{r['neg_p']:>10.4g} {r['neg_r']:>8.3f} "
            f"{'TAK' if r['degenerate_neg_a'] else '':>6}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    rows = run_grid()
    print(format_report(rows))
    n_pass = sum(1 for r in rows if r["passed"])
    print(f"\nPRZESZLO: {n_pass}/{len(rows)} komorek siatki "
          f"({len(WINDOW_SIZES)} okna x {len(SIGMAS)} poziomow szumu).")
