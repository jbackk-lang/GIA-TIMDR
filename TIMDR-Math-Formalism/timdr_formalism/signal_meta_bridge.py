"""timdr_formalism/signal_meta_bridge.py

Integracja klas sygnalu I/II/III (signal_class.py) z META-DYNAMICS
(MetaState(Λ,τ,ρ,J), _vendor_meta_state.py) - zlecona wprost przez
uzytkownika 2026-09-12, po opisaniu pelnego lancucha pipeline'u
sygnalowego:

    sygnal -> SG-Coupling -> Θ_bif -> klasa I/II/III -> MetaState -> faza systemu

Przed tym modulem `signal_class.py` (klasy I/II/III) i MetaState z
META-DYNAMICS byly DWOMA rozlacznymi, niepolaczonymi mechanizmami w
osobnych repo (patrz GIA-TIMDR/docs/theory/TIMDR_Branch_Specification.md,
sekcja "Warstwa meta") - ten plik jest PIERWSZYM rzeczywistym wiazaniem
miedzy nimi, nie tylko dokumentacja zamierzonej architektury.

WZOR ISTNIEJACY W EKOSYSTEMIE (szesc juz opisanych domen w
TIMDR_Branch_Specification.md, sekcja "Galaz META-DYNAMICS"): kazda
domena mapuje WLASNE wielkosci fizyczne na Λ/τ/ρ/J przez wlasny,
jawnie udokumentowany `meta_adapter.py` - ta galaz NIE narzuca jednego
wzoru, tylko wspolny KSZTALT (4 liczby + operator ewolucji). Ten plik
jest SIODMA taka instancja (pierwsza dla gałęzi M/S/pipeline'u
sygnalowego SG-Coupling/Θ_bif, w odroznieniu od pozostalych szesciu,
ktore sa spoza tego repo).

PRE-REJESTRACJA (spisana PRZED uruchomieniem czegokolwiek na
tests/test_sg_coupling_full_operator*.py, zgodnie z dyscyplina
anty-numerologiczna tego repo):

1. AGREGACJA: MetaState w innych domenach jest liczony per KROK CZASOWY
   przez agregacje PO PRZESTRZENI (np. po wszystkich komorkach siatki
   Quantum-Lattice). Tu nie ma przestrzeni - jest jeden skalarny sygnal
   w czasie. Analogiem "wielu elementow do zagregowania" jest wiec OKNO
   CZASOWE: sygnal dzielony jest na ROZLACZNE (partycja, nie okno
   przesuwne - ta sama zasada co P_k w protokole numerologii, zeby
   kolejne okna byly niezalezne od siebie) bloki `window_size` krokow,
   jeden MetaState per blok.

2. WZORY (kazdy z INNEJ, nietrywialnie powiazanej wielkosci zrodlowej -
   celowo, zeby kanaly NIE byly strukturalnie zagniezdzone jeden w
   drugim z definicji):

   Λ (struktura)     = std(Q_okno) / (std(Q_okno) + |mean(Q_okno)| + eps)
       Dyspersja parametru obwiedni Q wzgledem wlasnej skali w oknie -
       ten sam ksztalt wzoru co Λ_G (dyspersja krzywizny,
       sigma/(sigma+|mean|+eps)), bounded [0,1) z konstrukcji. Zaleznie
       WYLACZNIE od Q, nie od beta/klasy/N.

   τ (transformacja) = mean(|Δbeta_okno|) / dt_krok
       Tempo zmiany wagi podzialu beta miedzy kolejnymi krokami w oknie,
       znormalizowane krokiem czasowym symulacji - bezposredni analog
       "tempo zmiany defektu" z pozostalych szesciu domen. NIE bounded
       [0,1] - skala zalezy od dt_krok, patrz zastrzezenie w punkcie 4.

   ρ (anomalia)      = |{i w oknie: klasa[i] == "III"}| / |okno|
       Frakcja kroku w oknie sklasyfikowanych jako glebnoka anomalia -
       bezposredni analog "frakcja komorek nad progiem anomalii" z
       pozostalych szesciu domen. Bounded [0,1] z konstrukcji.
       Zalezne WYLACZNIE od klasy (czyli od beta), nie od N.

   J (kanal rezonansu/sprzezenia) = mean(|N_okno| / (max(|N_okno|) + eps))
       Srednia wzgledna wielkosc nakladania kanalow N(t)=S_down*S_up
       W OKNIE, znormalizowana do WLASNEGO maksimum w tym samym oknie -
       bounded [0,1] z konstrukcji. Zalezne WYLACZNIE od N (a wiec od
       S_down/S_up razem), NIE od samej klasy/beta wprost - to jest
       CELOWO INNA wielkosc zrodlowa niz ρ, zeby nie byc z definicji
       podzbiorem/nadzbiorem ρ (gdyby J bylo np. "frakcja kroku z
       cutoff=True", bylby to z KONSTRUKCJI nadzbior ρ, bo klasa III
       wymaga cutoff=True - to bylaby gwarantowana korelacja z
       definicji, nie empiryczny wynik do sprawdzenia).

3. OCZEKIWANIA PRZED URUCHOMIENIEM (na tryb miekki i twardy z
   tests/test_sg_coupling_full_operator{,_hard_mode}.py):
   - Oczekuje sie mean(ρ) tryb_twardy > mean(ρ) tryb_miekki (bo tryb
     twardy z definicji osiaga Klase III, miekki - nie, patrz
     tests/test_signal_class.py::test_trace_reaches_class_II_or_III_during_anomaly_soft_mode).
   - Oczekuje sie mean(J) tryb_twardy > mean(J) tryb_miekki (wieksze N
     przy glebszym przekroczeniu - ale to NIE jest tautologia jak w
     punkcie 2 wyzej, bo J bazuje na N, nie na klasie).
   - WSZYSTKIE magnitude(M) musza byc skonczone (brak NaN/inf).
   - Czy classify_phase() (progi 0.1/1.0 z oryginalnego szkicu
     META-DYNAMICS) FAKTYCZNIE rozroznia tryb miekki od twardego - NIE
     jest zakladane z gory. Sprawdzone i uczciwie zaraportowane w
     tests/test_signal_meta_bridge.py, dokladnie tak jak w pozostalych
     szesciu domenach ("mechanizm dziala, progi nieskalibrowane" bylo
     realnym wynikiem w Quantum-Lattice - tu moze wyjsc tak samo, inaczej,
     albo wcale nie rozroznic reżimow - kazdy z tych wynikow jest
     kompletna, honest odpowiedzia).

4. ZASTRZEZENIE DZIEDZICZONE (patrz _vendor_meta_state.py i oryginalny
   docstring classify_phase()): progi 0.1/1.0 sa arbitralne/heurystyczne
   w oryginalnym szkicu META-DYNAMICS, nie skalibrowane na ZADNEJ
   konkretnej domenie. Skala tu (τ w szczegolnosci, ktora dzieli przez
   dt_krok=0.01 domyslnie, wiec moze latwo przekroczyc 1.0 nawet dla
   niewielkich zmian beta) jest calkowicie inna niz skala w pozostalych
   szesciu domenach - NIE zaklada sie z gory, ze te same progi maja tu
   jakikolwiek sens, dokladnie jak przy Quantum-Lattice.
"""
from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

