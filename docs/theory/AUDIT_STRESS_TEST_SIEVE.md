# Audyt: stres-test sita (`timdr_formalism.pipeline`) sygnałami adwersarialnymi

> Nie jest to test hipotezy o TIMDR (jak `PREREG_*`/`RESULT_*` z serii
> mostu M/S↔topologia) — to test odporności WŁASNEGO KODU, w duchu
> wcześniejszych audytów tej sesji (`test_operators_wiring.py`, phase
> diagram SG-Coupling, które znalazły realny błąd przepełnienia
> `R_phase[S]`). Propozycja użytkownika: nakarmić sito sygnałami
> sztucznymi/ekstremalnymi i zobaczyć efekt przepełnienia. Kod:
> `core/stress_test_sieve.py`. Data: 2026-09-15.

## A) Kalibracja sita pod czystym zerem — sito jest BARDZIEJ konserwatywne niż nominalne α

Test: trzy generatory o IDENTYCZNYM rozkładzie (biały szum, ten sam
`sigma`) podstawione jako pozytywny/negatywny A/negatywny B —
genuine zerowy efekt z konstrukcji. `passed` (fałszywy alarm całego
sita) powinno wychodzić z częstością ok. `α·(1-α)=0,0475` (5% szansy,
że test pozytywny wyjdzie istotny × 95% szansy, że test negatywny NIE
wyjdzie istotny), gdyby oba testy wewnętrzne były niezależne.

**Wynik: 0/200 przebiegów dało `passed=True`.** Statystycznie bardzo
nieprawdopodobne, gdyby prawdziwa częstość wynosiła 4,75%
(`P(0 sukcesów w 200 | p=0,0475) ≈ 7,5×10⁻⁵`) — czyli to NIE jest
przypadek, to realna własność konstrukcji.

**Zdiagnozowane wprost, nie zgadnięte**: pojedynczy test pozytywny
(porównanie `pos` vs `neg_a`) SAM w sobie zachowuje się zgodnie z
oczekiwaniem — w kontrolnym przebiegu 50 powtórzeń dał `p<0,05` w 2/50
(4%), blisko nominalnego 5%, bez zagęszczenia identycznych wartości
(30 unikalnych wartości metryki na 30 okien — brak remisów
zniekształcających test). Przyczyna niższej niż oczekiwana częstości
`passed` leży w KONSTRUKCJI `run_controls()`: próbka `neg_a` jest
używana w OBU testach wewnętrznych (test pozytywny: `pos` vs `neg_a`;
test negatywny: `neg_a` vs `neg_b`) — więc gdy `neg_a` wypadnie
nietypowo (czysto losowo), ma tendencję do jednoczesnego „wygenerowania”
istotności w OBU testach naraz (bo różni się od obu pozostałych grup
w podobnym kierunku), a nie tylko w jednym — a `passed` wymaga
DOKŁADNIE jednego z nich istotnego, drugiego nie. Ta korelacja
strukturalna (współdzielona próbka `neg_a`) obniża częstość fałszywych
alarmów CAŁEGO sita poniżej naiwnego wyliczenia z niezależności.

**Wniosek**: sito jest, jeśli już, BARDZIEJ konserwatywne niż jego
nominalne `α` sugerowałoby w prostym rachunku — dobra, bezpieczna
własność, nie wada. To też liczbowo tłumaczy, czemu w całej serii
mostu M/S↔topologia (50 komórek, `α=0,05`) zaobserwowaliśmy tylko
1 formalne „przejście” (homologia perzystentna, i tak odrzucone jako
niewiarygodne) — realna częstość fałszywych alarmów całego sita jest
niższa niż naiwne `n×α`.

## B) Bateria 12 sygnałów adwersarialnych × 5 metryk — brak awarii krytycznych, ale realne ryzyko ciche

Żadna kombinacja nie spowodowała przepełnienia numerycznego
(`OverflowError`) ani zawieszenia programu. Trzy realne, warte
odnotowania znaleziska:

### B1. `h1_total_persistence_fn` (homologia) rzuca JAWNY, czytelny wyjątek na NaN/Inf

Dla `nan_injected`, `inf_injected`, `all_nan`: `ripser` sam odmawia
policzenia czegokolwiek i podnosi `ValueError: Input contains NaN` —
**to jest DOBRE zachowanie**: głośna, jednoznaczna awaria zamiast
cichego złego wyniku.

### B2. `torsion_max|τ|`, `winding_number`, `crossing_number` CICHO ignorują NaN/Inf i zwracają `0.0`

