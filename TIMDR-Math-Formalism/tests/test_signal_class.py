"""
tests/test_signal_class.py

Testy dla timdr_formalism/signal_class.py - implementacji oficjalnej
definicji klas sygnalu I/II/III (patrz naglowek tego modulu dla pelnego
uzasadnienia trzech decyzji: margines ostrzegawczy w beta, pominiecie
det(K), i rozwiazanie niespojnosci Q-vs-Q_crit/S_up% jako niezaleznych
bramek na rzecz jednego dyskryminatora - beta).
"""
import numpy as np

from timdr_formalism.signal_class import (
    classify_by_beta,
    classify_signal_point,
    classify_signal_trace,
    BETA_CLASS_III_THRESHOLD,
)
from test_sg_coupling_full_operator import run_sg_coupling_simulation_v2
from test_sg_coupling import calibrate_q_crit


# ---------------------------------------------------------------------
# classify_by_beta - granice
# ---------------------------------------------------------------------

def test_beta_exactly_one_is_class_I():
    assert classify_by_beta(1.0) == "I"


def test_beta_just_below_one_is_class_II():
    assert classify_by_beta(0.99) == "II"


def test_beta_at_threshold_boundary_is_class_II():
    """beta==0.5 DOKLADNIE nalezy do Klasy II (granica >=0.5), nie III -
    konwencja domkniecia przedzialu, spojna z tests/test_sg_coupling_phase_diagram.py
    (tam tez uzyto <0.5 dla "hard", nie <=0.5)."""
    assert classify_by_beta(BETA_CLASS_III_THRESHOLD) == "II"


def test_beta_just_below_threshold_is_class_III():
    assert classify_by_beta(0.499) == "III"


def test_beta_zero_is_class_III():
    assert classify_by_beta(0.0) == "III"


# ---------------------------------------------------------------------
# classify_signal_point - punkty referencyjne
# ---------------------------------------------------------------------

def test_deep_background_point_is_class_I():
    """Q wyraznie ponizej Q_crit (poza marginesem ostrzegawczym) ->
    beta dokladnie 1.0 -> Klasa I."""
    Q_crit = calibrate_q_crit(margin=1.3, alpha=0.1)
    result = classify_signal_point(Q=0.1, Q_crit=Q_crit)
    assert result.signal_class == "I"
    assert result.beta == 1.0
    assert result.S_up_pct == 0.0
    assert result.N == 0.0


def test_point_exactly_at_threshold_is_class_II_with_correct_S_up_pct():
    """Na samym progu Q=Q_crit: Klasa II, i S_up% MUSI byc < 5%
    (wymog oficjalnej definicji) - sprawdzone WPROST, nie tylko przez
    konstrukcje anticipation_fraction=0.05."""
    result = classify_signal_point(Q=0.35, Q_crit=0.35)
    assert result.signal_class == "II"
    assert 0.8 < result.beta < 1.0
    assert result.S_up_pct < 5.0


def test_deep_exceedance_point_is_class_III_with_large_S_up_pct():
    result = classify_signal_point(Q=0.95, Q_crit=0.35)
    assert result.signal_class == "III"
    assert result.S_up_pct >= 20.0


def test_mild_exceedance_above_threshold_is_still_class_II():
    """ZNALEZIONA NIESPOJNOSC (patrz naglowek signal_class.py, punkt a):
    Q>Q_crit NIE gwarantuje Klasy III - punkt tuz NAD progiem ma wciaz
    beta>=0.5 (kanal tlumiacy dominuje), wiec MUSI byc Klasa II mimo
    Q>Q_crit, zgodnie z decyzja 'beta jest jedynym dyskryminatorem'."""
    result = classify_signal_point(Q=0.36, Q_crit=0.35)
    assert result.is_past_hard_threshold is True
    assert result.signal_class == "II", (
        "Q>Q_crit nie powinno automatycznie dawac Klasy III, jesli beta wciaz >=0.5"
    )


# ---------------------------------------------------------------------
# classify_signal_trace - integracja z pelna symulacja
# ---------------------------------------------------------------------

