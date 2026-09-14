"""
timdr_formalism/theta_bifurcation.py

Pelny operator bifurkacji Theta_bif, zgodnie z propozycja z rozmowy:

    Theta_bif[S(t)] = S_holo(t)                 dla t < t_cutoff
                    = S_down(t) + S_up(t)         dla t >= t_cutoff

    S_down(t) = beta(t) * S(t) * exp(-lambda_down * (t - t_cutoff))
    S_up(t)   = (1-beta(t)) * R_phase[S(t)] * exp(+lambda_up * (t - t_cutoff))

gdzie R_phase[S] = -S (odbicie fazowe), a beta(t) in [0,1] to waga
podziału miedzy kanalem wygaszanym (S_down, "defekt/pamiec") a
kondensujacym (S_up, "nowy trend/punkt osobliwy").

DWIE RZECZY, KTORE BYLY NIEDOPRECYZOWANE W ORYGINALNEJ PROPOZYCJI --
musialem je jednoznacznie ustalic, zeby operator w ogole dal sie
zaimplementowac i przetestowac. To NIE sa cichy odstepstwa -- oba
udokumentowane tu i w testach, z uzasadnieniem:

1. WZOR NA beta(t). Propozycja mowila tylko "wagą podziału β(t)∈[0,1]
   determinowaną przez stopień przekroczenia Q_crit", bez wzoru. Przyjeta
   tu definicja:

       beta(t) = clip(1 - (Q(t)-Q_crit) / (1-Q_crit), 0, 1)

   Uzasadnienie: Q(t) asymptotycznie dazy do 1 (bo Q=1-L0/L(R), L(R)->inf
   przy R->inf), wiec (1-Q_crit) to maksymalny mozliwy "zapas" powyzej
   progu. Przy Q(t) tuz nad progiem: beta~1 (niemal caly sygnal idzie do
   kanalu WYGASZANEGO -- lekkie przekroczenie progu traktowane jako szum).
   Przy Q(t)->1 (glebokie przekroczenie): beta~0 (niemal caly sygnal idzie
   do kanalu KONDENSUJACEGO -- silne przekroczenie traktowane jako
   prawdziwy nowy trend). To jest WYBOR, nie jedyna mozliwa formalizacja
   -- ale jest monotoniczny, ograniczony do [0,1] z definicji, i zgodny z
   opisana intencja (male przekroczenia -> szum/tlumienie, duze -> realny
   sygnal/kondensacja).

2. NIEOGRANICZONY WZROST S_up JEST NIEFIZYCZNY I NUMERYCZNIE NIESTABILNY.
   Wzor S_up ~ exp(+lambda_up * (t-t_cutoff)) rosnie BEZ OGRANICZEN, jesli
   uklad pozostaje w trybie bifurkacji dluzej niz ~1/lambda_up jednostek
   czasu -- dla dlugiej anomalii (albo lambda_up niefortunnie dobranego)
   to daje przepelnienie (inf/NaN) w skonczonym czasie symulacji, nie
   "kondensacje w nowy trwaly stan". "Kondensacja w nowy trend" powinna
   NASYCAC SIE (zblizac do stalej amplitudy), nie rosnac bez konca --
   dokladnie tak jak realne zjawiska przejscia fazowego / bifurkacji w
   ukladach dynamicznych (np. bifurkacja widlowa: nowy punkt rownowagi ma
   SKONCZONA amplitude, nie rosnie w nieskonczonosc).

   POPRAWKA: exp(+lambda_up*dt) zastapione przez S_UP_MAX * tanh(lambda_up*dt)
   -- ta sama monotoniczna narastajaca odpowiedz dla malych dt (tanh(x)~x
   dla x bliskiego 0, wiec lokalne zachowanie startowe jest analogiczne
   do wzrostu), ale z gwarantowanym ograniczeniem |S_up|<=S_UP_MAX dla
   KAZDEGO dt, wiec zaden skonczony czas symulacji nie moze dac
   przepelnienia. Jawnie oznaczone jako ODSTEPSTWO od dostarczonego wzoru,
   nie cicha zamiana.

PRE-REJESTRACJA (przed uruchomieniem testow ponizej):
  Kontrola 1 (lekkie przekroczenie): Q tuz nad Q_crit -> beta bliskie 1
    -> |S_po_operatorze| powinno MALEC monotonicznie w czasie (dominuje
    kanal wygaszany).
  Kontrola 2 (glebokie i dlugie przekroczenie): Q bliskie 1 utrzymane
    przez dlugi czas -> beta bliskie 0 -> |S_po_operatorze| powinno
    ROSNAC, ale NASYCAC SIE do wartosci <= S_UP_MAX, nie rosnac bez
    ograniczen (test na wielu wartosciach czasu, w tym bardzo dlugim
    horyzoncie, sprawdzajacy brak inf/NaN).
  Kontrola 3 (poza trybem bifurkacji): dla Q(t) <= Q_crit operator musi
    zwracac S(t) BEZ ZMIAN (galaz "holomorficzna"/normalna, brak
    ingerencji).

ZNALEZIONA WLASCIWOSC MODELU (nie zalozona z gory, wyszla przy pisaniu
testow kontroli 1 -- pierwsza wersja testu zakladala, ze lekkie
przekroczenie progu powinno z czasem zanikac do ~0, i ta wersja testu
FAILOWALA): kanal S_up nasyca sie (przez tanh) do (1-beta)*S_up_max,
NIE do zera, dla KAZDEGO niezerowego (1-beta) -- czyli nawet BARDZO
lekkie przekroczenie progu (Q tuz nad Q_crit, beta~0.98) zostawia
TRWALY, niezerowy "odcisk" w sygnale (rzedu kilkunastu % oryginalnej
amplitudy dla przykladowych parametrow), zamiast w pelni zanikac do
zera. Powaga przekroczenia progu kontroluje ROZMIAR tego trwalego
residuum (male dla lekkiego przekroczenia, duze dla glebokiego), NIE
to, czy residuum w ogole istnieje. To jest uczciwie odnotowany
kompromis wprowadzony poprawka nasycenia (punkt 2 powyzej) -- gdyby
model mial w pelni "zapominac" lekkie przekroczenia, wymagaloby to
dodatkowego mechanizmu (np. progu na (1-beta), ponizej ktorego caly
wklad idzie do kanalu wygaszanego), ktorego oryginalna propozycja NIE
opisywala i ktory NIE zostal tu dodany bez wyraznej prosby -- ta wersja
jest wierna najprostszej, dosłownej interpretacji wzoru z poprawka
tylko tam, gdzie to bylo NIEZBEDNE (nasycenie zamiast wybuchu).

ZNALEZIONY REALNY BLAD (2026-09-12, przy budowie "phase diagram"
parametrow SG-Coupling, NIE zalozony/przewidziany z gory): poprawka z
punktu 2 (tanh zamiast exp) okazala sie NIEWYSTARCZAJACA. Deklarowany
sufit "|S_up|<=S_UP_MAX dla KAZDEGO dt" byl PRAWDZIWY tylko dopoki S
(wejsciowa wartosc sygnalu PRZED operatorem) pozostawalo w skali rzedu
1-10 -- czyli dokladnie tak, jak we wszystkich testach w tym pliku
(S0=0.5, 1.0, 2.0). Oryginalny wzor uzywal `R_phase[S] = -S` (SUROWA
wartosc/amplituda sygnalu), NIE kierunku znormalizowanego do dlugosci 1
-- wiec S_up skalowalo sie WPROST PROPORCJONALNIE do wielkosci S, a nie
bylo naprawde ograniczone przez S_up_max. W realnej petli SG-Coupling ze
sprzezeniem zwrotnym (gdzie S samo w sobie moze urosnac, zanim operator
w ogole zdazy zadzialac -- np. alpha=2.0, anomaly_bump=130.0 w
tests/test_sg_coupling_full_operator.py) to dawalo NIESTABILNA PETLE
DODATNIEGO SPRZEZENIA: kazdy krok mnozyl |S| przez czynnik rzedu
~S_up_max (bo S_up~S_up_max*(-S)), co samo w sobie jest niestabilnym
rownaniem rozniczkowym (|S_new|~S_up_max*|S_old|, S_up_max=10 > 1) --
skonczony wybuch do inf w kilkadziesiat krokow, dokladnie ten sam objaw
(przepelnienie), ktoremu poprawka z punktu 2 miala zapobiegac, tylko
przez inny mechanizm.

POPRAWKA: R_phase[S] zdefiniowane jako KIERUNEK (-sign(S), dlugosc <=1),
NIE surowa wartosc (-S). Teraz S_up = (1-beta)*(-sign(S))*S_up_max*
tanh(...) jest NAPRAWDE ograniczone przez S_up_max niezaleznie od tego,
jak duze jest wejsciowe S -- sufit jest teraz prawdziwy dla KAZDEGO S,
nie tylko dla S w skali testowanej w tym pliku. To jest zgodne z
zamierzona interpretacja "kondensacji do nowego trwalego stanu": nowy
stan powinien miec STALA, wyznaczona przez S_up_max amplitude,
niezaleznie od tego, jak wielka byla amplituda PRZED bifurkacja -- nie
powinien "pamietac" starej skali przez wspolczynnik proporcjonalnosci.
Zweryfikowane bezposrednio: tests/test_sg_coupling_phase_diagram.py
zawiera test regresyjny odtwarzajacy dokladnie ten przypadek
(alpha=2.0, anomaly_bump=130.0), ktory PRZED ta poprawka konczyl sie
przepelnieniem (inf), a PO niej daje skonczony wynik.

DODANY MARGINES OSTRZEGAWCZY W beta(Q) (2026-09-12, na potrzeby
klasyfikacji sygnalu I/II/III, patrz timdr_formalism/signal_class.py):
oficjalna definicja "Klasy II" (sygnal modulujacy) wymagala
`Q(R) <= Q_crit, ale blisko progu, beta w (0.8-1.0)`. Sprawdzone
bezposrednio: STARY wzor `compute_beta` byl funkcja SKOKOWA - zwracal
DOKLADNIE 1.0 dla KAZDEGO Q<=Q_crit, bez zadnego stopniowego zblizania
sie do progu - "beta w (0.8,1.0) PRZED przekroczeniem progu" bylo
matematycznie nieosiagalne starym wzorem.

POPRAWKA: `compute_beta` dostal parametr `anticipation_fraction`
(domyslnie 0.05 - patrz uzasadnienie liczbowe nizej) - definiuje
EFEKTYWNY, "miekki" prog
`Q_eff_crit = Q_crit - anticipation_fraction*(1-Q_crit)`, o
`anticipation_fraction` czesci pozostalego zapasu (1-Q_crit) PONIZEJ
prawdziwego progu. Ten sam liniowy wzor co wczesniej
(`1 - exceedance/max_slack`) jest teraz stosowany wzgledem
`Q_eff_crit` zamiast `Q_crit` - wiec beta zaczyna lagodnie spadac juz w
przedziale `[Q_eff_crit, Q_crit]`, osiagajac przy Q=Q_crit dokladnie
`1 - anticipation_fraction/(1+anticipation_fraction)`.

DLACZEGO DOKLADNIE 0.05, NIE ZGADNIETE: oficjalna definicja Klasy II
(`docs/theory/Signal_Classes.md`) wymaga JEDNOCZESNIE `beta w (0.8,1.0)`
ORAZ `S_up < 5%` (gdzie S_up% traktowane tu jako `(1-beta)*100%` - patrz
`timdr_formalism/signal_class.py`) na progu Q=Q_crit. Sprawdzone
bezposrednio: `anticipation_fraction=0.1` (pierwsza probowana wartosc)
dawalo `beta(Q_crit)~0.909`, czyli `S_up%~9.09%` - SPELNIA pierwszy
warunek, ALE LAMIE drugi (9.09%>5%). Rozwiazane algebraicznie z obu
warunkow naraz: `1-beta(Q_crit) = anticipation_fraction/(1+anticipation_fraction) = 0.05`
=> `anticipation_fraction = 0.05/0.95 ~ 0.0526`, zaokraglone w dol do
`0.05` (bezpieczny margines: `S_up%(Q_crit)=4.76%<5%`, `beta(Q_crit)=0.9524`
w (0.8,1.0)) - obie granice oficjalnej definicji spelnione JEDNOCZESNIE,
nie tylko jedna z dwoch. WAZNE: to NIE zmienia tego, KIEDY operator `theta_bifurcation`
faktycznie modyfikuje sygnal - ten prog (twardy, dokladnie `Q<=Q_crit`,
"galaz holomorficzna bez ingerencji") zostaje BEZ ZMIAN, bo jest
osobno, jawnie testowany (`test_exactly_at_threshold_returns_unchanged_signal`)
i to jest INNY fakt niz "jak blisko jestesmy progu" - margines
ostrzegawczy w `compute_beta` sluzy WYLACZNIE diagnostyce/klasyfikacji
(dziala tez jako uzyteczny, ciaglejszy sygnal wewnatrz samego operatora,
gdy Q>Q_crit juz przekroczone - patrz nizej), nie zmienia faktycznego
dzialania operatora PRZED przekroczeniem progu.

Skutek uboczny (zaakceptowany, zweryfikowany): poniewaz `compute_beta`
jest tez wolane WEWNATRZ `theta_bifurcation` gdy `Q>Q_crit`, nowy,
przesuniety wzor zmienia NIECO liczbowe wartosci beta rowniez PO
przekroczeniu progu (nieco wolniejszy spadek do zera, bo max_slack_eff
jest wiekszy niz max_slack) - cala istniejaca paczka testow
(theta_bifurcation, sg_coupling_full_operator, hard_mode, phase_diagram)
zostala ponownie uruchomiona i, gdzie trzeba, poprawiona z jawnym
wyjasnieniem, NIE cichym przesunieciem progu pod nowy wynik.

DODANE N(t) = S_down * S_up ("nakladanie kanalow", potrzebne do
klasyfikacji sygnalu): trywialna wielkosc wyprowadzona z juz
istniejacych S_down/S_up, dodana jako pole `N` w `ThetaBifResult`. Dla
Q<=Q_crit (brak bifurkacji) S_up=0, wiec N=0 zawsze - zgodne z
oczekiwaniem "N(t)~=0" dla sygnalu w normie.

UWAGA O POMINIETYM det(K): oficjalna propozycja klasyfikacji I/II/III
wlaczala tez `det(K)` (zapasc przestrzeni stanow, z GS-Matrix) jako
piaty warunek. Sprawdzone bezposrednio (rozniczki skonczone na
faktycznym update-mapie G/S z run_sg_coupling_simulation_v2): Jakobian
d(G_new,S_new)/d(G_old,S_old) ma KOLUMNE G_old TOZSAMOSCIOWO ZEROWA w
KAZDYM punkcie (bo G=R0+alpha*S^2 jest JEDNOKIERUNKOWYM odczytem z S -
G nigdy nie wplywa z powrotem na dynamike S), wiec det(K)=0 WSZEDZIE,
niezaleznie od Q/alpha/bump - nie rozroznia zadnej strefy. Na jawna
decyzje (2026-09-12): det(K) NIE jest uzywane w klasyfikatorze sygnalu
dla TEGO konkretnego toy-modelu - K (z GS-Matrix, `gs_matrix.py`) jest
osobnym, niepolaczonym numerycznie obiektem (macierz dla ODDZIELNEGO
ukladu `dV/dt=KV`), nie wielkoscia obliczalna z trajektorii (G(t),S(t))
tej symulacji bez wiekszej, osobno uzasadnionej zmiany modelu (nadanie
G wlasnej dynamiki ze sprzezeniem zwrotnym od S) - taka zmiana NIE
zostala tu wprowadzona bez wyraznej prosby.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

S_UP_MAX_DEFAULT = 10.0  # gorna granica amplitudy kanalu kondensujacego
BETA_ANTICIPATION_FRACTION_DEFAULT = 0.05  # patrz "DODANY MARGINES OSTRZEGAWCZY" w naglowku - 0.05 wyliczone tak, zeby S_up%(Q_crit)<5% ORAZ beta(Q_crit) w (0.8,1.0) jednoczesnie


@dataclass(frozen=True)
class ThetaBifResult:
    S_new: float
    beta: float
    S_down: float
    S_up: float
    N: float
    in_bifurcation: bool


def compute_beta(
    Q: float,
    Q_crit: float,
    anticipation_fraction: float = BETA_ANTICIPATION_FRACTION_DEFAULT,
) -> float:
    """Waga podziału beta(t) in [0,1] - patrz naglowek modulu, punkty 1
    i "DODANY MARGINES OSTRZEGAWCZY".

    `anticipation_fraction`: jaka czesc pozostalego zapasu (1-Q_crit)
    ponizej prawdziwego progu Q_crit ma stanowic "miekki" margines, w
    ktorym beta zaczyna juz lagodnie spadac ponizej 1.0 (uzyteczne dla
    klasyfikacji sygnalu - patrz timdr_formalism/signal_class.py, Klasa II).
    `anticipation_fraction=0.0` odtwarza STARY, czysto skokowy wzor
    (beta=1.0 dokladnie dla Q<=Q_crit)."""
    max_slack = 1.0 - Q_crit
    if max_slack <= 0:
        # Q_crit>=1: prog matematycznie nieosiagalny (strefa martwa,
        # patrz test_sg_coupling_phase_diagram.py) - brak sensownego
        # marginesu do zdefiniowania.
        return 1.0 if Q <= Q_crit else 0.0

    soft_margin = anticipation_fraction * max_slack
    Q_eff_crit = Q_crit - soft_margin
    max_slack_eff = max_slack + soft_margin  # = 1.0 - Q_eff_crit

    if Q <= Q_eff_crit:
        return 1.0
    exceedance = Q - Q_eff_crit
    beta = 1.0 - exceedance / max_slack_eff
    return float(np.clip(beta, 0.0, 1.0))


def theta_bifurcation(
    S: float,
    Q: float,
    Q_crit: float,
    time_since_cutoff_start: float,
    lambda_down: float = 2.0,
    lambda_up: float = 1.0,
    S_up_max: float = S_UP_MAX_DEFAULT,
) -> ThetaBifResult:
    """Pelny operator bifurkacji - patrz naglowek modulu dla wzorow i
    dwoch udokumentowanych odstepstw od oryginalnej, niedoprecyzowanej
    propozycji (wzor na beta, nasycenie zamiast nieograniczonego wzrostu).

    S: wartosc skladowej sygnalowej PRZED zastosowaniem operatora (S_raw).
    Q, Q_crit: biezaca wartosc parametru obwiedni i prog.
    time_since_cutoff_start: czas (w tych samych jednostkach co reszta
      symulacji) od POCZATKU biezacego, ciaglego epizodu przekroczenia
      progu (0.0 w pierwszej probce, w ktorej Q przekroczylo Q_crit).
      Wywolujacy jest odpowiedzialny za sledzenie poczatku epizodu
      (patrz run_sg_coupling_simulation_v2 w tests/test_theta_bifurcation.py
      dla przykladu integracji).
    """
    if time_since_cutoff_start < 0:
        raise ValueError(f"time_since_cutoff_start musi byc >= 0, dostano {time_since_cutoff_start}")
    if lambda_down <= 0 or lambda_up <= 0:
        raise ValueError("lambda_down i lambda_up musza byc > 0")
    if S_up_max <= 0:
        raise ValueError("S_up_max musi byc > 0")

    if Q <= Q_crit:
        # Galaz "holomorficzna" (poza trybem bifurkacji) - brak ingerencji.
        # N=S_down*S_up=S*0=0, zgodnie z oczekiwaniem "N(t)~=0" dla Klasy I.
        return ThetaBifResult(S_new=S, beta=1.0, S_down=S, S_up=0.0, N=0.0, in_bifurcation=False)

    beta = compute_beta(Q, Q_crit)

    S_down = beta * S * float(np.exp(-lambda_down * time_since_cutoff_start))

    # R_phase[S] = -sign(S) - KIERUNEK odbicia fazowego (dlugosc <=1), NIE
    # -S (surowa wartosc/amplituda). Patrz PUNKT 3 w naglowku modulu dla
    # pelnego uzasadnienia tej poprawki -- oryginalna wersja (-S zamiast
    # -sign(S)) skalowala S_up WPROST proporcjonalnie do wejsciowego S,
    # wiec S_UP_MAX NIE bylo faktycznym sufitem, gdy S samo w sobie bylo
    # juz duze (co zdarza sie realnie w petli SG-Coupling ze sprzezeniem
    # zwrotnym) - i to prowadzilo do dokladnie tego samego rodzaju
    # niekontrolowanego wzrostu, ktoremu ta poprawka (tanh) miala zapobiec.
    if S == 0.0:
        R_phase_direction = 0.0
    else:
        R_phase_direction = -1.0 if S > 0.0 else 1.0
    S_up = (1.0 - beta) * R_phase_direction * S_up_max * float(np.tanh(lambda_up * time_since_cutoff_start))

    S_new = S_down + S_up
    N = S_down * S_up  # "nakladanie kanalow" - patrz naglowek modulu
    return ThetaBifResult(S_new=S_new, beta=beta, S_down=S_down, S_up=S_up, N=N, in_bifurcation=True)
