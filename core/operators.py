# ============================================================
#   OPERATORS — warstwa matematyczna rdzenia TIMDR
#   Λ–τ–ρ / J / M / ΔS / Defekty / Rezonanse
# ============================================================
#
# NAPRAWIONE (audyt sesji 2026-08-31, dokonczone przy naprawie
# ImportError w tests/test_operators_wiring.py): constants.py byl
# plikiem, ktorego NIC nie importowalo - kilka progow/wag bylo
# zdefiniowanych, ale nigdzie nieuzywanych albo niezaleznie
# zduplikowanych (np. '12' tutaj i w core/diagnostics.py). Ponizej
# doszyto: op_deltaS z jednym zrodlem prawdy (DELTA_S_THRESHOLD) i
# opcja adaptacyjna, op_R_local (lokalny rezonans + EMA),
# op_stab_weighted (aktywacja STAB_*_WEIGHT), op_spectral_filtered
# (SPECTRAL_MIN/MAX_FREQ, NORMALIZE), op_prime z PRIME_SENSITIVITY,
# op_transition (filtr "Obszarow przejsciowych"). Stare funkcje
# (op_stab, op_spectral, op_R) NIETKNIETE - wsteczna kompatybilnosc z
# pipeline.py, zweryfikowana testami regresyjnymi w
# tests/test_operators_wiring.py.

import math
import statistics

from core.constants import (
    DELTA_S_THRESHOLD,
    DELTA_S_SOFT,
    DELTA_S_HARD,
    STAB_LAMBDA_WEIGHT,
    STAB_TAU_WEIGHT,
    STAB_RHO_WEIGHT,
    PRIME_SENSITIVITY,
    SPECTRAL_MIN_FREQ,
    SPECTRAL_MAX_FREQ,
    SPECTRAL_NORMALIZE,
    RESONANCE_MIN,
    RESONANCE_MAX_K,
    RESONANCE_SMOOTHING,  # noqa: F401 (typowa wartosc do przekazania jawnie w op_R_local(smoothing=...), patrz docstring)
)
from core.diagnostics import defect_map

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

def op_deltaS(tau_field: list, threshold=DELTA_S_THRESHOLD) -> list:
    """ΔS — defekt skrętu: punkty gwałtownej zmiany pola τ.

    `threshold`: próg stały (domyślnie DELTA_S_THRESHOLD - jedno
    źródło prawdy dzielone z `core.diagnostics.defect_map`, na którym
    ta funkcja się teraz opiera). `threshold=None` włącza próg
    ADAPTACYJNY (`adaptive_delta_s_threshold`), liczony na żywo z
    samego `tau_field`."""
    if threshold is None:
        threshold = adaptive_delta_s_threshold(tau_field)
    return defect_map(tau_field, threshold=threshold)


def adaptive_delta_s_threshold(tau_field: list, k: float = 2.5) -> float:
    """Próg adaptacyjny dla op_deltaS/defect_map: `k * odchylenie
    standardowe (populacyjne) kolejnych różnic` |tau[i]-tau[i-1]| —
    BEZ składnika średniej (nie mean+k*std): pole o stałej, dużej
    różnicy między kolejnymi punktami (brak wariancji różnic) daje
    próg 0, nie próg równy tej różnicy — bo "stała duża różnica" to tu
    NORMA pola, nie odchylenie od normy, którą ma wykrywać ten próg."""
    if len(tau_field) < 2:
        raise ValueError(
            "adaptive_delta_s_threshold wymaga co najmniej 2 punktów (żeby policzyć choć jedną różnicę)"
        )
    diffs = [abs(tau_field[i] - tau_field[i - 1]) for i in range(1, len(tau_field))]
    return k * statistics.pstdev(diffs)

# ------------------------------------------------------------
# 6. Operator R — rezonans (stabilizacja)
# ------------------------------------------------------------

def op_R(data: bytes) -> float:
    """R — rezonans: energia skrętu."""
    return sum(b * b for b in data) ** 0.5


def op_R_local(data: bytes, window: int = 3, smoothing=None) -> list:
    """R_local — lokalny rezonans: energia (sqrt sumy kwadratów) w
    przesuwnym oknie długości `window`, tryb "valid" (jak `op_tau`) —
    dla `window=3` daje DOKŁADNIE `len(data)-2` wartości, wyrównane
    indeks-w-indeks z `op_tau(data)` (oba centrowane na tych samych
    trójkach punktów).

    `smoothing=None` (domyślnie): surowe wartości lokalnej energii.
    `smoothing=alpha` w (0,1]: wygładzanie EMA (typowa wartość:
    `RESONANCE_SMOOTHING` z `core.constants`) — `y[0]=x[0]`,
    `y[i]=alpha*x[i]+(1-alpha)*y[i-1]`."""
    if window < 1:
        raise ValueError("window musi być dodatnią liczbą całkowitą")
    n = len(data)
    if n < window:
        return []
    raw = [
        math.sqrt(sum(b * b for b in data[start:start + window]))
        for start in range(n - window + 1)
    ]
    if smoothing is None or not raw:
        return raw
    out = [raw[0]]
    for x in raw[1:]:
        out.append(smoothing * x + (1 - smoothing) * out[-1])
    return out


