# ============================================================
#   SG SHOOTING — "double shooting" dla warunków początkowych
#   (u_ini, y_ini) tła SG, dopasowanych do Ωm(N_f) ≈ Ω_target
# ============================================================
"""
Z PDF: "min |Ωm(Nf) - Ω_target|, Ω_target ≈ 0.315" (Planck 2018).

UCZCIWIE — niedookreślenie problemu: to, co PDF podaje, to JEDEN cel
skalarny (Ωm w N_f) i DWIE wolne zmienne startowe (u_ini, y_ini). Dla
zadanej wartości Ωm(N_f) generycznie istnieje cała 1-parametrowa
rodzina par (u_ini, y_ini), które ją trafiają — nie pojedyncze
rozwiązanie. Fragment PDF przytoczony przez użytkownika nie podaje
drugiego warunku domykającego układ (np. dopasowania w_DE(N_f) albo
trafienia w konkretny punkt stały de Sittera na późnych czasach) — jeśli
taki warunek istnieje w źródle, dopisz go do `objective()` w
shoot_omega_m() (miejsce oznaczone komentarzem "DRUGI WARUNEK").

Implementacja: minimalizacja (Ωm(N_f)-target)² po (u_ini,y_ini) metodą
Neldera-Meada (podręcznikowy algorytm simplex, biblioteka standardowa —
w repo nie ma scipy, patrz brak requirements.txt), zgodnie z sugestią
PDF "Brent/Dekker / dowolny 1D/2D root finder". Trajektorie unphysical/
singular (patrz sg_background.SingularTrajectoryError) są karane dużą
wartością kary, żeby optymalizator omijał ten region przestrzeni
parametrów zamiast wywalać się wyjątkiem w środku minimalizacji.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from .sg_background import (
    SGParams,
    SingularTrajectoryError,
    integrate_background,
    omega_m,
)

OMEGA_M_TARGET_PLANCK2018 = 0.315  # Planck 2018 VI, ΛCDM — patrz PDF
_PENALTY = 1e6  # kara dla trajektorii unphysical/singular w funkcji celu


# ------------------------------------------------------------
# 1. Nelder-Mead (simplex) — generyczny minimalizator N-wymiarowy
# ------------------------------------------------------------

def nelder_mead(
    f: Callable[[tuple], float],
    x0: tuple,
    step: float = 0.1,
    tol: float = 1e-12,
    max_iter: int = 500,
) -> tuple:
    """Podręcznikowy Nelder-Mead (1965): reflect/expand/contract/shrink
    ze standardowymi współczynnikami (α=1, γ=2, ρ=0.5, σ=0.5) — nie
    autorska modyfikacja. Zatrzymuje się, gdy rozstrzał wartości f na
    simplexie spadnie poniżej tol, albo po max_iter iteracjach.

    Zwraca (x_best, f_best, iteracje)."""
    n = len(x0)
    alpha, gamma, rho, sigma = 1.0, 2.0, 0.5, 0.5

    simplex = [list(x0)]
    for i in range(n):
        point = list(x0)
        point[i] += step
        simplex.append(point)

    def score(p):
        return f(tuple(p))

    values = [score(p) for p in simplex]

    iteration = 0
    for iteration in range(1, max_iter + 1):
        order = sorted(range(len(simplex)), key=lambda i: values[i])
        simplex = [simplex[i] for i in order]
        values = [values[i] for i in order]

        if abs(values[-1] - values[0]) < tol:
            break

        centroid = [sum(p[j] for p in simplex[:-1]) / n for j in range(n)]
        worst = simplex[-1]

        reflected = [centroid[j] + alpha * (centroid[j] - worst[j]) for j in range(n)]
        f_reflected = score(reflected)

        if values[0] <= f_reflected < values[-2]:
            simplex[-1], values[-1] = reflected, f_reflected
            continue

        if f_reflected < values[0]:
            expanded = [centroid[j] + gamma * (reflected[j] - centroid[j]) for j in range(n)]
            f_expanded = score(expanded)
            if f_expanded < f_reflected:
                simplex[-1], values[-1] = expanded, f_expanded
            else:
                simplex[-1], values[-1] = reflected, f_reflected
            continue

        contracted = [centroid[j] + rho * (worst[j] - centroid[j]) for j in range(n)]
        f_contracted = score(contracted)
        if f_contracted < values[-1]:
            simplex[-1], values[-1] = contracted, f_contracted
            continue

        best = simplex[0]
        for i in range(1, len(simplex)):
            simplex[i] = [best[j] + sigma * (simplex[i][j] - best[j]) for j in range(n)]
            values[i] = score(simplex[i])

    order = sorted(range(len(simplex)), key=lambda i: values[i])
    return tuple(simplex[order[0]]), values[order[0]], iteration


# ------------------------------------------------------------
# 2. Double shooting: dopasowanie (u_ini, y_ini) do Ωm(N_f) ≈ target
# ------------------------------------------------------------

@dataclass
class ShootingResult:
    u_ini: float
    y_ini: float
    omega_m_final: float
    residual: float          # omega_m_final - target (nan jeśli nieudane)
    iterations: int
    converged: bool
    message: str


def _omega_m_at_Nf(
    u_ini: float, y_ini: float, params: SGParams, N_i: float, N_f: float, n_steps: int
) -> Optional[float]:
    """Całkuje tło i zwraca Ωm(N_f), albo None jeśli trajektoria okazała
    się unphysical/singular po drodze."""
    try:
        trajectory = integrate_background(
            u_ini, y_ini, params, N_i, N_f, n_steps=n_steps, check_physicality=True
        )
    except SingularTrajectoryError:
        return None
    final = trajectory[-1]
    return omega_m(final.u, final.x, final.y, params.xi)


def shoot_omega_m(
    params: SGParams,
    N_i: float,
    N_f: float = 0.0,
    target: float = OMEGA_M_TARGET_PLANCK2018,
    u_ini_guess: float = 0.0,
    y_ini_guess: float = 0.5,
    n_steps: int = 2000,
    max_iter: int = 500,
    tol: float = 1e-10,
    converged_atol: float = 1e-4,
) -> ShootingResult:
    """Szuka (u_ini, y_ini) minimalizujących (Ωm(N_f)-target)² metodą
    Neldera-Meada — patrz docstring modułu o niedookreśleniu problemu:
    wynik zależy od (u_ini_guess, y_ini_guess) i nie jest unikalny."""

    def objective(point: tuple) -> float:
        u_ini, y_ini = point
        om = _omega_m_at_Nf(u_ini, y_ini, params, N_i, N_f, n_steps)
        if om is None:
            return _PENALTY
        # DRUGI WARUNEK: jeśli PDF podaje dodatkowy cel (np. w_DE(N_f)),
        # dopisz go tutaj jako kolejny składnik sumy kwadratów.
        return (om - target) ** 2

    (u_ini, y_ini), _f_best, iterations = nelder_mead(
        objective, (u_ini_guess, y_ini_guess), step=0.05, tol=tol, max_iter=max_iter
    )

    om_final = _omega_m_at_Nf(u_ini, y_ini, params, N_i, N_f, n_steps)
    if om_final is None:
        return ShootingResult(
            u_ini, y_ini, float("nan"), float("nan"), iterations, False,
            "Nelder-Mead zbiegł do regionu unphysical/singular — spróbuj innego "
            "u_ini_guess/y_ini_guess.",
        )
    residual = om_final - target
    converged = abs(residual) < converged_atol
    message = "zbieżne" if converged else f"nie zbiegło w tolerancji: residuum={residual!r}"
    return ShootingResult(u_ini, y_ini, om_final, residual, iterations, converged, message)
