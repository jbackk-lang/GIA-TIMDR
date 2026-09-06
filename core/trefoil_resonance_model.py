# core/trefoil_resonance_model.py
"""
trefoil_resonance_model.py -- model dynamicznego (mechanicznego)
rezonansu trojwezla helikalnego: uklad wezlow sprzezonych przez os,
pobudzenie, odpowiedz, kryterium rewizji.

KONTEKST: uzytkownik doprecyzowal pytanie o "rezonans" z
TIMDR_Trefoil_FrenetTorsion.md, wskazujac ze samo slowo "rezonans" nic
nie znaczy bez odpowiedzi na trzy pytania: (1) co jest ukladem
rezonujacym, (2) co jest pobudzeniem, (3) co jest mierzone. Ten modul
odpowiada na wszystkie trzy explicite, jako osobny, jawnie nazwany
obiekt -- patrz docs/geometry/TIMDR_Trefoil_ResonanceModel.md dla
pelnego opisu 7-krokowego protokolu i wynikow.

WAZNE ROZROZNIENIE: to jest CZWARTE znaczenie slowa "rezonans" w tym
ekosystemie (obok: modalnego, sygnalowego M, kierunkowego -- patrz
docs/GLOSSARY_EN_PL.md sekcja "Rezonans / Resonance"). W przeciwienstwie
do rezonansu sygnalowego (licznik koincydencji, operator boolowski),
TO JEST prawdziwy fizyczny/mechaniczny rezonans -- uklad drgajacy z
czestosciami wlasnymi, wzmacniajacy odpowiedz przy dopasowaniu
czestosci pobudzenia. Nie nalezy mylic z "rezonansem" uzytym w
core/trefoil_frenet_torsion.py (tamten to rezonans SYGNALOWY --
koincydencja >=K z N kanalow anomalnych geometrycznie, ta sama logika
co rezonans-M w synoptyku). Oba dotycza tej samej figury (trojwezel),
ale sa DWOMA ROZNYMI obiektami matematycznymi wspoldzielacymi nazwe --
dokladnie ten sam wzorzec "jedno slowo, rozne obiekty", ktory ten
ekosystem juz stosuje do "skretu".

MODEL (Wariant C z propozycji uzytkownika: os helisy jako "falowod"
sprzegajacy wezly, wezly jako punkty/masy sprzezenia -- wybrany, bo
wprost odpowiada oryginalnej hipotezie "os wzdluz figury reprezentuje
skret": os NIESIE cos (sprzezenie), wezly sa punktami zaczepienia):

Pierscien 3 tlumionych oscylatorow harmonicznych (wezly 1-2-3-1),
sprzezonych przez segmenty osi:

    M x'' + Gamma x' + K x = F(t)

gdzie:
    M = diag(m1,m2,m3)          -- masy wezlow (domyslnie rowne)
    K = macierz sztywnosci       -- sztywnosc wlasna wezla (~kappa) NA
                                    PRZEKATNEJ + sprzezenie osiowe
                                    (~|tau|) miedzy sasiadujacymi
                                    wezlami w pierscieniu
    Gamma = diag(gamma,...)      -- tlumienie (jednakowe)
    F(t) = F0 * cos(omega*t)     -- pobudzenie harmoniczne, domyslnie
                                    lokalne (tylko wezel 1)

Parametry k0 (sztywnosc wezla) i kc0 (sprzezenie osiowe) sa fizycznie
zakotwiczone w geometrii idealnego trojwezla z
core/trefoil_frenet_torsion.py: k0 ~ kappa (krzywizna w wezle), kc0 ~
|tau| (torsja na osi) -- NIE dowolne stale.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

# --- parametry geometryczne bazowe (z core.trefoil_frenet_torsion,
#     idealny trojwezel: kappa=0.2062, tau=0.3509 identycznie we
#     wszystkich 3 wezlach -- potwierdzona symetria 3-krotna) ---
KAPPA_IDEAL = 0.2062
TAU_IDEAL = 0.3509

# Skalowanie geometria -> mechanika. Wybor modelowy, NIE skalibrowany
# na realnych danych (analogicznie do min_curvature w
# the_geo_pro_4d.py) -- punkt startowy do dalszej kalibracji.
K_SCALE = 5.0
KC_SCALE = 5.0
M0_DEFAULT = 1.0
GAMMA_DEFAULT = 0.08

K0 = K_SCALE * KAPPA_IDEAL
KC0 = KC_SCALE * abs(TAU_IDEAL)


def build_matrices(
    defect_r1: float = 0.0,
    defect_tau1: float = 0.0,
    k0: float = K0,
    kc0: float = KC0,
    m0: float = M0_DEFAULT,
    gamma: float = GAMMA_DEFAULT,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Buduje macierze M, K, Gamma pierscienia 3 sprzezonych oscylatorow
    z defektem D1(delta_r1, delta_tau1) na wezle 1 (indeks 0).

    - defect_r1: zmiana lokalnej sztywnosci wezla 1 (model: promien
      wezla Δr1 -> k1 = k0*(1+defect_r1)). Znak/skala to wybor
      modelowy -- rosnacy promien traktowany tu jako rosnaca sztywnosc,
      nie odwrotnie; nie zwalidowane na realnej geometrii.
    - defect_tau1: zmiana sprzezenia osiowego NA OBU segmentach osi
      stykajacych sie z wezlem 1 (segmenty 3-1 i 1-2), model: Δτ1 ->
      kc_(3,1) = kc_(1,2) = kc0*(1+defect_tau1). Segment 2-3
      (niedotkniety wezel) pozostaje kc0.

    UWAGA (uczciwe ograniczenie): przesuniecie wezla wzdluz osi (Δz1 z
    oryginalnej propozycji D1(Δz1,Δr1,Δτ1)) NIE jest reprezentowane w
    tym modelu -- zmienia tylko polozenie rownowagi ukladu, nie macierze
    M/K/Gamma, wiec nie wplywa na widmo rezonansowe liczone tutaj. To
    jest odnotowane, nie przemilczane -- patrz
    docs/geometry/TIMDR_Trefoil_ResonanceModel.md sekcja "Co NIE zostalo
    zrobione".
    """
    m = np.array([m0, m0, m0])
    k_onsite = np.array([k0 * (1 + defect_r1), k0, k0])
    kc = {
        (0, 1): kc0 * (1 + defect_tau1),
        (1, 2): kc0,
        (2, 0): kc0 * (1 + defect_tau1),
    }
    K = np.diag(k_onsite)
    for (i, j), val in kc.items():
        K[i, i] += val
        K[j, j] += val
        K[i, j] -= val
        K[j, i] -= val
    M = np.diag(m)
    Gamma = np.diag([gamma] * 3)
    return M, K, Gamma


