# Klasy sygnału I/II/III (TIMDR-SG)

Formalna klasyfikacja sygnału dla SG-Coupling + Θ_bif + GS-Matrix,
dostarczona przez użytkownika 2026-09-12 jako "OFICJALNA DEFINICJA KLAS
SYGNAŁÓW (TIMDR-SG)". Ten dokument zawiera oryginalną definicję,
**trzy decyzje implementacyjne konieczne do jej zaimplementowania bez
numerologii** (uzgodnione z użytkownikiem albo jawnie odnotowane), i
połączenie z mapą faz (`SG_COUPLING_PHASE_DIAGRAM.md`).

Kod: [`timdr_formalism/signal_class.py`](../../timdr_formalism/signal_class.py),
testy: [`tests/test_signal_class.py`](../../tests/test_signal_class.py).

## Oryginalna definicja

Klasy wynikają z: `Q(R)` (geometryczny próg obwiedni), `β` (współczynnik
bifurkacji), `S↓,S↑` (kanały wygaszający/kondensujący), `N(t)=S↓·S↑`
(nakładanie kanałów), `det(K)` (zapaść przestrzeni stanów, z GS-Matrix).

**Klasa I — sygnały zachowawcze**: `Q≤Q_crit`, `β≈1`, `S↑≈0`, `N(t)≈0`,
`det(K)>0`. Sygnał nie narusza geometrii obwiedni, brak bifurkacji.

**Klasa II — sygnały modulujące**: `Q≤Q_crit` ale blisko progu,
`β∈(0.8,1.0)`, `S↑>0` ale małe (`<5%`), `N(t)` niewielkie, `det(K)>0`.
Sygnał zaczyna wpływać na geometrię, ale jej nie łamie.

**Klasa III — anomalie strukturalne**: `Q>Q_crit`, `β<0.5`, `S↑` duże
(`≥20%`), `N(t)` duże (maksimum = punkt przełomu), `det(K)→0`.

## Trzy decyzje implementacyjne (nie ciche założenia)

### 1. Margines ostrzegawczy w β(Q)

Stary `compute_beta` (przed 2026-09-12) był funkcją skokową: `β=1.0`
dokładnie dla każdego `Q≤Q_crit`. "`β∈(0.8,1.0)` PRZED przekroczeniem
progu" (Klasa II) było więc matematycznie nieosiągalne.

