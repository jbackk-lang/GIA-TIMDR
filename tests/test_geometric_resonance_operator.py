# tests/test_geometric_resonance_operator.py
"""
test_geometric_resonance_operator.py -- testy dla
core/geometric_resonance_operator.py, implementacji Aksjomatu G5
(`docs/theory/Axioms_G_TIMDR_Geometry.md`).

Trzy cele tych testow:
1. Regresja: core/trefoil_resonance_model.py (N=3, warstwa kompatybilnosci)
   musi dawac BAJT-W-BAJT identyczny wynik jak przed podniesieniem do
   G5 -- zadna z sesji uzytkownika/testow napisanych dla trojwezla nie
   moze cicho zmienic zachowania.
2. Ogolnosc: implementacja NIE jest ukrytym przypadkiem szczegolnym
   N=3 -- test na N=4,5,6 z domknieta postacia analityczna (macierz
   cyrkulantowa) czestosci wlasnych pierscienia symetrycznego,
   niezalezna od kodu ktory testujemy.
3. Warunek stabilnosci (Aksjomat G5d): `is_stable()` poprawnie
   odroznia uklad stabilny (M,K,Gamma dodatnio okreslone) od
   niestabilnego (brak tlumienia, ujemna sztywnosc).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pytest

from core.geometric_resonance_operator import (
    build_ring_matrices,
    natural_frequencies,
    steady_state_response,
    find_peaks,
    estimate_Q,
    default_omega_sweep,
    is_stable,
)


class TestBackwardCompatibilityZTrojweztem:
    def test_trefoil_build_matrices_matches_general_operator(self):
        """core.trefoil_resonance_model.build_matrices() (N=3, warstwa
        kompatybilnosci) musi dawac DOKLADNIE ten sam wynik, co
        rekonstrukcja rownowazna z build_ring_matrices() -- regresja
        na wypadek, gdyby refaktoryzacja do operatora ogolnego cicho
        zmienila liczby."""
        from core.trefoil_resonance_model import build_matrices, K0, KC0, M0_DEFAULT, GAMMA_DEFAULT

        for defect_r1, defect_tau1 in [(0.0, 0.0), (0.3, 0.0), (0.0, 0.3), (0.6, 1.2)]:
            M_trefoil, K_trefoil, Gamma_trefoil = build_matrices(
                defect_r1=defect_r1, defect_tau1=defect_tau1,
            )
            kappa_arr = [K0 * (1 + defect_r1), K0, K0]
            tau_arr = [KC0 * (1 + defect_tau1), KC0, KC0 * (1 + defect_tau1)]
            M_gen, K_gen, Gamma_gen = build_ring_matrices(
                3, kappa_arr, tau_arr, m=[M0_DEFAULT] * 3, gamma=GAMMA_DEFAULT,
                k_scale=1.0, kc_scale=1.0,
            )
            assert np.array_equal(M_trefoil, M_gen)
            assert np.array_equal(K_trefoil, K_gen)
            assert np.array_equal(Gamma_trefoil, Gamma_gen)

    def test_trefoil_module_reexports_are_the_same_functions(self):
        """core.trefoil_resonance_model powinien re-eksportowac
        DOKLADNIE te same funkcje (nie kopie), zeby nie bylo dwoch
        rownoleglych implementacji do rozjechania sie w przyszlosci."""
        import core.trefoil_resonance_model as trefoil
        import core.geometric_resonance_operator as general

        assert trefoil.natural_frequencies is general.natural_frequencies
        assert trefoil.steady_state_response is general.steady_state_response
        assert trefoil.find_peaks is general.find_peaks
        assert trefoil.estimate_Q is general.estimate_Q
        assert trefoil.default_omega_sweep is general.default_omega_sweep
        assert trefoil.is_stable is general.is_stable


class TestOgolnoscDowolnegoN:
    """Dowod, ze operator NIE jest ukrytym przypadkiem szczegolnym N=3:
    dla pierscienia SYMETRYCZNEGO (kappa, tau jednakowe na wszystkich
    wezlach/segmentach) macierz K jest cyrkulantowa, a jej wartosci
    wlasne maja znana postac analityczna, NIEZALEZNA od kodu
    testowanego tutaj:
        lambda_j = k0 + 2*kc*(1 - cos(2*pi*j/N)),   j=0,...,N-1
    (z M=I, omega_j = sqrt(lambda_j)). Wyprowadzenie: K jest
    cyrkulantem [k0+2kc, -kc, 0,...,0,-kc] -- standardowy wzor na
    widmo macierzy cyrkulantowej."""

    @staticmethod
    def _theoretical_omegas(n, k0, kc):
        j = np.arange(n)
        lam = k0 + 2 * kc * (1 - np.cos(2 * np.pi * j / n))
        return np.sort(np.sqrt(np.clip(lam, 0, None)))

    @pytest.mark.parametrize("n_nodes", [3, 4, 5, 6, 8])
    def test_symmetric_ring_matches_circulant_theory(self, n_nodes):
        k0, kc = 1.7, 0.9
        kappa = [k0] * n_nodes
        tau = [kc] * n_nodes
        M, K, _ = build_ring_matrices(n_nodes, kappa, tau, k_scale=1.0, kc_scale=1.0)
        w_num = natural_frequencies(M, K)
        w_theory = self._theoretical_omegas(n_nodes, k0, kc)
        assert w_num == pytest.approx(w_theory, abs=1e-9)

    def test_n4_ring_has_singlet_doublet_singlet_structure(self):
        """N=4 simetryczny: teoria cyrkulantowa przewiduje 1 singlet
        (j=0, najnizszy), 1 zdegenerowany dublet (j=1,3, srodkowy) i
        1 singlet (j=2, najwyzszy) -- jakosciowo INNA struktura
        degeneracji niz N=3 (tam: 1 singlet + 1 dublet, bez drugiego
        singletu na gorze) -- dowod ze kod poprawnie generalizuje
        wzorzec degeneracji, nie tylko liczby."""
        M, K, _ = build_ring_matrices(4, [1.0] * 4, [0.5] * 4, k_scale=1.0, kc_scale=1.0)
        w = natural_frequencies(M, K)
        assert len(w) == 4
        assert w[1] == pytest.approx(w[2], rel=1e-9), "oczekiwano zdegenerowanego dubletu w srodku widma"
        assert w[0] < w[1] - 1e-6, "dolny singlet powinien byc wyraznie osobno"
        assert w[3] > w[2] + 1e-6, "gorny singlet powinien byc wyraznie osobno"

    def test_asymmetric_defect_on_n5_ring_breaks_symmetry_like_n3(self):
        """Jakosciowa regresja wzorca z N=3 na inne N: defekt na
        JEDNYM wezle pierscienia N=5 powinien zmienic macierz K (zlamac
        symetrie cyrkulantowa) - ten sam typ efektu co defekt na
        trojwezle, teraz sprawdzony na innym N."""
        n = 5
        kappa0 = [1.0] * n
        tau0 = [0.5] * n
        _, K0mat, _ = build_ring_matrices(n, kappa0, tau0, k_scale=1.0, kc_scale=1.0)

        kappa_defekt = list(kappa0)
        kappa_defekt[0] = kappa0[0] * 1.6
        _, K1, _ = build_ring_matrices(n, kappa_defekt, tau0, k_scale=1.0, kc_scale=1.0)
        assert not np.allclose(K0mat, K1)

        w0 = natural_frequencies(*build_ring_matrices(n, kappa0, tau0, k_scale=1.0, kc_scale=1.0)[:2])
        w1 = natural_frequencies(np.eye(n), K1)
        assert not np.allclose(np.sort(w0), np.sort(w1))

    def test_response_and_peaks_work_for_n6(self):
        """Koniec-do-konca na N=6: budowa macierzy -> skan czestosci ->
        odpowiedz ustalona -> wykrywanie pikow -- caly potok dziala dla
        N innego niz 3, nie tylko pojedyncze funkcje w izolacji."""
        n = 6
        M, K, Gamma = build_ring_matrices(n, [1.2] * n, [0.6] * n, gamma=0.05, k_scale=1.0, kc_scale=1.0)
        omegas = default_omega_sweep(M, K)
        F = np.zeros(n, dtype=complex)
        F[0] = 1.0
        X = steady_state_response(M, K, Gamma, F, omegas)
        amp0 = np.abs(X[:, 0])
        peaks = find_peaks(amp0, omegas)
        assert len(peaks) >= 1
        for p in peaks:
            q = estimate_Q(amp0, omegas, p)
            assert q > 0


class TestWalidacjaWejscia:
    def test_n_nodes_below_3_raises(self):
        with pytest.raises(ValueError):
            build_ring_matrices(2, [1.0, 1.0], [0.5, 0.5])
        with pytest.raises(ValueError):
            build_ring_matrices(1, [1.0], [0.5])

    def test_mismatched_kappa_tau_length_raises(self):
        with pytest.raises(ValueError):
            build_ring_matrices(4, [1.0, 1.0, 1.0], [0.5, 0.5, 0.5, 0.5])
        with pytest.raises(ValueError):
            build_ring_matrices(4, [1.0] * 4, [0.5] * 3)

    def test_mismatched_mass_length_raises(self):
        with pytest.raises(ValueError):
            build_ring_matrices(3, [1.0] * 3, [0.5] * 3, m=[1.0, 1.0])


class TestWarunekStabilnosciG5d:
    """Aksjomat G5d: is_stable() jako formalny, sprawdzalny predykat
    (nie tylko nieformalne 'Q nie eksploduje' z testow trojwezla)."""

    def test_baseline_symmetric_ring_is_stable(self):
        M, K, Gamma = build_ring_matrices(5, [1.0] * 5, [0.5] * 5, gamma=0.1, k_scale=1.0, kc_scale=1.0)
        assert is_stable(M, K, Gamma) is True

    def test_zero_damping_is_not_stable(self):
        """Gamma=0 (brak tlumienia na ktoryms wezle) lamie scisla
        dodatnia okreslonosc Gamma - warunek G5d nie jest spelniony
        (uklad moze miec biegun na rzeczywistej osi omega przy
        czestosci wlasnej, tj. prawdziwy nietlumiony rezonans)."""
        M, K, _ = build_ring_matrices(4, [1.0] * 4, [0.5] * 4, k_scale=1.0, kc_scale=1.0)
        Gamma_zero = np.zeros((4, 4))
        assert is_stable(M, K, Gamma_zero) is False

    def test_strongly_negative_node_stiffness_is_not_stable(self):
        """Wystarczajaco ujemna sztywnosc wezla moze zepsuc scisla
        dodatnia okreslonosc K (np. gdyby defekt geometryczny
        odpowiadal 'ujemnej krzywiznie' wiekszej niz sprzezenie moze
        skompensowac) - is_stable() powinien to wykryc, nie zwrocic
        cicho False-negative."""
        M, K, Gamma = build_ring_matrices(3, [1.0] * 3, [0.5] * 3, k_scale=1.0, kc_scale=1.0)
        K_broken = K.copy()
        K_broken[0, 0] = -10.0  # sztywnosc wezla 0 zdominowana ujemnie
        assert is_stable(M, K_broken, Gamma) is False

    def test_is_stable_does_not_raise_on_broken_input(self):
        """is_stable() ma byc diagnostyka - nigdy nie rzuca wyjatku,
        nawet na niepoprawnych (niekwadratowych) macierzach."""
        M = np.eye(3)
        K_bad = np.zeros((3, 2))
        Gamma = np.eye(3)
        assert is_stable(M, K_bad, Gamma) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
