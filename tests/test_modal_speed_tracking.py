"""Testy samonaprawy w czasie (sledzenie predkosci z drgan + os katowa) na sygnale o znanej zmiennej predkosci."""
import os, sys
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.modal_speed_tracking import track_speed, shaft_phase, order_resonance_map, order_sieve  # noqa: E402
from core.modal_self_repair import resonance_map  # noqa: E402

FS = 20000.0; DUR = 10.0; BPFO = 3.5
BANDS = [(1000.0 * i, 1000.0 * (i + 1)) for i in range(1, 10)]


def turbine(fault=True, seed=5, f0=5.0, f1=7.5):
    """Predkosc rosnie liniowo f0 -> f1 (wiatr); 1x wal (niewywazenie) + 3x (przejscie lopat); uderzenia co 1/BPFO obrotu."""
    rng = np.random.default_rng(seed); n = int(FS * DUR); t = np.arange(n) / FS
    fr = f0 + (f1 - f0) * t / DUR; th = np.cumsum(fr) / FS
    x = 0.8 * np.sin(2 * np.pi * th) + 0.4 * np.sin(2 * np.pi * 3 * th) + rng.standard_normal(n)
    if fault:
        k = np.floor(th * BPFO); idx = np.where(np.diff(k) > 0)[0]; imp = np.zeros(n); imp[idx] = 6
        x += np.convolve(imp, np.exp(-np.arange(150) / 25) * np.sin(2 * np.pi * 3500 * np.arange(150) / FS), "same")
    return x, t, fr


def test_speed_is_tracked_from_vibration_alone():
    x, t, fr = turbine()
    tr = track_speed(x, FS, 3.0, 12.0)
    truth = np.interp(tr.t, t, fr)
    assert np.sqrt(np.mean((tr.fr / truth - 1) ** 2)) < 0.01


def test_angle_domain_restores_fault_order_that_time_domain_smears():
    x, t, fr = turbine()
    tr = track_speed(x, FS, 3.0, 12.0); th = shaft_phase(tr, len(x), FS)
    Ro, orders = order_resonance_map(x, FS, th, BANDS)
    q_ord = order_sieve(Ro, orders, {"BPFO": BPFO})["QO_BPFO"]
    Rz, al = resonance_map(x - x.mean(), FS, BANDS)          # model nominalny: stala predkosc = srednia
    fc = BPFO * fr.mean(); band = (al >= 0.97 * fc) & (al <= 1.03 * fc)
    q_nom = float(np.log(Rz[:, band].max(0).max() + Rz[:, (al >= 0.97 * 2 * fc) & (al <= 1.03 * 2 * fc)].max(0).max()))
    assert q_ord > q_nom + np.log(2.0)   # szczyt w osi katowej co najmniej 2x wyzszy


def test_healthy_turbine_has_low_order_sieve():
    xh, _, _ = turbine(fault=False)
    xf, _, _ = turbine(fault=True)
    def q(x):
        tr = track_speed(x, FS, 3.0, 12.0); th = shaft_phase(tr, len(x), FS)
        Ro, o = order_resonance_map(x, FS, th, BANDS); return order_sieve(Ro, o, {"BPFO": BPFO})["QO_BPFO"]
    assert q(xf) > q(xh) + 1.5


def test_shaft_phase_integrates_speed():
    from core.modal_speed_tracking import SpeedTrack
    tr = SpeedTrack(np.array([0.0, 10.0]), np.array([5.0, 5.0]), np.ones(2))
    th = shaft_phase(tr, int(FS * DUR), FS)
    assert th[-1] == pytest.approx(5.0 * DUR, rel=1e-3)
