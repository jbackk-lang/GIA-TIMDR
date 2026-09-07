# ============================================================
#   CONSTANTS — stałe rdzenia TIMDR
#   MAGIC / progi / parametry skrętu / stabilizacja / widmo
# ============================================================

# ------------------------------------------------------------
# 1. MAGIC — znacznik kompresji J
# ------------------------------------------------------------

MAGIC = b'JCOMP'        # znacznik skrętu dla kompresji J
MAGIC_LEN = len(MAGIC)  # długość znacznika

# ------------------------------------------------------------
# 2. Progi ΔS — detekcja defektów skrętu
# ------------------------------------------------------------

DELTA_S_THRESHOLD = 12   # próg gwałtownej zmiany pola τ
DELTA_S_HARD = 18        # próg twardy (silny defekt)
DELTA_S_SOFT = 8         # próg miękki (początek defektu)

# ------------------------------------------------------------
# 3. Parametry skrętu (τ, J, M)
# ------------------------------------------------------------

TAU_SCALE = 1.0          # skala Laplasjanu τ
J_SCALE = 1.0            # skala operatora J
M_SCALE = 1.0            # skala twistu M

# ------------------------------------------------------------
# 4. Stabilizacja Λ–τ–ρ
# ------------------------------------------------------------

STAB_LAMBDA_WEIGHT = 1.0
STAB_TAU_WEIGHT = 0.8
STAB_RHO_WEIGHT = 0.6

# ------------------------------------------------------------
# 5. Rezonans R
# ------------------------------------------------------------

RESONANCE_MIN = 0.0
RESONANCE_MAX = 1e9
RESONANCE_SMOOTHING = 0.15

# NAPRAWIONE (audyt 2026-08-31, dokonczone przy naprawie importu
# tests/test_operators_wiring.py): RESONANCE_MAX=1e9 jest ~2 000 000x
# za duze dla lokalnej energii op_R_local() na oknie bajtow (teoretyczne
# maksimum dla window=3 to 255*sqrt(3)~=442 - patrz
# theoretical_local_resonance_max()) - "saturacja" wzgledem tej stalej
# nigdy nie nastepowala, wiec byla martwym progiem. RESONANCE_MAX_K to
# mnoznik teoretycznego maksimum (nie stala bezwzgledna) - uzywany jako
# DOMYSLNY, dynamiczny sufit rezonansu w op_transition() gdy
# resonance_max=None (skala bajtow: dziesiatki-setki, nie miliardy).
# RESONANCE_MAX (powyzej) zostaje NIETKNIETY dla wstecznej
# kompatybilnosci z kodem, ktory go juz czyta wprost.
RESONANCE_MAX_K = 3.0

# ------------------------------------------------------------
# 6. Widmo skrętu (SPECTRAL)
# ------------------------------------------------------------

SPECTRAL_NORMALIZE = True
SPECTRAL_MAX_FREQ = 2048
SPECTRAL_MIN_FREQ = 1

# ------------------------------------------------------------
# 7. Rytm skrętu (PRIME)
# ------------------------------------------------------------

PRIME_SENSITIVITY = 1.0
PRIME_MIN_CHANGES = 0
PRIME_MAX_CHANGES = 1e6

# ------------------------------------------------------------
# 8. Pipeline TIMDR
# ------------------------------------------------------------

PIPELINE_VERSION = "1.0.0"
PIPELINE_NAME = "TIMDR T→I→M→I(t)→R→E"

# ------------------------------------------------------------
# 9. Diagnostyka
# ------------------------------------------------------------

MEDIAN_WINDOW_DEFAULT = 3
XOR_BASE = 0

# ------------------------------------------------------------
# 10. Globalne ustawienia rdzenia
# ------------------------------------------------------------

DEBUG = False
VERBOSE = False
