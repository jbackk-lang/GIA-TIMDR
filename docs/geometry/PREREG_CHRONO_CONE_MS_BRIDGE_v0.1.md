# Pre-rejestracja: chrono_cone_ratio — most M/S↔G przez Chronoproces (peak-referenced phase + anomalia jako promień)

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> danych (nawet syntetycznych — kod jeszcze nie napisany w chwili
> zapisania tego dokumentu). Data: 2026-09-21. Szósty kandydat w
> rodzinie mostów M/S↔topologia/G (po torsji, winding/crossing,
> homologii perzystentnej, phase_winding OAM — punkt 19 skilla), ale
> KONSTRUKCYJNIE inny: pierwszy, który jawnie przechodzi przez
> formalizm Chronoprocesu Ξ=(T,x,Γ,φ) (`docs/theory/
> TIMDR_Chronoprocess.md`) zamiast embeddingu opóźniającego Takensa.

## 0. Skąd to się bierze

Propozycja użytkownika (parafraza): potraktujmy sygnał M/S
"timdr-owsko" — SZCZYT (lokalne maksimum) generuje SKRĘT (fazę/obrót),
SZUM/ANOMALIA (już istniejący obiekt M/S, §2 skilla: `|x-mean|>k·std`)
determinuje PROMIEŃ, a brakująca oś (skalar sam z siebie nie rotuje)
to CZAS, czytany przez Chronoproces. Fizycznie normalne (nie-anomalne)
obroty mają dawać kształty LEJOWATE (stożkowe).

