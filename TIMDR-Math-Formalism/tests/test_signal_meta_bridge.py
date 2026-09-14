"""tests/test_signal_meta_bridge.py

Testy dla timdr_formalism/signal_meta_bridge.py - integracji klas
sygnalu I/II/III z MetaState(Λ,τ,ρ,J). Patrz naglowek modulu testowanego
dla pelnej pre-rejestracji (wzory, uzasadnienie, oczekiwania PRZED
uruchomieniem). Realne liczby ponizej (mean rho/J, rozklad faz) zostaly
najpierw policzone bezposrednio w interpreterze (nie zgadniete), dopiero
potem wpisane jako asercje - zgodnie z dyscyplina anty-numerologiczna
tego repo.
"""
import numpy as np
from collections import Counter

from timdr_formalism.signal_meta_bridge import (
    aggregate_window_to_meta_state,
    signal_trace_to_meta_states,
    meta_states_to_phases,
)
from timdr_formalism.signal_class import classify_signal_trace
from timdr_formalism._vendor_meta_state import MetaState, MetaOperatorM

from test_sg_coupling_full_operator import run_sg_coupling_simulation_v2
from test_sg_coupling_full_operator_hard_mode import HARD_ALPHA, HARD_ANOMALY_BUMP
from test_sg_coupling import calibrate_q_crit


# ---------------------------------------------------------------------
# aggregate_window_to_meta_state - wzory jednostkowe, recznie policzone
# ---------------------------------------------------------------------

def test_lambda_zero_when_Q_constant_in_window():
    """Q stale w oknie -> std=0 -> Lambda dokladnie 0.0 (patrz wzor w
    naglowku modulu)."""
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.3, 0.3, 0.3, 0.3]),
        beta_window=np.array([1.0, 1.0, 1.0, 1.0]),
        classes_window=["I", "I", "I", "I"],
        N_window=np.array([0.0, 0.0, 0.0, 0.0]),
        dt_step=0.01,
    )
    assert ms.Lambda == 0.0


def test_lambda_bounded_in_zero_one_when_Q_varies():
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.1, 0.5, 0.2, 0.6, 0.15]),
        beta_window=np.array([1.0, 1.0, 1.0, 1.0, 1.0]),
        classes_window=["I"] * 5,
        N_window=np.zeros(5),
        dt_step=0.01,
    )
    assert 0.0 < ms.Lambda < 1.0


def test_tau_zero_when_beta_constant():
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.2, 0.2, 0.2]),
        beta_window=np.array([0.7, 0.7, 0.7]),
        classes_window=["II", "II", "II"],
        N_window=np.zeros(3),
        dt_step=0.01,
    )
    assert ms.tau == 0.0


def test_tau_matches_hand_computed_value():
    """beta = [1.0, 0.8, 1.0] -> |Δbeta| = [0.2, 0.2] -> mean=0.2,
    dt_step=0.1 -> tau = 0.2/0.1 = 2.0 dokladnie."""
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.3, 0.4, 0.3]),
        beta_window=np.array([1.0, 0.8, 1.0]),
        classes_window=["I", "II", "I"],
        N_window=np.zeros(3),
        dt_step=0.1,
    )
    assert abs(ms.tau - 2.0) < 1e-9


def test_rho_zero_when_no_class_iii_in_window():
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.3, 0.4]),
        beta_window=np.array([1.0, 0.9]),
        classes_window=["I", "II"],
        N_window=np.zeros(2),
        dt_step=0.01,
    )
    assert ms.rho == 0.0


def test_rho_one_when_all_class_iii_in_window():
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.9, 0.95]),
        beta_window=np.array([0.1, 0.05]),
        classes_window=["III", "III"],
        N_window=np.array([-1.0, -2.0]),
        dt_step=0.01,
    )
    assert ms.rho == 1.0


def test_rho_matches_manual_fraction():
    """2 z 5 krokow to Klasa III -> rho = 0.4 dokladnie."""
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.3, 0.9, 0.4, 0.95, 0.3]),
        beta_window=np.array([1.0, 0.2, 0.9, 0.1, 1.0]),
        classes_window=["I", "III", "II", "III", "I"],
        N_window=np.array([0.0, -1.0, 0.0, -2.0, 0.0]),
        dt_step=0.01,
    )
    assert abs(ms.rho - 0.4) < 1e-9