def theoretical_local_resonance_max(window: int, byte_max: int = 255) -> float:
    """Teoretyczne maksimum `op_R_local(window=window)` na bajtach
    `0..byte_max`: osiągane, gdy KAŻDY bajt okna = `byte_max` —
    `byte_max * sqrt(window)`. Zastępuje martwą stałą
    `RESONANCE_MAX=1e9` (patrz `core.constants`) jako sufit rezonansu
    faktycznie osiągalny na danych bajtowych, nie sufit ~2 000 000x za
    duży."""
    if window < 1:
        raise ValueError("window musi być dodatnią liczbą całkowitą")
    return byte_max * math.sqrt(window)

# ------------------------------------------------------------
# 7. Operator E — emergencja (zamknięcie M²)
# ------------------------------------------------------------

def op_E(data: bytes) -> bytes:
    """E — emergencja: zamknięcie struktury."""
    return op_lambda(op_J(data))

# ------------------------------------------------------------
# 8. Operator PRIME — rytm skrętu (Twój rytm z I²D)
# ------------------------------------------------------------

def op_prime(data: bytes, sensitivity: float = PRIME_SENSITIVITY) -> float:
    """PRIME — rytm skrętu: częstotliwość lokalnych zmian, skalowana
    przez `sensitivity` (domyślnie `PRIME_SENSITIVITY=1.0` z
    `core.constants` — wsteczna kompatybilność: wynik identyczny jak
    przed dodaniem tego parametru)."""
    changes = 0
    last = data[0] if data else 0
    for b in data:
        if b != last:
            changes += 1
        last = b
    return (changes / max(1, len(data))) * sensitivity

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


def op_spectral_filtered(data: bytes, fs: float = 1.0) -> list:
    """SPECTRAL_FILTERED — widmo `op_spectral()` z częstotliwością
    fizyczną `freq_k = k*fs/N` dołączoną do każdego bina i
    ograniczoną do pasma `[SPECTRAL_MIN_FREQ, SPECTRAL_MAX_FREQ]` z
    `core.constants` (czytane jako atrybuty TEGO modułu przy każdym
    wywołaniu — można je podmienić w locie przez
    `core.operators.SPECTRAL_MIN_FREQ = ...`, patrz testy). Gdy
    `SPECTRAL_NORMALIZE` jest prawdziwe, amplitudy w paśmie są
    znormalizowane tak, by maksymalny moduł `(re,im)` wynosił 1.0.

    Zwraca listę `(freq, re, im)` — inny kształt niż `op_spectral()`
    (`(re, im)`), celowo: `op_spectral()` zostaje NIETKNIĘTE dla
    wstecznej kompatybilności (patrz test regresyjny)."""
    raw = op_spectral(data)
    n = len(data)
    if n == 0:
        return []
    filtered = []
    for k, (re, im) in enumerate(raw):
        freq = k * fs / n
        if SPECTRAL_MIN_FREQ <= freq <= SPECTRAL_MAX_FREQ:
            filtered.append((freq, re, im))
    if SPECTRAL_NORMALIZE and filtered:
        max_mag = max(math.hypot(re, im) for _freq, re, im in filtered)
        if max_mag > 0:
            filtered = [(freq, re / max_mag, im / max_mag) for freq, re, im in filtered]
    return filtered

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


def op_stab_weighted(lam: list, tau: list, rho: list) -> list:
    """STAB ważony — aktywacja stałych `STAB_LAMBDA_WEIGHT`,
    `STAB_TAU_WEIGHT`, `STAB_RHO_WEIGHT` z `core.constants` (były
    zdefiniowane, ale nigdzie nieużywane — patrz nagłówek modułu):
    kombinacja liniowa trzech kanałów, wyrównanych długością przez
    wołającego (patrz `op_stab_weighted_from_data` po gotowe
    wyrównanie z surowych bajtów)."""
    if not (len(lam) == len(tau) == len(rho)):
        raise ValueError("lam, tau, rho muszą mieć tę samą długość")
    return [
        STAB_LAMBDA_WEIGHT * l + STAB_TAU_WEIGHT * t + STAB_RHO_WEIGHT * r
        for l, t, r in zip(lam, tau, rho)
    ]


