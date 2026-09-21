# tests/test_chrono_cone_bridge_v2.py
"""Testy jednostkowe "czy operator robi to co mowi" dla
core/chrono_cone_bridge_v2.py -- patrz docs/geometry/
PREREG_CHRONO_CONE_MS_BRIDGE_v0.2.md. Wzorem test_chrono_cone_bridge.py
(v0.1): kontrole syntetyczne (bramka) sa w core/chrono_cone_bridge_v2.py
jako skrypt; te testy sprawdzaja WYLACZNIE elementarne wlasciwosci
funkcji budujacych (theta_v2/ratio/net_turn), nie powtarzaja calej
bramki kontrolnej.
"""
import os
import sys

import numpy as np
import pytest

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from core.chrono_cone_bridge_v2 import (  # noqa: E402
    trend_referenced_phase,
    chrono_pendulum_curve,
    chrono_pendulum_ratio,
    chrono_pendulum_net_turn,
    _find_troughs,
    _find_extrema,
)
from core.chrono_cone_bridge import chrono_cone_ratio  # noqa: E402


def test_find_troughs_simple_triangle():
    xs = np.array([0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0])
    troughs = _find_troughs(xs)
    assert list(troughs) == [3]


def test_find_extrema_alternates_peaks_and_troughs():
    xs = np.array([0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0])
    extrema = _find_extrema(xs)
    # peak@1, trough@3, peak@5
    assert list(extrema) == [1, 3, 5]


def test_trend_referenced_phase_none_when_too_few_extrema():
    x = np.linspace(0, 1, 50)  # monotone, no interior extrema
    assert trend_referenced_phase(x) is None


def test_trend_referenced_phase_symmetric_cycle_returns_to_start():
    # wznoszenie -> opadanie -> wznoszenie, z DWOMA ekstremami WEWNETRZNYMI
    # (szczyt@15, dolina@45) -- segment [15,45] to jeden pelny cykl
    # opadania, wiec faza powinna spasc o dokladnie 2*pi (nie wrocic do
    # 0 mod cos wiekszego -- test docelowy "brak nieograniczonego
    # narastania" jest w test_chrono_pendulum_net_turn_symmetric_cycle_near_zero).
    x2 = np.concatenate([
        np.linspace(0, 1, 16),   # wznoszenie do szczytu @15
        np.linspace(1, -1, 31)[1:],  # opadanie do doliny @45
        np.linspace(-1, 0, 16)[1:],  # wznoszenie z powrotem
    ])
    theta2 = trend_referenced_phase(x2, smooth_window=1)
    assert theta2 is not None
    # dwa wewnetrzne ekstrema: szczyt @15, dolina @45
    # segment [15,45] opadanie -> -2pi; przed szczytem plasko 0; po dolinie plasko (0-2pi)=-2pi
    assert np.isclose(theta2[0], 0.0)
    assert np.isclose(theta2[15], 0.0)  # cum przed pierwszym ekstremum
    assert np.isclose(theta2[-1], -2 * np.pi)


def test_trend_referenced_phase_ascending_then_descending_signs():
    # wznoszenie -> opadanie -> wznoszenie: znaki segmentow +, -, (koniec plaski)
    x = np.array([0.0, 1.0, 2.0, 1.0, 0.0, 1.0, 2.0])
    theta = trend_referenced_phase(x, smooth_window=1)
    assert theta is not None
    # ekstrema: szczyt@2, dolina@4 (indeksy wewnetrzne)
    # segment [2,4] opadanie -> faza spada o 2pi
    assert theta[4] < theta[2]
    assert np.isclose(theta[2] - theta[4], 2 * np.pi)


def test_chrono_pendulum_ratio_nan_when_no_extrema():
    x = np.linspace(0, 1, 50)
    assert np.isnan(chrono_pendulum_ratio(x))


def test_chrono_pendulum_ratio_growing_amplitude_exceeds_one():
    rng = np.random.default_rng(0)
    n = 256
    t = np.arange(n, dtype=float)
    x = (1.0 + 0.05 * t) * np.sin(2 * np.pi / 15.0 * t) + rng.normal(0, 0.1, n)
    ratio = chrono_pendulum_ratio(x)
    assert not np.isnan(ratio)
    assert ratio > 1.5


def test_chrono_pendulum_ratio_matches_v1_when_both_gates_pass():
    # PREREG SS1: dla okna przechodzacego bramke w OBU wersjach,
    # wartosc ratio MUSI byc identyczna (formula r(t) niezmieniona,
    # theta wchodzi wylacznie jako brama istnienia).
    rng = np.random.default_rng(0)
    n = 256
    t = np.arange(n, dtype=float)
    x = (1.0 + 0.05 * t) * np.sin(2 * np.pi / 15.0 * t) + rng.normal(0, 0.1, n)
    ratio_v1 = chrono_cone_ratio(x)
    ratio_v2 = chrono_pendulum_ratio(x)
    assert not np.isnan(ratio_v1) and not np.isnan(ratio_v2)
    assert np.isclose(ratio_v1, ratio_v2)


def test_chrono_pendulum_net_turn_symmetric_cycle_near_zero():
    x2 = np.concatenate([
        np.linspace(0, 1, 16),
        np.linspace(1, -1, 31)[1:],
        np.linspace(-1, 0, 16)[1:],
    ])
    net_turn = chrono_pendulum_net_turn(x2, smooth_window=1)
    assert not np.isnan(net_turn)
    assert np.isclose(net_turn, -1.0)  # jeden pelny obrot ujemny (opadanie)


def test_chrono_pendulum_curve_shape():
    n = 200
    t = np.arange(n, dtype=float)
    x = np.sin(2 * np.pi / 15.0 * t)
    curve = chrono_pendulum_curve(x)
    assert curve is not None
    assert curve.shape == (n, 3)
    assert np.allclose(curve[:, 2], t)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
