# core/mobius_kg_bridge.py
"""
mobius_kg_bridge.py -- implementacja kandydujacego (NIE ustalonego)
mostu G<->K opisanego w Axioms_K_TIMDR.md / Axioms_G_TIMDR_Geometry.md
("widmo Laplasjanu Mobiusa jako regula selekcji czestotliwosci
modalnych"), doprecyzowanego 2026-09-17 jawnym operatorem:

    T(k,n)   = 1 jesli (k,n) dopuszczalne na Mobiusie, 0 w przeciwnym razie
    lambda_{k,n} = k^2 + (n*pi/2)^2
    omega_{k,n}  = sqrt(lambda_{k,n})
    MC_{K<->G}(k,n) = T(k,n) * (omega_{k,n} / omega_ref)

Regula doboru (dowiedziona w docs/geometry/TIMDR_Mobius_Laplacian_Spectrum.md,
zweryfikowana numerycznie dwiema niezaleznymi metodami): (k,n) dopuszczalne
<=> (k parzyste I n nieparzyste) LUB (k nieparzyste I n parzyste), k w Z,
n >= 1.

Status: kandydat, NIE ustalony most. Ten plik dostarcza TYLKO warstwe
operatorowa (T, lambda, omega, MC) + syntetyczna kontrole poprawnosci
("czy operator robi to co mowi" -- pary dopuszczalne/zabronione,
stabilnosc omega/omega_ref). Test na realnych danych (czy realne
czestotliwosci modalne "trafiaja" czesciej w dopuszczalne punkty
kratownicy niz przypadek) jest OSOBNYM plikiem
(core/real_mobius_kg_bridge.py), zgodnie z dyscyplina pre-rejestracji
(patrz docs/geometry/PREREG_MOBIUS_COHERENCE_BRIDGES.md).
"""
from __future__ import annotations

import math
from typing import Iterable, Tuple


def is_allowed(k: int, n: int) -> bool:
    """T(k,n) jako bool. Regula: (k parzyste, n nieparzyste) LUB
    (k nieparzyste, n parzyste). n musi byc >= 1 (definicja widma --
    n=0 nie wystepuje, transwersalny warunek Dirichleta zaczyna sie od
    n=1)."""
    if n < 1:
        return False
    k_even = (k % 2 == 0)
    n_even = (n % 2 == 0)
    return (k_even and not n_even) or ((not k_even) and n_even)


def lambda_kn(k: int, n: int) -> float:
    """lambda_{k,n} = k^2 + (n*pi/2)^2 -- WZOR OGOLNY, zdefiniowany dla
    KAZDEGO (k,n), niezaleznie od tego czy para jest dopuszczalna.
    Dopuszczalnosc jest osobnym predykatem (is_allowed), nie wplywa na
    sam wzor -- widmo Mobiusa to PODZBIOR {lambda_{k,n} : is_allowed(k,n)},
    nie inny wzor."""
    return float(k) ** 2 + (float(n) * math.pi / 2.0) ** 2


def omega_kn(k: int, n: int) -> float:
    """omega_{k,n} = sqrt(lambda_{k,n}) -- czestotliwosc wlasna w
    standardowej interpretacji rownania falowego (patrz Axioms_K_TIMDR.md,
    dopisek "most G<->K")."""
    return math.sqrt(lambda_kn(k, n))


def mc_k_g(k: int, n: int, omega_ref: float) -> float:
    """MC_{K<->G}(k,n) = T(k,n) * (omega_{k,n} / omega_ref).

    Zero dla par zabronionych (niezaleznie od omega_ref), znormalizowana
    czestotliwosc wlasna dla par dopuszczalnych. omega_ref > 0 wymagane
    (kalibrowane w PREREG, nie zgadywane tutaj)."""
    if omega_ref <= 0:
        raise ValueError(f"omega_ref musi byc > 0, dostano {omega_ref}")
    if not is_allowed(k, n):
        return 0.0
    return omega_kn(k, n) / omega_ref


def allowed_pairs(k_range: Iterable[int], n_range: Iterable[int]) -> list:
    return [(k, n) for k in k_range for n in n_range if is_allowed(k, n)]


def forbidden_pairs(k_range: Iterable[int], n_range: Iterable[int]) -> list:
    return [(k, n) for k in k_range for n in n_range if not is_allowed(k, n)]


def nearest_lattice_point(
    x: float, k_range: Iterable[int], n_range: Iterable[int]
) -> Tuple[int, int]:
    """Dla znormalizowanej czestotliwosci x=omega_measured/omega_ref,
    znajdz (k,n) w podanym zakresie minimalizujace |omega_{k,n}/omega_ref
    (przy omega_ref=1, tj. dziala na juz-znormalizowanej wartosci x
    traktowanej jako omega_{k,n}) - x|. Uzywane WYLACZNIE w tescie na
    realnych danych (real_mobius_kg_bridge.py) do mapowania ciaglej,
    zmierzonej czestotliwosci na dyskretna kratownice (k,n). Zwraca
    pierwsza znaleziona parę o minimalnej odleglosci (deterministyczne
    przy ustalonej kolejnosci k_range/n_range)."""
    best = None
    best_dist = float("inf")
    for k in k_range:
        for n in n_range:
            if n < 1:
                continue
            d = abs(omega_kn(k, n) - x)
            if d < best_dist:
                best_dist = d
                best = (k, n)
    if best is None:
        raise ValueError("pusty zakres k_range/n_range")
    return best
