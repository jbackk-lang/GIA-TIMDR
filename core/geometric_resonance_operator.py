# core/geometric_resonance_operator.py
"""
geometric_resonance_operator.py -- implementacja Aksjomatu G5
(`docs/theory/Axioms_G_TIMDR_Geometry.md`): operator **G-Rezonans**
gałęzi geometrycznej TIMDR.

STATUS: to podniesienie do rangi formalnego operatora gałęzi G
prototypu zbudowanego wcześniej w tej samej sesji wyłącznie dla
trójwęzła (`core/trefoil_resonance_model.py`, pierścień 3 węzłów) --
patrz `docs/geometry/TIMDR_GResonance_Operator.md` po pełny opis,
dokładny status walidacji (co jest potwierdzone na N=3, co jest tylko
sprawdzone strukturalnie na innym N, co NIE jest zwalidowane
empirycznie) i uczciwe ograniczenia. `trefoil_resonance_model.py` jest
teraz CIENKĄ WARSTWĄ nad tym modułem (N=3, stałe geometryczne idealnego
trójwęzła) -- zachowaną dla wstecznej kompatybilności z istniejącymi
testami/dokumentacją, nie duplikatem.

DOMENA / PRZECIWDZIEDZINA / DEFINICJA (Aksjomat G5, skrót -- pełny
tekst w Axioms_G_TIMDR_Geometry.md):
  - Domena: zamknięta krzywa \\(C \\subset \\mathbb{R}^3\\) z N>=3
    wyróżnionymi węzłami sprzężenia \\(p_0,...,p_{N-1}\\) rozłożonymi
    cyklicznie wzdłuż \\(C\\) (węzeł i sąsiaduje z węzłami
    (i-1) mod N, (i+1) mod N), każdy niosący lokalną krzywiznę
    \\(\\kappa_i\\) krzywej w tym punkcie, każdy SEGMENT łączący węzeł i
    z węzłem (i+1) mod N niosący torsję \\(\\tau_i\\) tego segmentu.
  - Przeciwdziedzina: widmo rezonansowe -- zbiór częstości własnych
    \\(\\{\\omega_k\\}\\), ich dobroci \\(\\{Q_k\\}\\) i profilu
    amplitudy odpowiedzi \\(A(\\omega)\\) w funkcji częstości pobudzenia.
  - Definicja: układ N tłumionych oscylatorów harmonicznych sprzężonych
    w pierścień (macierze M/K/Gamma zbudowane z kappa/tau -- patrz
    `build_ring_matrices`), pobudzany lokalnie (jeden węzeł),
    \\(M x'' + \\Gamma x' + Kx = F(t)\\); odpowiedź ustalona
    \\(X(\\omega) = (K-\\omega^2 M + i\\omega\\Gamma)^{-1}F\\)
    (`steady_state_response`); widmo = piki \\(|X(\\omega)|\\)
    (`find_peaks`) z ich dobrocią (`estimate_Q`).
  - Warunek stabilności (Aksjomat G5d): brak destrukcyjnego
    (nieograniczonego) wzrostu odpowiedzi dla ŻADNEGO skończonego
    pobudzenia -- formalizowane jako `is_stable()` niżej (dodatnia
    określoność M, K i dodatnia określoność Gamma na każdym węźle).

CZYM TO NIE JEST (Aksjomat G6, rozszerzone o G5): to NIE jest
rezonans modalny gałęzi K (`Axioms_K_TIMDR.md`, wyrównanie
częstotliwość/faza modułów \\((f,\\phi,A)\\) na przestrzeni
topologicznej \\(T=(X,\\tau)\\)) -- inna domena (krzywa z węzłami, nie
moduły na przestrzeni topologicznej), inny obiekt matematyczny (układ
mechaniczny drugiego rzędu, nie wyrównanie parametrów falowych), mimo
że oba używają słowa "częstość własna". Nie jest też rezonansem M ani
rezonansem sygnałowym z `core/trefoil_frenet_torsion.py` (koincydencja
progowa, operator boolowski na kanałach czasowych) -- ten operator nie
działa na szeregach czasowych w ogóle.
"""
from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

import numpy as np


