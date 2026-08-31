"""
test_sg_background.py — testy core/sg_background.py (tło kosmologii SG).

Zakres tego, co jest tu SPRAWDZANE (i uczciwie: co NIE jest):
- Arytmetyka wzorów D/Ωm/S na ręcznie policzonych liczbach - TAK.
- is_physical() poprawnie flaguje D<=0 i Ωm<=0 - TAK.
- RK4 poprawnie całkuje (na niezależnym, znanym analitycznie układzie,
  nie na samym układzie SG, żeby test integratora nie zależał od tego,
  czy równania SG są przepisane poprawnie) - TAK.
- integrate_background rzuca SingularTrajectoryError, gdy D<=0 już na
  starcie - TAK.
- Przypadek ξ=0 jako test regresyjny struktury układu (u odsprzężone od
  x,y, patrz test_xi_zero_decouples_u) - TAK.
- Zgodność całego modelu SG z literaturą scalar-Gauss-Bonnet - NIE
  (brak dostępu do źródłowej pracy, patrz docstring sg_background.py).
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from core.sg_background import (
    SGParams,
    SGState,
    D_expr,
    omega_m,
    S_expr,
    is_physical,
    background_derivatives,
    integrate_background,
    SingularTrajectoryError,
    SQRT6,
    _rk4_step,
)


# ── D_expr / omega_m — arytmetyka wprost ze wzoru ──────────────────────

def test_D_expr_at_u_zero_is_one():
    assert D_expr(u=0.0, xi=0.3) == 1.0


def test_D_expr_matches_hand_computed_value():
    # D = 1 - 6*0.1*2^2 - 36*0.1^2*2^4 = 1 - 2.4 - 5.76 = -7.16
    assert D_expr(u=2.0, xi=0.1) == pytest.approx(-7.16)


def _t_star_root(xi: float) -> float:
    """Dodatni pierwiastek t (t=u²) równania 36ξ²t² + 6ξt - 1 = 0
    (przepisane z D(t) = 1 - 6ξt - 36ξ²t² = 0) - policzony tu NIEZALEŻNIE
    od D_expr (wzór kwadratowy wprost), żeby test poniżej faktycznie
    sprawdzał D_expr, a nie porównywał go z samym sobą."""
    a = 36.0 * xi ** 2
    b = 6.0 * xi
    c = -1.0
    disc = b ** 2 - 4.0 * a * c
    root_plus = (-b + math.sqrt(disc)) / (2.0 * a)
    root_minus = (-b - math.sqrt(disc)) / (2.0 * a)
    return max(root_plus, root_minus)


def test_D_expr_has_real_zero_for_nonzero_xi():
    """POPRAWKA UŻYTKOWNIKA (2026-08-31): ze znakiem minus przed
    36ξ²u⁴, D = 1 - 6ξu² - 36ξ²u⁴ MA realne zero dla każdego ξ≠0 - w
    przeciwieństwie do pierwszej wersji formuły (plus), gdzie D był
    ograniczony z dołu przez 0.75 i nigdy nie osiągał zera (patrz
    historia w README.md i docstring modułu). Sprawdzone dla kilku
    wartości ξ (dodatnich i ujemnych) niezależnie policzonym
    pierwiastkiem kwadratowym."""
    for xi in (1.0, -1.0, 2.5, -0.3):
        t_star = _t_star_root(xi)
        assert t_star > 0
        u_star = math.sqrt(t_star)
        assert D_expr(u_star, xi) == pytest.approx(0.0, abs=1e-9)


def test_D_expr_still_one_at_u_zero_after_sign_fix():
    # regresja: zmiana znaku nie rusza D(u=0)=1 (oba człony z ξ znikają)
    assert D_expr(u=0.0, xi=2.7) == 1.0


def test_omega_m_at_origin_is_one():
    assert omega_m(u=0.0, x=0.0, y=0.0, xi=0.3) == 1.0


def test_omega_m_matches_hand_computed_value():
    # Ωm = 1 - 0.2^2 - 0.3^2 - 6*0.1*0.5^2 - 12*0.1*0.5*0.2
    # = 1 - 0.04 - 0.09 - 0.15 - 0.12 = 0.6
    result = omega_m(u=0.5, x=0.2, y=0.3, xi=0.1)
    assert result == pytest.approx(0.6)


# ── S_expr — dzielenie przez D (patrz docstring modułu) ────────────────

def test_S_expr_diverges_near_real_zero_of_D():
    """Sedno poprawki znaku: S dzieli przez D, a D ma teraz PRAWDZIWE
    zero (test_D_expr_has_real_zero_for_nonzero_xi) - |S| rośnie BEZ
    OGRANICZEŃ w miarę zbliżania się u do tego zera od strony D>0,
    dokładnie zgodnie z intuicją "śladem są miejsca zerowe D", którą
    użytkownik podał jako klucz do interpretacji formuły S."""
    xi = 1.0
    params = SGParams(lam=0.5, xi=xi, beta=0.5)
    u_star = math.sqrt(_t_star_root(xi))

    def s_at(fraction_of_u_star):
        return abs(S_expr(u=fraction_of_u_star * u_star, x=0.05, y=0.05, params=params))

    fractions = [0.5, 0.9, 0.99, 0.999]
    Ds = [D_expr(f * u_star, xi) for f in fractions]
    assert all(d > 0 for d in Ds)
    assert Ds == sorted(Ds, reverse=True)  # D maleje monotonicznie ku zeru
    Ss = [s_at(f) for f in fractions]
    assert Ss == sorted(Ss)  # |S| rośnie
    assert Ss[-1] > 500 * Ss[0]  # prawdziwa dywergencja, nie łagodny trend


def test_S_expr_raises_on_exact_D_zero():
    """D_expr() sam nigdy nie zwraca 0.0 dla rzeczywistych (u,ξ) (patrz
    test_D_expr_is_bounded_below_by_three_quarters) - więc żeby
    przetestować guard clause w S_expr() (ZeroDivisionError zamiast
    cichego zwrócenia inf), wymuszamy D=0 przez monkeypatch modułowej
    funkcji D_expr. To testuje kod obronny, nie prawdziwie osiągalny
    stan fizyczny."""
    import core.sg_background as bg_module

    params = SGParams(lam=0.1, xi=0.2, beta=0.5)
    original_D = bg_module.D_expr
    bg_module.D_expr = lambda u, xi: 0.0
    try:
        with pytest.raises(ZeroDivisionError):
            bg_module.S_expr(u=0.1, x=0.1, y=0.1, params=params)
    finally:
        bg_module.D_expr = original_D


# ── is_physical ──────────────────────────────────────────────────────

def test_is_physical_true_for_origin():
    params = SGParams(lam=0.5, xi=0.1, beta=0.5)
    state = SGState(u=0.0, x=0.0, y=0.0, ln_H=0.0)
    check = is_physical(state, params)
    assert check.physical
    assert check.reasons == []


def test_is_physical_flags_negative_omega_m():
    params = SGParams(lam=0.5, xi=0.0, beta=0.5)
    # xi=0 -> Ωm = 1 - x^2 - y^2 ; x=y=0.9 -> Ωm = 1-0.81-0.81 <0
    state = SGState(u=0.0, x=0.9, y=0.9, ln_H=0.0)
    check = is_physical(state, params)
    assert not check.physical
    assert any("Ωm" in r for r in check.reasons)


def test_is_physical_flags_nonpositive_D():
    import core.sg_background as bg_module

    params = SGParams(lam=0.1, xi=0.2, beta=0.5)
    state = SGState(u=0.1, x=0.0, y=0.0, ln_H=0.0)
    original_D = bg_module.D_expr
    bg_module.D_expr = lambda u, xi: -1.0
    try:
        check = bg_module.is_physical(state, params)
        assert not check.physical
        assert any(r.startswith("D=") for r in check.reasons)
    finally:
        bg_module.D_expr = original_D


# ── RK4: test integratora NIEZALEŻNY od układu SG ──────────────────────

def test_rk4_step_reproduces_known_exponential_decay():
    """Test samego mechanizmu RK4 (_rk4_step) na trywialnym, znanym
    analitycznie układzie y'=-y (rozwiązanie y=y0*exp(-t)), podmieniając
    background_derivatives przez monkeypatch - żeby test integratora NIE
    zależał od poprawności przepisania równań SG."""
    import core.sg_background as bg_module

    original = bg_module.background_derivatives
    # potraktuj "u" jako jedyną zmienną testową: u' = -u, reszta = 0
    bg_module.background_derivatives = lambda state, params: (-state.u, 0.0, 0.0, 0.0)
    try:
        params = SGParams(lam=0.0, xi=0.0, beta=0.0)
        state = SGState(u=1.0, x=0.0, y=0.0, ln_H=0.0)
        dN = 0.01
        for _ in range(100):  # N: 0 -> 1
            state = bg_module._rk4_step(state, params, dN)
        expected = math.exp(-1.0)
        assert state.u == pytest.approx(expected, rel=1e-6)
    finally:
        bg_module.background_derivatives = original


# ── integrate_background: warunki brzegowe i wyjątki ────────────────────

def test_integrate_background_sets_correct_initial_conditions():
    params = SGParams(lam=0.3, xi=0.05, beta=0.5)
    trajectory = integrate_background(u_ini=0.1, y_ini=0.4, params=params, N_i=-1.0, N_f=-1.0, n_steps=1)
    # N_i == N_f -> dN=0, jeden "krok" zerowej długości, stan startowy zachowany
    first = trajectory[0]
    assert first.u == 0.1
    assert first.x == 0.0
    assert first.y == 0.4
    assert first.ln_H == 0.0


def test_integrate_background_raises_when_initial_state_unphysical():
    params = SGParams(lam=0.3, xi=0.0, beta=0.5)
    # xi=0 -> Ωm=1-x^2-y^2 ; x=0 (wymuszone), y=1.5 -> Ωm=1-2.25<0 od startu
    with pytest.raises(SingularTrajectoryError):
        integrate_background(u_ini=0.0, y_ini=1.5, params=params, N_i=0.0, N_f=-1.0, n_steps=10)


def test_integrate_background_rejects_zero_steps():
    params = SGParams(lam=0.3, xi=0.05, beta=0.5)
    with pytest.raises(ValueError):
        integrate_background(u_ini=0.0, y_ini=0.1, params=params, N_i=0.0, N_f=-1.0, n_steps=0)


# ── ξ=0: test regresyjny struktury układu (u odsprzężone od x,y) ───────

def test_xi_zero_decouples_u_from_x_y():
    """Dla ξ=0 wszystkie człony z ξ znikają z x'/y'/S, więc (x,y) mają
    ewoluować NIEZALEŻNIE od u (u tylko "słucha" x poprzez u'=x, nie
    wpływa na nic innego) - sprawdzamy to uruchamiając całkowanie z
    dwoma różnymi u_ini przy tych samych (y_ini, params) i porównując
    trajektorie x(N), y(N) (powinny być identyczne, bo nie zależą od u)."""
    params = SGParams(lam=0.4, xi=0.0, beta=0.6)
    traj_a = integrate_background(u_ini=0.0, y_ini=0.3, params=params, N_i=0.0, N_f=-2.0, n_steps=200)
    traj_b = integrate_background(u_ini=5.0, y_ini=0.3, params=params, N_i=0.0, N_f=-2.0, n_steps=200)

    for a, b in zip(traj_a, traj_b):
        assert a.x == pytest.approx(b.x, abs=1e-9)
        assert a.y == pytest.approx(b.y, abs=1e-9)
        assert a.ln_H == pytest.approx(b.ln_H, abs=1e-9)
    # u sam w sobie MA się różnić (różne u_ini, ta sama dynamika u'=x)
    assert traj_a[-1].u != pytest.approx(traj_b[-1].u)


def test_background_derivatives_du_equals_x():
    """u' = x dosłownie - najprostszy, bezpośredni test jednej linijki
    wzoru bez pośrednictwa całego integratora."""
    params = SGParams(lam=0.2, xi=0.05, beta=0.5)
    state = SGState(u=0.1, x=0.37, y=0.2, ln_H=0.0)
    du, _dx, _dy, _dlnH = background_derivatives(state, params)
    assert du == state.x == 0.37


def test_background_derivatives_dlnH_equals_S_over_sqrt6():
    params = SGParams(lam=0.2, xi=0.05, beta=0.5)
    state = SGState(u=0.1, x=0.1, y=0.2, ln_H=0.0)
    _du, _dx, _dy, dlnH = background_derivatives(state, params)
    assert dlnH == pytest.approx(S_expr(state.u, state.x, state.y, params) / SQRT6)