def test_trace_is_class_I_before_anomaly_window():
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2()
    Q_crit = calibrate_q_crit(margin=1.3)
    results = classify_signal_trace(t, Q, Q_crit, cutoff, S_down, S_up)
    before_mask = t < 4.5
    classes_before = [r.signal_class for i, r in enumerate(results) if before_mask[i]]
    assert all(c == "I" for c in classes_before), (
        f"oczekiwano samej Klasy I przed oknem anomalii, dostano {set(classes_before)}"
    )


def test_trace_reaches_class_II_or_III_during_anomaly_soft_mode():
    """Tryb miekki (domyslne parametry) - z test_v2_beta_is_responsive_but_stays_high...
    juz wiadomo, ze beta_min~0.98 w oknie anomalii, wiec oczekujemy
    Klasy II (nie III) podczas anomalii w tym konkretnym, miekkim
    przykladzie."""
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2()
    Q_crit = calibrate_q_crit(margin=1.3)
    results = classify_signal_trace(t, Q, Q_crit, cutoff, S_down, S_up)
    anomaly_mask = (t >= 4.8) & (t <= 5.2) & cutoff
    classes_during = [r.signal_class for i, r in enumerate(results) if anomaly_mask[i]]
    assert len(classes_during) > 0
    assert set(classes_during) <= {"II", "III"}
    assert "III" not in classes_during, "tryb miekki nie powinien osiagac Klasy III"


def test_trace_reaches_class_III_during_anomaly_hard_mode():
    """Tryb twardy (alpha=10, anomaly_bump=100, juz ustalone w
    test_sg_coupling_full_operator_hard_mode.py: beta_min~0.29<0.5) -
    MUSI dac Klase III podczas anomalii."""
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=10.0, anomaly_bump=100.0
    )
    Q_crit = calibrate_q_crit(margin=1.3, alpha=10.0)
    results = classify_signal_trace(t, Q, Q_crit, cutoff, S_down, S_up)
    anomaly_mask = (t >= 4.8) & (t <= 5.2) & cutoff
    classes_during = [r.signal_class for i, r in enumerate(results) if anomaly_mask[i]]
    assert "III" in classes_during, "tryb twardy powinien osiagnac Klase III"


def test_N_is_zero_whenever_cutoff_not_triggered():
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=10.0, anomaly_bump=100.0
    )
    Q_crit = calibrate_q_crit(margin=1.3, alpha=10.0)
    results = classify_signal_trace(t, Q, Q_crit, cutoff, S_down, S_up)
    for i, r in enumerate(results):
        if not cutoff[i]:
            assert r.N == 0.0


def test_quiet_zone_can_dip_into_class_II_without_ever_triggering_cutoff():
    """Dokumentowane w docs/theory/Signal_Classes.md ('Polaczenie z mapa
    faz'): strefa 'cicha' phase diagram (cutoff nigdy sie nie wyzwala)
    NIE znaczy 'zawsze Klasa I' - Q moze wejsc w margines ostrzegawczy
    [Q_eff_crit, Q_crit] bez przekroczenia Q_crit, dajac chwilowo Klase
    II. Zweryfikowany przyklad: alpha=0.1, anomaly_bump=1.5."""
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=0.1, anomaly_bump=1.5
    )
    Q_crit = calibrate_q_crit(margin=1.3, alpha=0.1)
    assert not cutoff.any(), "ten przyklad ma byc 'cicha' strefa - cutoff nie powinien sie wyzwolic"
    results = classify_signal_trace(t, Q, Q_crit, cutoff, S_down, S_up)
    classes = [r.signal_class for r in results]
    assert "II" in classes, "oczekiwano co najmniej jednego kroku w Klasie II mimo braku cutoff"
    assert "III" not in classes


def test_N_is_finite_and_defined_whenever_cutoff_triggered():
    """N=S_down*S_up - z ustalonych wczesniej znakow kanalow (S_down i
    S_up zwykle przeciwne znaki, patrz theta_bifurcation.py), N jest
    zwykle <=0, ale co najwazniejsze: zawsze SKONCZONE (nie NaN/inf)."""
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=10.0, anomaly_bump=100.0
    )
    Q_crit = calibrate_q_crit(margin=1.3, alpha=10.0)
    results = classify_signal_trace(t, Q, Q_crit, cutoff, S_down, S_up)
    for i, r in enumerate(results):
        if cutoff[i]:
            assert np.isfinite(r.N)
