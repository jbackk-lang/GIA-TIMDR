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
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

S_UP_MAX_DEFAULT = 10.0  # gorna granica amplitudy kanalu kondensujacego


@dataclass(frozen=True)
class ThetaBifResult:
    S_new: float
    beta: float
    S_down: float
    S_up: float
    in_bifurcation: bool


def compute_beta(Q: float, Q_crit: float) -> float:
    """Waga podziału beta(t) in [0,1] - patrz naglowek modulu, punkt 1."""
    if Q <= Q_crit:
        return 1.0  # poza trybem bifurkacji, konwencja: caly "wklad" w kanale spoczynkowym
    max_slack = 1.0 - Q_crit
    if max_slack <= 0:
        return 0.0
    exceedance = Q - Q_crit
    beta = 1.0 - exceedance / max_slack
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
        return ThetaBifResult(S_new=S, beta=1.0, S_down=S, S_up=0.0, in_bifurcation=False)

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
    return ThetaBifResult(S_new=S_new, beta=beta, S_down=S_down, S_up=S_up, in_bifurcation=True)