def test_J_zero_when_N_all_zero():
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.1, 0.2]),
        beta_window=np.array([1.0, 1.0]),
        classes_window=["I", "I"],
        N_window=np.array([0.0, 0.0]),
        dt_step=0.01,
    )
    assert ms.J == 0.0


def test_J_one_when_N_constant_nonzero():
    """N stale i niezerowe w oknie -> |N|/max(|N|) = 1.0 dla kazdego
    kroku -> J dokladnie 1.0 (z dokladnoscia do EPS)."""
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.9, 0.9, 0.9]),
        beta_window=np.array([0.1, 0.1, 0.1]),
        classes_window=["III", "III", "III"],
        N_window=np.array([-5.0, -5.0, -5.0]),
        dt_step=0.01,
    )
    assert abs(ms.J - 1.0) < 1e-6


def test_J_bounded_in_zero_one_when_N_varies():
    ms = aggregate_window_to_meta_state(
        Q_window=np.array([0.9, 0.95, 0.85]),
        beta_window=np.array([0.2, 0.1, 0.3]),
        classes_window=["III", "III", "II"],
        N_window=np.array([-1.0, -5.0, -0.2]),
        dt_step=0.01,
    )
    assert 0.0 <= ms.J <= 1.0


# ---------------------------------------------------------------------
# signal_trace_to_meta_states / meta_states_to_phases - mechanika
# ---------------------------------------------------------------------

def test_window_count_matches_partition_with_remainder():
    """20 krokow, window_size=6 -> bloki [0:6),[6:12),[12:18),[18:20) = 4 okna
    (ostatni krotszy, nie pomijany)."""
    t = np.arange(0, 0.2, 0.01)  # 20 probek
    Q = np.linspace(0.1, 0.5, len(t))
    beta = np.ones(len(t))
    classes = ["I"] * len(t)
    N = np.zeros(len(t))
    meta_states, window_starts = signal_trace_to_meta_states(t, Q, beta, classes, N, window_size=6)
    assert len(meta_states) == 4
    assert len(window_starts) == 4


def test_meta_states_to_phases_first_entry_is_none():
    op_states = [MetaState(0.1, 0.1, 0.1, 0.1), MetaState(0.2, 0.2, 0.2, 0.2)]
    window_starts = [0.0, 1.0]
    results = meta_states_to_phases(op_states, window_starts)
    assert results[0] == (None, None)
    assert len(results) == 2


def test_meta_states_to_phases_finite_magnitude_synthetic():
    op_states = [MetaState(0.1, 0.1, 0.1, 0.1), MetaState(0.5, 0.05, 0.9, 0.2)]
    window_starts = [0.0, 0.5]
    results = meta_states_to_phases(op_states, window_starts)
    magnitude, phase = results[1]
    assert np.isfinite(magnitude)
    assert phase in {"stabilna", "przejsciowa", "krytyczna"}


# ---------------------------------------------------------------------
# Integracja pelna: tryb miekki vs twardy (realne trajektorie SG-Coupling)
# ---------------------------------------------------------------------

def _run_full_pipeline(alpha, anomaly_bump, window_size=50):
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=alpha, anomaly_bump=anomaly_bump
    )
    Q_crit = calibrate_q_crit(margin=1.3, alpha=alpha)
    class_results = classify_signal_trace(t, Q, Q_crit, cutoff, S_down, S_up)
    classes = [r.signal_class for r in class_results]
    N_trace = np.array([r.N for r in class_results])
    meta_states, window_starts = signal_trace_to_meta_states(
        t, Q, beta, classes, N_trace, window_size=window_size
    )
    phases = meta_states_to_phases(meta_states, window_starts)
    return meta_states, phases


def test_soft_mode_never_reaches_class_iii_so_mean_rho_is_exactly_zero():
    """Ustalone juz wczesniej (test_sg_coupling_phase_diagram.py,
    test_signal_class.py): domyslny tryb miekki (alpha=0.1, bump=3.0)
    nigdy nie osiaga Klasy III. Zweryfikowane bezposrednio przed
    napisaniem tej asercji: mean(rho)=0.0 dokladnie (0/20 okien)."""
    meta_states, _ = _run_full_pipeline(alpha=0.1, anomaly_bump=3.0)
    mean_rho = np.mean([ms.rho for ms in meta_states])
    assert mean_rho == 0.0


