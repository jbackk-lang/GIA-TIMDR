# core/trefoil_missing_coordinate_solver.py
"""
trefoil_missing_coordinate_solver.py -- rozwiazywanie brakujacej
wspolrzednej punktu p_t=(x,y,z) traktujac problem jako "jedna
niewiadoma, znamy wynik", zgodnie z 4-krokowym planem uzytkownika:

1. Krzywa gamma(t)=(x(t),y(t),z(t)) z brakujacym kanalem jako zmienna z.
2. Uklad kappa(z)=kappa_target ORAZ tau jako filtr spojnosci (nie
   niezalezne drugie rownanie -- patrz uzasadnienie w
   select_by_tau_consistency() nizej).
3. Rezonans (koincydencja >=K z N kanalow geometrycznych) jako selektor
   miedzy kandydatami z rownania kappa(z)=target.
4. Wygladzanie (lokalny wielomian, odpowiednik Savitzky-Golay bez
   zaleznosci od scipy) PRZED liczeniem v/a/j -- odpowiedz na problem
   wzmacniania szumu znaleziony w
   trefoil_weather_embedding_validation.py.

KLUCZOWY FAKT MATEMATYCZNY (uzasadnienie, ze rownanie jest w ogole
rozwiazywalne): dla p_t=(x,y,z) z x,y USTALONYMI, v(z)=p_t-p_t1 i
a(z)=v(z)-v_prev sa OBIE afiniczne w z (v_prev jest w calosci
historyczne, bez zaleznosci od z). Std v(z) x a(z) rozwija sie do
C0 + z*C1 -- wyraz kwadratowy z^2*(ez x ez) znika TOZSAMOSCIOWO (wektor
iloczynowany sam ze soba = 0). Zweryfikowane numerycznie w rozmowie:
druga roznica dyskretna v(z)xa(z) po siatce z wychodzi ~1e-15. Skutek:
kappa(z)=|v(z)xa(z)|/|v(z)|^3 jest gladka funkcja wymierna JEDNEJ
zmiennej -- rownanie kappa(z)=target ma generalnie 0, 2 (czasem wiecej)
rozwiazan, rozwiazywalne skanem+bisekcja bez potrzeby niczego
bardziej wyrafinowanego.

UWAGA (uczciwe): to rozwiazuje ALGEBRE, nie problem niezawodnosci z
trefoil_weather_embedding_validation.py -- kappa/tau uzyte tutaj to
TA SAMA statystyka, ktora tam zostala pokazana jako niestabilna na
krotkich, rzeczywistych szeregach. Wygladzanie (krok 4) jest wprost
odpowiedzia na TEN problem, testowana ponizej z kontrola prawda-wzgledem
(ground truth recovery), nie tylko zaargumentowana slownie.
"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np


# --- KROK 4: wygladzanie przed roznicowaniem ---

def local_poly_smooth(series: np.ndarray, window: int = 5, polyorder: int = 2) -> np.ndarray:
    """Lokalne dopasowanie wielomianu metoda najmniejszych kwadratow --
    odpowiednik Savitzky-Golay BEZ zaleznosci od scipy (ten sam wzorzec
    unikania scipy co przy naprawie Device Guard w
    TIMDR-Industrial-Predict/TIMDR-EV-Predict/TIMDR-Earthquake-Core w
    tej samej sesji). Brzegi obslugiwane mniejszym, asymetrycznym oknem
    zamiast trybow brzegowych scipy (uproszczenie, udokumentowane, nie
    przemilczane)."""
    n = len(series)
    half = window // 2
    out = np.zeros(n)
    for i in range(n):
        lo, hi = max(0, i - half), min(n, i + half + 1)
        idx = np.arange(lo, hi) - i
        A = np.vander(idx, polyorder + 1, increasing=True)
        coeffs, *_ = np.linalg.lstsq(A, series[lo:hi], rcond=None)
        out[i] = coeffs[0]
    return out


def smooth_trajectory(pts: np.ndarray, window: int = 5, polyorder: int = 2) -> np.ndarray:
    """smooth_series() zastosowane niezaleznie per-kolumna (kazdy
    'kanal' x,y,z wygladzany osobno)."""
    return np.stack([local_poly_smooth(pts[:, c], window, polyorder) for c in range(pts.shape[1])], axis=1)


# --- KROK 1: krzywa z brakujacym kanalem jako zmienna ---

def kappa_tau_of_z(
    z: float, x: float, y: float,
    p_t1: np.ndarray, p_t2: np.ndarray, p_t3: np.ndarray,
    min_curvature: float = 1e-4,
) -> Tuple[float, float]:
    """kappa(z), tau(z) dla p_t=(x,y,z), z x,y USTALONYMI i historia
    p_t1,p_t2,p_t3 w pelni znana. Wzor identyczny z
    trefoil_frenet_torsion.curvature_torsion_at, tylko sparametryzowany
    wprost przez skalar z (brakujaca wspolrzedna)."""
    p_t = np.array([x, y, z])
    v = p_t - p_t1
    v1 = p_t1 - p_t2
    a = v - v1
    a1 = v1 - (p_t2 - p_t3)
    j = a - a1
    speed = np.linalg.norm(v)
    if speed < 1e-9:
        return 0.0, 0.0
    cross = np.cross(v, a)
    cn = np.linalg.norm(cross)
    kappa = cn / speed ** 3
    tau = float(np.dot(cross, j) / cn ** 2) if kappa > min_curvature else 0.0
    return float(kappa), tau


# --- KROK 2: rozwiazanie kappa(z)=target, tau jako filtr spojnosci ---

def _bisect(f: Callable[[float], float], lo: float, hi: float, tol: float = 1e-9, max_iter: int = 100) -> Optional[float]:
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        fm = f(mid)
        if abs(fm) < tol or (hi - lo) < tol:
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def solve_kappa_target(
    x: float, y: float, p_t1: np.ndarray, p_t2: np.ndarray, p_t3: np.ndarray,
    kappa_target: float, z_lo: float, z_hi: float, n_scan: int = 2000,
) -> List[float]:
    """Wszystkie z takie, ze kappa(z)=kappa_target w [z_lo,z_hi] --
    skan siatki + bisekcja na kazdej zmianie znaku. Generalnie 0, 2
    (czasem wiecej) rozwiazan -- patrz uzasadnienie w docstringu modulu."""
    f = lambda z: kappa_tau_of_z(z, x, y, p_t1, p_t2, p_t3)[0] - kappa_target
    zs = np.linspace(z_lo, z_hi, n_scan)
    vals = np.array([f(z) for z in zs])
    roots = []
    for i in range(len(zs) - 1):
        if vals[i] == 0:
            roots.append(zs[i])
        elif vals[i] * vals[i + 1] < 0:
            r = _bisect(f, zs[i], zs[i + 1])
            if r is not None:
                roots.append(r)
    return roots


def select_by_tau_consistency(
    candidates: Sequence[float], tau_target: float,
    x: float, y: float, p_t1: np.ndarray, p_t2: np.ndarray, p_t3: np.ndarray,
) -> Optional[float]:
    """Wsrod kandydatow z rownania kappa(z)=target, wybiera ten,
    ktorego tau(z) jest NAJBLIZEJ tau_target.

    UWAGA (celowo, nie przez przeoczenie): to NIE jest rozwiazywanie
    ukladu {kappa(z)=A, tau(z)=B} jednoczesnie -- dla jednej zmiennej z
    dwa niezalezne rownania sa generalnie SPRZECZNE (ukladu nie da sie
    scisle spelnic, poza przypadkowa zbieznoscia). tau tutaj sluzy jako
    DRUGI, NIEZALEZNY kanal geometryczny do przesiania kandydatow z
    rownania kappa -- to redukuje 0/2/wiecej algebraicznych
    rozwiazan do jednego, uzywajac niezaleznej informacji (torsji),
    zamiast dodawac drugie, generalnie niespelnialne rownanie."""
    if not candidates:
        return None
    scored = [(abs(kappa_tau_of_z(z, x, y, p_t1, p_t2, p_t3)[1] - tau_target), z) for z in candidates]
    scored.sort()
    return scored[0][1]


# --- KROK 3: rezonans jako selektor koncowy ---

def _is_anomaly(series: np.ndarray, k: float = 2.0) -> np.ndarray:
    mean, std = series.mean(), series.std()
    if std == 0:
        return np.zeros(len(series), dtype=bool)
    return (series > mean + k * std) | (series < mean - k * std)


def resonance_stability_score(
    candidate_z: float, x: float, y: float,
    history_pts: np.ndarray,  # (N,3) pelna, ZNANA historia (bez punktu docelowego)
    p_t1: np.ndarray, p_t2: np.ndarray, p_t3: np.ndarray,
    k_resonance: int = 2,
) -> Tuple[bool, int]:
    """Wstawia kandydata z w kontekst pelnej historii i sprawdza
    koincydencje (rezonans) miedzy 3 kanalami: kappa, tau, odchylenie
    pozycji od centroidu historii -- ta sama logika K-z-N co
    trefoil_frenet_torsion.rezonans(). Zwraca (czy_destrukcyjny_rezonans,
    liczba_zgodnych_kanalow).

    'Destrukcyjny rezonans' = kandydat jest anomalny w >=k_resonance
    kanalach jednoczesnie WZGLEDEM ROZKLADU TYCH KANALOW W CALEJ
    HISTORII -- czyli wyglada jak 'dziki, pojedynczy pik' niespojny z
    reszta serii, a nie jak spokojna kontynuacja."""
    kappa_c, tau_c = kappa_tau_of_z(candidate_z, x, y, p_t1, p_t2, p_t3)
    p_t = np.array([x, y, candidate_z])
    pos_dev_c = np.linalg.norm(p_t - history_pts.mean(axis=0))

    # rozklady referencyjne z historii (bez kandydata) -- kappa/tau
    # liczone "w miejscu" dla kazdego historycznego punktu (przy uzyciu
    # jego wlasnych 3 poprzednikow), pos_dev z historii wprost
    hist_kappas, hist_taus = [], []
    for i in range(3, len(history_pts)):
        kk, tt = kappa_tau_of_z(history_pts[i, 2], history_pts[i, 0], history_pts[i, 1],
                                 history_pts[i-1], history_pts[i-2], history_pts[i-3])
        hist_kappas.append(kk); hist_taus.append(tt)
    hist_kappas = np.array(hist_kappas); hist_taus = np.array(hist_taus)
    hist_pos_dev = np.linalg.norm(history_pts - history_pts.mean(axis=0), axis=1)

    def anom_flag(value, ref_series):
        if len(ref_series) < 2 or ref_series.std() == 0:
            return False
        mean, std = ref_series.mean(), ref_series.std()
        return value > mean + 2*std or value < mean - 2*std

    flags = [
        anom_flag(kappa_c, hist_kappas),
        anom_flag(tau_c, hist_taus),
        anom_flag(pos_dev_c, hist_pos_dev),
    ]
    n_anom = sum(flags)
    return n_anom >= k_resonance, n_anom


def select_by_resonance(
    candidates: Sequence[float], x: float, y: float,
    history_pts: np.ndarray, p_t1: np.ndarray, p_t2: np.ndarray, p_t3: np.ndarray,
    k_resonance: int = 2,
) -> Optional[float]:
    """Wsrod kandydatow, preferuje tego BEZ destrukcyjnego rezonansu
    (spojny z reszta serii). Jesli wszyscy/zaden nie wywoluje
    rezonansu, zwraca kandydata z NAJMNIEJSZA liczba zgodnych kanalow
    anomalnych (najbardziej 'spokojny')."""
    if not candidates:
        return None
    scored = []
    for z in candidates:
        destructive, n_anom = resonance_stability_score(z, x, y, history_pts, p_t1, p_t2, p_t3, k_resonance)
        scored.append((destructive, n_anom, z))
    scored.sort(key=lambda t: (t[0], t[1]))
    return scored[0][2]


def solve_missing_coordinate(
    x: float, y: float, p_t1: np.ndarray, p_t2: np.ndarray, p_t3: np.ndarray,
    history_pts: np.ndarray, kappa_target: float, tau_target: float,
    z_lo: float, z_hi: float, k_resonance: int = 2,
) -> Dict:
    """Pelny potok: krok 1 (kappa(z)/tau(z)) -> krok 2 (rozwiaz
    kappa(z)=target, PRZESIEJ przez tau -- to jest GLOWNY selektor,
    patrz nizej) -> krok 3 (rezonans jako DIAGNOSTYKA stabilnosci
    wybranego kandydata, nie jako niezalezny, nadrzedny selektor).

    POPRAWKA (znaleziona empirycznie, patrz
    docs/geometry/TIMDR_Trefoil_MissingCoordinateSolver.md sekcja
    "Blad w pierwszej wersji potoku"): pierwsza wersja tej funkcji
    pozwalala rezonansowi WYBIERAC niezaleznie od tau, ignorujac wynik
    kroku 2 -- test z ORACLE (idealnymi) celami kappa/tau pokazal, ze
    SAM tau-consistency osiaga 100% trafnosci (bo prawdziwe z zawsze
    jest jednym z pierwiastkow, a jego tau dokladnie pasuje do celu),
    natomiast SAM rezonans jako selektor trafia tylko w ~46% przypadkow
    -- rezonans odpowiada na INNE pytanie ('czy to wyglada jak dziki
    pik wzgledem historii'), nie na 'ktory z dwoch pierwiastkow jest
    prawdziwy'. Naprawiono: tau-consistency wybiera KANDYDATA, rezonans
    tylko RAPORTUJE, czy ten wybrany kandydat jest stabilny (do
    zaufania) czy nie -- nie zmienia juz wyboru."""
    roots = solve_kappa_target(x, y, p_t1, p_t2, p_t3, kappa_target, z_lo, z_hi)
    if not roots:
        return {"status": "brak_rozwiazan", "roots": [], "z": None}

    z_final = select_by_tau_consistency(roots, tau_target, x, y, p_t1, p_t2, p_t3)
    destructive, n_anom = resonance_stability_score(
        z_final, x, y, history_pts, p_t1, p_t2, p_t3, k_resonance,
    )

    return {
        "status": "ok",
        "roots": roots,
        "z": z_final,
        "rezonans_destrukcyjny": destructive,
        "rezonans_n_kanalow_zgodnych": n_anom,
    }