Dla tych samych trzech sygnałów (`nan_injected`, `inf_injected`,
`all_nan`) pozostałe trzy metryki NIE rzucają wyjątku — wewnętrzne
filtrowanie `~np.isnan(...)` po cichu odrzuca skażone próbki i liczy
wynik z tego, co zostało, zwracając wartość wyglądającą jak normalny,
niski wynik (`0.0`). **To jest realne ryzyko przy przyszłym
zastosowaniu do prawdziwych danych**: prawdziwe szeregi M/S (sejsmika,
łożyska) miewają luki/braki/błędne odczyty (dokładnie problem
znaleziony wcześniej w `trefoil_weather_embedding_validation.py`,
artefakt luk w próbkowaniu) — te trzy metryki NIE poinformują, że okno
było uszkodzone, po prostu zwrócą liczbę tak, jakby dane były czyste.
Nie jest to naprawione teraz (to byłaby zmiana zachowania po fakcie,
nie stres-test) — jest to udokumentowane jako znane ograniczenie do
uwzględnienia, gdyby ktoś kiedyś wracał do tej rodziny metryk na
realnych danych: **wymagana byłaby jawna walidacja braków (np.
`np.any(np.isnan(x))` na wejściu, z odrzuceniem okna) przed
zaufaniem wynikowi**.

### B3. `phase_winding_fn` propaguje NaN w PRZEWIDYWALNY sposób (nie cicho jak B2, nie głośno jak B1)

Dla `nan_injected`/`inf_injected`/`all_nan`: zwraca `nan` wprost
(`finite=False`) — nie crashuje, ale też nie udaje normalnego wyniku
jak `0.0`. To trzeci, pośredni tryb. Sprawdzone przez pipeline (patrz
sekcja C): `nan < alpha` i `nan >= alpha` są OBIE `False` w Pythonie —
więc `pos_ok=False` i `neg_ok=False` jednocześnie, co przez przypadek
(nie przez jawną walidację) ląduje w gałęzi „metryka jest zepsuta” w
`run_controls()`. Działa poprawnie, ale **przez niezamierzoną
własność porównań NaN, nie przez jawne sprawdzenie** — krucha
poprawność, nie zaprojektowana odporność.

### B4. Wydajność: `h1_total_persistence_fn` i `crossing_metric_fn` NIE skalują się do dużych okien

Dla `very_long_n5000`: `h1_total_persistence_fn` zajęła **22,5 sekundy**
na JEDNO wywołanie (filtracja Vietorisa-Ripsa rośnie szybko z liczbą
punktów), `crossing_metric_fn` — 3,5 sekundy (macierz par O(n²)).
Reszta (`torsion`, `winding`, `phase_winding`) pozostaje szybka nawet
przy n=5000 (<1s). **Praktyczne ograniczenie do odnotowania**: gdyby
ktoś chciał kiedyś zastosować most homologii perzystentnej do okien
dłuższych niż ~kilkaset próbek, potrzebna byłaby zupełnie inna
strategia obliczeniowa (subsampling, przybliżone metody) — przy
pełnej siatce (30 okien × wiele wariantów) czas eksplodowałby do
niepraktycznych rozmiarów.

### B5. Brak przepełnienia przy ekstremalnych amplitudach

`huge_amplitude_1e150` i `tiny_amplitude_1e-150` — wszystkie 5 metryk
zwróciły skończone, sensowne wartości. Normalizacja `(x-mean)/std`
zastosowana na wejściu każdej metryki (amendment wprowadzony już przy
poprzednich mostach) okazuje się skutecznie chronić przed
przepełnieniem skali, dokładnie tak, jak była zaprojektowana.

## C) Zdegenerowany `metric_fn` wprost przez `run_controls()` — sito NIE daje się oszukać

Trzy patologiczne „metryki” (stała, zawsze-NaN, losowa niezwiązana z
danymi) przepuszczone przez pełny `run_controls()`:

| metryka | wynik | trafna diagnoza sita? |
|---|---|---|
| stała `42.0` niezależnie od danych | `passed=False`, „metryka za mało czuła” | TAK |
| zawsze `NaN` | `passed=False`, „metryka jest zepsuta” | TAK (przez przypadek semantyki NaN, patrz B3) |
| losowa, kompletnie niezwiązana z wejściem | `passed=False`, „metryka za mało czuła” (pos_p=0,093, neg_p=0,73) | TAK |

**Żadna z trzech patologicznych metryk nie oszukała sita** — we
wszystkich trzech przypadkach `run_controls()` poprawnie zgłosił, że
metryka nie nadaje się do użytku, z sensowną diagnozą przyczyny.

## Wniosek zbiorczy

„Efekt przepełnienia” w rozumieniu awarii numerycznej (przepełnienie
`float`, crash, zawieszenie) **nie wystąpił w żadnej z 60 kombinacji
sygnał×metryka**. Znaleziono za to trzy realne, warte zapamiętania
rzeczy: (1) sito jest empirycznie BARDZIEJ konserwatywne niż jego
nominalne `α` sugerowałoby naiwnym rachunkiem, dzięki strukturalnej
korelacji między dwoma testami wewnętrznymi — dobra własność; (2) trzy
z pięciu metryk CICHO ignorują skażone (NaN/Inf) dane wejściowe zamiast
zgłaszać awarię — realne ryzyko przy przyszłym zastosowaniu do
prawdziwych, dziurawych danych, nie naprawione teraz, tylko
udokumentowane; (3) homologia perzystentna i crossing number mają
praktyczne granice skalowalności (odpowiednio ~sekundy i ~dziesiątki
sekund przy n=5000), istotne dla przyszłych prób na dłuższych oknach.
