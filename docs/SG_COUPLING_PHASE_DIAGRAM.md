# Phase diagram TIMDR-SG-Coupling

Mapa parametrow (`alpha`, sila wstrzknietej anomalii) dla petli
SG-Coupling z pelnym operatorem Theta_bif
(`timdr_formalism/theta_bifurcation.py`). Kod klasyfikujacy i testy:
[`tests/test_sg_coupling_phase_diagram.py`](../tests/test_sg_coupling_phase_diagram.py).
Buduje na dwoch wczesniej ustalonych rezimach:
[`tests/test_sg_coupling_full_operator.py`](../tests/test_sg_coupling_full_operator.py)
(rezim "miekki") i
[`tests/test_sg_coupling_full_operator_hard_mode.py`](../tests/test_sg_coupling_full_operator_hard_mode.py)
(rezim "twardy").

**Powiazanie z klasami sygnalu I/II/III** (2026-09-12): ta mapa
klasyfikuje CALE kombinacje `(alpha, anomaly_bump)` w jedna z 4 stref;
[`docs/theory/Signal_Classes.md`](theory/Signal_Classes.md) klasyfikuje
KAZDY KROK czasowy z osobna (I/II/III) i pokazuje, jak obie warstwy sie
lacza - w tym udokumentowane zastrzezenie, ze strefa "cicha" NIE zawsze
znaczy "caly czas Klasa I".

![Phase diagram: siatka alpha x anomaly_bump pokolorowana wg strefy (martwa/cicha/miekka/twarda)](sg_coupling_phase_diagram.svg)

## Cztery strefy, nie trzy

Pierwotna propozycja mowila o trzech strefach (miekka/twarda/martwa).
Przy budowie okazalo sie, ze potrzebna jest **czwarta**, bo "martwa" i
"cutoff sie nie wyzwolil" to dwa rozne zjawiska o roznych przyczynach:

- **Martwa** (`Q_crit(alpha) > 1.0`) - kalibracja progu z tla
  (`calibrate_q_crit`, margines 1.3x) daje wartosc **matematycznie
  nieosiagalna**, bo `Q(R) = 1 - L0/(L0+2*pi*R) < 1` dla kazdego
  skonczonego `R`. Cutoff nie wyzwoli sie NIGDY dla tego `alpha`,
  niezaleznie od tego, jak silna bedzie anomalia. Granica zalezy
  **wylacznie od `alpha`** (kalibracja nie zna `anomaly_bump`) -
  sprawdzone wprost testem `test_dead_zone_is_independent_of_anomaly_strength`.
- **Cicha** (`Q_crit(alpha) <= 1.0`, ale cutoff sie nie wyzwolil) - prog
  jest osiagalny w zasadzie, ale AKURAT ta anomalia jest za slaba, zeby
  go przekroczyc w oknie `t in [4.8, 5.2]`.
- **Miekka** (`beta_min >= 0.5` podczas anomalii) - cutoff sie
  wyzwala, ale kanal tlumiacy (S_down) dominuje przez cala anomalie.
- **Twarda** (`beta_min < 0.5`) - kanal kondensujacy (S_up) przejmuje
  dominacje.

Granica miekka/twarda na `beta=0.5` to nie liczba dobrana pod wynik -
to matematyczny punkt rownowagi wag kanalow (`beta = 1-beta` przy
`beta=0.5`), ten sam prog uzyty juz wczesniej przy budowie trybu
twardego.

## Znaleziony po drodze realny blad (nie tylko trzecia/czwarta strefa)

Przy pierwszym przeszukiwaniu siatki pod katem tego dokumentu,
kombinacja `alpha=2.0, anomaly_bump=130.0` dala **przepelnienie (inf)**
- nie "twarda strefa", tylko faktyczny numeryczny wybuch. Zdiagnozowane
bezposrednio (wydruk krok-po-kroku): operator mial niezamierzona,
niestabilna petle dodatniego sprzezenia, bo `R_phase[S] = -S` (surowa
wartosc sygnalu) zamiast znormalizowanego kierunku `-sign(S)` - wiec
deklarowany sufit `S_up_max` NIE byl faktycznym ograniczeniem, gdy `S`
samo w sobie bylo juz duze (co zdarza sie realnie w tej petli ze
sprzezeniem zwrotnym). Naprawione w
[`timdr_formalism/theta_bifurcation.py`](../timdr_formalism/theta_bifurcation.py)
(patrz jego naglowek, sekcja "ZNALEZIONY REALNY BLAD"), zweryfikowane
testem regresyjnym (`test_previously_blowing_up_point_is_now_finite`) i
ponownym przeszukaniem szerszego zakresu (`alpha` do 13.5, `bump` do
500) bez ani jednego przepelnienia - co jest **obserwacja w
przeszukanym zakresie, nie dowodem zupelnosci naprawy** dla kazdego
mozliwego parametru.

## Jak czytac siatke

Wiersze: `alpha` (0.1 do 16). Kolumny: `anomaly_bump` (0.01 do 130).
Dla kazdego `alpha` idac w prawo (silniejsza anomalia): cicha -> miekka
-> twarda - monotoniczne, zgodne z intuicja (silniejsza anomalia pcha
glebiej w tryb kondensacji). Dla kazdego `anomaly_bump` idac w dol
(wiekszy `alpha`, do pewnego momentu): cicha strefa sie zaweza (wieksze
`alpha` samo z siebie podnosi `Q` tla, wiec slabsza anomalia wystarcza,
zeby przekroczyc kalibrowany prog), a granica miekka/twarda przesuwa
sie w lewo (latwiej o twarda strefe) - **az do `alpha~13.5-14`, gdzie
caly wiersz nagle staje sie martwy** - nieciagly przeskok, nie
stopniowe przejscie, bo to inny mechanizm (kalibracja przekracza 1.0,
nie stopniowe pogłębianie kondensacji).

## Ograniczenia tej mapy (uczciwie odnotowane)

- Siatka jest **dyskretna** (12x12 punktow) - granice miedzy strefami na
  obrazku sa interpolacja wizualna, nie dokladnym wyznaczeniem krzywej
  (poza granica martwej strefy, ktora ma dedykowana bisekcje w kodzie).
- Wszystkie pozostale parametry (`L0=5.0, R0=0.2, dt=0.01, duration=10.0,
  margin=1.3, lambda_down=2.0, lambda_up=1.0`) sa zamrozone na
  wartosciach domyslnych z reszty pakietu - mapa jest dla TEGO
  konkretnego przekroju przestrzeni parametrow, nie dla wszystkich
  siedmiu wymiarow naraz.
- "Brak przepelnienia w przeszukanym zakresie" (patrz wyzej) nie jest
  dowodem, ze operator jest wolny od tej klasy bledow dla kazdego
  mozliwego `alpha`/`anomaly_bump` - tylko ze nie znaleziono kontrprzykladu
  w powiekszonym, ale wciaz skonczonym przeszukaniu.
