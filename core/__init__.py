# ============================================================
#   CORE INIT — centralny interfejs TIMDR
# ============================================================

# --- Importy rdzenia ----------------------------------------

from .timdr_core import (
    lambda_tau_rho,
    lambda_tau_rho_inverse,
    J_operator,
    twist_M,
    TIMDR_pipeline
)

from .j_compression import (
    j_compress,
    j_decompress,
    j_hash
)

# --- Wystawienie API -----------------------------------------

__all__ = [
    # Transformacja Λ–τ–ρ
    "lambda_tau_rho",
    "lambda_tau_rho_inverse",

    # Operator skrętu J
    "J_operator",

    # Twist M
    "twist_M",

    # Pipeline TIMDR
    "TIMDR_pipeline",

    # Kompresja J
    "j_compress",
    "j_decompress",
    "j_hash",
]
