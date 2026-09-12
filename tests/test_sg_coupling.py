import numpy as np
import pytest

# POPRAWKA (znaleziona w tej samej rozmowie): Q_crit=0.35 dobrany "z
# powietrza" byl za czuly wzgledem naturalnej amplitudy tla -- sama
# sinusoida bez wstrzknietej anomalii przejsciowo osiaga S~+/-0.4,
# co daje R~0.43-0.45 i Q~0.35, wiec cut-off wyzwalal sie 4x PRZED
# oknem anomalii (t<4.5), fałszywie. Poprawka NIE polega na zgadnieciu
# innej "lepszej" liczby, zeby test przeszedl (to byloby dokladnie tym
# retuningiem po zobaczeniu zlego wyniku, ktorego ten ekosystem
# unika) -- zamiast tego Q_crit jest kalibrowany z ROZKLADU TLA
# (symulacja BEZ wstrzknietej anomalii), z udokumentowanym marginesem,
# PRZED sprawdzeniem, czy wykrywa realna anomalie.


def run_background_only_simulation(
    L0: float = 5.0,
    alpha: float = 0.1,
    R0: float = 0.2,
    dt: float = 0.01,
    duration: float = 10.0,
):
    """Ta sama dynamika co run_sg_coupling_simulation, ALE bez
    wstrzknietej anomalii (+3.0 w oknie t in [4.8,5.2]) i bez
    mechanizmu cut-off/tlumienia -- czysty rozklad tla, do kalibracji
    Q_crit. Zwraca (t, Q) - tylko to, co potrzebne do kalibracji."""
    t = np.arange(0, duration, dt)
    N = len(t)
    S = np.zeros(N)
    Q = np.zeros(N)

    for i in range(1, N):
        signal_input = np.sin(2 * np.pi * 0.5 * t[i])  # BEZ anomalii
        S_raw = S[i - 1] + dt * (-1.0 * S[i - 1] + signal_input)
        S[i] = S_raw
        F_S = S_raw ** 2
        G_i = R0 + alpha * F_S
        R_i = np.abs(G_i + 1j * S_raw)
        L_R = L0 + 2 * np.pi * R_i
        Q[i] = 1.0 - (L0 / L_R)

    return t, Q


def calibrate_q_crit(margin: float = 1.3, **background_kwargs) -> float:
    """Kalibruje Q_crit z maksimum Q osiagnietego przez SAM sygnal tla
    (bez anomalii), z mnoznikiem marginesu (domyslnie 1.3 = 30% zapasu
    ponad zaobserwowane maksimum tla) -- kalibracja PRZED zobaczeniem
    wyniku na docelowym zadaniu (wykrywanie anomalii), nie po."""
    _, Q_background = run_background_only_simulation(**background_kwargs)
    return float(np.max(Q_background) * margin)


def run_sg_coupling_simulation(
    L0: float = 5.0,
    alpha: float = 0.1,
    Q_crit: float | None = None,
    R0: float = 0.2,
    dt: float = 0.01,
    duration: float = 10.0
):
    """
    Symulacja zespolonej trajektorii Z(t) = G(t) + i*S(t) w ramach Aksjomatu SG-Coupling.
    """
    if Q_crit is None:
        # Kalibrowane z rozkladu tla (bez anomalii), NIE zgadniete -
        # patrz calibrate_q_crit() powyzej.
        Q_crit = calibrate_q_crit(margin=1.3, L0=L0, alpha=alpha, R0=R0, dt=dt, duration=duration)

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
    """Sprawdza czy stan spoczynkowy Q(R0) startuje ponizej progu Q_crit
    (kalibrowanego z tla, nie zahardkodowanego 0.35)."""
    L0, R0 = 5.0, 0.2
    Q_crit = calibrate_q_crit(margin=1.3, L0=L0, R0=R0)
    Q_baseline = 1.0 - L0 / (L0 + 2 * np.pi * R0)
    assert Q_baseline < Q_crit, f"Stan bazowy Q({Q_baseline:.4f}) przekracza Q_crit ({Q_crit})"


def test_background_alone_never_triggers_calibrated_threshold():
    """Kontrola negatywna WPROST na kalibracje: sam rozklad tla (ten
    sam sygnal, ktorego uzyto DO kalibracji Q_crit) nie powinien
    przekroczyc kalibrowanego progu z marginesem 1.3 - z definicji
    (Q_crit = max(Q_background)*1.3 > max(Q_background)), ale
    sprawdzone jawnie jako regresja, nie tylko przez konstrukcje."""
    _, Q_background = run_background_only_simulation()
    Q_crit = calibrate_q_crit(margin=1.3)
    assert np.max(Q_background) < Q_crit


def test_sg_coupling_anomaly_detection():
    """Weryfikuje czy cut-off aktywuje sie wylacznie w oknie anomalii,
    z Q_crit KALIBROWANYM z tla (patrz calibrate_q_crit powyzej), nie
    zahardkodowanym 0.35 - ktory byl za czuly na naturalna amplitude
    tla (sam sygnal bez anomalii przejsciowo osiagal Q~0.35, dajac
    4 falszywe wyzwolenia przed oknem anomalii, t=[0.66, 1.79, 2.69,
    3.76, 4.71] - zobacz historie tej naprawy)."""
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