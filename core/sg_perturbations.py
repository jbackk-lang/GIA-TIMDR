# ============================================================
#   SG PERTURBATIONS — Geff, slip η, wzrost struktur (growth/RSD),
#   soczewkowanie grawitacyjne (lensing/WL) dla modelu SG
# ============================================================
"""
Z PDF:

    k²Φ = -4π Geff a² ρ_m δ_m
    Geff = 1/(8πF) · (1 + FT²/(2F+3FT²))
    η = (F + 2FT²) / (F + 4FT²)

Domknięcie z tłem (dopisane przez użytkownika, 2026-08-31, po pytaniu o
brakujące ogniwo F(u)/F_T(u)):

    F(T)  = 1 - ξT²
    F_T(T) = dF/dT = -2ξT
    T(N)  = √6 · u(N) · H(N)          (wprost z u = T/(√6 H), sg_background.py)

Ten łańcuch (SGState -> T_of_state -> F_of_T/FT_of_T -> G_eff/slip_eta)
jest zaimplementowany w sekcji 0 niżej — Geff(N)/η(N) dają się teraz
policzyć z PRAWDZIWEJ trajektorii tła (u(N),H(N)) zwróconej przez
sg_background.integrate_background(), nie tylko z ręcznie podanych F/FT.

Moduły "growth/RSD" i "lensing/WL", do których PDF każe wpiąć Geff/η,
NIE ISTNIAŁY wcześniej nigdzie w tym repo (sprawdzone: brak jakiegokolwiek
pliku/funkcji z "growth", "RSD" czy "lensing" w GIA-TIMDR przed tą
zmianą) — to, co niżej, to nowy, minimalny, ale samodzielnie działający
i przetestowany kod, nie podłączenie do czegoś gotowego.

Równanie wzrostu liniowego (growth_derivatives/integrate_growth) to
STANDARDOWA postać z literatury MG (np. Pogosian & Silvestri 2016):

    δ'' + (2 + H'/H) δ' - (3/2) Ωm (Geff/G) δ = 0        (' = d/dN)

— H'/H = (ln H)' jest DOKŁADNIE tym, co już liczy
sg_background.background_derivatives() (czwarta składowa), więc trajektoria
tła daje ten wkład za darmo, bez dodatkowych założeń. Geff/G (bezwymiarowe,
patrz G_eff_over_G) to osobny wkład z tego samego łańcucha F(T)/F_T(T).

Soczewkowanie (lensing_sigma) używa Σ = Geff·(1+η)/2 — STANDARDOWA
kombinacja z literatury (Pogosian & Silvestri 2016, notacja Σ/μ/γ),
NIE wzór podany w PDF użytkownika — do potwierdzenia/zmiany, jeśli
źródłowa praca definiuje to inaczej.
"""
from __future__ import annotations

import bisect
import math
from dataclasses import dataclass
from typing import Callable, List, Sequence

from .sg_background import SGState, SQRT6


# ------------------------------------------------------------
# 0. Mapowanie F(T)/F_T(T) i T(u,H) — wiąże Geff/η z trajektorią tła
# ------------------------------------------------------------

def T_of_state(state: SGState) -> float:
    """T = √6 · u · H, wprost z definicji u = T/(√6 H) (sg_background.py) -
    odwrócone względem u, korzystając z H=exp(ln_H) już policzonego w
    trajektorii tła."""
    return SQRT6 * state.u * state.H


def F_of_T(T: float, xi: float) -> float:
    """F(T) = 1 - ξT² (dopisane przez użytkownika, 2026-08-31)."""
    return 1.0 - xi * T ** 2


def FT_of_T(T: float, xi: float) -> float:
    """F_T(T) = dF/dT = -2ξT (dopisane przez użytkownika, 2026-08-31)."""
    return -2.0 * xi * T


def G_eff_over_G(F: float, FT: float) -> float:
    """Geff/G — bezwymiarowy stosunek do standardowej grawitacji. W
    granicy GR (F=1, FT=0) G_eff() zwraca 1/(8π) (patrz jego wzór) —
    czyli w tych jednostkach G=1/(8π), więc Geff/G = 8π·Geff. To jest
    dokładnie ta wartość (bezwymiarowa, =1 w granicy GR), którą trzeba
    podać jako geff_over_g_of_N do growth_derivatives()/
    integrate_growth() w sekcji 2 — NIE surowe G_eff() (ma jednostki
    1/(8π), nie 1)."""
    return 8.0 * math.pi * G_eff(F, FT)


def G_eff_over_G_of_state(state: SGState, xi: float) -> float:
    """Geff/G policzone wprost z prawdziwego stanu tła (u,H): state ->
    T_of_state -> F_of_T/FT_of_T -> G_eff_over_G."""
    T = T_of_state(state)
    return G_eff_over_G(F_of_T(T, xi), FT_of_T(T, xi))