def natural_frequencies(M: np.ndarray, K: np.ndarray) -> np.ndarray:
    """Czestosci wlasne nietlumionego ukladu (posortowane rosnaco),
    z uogolnionego problemu wlasnego K v = omega^2 M v."""
    w2 = np.linalg.eigvalsh(np.linalg.inv(M) @ K)
    w2 = np.clip(w2, 0, None)
    return np.sqrt(np.sort(w2))


def steady_state_response(
    M: np.ndarray, K: np.ndarray, Gamma: np.ndarray,
    F_vec: np.ndarray, omegas: np.ndarray,
) -> np.ndarray:
    """Odpowiedz ustalona (phasor, liniowy uklad pobudzany
    harmonicznie): X(omega) = (K - omega^2*M + i*omega*Gamma)^-1 * F.
    Zwraca zespolona macierz (len(omegas), 3)."""
    X = np.zeros((len(omegas), 3), dtype=complex)
    for idx, w in enumerate(omegas):
        A = K - (w ** 2) * M + 1j * w * Gamma
        X[idx] = np.linalg.solve(A, F_vec)
    return X


def find_peaks(amp_column: np.ndarray, omegas: np.ndarray, min_frac: float = 0.2) -> List[int]:
    """Lokalne maksima w kolumnie amplitudy, powyzej min_frac*max --
    proste wykrywanie pikow rezonansowych (nie FFT, dziala na gestym
    skanie omega)."""
    idxs = []
    for i in range(1, len(omegas) - 1):
        if (amp_column[i] > amp_column[i - 1] and amp_column[i] > amp_column[i + 1]
                and amp_column[i] > min_frac * amp_column.max()):
            idxs.append(i)
    return idxs


def estimate_Q(amp_column: np.ndarray, omegas: np.ndarray, idx_peak: int) -> float:
    """Przyblizone Q (ostrosc piku) metoda polowy mocy (FWHM):
    Q = omega_peak / szerokosc_pasma_3dB."""
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
    """Skan czestosci obejmujacy czestosci wlasne ukladu bazowego."""
    w_nat = natural_frequencies(M, K)
    return np.linspace(0.01, w_nat[-1] * span, n)
