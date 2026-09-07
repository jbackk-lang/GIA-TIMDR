# tests/test_trefoil_missing_coordinate_solver.py
"""
test_trefoil_missing_coordinate_solver.py -- testy dla
core/trefoil_missing_coordinate_solver.py.

Cztery testy, w kolejnosci od czystej algebry do uczciwej oceny
praktycznej:

1. v x a jest DOKLADNIE liniowe w brakujacej wspolrzednej (fakt
   matematyczny, na ktorym opiera sie rozwiazywalnosc rownania).
2. Z idealnymi (oracle) celami kappa/tau, prawdziwe z jest zawsze
   jednym z pierwiastkow, a select_by_tau_consistency ZAWSZE je
   poprawnie wybiera (100% trafnosci) -- potwierdza, ze algebra i
   filtr tau dzialaja bezblednie, gdy cele sa znane dokladnie.
3. select_by_resonance SAMO w sobie jest DUZO slabszym selektorem niz
   tau-consistency (~46% trafnosci vs 100%) -- bo odpowiada na inne
   pytanie (czy wyglada jak dziki pik), nie "ktory pierwiastek jest
   prawdziwy". To byl realny blad w pierwszej wersji potoku (rezonans
   nadpisywal wybor tau) -- test pilnuje regresji.
4. W REALISTYCZNYM scenariuszu (cele kappa/tau szacowane z niedawnej
   historii, nie oracle) caly potok -- z wygladzaniem lub bez --
   WYRAZNIE PRZEGRYWA z trywialnym baseline (powtorz ostatnia znana
   wartosc). To jest uczciwy wynik NEGATYWNY: wygladzanie pomaga
   (~20% redukcji bledu), ale nie wystarcza, zeby dogonic baseline --
   bo szacowanie celu z zaszumionej historii dziedziczy dokladnie ten
   sam problem niestabilnosci kappa/tau, co
   trefoil_weather_embedding_validation.py.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pytest

from core.trefoil_missing_coordinate_solver import (
    kappa_tau_of_z,
    select_by_resonance,
    select_by_tau_consistency,
    smooth_trajectory,
    solve_kappa_target,
    solve_missing_coordinate,
)


def _gen_correlated_walk(n, rng, corr=0.7):
    base = np.cumsum(rng.normal(0, 1, n))
    p1 = base + rng.normal(0, 1, n) * np.sqrt(1 - corr)
    p2 = -0.5 * base + rng.normal(0, 1, n) * np.sqrt(1 - corr) * 2 + np.cumsum(rng.normal(0, 0.3, n))
    p3 = 0.3 * base + np.cumsum(rng.normal(0, 0.5, n))
    pts = np.stack([p1, p2, p3], axis=1)
    return (pts - pts.mean(axis=0)) / pts.std(axis=0)


def _recent_kappa_tau_targets(pts, i, lookback=5):
    ks, ts = [], []
    for j in range(max(3, i - lookback), i):
        k, t = kappa_tau_of_z(pts[j, 2], pts[j, 0], pts[j, 1], pts[j - 1], pts[j - 2], pts[j - 3])
        ks.append(k)
        ts.append(t)
    return np.median(ks), np.median(ts)


def test_1_krzyz_v_a_jest_dokladnie_liniowe_w_brakujacej_wspolrzednej():
    rng = np.random.default_rng(0)
    p_t1, p_t2, p_t3 = rng.normal(size=3), rng.normal(size=3), rng.normal(size=3)
    x0, y0 = 1.3, -0.7
    zs = np.linspace(-3, 3, 7)
    cross_vals = []
    for z in zs:
        p_t = np.array([x0, y0, z])
        v = p_t - p_t1
        a = v - (p_t1 - p_t2)
        cross_vals.append(np.cross(v, a))
    second_diff = np.diff(np.array(cross_vals), n=2, axis=0)
    assert np.abs(second_diff).max() < 1e-10


def test_2_oracle_targets_tau_consistency_zawsze_trafia():
    rng = np.random.default_rng(123)
    hits = 0
    n_trials = 60
    for _ in range(n_trials):
        pts = _gen_correlated_walk(30, rng)
        i = rng.integers(10, 28)
        true_z = pts[i, 2]
        x, y = pts[i, 0], pts[i, 1]
        p_t1, p_t2, p_t3 = pts[i - 1], pts[i - 2], pts[i - 3]
        kappa_true, tau_true = kappa_tau_of_z(true_z, x, y, p_t1, p_t2, p_t3)

        roots = solve_kappa_target(x, y, p_t1, p_t2, p_t3, kappa_true, -6, 6)
        assert any(abs(r - true_z) < 0.05 for r in roots), "prawdziwe z powinno byc jednym z pierwiastkow"

        z_pick = select_by_tau_consistency(roots, tau_true, x, y, p_t1, p_t2, p_t3)
        if abs(z_pick - true_z) < 0.05:
            hits += 1

    assert hits / n_trials > 0.95, f"oczekiwano ~100% trafnosci z oracle celami, uzyskano {hits/n_trials:.2f}"


def test_3_rezonans_sam_w_sobie_jest_slabszym_selektorem_niz_tau():
    rng = np.random.default_rng(123)
    hits_tau, hits_res = 0, 0
    n_trials = 60
    for _ in range(n_trials):
        pts = _gen_correlated_walk(30, rng)
        i = rng.integers(10, 28)
        true_z = pts[i, 2]
        x, y = pts[i, 0], pts[i, 1]
        p_t1, p_t2, p_t3 = pts[i - 1], pts[i - 2], pts[i - 3]
        kappa_true, tau_true = kappa_tau_of_z(true_z, x, y, p_t1, p_t2, p_t3)
        roots = solve_kappa_target(x, y, p_t1, p_t2, p_t3, kappa_true, -6, 6)
        if not roots:
            continue
        z_tau = select_by_tau_consistency(roots, tau_true, x, y, p_t1, p_t2, p_t3)
        z_res = select_by_resonance(roots, x, y, pts[:i], p_t1, p_t2, p_t3)
        hits_tau += abs(z_tau - true_z) < 0.05
        hits_res += abs(z_res - true_z) < 0.05

    rate_tau, rate_res = hits_tau / n_trials, hits_res / n_trials
    assert rate_tau > 0.9
    assert rate_res < rate_tau - 0.3, (
        f"oczekiwano, ze rezonans SAM w sobie jest wyraznie slabszy niz tau "
        f"(tau={rate_tau:.2f}, rezonans={rate_res:.2f})"
    )


def test_4_realistyczny_potok_przegrywa_z_trywialnym_baseline():
    """Uczciwy wynik negatywny: gdy cele kappa/tau sa SZACOWANE z
    niedawnej historii (realistyczny scenariusz, nie oracle), caly
    potok -- z wygladzaniem lub bez -- daje WIEKSZY blad odzysku niz
    trywialny baseline (powtorz ostatnia znana wartosc)."""
    rng = np.random.default_rng(123)
    N = 30
    errors_ns, errors_baseline = [], []
    n_trials = 60
    for _ in range(n_trials):
        pts = _gen_correlated_walk(N, rng)
        i = rng.integers(10, N - 2)
        true_z = pts[i, 2]
        x, y = pts[i, 0], pts[i, 1]
        history = pts[:i]
        p_t1, p_t2, p_t3 = history[i - 1], history[i - 2], history[i - 3]
        lookback = min(5, i - 3)
        kappa_t, tau_t = _recent_kappa_tau_targets(history, i, lookback=lookback)

        result = solve_missing_coordinate(
            x, y, p_t1, p_t2, p_t3, history,
            kappa_target=max(kappa_t, 0.05), tau_target=tau_t,
            z_lo=-6, z_hi=6,
        )
        if result["status"] == "ok" and result["z"] is not None:
            errors_ns.append(abs(result["z"] - true_z))
        errors_baseline.append(abs(pts[i - 1, 2] - true_z))

    assert len(errors_ns) > 10, "za malo rozwiazanych probek do oceny"
    mean_geo = np.mean(errors_ns)
    mean_baseline = np.mean(errors_baseline)
    assert mean_geo > 1.5 * mean_baseline, (
        f"oczekiwano, ze potok geometryczny bedzie WYRAZNIE gorszy niz baseline "
        f"(geo={mean_geo:.3f}, baseline={mean_baseline:.3f}) -- to jest wlasnie "
        f"potwierdzenie uczciwego wyniku negatywnego"
    )


def test_smooth_trajectory_redukuje_blad_wzgledem_czystego_sygnalu():
    """Sanity check kroku 4 w izolacji (bez calego potoku): lokalne
    wygladzanie wielomianowe faktycznie zmniejsza MSE wzgledem
    znanego, gladkiego sygnalu odniesienia."""
    rng = np.random.default_rng(1)
    n = 30
    clean = np.sin(np.linspace(0, 3, n))
    noisy = clean + rng.normal(0, 0.3, n)
    pts = np.stack([noisy, noisy, noisy], axis=1)
    smoothed = smooth_trajectory(pts, window=5, polyorder=2)
    mse_noisy = np.mean((noisy - clean) ** 2)
    mse_smoothed = np.mean((smoothed[:, 0] - clean) ** 2)
    assert mse_smoothed < mse_noisy


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
