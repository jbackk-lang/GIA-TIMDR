import math
import numpy as np

def track_and_plot_entropy_evolution(steps=200):
    """
    Funkcja symuluje i śledzi dynamiczne zmiany entropii (Delta S)
    w pełnym cyklu obrotu operatora Tau (0 do 720 stopni) na powierzchni torusa.
    """
    # Dziedzina parametru czasu/kąta t (od 0 do 4*pi, czyli pełne 720 stopni)
    t_values = np.linspace(0, 4 * np.pi, steps)
    
    angles = []
    delta_S_profile = []
    
    for t in t_values:
        angle_deg = np.degrees(t) % 720.0
        angles.append(np.degrees(t))  # Ciągły wzrost kąta dla osi X
        
        # Matematyczna symulacja wpływu potrójnego skrętu Tetroidy na entropię układu.
        # Składnik cos(3t) symuluje nakładanie się 3 ścian osobliwości.
        # Składnik ujemny odpowiada za wymuszoną kompresję topologiczną w węźle torusa.
        base_interference = np.cos(3 * t) * np.sin(2 * t)
        compression_factor = -0.5 * (t / (2 * np.pi))  # Narastająca stabilizacja wraz z upływem cyklu
        
        # Wyliczenie wypadkowej dywergencji Delta S
        delta_S = base_interference + compression_factor
        delta_S_profile.append(delta_S)
        
    return angles, delta_S_profile

# Przygotowanie danych do wizualizacji za pomocą edugraph
angles, delta_S = track_and_plot_entropy_evolution()
