# tests/test_chrono_cone_bridge.py
"""Testy jednostkowe "czy operator robi to co mówi" dla
core/chrono_cone_bridge.py -- patrz docs/geometry/
PREREG_CHRONO_CONE_MS_BRIDGE_v0.1.md. Kontrole syntetyczne (bramka
pozytywna/negatywna na pelnej siatce) sa w core/chrono_cone_bridge.py
(uruchamiane jako skrypt, wzorem core/winding_crossing_ms_bridge.py i
core/real_*_noise_robustness_bridge.py -- ta rodzina modulow w tym
repo NIE ma osobnych plikow pytest dla siebie, tylko dla warstwy
niżej). Te testy sprawdzaja WYLACZNIE elementarne wlasciwosci funkcji
budujacych (theta/r/ratio), nie powtarzaja calej bramki kontrolnej.
"""
import os
import sys

import numpy as np
import pytest

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from core.chrono_cone_bridge import (  # noqa: E402
    peak_referenced_phase,
    anomaly_radius,
    chrono_cone_curve,
    chrono_cone_ratio,
    _moving_average,
    _find_peaks,
)


def test_find_peaks_simple_triangle():
    xs = np.array([0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0])
    peaks = _find_peaks(xs)
    assert list(peaks) == [1, 5]


def test_moving_average_preserves_length_and_constant():
    x = np.full(20, 3.0)
    sm = _moving_average(x, 5)
    assert len(sm) == len(x)
    assert np.allclose(sm, 3.0)


def test_peak_referenced_phase_none_when_too_few_peaks():
    x = np.linspace(0, 1, 50)  # monotone, no interior local maxima
    assert peak_referenced_phase(x) is None


def test_peak_referenced_phase_counts_full_turns():
    n = 300
    t = np.arange(n, dtype=float)
    x = np.sin(2 * np.pi / 15.0 * t)
    theta = peak_referenced_phase(x, smooth_window=5)
    assert theta is not None
    # faza jest niemalejaca i konczy sie w wielokrotnosci 2*pi
    assert np.all(np.diff(theta) >= -1e-9)
    assert theta[-1] % (2 * np.pi) < 1e-6 or (2 * np.pi - theta[-1] % (2 * np.pi)) < 1e-6


def test_anomaly_radius_matches_continuous_deviation():
    x = np.array([0.0, 0.0, 10.0, 0.0])
    r = anomaly_radius(x)
    m, sd = x.mean(), x.std()
    assert np.allclose(r, np.abs(x - m) / sd)


def test_anomaly_radius_constant_signal_is_zero():
    x = np.full(10, 5.0)
    r = anomaly_radius(x)
    assert np.allclose(r, 0.0)


def test_chrono_cone_ratio_nan_when_no_peaks():
    x = np.linspace(0, 1, 50)
    assert np.isnan(chrono_cone_ratio(x))


def test_chrono_cone_ratio_growing_amplitude_exceeds_one():
    rng = np.random.default_rng(0)
    n = 256
    t = np.arange(n, dtype=float)
    x = (1.0 + 0.05 * t) * np.sin(2 * np.pi / 15.0 * t) + rng.normal(0, 0.1, n)
    ratio = chrono_cone_ratio(x)
    assert not np.isnan(ratio)
    assert ratio > 1.5


def test_chrono_cone_ratio_constant_amplitude_near_one():
    rng = np.random.default_rng(1)
    n = 256
    t = np.arange(n, dtype=float)
    x = np.sin(2 * np.pi / 15.0 * t) + rng.normal(0, 0.1, n)
    ratio = chrono_cone_ratio(x)
    assert not np.isnan(ratio)
    assert 0.5 < ratio < 2.0


def test_chrono_cone_curve_shape():
    n = 200
    t = np.arange(n, dtype=float)
    x = np.sin(2 * np.pi / 15.0 * t)
    curve = chrono_cone_curve(x)
    assert curve is not None
    assert curve.shape == (n, 3)
    # os z jest dokladnie indeksem probki (Chronoproces, uproszczenie SS4)
    assert np.allclose(curve[:, 2], t)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
