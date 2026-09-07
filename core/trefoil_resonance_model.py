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

NAPRAWIONE/PODNIESIONE (na wyrazna prosbe uzytkownika, w tej samej
sesji): ten modul byl PIERWOTNIE samodzielna implementacja (pierscien
zakodowany na sztywno jako N=3). Podniesiony teraz do Aksjomatu G5
(`docs/theory/Axioms_G_TIMDR_Geometry.md`) jako pelnoprawny operator
gałęzi G -- OGÓLNA implementacja (dowolne N>=3) zyje teraz w
`core/geometric_resonance_operator.py`, a ten modul jest CIENKA
WARSTWA nad nia (N=3, stale geometryczne idealnego trojwezla),
zachowana dla wstecznej kompatybilnosci z istniejacymi testami/
dokumentacja -- `build_matrices()` ponizej daje BAJT-W-BAJT identyczny
wynik jak przed ta zmiana (patrz test regresyjny w
tests/test_geometric_resonance_operator.py:
test_trefoil_build_matrices_matches_general_operator).
"""
from __future__ import annotations

from typing import Tuple

import numpy as np

from core.geometric_resonance_operator import (  # noqa: F401 (re-eksport dla wstecznej kompatybilnosci)
    build_ring_matrices,
    natural_frequencies,
    steady_state_response,
    find_peaks,
    estimate_Q,
    default_omega_sweep,
    is_stable,
)

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
    z defektem D1(delta_r1, delta_tau1) na wezle 1 (indeks 0). Cienka
    warstwa nad `geometric_resonance_operator.build_ring_matrices`
    (N=3, k_scale=kc_scale=1.0 -- k0/kc0 sa tu JUZ w jednostkach
    mechanicznych, nie surowa geometria, w odroznieniu od ogolnego
    operatora gdzie kappa/tau sa surowa geometria a skalowanie jest
    osobnym parametrem).

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
    kappa_arr = [k0 * (1 + defect_r1), k0, k0]
    tau_arr = [kc0 * (1 + defect_tau1), kc0, kc0 * (1 + defect_tau1)]
    return build_ring_matrices(
        3, kappa_arr, tau_arr, m=[m0, m0, m0], gamma=gamma, k_scale=1.0, kc_scale=1.0,
    )
