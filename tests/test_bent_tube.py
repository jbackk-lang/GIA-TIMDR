"""Testy rury zgietej i skreconej na sygnalach dwuskalowych o znanej geometrii."""
import os, sys
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.bent_tube import bent_tube, bend_features, tube_surface  # noqa: E402

FS = 8000.0; T = np.arange(int(4 * FS)) / FS; MID = slice(len(T) // 10, -len(T) // 10)


def test_slow_tone_bends_axis_into_helix():
    a, W, v = 0.5, 2 * np.pi * 10.0, 5.0
    bt = bent_tube(a * np.cos(W * T), FS, slow=(1, 200), fast=(1000, None), v=v)
    assert np.median(bt.kappa[MID]) == pytest.approx(a * W ** 2 / (v ** 2 + a ** 2 * W ** 2), rel=2e-2)
    assert np.median(bt.tau[MID]) == pytest.approx(v * W / (v ** 2 + a ** 2 * W ** 2), rel=2e-2)


def test_scales_separate_bend_from_breathing():
    slow = 0.5 * np.cos(2 * np.pi * 10 * T)
    fast = (1 + 0.6 * np.cos(2 * np.pi * 37 * T)) * np.cos(2 * np.pi * 2500 * T)
    f = bend_features(bent_tube(slow + fast, FS))
    assert f["bend_radius"] == pytest.approx(0.5, rel=2e-2)          # zgiecie osi = amplituda czesci wolnej
    assert f["breath"] == pytest.approx(0.6 / np.sqrt(2), rel=5e-2)  # oddech promienia = glebokosc modulacji / sqrt 2


def test_speed_change_stretches_tube_longitudinally():
    const = bend_features(bent_tube(0.5 * np.cos(2 * np.pi * 10 * T), FS))["stretch"]
    ph = 2 * np.pi * np.cumsum(8 + 4 * T / T[-1]) / FS       # czestotliwosc wolnej czesci 8 -> 12 Hz
    chirp = bend_features(bent_tube(0.5 * np.cos(ph), FS))["stretch"]
    assert const < 0.01 and chirp > 5 * const


def test_no_slow_part_gives_straight_tube():
    f = bend_features(bent_tube(np.cos(2 * np.pi * 2500 * T), FS))
    assert f["bend_radius"] < 1e-3


def test_surface_shape():
    bt = bent_tube(0.5 * np.cos(2 * np.pi * 10 * T) + np.cos(2 * np.pi * 2500 * T), FS)
    assert tube_surface(bt, n_theta=8, step=100).shape == (len(T[::100]), 8, 3)
