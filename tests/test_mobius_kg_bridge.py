# tests/test_mobius_kg_bridge.py
"""
Testy syntetyczne dla core/mobius_kg_bridge.py -- "czy operator robi to,
co mowi" (punkt 2 planu uzytkownika, 2026-09-17). Zero realnych danych,
zero progow do pre-rejestracji -- to sa czyste testy zgodnosci z
DEFINICJA (T(k,n), lambda_{k,n}, MC_K_G), analogicznie do 4 testow
stabilnosci weingarten.py czy 65 testow envelope.py w tym ekosystemie.
"""
import math
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.mobius_kg_bridge import (
    is_allowed,
    lambda_kn,
    omega_kn,
    mc_k_g,
    allowed_pairs,
    forbidden_pairs,
    nearest_lattice_point,
)

K_RANGE = range(-6, 7)
N_RANGE = range(1, 8)


def test_allowed_pairs_nonempty_and_forbidden_pairs_nonempty():
    allowed = allowed_pairs(K_RANGE, N_RANGE)
    forbidden = forbidden_pairs(K_RANGE, N_RANGE)
    assert len(allowed) > 0
    assert len(forbidden) > 0
    # kazda para jest albo dopuszczalna, albo zabroniona -- rozlaczne pokrycie
    assert set(allowed).isdisjoint(set(forbidden))
    assert len(allowed) + len(forbidden) == len(list(K_RANGE)) * len(list(N_RANGE))


def test_known_allowed_pairs():
    # (k parzyste, n nieparzyste)
    for (k, n) in [(0, 1), (2, 1), (0, 3), (-2, 1), (4, 3)]:
        assert is_allowed(k, n), f"({k},{n}) powinno byc dopuszczalne"
    # (k nieparzyste, n parzyste)
    for (k, n) in [(1, 2), (-1, 2), (3, 2), (1, 4), (-3, 4)]:
        assert is_allowed(k, n), f"({k},{n}) powinno byc dopuszczalne"


def test_known_forbidden_pairs():
    # kontrolny przyklad z docs/geometry/TIMDR_Mobius_Laplacian_Spectrum.md sekcja 2
    assert not is_allowed(0, 2)
    for (k, n) in [(0, 2), (2, 2), (1, 1), (-1, 1), (0, 4), (3, 3)]:
        assert not is_allowed(k, n), f"({k},{n}) powinno byc zabronione"


def test_n_zero_or_negative_always_forbidden():
    for k in range(-5, 6):
        for n in (0, -1, -2):
            assert not is_allowed(k, n)


def test_mc_k_g_is_one_for_allowed_at_own_reference():
    # MC(k,n) przy omega_ref = omega_kn(k,n) samego siebie musi dawac dokladnie 1.0
    for (k, n) in allowed_pairs(K_RANGE, N_RANGE)[:20]:
        ref = omega_kn(k, n)
        assert mc_k_g(k, n, ref) == pytest.approx(1.0)


def test_mc_k_g_is_zero_for_forbidden_regardless_of_reference():
    for (k, n) in forbidden_pairs(K_RANGE, N_RANGE)[:20]:
        for ref in (0.5, 1.0, 3.7, 100.0):
            assert mc_k_g(k, n, ref) == 0.0


def test_mc_k_g_rejects_nonpositive_reference():
    with pytest.raises(ValueError):
        mc_k_g(0, 1, 0.0)
    with pytest.raises(ValueError):
        mc_k_g(0, 1, -1.0)


def test_ground_state_matches_pdf_pi_squared_over_4():
    # lambda_1 = pi^2/4, (k,n)=(0,1) -- wartosc z docs/geometry/TIMDR_Mobius_Laplacian_Spectrum.md
    assert is_allowed(0, 1)
    assert lambda_kn(0, 1) == pytest.approx(math.pi ** 2 / 4, rel=1e-9)


def test_forbidden_pair_0_2_matches_pdf_example():
    # explicit kontrprzyklad z dokumentu: (k=0,n=2) obecne w widmie
    # cylindra (lambda=pi^2), nieobecne w widmie Mobiusa
    assert lambda_kn(0, 2) == pytest.approx(math.pi ** 2, rel=1e-9)
    assert not is_allowed(0, 2)


def test_omega_kn_stability_across_repeated_calls():
    # deterministycznosc -- ta sama para (k,n) zawsze daje ten sam omega
    for (k, n) in allowed_pairs(K_RANGE, N_RANGE)[:10]:
        vals = [omega_kn(k, n) for _ in range(5)]
        assert len(set(vals)) == 1


def test_mc_k_g_scales_linearly_with_inverse_reference():
    k, n = 0, 1
    base_ref = omega_kn(k, n)
    mc_at_2x_ref = mc_k_g(k, n, 2 * base_ref)
    assert mc_at_2x_ref == pytest.approx(0.5)


def test_nearest_lattice_point_finds_exact_match_for_allowed_omega():
    # omega_{k,n} zalezy od k^2, wiec (k,n) i (-k,n) daja identyczna
    # wartosc -- funkcja moze zwrocic dowolna z tej pary przy remisie;
    # sprawdzamy zgodnosc WARTOSCI omega, nie znaku k.
    k, n = 2, 3
    x = omega_kn(k, n)
    found_k, found_n = nearest_lattice_point(x, range(-6, 7), range(1, 8))
    assert omega_kn(found_k, found_n) == pytest.approx(x)
    assert abs(found_k) == abs(k)
    assert found_n == n


def test_nearest_lattice_point_prefers_closest_not_first():
    # x tuz obok omega(0,1)=pi/2~1.5708, a nie np. duzo dalej polozonego (2,1)
    x = math.pi / 2 + 0.01
    found = nearest_lattice_point(x, range(-6, 7), range(1, 8))
    assert found == (0, 1)