def build_ring_matrices(
    n_nodes: int,
    kappa: Sequence[float],
    tau: Sequence[float],
    m: Optional[Sequence[float]] = None,
    gamma: float = 0.08,
    k_scale: float = 1.0,
    kc_scale: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Buduje macierze M, K, Gamma pierścienia `n_nodes` tłumionych,
    sprzężonych oscylatorów harmonicznych wzdłuż zamkniętej krzywej z
    N węzłami (Aksjomat G5, definicja).

    - `kappa[i]`: lokalna krzywizna krzywej w węźle i -> sztywność
      WŁASNA węzła i, `k_onsite[i] = k_scale * kappa[i]`.
    - `tau[i]`: torsja SEGMENTU łączącego węzeł i z węzłem
      `(i+1) % n_nodes` -> sprzężenie osiowe tego segmentu,
      `kc[i] = kc_scale * |tau[i]|` (wartość bezwzględna -- znak torsji
      nie zmienia siły sprzężenia w tym modelu, tylko jej geometryczny
      kierunek, który tu nie jest reprezentowany).
    - `m`: masy węzłów (domyślnie 1.0 dla każdego -- wybór modelowy,
      niezwiązany z żadnym geometrycznym parametrem, tak jak w
      pierwotnym prototypie trójwęzła).
    - `k_scale`/`kc_scale`: przejście geometria -> mechanika (jednostki
      umowne -- patrz "uczciwe ograniczenie" w
      `docs/geometry/TIMDR_GResonance_Operator.md`: te stałe NIE są
      skalibrowane na realnych danych).

    `kappa` i `tau` muszą mieć długość `n_nodes` (jedna wartość
    krzywizny na węzeł, jedna wartość torsji na segment -- w pierścieniu
    liczba segmentów = liczba węzłów).

    Wymaga `n_nodes >= 3`: przy N=2 "pierścień" degeneruje się do DWÓCH
    równoległych sprzężeń między tą samą parą węzłów (segment 0->1 i
    segment 1->0 to fizycznie różne odcinki krzywej, ale jako sprężyny
    między tymi samymi dwoma masami są nierozróżnialne) -- to nie jest
    błąd matematyczny, ale na tyle zwyrodniały/mylący przypadek
    (podwójne, nieodróżnialne sprzężenie), że jest tu jawnie wykluczony,
    zamiast po cichu zwracać poprawną, ale mylącą macierz.
    """
    if n_nodes < 3:
        raise ValueError(
            "build_ring_matrices wymaga n_nodes >= 3 - pierścień o N=2 ma dwa "
            "nierozróżnialne sprzężenia między tą samą parą węzłów (patrz docstring)"
        )
    kappa_arr = np.asarray(kappa, dtype=float)
    tau_arr = np.asarray(tau, dtype=float)
    if len(kappa_arr) != n_nodes or len(tau_arr) != n_nodes:
        raise ValueError(
            f"kappa i tau musza miec dlugosc n_nodes={n_nodes} "
            f"(dostano {len(kappa_arr)}, {len(tau_arr)})"
        )

    m_arr = np.full(n_nodes, 1.0) if m is None else np.asarray(m, dtype=float)
    if len(m_arr) != n_nodes:
        raise ValueError(f"m musi miec dlugosc n_nodes={n_nodes} (dostano {len(m_arr)})")

    k_onsite = k_scale * kappa_arr
    kc = kc_scale * np.abs(tau_arr)

    K = np.diag(k_onsite)
    for i in range(n_nodes):
        j = (i + 1) % n_nodes
        K[i, i] += kc[i]
        K[j, j] += kc[i]
        K[i, j] -= kc[i]
        K[j, i] -= kc[i]

    M = np.diag(m_arr)
    Gamma = np.diag(np.full(n_nodes, gamma))
    return M, K, Gamma


def natural_frequencies(M: np.ndarray, K: np.ndarray) -> np.ndarray:
    """Częstości własne nietłumionego układu (posortowane rosnąco),
    z uogólnionego problemu własnego K v = omega^2 M v. N-niezależne
    (działa dla dowolnego wymiaru macierzy)."""
    w2 = np.linalg.eigvalsh(np.linalg.inv(M) @ K)
    w2 = np.clip(w2, 0, None)
    return np.sqrt(np.sort(w2))


def steady_state_response(
    M: np.ndarray, K: np.ndarray, Gamma: np.ndarray,
    F_vec: np.ndarray, omegas: np.ndarray,
) -> np.ndarray:
    """Odpowiedź ustalona (phasor, liniowy układ pobudzany
    harmonicznie): X(omega) = (K - omega^2*M + i*omega*Gamma)^-1 * F.
    Zwraca zespoloną macierz (len(omegas), N)."""
    n = M.shape[0]
    X = np.zeros((len(omegas), n), dtype=complex)
    for idx, w in enumerate(omegas):
        A = K - (w ** 2) * M + 1j * w * Gamma
        X[idx] = np.linalg.solve(A, F_vec)
    return X


def find_peaks(amp_column: np.ndarray, omegas: np.ndarray, min_frac: float = 0.2) -> List[int]:
    """Lokalne maksima w kolumnie amplitudy, powyżej min_frac*max --
    proste wykrywanie pików rezonansowych (nie FFT, działa na gęstym
    skanie omega)."""
    idxs = []
    for i in range(1, len(omegas) - 1):
        if (amp_column[i] > amp_column[i - 1] and amp_column[i] > amp_column[i + 1]
                and amp_column[i] > min_frac * amp_column.max()):
            idxs.append(i)
    return idxs


def estimate_Q(amp_column: np.ndarray, omegas: np.ndarray, idx_peak: int) -> float:
    """Przybliżone Q (ostrość piku) metodą połowy mocy (FWHM):
    Q = omega_peak / szerokość_pasma_3dB."""
    peak_val = amp_column[idx_peak]
    half = peak_val / np.sqrt(2)
    left = idx_peak
    while left > 0 and amp_column[left] > half:
        left -= 1
    right = idx_peak
    while right < len(omegas) - 1 and amp_column[right] > half:
        right += 1
    bw = omegas[right] - omegas[left]
    return omegas[idx_peak] / bw if bw > 0 else float("inf")


def default_omega_sweep(M: np.ndarray, K: np.ndarray, n: int = 8000, span: float = 1.8) -> np.ndarray:
    """Skan częstości obejmujący częstości własne układu bazowego."""
    w_nat = natural_frequencies(M, K)
    return np.linspace(0.01, w_nat[-1] * span, n)


def is_stable(M: np.ndarray, K: np.ndarray, Gamma: np.ndarray, tol: float = 1e-9) -> bool:
    """Warunek stabilności operatora G-Rezonans (Aksjomat G5d):
    formalny, sprawdzalny predykat zastępujący nieformalne "Q nie
    eksploduje".

    Gdy (a) M jest symetryczna ściśle dodatnio określona (fizyczne
    masy > 0), (b) K jest symetryczna ściśle dodatnio określona
    (sztywności > 0 na każdym węźle -- silniejsze niż tylko
    półokreśloność, bo wymagamy braku trybu zerowej częstości), (c)
    Gamma jest symetryczna ściśle dodatnio określona (tłumienie > 0 na
    KAŻDYM węźle) -- to macierz układu
    \\(A(\\omega) = K - \\omega^2 M + i\\omega\\Gamma\\) jest
    nieosobliwa dla KAŻDEGO rzeczywistego omega: przy omega=0,
    A=K (nieosobliwa z (b)); przy omega!=0, część urojona
    omega*Gamma jest ściśle dodatnio określona, więc A nie może mieć
    zerowej wartości własnej (macierz hermitowska z niezerową częścią
    urojoną na przekątnej dodatniej nie może być osobliwa). Brak
    zer na rzeczywistej osi omega w mianowniku odpowiedzi ustalonej
    oznacza SKOŃCZONĄ odpowiedź dla każdej skończonej częstości
    pobudzenia -- formalny odpowiednik "braku destrukcyjnego wzrostu Q"
    z opisu operatora.

    Zwraca True/False, nie rzuca wyjątku -- pomyślane jako diagnostyka
    do wywołania PRZED `steady_state_response()` na nieznanym układzie
    (np. po defekcie, który mógł popsuć dodatnią określoność K, jeśli
    zmiana sztywności węzła jest wystarczająco ujemna)."""

    def _is_strictly_pd(mat: np.ndarray) -> bool:
        if mat.shape[0] != mat.shape[1]:
            return False
        if not np.allclose(mat, mat.T, atol=tol):
            return False
        eigvals = np.linalg.eigvalsh(mat)
        return bool(np.all(eigvals > tol))

    return _is_strictly_pd(M) and _is_strictly_pd(K) and _is_strictly_pd(Gamma)