**Uzasadnienie, czemu to mieści się w kategorii "znana technika" (jak
most Fouriera), nie "nowa hipoteza"**: liczenie fazy względem kolejnych
lokalnych ekstremów ("peak-referenced phase") jest znaną, pokrewną
odmianą unwrapowania fazy w DSP — prostszą i bardziej odporną na szum
wieloskładnikowy niż faza Hilberta (`phase_winding`, punkt 19 skilla),
bo nie wymaga transformaty analitycznej ani zakłada wąskopasmowości.
Zgodnie z zasadą punktu 15 skilla ("gdy propozycja łączy >2 gałęzie
naraz lub nie ma uzasadnienia analogicznego do mostu Fouriera —
zaflaguj") ten most łączy DWIE gałęzie (M/S→r, M/S→θ) plus WYŁĄCZNIE
trzecią, formalnie już istniejącą oś T Chronoprocesu jako oś z — nie
jest to nowa hipoteza matematyczna, tylko nowa kombinacja istniejących,
audytowanych obiektów (anomalia z §2, peak-referenced phase jako
technika DSP).

## 1. Audyt nazw PRZED użyciem (zgodnie z punktem 6 protokołu)

- `funnel_ratio`/`phasespace_funnel_ratio` już istnieje w
  **TIMDR-fusion-tools** (plazma tokamaka TCABR) — **NIEZWIĄZANY**
  projekt, inna domena fizyczna. Metryka poniżej jest NAZWANA INACZEJ
  (`chrono_cone_ratio`) właśnie żeby uniknąć kolizji nazwy między
  niepowiązanymi obiektami (punkt 15 skilla) — to jest NOWY, niezależny
  obiekt, TYLKO koncepcyjnie inspirowany (kształt "pierwszy fragment
  okna vs ostatni fragment okna"), kod NIE jest łączony ani kopiowany,
  wynik z tamtego repo NIE jest zakładany jako przenoszący się tutaj.
- `anomalia` (`|x-mean|>k·std`, boolean) — istniejący, audytowany obiekt
  M/S (`TIMDR-Math-Formalism/timdr_formalism/chronosignal.py::
  anomalia_flags`). `r(t)` poniżej jest tej samej wielkości CIĄGŁĄ
  wersją (`|x-mean|/std`, bez progowania) — jawnie nazwane jako
  rozszerzenie z boolean na ciągłą skalę, nie nowa definicja anomalii.
- "skręt" — NIE używam tego słowa dla θ(t) w kodzie/nazwach zmiennych
  (już 8 kolizji symbolu wg punktu 2 skilla); nazywam to "peak-referenced
  phase" / `theta`, żeby nie dodawać dziewiątej.
- Chronoproces Γ — patrz §4 niżej, jawne uproszczenie odnotowane.

## 2. θ(t) — peak-referenced phase (zamrożone)

1. Wygładzenie: `xs = moving_average(x, smooth_window)`, okno
   **`smooth_window=5`** (nieparzyste, centrowane, brzegi metodą "edge"
   paddingu). **Uwaga o wyborze wartości**: nie znaleziono w tym repo
   potwierdzonego, wcześniejszego użycia konkretnej stałej
   `smooth_window=51` do zweryfikowania grepem w czasie dostępnym w tej
   sesji (przeszukanie części drzewa repo nie trafiło na taki wzorzec)
   — zamiast zgadywać/kopiować niepotwierdzony precedens, `5` jest
   NOWĄ, jawnie uzasadnioną wartością: rozmiary okien tego mostu (§5)
   są rzędu dziesiątek-setek próbek z oscylacją o okresie rzędu ~15
   próbek (§3), więc okno wygładzania musi być WYRAŹNIE mniejsze niż
   okres, inaczej wygładzenie samo eliminuje szczyty. `5` << 15 spełnia
   to przy minimalnym filtrowaniu pojedynczych próbek szumu.
2. Szczyty: ścisłe lokalne maksima `xs[i]>xs[i-1] and xs[i]>xs[i+1]`,
   tylko punkty wewnętrzne (bez zawijania na brzegach okna).
3. Jeśli liczba szczytów < 2 → θ(t) **NIEZDEFINIOWANE** dla tego okna
   (zwraca `NaN`, nie 0 — zero byłoby fałszywym "brak rotacji", NaN
   jawnie mówi "za mało struktury, żeby ocenić"). To jest oczekiwana,
   jawnie obsłużona sytuacja przy krótkich oknach/szumie bez struktury,
   nie błąd.
4. Między kolejnymi szczytami `p_k`, `p_{k+1}`: faza rośnie LINIOWO od
   `2πk` do `2π(k+1)` (interpolacja liniowa indeksu próbki). Przed
   pierwszym szczytem: faza=0 (płasko). Po ostatnim szczycie: faza
   zamrożona na `2π(n_peaks-1)` (płasko — brak podstawy do
   ekstrapolacji kolejnego szczytu). Jeden szczyt = jeden pełny "skręt"
   w sensie użytkownika (2π), zgodnie z propozycją.

## 3. r(t) — promień z anomalii (zamrożone, wybór uzasadniony PRZED danymi)

```
r(t) = |x(t) - mean(x_window)| / std(x_window)
```

Wybrana **wprost jako ciągła wersja `anomalia_flags()`** (§1 wyżej) —
nie nowa definicja, tylko usunięcie progu `k` z istniejącego obiektu
gałęzi M/S. Alternatywa rozważona i odrzucona: odchylenie od
`rolling_median` znormalizowane `rolling_std` (lokalne, nie globalne) —
odrzucona, bo wprowadzałaby DRUGI wolny parametr (rozmiar okna
rolującego) obok już istniejącego `smooth_window`, bez wyraźnej
potrzeby przy oknach tej wielkości (§5, rzędu 48-1024 próbek — globalna
znormalizowana anomalia jest tu wystarczająco lokalna). Przy `std==0`
(sygnał stały): `r(t)=0` wszędzie (zgodnie z konwencją
`anomalia_flags()` dla tego przypadku brzegowego).

## 4. z(t) — trzecia oś: Chronoproces, jawnie uproszczony (zamrożone)

`docs/theory/TIMDR_Chronoprocess.md` §3 definiuje rzut G jako
`Γ:T×I→ℝ³` — RODZINĘ trajektorii `{γ_s}_{s∈I}`, bo pojedyncza
trajektoria 1D nie ma operatora kształtu (błąd kategorii, nazwany
wprost w genezie tamtego dokumentu). Ten most **NIE buduje pełnej
rodziny/kongruencji** — używa NAJPROSTSZEJ możliwej interpretacji: `I`
jednoelementowe, `{γ}` = pojedynczy obserwowany przebieg,
`z(t)=Γ(t,s₀)=t`. To jest **jawnie nazwane uproszczenie**, nie
implementacja `chronocongruence.py` (`TIMDR-Geometry-Formalism`) — nie
twierdzę, że krzywa 3D poniżej jest "powierzchnią" w sensie Aksjomatów
G3/G8/G9. Oś z to dosłownie indeks próbki w oknie (`t=0..n-1`), potrzebny
WYŁĄCZNIE po to, żeby (r,θ) (skalar+faza, z natury 2D/płaskie) miało
trzeci wymiar do rotacji — zgodnie z uwagą użytkownika, że "skalar sam z
siebie nie rotuje".

## 5. Krzywa 3D i metryka `chrono_cone_ratio`

```
p(t) = (r(t)·cos θ(t), r(t)·sin θ(t), t),  t = 0..n-1
```

**`chrono_cone_ratio`** (NOWA nazwa, patrz audyt §1 — NIE
`funnel_ratio`): dla zamrożonego `edge_fraction=0.2` (20%),
`n_edge=max(2, round(0.2·n))`:

```
r_start = mean(r(t) dla t w pierwszych n_edge próbkach)
r_end   = mean(r(t) dla t w ostatnich n_edge próbkach)
chrono_cone_ratio = r_end / r_start   (NaN jeśli r_start < 1e-9 lub θ niezdefiniowane)
```

`ratio > 1` → lej ROZSZERZAJĄCY się (promień anomalii rośnie z
czasem); `ratio < 1` → lej ZWĘŻAJĄCY się; `ratio ≈ 1` → cylinder (brak
leja). **Jawnie odnotowane**: `NaN` jest osobnym, trzecim wynikiem
(niezdefiniowane), NIE traktowanym jako `ratio=1` — komórki siatki z
dużym odsetkiem `NaN` (mało szczytów) będą raportowane jako
INCONCLUSIVE z powodu braku mocy (zgodnie z punktem 15 skilla: wysokie
p ≠ brak efektu, gdy brak zdarzeń kwalifikujących się do testu),
nie po cichu odrzucane/zerowane.

## 6. Kontrole syntetyczne (zamrożone, PRZED implementacją)

Wspólne dla (a)/(b)/(c): `t=arange(n)`, `w=2π/15` (okres≈15 próbek —
wybrany tak, żeby okna z §7 dawały WIELE pełnych okresów, potrzebne dla
stabilnego liczenia szczytów, w odróżnieniu od poprzednich pięciu
mostów, które nie wymagały wielu okresów w oknie).

- **(a) POZYTYWNA — amplituda rosnąca w czasie**:
  `x(t) = (1 + 0.05·t)·sin(w·t) + N(0, 0.15²)`. Przewidywanie PRZED
  uruchomieniem: `chrono_cone_ratio` istotnie WYŻSZY niż tło (a),
  mediana wyraźnie > 1 (lej rozszerzający).
- **(b) NEGATYWNA A — czysty szum biały**: `x(t) = N(0, 1.0²)`, brak
  struktury okresowej. Przewidywanie: `chrono_cone_ratio` bliski 1
  (brak systematycznego trendu amplitudy) ORAZ wysoki odsetek `NaN`/
  niestabilne liczenie szczytów (szum nie ma prawdziwego oscylatora —
  liczba "szczytów" zależy od przypadku, nie od struktury).
- **(c) NEGATYWNA B — stacjonarna oscylacja, STAŁA amplituda**:
  `x(t) = 1.0·sin(w·t) + N(0, 0.15²)` (ten sam `w` i poziom szumu co
  (a), ale BEZ wzrostu amplitudy). Przewidywanie: `chrono_cone_ratio`
  bliski 1 (cylinder, NIE lej) — to jest kontrola odróżniająca "lej" od
  "zwykła oscylacja", zgodnie wprost z propozycją użytkownika.

**Mapowanie na `pipeline.run_controls()`** (ta sama funkcja co
poprzednich pięć mostów): `positive_injector=(a)`,
`negative_generator_a=(b)`, `negative_generator_b=(c)`. Test
POZYTYWNY: (a) vs (b) — oczekiwana ISTOTNA różnica (p<α), duży rozmiar
efektu, kierunek `median(a) > median(b)`. Test NEGATYWNY: (b) vs (c) —
oczekiwany BRAK istotnej różnicy (obie blisko ratio≈1, mimo różnych
mechanizmów) — **jeśli (b) i (c) OKAŻĄ SIĘ istotnie różne, to sam w
sobie ważny wynik** (oznaczałoby, że biały szum i czysta oscylacja o
stałej amplitudzie NIE są nieodróżnialne tą metryką — zgłoszone wprost,
nie ukryte, niezależnie czy pomaga czy szkodzi hipotezie).

**Obsługa `NaN` w bramce kontrolnej**: jeśli >50% wartości w
którejkolwiek z trzech grup (a/b/c) to `NaN` — kontrola oznaczona jako
NIEROZSTRZYGNIĘTA z powodu mocy (nie automatyczny fail/pass), wartości
`NaN` usuwane przed testem Manna-Whitneya, liczba pozostałych
(`n_valid`) raportowana jawnie obok wyniku.

## 7. Siatka syntetyczna (zamrożona)

`WINDOW_SIZES=(128, 256)` — celowo WIĘKSZE niż siatki poprzednich pięciu
mostów (32-300, w tym okna rzędu kilkunastu-kilkudziesięciu próbek) —
**jawna, uzasadniona zmiana mechanizmu**: peak-referenced phase +
porównanie brzeg-do-brzegu potrzebuje WIELU pełnych okresów oscylacji w
oknie (inaczej liczba szczytów jest za mała, żeby `edge_fraction=0.2`
miało sens), w odróżnieniu od poprzednich metryk (embedding + jedna
liczba na całe okno). To NIE jest dostrajanie po zobaczeniu wyniku —
decyzja podjęta z analizy wymagań mechanizmu PRZED uruchomieniem
czegokolwiek.

`N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05` — bez zmian względem konwencji
repo.

## 8. Realne dane (zamrożone — te same trzy domeny co poprzednich pięć mostów)

**Ważne zastrzeżenie o rozmiarach okien**: z tego samego powodu co §7,
okna dla tego mostu są WIĘKSZE niż w poprzednich pięciu mostach na
realnych danych (`PREREG_REAL_{BEARING,SEISMIC,BTC}_NOISE_ROBUSTNESS.md`)
— zamrożone tutaj z tego samego uzasadnienia strukturalnego (potrzeba
wielu okresów na okno), NIE po zobaczeniu żadnego wyniku na realnych
danych.

1. **Łożyska CWRU** (`TIMDR-Industrial-Predict/data/cwru_bearing/`,
   4 pliki, 1536 próbek każdy, jak w poprzednich mostach):
   `normal_1797_de_first1536.csv` (zdrowe) vs `ir_0021_...csv`,
   `or6_0021_...csv`, `b_0021_...csv` (trzy typy defektu, trzy
   niezależne przebiegi). `WINDOW_SIZES=(256, 512)` → 6/3 dostępnych
   segmentów na plik (< `N_WINDOWS=30` → silne reużycie, odnotowane
   jak w poprzednich mostach, kolumna `reuse`).
2. **Sejsmika Ridgecrest 2019** (`TIMDR-Earthquake-Core/data/
   ridgecrest_2019/real_waveform_CLC_RIO/{CLC_HHZ,RIO_HHZ}.csv`,
   100Hz, `event_idx=6004` — ten sam wzór obliczenia z
   `PREREG_REAL_SEISMIC_NOISE_ROBUSTNESS.md §0`, niezmieniony): region
   tła `[0,6004)`, region kody `[6004,36001)`. `WINDOW_SIZES=(512,
   1024)` → tło 11/5 segmentów, koda 58/29 segmentów. Dwie stacje,
   niemieszane.
3. **BTC/USD** (`deliverable_timdr_finanse/data/btcusd_1h.csv`,
   zwroty logarytmiczne godzinowe, n=719). **Odstępstwo od poprzedniego
   mostu, zamrożone tutaj z uzasadnieniem strukturalnym**: poprzedni
   most BTC dzielił na bloki 24h (dając okna 12/24 próbek) — za krótkie
   dla tego mechanizmu (okres oscylacji ~15 próbek nie mieści się
   choćby raz w oknie=12). Tutaj **`BLOCK_SIZE=48h`** (wciąż reguła
   "okno nigdy nie przecina granicy bloku", niezmieniona), `n_blocks=
   floor(719/48)=14`, podział medianą lokalnej zmienności bloku (ta
   sama metoda co poprzednio) → ~7/7 bloków wysoka/niska zmienność.
   `WINDOW_SIZES=(48,)` — JEDYNY rozmiar, cały blok (brak dzielenia na
   pół, w odróżnieniu od poprzedniego mostu, bo 24 próbki to już za
   mało). **Jawnie odnotowane ograniczenie a priori**: nawet 48 próbek
   przy nieregularnym, nieoscylacyjnym sygnale finansowym (zwroty
   godzinowe nie są z natury okresowe jak wibracje/sejsmika) może dać
   wysoki odsetek `NaN` (za mało "szczytów" o strukturze) — jeśli tak,
   będzie to zgłoszone jako INCONCLUSIVE z powodu mocy dla tej domeny,
   nie interpretowane jako potwierdzony brak leja.

Metryka: tylko `chrono_cone_ratio` (jedna metryka, w odróżnieniu od
poprzednich pięciu mostów, które porównywały kilka metryk naraz — ten
most testuje JEDNĄ, nowo zdefiniowaną wielkość).

`SIGMAS` (addytywny szum syntetyczny na wierzch realnego segmentu,
identyczna konstrukcja co poprzednie trzy mosty realne):
`(0.0, 0.1, 0.3, 0.5, 1.0)` — ułamek własnego std segmentu.
`N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05`.

## 9. Klasyfikacja wyniku (ustalona z góry)

Dla każdej domeny/pliku: test główny (realny defekt/koda/wysoka-
zmienność vs realne zdrowie/tło/niska-zmienność, przy `sigma=0.0`,
najczystszy wiersz — konwencja z poprzednich trzech mostów realnych)
+ Mann-Whitney U + rank-biserial r. **SUPPORTED** = p<0.05 i |r|≥0.3
(średni lub duży efekt) I kierunek zgodny z hipotezą leja (żaden
kierunek nie jest z góry preferowany — sam fakt istotnej,
nietrywialnej separacji jest wynikiem, kierunek raportowany opisowo).
**NOT SUPPORTED** = p≥0.05 przy wystarczającej liczbie ważnych
(nie-`NaN`) obserwacji w obu grupach (≥10 w każdej). **INCONCLUSIVE** =
zbyt mało ważnych obserwacji (<10 w którejś grupie) — brak mocy, nie
brak efektu.

## 10. Status

Zamrożone. Następny krok: implementacja dokładnie wg powyższego
(`core/chrono_cone_bridge.py`), uruchomienie NAJPIERW kontroli
syntetycznych (§6-7) — jeśli bramka kontrolna nie przejdzie zgodnie z
przewidywaniem, ZATRZYMANIE i zgłoszenie tego jako pełnoprawny wynik
negatywny na etapie mechaniki, BEZ przechodzenia do realnych danych.
Jeśli kontrole przejdą: uruchomienie na trzech domenach realnych (§8),
Mann-Whitney + rozmiar efektu, raport — łącznie z wynikiem negatywnym/
niejednoznacznym, bez retuningu po fakcie.