**Poprawka** (uzgodniona z użytkownikiem — wybrał "dodaj miękki
margines przed progiem"): `compute_beta` dostał parametr
`anticipation_fraction`. Definiuje efektywny próg
`Q_eff_crit = Q_crit - anticipation_fraction·(1-Q_crit)`, poniżej
którego β zaczyna łagodnie spadać. **Wartość `0.05`, nie zgadnięta** —
wyliczona algebraicznie tak, żeby na progu `Q=Q_crit` JEDNOCZEŚNIE:
`β(Q_crit)=0.9524∈(0.8,1.0)` ORAZ `S_up%(Q_crit)=4.76%<5%` — pierwsza
próbowana wartość (`0.1`) dawała `β=0.909` (spełnia pierwszy warunek)
ale `S_up%=9.09%` (**łamie** drugi). Sprawdzone bezpośrednio przed
przyjęciem `0.05` jako domyślnej.

Ważne: to NIE zmienia, kiedy operator `theta_bifurcation()` faktycznie
modyfikuje sygnał (twardy próg `Q≤Q_crit → brak ingerencji` zostaje bez
zmian, osobno testowany) — margines dotyczy wyłącznie diagnostyki/
klasyfikacji.

### 2. Pominięcie det(K)

Sprawdzone bezpośrednio (różnice skończone na faktycznym update-mapie
`G,S` z `run_sg_coupling_simulation_v2`): Jakobian
`∂(G_new,S_new)/∂(G_old,S_old)` ma kolumnę `G_old` tożsamościowo zerową
w KAŻDYM punkcie — `G=R0+α·S²` jest jednokierunkowym odczytem z `S`, `G`
nigdy nie wpływa z powrotem na dynamikę. Skutek: `det(K)=0` WSZĘDZIE,
niezależnie od `Q`/`α`/`bump` — nie rozróżnia żadnej strefy od innej.

**Decyzja użytkownika (2026-09-12)**: `det(K)` NIE jest używane w tym
klasyfikatorze dla tego konkretnego toy-modelu. `K` (z `gs_matrix.py`)
pozostaje osobnym, niepołączonym numerycznie obiektem (macierz dla
NIEZALEŻNEGO układu `dV/dt=KV`), nie wielkością obliczalną z trajektorii
`(G(t),S(t))` tej symulacji bez większej zmiany modelu (nadania `G`
własnej dynamiki ze sprzężeniem zwrotnym od `S`) — taka zmiana nie
została wprowadzona bez wyraźnej prośby.

### 3. Niespójność granic Klasy II/III — β jako jedyny dyskryminator

Znalezione przy implementacji (nie było częścią wcześniejszej dyskusji
z użytkownikiem — odnotowane tu wprost):

- **`Q>Q_crit` NIE gwarantuje `β<0.5`.** Między `Q_crit` a głębokim
  przekroczeniem istnieje cały zakres, w którym `Q>Q_crit`, ale
  `β` wciąż `≥0.5` — to dokładnie "strefa miękka" z
  `test_sg_coupling_phase_diagram.py`. Taki punkt nie spełniałby
  dosłownie ani warunku Klasy II (`Q>Q_crit`), ani Klasy III
  (`β≥0.5`), gdyby oba warunki (Q vs Q_crit, i β vs próg) traktować
  jako niezależne, równorzędne bramki.
- **`S_up≥20%` (czyli `β≤0.8`) i `β<0.5` to DWIE różne granice.**
  Punkt o `β=0.7` ma `S_up%=30%≥20%`, ale nie ma `β<0.5`.

**Rozwiązanie**: `β` jest jedynym, autorytatywnym dyskryminatorem granic
klas — bo jest jedyną wielkością wspólną wszystkim trzem opisom, i bo
granica `β<0.5` była już wcześniej ustalona i matematycznie uzasadniona
w `test_sg_coupling_phase_diagram.py` jako punkt równowagi wag kanałów
(`β=1-β` dokładnie przy `β=0.5`). `Q` vs `Q_crit` i `S_up%` są
raportowane jako wielkości OPISOWE/DIAGNOSTYCZNE, nie niezależne bramki:

```
Klasa I:   beta == 1.0 DOKŁADNIE   (Q <= Q_eff_crit, zero reakcji)
Klasa II:  0.5 <= beta < 1.0        (modulujące - obejmuje ZARÓWNO
                                     "blisko progu od dołu" JAK I
                                     "lekkie przekroczenie od góry")
Klasa III: beta < 0.5              (ten sam próg co w phase diagram)
```

## Połączenie z mapą faz (phase diagram)

`test_sg_coupling_phase_diagram.py` klasyfikuje CAŁE kombinacje
`(alpha, anomaly_bump)` w jedną z 4 stref (martwa/cicha/miękka/twarda) -
werdykt na poziomie CAŁEGO przebiegu. `signal_class.py` klasyfikuje
KAŻDY KROK czasowy z osobna. Te dwie warstwy NIE są identyczne:

| Strefa (phase diagram)                | Typowa klasa sygnału w oknie anomalii |
|----------------------------------------|----------------------------------------|
| martwa (`Q_crit>1`, konfiguracja nieprawidłowa) | brak — pytanie o klasę nie ma sensu |
| cicha (cutoff nigdy się nie wyzwala)   | prawie zawsze I — **ale patrz zastrzeżenie niżej** |
| miękka (`beta_min≥0.5`)                | II (zweryfikowane: `test_trace_reaches_class_II_or_III_during_anomaly_soft_mode`) |
| twarda (`beta_min<0.5`)                | III (zweryfikowane: `test_trace_reaches_class_III_during_anomaly_hard_mode`) |

**Zastrzeżenie, sprawdzone bezpośrednio, nie założone**: strefa "cicha"
(cutoff nigdy się nie wyzwala, `Q` nigdy nie przekracza `Q_crit`) NIE
znaczy "zawsze Klasa I" — `Q` może wejść w margines ostrzegawczy
`[Q_eff_crit, Q_crit]` BEZ przekroczenia `Q_crit`, dając chwilowo Klasę
II. Zweryfikowany przykład: `alpha=0.1, anomaly_bump=1.5` — cutoff nigdy
się nie wyzwala (nadal "cicha" wg phase diagram, `Qmax=0.4776 < Q_crit=0.4873`),
ale 15 z 1000 kroków symulacji rejestruje Klasę II (bo `Q` wszedł w
`[Q_eff_crit≈0.4616, Q_crit≈0.4873]`). Dla porównania: `anomaly_bump=1.3`
daje czystą Klasę I przez cały przebieg (`Qmax=0.4538`, poniżej
`Q_eff_crit`). Innymi słowy: "cicha" (phase diagram) = "prawie zawsze I,
z możliwymi krótkimi wizytami w II blisko granicy", nie "zawsze
dokładnie I".

## Integracja z MetaState (Λ,τ,ρ,J) — pełny łańcuch pipeline'u

**Dodane 2026-09-12**, na wyraźne zlecenie użytkownika, po opisaniu
pełnego łańcucha: `sygnał → SG-Coupling → Θ_bif → klasa I/II/III →
MetaState → faza systemu`. Do tego momentu klasy I/II/III i MetaState
z gałęzi META-DYNAMICS były dwoma rozłącznymi mechanizmami w osobnych
repo — [`timdr_formalism/signal_meta_bridge.py`](../../timdr_formalism/signal_meta_bridge.py)
jest pierwszym rzeczywistym wiązaniem między nimi (siódma domenowa
instancja MetaState w tym ekosystemie, po sześciu opisanych w
`GIA-TIMDR/docs/theory/TIMDR_Branch_Specification.md`).

Sygnał dzielony jest na rozłączne okna czasowe (partycja, nie okno
przesuwne); każde okno agregowane jest do jednego `MetaState`:

| Kanał | Wzór | Zależy wyłącznie od |
|---|---|---|
| Λ (struktura) | `std(Q_okno) / (std(Q_okno) + |mean(Q_okno)| + ε)` | `Q` |
| τ (transformacja) | `mean(|Δβ_okno|) / dt_krok` | `β` |
| ρ (anomalia) | frakcja kroków w oknie z klasą III | klasy (czyli `β`) |
| J (rezonans/sprzężenie) | `mean(|N_okno| / (max|N_okno| + ε))` | `N = S_down·S_up` |

`ρ` i `J` zależą od dwóch RÓŻNYCH wielkości źródłowych (klasa vs `N`)
celowo — gdyby `J` było zdefiniowane np. jako "frakcja kroków z
`cutoff=True`", byłoby z KONSTRUKCJI nadzbiorem `ρ` (Klasa III wymaga
`cutoff=True`), co dałoby gwarantowaną korelację zamiast empirycznego
wyniku do sprawdzenia.

