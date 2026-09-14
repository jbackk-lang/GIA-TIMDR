"""
timdr_formalism/gs_matrix.py

GS-Matrix (sprzezenie geometria<->sygnal, gałęzie G i S) -- poprawiona
wersja po audycie znalezionym w tej rozmowie (patrz historia commitow /
konwersacja): pierwotna propozycja twierdzila "K hermitowskie (K=K†)
<=> brak strat energii/informacji" dla ukladu

    dV/dt = K V,   V = [G, S]^T

To bylo bledne dla rzeczywistej macierzy K: jesli K jest symetryczna
(rzeczywisty przypadek hermitowskosci), jej wartosci wlasne sa
RZECZYWISTE, wiec rozwiazanie V(t) = exp(Kt) V(0) rosnie lub zanika
WYKLADNICZO wzdluz kierunkow wlasnych (chyba ze wartosc wlasna = 0) --
to jest DOKLADNA ODWROTNOSC zachowania normy. Macierz, ktora faktycznie
zachowuje norme ||V(t)|| (czysty obrot w przestrzeni stanow) musi byc
ANTYSYMETRYCZNA: K^T = -K (dokladnie jak podana w oryginalnej propozycji
struktura symplektyczna J=[[0,1],[-1,0]] dla czlonu sprzegajacego -- ale
ta obserwacja stala w sprzecznosci z rownoczesnym zadaniem K=K†, bo
K_21=-K_12 (antysymetria) i K_21=K_12 (hermitowskosc/symetria dla
macierzy rzeczywistej) nie moga zachodzic jednoczesnie przy alpha!=0).

POPRAWKA: rozdziel K na dwie czesci (kazda macierz rzeczywista ma
jednoznaczny taki rozklad):

    K = K_anti + K_sym
    K_anti = (K - K^T) / 2   (antysymetryczna -- zachowawcza, obrot)
    K_sym  = (K + K^T) / 2   (symetryczna -- tlumienie/wzmocnienie)

PRE-REJESTRACJA (przed uruchomieniem testow ponizej):
  Kontrola pozytywna (zachowawcza): czysto antysymetryczne K (np.
    [[0, a], [-a, 0]] dla dowolnego a) -> ||V(t)|| powinno pozostac
    STALE (w granicach bledu numerycznego calkowania) dla dowolnego
    V(0) != 0 i dowolnego horyzontu czasowego -- bo exp(K_anti*t) jest
    macierza ortogonalna (obrot) dla kazdego t.
  Kontrola negatywna (nie-zachowawcza): czysto symetryczne K z
    dodatnia wartoscia wlasna -> ||V(t)|| powinno ROSNAC monotonicznie
    (a nie pozostawac stale) dla V(0) w kierunku tej wartosci wlasnej.
    Analogicznie: ujemna wartosc wlasna -> ||V(t)|| powinno MALEC.
  Test integracji numerycznej: RK4 z krokiem dt malym wzgledem skali
    czasowej ukladu (tu: dt<=0.001 dla typowych |K|~O(1)) -- bledy
    dyskretyzacji RK4 sa O(dt^4) na krok, wiec przy tej skali blad
    skumulowany w normie powinien byc rzedu <1e-3 na horyzoncie t~10,
    nie wiecej.

To repo mial juz raz problem z Windows Device Guard blokujacym scipy
(patrz calibration.py) -- ten modul jest CELOWO numpy-only (wlasna
implementacja RK4, bez scipy.integrate), zeby nie wprowadzic tego
samego ryzyka trzeci raz.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class KDecomposition:
    K_anti: np.ndarray  # antysymetryczna czesc (zachowawcza, obrot)
    K_sym: np.ndarray  # symetryczna czesc (tlumienie/wzmocnienie)


def decompose_K(K: np.ndarray) -> KDecomposition:
    """Rozklad K = K_anti + K_sym, jednoznaczny dla kazdej macierzy
    kwadratowej rzeczywistej. K_anti^T = -K_anti (antysymetryczna,
    generuje obrot -- zachowawcza czesc sprzezenia G<->S). K_sym^T =
    K_sym (symetryczna, generuje wzrost/zanik wzdluz wlasnych kierunkow
    -- czesc tlumiaca/wzmacniajaca, NIE zachowawcza)."""
    K = np.asarray(K, dtype=float)
    if K.shape[0] != K.shape[1]:
        raise ValueError(f"K musi byc kwadratowa, dostano ksztalt {K.shape}")
    K_anti = (K - K.T) / 2.0
    K_sym = (K + K.T) / 2.0
    return KDecomposition(K_anti=K_anti, K_sym=K_sym)


def is_conservative(K: np.ndarray, tol: float = 1e-9) -> bool:
    """Poprawny warunek zachowawczosci dla rzeczywistego dV/dt=KV:
    K^T = -K (antysymetryczna), NIE K=K† (hermitowskosc/symetria) --
    patrz naglowek modulu dla pelnego uzasadnienia bledu w oryginalnej
    propozycji."""
    K = np.asarray(K, dtype=float)
    return bool(np.allclose(K.T, -K, atol=tol))


def simulate_linear_system(
    K: np.ndarray, V0: np.ndarray, dt: float, n_steps: int
) -> np.ndarray:
    """Calkuje dV/dt = K V metoda RK4 (bez scipy -- patrz naglowek
    modulu). Zwraca tablice (n_steps+1, dim) z V(t) dla t=0,dt,2dt,...

    RK4 dla ukladu liniowego stalego K:
      k1 = K @ V
      k2 = K @ (V + dt/2 * k1)
      k3 = K @ (V + dt/2 * k2)
      k4 = K @ (V + dt * k3)
      V_next = V + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    """
    K = np.asarray(K, dtype=float)
    V = np.asarray(V0, dtype=float).copy()
    if K.shape[0] != K.shape[1] or K.shape[0] != V.shape[0]:
        raise ValueError(
            f"niezgodne wymiary: K {K.shape}, V0 {V.shape}"
        )
    if dt <= 0:
        raise ValueError(f"dt musi byc > 0, dostano {dt}")
    if n_steps < 0:
        raise ValueError(f"n_steps musi byc >= 0, dostano {n_steps}")

    trajectory = np.zeros((n_steps + 1, len(V)))
    trajectory[0] = V
    for i in range(n_steps):
        k1 = K @ V
        k2 = K @ (V + dt / 2 * k1)
        k3 = K @ (V + dt / 2 * k2)
        k4 = K @ (V + dt * k3)
        V = V + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        trajectory[i + 1] = V
    return trajectory
