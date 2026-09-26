import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.signal_character import signal_character  # noqa: E402

FS = 32000.0; T = np.arange(int(2 * FS)) / FS; RNG = np.random.default_rng(0)


def test_tones_are_modal():
    x = sum(np.sin(2 * np.pi * f * T) for f in (25, 50, 75, 150)) + 0.1 * RNG.standard_normal(len(T))
    assert signal_character(x, FS)["typ"] == "modalny"


def test_impacts_ringing_in_bands_are_field():
    imp = np.zeros(len(T)); imp[(np.arange(0, 2, 1 / 76.3) * FS).astype(int)] = 6
    ring = sum(np.convolve(imp, np.exp(-np.arange(200) / 30) * np.sin(2 * np.pi * c * np.arange(200) / FS), "same")
               for c in (3500, 5500, 9500, 12500))
    assert signal_character(ring + RNG.standard_normal(len(T)), FS)["typ"] == "polowy"


def test_white_noise_is_undetermined():
    assert signal_character(RNG.standard_normal(len(T)), FS)["typ"] == "nieokreslony"