**Wynik na trybie miękkim vs twardym (zweryfikowany bezpośrednio,
`tests/test_signal_meta_bridge.py`, 20 okien po `window_size=50` kroków
każdy):**

| | tryb miękki | tryb twardy |
|---|---|---|
| mean(ρ) | `0.0` (dokładnie — nigdy nie osiąga Klasy III) | `~0.013` |
| mean(J) | `~0.001` | `~0.019` (≈19×) |
| faza "stabilna" | 11/20 okien | 2/20 okien |
| faza "przejściowa" | 5/20 okien | 14/20 okien |
| faza "krytyczna" | 3/20 okien | 3/20 okien — **identycznie** |

**Uczciwie odnotowany wynik częściowy** — dokładnie ten sam wzorzec co
w pozostałych sześciu domenach META-DYNAMICS: mechanizm reaguje na
różnicę reżimów w oczekiwanym kierunku (mniej "stabilna", więcej
"przejściowa" w trybie twardym), ale próg "krytyczna" (dziedziczony bez
zmian z oryginalnego szkicu META-DYNAMICS, `magnitude(M) ≥ 1.0`) NIE
rozdziela reżimów — liczba okien "krytyczna" jest identyczna w obu
trybach. Progi `0.1`/`1.0` są arbitralne/nieskalibrowane na skali tego
konkretnego sygnału (tak jak w Quantum-Lattice i pozostałych domenach)
— **mechanizm działa, progi nie są skalibrowane**, nie jest to ukrywane
ani przerabiane na wynik lepszy niż jest.
