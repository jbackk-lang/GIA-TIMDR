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

# RESONANCE_MIN=0.0: uczciwie - op_R_local() zwraca sqrt(suma kwadratow),
# WIEC ZAWSZE >= 0. Prog "> 0.0" jest wiec prawie zawsze spelniony (poza
# zdegenerowanym przypadkiem okna samych zer) - to NIE jest realny dolny
# filtr szumu, tylko formalna dolna granica dziedziny. Zeby MIN mial
# realna tresc sygnalowa (odcinac szum, nie tylko "nieujemne"), trzeba go
# wyznaczyc z danych referencyjnych - patrz
# operators.adaptive_resonance_bounds().
RESONANCE_MIN = 0.0

# RESONANCE_MAX=1e9: HISTORYCZNA wartosc, uczciwie martwa dla danych
# bajtowych - teoretyczne maksimum op_R_local(window=3) na bajtach
# 0-255 to 255*sqrt(3) =~ 442, czyli 1e9 jest ~2 000 000x za duze i
# warunek "R < RESONANCE_MAX" jest praktycznie zawsze prawdziwy (audyt
# sesji 2026-08-31, potwierdzone przez uzytkownika). op_transition() NIE
# UZYWA juz tej stalej jako domyslnej - liczy wlasciwy sufit dynamicznie
# przez RESONANCE_MAX_K * operators.theoretical_local_resonance_max(window)
# (patrz nizej i operators.py). Stala zostaje tu jako udokumentowany
# przyklad "martwej"/niedostrojonej wartosci, nie jako zalecany domyslny.
RESONANCE_MAX = 1e9

# Mnoznik k we wzorze RESONANCE_MAX = k * teoretyczne_maksimum(window)
# (sugestia uzytkownika: k w [1,5], 3.0 to srodek zakresu) - w
# przeciwienstwie do stalego RESONANCE_MAX, ten mnoznik NIE zalezy od
# window/zakresu bajtow, wiec nie "rozjezdza sie", gdy rho_window w
# op_transition() sie zmienia.
RESONANCE_MAX_K = 3.0

RESONANCE_SMOOTHING = 0.15

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
