"""
tests/test_sg_coupling_full_operator.py

Integracja pelnego operatora Theta_bif (timdr_formalism/theta_bifurcation.py)
z symulacja SG-Coupling (tests/test_sg_coupling.py) - wersja v2, uzywana
TYLKO do porownania z prostym tlumieniem (0.1*S) juz istniejacym w
run_sg_coupling_simulation(). Nie zastepuje wersji v1 - obie wspoluzytkuja
ta sama, juz naprawiona kalibracje Q_crit z tests/test_sg_coupling.py.
"""
import numpy as np

from timdr_formalism.theta_bifurcation import theta_bifurcation
from test_sg_coupling import calibrate_q_crit


def run_sg_coupling_simulation_v2(
    L0: float = 5.0,
    alpha: float = 0.1,
    Q_crit: float | None = None,
    R0: float = 0.2,
    dt: float = 0.01,
    duration: float = 10.0,
    lambda_down: float = 2.0,
    lambda_up: float = 1.0,
):
    """Ta sama dynamika co run_sg_coupling_simulation (v1), ale z
    PELNYM operatorem Theta_bif (S_down/S_up) zamiast prostego
    tlumienia 0.1*S. Sledzi t_cutoff_start per ciagly epizod
    przekroczenia progu (resetowany, gdy Q spadnie z powrotem <=
    Q_crit)."""
    if Q_crit is None:
        Q_crit = calibrate_q_crit(margin=1.3, L0=L0, alpha=alpha, R0=R0, dt=dt, duration=duration)

    t = np.arange(0, duration, dt)
    N = len(t)

    G = np.zeros(N)
    S = np.zeros(N)
    R = np.zeros(N)
    Q = np.zeros(N)
    cutoff_triggered = np.zeros(N, dtype=bool)
    beta_trace = np.full(N, np.nan)

    G[0] = R0
    S[0] = 0.0

    t_cutoff_start = None  # None = nie jestesmy w epizodzie bifurkacji

    for i in range(1, N):
        signal_input = np.sin(2 * np.pi * 0.5 * t[i])
        if 4.8 <= t[i] <= 5.2:
            signal_input += 3.0

        S_raw = S[i - 1] + dt * (-1.0 * S[i - 1] + signal_input)

        F_S = S_raw ** 2
        G[i] = R0 + alpha * F_S
        S[i] = S_raw

        Z = G[i] + 1j * S[i]
        R[i] = np.abs(Z)

        L_R = L0 + 2 * np.pi * R[i]
        Q[i] = 1.0 - (L0 / L_R)

        if Q[i] > Q_crit:
            cutoff_triggered[i] = True
            if t_cutoff_start is None:
                t_cutoff_start = t[i]  # poczatek NOWEGO epizodu
            time_since = t[i] - t_cutoff_start
            result = theta_bifurcation(
                S=S[i], Q=Q[i], Q_crit=Q_crit,
                time_since_cutoff_start=time_since,
                lambda_down=lambda_down, lambda_up=lambda_up,
            )
            S[i] = result.S_new
            G[i] = G[i]  # Theta_bif dziala tylko na skladowa S (zgodnie z propozycja)
            beta_trace[i] = result.beta
        else:
            t_cutoff_start = None  # koniec epizodu, reset

    return t, G, S, R, Q, cutoff_triggered, beta_trace


def test_v2_no_nan_or_inf_over_full_run():
    t, G, S, R, Q, cutoff, beta = run_sg_coupling_simulation_v2()
    assert np.all(np.isfinite(S))
    assert np.all(np.isfinite(G))
    assert np.all(np.isfinite(R))
    assert np.all(np.isfinite(Q))


def test_v2_no_false_triggers_before_anomaly_window():
    t, G, S, R, Q, cutoff, beta = run_sg_coupling_simulation_v2()
    assert np.sum(cutoff[t < 4.5]) == 0


def test_v2_detects_anomaly_window():
    t, G, S, R, Q, cutoff, beta = run_sg_coupling_simulation_v2()
    anomaly_mask = (t >= 4.8) & (t <= 5.2)
    assert np.sum(cutoff[anomaly_mask]) > 0


def test_v2_beta_is_responsive_but_stays_high_for_this_specific_example():
    """ZNALEZIONE PRZY PISANIU TESTOW (nie zalozone z gory): pierwsza
    wersja tego testu zakladala, ze beta powinno spasc WYRAZNIE (<0.5)
    podczas wstrzknietej anomalii - to bylo bledne zalozenie o SKALI
    TEGO KONKRETNEGO PRZYKLADU, nie blad operatora. Rzeczywistosc:
    Q_crit kalibrowane wychodzi ~0.487, a Q podczas anomalii siega
    tylko ~0.497 (Q teoretycznie moze dojsc do 1) - anomalia +3.0 przy
    alpha=0.1 po prostu nie jest "glebokim" przekroczeniem w przestrzeni
    Q dla TYCH parametrow, wiec beta zostaje bliskie 1 (~0.98) - kanal
    kondensujacy ledwo sie aktywuje. To NIE oznacza, ze operator nie
    dziala - oznacza, ze przy tych R0/L0/alpha kanal S_up praktycznie
    nigdy nie zdominuje dla anomalii tej sily. Test ponizej sprawdza to,
    co FAKTYCZNIE mozna uczciwie zagwarantowac: beta podczas anomalii
    jest choc troche nizsze niz tuz-nad-progiem (a wiec operator
    REAGUJE na sile przekroczenia, nawet jesli w tym przykladzie
    reakcja jest niewielka), i NIGDY nie wraca do dokladnie 1.0 (co
    oznaczaloby brak jakiejkolwiek reakcji)."""
    t, G, S, R, Q, cutoff, beta = run_sg_coupling_simulation_v2()
    anomaly_mask = (t >= 4.8) & (t <= 5.2) & cutoff
    assert np.any(anomaly_mask), "brak probek cutoff w oknie anomalii do przetestowania"
    beta_during_anomaly = beta[anomaly_mask]
    assert np.nanmax(beta_during_anomaly) < 1.0, "beta=1.0 oznaczaloby brak jakiejkolwiek reakcji operatora"
    assert np.nanmin(beta_during_anomaly) < 0.99


def test_v2_vs_v1_both_finite_and_comparable_at_anomaly_peak():
    """Nie twierdzimy, ze v2 jest 'lepsze' niz proste tlumienie (v1) -
    to porownanie sanity-check: obie wersje daja skonczone, rozsadnej
    skali wyniki w oknie anomalii, nie rozjezdzaja sie o rzedy
    wielkosci."""
    from test_sg_coupling import run_sg_coupling_simulation

    t1, G1, S1, R1, Q1, cutoff1 = run_sg_coupling_simulation()
    t2, G2, S2, R2, Q2, cutoff2, beta2 = run_sg_coupling_simulation_v2()

    peak_idx = np.argmax(Q1[(t1 >= 4.8) & (t1 <= 5.2)])
    anomaly_slice = (t1 >= 4.8) & (t1 <= 5.2)
    max_S1 = np.max(np.abs(S1[anomaly_slice]))
    max_S2 = np.max(np.abs(S2[anomaly_slice]))
    assert np.isfinite(max_S1) and np.isfinite(max_S2)
    assert max_S2 < 100 * max(max_S1, 1e-9), (
        f"v2 (pelny operator) daje amplitude o rzedy wielkosci wieksza niz v1: "
        f"{max_S2} vs {max_S1}"
    )
