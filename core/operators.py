# ============================================================
#   OPERATORS — warstwa matematyczna rdzenia TIMDR
#   Λ–τ–ρ / J / M / ΔS / Defekty / Rezonanse
# ============================================================

import math

# ------------------------------------------------------------
# 1. Operator Λ — redukcja lokalnej zmiany
# ------------------------------------------------------------

def op_lambda(data: bytes) -> bytes:
    """Λ — minimalna redukcja skrętu (lokalna różnica)."""
    out = bytearray()
    last = 0
    for b in data:
        out.append(b ^ last)
        last = b
    return bytes(out)

# ------------------------------------------------------------
# 2. Operator τ — pole skrętu (Laplacian)
# ------------------------------------------------------------

def op_tau(data: bytes) -> list:
    """τ — pole skrętu: ∇²S (Laplacian dyskretny)."""
    tau = []
    for i in range(1, len(data) - 1):
        lap = data[i - 1] - 2 * data[i] + data[i + 1]
        tau.append(lap)
    return tau

# ------------------------------------------------------------
# 3. Operator J — punktowa zmiana skrętu (dτ/ds)
# ------------------------------------------------------------

def op_J(data: bytes) -> bytes:
    """J — operator punktowy skrętu: dτ/ds."""
    out = bytearray()
    last = 0
    for b in data:
        out.append(b ^ last)
        last = b
    return bytes(out)

# ------------------------------------------------------------
# 4. Operator M — twist (orientacja zmiany)
# ------------------------------------------------------------

def op_M(data: bytes) -> bytes:
    """M — twist: orientacja zmiany."""
    return op_J(data)

# ------------------------------------------------------------
# 5. Operator ΔS — detekcja defektu skrętu
# ------------------------------------------------------------

def op_deltaS(tau_field: list) -> list:
    """ΔS — defekt skrętu: punkty gwałtownej zmiany pola τ."""
    defects = []
    for i in range(1, len(tau_field)):
        if abs(tau_field[i] - tau_field[i - 1]) > 12:  # próg topologiczny
            defects.append((i, tau_field[i]))
    return defects

# ------------------------------------------------------------
# 6. Operator R — rezonans (stabilizacja)
# ------------------------------------------------------------

def op_R(data: bytes) -> float:
    """R — rezonans: energia skrętu."""
    return sum(b * b for b in data) ** 0.5

# ------------------------------------------------------------
# 7. Operator E — emergencja (zamknięcie M²)
# ------------------------------------------------------------

def op_E(data: bytes) -> bytes:
    """E — emergencja: zamknięcie struktury."""
    return op_lambda(op_J(data))

# ------------------------------------------------------------
# 8. Operator PRIME — rytm skrętu (Twój rytm z I²D)
# ------------------------------------------------------------

def op_prime(data: bytes) -> float:
    """PRIME — rytm skrętu: częstotliwość lokalnych zmian."""
    changes = 0
    last = data[0] if data else 0
    for b in data:
        if b != last:
            changes += 1
        last = b
    return changes / max(1, len(data))

# ------------------------------------------------------------
# 9. Operator SPECTRAL — widmo skrętu
# ------------------------------------------------------------

def op_spectral(data: bytes) -> list:
    """SPECTRAL — widmo skrętu (prosty FFT dyskretny)."""
    N = len(data)
    spectrum = []
    for k in range(N):
        re = sum(data[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
        im = sum(data[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
        spectrum.append((re, im))
    return spectrum

# ------------------------------------------------------------
# 10. Operator REL — relacja skrętu (I(t))
# ------------------------------------------------------------

def op_rel(M: bytes) -> bytes:
    """REL — relacja skrętu: M(t)."""
    return op_lambda(M)

# ------------------------------------------------------------
# 11. Operator STAB — stabilizacja (Λ–τ–ρ)
# ------------------------------------------------------------

def op_stab(data: bytes) -> bytes:
    """STAB — stabilizacja skrętu."""
    return op_lambda(op_J(data))
