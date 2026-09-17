# core/zero_mode_topology_bridge.py
"""
zero_mode_topology_bridge.py -- implementacja kandydujacego (NIE
ustalonego) mostu M/S<->G ("most M/S<->G #1: tlumienie trybu zerowego
+ koherencja topologiczna", dopisek w Axioms_S_TIMDR_Signal.md /
Axioms_G_TIMDR_Geometry.md, 2026-09-17).

    Z0(S)  = mu^2 * T / (Eac + eps),  mu=srednia okna, Eac=INTEGRAL (S-mu)^2 dt
    G_i(S) = norm(W_i, C_i, P_i)  -- znormalizowana kombinacja
             winding_number/crossing_number/phase_winding (istniejace
             metryki z core/winding_crossing_ms_bridge.py,
             core/phase_winding_oam_ms_bridge.py, punkt 19 skilla)
    MC_{M/S<->G}(S) ciagly  = w1*(1-Z0) + w3*(G_i/Gref)
    MC_{M/S<->G}(S) binarny = 1[Z0<theta0] * 1[G_i>thetaG]

UWAGA o Z0 i dt: dyskretnie, Eac_dyskretne = sum((S-mu)^2)*dt oraz
T = N*dt (N=liczba probek). dt SKRACA SIE w ilorazie:
    Z0 = mu^2*N*dt / (sum((S-mu)^2)*dt + eps) = mu^2*N / (sum((S-mu)^2)+eps)
-- Z0 jest wiec NIEZMIENNICZE wzgledem wyboru jednostki czasu/czestotliwosci
probkowania (ten sam test niezmienniczosci co w moscie Fouriera M/S<->K,
punkt 17 skilla), zweryfikowane explicite w tests/test_zero_mode_topology_bridge.py.

Status: kandydat, NIE ustalony most. Ten plik dostarcza warstwe
operatorowa + kalibracje G_i z zadanego tla. Testy syntetyczne:
tests/test_zero_mode_topology_bridge.py. Pre-rejestracja progow
theta0/thetaG/wag: docs/geometry/PREREG_MOBIUS_COHERENCE_BRIDGES.md.
Test na realnych danych: core/real_zero_mode_topology_bridge.py.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from core.winding_crossing_ms_bridge import (  # noqa: E402
    winding_metric_fn,
    crossing_metric_fn,
)
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa: E402


# ---------------------------------------------------------------------
# Z0 -- tlumienie trybu zerowego
# ---------------------------------------------------------------------


def zero_mode_fraction(signal_1d: np.ndarray, eps: float = 1e-9) -> float:
    """Z0 = mu^2*N / (sum((S-mu)^2) + eps) -- patrz dowod niezmienniczosci
    dt w docstringu modulu. Male Z0 = 'brak trybu zerowego' (Mobius-like),
    duze Z0 = sygnal zdominowany skladowa stala."""
    x = np.asarray(signal_1d, dtype=float)
    n = len(x)
    if n == 0:
        return 0.0
    mu = float(x.mean())
    eac = float(np.sum((x - mu) ** 2))
    return (mu ** 2 * n) / (eac + eps)


# ---------------------------------------------------------------------
# G_i -- znormalizowana kombinacja winding/crossing/phase_winding
# ---------------------------------------------------------------------


@dataclass(frozen=True)
class GiRanges:
    """Zakresy [min,max] trzech metryk skladowych, kalibrowane z
    OSOBNEGO zbioru tla (NIE z danych, na ktorych G_i jest pozniej
    raportowane) -- ten sam wzorzec co calibrate_q_crit() w gs_matrix.py."""
    w_min: float
    w_max: float
    c_min: float
    c_max: float
    p_min: float
    p_max: float


def compute_wcp(signal_1d: np.ndarray) -> Tuple[float, float, float]:
    return (
        winding_metric_fn(signal_1d),
        crossing_metric_fn(signal_1d),
        phase_winding_fn(signal_1d),
    )


def calibrate_gi_ranges(background_signals) -> GiRanges:
    """Kalibruje GiRanges z listy sygnalow tla (np. mieszanka kontroli
    pozytywnej i negatywnej z syntetycznej pre-rejestracji, LUB same
    okna tla realnych danych w tescie realnym) -- min/max KAZDEJ z
    trzech metryk po calym zbiorze tla."""
    Ws, Cs, Ps = [], [], []
    for s in background_signals:
        w, c, p = compute_wcp(s)
        Ws.append(w)
        Cs.append(c)
        Ps.append(p)
    return GiRanges(
        w_min=float(min(Ws)), w_max=float(max(Ws)),
        c_min=float(min(Cs)), c_max=float(max(Cs)),
        p_min=float(min(Ps)), p_max=float(max(Ps)),
    )


def _minmax01(v: float, vmin: float, vmax: float, eps: float = 1e-9) -> float:
    x = (v - vmin) / (vmax - vmin + eps)
    return float(min(1.0, max(0.0, x)))


def g_i(signal_1d: np.ndarray, ranges: GiRanges) -> float:
    """G_i = mean(norm(W), norm(C), norm(P)) -- kazda skladowa
    znormalizowana min-max do [0,1] wzgledem PRE-KALIBROWANYCH zakresow
    `ranges` (nie wzgledem samej siebie -- to zapewnia porownywalnosc
    miedzy roznymi oknami/sygnalami, ktore uzywaja tych samych `ranges`)."""
    w, c, p = compute_wcp(signal_1d)
    nw = _minmax01(w, ranges.w_min, ranges.w_max)
    nc = _minmax01(c, ranges.c_min, ranges.c_max)
    np_ = _minmax01(p, ranges.p_min, ranges.p_max)
    return (nw + nc + np_) / 3.0


# ---------------------------------------------------------------------
# MC_{M/S<->G} -- operator ciagly i binarny
# ---------------------------------------------------------------------


def mc_ms_g_continuous(z0: float, gi: float, w1: float = 0.5, w3: float = 0.5,
                        gref: float = 1.0) -> float:
    return w1 * (1.0 - z0) + w3 * (gi / gref)


def mc_ms_g_binary(z0: float, gi: float, theta0: float, thetaG: float) -> bool:
    return bool(z0 < theta0 and gi > thetaG)
