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


def _impacts(times, amp=6.0):
    imp = np.zeros(len(T)); imp[(np.asarray(times) * FS).astype(int)] = amp
    return sum(np.convolve(imp, np.exp(-np.arange(200) / 30) * np.sin(2 * np.pi * c * np.arange(200) / FS), "same")
               for c in (3500, 5500, 9500))


def test_duality_map():
    tones = sum(np.sin(2 * np.pi * f * T) for f in (25, 50, 75))
    noise = RNG.standard_normal(len(T))
    per = 1 / 76.3; ideal = np.arange(0.01, 1.99, per)
    rhythm = _impacts(ideal + RNG.normal(0, 0.01 * per, len(ideal)))   # rytm z poslizgiem 1% (jak lozysko)
    scattered = _impacts(np.sort(RNG.uniform(0.01, 1.99, 12)))
    assert signal_character(tones + 0.1 * noise, FS)["dualnosc"] == "falowy"
    assert signal_character(noise, FS)["dualnosc"] == "szumowy"
    assert signal_character(scattered + 0.3 * noise, FS)["dualnosc"] == "czasteczkowy"
    assert signal_character(rhythm + 0.3 * noise, FS)["dualnosc"] == "pakiet falowy"
    assert signal_character(20 * tones + rhythm + 0.3 * noise, FS)["dualnosc"] == "mieszany (fala + pakiet)"


def test_strictly_periodic_impacts_are_both_wave_and_particle():
    """Scisle okresowy ciag impulsow ma widmo z samych linii (szereg Fouriera): jest i fala, i czastka."""
    x = _impacts(np.arange(0.01, 1.99, 1 / 76.3)) + 0.3 * RNG.standard_normal(len(T))
    assert signal_character(x, FS)["dualnosc"] == "mieszany (fala + pakiet)"
