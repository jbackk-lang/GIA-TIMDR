# Pre-rejestracja: most M/S↔topologia/K na REALNYCH danych finansowych (BTC/USD 720h) + szum syntetyczny

> Trzecia domena realnych danych, po łożyskach (`RESULT_REAL_BEARING_
> NOISE_ROBUSTNESS.md`, 123/150, region jednorodny — silny efekt) i
> sejsmice (`RESULT_REAL_SEISMIC_NOISE_ROBUSTNESS.md`, 47/100, region
> niejednorodny — słabszy, kruchy efekt). Standardowa kolejność
> (freeze→build). Konstrukcja świadomie zaprojektowana pod kątem
> lekcji o jednorodności regionu pozytywnego (`AUDIT_G_COMPLEXITY_
> HYPOTHESIS.md`, kontrola 2) — region pozytywny i negatywny mają być
> jednorodne z konstrukcji, nie tylko z nadziei.
>
> **Odrębność od wcześniejszej pracy z BTC w tym ekosystemie**:
> `PREREG_MS_K_EVENTS.md` (TIMDR-Time-Formalism) używał tych samych
> danych BTC z INNĄ metodologią (okna zdarzeń, most Fouriera Δt·Δf) i
> — jak ustalono w audycie źródeł danych tej sesji — bez odtwarzalnego
> skryptu (liczby ad hoc). Ten most jest nową, niezależną konstrukcją,
> nie kontynuacją tamtej.

## 0. Dane

`deliverable_timdr_finanse/data/btcusd_1h.csv` — 720 świec godzinowych
BTC/USD, kolumny `time,open,high,low,close,volume`. Sygnał analizowany:
**logarytmiczne zwroty godzinowe** `r_t = log(close_t/close_{t-1})`,
n=719 próbek (standard w finansach — cena surowa jest niestacjonarna,
zwroty są bliższe stacjonarności, co robi normalizację `(x-mean)/std` w
`metric_fn` sensowną, a nie maskującą trend).

## 1. Definicja reżimu pozytyw/negatyw (zamrożona, obliczona z danych w sposób nieujawniający wyniku testu)

Podział na **niezachodzące bloki 24h** (24 próbki zwrotu każdy),
`n_blocks=29` (⌊719/24⌋). Dla każdego bloku liczona **zmienność
lokalna** = odchylenie standardowe zwrotów w tym bloku. Bloki dzielone
**medianą** rozkładu tych 29 wartości na dwie połowy: `WYSOKA
ZMIENNOŚĆ` (region pozytywny) i `NISKA ZMIENNOŚĆ` (region negatywny/
tło). To jest podział na reżim (stan utrzymujący się przez blok), nie
pojedyncze zdarzenie punktowe — analogicznie do łożysk (stan), nie do
sejsmiki (przejście+zanikanie).

**Kluczowa różnica projektowa względem mostu sejsmicznego (wyciągnięty
wniosek)**: okna metryki (`window_size` próbek) są losowane WYŁĄCZNIE
Z WNĘTRZA pojedynczego bloku 24h — nigdy nie przecinają granicy dwóch
bloków ani nie łączą (konkatenują) różnych bloków. To gwarantuje, że
każde okno jest w całości jednym, ciągłym, rzeczywistym fragmentem
danych z jednego reżimu zmienności — bez sztucznych artefaktów
sklejania, i bez ryzyka złapania przejścia między reżimami w jednym
oknie.

## 2. Metryki (bez zmian)

Reużyte 1:1: `torsion_max|tau|`, `winding_number`, `crossing_number`,
`h1_persistence`, `phase_winding`.

## 3. Generator: okno wewnątrz bloku + szum (zamrożone)

Dla `window_size ∈ {12, 24}`: przy `window_size=24` okno = cały blok
(brak wyboru podokna). Przy `window_size=12` blok dzieli się na dwie
NIEZACHODZĄCE połówki (pierwsza/druga), wybór połówki deterministyczny
z parzystości `seed`. Segment wybierany deterministycznie z `seed`
(modulo liczba dostępnych bloków danego reżimu). Szum gaussowski
`N(0, sigma_frac·std(segment))` dodany PO wyborze segmentu, identyczna
konstrukcja co w poprzednich dwóch mostach na realnych danych.

## 4. Siatka (zamrożona)

`WINDOW_SIZES=(12,24)`. `SIGMAS=(0.0,0.1,0.3,0.5,1.0)` — ułamek
własnego std segmentu, identyczna siatka nominalna co we wszystkich
poprzednich mostach. `N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05`.

Liczba dostępnych bloków per reżim będzie policzona PRZED uruchomieniem
(mediana z 29 bloków daje ~14-15 na reżim) — przy `window_size=24`
oznacza to silne reużycie (14-15 < 30, disclosed jak poprzednio); przy
`window_size=12` dostępnych jest 2× więcej sub-okien (~28-30),
reużycie minimalne lub żadne.

Łącznie: 5 metryk × 2 okna × 5 sigm = **50 komórek** (jeden instrument,
BTC/USD — bez podziału na "stacje"/"typy defektu" jak w poprzednich
dwóch mostach, bo mamy tylko jeden szereg cenowy).

## 5. Oczekiwania a priori — PRZED uruchomieniem

**Pesymistyczne co do interpretacji, umiarkowanie optymistyczne co do
surowego wyniku.** Region pozytywny jest tu zaprojektowany jako
jednorodny (lekcja z sejsmiki) — więc oczekuję wyniku BLIŻSZEGO
łożyskom (silny, odporny na szum) niż sejsmice (słaby, kruchy), pod
warunkiem że hipoteza o roli jednorodności (potwierdzona w kontrolowany
sposób w `AUDIT_G_COMPLEXITY_HYPOTHESIS.md`) faktycznie uogólnia się na
NOWĄ, trzecią domenę — to jest właśnie testowane, nie zakładane.
Zastrzeżenie: "wysoka zmienność" w finansach nie musi oznaczać tej
samej klasy zjawiska fizycznego co "defekt mechaniczny" — reżim
zmienności może mieć zupełnie inny mechanizm (np. grubsze ogony
rozkładu zwrotów, autokorelacja zmienności/GARCH) niż impulsowość
łożysk. Kontrola porównawcza z kurtozą i entropią widmową (jak w
`AUDIT_G_COMPLEXITY_HYPOTHESIS.md`) zostanie wykonana PO głównym
wyniku, tak jak poprzednio.
