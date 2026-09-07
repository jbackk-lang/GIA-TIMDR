# tests/test_trefoil_resonance_model.py
"""
test_trefoil_resonance_model.py -- testy dla core/trefoil_resonance_model.py.

Odpowiadaja na 7-krokowy protokol uzytkownika:
1. Idealny trojwezel jako referencja -> test symetrii bazowej
   (zdegenerowany dublet czestosci wlasnych).
2. Defekt D1(Δr1,Δτ1) na wezle 1 -> test ze macierze poprawnie
   lamia symetrie tylko przy niezerowym defekcie.
3-5. Pobudzenie lokalne + odpowiedz ustalona -> test ze odpowiedz
   bazowa ma dokladnie 2 rozroznialne piki (singlet + dublet).
6. Defekt -> rezonans: test ze Δτ1 rozszczepia dublet (rosnaco z
   defektem), a Δr1 przesuwa GLOWNIE singlet (jakosciowo rozny
   odcisk defektu w widmie).
7. Rezonans jako kryterium rewizji: test ze w przetestowanym zakresie
   defektu uklad pozostaje stabilny -- Q nie eksploduje, stosunki
   amplitud sasiadow do wezla pobudzanego zostaja ograniczone.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pytest

from core.trefoil_resonance_model import (
    build_matrices,
    natural_frequencies,
    steady_state_response,
    find_peaks,
    estimate_Q,
    default_omega_sweep,
)

F_NODE1 = np.array([1.0, 0.0, 0.0], dtype=complex)


def test_krok1_idealny_trojwezel_ma_zdegenerowany_dublet():
    """Bez defektu: symetria 3-krotna pierscienia -> 1 tryb
    niezdegenerowany (singlet) + 1 podwojnie zdegenerowany (dublet)."""
    M, K, _ = build_matrices()
    w_nat = natural_frequencies(M, K)
    assert len(w_nat) == 3
    # dublet: dwie najwyzsze czestosci rowne w granicy precyzji numerycznej
    assert w_nat[2] == pytest.approx(w_nat[1], rel=1e-9)
    # singlet wyraznie rozny od dubletu
    assert abs(w_nat[0] - w_nat[1]) > 0.5


def test_krok2_defekt_lamie_symetrie_macierzy():
    M0, K0, _ = build_matrices()
    M1, K1, _ = build_matrices(defect_tau1=0.3)
    M2, K2, _ = build_matrices(defect_r1=0.3)
    assert not np.allclose(K0, K1)
    assert not np.allclose(K0, K2)
    # bez defektu macierze identyczne przy powtornym wywolaniu (determinizm)
    M0b, K0b, _ = build_matrices()
    assert np.allclose(K0, K0b) and np.allclose(M0, M0b)


def test_krok3to5_odpowiedz_bazowa_ma_dwa_piki():
    M, K, Gamma = build_matrices()
    omegas = default_omega_sweep(M, K)
    X = steady_state_response(M, K, Gamma, F_NODE1, omegas)
    amp1 = np.abs(X[:, 0])
    peaks = find_peaks(amp1, omegas)
    assert len(peaks) == 2, f"oczekiwano 2 pikow (singlet+dublet), znaleziono {len(peaks)}"
    w_nat = natural_frequencies(M, K)
    # piki powinny pokrywac sie w przyblizeniu z czestosciami wlasnymi
    assert omegas[peaks[0]] == pytest.approx(w_nat[0], abs=0.05)
    assert omegas[peaks[1]] == pytest.approx(w_nat[1], abs=0.05)


def test_krok6_defekt_tau_rozszczepia_dublet_rosnaco():
    M0, K0, _ = build_matrices()
    w0 = natural_frequencies(M0, K0)
    splits = []
    for dtau1 in (0.10, 0.30, 0.60, 1.20):
        M, K, _ = build_matrices(defect_tau1=dtau1)
        w = natural_frequencies(M, K)
        split = w[2] - w[1]
        splits.append(split)
        # singlet (w[0]) prawie nietkniety przez defekt sprzezenia
        assert abs(w[0] - w0[0]) < 0.01

    assert splits[0] > 1e-6, "brak rozszczepienia dubletu przy niezerowym Δτ1"
    # rozszczepienie rosnie monotonicznie z sila defektu
    assert all(splits[i] < splits[i + 1] for i in range(len(splits) - 1))


def test_krok6_defekt_r1_przesuwa_glownie_singlet():
    M0, K0, _ = build_matrices()
    w0 = natural_frequencies(M0, K0)

    M, K, _ = build_matrices(defect_r1=0.60)
    w = natural_frequencies(M, K)

    shift_singlet = abs(w[0] - w0[0])
    split_doublet = w[2] - w[1]

    assert shift_singlet > 0.05, "Δr1 powinien wyraznie przesunac singlet"
    # jakosciowy odcisk: przesuniecie singletu wieksze niz rozszczepienie dubletu
    # dla tej samej (wzglednej) sily defektu -- rozny "podpis" Δr1 vs Δτ1
    assert shift_singlet > split_doublet


def test_krok7_stabilnosc_w_przetestowanym_zakresie_defektu():
    """Rezonans jako kryterium rewizji: sprawdz, ze defekt (do +120%
    Δτ1 / +60% Δr1) NIE powoduje niekontrolowanego wzrostu ostrosci
    piku (Q) ani nieproporcjonalnego 'przecieku' energii do sasiadow
    -- w tym zakresie uklad jest stabilny (rezonans zmienia KSZTALT
    widma, nie eskaluje destrukcyjnie)."""
    M0, K0, Gamma0 = build_matrices()
    omegas = default_omega_sweep(M0, K0)
    X0 = steady_state_response(M0, K0, Gamma0, F_NODE1, omegas)
    amp0 = np.abs(X0)
    peaks0 = find_peaks(amp0[:, 0], omegas)
    Q0 = [estimate_Q(amp0[:, 0], omegas, i) for i in peaks0]

    for dtau1, dr1 in [(0.30, 0.0), (0.60, 0.0), (1.20, 0.0), (0.0, 0.30), (0.0, 0.60)]:
        M, K, Gamma = build_matrices(defect_tau1=dtau1, defect_r1=dr1)
        X = steady_state_response(M, K, Gamma, F_NODE1, omegas)
        amp = np.abs(X)
        peaks = find_peaks(amp[:, 0], omegas)
        assert len(peaks) >= 1
        Q = [estimate_Q(amp[:, 0], omegas, i) for i in peaks]
        # Q nie eksploduje: pozostaje w rozsadnej wielokrotnosci Q bazowego
        assert max(Q) < 3 * max(Q0), (
            f"Q wzroslo ponad 3x bazy przy defekcie tau={dtau1}, r={dr1}: {Q} vs baza {Q0}"
        )
        # stosunek amplitudy sasiada do wezla pobudzanego pozostaje ograniczony (<=1.5x bazy)
        for i in peaks:
            ratio2 = amp[i, 1] / amp[i, 0] if amp[i, 0] > 1e-9 else 0.0
            assert ratio2 < 1.5, f"nieproporcjonalny przeciek energii do sasiada przy defekcie tau={dtau1}, r={dr1}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