def slip_eta_of_state(state: SGState, xi: float) -> float:
    """η policzone wprost z prawdziwego stanu tła (u,H), tym samym
    łańcuchem co G_eff_over_G_of_state."""
    T = T_of_state(state)
    return slip_eta(F_of_T(T, xi), FT_of_T(T, xi))


# ------------------------------------------------------------
# 1. Geff i slip η — bezpośrednio z PDF, funkcje F, FT
# ------------------------------------------------------------

def G_eff(F: float, FT: float) -> float:
    """Geff = 1/(8πF) · (1 + FT²/(2F+3FT²))

    F, FT > 0 zakładane fizycznie (F to efektywna masa Plancka² -
    musi być dodatnia, żeby grawitacja nie zmieniła znaku; FT to
    poprawka tensorowa/GB). Rzuca ValueError przy F=0 albo przy
    zerowaniu się mianownika (2F+3FT²)=0, zamiast po cichu zwrócić inf."""
    if F == 0.0:
        raise ValueError("F=0 - Geff niezdefiniowane (dzielenie przez zero)")
    denom = 2.0 * F + 3.0 * FT ** 2
    if denom == 0.0:
        raise ValueError("2F+3FT²=0 - Geff niezdefiniowane (dzielenie przez zero)")
    return (1.0 / (8.0 * math.pi * F)) * (1.0 + (FT ** 2) / denom)


def slip_eta(F: float, FT: float) -> float:
    """η = (F + 2FT²) / (F + 4FT²)

    Rzuca ValueError przy zerowaniu się mianownika (F+4FT²)=0."""
    denom = F + 4.0 * FT ** 2
    if denom == 0.0:
        raise ValueError("F+4FT²=0 - η niezdefiniowane (dzielenie przez zero)")
    return (F + 2.0 * FT ** 2) / denom


# ------------------------------------------------------------
# 2. Growth/RSD — równanie wzrostu liniowego z Geff
# ------------------------------------------------------------

def growth_derivatives(
    delta: float,
    ddelta_dN: float,
    omega_m_of_N: float,
    hprime_over_h_of_N: float,
    geff_over_g_of_N: float,
) -> tuple:
    """Prawa strona rozłożonego na I rząd równania wzrostu:

        δ'  = ddelta_dN
        δ'' = -(2 + H'/H) δ' + (3/2) Ωm (Geff/G) δ

    Wszystkie trzy "of_N" argumenty to wartości W JEDNYM punkcie N
    (Ωm(N), H'/H(N)=(lnH)'(N), Geff(N)/G) — integrate_growth() woła to
    z funkcji dostarczonych przez wywołującego (np. odczytanych z
    trajektorii sg_background, albo z zewnętrznego modelu)."""
    dddelta = -(2.0 + hprime_over_h_of_N) * ddelta_dN + 1.5 * omega_m_of_N * geff_over_g_of_N * delta
    return (ddelta_dN, dddelta)


@dataclass
class GrowthPoint:
    N: float
    delta: float
    ddelta_dN: float

    @property
    def growth_rate_f(self) -> float:
        """f = δ'/δ = dlnδ/dN - tempo wzrostu (wchodzi do obserwabli RSD
        fσ8). NaN jeśli δ=0 w tym punkcie."""
        if self.delta == 0.0:
            return float("nan")
        return self.ddelta_dN / self.delta


def integrate_growth(
    delta_ini: float,
    ddelta_dN_ini: float,
    N_i: float,
    N_f: float,
    omega_m_fn: Callable[[float], float],
    hprime_over_h_fn: Callable[[float], float],
    geff_over_g_fn: Callable[[float], float],
    n_steps: int = 2000,
) -> List[GrowthPoint]:
    """Całkuje równanie wzrostu od N_i do N_f metodą RK4 (biblioteka
    standardowa), pobierając Ωm(N), H'/H(N), Geff(N)/G z dostarczonych
    funkcji jednej zmiennej (N) - dzięki temu ten sam solver działa
    zarówno z prawdziwą trajektorią tła SG (funkcje zbudowane przez
    background_functions_from_trajectory() w sekcji 4, patrz
    tests/test_sg_perturbations.py::test_growth_driven_by_real_sg_background_trajectory),
    jak i z dowolnym innym modelem tła, bez zmian w kodzie."""
    if n_steps < 1:
        raise ValueError("n_steps musi być >= 1")

    def deriv(N: float, delta: float, ddelta: float) -> tuple:
        return growth_derivatives(
            delta, ddelta, omega_m_fn(N), hprime_over_h_fn(N), geff_over_g_fn(N)
        )

    dN = (N_f - N_i) / n_steps
    N = N_i
    delta, ddelta = delta_ini, ddelta_dN_ini
    points = [GrowthPoint(N, delta, ddelta)]

    for _ in range(n_steps):
        k1 = deriv(N, delta, ddelta)
        k2 = deriv(N + dN / 2.0, delta + dN / 2.0 * k1[0], ddelta + dN / 2.0 * k1[1])
        k3 = deriv(N + dN / 2.0, delta + dN / 2.0 * k2[0], ddelta + dN / 2.0 * k2[1])
        k4 = deriv(N + dN, delta + dN * k3[0], ddelta + dN * k3[1])

        delta = delta + (dN / 6.0) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        ddelta = ddelta + (dN / 6.0) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        N += dN
        points.append(GrowthPoint(N, delta, ddelta))

    return points


