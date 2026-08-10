# ============================================================
#   DIAGNOSTICS — MEDIAN / XOR / SPECTRAL / PRIME
#   Rdzeń diagnostyczny TIMDR
# ============================================================

import math
from typing import List, Tuple

# ------------------------------------------------------------
# 1. MEDIAN FILTER — wygładzanie pola skrętu
# ------------------------------------------------------------

def median_filter(data: List[int], window: int = 3) -> List[int]:
    """MEDIAN — prosty filtr medianowy dla pola skrętu."""
    if window < 1:
        return data
    k = window // 2
    out = []
    for i in range(len(data)):
        w = data[max(0, i - k):min(len(data), i + k + 1)]
        out.append(sorted(w)[len(w) // 2])
    return out

# ------------------------------------------------------------
# 2. XOR ANALYZER — lokalna zmiana skrętu
# ------------------------------------------------------------

def xor_analyzer(data: bytes) -> List[int]:
    """XOR — analiza lokalnej zmiany (skręt punktowy)."""
    out = []
    last = 0
    for b in data:
        out.append(b ^ last)
        last = b
    return out

# ------------------------------------------------------------
# 3. SPECTRAL ANALYZER — widmo skrętu
# ------------------------------------------------------------

def spectral_analyzer(data: bytes) -> List[Tuple[float, float]]:
    """SPECTRAL — proste widmo skrętu (dyskretny FFT)."""
    N = len(data)
    if N == 0:
        return []
    spectrum = []
    for k in range(N):
        re = sum(data[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
        im = sum(data[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
        spectrum.append((re, im))
    return spectrum

# ------------------------------------------------------------
# 4. PRIME ANALYZER — rytm skrętu
# ------------------------------------------------------------

def prime_analyzer(data: bytes) -> float:
    """PRIME — rytm skrętu: gęstość lokalnych zmian."""
    if not data:
        return 0.0
    changes = 0
    last = data[0]
    for b in data:
        if b != last:
            changes += 1
        last = b
    return changes / len(data)

# ------------------------------------------------------------
# 5. DEFECT MAP — mapa defektów skrętu
# ------------------------------------------------------------

def defect_map(tau_field: List[int], threshold: int = 12) -> List[Tuple[int, int]]:
    """Mapa defektów: punkty gwałtownej zmiany pola τ."""
    defects = []
    for i in range(1, len(tau_field)):
        if abs(tau_field[i] - tau_field[i - 1]) > threshold:
            defects.append((i, tau_field[i]))
    return defects

# ------------------------------------------------------------
# 6. FULL DIAGNOSTIC — kompletna analiza jednego wejścia
# ------------------------------------------------------------

def full_diagnostic(data: bytes) -> dict:
    """Pełna diagnostyka: MEDIAN → XOR → SPECTRAL → PRIME → DEFECTS."""
    xor = xor_analyzer(data)
    median = median_filter(xor)
    spectral = spectral_analyzer(data)
    prime = prime_analyzer(data)
    defects = defect_map(median)

    return {
        "xor": xor,
        "median": median,
        "spectral": spectral,
        "prime": prime,
        "defects": defects,
    }
