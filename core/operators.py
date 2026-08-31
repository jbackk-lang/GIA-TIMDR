# ============================================================
#   OPERATORS — warstwa matematyczna rdzenia TIMDR
#   Λ–τ–ρ / J / M / ΔS / Defekty / Rezonanse
# ============================================================
"""
UZUPEŁNIENIE 2026-08-31 (audyt sesji + poprawki użytkownika): do tego
pliku dopisano funkcje aktywujące stałe z constants.py, które wcześniej
nie były przez NIC importowane (sprawdzone: `grep -rn "constants"
core/` dawało zero wyników) - progi typu DELTA_S_THRESHOLD były
niezależnie zduplikowane jako gołe literały w kilku miejscach zamiast
odczytywane z jednego źródła, a wagi/parametry typu STAB_*_WEIGHT,
SPECTRAL_*, PRIME_SENSITIVITY, RESONANCE_* były zdefiniowane, ale
dosłownie nigdzie nieużywane.

Zasada przyjęta przy tych poprawkach: gdzie zmiana to bezpieczny,
wstecznie kompatybilny parametr z domyślną wartością równą staremu
zachowaniu (op_deltaS, op_prime) - MODYFIKUJĘ istniejącą funkcję.
Gdzie zmiana wymagałaby zmiany kształtu/typu zwracanej wartości albo
sygnatury w sposób łamiący dotychczasowe wywołania z pipeline.py
(op_stab, op_spectral, op_R) - DODAJĘ nową, osobno nazwaną funkcję
obok starej, która zostaje nietknięta.
"""

import math

from .constants import (
    DELTA_S_THRESHOLD,
    DELTA_S_SOFT,
    DELTA_S_HARD,
    STAB_LAMBDA_WEIGHT,
    STAB_TAU_WEIGHT,
    STAB_RHO_WEIGHT,
    SPECTRAL_MIN_FREQ,
    SPECTRAL_MAX_FREQ,
    SPECTRAL_NORMALIZE,
    PRIME_SENSITIVITY,
    RESONANCE_MIN,
    RESONANCE_MAX_K,
    RESONANCE_SMOOTHING,
)

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

def adaptive_delta_s_threshold(tau_field: list, k: float = 2.5) -> float:
    """Próg adaptacyjny: k * odchylenie standardowe |Δτ| (różnic
    kolejnych wartości tau_field) - zamiast stałej '12' bez
    wyprowadzenia matematycznego. k=2.5 to typowa wartość progu
    "istotnego odchylenia" w analizie sygnałów, NIE wyprowadzona z
    danych TIMDR - do dostrojenia empirycznie na prawdziwych danych,
    nie autorytatywna liczba."""
    diffs = [abs(tau_field[i] - tau_field[i - 1]) for i in range(1, len(tau_field))]
    if not diffs:
        raise ValueError("tau_field za krótki, żeby policzyć odchylenia (potrzeba >= 2 elementy)")
    n = len(diffs)
    mean = sum(diffs) / n
    variance = sum((d - mean) ** 2 for d in diffs) / n
    return k * (variance ** 0.5)


def op_deltaS(tau_field: list, threshold=DELTA_S_THRESHOLD) -> list:
    """ΔS — defekt skrętu: punkty gwałtownej zmiany pola τ.

    `threshold` czyta teraz DELTA_S_THRESHOLD z constants.py zamiast
    literału `12` wklejonego na sztywno (poprzednia wersja - patrz git
    history) - to samo źródło prawdy, którego używa też defect_map() w
    diagnostics.py, więc nie mogą się już rozjechać niezależną edycją.

    threshold=None włącza próg ADAPTACYJNY (k*std(|Δτ|), patrz
    adaptive_delta_s_threshold() wyżej) zamiast stałej liczby - opt-in,
    nie zmienia domyślnego zachowania."""
    if threshold is None:
        threshold = adaptive_delta_s_threshold(tau_field)
    defects = []
    for i in range(1, len(tau_field)):
        if abs(tau_field[i] - tau_field[i - 1]) > threshold:
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

def op_prime(data: bytes, sensitivity: float = PRIME_SENSITIVITY) -> float:
    """PRIME — rytm skrętu: częstotliwość lokalnych zmian, skalowana
    przez `sensitivity` (domyślnie PRIME_SENSITIVITY=1.0 z constants.py -
    ta sama wartość, więc domyślne wywołanie zachowuje się identycznie
    jak poprzednio; wcześniej ta stała była zdefiniowana, ale nigdzie
    nieużywana)."""
    changes = 0
    last = data[0] if data else 0
    for b in data:
        if b != last:
            changes += 1
        last = b
    return sensitivity * changes / max(1, len(data))