# ------------------------------------------------------------
# 3. Lensing/WL — kombinacja Σ z Geff i η
# ------------------------------------------------------------

def lensing_sigma(geff_over_g: float, eta: float) -> float:
    """Σ = Geff·(1+η)/2 - standardowa (Pogosian & Silvestri 2016)
    efektywna siła grawitacji dla soczewkowania (wchodzi do równania
    Poissona dla Φ+Ψ, które widzą fotony). NIE jest to wzór podany w
    PDF użytkownika - patrz docstring modułu."""
    return geff_over_g * (1.0 + eta) / 2.0


# ------------------------------------------------------------
# 4. Wiring do prawdziwej trajektorii tła (integrate_background)
# ------------------------------------------------------------

@dataclass
class BackgroundFunctions:
    """Cztery funkcje N -> wartość, zbudowane przez interpolację liniową
    nad trajektorią tła - dokładnie te, których potrzebuje
    integrate_growth() (omega_m_fn, hprime_over_h_fn, geff_over_g_fn) i
    lensing (eta_fn), żeby jechać na PRAWDZIWEJ, policzonej trajektorii
    (u(N),H(N)) zamiast na ręcznie podanych stałych."""
    omega_m_fn: Callable[[float], float]
    hprime_over_h_fn: Callable[[float], float]
    geff_over_g_fn: Callable[[float], float]
    eta_fn: Callable[[float], float]


def _linear_interp(x: float, xs: Sequence[float], ys: Sequence[float]) -> float:
    """Interpolacja liniowa xs (rosnąco lub malejąco) -> ys, z
    przycięciem (clamp) do wartości brzegowej poza zakresem xs - bez
    numpy/scipy (brak w tym repo)."""
    n = len(xs)
    if n == 1:
        return ys[0]
    increasing = xs[-1] >= xs[0]
    keys = xs if increasing else list(reversed(xs))
    vals = ys if increasing else list(reversed(ys))

    if x <= keys[0]:
        return vals[0]
    if x >= keys[-1]:
        return vals[-1]

    i = bisect.bisect_right(keys, x) - 1
    i = max(0, min(i, n - 2))
    x0, x1 = keys[i], keys[i + 1]
    y0, y1 = vals[i], vals[i + 1]
    if x1 == x0:
        return y0
    t = (x - x0) / (x1 - x0)
    return y0 + t * (y1 - y0)


def background_functions_from_trajectory(
    trajectory: Sequence[SGState],
    N_i: float,
    N_f: float,
    params,  # SGParams — bez importu typu, żeby uniknąć zależności cyklicznej w adnotacjach
) -> BackgroundFunctions:
    """Buduje Ωm(N), H'/H(N), Geff(N)/G, η(N) przez interpolację liniową
    nad trajektorią zwróconą przez sg_background.integrate_background()
    (lista SGState w RÓWNYCH krokach N od N_i do N_f - dokładnie to, co
    ta funkcja zwraca, więc N-y są tu rekonstruowane, nie przechowywane
    osobno). Wynik podłącza się bezpośrednio pod integrate_growth():

        traj = integrate_background(u_ini, y_ini, params, N_i, N_f)
        bg = background_functions_from_trajectory(traj, N_i, N_f, params)
        points = integrate_growth(1.0, 1.0, N_i, N_f,
                                   bg.omega_m_fn, bg.hprime_over_h_fn, bg.geff_over_g_fn)
    """
    from .sg_background import omega_m as omega_m_expr, background_derivatives

    n = len(trajectory) - 1
    if n < 1:
        raise ValueError("trajektoria musi mieć co najmniej 2 punkty")
    dN = (N_f - N_i) / n
    Ns = [N_i + i * dN for i in range(n + 1)]

    omega_m_vals = [omega_m_expr(s.u, s.x, s.y, params.xi) for s in trajectory]
    hprime_over_h_vals = [background_derivatives(s, params)[3] for s in trajectory]
    geff_over_g_vals = [G_eff_over_G_of_state(s, params.xi) for s in trajectory]
    eta_vals = [slip_eta_of_state(s, params.xi) for s in trajectory]

    return BackgroundFunctions(
        omega_m_fn=lambda N: _linear_interp(N, Ns, omega_m_vals),
        hprime_over_h_fn=lambda N: _linear_interp(N, Ns, hprime_over_h_vals),
        geff_over_g_fn=lambda N: _linear_interp(N, Ns, geff_over_g_vals),
        eta_fn=lambda N: _linear_interp(N, Ns, eta_vals),
    )
