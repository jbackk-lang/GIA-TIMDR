"""
test_sg_perturbations.py — testy core/sg_perturbations.py.

Zakres: G_eff()/slip_eta() na ręcznie policzonych liczbach wprost ze
wzoru z PDF (bez własnej interpretacji). growth_derivatives()/
integrate_growth() na niezależnym, znanym analitycznie przypadku
(standardowy wzrost w ΛCDM z Geff=G, patrz test niżej). lensing_sigma()
na wartościach brzegowych. T_of_state/F_of_T/FT_of_T/G_eff_over_G i
background_functions_from_trajectory() testują domknięcie z prawdziwą
trajektorią tła (u(N),H(N)) - dopisane po tym, jak użytkownik podał
brakujące wcześniej mapowanie F(T)=1-ξT², F_T(T)=-2ξT, T=√6·u·H.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from core.sg_background import SGParams, SGState, integrate_background
from core.sg_perturbations import (
    G_eff,
    slip_eta,
    growth_derivatives,
    integrate_growth,
    lensing_sigma,
    GrowthPoint,
    T_of_state,
    F_of_T,
    FT_of_T,
    G_eff_over_G,
    G_eff_over_G_of_state,
    slip_eta_of_state,
    background_functions_from_trajectory,
)


# ── G_eff / slip_eta — arytmetyka wprost ze wzoru z PDF ─────────────────

def test_G_eff_reduces_to_1_over_8piF_when_FT_zero():
    # FT=0 -> Geff = 1/(8piF) * (1 + 0) = 1/(8piF)
    F = 2.0
    expected = 1.0 / (8.0 * math.pi * F)
    assert G_eff(F, FT=0.0) == pytest.approx(expected)


def test_G_eff_matches_hand_computed_value():
    # F=1, FT=1: denom=2*1+3*1=5, Geff = 1/(8pi) * (1 + 1/5) = 1/(8pi) * 1.2
    expected = (1.0 / (8.0 * math.pi)) * 1.2
    assert G_eff(F=1.0, FT=1.0) == pytest.approx(expected)


def test_G_eff_raises_on_zero_F():
    with pytest.raises(ValueError):
        G_eff(F=0.0, FT=0.5)


def test_G_eff_raises_when_denominator_vanishes():
    # 2F+3FT^2=0 przy F=-1.5, FT=1 (F ujemne, ale test sprawdza tylko guard matematyczny)
    with pytest.raises(ValueError):
        G_eff(F=-1.5, FT=1.0)


def test_slip_eta_is_one_when_FT_zero():
    # FT=0 -> eta = F / F = 1 (brak slipu bez poprawki tensorowej)
    assert slip_eta(F=3.7, FT=0.0) == pytest.approx(1.0)


def test_slip_eta_matches_hand_computed_value():
    # F=1, FT=1: eta = (1+2)/(1+4) = 3/5 = 0.6
    assert slip_eta(F=1.0, FT=1.0) == pytest.approx(0.6)


def test_slip_eta_raises_when_denominator_vanishes():
    with pytest.raises(ValueError):
        slip_eta(F=-4.0, FT=1.0)  # F+4FT^2 = -4+4 = 0


# ── growth/RSD: test na znanym analitycznie przypadku ΛCDM-podobnym ────

def test_growth_derivatives_matches_hand_computed_value():
    ddelta, dddelta = growth_derivatives(
        delta=2.0, ddelta_dN=0.5,
        omega_m_of_N=0.3, hprime_over_h_of_N=-1.2, geff_over_g_of_N=1.0,
    )
    assert ddelta == 0.5
    # dddelta = -(2-1.2)*0.5 + 1.5*0.3*1.0*2.0 = -0.4 + 0.9 = 0.5
    assert dddelta == pytest.approx(0.5)


def test_integrate_growth_matter_domination_power_law():
    """Test NIEZALEŻNY od sg_background/SG: w erze zdominowanej przez
    materię ze standardową grawitacją (Geff/G=1, Ωm=1, H'/H=-3/2 - stałe
    w czasie e-foldów, jak dla a∝t^(2/3)) rozwiązaniem rosnącym równania
    wzrostu jest δ∝a=e^N (znany wynik podręcznikowy) - sprawdzamy, że
    integrate_growth to odtwarza z warunkiem początkowym dopasowanym do
    tego trybu (δ'=δ)."""
    const_omega_m = lambda N: 1.0
    const_hprime_over_h = lambda N: -1.5
    const_geff_over_g = lambda N: 1.0

    N_i, N_f = 0.0, 2.0
    delta_ini = 1.0
    points = integrate_growth(
        delta_ini=delta_ini, ddelta_dN_ini=delta_ini,  # δ'=δ dla trybu rosnącego δ∝e^N
        N_i=N_i, N_f=N_f,
        omega_m_fn=const_omega_m, hprime_over_h_fn=const_hprime_over_h,
        geff_over_g_fn=const_geff_over_g, n_steps=1000,
    )
    final = points[-1]
    expected = delta_ini * math.exp(N_f - N_i)
    assert final.delta == pytest.approx(expected, rel=1e-4)
    assert final.growth_rate_f == pytest.approx(1.0, abs=1e-3)  # f=1 dla δ∝e^N


def test_integrate_growth_rejects_zero_steps():
    with pytest.raises(ValueError):
        integrate_growth(
            1.0, 1.0, 0.0, 1.0,
            lambda N: 0.3, lambda N: -1.5, lambda N: 1.0, n_steps=0,
        )


def test_growth_point_growth_rate_f_nan_when_delta_zero():
    point = GrowthPoint(N=0.0, delta=0.0, ddelta_dN=1.0)
    assert math.isnan(point.growth_rate_f)


# ── lensing_sigma ────────────────────────────────────────────────────

def test_lensing_sigma_reduces_to_geff_when_no_slip():
    # eta=1 (brak slipu) -> Sigma = Geff*(1+1)/2 = Geff
    assert lensing_sigma(geff_over_g=1.3, eta=1.0) == pytest.approx(1.3)


def test_lensing_sigma_matches_hand_computed_value():
    # Geff/G=2.0, eta=0.6 -> Sigma = 2.0*1.6/2 = 1.6
    assert lensing_sigma(geff_over_g=2.0, eta=0.6) == pytest.approx(1.6)


# ── T_of_state / F_of_T / FT_of_T — domknięcie z tłem ───────────────────

def test_T_of_state_matches_definition():
    # T = sqrt(6) * u * H ; H = exp(ln_H)
    state = SGState(u=0.2, x=0.0, y=0.0, ln_H=math.log(2.0))
    expected = math.sqrt(6.0) * 0.2 * 2.0
    assert T_of_state(state) == pytest.approx(expected)


def test_F_of_T_matches_hand_computed_value():
    # F(T) = 1 - xi*T^2 ; xi=0.1, T=2 -> 1 - 0.1*4 = 0.6
    assert F_of_T(T=2.0, xi=0.1) == pytest.approx(0.6)


def test_FT_of_T_matches_hand_computed_value():
    # FT(T) = -2*xi*T ; xi=0.1, T=2 -> -0.4
    assert FT_of_T(T=2.0, xi=0.1) == pytest.approx(-0.4)


def test_G_eff_over_G_is_one_in_GR_limit():
    # F=1, FT=0 (xi=0 -> F=1, FT=0 dla dowolnego T) -> Geff/G=1 (standardowa grawitacja)
    assert G_eff_over_G(F=1.0, FT=0.0) == pytest.approx(1.0)


def test_G_eff_over_G_of_state_chain_matches_manual_computation():
    """Sprawdza cały łańcuch state -> T -> F,FT -> Geff/G daje to samo,
    co ręczne złożenie tych samych funkcji krok po kroku."""
    xi = 0.05
    state = SGState(u=0.3, x=0.1, y=0.2, ln_H=0.0)  # H=exp(0)=1
    T = T_of_state(state)
    expected = G_eff_over_G(F_of_T(T, xi), FT_of_T(T, xi))
    assert G_eff_over_G_of_state(state, xi) == pytest.approx(expected)


def test_slip_eta_of_state_chain_matches_manual_computation():
    xi = 0.05
    state = SGState(u=0.3, x=0.1, y=0.2, ln_H=0.0)
    T = T_of_state(state)
    expected = slip_eta(F_of_T(T, xi), FT_of_T(T, xi))
    assert slip_eta_of_state(state, xi) == pytest.approx(expected)


def test_G_eff_over_G_of_state_reduces_to_one_when_xi_zero():
    # xi=0 -> F=1, FT=0 niezależnie od stanu -> Geff/G=1 (GR)
    state = SGState(u=5.0, x=-2.0, y=3.0, ln_H=1.0)
    assert G_eff_over_G_of_state(state, xi=0.0) == pytest.approx(1.0)
    assert slip_eta_of_state(state, xi=0.0) == pytest.approx(1.0)


# ── background_functions_from_trajectory: interpolacja + wpięcie end-to-end ──

def test_background_functions_from_trajectory_interpolates_exactly_at_nodes():
    """W punktach WĘZŁOWYCH (dokładnie tych N, dla których mamy stan z
    trajektorii) interpolacja liniowa musi zwrócić dokładnie policzoną
    wartość, nie przybliżenie."""
    params = SGParams(lam=0.2, xi=0.02, beta=0.5)
    N_i, N_f = 0.0, -1.0
    trajectory = integrate_background(u_ini=0.05, y_ini=0.3, params=params, N_i=N_i, N_f=N_f, n_steps=10)
    bg = background_functions_from_trajectory(trajectory, N_i, N_f, params)

    n = len(trajectory) - 1
    dN = (N_f - N_i) / n
    for i, state in enumerate(trajectory):
        N = N_i + i * dN
        from core.sg_background import omega_m as omega_m_expr, background_derivatives
        expected_omega_m = omega_m_expr(state.u, state.x, state.y, params.xi)
        expected_hprime = background_derivatives(state, params)[3]
        expected_geff = G_eff_over_G_of_state(state, params.xi)
        expected_eta = slip_eta_of_state(state, params.xi)
        assert bg.omega_m_fn(N) == pytest.approx(expected_omega_m)
        assert bg.hprime_over_h_fn(N) == pytest.approx(expected_hprime)
        assert bg.geff_over_g_fn(N) == pytest.approx(expected_geff)
        assert bg.eta_fn(N) == pytest.approx(expected_eta)


def test_background_functions_from_trajectory_rejects_single_point():
    with pytest.raises(ValueError):
        background_functions_from_trajectory(
            [SGState(u=0.0, x=0.0, y=0.0, ln_H=0.0)], N_i=0.0, N_f=0.0,
            params=SGParams(lam=0.1, xi=0.1, beta=0.5),
        )


def test_growth_driven_by_real_sg_background_trajectory():
    """Test end-to-end: prawdziwa trajektoria tła SG (integrate_background)
    -> background_functions_from_trajectory -> integrate_growth. Sprawdza
    tylko, że pipeline faktycznie działa i daje skończone, sensowne
    liczby (nie NaN/inf) - NIE zgodność z jakąś znaną wartością
    obserwacyjną (patrz zastrzeżenia w README/docstringach o braku
    niezależnej weryfikacji fizyki modelu SG)."""
    xi = 0.02  # małe xi, żeby F=1-xi*T^2 nie zszedł do zera/ujemnych po drodze
    params = SGParams(lam=0.2, xi=xi, beta=0.5)
    N_i, N_f = 0.0, -3.0
    trajectory = integrate_background(u_ini=0.05, y_ini=0.3, params=params, N_i=N_i, N_f=N_f, n_steps=300)
    bg = background_functions_from_trajectory(trajectory, N_i, N_f, params)

    points = integrate_growth(
        delta_ini=1.0, ddelta_dN_ini=1.0, N_i=N_i, N_f=N_f,
        omega_m_fn=bg.omega_m_fn, hprime_over_h_fn=bg.hprime_over_h_fn,
        geff_over_g_fn=bg.geff_over_g_fn, n_steps=300,
    )

    assert len(points) == 301
    for p in points:
        assert math.isfinite(p.delta)
        assert math.isfinite(p.ddelta_dN)

    # lensing Sigma wzdłuż tej samej trajektorii - też powinno być skończone
    for state in trajectory[::50]:
        geff_g = G_eff_over_G_of_state(state, xi)
        eta = slip_eta_of_state(state, xi)
        sigma = lensing_sigma(geff_g, eta)
        assert math.isfinite(sigma)