# ------------------------------------------------------------
# 9. Operator SPECTRAL — widmo skrętu
# ------------------------------------------------------------

def op_spectral(data: bytes) -> list:
    """SPECTRAL — widmo skrętu (prosty FFT dyskretny). Niezmienione -
    patrz op_spectral_filtered() niżej dla wersji z obcięciem pasma i
    normalizacją (SPECTRAL_MIN_FREQ/MAX_FREQ/NORMALIZE z constants.py)."""
    N = len(data)
    spectrum = []
    for k in range(N):
        re = sum(data[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
        im = sum(data[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
        spectrum.append((re, im))
    return spectrum


def op_spectral_filtered(data: bytes, fs: float = 1.0) -> list:
    """SPECTRAL (obcięte pasmo + normalizacja) — jak op_spectral(), ale
    aktywuje SPECTRAL_MIN_FREQ/MAX_FREQ/NORMALIZE z constants.py, które
    wcześniej nie były używane NIGDZIE (op_spectral() liczyło pełne
    widmo bez żadnego obcięcia). `fs` (częstotliwość próbkowania, Hz) to
    NOWY parametr - bez niego MIN_FREQ/MAX_FREQ (podane w Hz) nie mają
    sensu fizycznego, bo sama DFT zna tylko indeksy k, nie Hz; fs=1.0
    (domyślne) traktuje częstotliwość jako znormalizowaną (cykle/próbkę).

    Zwraca listę (freq, re, im) tylko dla biner w [SPECTRAL_MIN_FREQ,
    SPECTRAL_MAX_FREQ], znormalizowaną do maks. amplitudy=1 jeśli
    SPECTRAL_NORMALIZE=True. Osobna funkcja od op_spectral() - dodana,
    nie modyfikuje starej (inny kształt wyniku: trójki z częstotliwością,
    nie same (re,im))."""
    N = len(data)
    if N == 0:
        return []
    spectrum = []
    for k in range(N):
        freq = k * fs / N
        if freq < SPECTRAL_MIN_FREQ or freq > SPECTRAL_MAX_FREQ:
            continue
        re = sum(data[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
        im = sum(data[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
        spectrum.append((freq, re, im))

    if SPECTRAL_NORMALIZE and spectrum:
        max_mag = max(math.hypot(re, im) for _freq, re, im in spectrum)
        if max_mag > 0:
            spectrum = [(freq, re / max_mag, im / max_mag) for freq, re, im in spectrum]

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
    """STAB — stabilizacja skrętu. Niezmienione - patrz
    op_stab_weighted()/op_stab_weighted_from_data() niżej dla wersji,
    która faktycznie używa STAB_LAMBDA_WEIGHT/STAB_TAU_WEIGHT/
    STAB_RHO_WEIGHT (wcześniej zdefiniowane w constants.py, ale
    nieużywane - ta funkcja ich nigdy nie stosowała)."""
    return op_lambda(op_J(data))


# ------------------------------------------------------------
# 12. Operator R lokalny (ρ) + EMA — dla op_stab_weighted i op_transition
# ------------------------------------------------------------

def _ema(values: list, alpha: float) -> list:
    """Wykładnicza średnia ruchoma: y[0]=x[0], y[i]=alpha*x[i]+(1-alpha)*y[i-1].
    Podręcznikowy wzór, biblioteka standardowa - używana przez
    op_R_local() do aktywowania RESONANCE_SMOOTHING z constants.py
    (wcześniej zdefiniowane, nigdy nieużyte)."""
    if not values:
        return []
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("alpha (współczynnik EMA) musi być w [0,1]")
    out = [values[0]]
    for v in values[1:]:
        out.append(alpha * v + (1.0 - alpha) * out[-1])
    return out


def op_R_local(data: bytes, window: int = 3, smoothing: float = None) -> list:
    """ρ / lokalny rezonans — ten sam wzór co istniejący, GLOBALNY op_R()
    (energia sqrt(Σb²)), ale liczony w przesuwnym oknie zamiast dla
    całego `data` naraz, więc ma wartość PER POZYCJA zamiast jednej
    liczby dla całego sygnału. NOWY operator - wypełnia lukę: op_R()
    sam z siebie nie da się użyć do maski per-pozycja (op_transition()
    poniżej), ani jako "kanał ρ" w op_stab_weighted() (potrzebne tam
    sekwencje, nie skalar).

    window=3 (domyślne) wyrównuje długość wyniku (len(data)-2) z
    op_tau() - te same indeksy (pozycja i w wyniku odpowiada oryginalnej
    pozycji i+1 w `data`), więc oba dają się bezpośrednio łączyć.

    smoothing=None (domyślne): surowe wartości energii, bez wygładzania.
    smoothing=RESONANCE_SMOOTHING (z constants.py) aktywuje EMA - tej
    stałej też nikt wcześniej nie używał."""
    if window < 1:
        raise ValueError("window musi być >= 1")
    n = len(data)
    if n < window:
        return []
    raw = [
        sum(b * b for b in data[i:i + window]) ** 0.5
        for i in range(n - window + 1)
    ]
    if smoothing is None:
        return raw
    return _ema(raw, smoothing)


# ------------------------------------------------------------
# 13. Operator STAB ważony — aktywuje STAB_*_WEIGHT
# ------------------------------------------------------------

def op_stab_weighted(lambda_channel: list, tau_channel: list, rho_channel: list) -> list:
    """Ważona stabilność trzech kanałów (Λ,τ,ρ), zgodnie z wagami z
    constants.py (STAB_LAMBDA_WEIGHT/STAB_TAU_WEIGHT/STAB_RHO_WEIGHT) -
    NOWA funkcja, NIE modyfikuje istniejącego op_stab(data) (który
    zostaje bez zmian - używany przez pipeline.py).

    Wymaga trzech sekwencji tej SAMEJ długości (rzuca ValueError w
    przeciwnym razie zamiast po cichu obcinać/dopełniać) - użyj
    op_stab_weighted_from_data(), żeby zbudować je poprawnie wyrównane
    z jednego strumienia bajtów."""
    n = len(lambda_channel)
    if len(tau_channel) != n or len(rho_channel) != n:
        raise ValueError(
            f"kanały muszą mieć tę samą długość: Λ={n}, τ={len(tau_channel)}, ρ={len(rho_channel)}"
        )
    return [
        STAB_LAMBDA_WEIGHT * lambda_channel[i]
        + STAB_TAU_WEIGHT * tau_channel[i]
        + STAB_RHO_WEIGHT * rho_channel[i]
        for i in range(n)
    ]


def op_stab_weighted_from_data(data: bytes, rho_window: int = 3) -> list:
    """Buduje trzy wyrównane kanały (Λ,τ,ρ) z JEDNEGO strumienia bajtów
    i woła op_stab_weighted() - wygodny odpowiednik starego
    op_stab(data), tym razem z faktycznie użytymi wagami.

    Wyrównanie: op_lambda(data) ma długość len(data) (pozycja i <-> i),
    op_tau(data) ma długość len(data)-2 (pozycje 1..len(data)-2) - więc
    kanał Λ jest przycinany do tego samego zakresu (`[1:-1]`). Kanał ρ =
    op_R_local(data, window=3) ma z definicji tę samą długość i te same
    indeksy co op_tau() (patrz jego docstring) - stąd rho_window=3
    domyślnie; inna wartość rho_window da inną długość i
    op_stab_weighted() to wykryje jako ValueError, zamiast po cichu
    dopasować błędne dane."""
    n = len(data)
    if n < 3:
        raise ValueError("dane muszą mieć długość >= 3, żeby zbudować wyrównane kanały Λ/τ/ρ")
    lambda_channel = list(op_lambda(data))[1:n - 1]
    tau_channel = op_tau(data)
    rho_channel = op_R_local(data, window=rho_window)
    return op_stab_weighted(lambda_channel, tau_channel, rho_channel)


# ------------------------------------------------------------
# 14. Skala rezonansu — teoretyczny sufit i granice adaptacyjne
# ------------------------------------------------------------

def theoretical_local_resonance_max(window: int, byte_max: int = 255) -> float:
    """Teoretyczne maksimum op_R_local(window) na danych bajtowych:
    sqrt(window * byte_max²) = byte_max * sqrt(window) - osiągane, gdy
    KAŻDY bajt w oknie ma wartość byte_max (255 domyślnie). To jest
    właściwa skala odniesienia dla RESONANCE_MAX (poprawka użytkownika,
    2026-08-31: stara stała RESONANCE_MAX=1e9 była ~2 000 000x za duża
    dla window=3, więc filtr górny nigdy się nie domykał - patrz
    RESONANCE_MAX_K niżej i constants.py)."""
    if window < 1:
        raise ValueError("window musi być >= 1")
    return byte_max * (window ** 0.5)


def adaptive_resonance_bounds(resonance_values: list, k: float = 3.0) -> tuple:
    """Granice rezonansu wyznaczone z DANYCH REFERENCYJNYCH zamiast z
    teoretycznego zakresu bajtów: (max(0, mean - k*std), mean + k*std) -
    "k-sigma band". Sensowniejsze niż theoretical_local_resonance_max(),
    gdy masz prawdziwy sygnał referencyjny (nie tylko wiesz, że to
    bajty 0-255) - wartości poza tym pasmem to albo szum (poniżej), albo
    nasycenie/anomalia (powyżej), w sensie STATYSTYKI TEGO KONKRETNEGO
    sygnału, nie abstrakcyjnego zakresu bajtów."""
    n = len(resonance_values)
    if n == 0:
        raise ValueError("resonance_values nie może być puste")
    mean = sum(resonance_values) / n
    variance = sum((v - mean) ** 2 for v in resonance_values) / n
    sigma = variance ** 0.5
    return (max(0.0, mean - k * sigma), mean + k * sigma)


# ------------------------------------------------------------
# 15. Operator TRANSITION — brakujący filtr "Obszarów przejściowych"
# ------------------------------------------------------------

def op_transition(
    data: bytes,
    delta_s_soft: float = DELTA_S_SOFT,
    delta_s_hard: float = DELTA_S_HARD,
    resonance_min: float = RESONANCE_MIN,
    resonance_max: float = None,
    resonance_smoothing: float = RESONANCE_SMOOTHING,
    rho_window: int = 3,
) -> dict:
    """Wykrywa obszary przejściowe (Transition Regions,
    docs/TIMDR_Full_Document_PL.md §2.4 i docs/GLOSSARY_EN_PL.md):
    granice między modalnościami, opisane w teorii jako strefy
    bifurkacji + wzmacniacze rezonansu. Ten operator NIE ISTNIAŁ
    wcześniej nigdzie w kodzie (sprawdzone przy audycie tej sesji) -
    teoria go nazywała, kod nigdy go nie implementował.

    Zwraca słownik trzech GĘSTYCH masek bool (długość len(data)-2, te
    same indeksy co op_tau()/op_R_local(), pozycja i <-> oryginalna
    pozycja i+1 w `data`):
      - "soft": ΔS > delta_s_soft (zmiana reżimu dynamiki)
      - "hard": ΔS > delta_s_hard (silna bifurkacja)
      - "transition": soft ORAZ lokalny rezonans w (resonance_min, resonance_max)
        (dokładna definicja z teorii: strefa bifurkacji + wzmocniony rezonans RAZEM)

    WAŻNE o rezonansie: stary, globalny op_R(data) zwraca JEDNĄ liczbę
    dla całego sygnału - nie da się z niej zbudować maski per-pozycja.
    Ten operator używa więc op_R_local() (lokalna, opcjonalnie
    wygładzona EMA wersja tego samego wzoru energii), nie op_R().

    NAPRAWIONE (poprawka użytkownika, 2026-08-31): resonance_max=None
    (domyślnie) NIE czyta już stałej RESONANCE_MAX=1e9 z constants.py
    (była ~2 000 000x za duża dla window=3 na bajtach - filtr górny
    nigdy się nie domykał, transition_mask ~= soft_mask). Zamiast tego
    liczy właściwy sufit DYNAMICZNIE, dopasowany do rho_window:

        resonance_max = RESONANCE_MAX_K * theoretical_local_resonance_max(rho_window)

    (RESONANCE_MAX_K=3.0 domyślnie - "3x teoretyczne maksimum energii
    okna" jako umowna granica nasycenia). Podaj własny resonance_max
    (liczbę), żeby to nadpisać - najlepiej przez
    adaptive_resonance_bounds() na prawdziwych danych referencyjnych,
    jeśli je masz (bardziej znaczące niż teoretyczny zakres bajtów).

    UCZCIWIE o resonance_min: RESONANCE_MIN=0.0 zostaje domyślne, ale
    op_R_local() z definicji zwraca wartości >= 0 - więc "r >
    resonance_min" jest prawie zawsze prawdziwe (poza zdegenerowanym
    oknem samych zer). To NIE jest realny filtr szumu, tylko formalna
    dolna granica dziedziny - dla realnego odcięcia szumu podaj
    resonance_min z adaptive_resonance_bounds() na danych
    referencyjnych."""
    n = len(data)
    tau_field = op_tau(data)
    if not tau_field:
        return {"soft": [], "hard": [], "transition": []}

    if resonance_max is None:
        resonance_max = RESONANCE_MAX_K * theoretical_local_resonance_max(rho_window)

    soft_defects = {i for i, _v in op_deltaS(tau_field, threshold=delta_s_soft)}
    hard_defects = {i for i, _v in op_deltaS(tau_field, threshold=delta_s_hard)}
    resonance = op_R_local(data, window=rho_window, smoothing=resonance_smoothing)

    m = len(tau_field)  # = n - 2, wspólny zakres indeksów
    soft_mask = [i in soft_defects for i in range(m)]
    hard_mask = [i in hard_defects for i in range(m)]
    resonance_mask = [resonance_min < r < resonance_max for r in resonance[:m]]
    transition_mask = [s and r for s, r in zip(soft_mask, resonance_mask)]

    return {"soft": soft_mask, "hard": hard_mask, "transition": transition_mask}