def op_stab_weighted_from_data(data: bytes) -> list:
    """Buduje trzy kanały (Λ, τ, ρ) wyrównane długością z surowych
    bajtów i woła `op_stab_weighted`: `lam` = `op_lambda(data)` bez
    pierwszego i ostatniego elementu (wyrównanie z `op_tau`, który z
    natury nie ma wartości na krańcach), `tau` = `op_tau(data)`,
    `rho` = `op_R_local(data, window=3)` (też `len(data)-2` wartości —
    patrz `op_R_local`)."""
    if len(data) < 3:
        raise ValueError("op_stab_weighted_from_data wymaga co najmniej 3 bajtów (tyle, co op_tau)")
    lam = list(op_lambda(data))[1:len(data) - 1]
    tau = op_tau(data)
    rho = op_R_local(data, window=3)
    return op_stab_weighted(lam, tau, rho)

# ------------------------------------------------------------
# 12. Operator TRANSITION — "Obszary przejściowe" (§2.4 dokumentacji
#     teoretycznej) i pomocnicze progi rezonansu adaptacyjnego
# ------------------------------------------------------------


def adaptive_resonance_bounds(values: list, k: float = 3.0) -> tuple:
    """Pasmo `[mean-k*std, mean+k*std]` (odchylenie standardowe
    populacyjne) dla listy wartości rezonansu — dolna granica
    OBCINANA do 0.0 (energia/amplituda z definicji nieujemna, pasmo
    nigdy nie schodzi poniżej zera nawet przy dużej wariancji)."""
    if not values:
        raise ValueError("adaptive_resonance_bounds wymaga niepustej listy wartości")
    mean = sum(values) / len(values)
    std = statistics.pstdev(values)
    lo = max(0.0, mean - k * std)
    hi = mean + k * std
    return lo, hi


def op_transition(
    data: bytes,
    delta_s_soft: float = DELTA_S_SOFT,
    delta_s_hard: float = DELTA_S_HARD,
    resonance_min: float = RESONANCE_MIN,
    resonance_max=None,
) -> dict:
    """TRANSITION — filtr "Obszarów przejściowych" z §2.4 dokumentacji
    teoretycznej: dla każdej pozycji `op_tau(data)` zwraca TRZY gęste
    (pełnej długości, wyrównane z `tau_field`) maski boolowskie:

    - `soft`: `|Δτ| > delta_s_soft` (miękki próg defektu, patrz
      `DELTA_S_SOFT`),
    - `hard`: `|Δτ| > delta_s_hard` (twardy próg, `DELTA_S_HARD`) —
      z definicji podzbiór `soft` dla `delta_s_hard >= delta_s_soft`,
    - `transition`: `soft` ORAZ lokalna energia (`op_R_local(data,
      window=3)`, wyrównana z `tau_field` z konstrukcji) mieści się w
      paśmie `[resonance_min, resonance_max]` — "obszar przejściowy"
      to miejsce, gdzie zaszła zmiana WYSTARCZAJĄCO duża (soft), ale
      NIE tak ekstremalna, by wypaść poza akceptowalne pasmo
      rezonansu (np. czysty szum impulsowy poza skalą danych).

    `resonance_max=None` (domyślnie) liczy sufit DYNAMICZNIE jako
    `RESONANCE_MAX_K * theoretical_local_resonance_max(3)` —
    NAPRAWIONE (audyt 2026-08-31): stara, martwa stała
    `RESONANCE_MAX=1e9` była ~2 000 000x za duża dla energii lokalnej
    na bajtach (teoretyczne maksimum ~442) — "saturacja" nigdy nie
    następowała, próg był w praktyce nieaktywny. Nowy domyślny sufit
    jest w skali bajtów (dziesiątki-setki), nie miliardów.

    Dla `len(data) < 3` (za mało na `op_tau`) zwraca trzy puste listy,
    nie rzuca wyjątku."""
    if len(data) < 3:
        return {"soft": [], "hard": [], "transition": []}

    if resonance_max is None:
        resonance_max = RESONANCE_MAX_K * theoretical_local_resonance_max(3)

    tau_field = op_tau(data)
    resonance = op_R_local(data, window=3)  # wyrównane z tau_field z konstrukcji (oba "valid" na trójkach)

    soft, hard, transition = [], [], []
    prev = tau_field[0] if tau_field else 0
    for idx, cur in enumerate(tau_field):
        diff = abs(cur - prev) if idx > 0 else 0  # brak poprzednika w tau_field -> brak skoku
        is_soft = diff > delta_s_soft
        is_hard = diff > delta_s_hard
        in_band = resonance_min <= resonance[idx] <= resonance_max
        soft.append(is_soft)
        hard.append(is_hard)
        transition.append(is_soft and in_band)
        prev = cur
    return {"soft": soft, "hard": hard, "transition": transition}
