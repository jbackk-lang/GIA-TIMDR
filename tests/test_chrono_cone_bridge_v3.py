# tests/test_chrono_cone_bridge_v3.py
"""Testy jednostkowe "czy operator robi to co mowi" dla
core/chrono_cone_bridge_v3.py -- patrz docs/geometry/
PREREG_CHRONO_CONE_MS_BRIDGE_v0.3.md. Wzorem test_chrono_cone_bridge_v2.py:
kontrole syntetyczne (Kontrola #0 na calej siatce + Kontrola #1) sa w
core/chrono_cone_bridge_v3.py jako skrypt; te testy sprawdzaja
elementarne wlasciwosci funkcji budujacych (kalibracja k, r_total,
ratio, gate) PLUS jeden regresyjny test Kontroli #0 na jednym rozmiarze
okna (pelna siatka jest wolniejsza, uruchamiana przez skrypt glowny).
"""
import os
import sys

import numpy as np
import pytest

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from core.chrono_cone_bridge_v3 import (  # noqa: E402
    calibrate_k,
    centrifugal_radius,
    chrono_centrifugal_curve,
    chrono_centrifugal_ratio,
    run_noise_risk_control,
    A_MAX,
    K_TABLE,
    ALL_WINDOW_SIZES,
)
from core.chrono_cone_bridge import anomaly_radius  # noqa: E402
from core.chrono_cone_bridge_v2 import trend_referenced_phase  # noqa: E402


def test_k_table_covers_all_grid_sizes():
    for w in ALL_WINDOW_SIZES:
        assert w in K_TABLE
        assert K_TABLE[w] > 0
        assert not np.isnan(K_TABLE[w])


def test_calibrate_k_matches_frozen_table():
    # PREREG SS3: metoda deterministyczna (stały calib_seed) -- ponowne
    # wywolanie musi dac dokladnie te sama wartosc co w K_TABLE.
    for w in (128, 256):
        assert np.isclose(calibrate_k(w), K_TABLE[w])


def test_calibrate_k_scales_inversely_with_target_amplification():
    w = 128
    k_default = calibrate_k(w, target_amplification=A_MAX)
    k_double = calibrate_k(w, target_amplification=2 * A_MAX)
    assert np.isclose(k_double, 2 * k_default)


def test_centrifugal_radius_never_below_anomaly_radius():
    rng = np.random.default_rng(0)
    n = 256
    t = np.arange(n, dtype=float)
    x = (1.0 + 0.05 * t) * np.sin(2 * np.pi / 15.0 * t) + rng.normal(0, 0.1, n)
    r_plain = anomaly_radius(x)
    r_tot = centrifugal_radius(x)
    assert r_tot is not None
    # r_total = r_anomalia * (1 + k*theta^2) >= r_anomalia zawsze (k>0, theta^2>=0)
    assert np.all(r_tot >= r_plain - 1e-12)


def test_centrifugal_radius_none_when_no_extrema():
    x = np.linspace(0, 1, 50)  # monotone
    assert trend_referenced_phase(x) is None
    assert centrifugal_radius(x) is None


def test_chrono_centrifugal_ratio_nan_when_no_extrema():
    x = np.linspace(0, 1, 50)
    assert np.isnan(chrono_centrifugal_ratio(x))


def test_chrono_centrifugal_ratio_finite_on_growing_amplitude():
    rng = np.random.default_rng(0)
    n = 256
    t = np.arange(n, dtype=float)
    x = (1.0 + 0.05 * t) * np.sin(2 * np.pi / 15.0 * t) + rng.normal(0, 0.1, n)
    ratio = chrono_centrifugal_ratio(x)
    assert not np.isnan(ratio)
    assert ratio > 0


def test_chrono_centrifugal_curve_shape():
    n = 200
    t = np.arange(n, dtype=float)
    x = np.sin(2 * np.pi / 15.0 * t)
    curve = chrono_centrifugal_curve(x)
    assert curve is not None
    assert curve.shape == (n, 3)
    assert np.allclose(curve[:, 2], t)


def test_noise_risk_control_flags_false_signal_at_window_128():
    # Regresja PREREG SS5.0: przy k skalibrowanym wg zamrozonej metody,
    # czlon odsrodkowy na CZYSTYM SZUMIE daje wykrywalna, statystycznie
    # istotna, nietrywialna roznice wzgledem czystej metryki v0.2 -- to
    # jest UDOKUMENTOWANY wynik negatywny (RESULT v0.3), NIE oczekiwany
    # "dobry" wynik -- test pinuje ten fakt jako regresje, nie jako
    # potwierdzenie hipotezy.
    result = run_noise_risk_control(window_size=128, n_windows=30, seed=0)
    assert not result.inconclusive
    assert result.false_signal is True
    assert result.p < 0.05
    assert abs(result.r_eff) >= 0.3


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