import numpy as np

from timdr_formalism._vendor_meta_state import MetaState, MetaOperatorM

EPS = 1e-9


def _window_slices(n: int, window_size: int):
    """Partycja (bloki rozlaczne, NIE okno przesuwne) [0,n) na bloki
    dlugosci window_size - ostatni blok moze byc krotszy, jesli n nie
    dzieli sie rowno."""
    if window_size <= 0:
        raise ValueError(f"window_size musi byc > 0, dostano {window_size}")
    start = 0
    while start < n:
        end = min(start + window_size, n)
        yield start, end
        start = end


def aggregate_window_to_meta_state(
    Q_window: np.ndarray,
    beta_window: np.ndarray,
    classes_window: Sequence[str],
    N_window: np.ndarray,
    dt_step: float,
) -> MetaState:
    """Agreguje jedno okno (blok rozlaczny) sladu symulacji do
    pojedynczego MetaState(Λ,τ,ρ,J). Wzory i uzasadnienie - patrz
    naglowek modulu, punkt 2 pre-rejestracji."""
    Q_window = np.asarray(Q_window, dtype=float)
    beta_window = np.asarray(beta_window, dtype=float)
    N_window = np.asarray(N_window, dtype=float)

    if len(Q_window) == 0:
        raise ValueError("okno puste - nie da sie zagregowac MetaState")

    # Λ: dyspersja Q w oknie, wzgledem wlasnej skali (ten sam ksztalt co Λ_G).
    q_mean = float(np.mean(Q_window))
    q_std = float(np.std(Q_window))
    Lambda = q_std / (q_std + abs(q_mean) + EPS)

    # τ: tempo zmiany beta w oknie, na jednostke czasu.
    if len(beta_window) >= 2:
        d_beta = np.diff(beta_window)
        tau = float(np.mean(np.abs(d_beta))) / dt_step
    else:
        tau = 0.0

    # ρ: frakcja kroku w oknie sklasyfikowanych jako Klasa III.
    n_total = len(classes_window)
    n_class_iii = sum(1 for c in classes_window if c == "III")
    rho = n_class_iii / n_total if n_total > 0 else 0.0

    # J: srednia relatywna wielkosc nakladania kanalow N(t), znormalizowana
    # do WLASNEGO maksimum |N| w tym samym oknie.
    abs_N = np.abs(N_window)
    max_abs_N = float(np.max(abs_N)) if len(abs_N) > 0 else 0.0
    if max_abs_N > 0:
        J = float(np.mean(abs_N / (max_abs_N + EPS)))
    else:
        J = 0.0

    return MetaState(Lambda=Lambda, tau=tau, rho=rho, J=J)


