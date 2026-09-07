# ============================================================
#   SG BACKGROUND — tło kosmologiczne scalar-Gauss-Bonnet (SG)
#   w zmiennych zredukowanych TIMDR (u, x, y, ln H)
# ============================================================
"""
Mapowanie zmiennych (z PDF źródłowego, sekcja "Mapowanie zmiennych SG na TIMDR"):

    u = T / (√6 H)      — geometryczne przesunięcie pola (TIMDR: displacement)
    x = Ṫ / (√6 H)      — prędkość pola (TIMDR: velocity)
    y = √V / (√3 H)     — kanał amplitudy potencjału (TIMDR: potential amplitude channel)

gdzie T to pole skalarne SG, H to parametr Hubble'a, V to potencjał
pola, kropka to d/dt. Zmienna niezależna to liczba e-foldów N = ln(a),
prim (') = d/dN w całym tym module.

UWAGA o formule S (ważne dla poprawności całego modułu): w tekście
wklejonym przez użytkownika z PDF nie było widocznej kreski ułamkowej
między resztą wyrażenia a D — w przeciwieństwie do równań u'/x'/y',
gdzie \\frac{...}{...} zostało jawnie skopiowane. Po dopytaniu
użytkownika (2026-08-31, "daj do nieskończoności, tropem jest tu
intuicja miejsc zerowych"): D jest w MIANOWNIKU S (S = [...] / D), nie
mnoży — potwierdzone jako świadomy wybór: trajektoria ma być faktycznie
osobliwa (S → ±∞) w miejscach zerowych D, zgodnie z warunkiem
fizyczności "D>0" opisanym w PDF ("unphysical/singular trajectory" gdy
D<=0). Patrz is_physical() i SingularTrajectoryError.

UWAGA o znaku przy 36ξ²u⁴ (poprawka użytkownika, 2026-08-31): pierwsza
wersja tego modułu miała D = 1 - 6ξu² + 36ξ²u⁴ (plus) — dowiedzione
wtedy (patrz test_D_expr_is_bounded_below_by_three_quarters w historii
testów), że przy TYM znaku D ma minimum globalne = 0.75 dla
WSZYSTKICH rzeczywistych u,ξ i NIGDY nie osiąga zera - sprzeczne z
ideą "śladem są miejsca zerowe D". Użytkownik potwierdził (podstawienie
z=ξu², D(z)=1-6z+36z², wierzchołek z_min=6/(2·36)=1/12,
D_min=1-6/12+36/144=1-0.5+0.25=0.75 - dokładnie ten sam rachunek), że
w PDF przed 36ξ²u⁴ jest MINUS:

    D = 1 - 6ξu² - 36ξ²u⁴

Przy tym znaku D(t=u²) to funkcja wklęsła w dół (współczynnik przy t²
jest teraz ujemny) z D(0)=1>0 i D→-∞ przy t→∞ dla dowolnego ξ≠0 - więc
D MA realne zero dla dowolnego ξ≠0 (dowód i dokładna wartość zera w
test_D_expr_has_real_zero_for_nonzero_xi), a warunek fizyczności "D>0"
jest sensowny (może być naruszony) i S faktycznie dywerguje w tym
punkcie, tak jak sugerowała intuicja "miejsc zerowych".

UCZCIWIE: to jest transkrypcja wzorów podanych przez użytkownika z
zewnętrznego PDF, NIE niezależna weryfikacja fizyki tego modelu
scalar-Gauss-Bonnet (nie mam dostępu do źródłowej pracy). Sprawdzone
zostały tylko: spójność wewnętrzna (patrz test_sg_background.py: RK4
odtwarza znane rozwiązania prostych układów, D ma realne zero i S
faktycznie dywerguje w jego pobliżu), nie zgodność z literaturą SG.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


# ------------------------------------------------------------
# 1. Parametry modelu i stan tła
# ------------------------------------------------------------

@dataclass(frozen=True)
class SGParams:
    """Stałe parametry modelu SG (nie zmieniają się w czasie całkowania)."""
    lam: float    # λ — sprzężenie potencjału pola skalarnego
    xi: float     # ξ — sprzężenie Gaussa-Bonneta
    beta: float   # β — parametr kinetyczny


@dataclass
class SGState:
    """Stan tła w jednym punkcie N (e-fold)."""
    u: float       # przesunięcie geometryczne pola
    x: float       # prędkość pola
    y: float       # kanał amplitudy potencjału (y = √V / (√3 H), z definicji y >= 0)
    ln_H: float    # ln(H) — do odzyskania H = exp(ln_H) bez utraty precyzji

    def as_tuple(self) -> tuple:
        return (self.u, self.x, self.y, self.ln_H)

    @property
    def H(self) -> float:
        return math.exp(self.ln_H)


# ------------------------------------------------------------
# 2. Wyrażenia pomocnicze: D, Ωm, S
# ------------------------------------------------------------

def D_expr(u: float, xi: float) -> float:
    """D = 1 - 6ξu² - 36ξ²u⁴ — wyznacznik układu (mianownik S). D=0
    oznacza trajektorię osobliwą (patrz docstring modułu i
    is_physical()) - ze znakiem minus przed 36ξ²u⁴ (poprawka
    użytkownika, 2026-08-31) D ma realne zero dla każdego ξ≠0, patrz
    test_D_expr_has_real_zero_for_nonzero_xi."""
    return 1.0 - 6.0 * xi * u ** 2 - 36.0 * xi ** 2 * u ** 4


def omega_m(u: float, x: float, y: float, xi: float) -> float:
    """Ωm = 1 - x² - y² - 6ξu² - 12ξux — związek Friedmanna (domknięcie
    układu): udział materii NIE jest osobną zmienną całkowaną, tylko
    wyliczaną algebraicznie z (u,x,y) w każdym punkcie."""
    return 1.0 - x ** 2 - y ** 2 - 6.0 * xi * u ** 2 - 12.0 * xi * u * x


def S_expr(u: float, x: float, y: float, params: SGParams) -> float:
    """S = [6x²(2β-1) - 48ξux + 6ξλy² - 144ξ²u² - 3Ωm²] / D

    Człon źródłowy równania (lnH)' i sprzężenie zwrotne w x'/y'. DZIELI
    przez D (patrz docstring modułu — potwierdzone przez użytkownika:
    trajektoria jest osobliwa przy D=0, więc to jest ułamek, nie
    mnożenie)."""
    xi, lam, beta = params.xi, params.lam, params.beta
    om = omega_m(u, x, y, xi)
    numerator = (
        6.0 * x ** 2 * (2.0 * beta - 1.0)
        - 48.0 * xi * u * x
        + 6.0 * xi * lam * y ** 2
        - 144.0 * xi ** 2 * u ** 2
        - 3.0 * om ** 2
    )
    D = D_expr(u, xi)
    if D == 0.0:
        raise ZeroDivisionError(
            "D=0 - trajektoria osobliwa (patrz is_physical()); S niezdefiniowane w tym punkcie"
        )
    return numerator / D


# ------------------------------------------------------------
# 3. Warunek fizyczności
# ------------------------------------------------------------

@dataclass
class PhysicalityCheck:
    physical: bool
    D: float
    omega_m: float
    reasons: list = field(default_factory=list)  # naruszone warunki (puste jeśli physical=True)


def is_physical(state: SGState, params: SGParams) -> PhysicalityCheck:
    """Sprawdza D>0 oraz Ωm>0 — dwa warunki fizyczności/stabilności z
    PDF. Zwraca obiekt z flagą physical i listą naruszonych warunków,
    żeby wywołujący (np. shooting) mógł odrzucić/oznaczyć trajektorię
    jako unphysical/singular bez zgadywania z samego wyjątku."""
    D = D_expr(state.u, params.xi)
    om = omega_m(state.u, state.x, state.y, params.xi)
    reasons = []
    if not (D > 0.0):
        reasons.append(f"D={D!r} <= 0 (wymagane D>0)")
    if not (om > 0.0):
        reasons.append(f"Ωm={om!r} <= 0 (wymagane Ωm>0)")
    return PhysicalityCheck(physical=not reasons, D=D, omega_m=om, reasons=reasons)


# ------------------------------------------------------------
# 4. Układ równań tła (prawa strona, prim = d/dN)
# ------------------------------------------------------------

SQRT6 = math.sqrt(6.0)


def background_derivatives(state: SGState, params: SGParams) -> tuple:
    """Prawa strona układu autonomicznego tła SG:

        u' = x
        x' = -3x - λy²/√6 - 12ξu - S·(x + 6ξu)
        y' = -λxy - Sy
        (lnH)' = S/√6

    Zwraca (u', x', y', (lnH)') jako krotkę (ten sam porządek co
    SGState.as_tuple(), żeby dało się bezpośrednio użyć w kroku RK4)."""
    u, x, y, _ln_H = state.as_tuple()
    lam = params.lam
    xi = params.xi

    S = S_expr(u, x, y, params)

    du = x
    dx = -3.0 * x - (lam * y ** 2) / SQRT6 - 12.0 * xi * u - S * (x + 6.0 * xi * u)
    dy = -lam * x * y - S * y
    dlnH = S / SQRT6

    return (du, dx, dy, dlnH)


# ------------------------------------------------------------
# 5. Całkowanie: krok RK4 + pętla po N
# ------------------------------------------------------------

class SingularTrajectoryError(Exception):
    """Trajektoria natrafiła na D<=0 (osobliwość) albo Ωm<=0 podczas
    całkowania — patrz PhysicalityCheck w atrybucie .check i wartość N
    w atrybucie .N."""

    def __init__(self, message: str, check: PhysicalityCheck, N: float):
        super().__init__(message)
        self.check = check
        self.N = N


def _rk4_step(state: SGState, params: SGParams, dN: float) -> SGState:
    """Jeden krok RK4 dla układu background_derivatives — biblioteka
    standardowa (brak scipy w tym repo), stała długość kroku."""

    def deriv(s: SGState) -> tuple:
        return background_derivatives(s, params)

    def add(s: SGState, k: tuple, scale: float) -> SGState:
        return SGState(
            u=s.u + scale * k[0],
            x=s.x + scale * k[1],
            y=s.y + scale * k[2],
            ln_H=s.ln_H + scale * k[3],
        )

    k1 = deriv(state)
    k2 = deriv(add(state, k1, dN / 2.0))
    k3 = deriv(add(state, k2, dN / 2.0))
    k4 = deriv(add(state, k3, dN))

    return SGState(
        u=state.u + (dN / 6.0) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
        x=state.x + (dN / 6.0) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]),
        y=state.y + (dN / 6.0) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]),
        ln_H=state.ln_H + (dN / 6.0) * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]),
    )


def integrate_background(
    u_ini: float,
    y_ini: float,
    params: SGParams,
    N_i: float,
    N_f: float = 0.0,
    n_steps: int = 2000,
    check_physicality: bool = True,
) -> list:
    """Całkuje układ tła od N_i do N_f (domyślnie N_f=0, tj. "dziś"),
    zaczynając od:

        x(N_i) = 0, u(N_i) = u_ini, y(N_i) = y_ini, ln H(N_i) = 0

    (dokładnie warunki początkowe z PDF, sekcja "Double shooting").
    Zwraca listę SGState (jeden na krok, włącznie z punktem startowym
    i końcowym) — wywołujący (np. shooting) bierze zwykle tylko
    ostatni element.

    Jeśli check_physicality=True (domyślnie), przerywa całkowanie i
    rzuca SingularTrajectoryError w momencie, gdy D<=0 lub Ωm<=0 — to
    jest dokładnie flaga "unphysical/singular trajectory" z PDF."""
    if n_steps < 1:
        raise ValueError("n_steps musi być >= 1")

    state = SGState(u=u_ini, x=0.0, y=y_ini, ln_H=0.0)
    dN = (N_f - N_i) / n_steps
    trajectory = [state]

    if check_physicality:
        check = is_physical(state, params)
        if not check.physical:
            raise SingularTrajectoryError(
                f"Warunek początkowy jest już unphysical: {check.reasons}",
                check=check, N=N_i,
            )

    N = N_i
    for _ in range(n_steps):
        state = _rk4_step(state, params, dN)
        N += dN
        trajectory.append(state)
        if check_physicality:
            check = is_physical(state, params)
            if not check.physical:
                raise SingularTrajectoryError(
                    f"Trajektoria unphysical/singular przy N={N!r}: {check.reasons}",
                    check=check, N=N,
                )

    return trajectory
