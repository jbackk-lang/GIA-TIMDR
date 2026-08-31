"""
test_sg_shooting.py — testy core/sg_shooting.py.

Zakres: nelder_mead() jako generyczny minimalizator jest testowany na
funkcjach NIEZALEŻNYCH od kosmologii (paraboloida, funkcja Rosenbrocka)
- test samego mechanizmu optymalizacji, oddzielony od poprawności
równań SG. shoot_omega_m() jest testowane na łatwym przypadku ξ=0
(patrz test_sg_background.py::test_xi_zero_decouples_u_from_x_y - przy
ξ=0 (x,y) nie zależą od u, więc problem jest efektywnie 1-parametrowy w
y_ini, co go dobrze uwarunkowuje).
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from core.sg_background import SGParams
from core.sg_shooting import nelder_mead, shoot_omega_m, OMEGA_M_TARGET_PLANCK2018


# ── nelder_mead: testy niezależne od kosmologii ─────────────────────────

def test_nelder_mead_finds_minimum_of_simple_paraboloid():
    def f(point):
        x, y = point
        return (x - 3.0) ** 2 + (y + 2.0) ** 2

    (x, y), f_best, iterations = nelder_mead(f, x0=(0.0, 0.0), step=0.5, tol=1e-14, max_iter=500)
    assert x == pytest.approx(3.0, abs=1e-4)
    assert y == pytest.approx(-2.0, abs=1e-4)
    assert f_best == pytest.approx(0.0, abs=1e-6)
    assert iterations <= 500


def test_nelder_mead_finds_minimum_of_rosenbrock():
    """Klasyczna funkcja testowa dla optymalizatorów gradient-free -
    minimum w (1,1), wąska, zakrzywiona dolina (trudniejsza niż
    paraboloida, dobry test odporności samej implementacji)."""
    def f(point):
        x, y = point
        return (1.0 - x) ** 2 + 100.0 * (y - x ** 2) ** 2

    (x, y), f_best, _iterations = nelder_mead(f, x0=(-1.0, 1.0), step=0.3, tol=1e-14, max_iter=2000)
    assert x == pytest.approx(1.0, abs=1e-2)
    assert y == pytest.approx(1.0, abs=1e-2)
    assert f_best < 1e-3


def test_nelder_mead_respects_max_iter():
    def f(point):
        x, y = point
        return (x - 100.0) ** 2 + (y - 100.0) ** 2

    _point, _f_best, iterations = nelder_mead(f, x0=(0.0, 0.0), step=0.1, tol=0.0, max_iter=5)
    assert iterations <= 5


# ── shoot_omega_m: przypadek ξ=0 (dobrze uwarunkowany, 1D w praktyce) ──

def test_shoot_omega_m_converges_for_xi_zero():
    """Dla ξ=0, Ωm(N_f) zależy praktycznie tylko od y_ini (u jest
    odsprzężone, patrz test_sg_background.py) - łatwy, dobrze
    uwarunkowany przypadek do sprawdzenia, że cała pętla
    shoot->integrate->Nelder-Mead faktycznie zbiega do zadanego celu."""
    params = SGParams(lam=0.3, xi=0.0, beta=0.5)
    result = shoot_omega_m(
        params, N_i=0.0, N_f=-1.0, target=OMEGA_M_TARGET_PLANCK2018,
        u_ini_guess=0.0, y_ini_guess=0.5, n_steps=200, max_iter=300,
    )
    assert result.converged, result.message
    assert result.omega_m_final == pytest.approx(OMEGA_M_TARGET_PLANCK2018, abs=1e-3)


def test_shoot_omega_m_reports_failure_without_raising_when_start_is_unphysical():
    """Punkt startowy jawnie unphysical (Ωm<0 od razu) - funkcja ma
    zwrócić czytelny ShootingResult z converged=False, NIE wyrzucić
    wyjątku (SingularTrajectoryError jest łapany wewnątrz _omega_m_at_Nf)."""
    params = SGParams(lam=0.3, xi=0.0, beta=0.5)
    result = shoot_omega_m(
        params, N_i=0.0, N_f=-1.0, target=OMEGA_M_TARGET_PLANCK2018,
        u_ini_guess=0.0, y_ini_guess=10.0,  # Ωm(N_i)=1-100<0, jawnie unphysical
        n_steps=50, max_iter=5,
    )
    assert isinstance(result.converged, bool)
    assert isinstance(result.message, str)