def signal_trace_to_meta_states(
    t: np.ndarray,
    Q: np.ndarray,
    beta_trace: np.ndarray,
    classes: Sequence[str],
    N_trace: np.ndarray,
    window_size: int = 50,
) -> Tuple[List[MetaState], List[float]]:
    """Dzieli caly slad symulacji na rozlaczne okna `window_size` krokow
    i zwraca (lista MetaState - jeden per okno, lista czasow poczatku
    kazdego okna). `beta_trace`/`N_trace` moga zawierac NaN dla krokow
    bez wyzwolonego cutoff (konwencja run_sg_coupling_simulation_v2) -
    zastepowane tu 1.0 (beta, brak reakcji = pelne "holomorficzne"
    zachowanie) i 0.0 (N, brak nakladania kanalow) przed agregacja,
    zgodnie z ta sama konwencja co reszta pipeline'u."""
    t = np.asarray(t, dtype=float)
    Q = np.asarray(Q, dtype=float)
    beta_trace = np.asarray(beta_trace, dtype=float)
    N_trace = np.asarray(N_trace, dtype=float)

    beta_filled = np.where(np.isnan(beta_trace), 1.0, beta_trace)
    N_filled = np.where(np.isnan(N_trace), 0.0, N_trace)

    if len(t) < 2:
        raise ValueError("potrzeba co najmniej 2 probek, zeby wyznaczyc dt_step")
    dt_step = float(t[1] - t[0])

    meta_states: List[MetaState] = []
    window_starts: List[float] = []

    for start, end in _window_slices(len(t), window_size):
        meta_states.append(
            aggregate_window_to_meta_state(
                Q_window=Q[start:end],
                beta_window=beta_filled[start:end],
                classes_window=classes[start:end],
                N_window=N_filled[start:end],
                dt_step=dt_step,
            )
        )
        window_starts.append(float(t[start]))

    return meta_states, window_starts


def meta_states_to_phases(
    meta_states: Sequence[MetaState],
    window_starts: Sequence[float],
) -> List[Tuple[Optional[float], Optional[str]]]:
    """Dla kazdej PARY kolejnych MetaState liczy operator ewolucji M i
    klasyfikuje faze systemu. Pierwsze okno nie ma poprzednika - zwraca
    (None, None) dla niego, zeby dlugosc wyniku byla rowna dlugosci
    wejscia (ulatwia zestawianie z window_starts przy analizie)."""
    if len(meta_states) != len(window_starts):
        raise ValueError("meta_states i window_starts musza miec ta sama dlugosc")

    op = MetaOperatorM()
    results: List[Tuple[Optional[float], Optional[str]]] = [(None, None)]

    for i in range(1, len(meta_states)):
        dt_between = window_starts[i] - window_starts[i - 1]
        if dt_between <= 0:
            raise ValueError(f"window_starts musza byc rosnace, dostano dt={dt_between} na indeksie {i}")
        M = op.compute(meta_states[i - 1], meta_states[i], dt_between)
        magnitude = op.magnitude(M)
        phase = op.classify_phase(M)
        results.append((magnitude, phase))

    return results
