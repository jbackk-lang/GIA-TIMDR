"""Testy rury analitycznej na sygnalach o znanym promieniu i skrecie."""
import os, sys
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.analytic_tube import (tube_from_signal, reconstruct, winding_turns, revolution_curvatures,  # noqa: E402
                                helix_curvature_torsion, band_tubes, breathing_spectrum)
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa: E402

FS = 8000.0
T = np.arange(int(2 * FS)) / FS
MID = slice(len(T) // 10, -len(T) // 10)   # bez brzegow (efekt brzegowy transformaty Hilberta)


def test_tone_gives_cylinder_and_helix():
    a, f0, v = 2.0, 100.0, 50.0
    tb = tube_from_signal(a * np.cos(2 * np.pi * f0 * T), FS, v=v)
    w = 2 * np.pi * f0
    assert np.allclose(tb.A[MID], a, rtol=1e-3)                    # promien rury = amplituda
    assert np.allclose(tb.omega[MID], w, rtol=1e-3)                 # tempo skretu = czestotliwosc
    k, t = helix_curvature_torsion(tb.curve, 1 / FS)
    assert np.median(k[MID]) == pytest.approx(a * w ** 2 / (v ** 2 + a ** 2 * w ** 2), rel=1e-2)
    assert np.median(t[MID]) == pytest.approx(v * w / (v ** 2 + a ** 2 * w ** 2), rel=1e-2)


def test_cylinder_curvatures():
    km, kp, H, K = revolution_curvatures(np.full(1000, 2.0), 0.01)
    assert np.allclose(km, 0) and np.allclose(kp, 0.5) and np.allclose(H, 0.25) and np.allclose(K, 0)


def test_reconstruction_is_exact():
    x = np.random.default_rng(0).standard_normal(len(T))
    tb = tube_from_signal(x, FS)
    assert np.allclose(reconstruct(tb.A, tb.phi), x, atol=1e-10)


def test_winding_equals_timdr_phase_winding():
    x = np.cos(2 * np.pi * 37.0 * T) + 0.1 * np.random.default_rng(1).standard_normal(len(T))
    assert winding_turns(tube_from_signal(x, FS).phi) == pytest.approx(phase_winding_fn(x), abs=1e-9)
    assert winding_turns(tube_from_signal(np.cos(2 * np.pi * 37.0 * T), FS).phi) == pytest.approx(74.0, abs=0.5)


def test_am_signal_tube_breathes_at_modulation_frequency():
    a, m, Om, f0 = 1.0, 0.5, 7.0, 400.0
    x = a * (1 + m * np.cos(2 * np.pi * Om * T)) * np.cos(2 * np.pi * f0 * T)
    tb = tube_from_signal(x, FS)
    assert np.allclose(tb.A[MID], (a * (1 + m * np.cos(2 * np.pi * Om * T)))[MID], atol=1e-2)
    f, E = breathing_spectrum(tb.A, FS)
    assert f[np.argmax(E[1:]) + 1] == pytest.approx(Om, abs=0.6)


def test_band_tubes_separate_tones():
    x = 1.5 * np.cos(2 * np.pi * 1200 * T) + 0.5 * np.cos(2 * np.pi * 2700 * T)
    A, P = band_tubes(x, FS, [(1000, 2000), (2000, 3000)])
    assert np.median(A[0]) == pytest.approx(1.5, rel=1e-3) and np.median(A[1]) == pytest.approx(0.5, rel=1e-3)
