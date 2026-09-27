import numpy as np
from core.transition_params import event_density, coherence_cycles, n_cycles, regime, feasibility, band_envelope

FS = 20000.0


def _impulses(rate, tau, T=2.0, seed=0):
    rng = np.random.default_rng(seed); n = int(T * FS); t = np.arange(n) / FS
    x = 0.05 * rng.standard_normal(n)
    for t0 in np.arange(0.01, T, 1 / rate):
        m = t >= t0; x[m] += np.exp(-(t[m] - t0) / tau) * np.sin(2 * np.pi * 4000 * (t[m] - t0))
    return x


def test_density_particle_vs_dense():
    lo = event_density(band_envelope(_impulses(20, 0.002), FS, 3000, 5000), FS)
    hi = event_density(band_envelope(_impulses(400, 0.002), FS, 3000, 5000), FS)
    assert lo["D"] < 0.3 and regime(lo["D"]) == "czasteczka"
    assert 20 * 0.5 < lo["rate"] < 20 * 1.5
    assert hi["D"] > lo["D"] * 5 and regime(hi["D"]) != "czasteczka"
    assert hi["rate"] < 400 * 0.5         # zlane uderzenia nie wystaja ponad tlo (licznik czastek zawodzi) -- jak w budynku LANL
    noise = event_density(band_envelope(np.random.default_rng(1).standard_normal(40000), FS, 3000, 5000), FS)
    assert 2.5 < noise["D"] < 5.0            # szum gaussowski: eta = pi/4, D ~ 3,7


def test_coherence_sine_vs_drift():
    t = np.arange(int(2 * FS)) / FS
    pure = np.sin(2 * np.pi * 100 * t)
    drift = np.sin(2 * np.pi * (100 * t + 15 * t ** 2))      # czestotliwosc 100 -> 160 Hz
    assert coherence_cycles(pure, FS, 100) > coherence_cycles(drift, FS, 100, rel_band=0.8)


def test_feasibility_rules():
    assert not feasibility(3, 100, 0.1, "stala")["sito_ma_szanse"]
    assert not feasibility(150, 1000, 0.1, "wolna")["sito_ma_szanse"]
    f = feasibility(150, 1000, 0.1, "stala"); assert f["sito_ma_szanse"] and f["reżim"] == "czasteczka"
    assert n_cycles(2.0, 76.0) == 152.0