def test_hard_mode_mean_rho_is_positive_and_higher_than_soft_mode():
    """Sprawdzone bezposrednio: tryb twardy (HARD_ALPHA/HARD_ANOMALY_BUMP)
    daje mean(rho)~0.013 (nieco ponad 1 z 20 okien ma cala frakcje w
    Klasie III), tryb miekki dokladnie 0.0 - wiec twardy > miekki."""
    meta_states_soft, _ = _run_full_pipeline(alpha=0.1, anomaly_bump=3.0)
    meta_states_hard, _ = _run_full_pipeline(alpha=HARD_ALPHA, anomaly_bump=HARD_ANOMALY_BUMP)
    mean_rho_soft = np.mean([ms.rho for ms in meta_states_soft])
    mean_rho_hard = np.mean([ms.rho for ms in meta_states_hard])
    assert mean_rho_hard > mean_rho_soft
    assert mean_rho_hard > 0.0


def test_hard_mode_mean_J_higher_than_soft_mode():
    """Sprawdzone bezposrednio: mean(J) tryb miekki ~0.001, tryb twardy
    ~0.019 (rzedu 19x wiecej) - J bazuje na N (S_down*S_up), NIE na
    klasie/beta wprost, wiec to NIE jest ta sama tautologia co rho."""
    meta_states_soft, _ = _run_full_pipeline(alpha=0.1, anomaly_bump=3.0)
    meta_states_hard, _ = _run_full_pipeline(alpha=HARD_ALPHA, anomaly_bump=HARD_ANOMALY_BUMP)
    mean_J_soft = np.mean([ms.J for ms in meta_states_soft])
    mean_J_hard = np.mean([ms.J for ms in meta_states_hard])
    assert mean_J_hard > mean_J_soft


def test_all_magnitudes_finite_in_both_regimes():
    for alpha, bump in [(0.1, 3.0), (HARD_ALPHA, HARD_ANOMALY_BUMP)]:
        _, phases = _run_full_pipeline(alpha=alpha, anomaly_bump=bump)
        magnitudes = [m for m, _ in phases if m is not None]
        assert len(magnitudes) > 0
        assert all(np.isfinite(m) for m in magnitudes)


def test_classify_phase_partially_but_not_cleanly_separates_regimes():
    """UCZCIWY WYNIK (sprawdzony bezposrednio PRZED napisaniem tej
    asercji, nie zalozony) - dokladnie ten sam wzorzec "mechanizm
    dziala, progi nieskalibrowane", ktory znaleziono juz w szesciu
    innych domenach META-DYNAMICS (patrz TIMDR_Branch_Specification.md):

    Tryb miekki (20 okien):  stabilna=11, przejsciowa=5,  krytyczna=3
    Tryb twardy (20 okien):  stabilna=2,  przejsciowa=14, krytyczna=3

    Mechanizm CZESCIOWO odzwierciedla roznice rezimow (mniej "stabilna",
    wiecej "przejsciowa" w trybie twardym - kierunek zgodny z
    intuicja). ALE liczba okien "krytyczna" jest IDENTYCZNA (3) w obu
    trybach - progi 0.1/1.0 (odziedziczone bez zmian z oryginalnego
    szkicu META-DYNAMICS, patrz _vendor_meta_state.py) NIE rozdzielaja
    najbardziej ekstremalnej kategorii miedzy rezimami. Nie jest to
    ukrywane ani przerabiane na "dziala lepiej niz jest" - to jest
    dokladnie taki sam, uczciwie zaraportowany czesciowy wynik jak w
    Quantum-Lattice (mechanizm dziala - p=7.3e-136 - ale progi 0.1/1.0
    nigdy sie nie odpalily na tamtej skali danych)."""
    _, phases_soft = _run_full_pipeline(alpha=0.1, anomaly_bump=3.0)
    _, phases_hard = _run_full_pipeline(alpha=HARD_ALPHA, anomaly_bump=HARD_ANOMALY_BUMP)

    labels_soft = [p for _, p in phases_soft if p is not None]
    labels_hard = [p for _, p in phases_hard if p is not None]

    counts_soft = Counter(labels_soft)
    counts_hard = Counter(labels_hard)

    # Kierunek zgodny z intuicja: twardy ma mniej "stabilna", wiecej "przejsciowa".
    assert counts_hard["stabilna"] < counts_soft["stabilna"]
    assert counts_hard["przejsciowa"] > counts_soft["przejsciowa"]

    # Uczciwie odnotowane OGRANICZENIE: "krytyczna" NIE rozdziela rezimow
    # przy tych progach - to jest sprawdzony fakt, nie domysl.
    assert counts_hard["krytyczna"] == counts_soft["krytyczna"] == 3
