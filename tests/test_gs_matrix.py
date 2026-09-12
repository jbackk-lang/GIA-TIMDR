"""
tests/test_gs_matrix.py

Testy dla poprawionego GS-Matrix (timdr_formalism/gs_matrix.py) - patrz
PRE-REJESTRACJA w naglowku gs_matrix.py dla pelnego uzasadnienia.
Kontrola pozytywna: antysymetryczne K zachowuje norme (obrot).
Kontrola negatywna: symetryczne K NIE zachowuje normy (wzrost/zanik).
"""
import numpy as np
import pytest

from timdr_formalism.gs_matrix import (
    decompose_K,
    is_conservative,
    simulate_linear_system,
)


def test_decompose_recovers_original_matrix():
    K = np.array([[0.3, 1.2], [-0.7, -0.1]])
    d = decompose_K(K)
    assert np.allclose(d.K_anti + d.K_sym, K)


def test_decompose_anti_is_antisymmetric_and_sym_is_symmetric():
    K = np.array([[0.3, 1.2], [-0.7, -0.1]])
    d = decompose_K(K)
    assert np.allclose(d.K_anti.T, -d.K_anti)
    assert np.allclose(d.K_sym.T, d.K_sym)


def test_decompose_rejects_non_square():
    with pytest.raises(ValueError):
        decompose_K(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))


# ---------------------------------------------------------------------
# is_conservative: K^T=-K, NIE K=K dagger (poprawka bledu z propozycji)
# ---------------------------------------------------------------------

def test_is_conservative_true_for_pure_antisymmetric():
    K = np.array([[0.0, 2.0], [-2.0, 0.0]])
    assert is_conservative(K)


def test_is_conservative_false_for_symmetric():
    # symetryczna, NIE antysymetryczna -> nie-zachowawcza, mimo ze
    # "hermitowska" (symetryczna rzeczywista = hermitowska) - to
    # dokladnie przypadek bledu z oryginalnej propozycji.
    K = np.array([[1.0, 2.0], [2.0, 1.0]])
    assert not is_conservative(K)


def test_is_conservative_false_for_mixed():
    K = np.array([[0.5, 1.0], [-1.0, 0.2]])  # ma nietrywialna czesc symetryczna
    assert not is_conservative(K)


# ---------------------------------------------------------------------
# Kontrola POZYTYWNA: antysymetryczne K -> norma V(t) STALA (obrot)
# ---------------------------------------------------------------------

def test_pure_antisymmetric_K_preserves_norm():
    K = np.array([[0.0, 1.5], [-1.5, 0.0]])
    V0 = np.array([1.0, 0.3])
    dt = 0.001
    n_steps = 10_000  # horyzont t=10
    traj = simulate_linear_system(K, V0, dt, n_steps)
    norms = np.linalg.norm(traj, axis=1)
    norm0 = norms[0]
    max_drift = np.max(np.abs(norms - norm0))
    assert max_drift < 1e-3, f"dryf normy {max_drift} przekracza tolerancje RK4"


@pytest.mark.parametrize("a", [0.1, 1.0, 3.0, 7.5])
def test_pure_antisymmetric_K_preserves_norm_various_couplings(a):
    K = np.array([[0.0, a], [-a, 0.0]])
    V0 = np.array([2.0, -1.0])
    traj = simulate_linear_system(K, V0, dt=0.001, n_steps=5000)
    norms = np.linalg.norm(traj, axis=1)
    assert np.max(np.abs(norms - norms[0])) < 1e-3


# ---------------------------------------------------------------------
# Kontrola NEGATYWNA: symetryczne K -> norma V(t) rosnie/zanika
# ---------------------------------------------------------------------

def test_symmetric_K_with_positive_eigenvalue_grows():
    # K = diag(0.5, -0.5): wartosci wlasne +0.5 i -0.5.
    K = np.array([[0.5, 0.0], [0.0, -0.5]])
    V0 = np.array([1.0, 0.0])  # czysto w kierunku dodatniej wartosci wlasnej
    traj = simulate_linear_system(K, V0, dt=0.001, n_steps=2000)  # t=2
    norms = np.linalg.norm(traj, axis=1)
    assert norms[-1] > norms[0] * 2.0, (
        f"oczekiwano wyraznego wzrostu normy, dostano {norms[0]} -> {norms[-1]}"
    )
    # monotonicznie rosnaca (do numerycznego szumu)
    assert np.all(np.diff(norms) >= -1e-9)


def test_symmetric_K_with_negative_eigenvalue_decays():
    K = np.array([[-0.5, 0.0], [0.0, 0.5]])
    V0 = np.array([1.0, 0.0])  # w kierunku UJEMNEJ wartosci wlasnej
    traj = simulate_linear_system(K, V0, dt=0.001, n_steps=2000)
    norms = np.linalg.norm(traj, axis=1)
    assert norms[-1] < norms[0] * 0.5, (
        f"oczekiwano wyraznego zaniku normy, dostano {norms[0]} -> {norms[-1]}"
    )


# ---------------------------------------------------------------------
# Walidacja wejscia symulacji
# ---------------------------------------------------------------------

def test_simulate_rejects_dimension_mismatch():
    with pytest.raises(ValueError):
        simulate_linear_system(np.eye(2), np.array([1.0, 2.0, 3.0]), dt=0.01, n_steps=10)


def test_simulate_rejects_nonpositive_dt():
    with pytest.raises(ValueError):
        simulate_linear_system(np.eye(2), np.array([1.0, 0.0]), dt=0.0, n_steps=10)
