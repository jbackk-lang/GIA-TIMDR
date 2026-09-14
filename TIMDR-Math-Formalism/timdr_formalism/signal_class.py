"""
timdr_formalism/signal_class.py

Klasy sygnalu I/II/III dla SG-Coupling/Theta_bif - implementacja
OFICJALNEJ definicji dostarczonej przez uzytkownika 2026-09-12
("OFICJALNA DEFINICJA KLAS SYGNALOW (TIMDR-SG)", docelowo
docs/theory/Signal_Classes.md).

Oficjalna definicja (skrot, pelna tresc w Signal_Classes.md):
  Klasa I   (zachowawcze):  Q<=Q_crit, beta~1, S_up~0, N~0, det(K)>0
  Klasa II  (modulujace):   Q<=Q_crit ale blisko progu, beta w (0.8,1.0),
                            S_up>0 ale male (<5%), N niewielkie, det(K)>0
  Klasa III (anomalie strukt.): Q>Q_crit, beta<0.5, S_up duze (>=20%),
                            N duze (max = punkt przelomu), det(K)->0

DWIE RZECZY WYMAGAJACE ROZWIAZANIA PRZED IMPLEMENTACJA (obie
przedyskutowane i zdecydowane z uzytkownikiem PRZED napisaniem tego
kodu, nie ciche zalozenia):

1. beta w (0.8,1.0) DLA Q<=Q_crit bylo niemozliwe starym `compute_beta`
   (funkcja skokowa, beta=1.0 dokladnie dla kazdego Q<=Q_crit) - patrz
   `timdr_formalism/theta_bifurcation.py`, "DODANY MARGINES
   OSTRZEGAWCZY". Rozwiazane dodaniem `anticipation_fraction` do
   `compute_beta` (domyslnie 0.05, wyliczone tak, zeby JEDNOCZESNIE
   spelnic beta w (0.8,1.0) ORAZ S_up%<5% na progu, nie tylko jeden z
   dwoch warunkow).

2. det(K) jest TOZSAMOSCIOWO ZERO w tym toy-modelu (sprawdzone
   rozniczkami skonczonymi na faktycznym update-mapie G/S - G nie ma
   sprzezenia zwrotnego do dynamiki S) - NIE roznica zadnej strefy od
   innej. Na jawna decyzje uzytkownika (2026-09-12): det(K) NIE jest
   uzywane w tym klasyfikatorze. Patrz naglowek theta_bifurcation.py,
   "UWAGA O POMINIETYM det(K)".

TRZECIA RZECZ, ZNALEZIONA PRZY IMPLEMENTACJI (nie byla czescia
dyskusji z uzytkownikiem - odnotowana tu wprost, nie cicho pominieta):
warunki oficjalnej definicji dla Klasy II/III NIE sa w pelni spojne ze
soba jako niezalezne bramki:

  a) "Q>Q_crit" (warunek Klasy III) NIE gwarantuje "beta<0.5" - miedzy
     Q_crit a glebokim przekroczeniem jest CALY zakres Q, w ktorym
     Q>Q_crit, ale beta wciaz >=0.5 (to jest dokladnie "strefa miekka"
     z test_sg_coupling_phase_diagram.py) - taki punkt spelnialby
     literalnie ANI warunku Klasy II (bo Q>Q_crit), ANI Klasy III (bo
     beta>=0.5), gdyby oba warunki (Q vs Q_crit, i beta vs prog)
     traktowac jako niezalezne, rownorzedne bramki.//
  b) "S_up>=20%" (tj. beta<=0.8) i "beta<0.5" to DWIE ROZNE granice
     (S_up>=20% jest SLABSZYM warunkiem niz beta<0.5 - punkt o beta=0.7
     ma S_up%=30%>=20%, ale NIE ma beta<0.5).

ROZWIAZANIE (decyzja implementacyjna, jawnie oznaczona): `beta` jest
TRAKTOWANE JAKO PIERWOTNY, JEDYNY dyskryminator granic klas (bo jest
JEDYNA wielkoscia wspolna wszystkim trzem opisom klas, i bo granica
beta<0.5 byla juz wczesniej ustalona i uzasadniona matematycznie w
test_sg_coupling_phase_diagram.py jako punkt rownowagi wag kanalow).
`Q` vs `Q_crit` i `S_up%` sa raportowane jako wielkosci OPISOWE/
DIAGNOSTYCZNE (spojne z klasa w wiekszosci przypadkow, ale NIE
niezaleznymi bramkami) - `N(t)` podobnie, diagnostyczne, nie
klasyfikujace. Granice klas w tej implementacji:

  Klasa I:   beta == 1.0 DOKLADNIE (Q<=Q_eff_crit, zero reakcji)
  Klasa II:  0.5 <= beta < 1.0        (modulujace - obejmuje ZAROWNO
             "blisko progu od dolu" JAK I "lekkie przekroczenie od gory")
  Klasa III: beta < 0.5              (ten sam prog co w phase_diagram.py)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from timdr_formalism.theta_bifurcation import (
    compute_beta,
    BETA_ANTICIPATION_FRACTION_DEFAULT,
)

BETA_CLASS_III_THRESHOLD = 0.5  # ten sam prog co test_sg_coupling_phase_diagram.py


@dataclass(frozen=True)
class SignalClassResult:
    signal_class: str  # "I" | "II" | "III"
    Q: float
    Q_crit: float
    beta: float
    S_up_pct: float  # (1-beta)*100 - diagnostyczne, patrz naglowek modulu
    N: Optional[float]  # S_down*S_up, None jesli nie podano (brak pelnego sladu)
    is_past_hard_threshold: bool  # Q > Q_crit (opisowe, NIE bramka klasy)


def classify_by_beta(beta: float) -> str:
    """Jedyny, autorytatywny dyskryminator granic klas - patrz naglowek
    modulu dla uzasadnienia, dlaczego to jest beta, nie Q vs Q_crit ani
    S_up% osobno."""
    if beta >= 1.0:
        return "I"
    if beta >= BETA_CLASS_III_THRESHOLD:
        return "II"
    return "III"


def classify_signal_point(
    Q: float,
    Q_crit: float,
    anticipation_fraction: float = BETA_ANTICIPATION_FRACTION_DEFAULT,
    S_down: Optional[float] = None,
    S_up: Optional[float] = None,
) -> SignalClassResult:
    """Klasyfikuje POJEDYNCZY punkt (Q, Q_crit) do klasy sygnalu I/II/III.

    S_down/S_up: opcjonalne, RZECZYWISTE wartosci kanalow z
    theta_bifurcation() (jesli operator faktycznie juz zadzialal, tj.
    Q>Q_crit) - podane, zeby policzyc N(t)=S_down*S_up jako
    diagnostyke. Jesli nie podane (lub Q<=Q_crit, gdzie rzeczywiste
    S_up operatora jest zawsze 0.0 z definicji), N=0.0 przez konwencje
    (brak ingerencji = brak nakladania kanalow).
    """
    beta = compute_beta(Q, Q_crit, anticipation_fraction=anticipation_fraction)
    signal_class = classify_by_beta(beta)
    S_up_pct = (1.0 - beta) * 100.0

    if S_down is not None and S_up is not None:
        N = S_down * S_up
    else:
        N = 0.0

    return SignalClassResult(
        signal_class=signal_class,
        Q=Q,
        Q_crit=Q_crit,
        beta=beta,
        S_up_pct=S_up_pct,
        N=N,
        is_past_hard_threshold=Q > Q_crit,
    )


def classify_signal_trace(t, Q, Q_crit, cutoff, S_down_trace, S_up_trace,
                           anticipation_fraction: float = BETA_ANTICIPATION_FRACTION_DEFAULT):
    """Klasyfikuje KAZDY krok juz policzonej symulacji
    (run_sg_coupling_simulation_v2 z tests/test_sg_coupling_full_operator.py)
    - zwraca liste SignalClassResult, jeden na krok.

    Dla krokow bez wyzwolonego cutoff (cutoff[i]=False), S_down_trace/
    S_up_trace sa NaN w surowym sladzie (operator nie zostal wywolany)
    - tu jawnie podstawiane N=0.0 (konwencja: brak ingerencji = brak
    nakladania), zamiast NaN wyciekajacego do wyniku."""
    results = []
    for i in range(len(t)):
        if cutoff[i]:
            S_down_i = float(S_down_trace[i])
            S_up_i = float(S_up_trace[i])
            result = classify_signal_point(
                Q[i], Q_crit, anticipation_fraction=anticipation_fraction,
                S_down=S_down_i, S_up=S_up_i,
            )
        else:
            result = classify_signal_point(
                Q[i], Q_crit, anticipation_fraction=anticipation_fraction,
            )
        results.append(result)
    return results
