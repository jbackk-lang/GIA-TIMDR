# ============================================================
#   PIPELINE TIMDR — T → I → M → I(t) → R → E
#   Integracja rdzenia, operatorów, diagnostyki i kompresji J
# ============================================================

from .timdr_core import (
    lambda_tau_rho,
    lambda_tau_rho_inverse,
    J_operator,
    twist_M
)

from .j_compression import (
    j_compress,
    j_decompress
)

from .operators import (
    op_lambda,
    op_tau,
    op_J,
    op_M,
    op_deltaS,
    op_R,
    op_E,
    op_prime,
    op_spectral,
    op_rel,
    op_stab
)

from .diagnostics import (
    median_filter,
    xor_analyzer,
    spectral_analyzer,
    prime_analyzer,
    defect_map,
    full_diagnostic
)


# ------------------------------------------------------------
# 1. PIPELINE: T → I → M → I(t) → R → E
# ------------------------------------------------------------

def TIMDR_pipeline(data: bytes) -> dict:
    """
    Główny pipeline TIMDR:
    T — momentum (wejście)
    I — process (Λ–τ–ρ)
    M — twist (J)
    I(t) — relation + time
    R — stabilization
    E — emergence
    """

    # --- T: momentum (surowe dane) ---------------------------
    T = data

    # --- I: process (Λ–τ–ρ) ----------------------------------
    I = lambda_tau_rho(T)

    # --- M: twist (J) ----------------------------------------
    M = twist_M(I)

    # --- I(t): relation + time -------------------------------
    It = op_rel(M)

    # --- R: stabilization ------------------------------------
    R = lambda_tau_rho_inverse(It)

    # --- E: emergence ----------------------------------------
    E = op_E(R)

    return {
        "T": T,
        "I": I,
        "M": M,
        "I(t)": It,
        "R": R,
        "E": E
    }


# ------------------------------------------------------------
# 2. PIPELINE + DIAGNOSTYKA
# ------------------------------------------------------------

def TIMDR_pipeline_diagnostic(data: bytes) -> dict:
    """
    Pipeline + pełna diagnostyka:
    MEDIAN → XOR → SPECTRAL → PRIME → DEFECTS
    """

    base = TIMDR_pipeline(data)
    diag = full_diagnostic(data)

    return {
        "pipeline": base,
        "diagnostic": diag
    }


# ------------------------------------------------------------
# 3. PIPELINE + KOMpresja J
# ------------------------------------------------------------

def TIMDR_pipeline_compressed(data: bytes) -> dict:
    """
    Pipeline z kompresją J jako stabilizatorem.
    Zgodnie z zasadą: TIMDR działa tylko z kompresją J.
    """

    compressed = j_compress(data)
    decompressed = j_decompress(compressed)

    base = TIMDR_pipeline(decompressed)

    return {
        "compressed": compressed,
        "decompressed": decompressed,
        "pipeline": base
    }


# ------------------------------------------------------------
# 4. PIPELINE FULL — wszystko naraz
# ------------------------------------------------------------

def TIMDR_pipeline_full(data: bytes) -> dict:
    """
    Pełny pipeline:
    - kompresja J
    - pipeline TIMDR
    - diagnostyka
    - operatory
    """

    compressed = j_compress(data)
    decompressed = j_decompress(compressed)

    base = TIMDR_pipeline(decompressed)
    diag = full_diagnostic(decompressed)

    ops = {
        "lambda": op_lambda(decompressed),
        "tau": op_tau(decompressed),
        "J": op_J(decompressed),
        "M": op_M(decompressed),
        "deltaS": op_deltaS(op_tau(decompressed)),
        "R": op_R(decompressed),
        "E": op_E(decompressed),
        "prime": op_prime(decompressed),
        "spectral": op_spectral(decompressed),
        "rel": op_rel(op_M(decompressed)),
        "stab": op_stab(decompressed)
    }

    return {
        "compressed": compressed,
        "decompressed": decompressed,
        "pipeline": base,
        "diagnostic": diag,
        "operators": ops
    }
