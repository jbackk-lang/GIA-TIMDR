# ============================================================
#   TIMDR CORE — Λ–τ–ρ / J / M / Pipeline
# ============================================================

# --- 1. Λ–τ–ρ: podstawowa transformacja skrętu ----------------

def lambda_tau_rho(data: bytes) -> bytes:
    """Minimalna transformacja TIMDR: redukcja → pole → stabilizacja."""
    out = bytearray()
    last = 0
    for b in data:
        d = b ^ last
        out.append(d)
        last = b
    return bytes(out)

def lambda_tau_rho_inverse(data: bytes) -> bytes:
    """Odwrócenie transformacji."""
    out = bytearray()
    last = 0
    for d in data:
        b = d ^ last
        out.append(b)
        last = b
    return bytes(out)

# --- 2. J: operator skrętu ------------------------------------

def J_operator(data: bytes) -> bytes:
    """Operator punktowy skrętu — dτ/ds."""
    out = bytearray()
    last = 0
    for b in data:
        out.append(b ^ last)
        last = b
    return bytes(out)

# --- 3. M: twist ----------------------------------------------

def twist_M(data: bytes) -> bytes:
    """Minimalny twist — orientacja zmiany."""
    return J_operator(data)

# --- 4. Pipeline TIMDR ----------------------------------------

def TIMDR_pipeline(data: bytes):
    """T → I → M → I(t) → R → E"""
    T = data
    I = lambda_tau_rho(T)
    M = twist_M(I)
    It = M  # relacja + czas (tu minimalna wersja)
    R = lambda_tau_rho_inverse(It)
    E = R  # emergencja struktury
    return {
        "T": T,
        "I": I,
        "M": M,
        "I(t)": It,
        "R": R,
        "E": E
    }
