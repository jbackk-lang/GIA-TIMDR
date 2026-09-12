import numpy as np
import pytest

def run_sg_coupling_simulation(
    L0: float = 5.0,
    alpha: float = 0.1,
    Q_crit: float = 0.35,
    R0: float = 0.2,
    dt: float = 0.01,
    duration: float = 10.0
):
    """
    Symulacja zespolonej trajektorii Z(t) = G(t) + i*S(t) w ramach Aksjomatu SG-Coupling.
    """
    t = np.arange(0, duration, dt)
    N = len(t)
    
    G = np.zeros(N)
    S = np.zeros(N)
    R = np.zeros(N)
    Q = np.zeros(N)
    cutoff_triggered = np.zeros(N, dtype=bool)
    
    G[0] = R0
    S[0] = 0.0
    
    for i in range(1, N):
        # Generowanie sygnału wejściowego (anomalia w oknie t ∈ [4.8, 5.2])
        signal_input = np.sin(2 * np.pi * 0.5 * t[i])
        if 4.8 <= t[i] <= 5.2:
            signal_input += 3.0
            
        S_raw = S[i-1] + dt * (-1.0 * S[i-1] + signal_input)
        
        # [SG-1] Wskaźnik sygnałowy F[S] moduluje geometrię G(t)
        F_S = S_raw**2
        G[i] = R0 + alpha * F_S
        S[i] = S_raw
        
        # Zespolony stan Z(t) oraz promień obwiedni R(t) = |Z(t)|
        Z = G[i] + 1j * S[i]
        R[i] = np.abs(Z)
        
        # [SG-2] Parametr obwiedni Q(R)
        L_R = L0 + 2 * np.pi * R[i]
        Q[i] = 1.0 - (L0 / L_R)
        
        # [SG-3] Sprzężenie zwrotne i operator cut-off Θ po przekroczeniu Q_crit
        if Q[i] > Q_crit:
            cutoff_triggered[i] = True
            # Operator rzutujący Θ: odbicie fazy + tłumienie urojonej składowej
            Z_damped = G[i] - 1j * (0.1 * S[i])
            G[i] = Z_damped.real
            S[i] = Z_damped.imag
            
    return t, G, S, R, Q, cutoff_triggered


def test_sg_coupling_baseline_stability():
    """Sprawdza czy stan spoczynkowy Q(R0) startuje poniżej progu Q_crit."""
    L0, R0, Q_crit = 5.0, 0.2, 0.35
    Q_baseline = 1.0 - L0 / (L0 + 2 * np.pi * R0)
    assert Q_baseline < Q_crit, f"Stan bazowy Q({Q_baseline:.4f}) przekracza Q_crit ({Q_crit})"


def test_sg_coupling_anomaly_detection():
    """Weryfikuje czy cut-off aktywuje się wyłącznie w oknie anomalii."""
    t, G, S, R, Q, cutoff = run_sg_coupling_simulation()
    
    # Brak zdarzeń przed anomalią (t < 4.5)
    assert np.sum(cutoff[t < 4.5]) == 0, "Wyzwolono cut-off w stanie bezszumnym przed anomalią"
    
    # Aktywacja cut-off w oknie anomalii (t ∈ [4.8, 5.2])
    anomaly_mask = (t >= 4.8) & (t <= 5.2)
    assert np.sum(cutoff[anomaly_mask]) > 0, "Brak detekcji anomalii w wyznaczonym oknie"


def test_sg_coupling_reflection_damping():
    """Sprawdza czy operator Θ poprawnie odbija znak składowej urojonej (S)."""
    t, G, S, R, Q, cutoff = run_sg_coupling_simulation()
    
    # Znajdź pierwszą próbkę z aktywowanym cut-offem
    first_cutoff_idx = np.where(cutoff)[0][0]
    
    # W momencie cut-offu składowa S powinna zmienić znak na ujemny (dzięki -1j)
    assert S[first_cutoff_idx] < 0, "Operator Θ nie wykonał odbicia składowej sygnałowej"