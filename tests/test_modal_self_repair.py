"""Testy samonaprawiajacego sie modelu modalnego na sygnalach o znanym rozstrojeniu."""
import os, sys
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.modal_self_repair import repair_model, resonance_map, lock_quality  # noqa: E402

FS = 32000.0
BANDS = [(1000.0 * i, 1000.0 * (i + 1)) for i in range(1, 16)]
MULT = {"BPFO": 3.054, "BPFI": 4.946}


def impacts(fault_freq, seed=3, carrier=5500.0, amp=6.0):
    rng = np.random.default_rng(seed); n = int(2 * FS); x = rng.standard_normal(n); imp = np.zeros(n)
    imp[(np.arange(0, 2, 1 / fault_freq) * FS).astype(int)] = amp
    ring = np.exp(-np.arange(200) / 30) * np.sin(2 * np.pi * carrier * np.arange(200) / FS)
    return x + np.convolve(imp, ring, "same")


@pytest.mark.parametrize("true_s", [1.03, 0.975, 1.0])
def test_repair_recovers_known_detuning(true_s):
    x = impacts(MULT["BPFO"] * 1500 / 60 * true_s)
    r = repair_model(x, FS, 1500, MULT, BANDS)
    assert r.hypothesis == "BPFO"
    assert r.s == pytest.approx(true_s, abs=0.002)


def test_repair_improves_lock_quality_when_detuned():
    r = repair_model(impacts(MULT["BPFO"] * 1500 / 60 * 1.03), FS, 1500, MULT, BANDS)
    assert r.quality_after > 2 * r.quality_before


def test_inner_race_hypothesis_selected():
    r = repair_model(impacts(MULT["BPFI"] * 1500 / 60 * 1.02), FS, 1500, MULT, BANDS)
    assert r.hypothesis == "BPFI" and r.s == pytest.approx(1.02, abs=0.002)


def test_noise_repair_is_bounded_and_lock_stays_low():
    x = np.random.default_rng(11).standard_normal(int(2 * FS))
    r = repair_model(x, FS, 1500, MULT, BANDS)
    assert r.repair <= 0.06 + 1e-9 and r.quality_after < 4.0


def test_loop_converges_quickly():
    r = repair_model(impacts(MULT["BPFO"] * 1500 / 60 * 1.03), FS, 1500, MULT, BANDS)
    assert len(r.trajectory) <= 26 and abs(r.trajectory[-1] - r.trajectory[-2]) < 1e-3


def test_lock_quality_is_background_for_absent_frequency():
    x = impacts(MULT["BPFO"] * 25)
    Rz, al = resonance_map(x - x.mean(), FS, BANDS)
    assert lock_quality(Rz, al, [MULT["BPFO"] * 25]) > 5 * lock_quality(Rz, al, [137.0])
