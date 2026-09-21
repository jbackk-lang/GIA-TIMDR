# Pre-rejestracja: chrono_membrane_bridge — widmo macierzy korelacji między jednoczesnymi kanałami łożyska CWRU jako obiekt G (pajęczyna/membrana/kotara)

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> danych (nawet syntetycznych — kod jeszcze nie napisany w chwili
> zapisania tego dokumentu). Data: 2026-09-21. Czwarta iteracja tego
> samego wątku badawczego (po `chrono_cone_ratio` v0.1,
> `chrono_pendulum_ratio`/`net_turn` v0.2, `chrono_centrifugal_ratio`
> v0.3 — wszystkie w `docs/geometry/PREREG_CHRONO_CONE_MS_BRIDGE_v0.{1,2,3}.md`
> / `RESULT_..._v0.{1,2,3}.md`), ale ISTOTNA zmiana kierunku, nie v0.4
> tej samej konstrukcji — patrz §0.

## 0. Skąd to się bierze — diagnoza porażki v0.1-v0.3

Wszystkie trzy poprzednie wersje próbowały zbudować obiekt gałęzi G
(geometria) z JEDNEGO sygnału skalarnego (jeden kanał DE łożyska),
sztucznie "embedowanego" w 2D/3D przez fazę+promień+czas. Formalny
Chronoproces (`docs/theory/TIMDR_Chronoprocess.md` §3) definiuje rzut G
jako `Γ:T×I→ℝ³`, czytający RODZINĘ trajektorii `{γ_s}_{s∈I}` (indeksowaną
przez `s`, nie tylko czas `t`), tworzącą prawdziwą powierzchnię
`S=Γ(T×I)⊂ℝ³`. We wszystkich trzech poprzednich wersjach ta rodzina była
JAWNIE tylko "trywialną rodziną jednoelementową `{γ}`" (odnotowane wprost
w każdym z trzech PREREG-ów, §4) — czyli NIE była prawdziwą rodziną
wcale. To był błąd kategorii, nie błąd implementacji: v0.1-v0.3 różniły
się WYŁĄCZNIE sposobem liczenia fazy/promienia na TYM SAMYM
jednoelementowym `{γ}`, więc żadna z nich nie mogła w zasadzie
przetestować hipotezy o rodzinie.

Właściciel projektu trafnie zdiagnozował: **G musi się odnosić do wielu
jednoczesnych źródeł, nie jednego** — i zaproponował zmianę słownika z
"most" (jedna krzywa łącząca dwa punkty/gałęzie) na "pajęczyna/membrana/
kotara" (powierzchnia rozpięta na wielu jednoczesnych źródłach),
charakteryzowaną przez jej "widmo" (spektrum — wartości własne). Tu `s`
indeksuje KANAŁ (DE/FE/BA — patrz §2, ile jest dostępnych naraz), `t`
indeksuje próbkę czasu — to jest już PRAWDZIWA rodzina `{γ_s}_{s∈I}`,
`I` = zbiór kanałów, nie jednoelementowa.

**Wybrane źródło danych**: łożyska CWRU, wiele osi/kanałów NARAZ
(DE/FE/BA, jeśli dostępne jednocześnie w tym samym pliku/nagraniu) — nie
sejsmika, nie kombinacja, zgodnie z decyzją właściciela projektu.

## 1. Audyt nazw PRZED użyciem (punkt 6 protokołu)

- Sprawdzone grepem na CAŁYM drzewie sąsiednich repozytoriów (nie tylko
  `GIA-TIMDR`): `chrono_membrane`, `membrane_spectral_ratio`,
  `spectral_concentration`, `participation_ratio` — **zero kolizji** w
  jakimkolwiek repo. Nowe nazwy.
- **Ważne rozróżnienie od istniejącego obiektu**: `GIA-TIMDR` ma już
  ugruntowaną linię "widma Laplasjanu Möbiusa"
  (`docs/geometry/TIMDR_Mobius_Laplacian_Spectrum.md`,
  `core/mobius_kg_bridge.py`, `MobiusCoherence`, punkty 19-20 skilla) —
  to jest widmo operatora Laplace'a na SIATCE (graph Laplacian, punkty
  geometryczne + krawędzie), obiekt gałęzi K/G. Konstrukcja poniżej
  liczy widmo MACIERZY KORELACJI/KOWARIANCJI między KANAŁAMI sygnału
  M/S (nie graf, nie siatka, nie operator Laplace'a) — **inny obiekt
  matematyczny, inna macierz, inne źródło** — celowo NIE nazwany
  "Mobius"/"Laplacian" niczego, żeby nie sugerować związku, którego nie
  ma. Nazwa `chrono_membrane_bridge` odnosi się do metafory
  "membrana/kotara rozpięta na jednoczesnych źródłach" z §0, nie do
  istniejącej linii Möbiusa.
- `anomaly_radius`, `peak_referenced_phase`, `chrono_cone_ratio` (v0.1),
  `trend_referenced_phase` (v0.2) — istniejące, audytowane obiekty
  poprzednich trzech rund. Ten most NIE reużywa żadnego z nich —
  konstrukcja jest fundamentalnie inna (macierz korelacji między
  kanałami, nie faza/promień jednego kanału). Odnotowane wprost, żeby
  było jasne, że to nie jest v0.4 tej samej rodziny.
- "skręt" — jak w v0.1-v0.3, nie używane w kodzie/nazwach.

## 2. Krok 1: co jest dostępne (zbadane PRZED projektowaniem metryk)

Źródło: `docs/geometry/B4_BEARING_DATA_FREEZE.md` +
`TIMDR-Geometry-Formalism/timdr_geometry/b4_bearing_data_gate.py`
(`load_synchronous_cwru_channels`). Sparsowane bezpośrednio z plików
NPZ (`TIMDR-Industrial-Predict/data/cwru_bearing/b4_raw/source_mirror/
Data/1797 RPM/`):

| plik | klasa | kanały obecne | długość (próbki) |
|---|---|---|---|
| `1797_Normal.npz` | zdrowe (normal) | **DE, FE** (BRAK BA) | 243 938 |
| `1797_IR_21_DE12.npz` | uszkodzenie bieżni wewnętrznej (IR) | **DE, FE, BA** | 122 136 |
| `1797_OR@6_21_DE12.npz` | uszkodzenie bieżni zewnętrznej (OR@6) | **DE, FE, BA** | 122 426 |

Wszystkie trzy pliki mają wspólną oś czasu `t_i = i/12000` WEWNĄTRZ
danego pliku (§ freeze), fs=12kHz. `Normal` NIE ma kanału BA lokalnie —
to jest jawnie odnotowane ograniczenie danych, nie luka w kodzie
ładującym. Brak czwartego typu uszkodzenia (`b_0021`, kulka) jako pliku
NPZ wielokanałowego w tym repo — tylko jako CSV jednokanałowy
(`ir_0021_1797_de_first1536.csv` itp., używane w v0.1-v0.3) — ten typ
uszkodzenia jest tu POMIJANY (nie ma z czego zbudować macierzy
korelacji), odnotowane wprost, nie ukryte.

**Konsekwencja dla protokołu "uczciwe porównanie normal vs fault"**:
wspólny podzbiór kanałów dostępny jednocześnie we WSZYSTKICH trzech
plikach to **N=2 (DE, FE)** — to jest PRIMARNY test tej sesji
(normal vs IR, normal vs OR@6, N=2 kanały, uczciwe bo ten sam zestaw
kanałów po obu stronach). **N=3 (DE, FE, BA)** jest dostępne WYŁĄCZNIE
w IR i OR@6 (obu typach fault, nie w normal) — używane jako
SEKUNDARNY, jawnie diagnostyczny test fault-vs-fault (czy dwa różne
typy uszkodzenia różnią się widmem przy pełnym N=3), NIE jako część
klasyfikacji normal-vs-fault (bo normal nie ma tam czego porównywać).

## 3. Krok 2: obiekt geometryczny — konstrukcja (zamrożona)

### 3.1 Korelacja czy kowariancja — WYBRANA: korelacja (Pearson), uzasadnienie

DE, FE, BA to fizycznie różne czujniki (inne miejsce montażu, inne
wzmocnienie/czułość) — ich WARIANCJE bezwzględne różnią się o rzędy
wielkości niezależnie od tego, jak silnie są ze sobą sprzężone. Macierz
KOWARIANCJI byłaby zdominowana przez kanał o największej wariancji
(typowo DE, najbliżej źródła defektu) niezależnie od struktury
sprzężenia, mieszając "siłę sygnału pojedynczego kanału" z "siłą
sprzężenia między kanałami" — dwa różne zjawiska. Macierz KORELACJI
(znormalizowana do przekątnej =1) izoluje WYŁĄCZNIE strukturę
współzmienności/synchronizacji, która jest tu przedmiotem
zainteresowania ("membrana się zapada w jeden kierunek" = kanały stają
się silnie skorelowane, niezależnie od tego, który ma większą
bezwzględną amplitudę). Decyzja podjęta PRZED zobaczeniem jakichkolwiek
danych.

### 3.2 Macierz korelacji i widmo

Dla okna zawierającego `N` jednocześnie dostępnych kanałów, każdy o
długości `n` próbek w oknie:

```
C(t) = corrcoef(x_1[okno], ..., x_N[okno])      # N x N, symetryczna, C_ii=1
λ_1(t) ≥ λ_2(t) ≥ ... ≥ λ_N(t) ≥ 0 = eigvalsh(C(t))   # widmo, posortowane malejąco
```

`C(t)` jest symetryczna nieujemnie określona z konstrukcji (macierz
korelacji Pearsona) — widmo jest rzeczywiste i nieujemne bez żadnych
sztuczek numerycznych; `np.linalg.eigvalsh` (dedykowany dla macierzy
symetrycznych, szybki i stabilny). Ujemne wartości własne rzędu
błędu numerycznego (`~1e-15`) są przycinane do `0` (`np.clip`), bo
teoretycznie macierz jest PSD — odnotowane wprost jako czysto
numeryczna korekta, nie zmiana definicji.

To jest "membrana" tej sesji: jej kształt w czasie (jak widmo ewoluuje
między/wewnątrz okien) to odpowiednik "kotary" — rozpięta (widmo
rozłożone równomiernie, brak dominującego kierunku) vs kurcząca się w
jeden kierunek (jeden dominujący `λ_1`, reszta blisko zera — kanały
silnie sprzężone).

## 4. Krok 3: metryki (zamrożone, zdefiniowane PRZED danymi)

### 4.1 Koncentracja spektralna (primarna)

```
spectral_concentration(t) = λ_1(t) / Σ_i λ_i(t)
```

Udział największej wartości własnej w całkowitej "energii" widma.
Zakres `[1/N, 1]`. Rośnie do `1`, gdy kanały stają się silnie sprzężone
(membrana "zapada się" w jeden kierunek). Przy `N` niezależnych,
identycznie rozłożonych kanałach bez żadnego wspólnego składnika,
wartość OCZEKIWANA (w granicy dużej próby) to `1/N` — ale przy
SKOŃCZONEJ próbie sama próbkowa macierz korelacji ma nietrywialny
rozkład (losowa macierz Wisharta/korelacji), więc `spectral_concentration`
nawet na czystym szumie jest > `1/N` w oczekiwaniu, z rozrzutem
zależnym od `n` (liczby próbek w oknie) i `N` (liczby kanałów) — stąd
KONIECZNOŚĆ kontroli negatywnej na czystym szumie (§5), nie założenie a
priori.

### 4.2 Efektywna ranga / participation ratio (primarna)

```
participation_ratio(t) = (Σ_i λ_i(t))² / Σ_i λ_i(t)²
```

Standardowa miara z fizyki/statystyki (inverse participation ratio,
odwrócona) — ile "niezależnych wymiarów" faktycznie jest aktywnych.
Zakres `[1, N]`: `=N`, gdy wszystkie `λ_i` równe (membrana w pełni
rozpięta), `=1`, gdy jeden `λ_1` dominuje (membrana zapadnięta w jeden
kierunek). NIE nowy wymysł — ten sam wzór używany do "effective rank"/
"participation ratio" w fizyce nieporządku i analizie PCA.

### 4.3 `membrane_spectral_ratio` (sekundarna, analogiczna do rodziny v0.1-v0.3)

Dla okna o długości `n` i `EDGE_FRACTION=0.2` (ta sama stała co cała
rodzina v0.1-v0.3, `n_edge=max(N+3, round(0.2·n))` — próg `N+3` zamiast
gołego `2` z poprzednich wersji, bo tu KAŻDY brzeg wymaga policzenia
osobnej macierzy korelacji `N×N` z próbek TEGO brzegu, nie pojedynczej
statystyki; przy `N=3` korelacja z < 6 próbek byłaby zdegenerowana —
próg uzasadniony PRZED danymi, nie dostrojony po fakcie):

```
C_start = corrcoef(x_1[:n_edge], ..., x_N[:n_edge])
C_end   = corrcoef(x_1[-n_edge:], ..., x_N[-n_edge:])
conc_start = λ_1(C_start) / Σλ_i(C_start)
conc_end   = λ_1(C_end) / Σλ_i(C_end)
membrane_spectral_ratio = conc_end / conc_start     (NaN jeśli conc_start < 1e-9)
```

Nazwa uzasadniona: kolizji brak (§1), opisuje dosłownie to, co liczy —
stosunek koncentracji widma membrany na końcu vs początku okna,
analogicznie do `chrono_cone_ratio`/`chrono_pendulum_ratio` (koniec/
początek), ale na WIDMIE macierzy korelacji wielu kanałów, nie na
promieniu anomalii jednego kanału. `ratio > 1` → kanały coraz silniej
sprzęgają się w czasie trwania okna; `ratio < 1` → coraz słabiej; `ratio
≈ 1` → stabilne sprzężenie (bez trendu wewnątrz okna).

## 5. Krok 4: kontrole syntetyczne (zamrożone PRZED implementacją)

Trzy generatory, `N_CHANNELS ∈ {2, 3}` (dopasowane do §2: N=2 primarny
test, N=3 sekundarny), `OMEGA_SHARED = 2π/15` (okres współdzielonego
składnika — wartość nieistotna dla mechanizmu korelacji, w
odróżnieniu od v0.1-v0.3 gdzie okres determinował liczbę szczytów;
zachowana tu tylko dla spójności wizualnej z resztą rodziny, nie z
konieczności matematycznej).

- **(a) POZYTYWNA — niezależny szum + STOPNIOWO rosnący współdzielony
  składnik**: `x_i(t) = N(0, σ²) + growth(t)·sin(ω·t)`,
  `growth(t) = GROWTH_RATE·t` (liniowo rosnąca od `0`), TEN SAM
  `sin(ω·t)` dodany do WSZYSTKICH `N` kanałów. Przewidywanie PRZED
  uruchomieniem: `membrane_spectral_ratio` istotnie WYŻSZY niż (b),
  mediana wyraźnie > 1 (koncentracja rośnie w miarę jak wspólny
  składnik dominuje nad niezależnym szumem pod koniec okna).
- **(b) NEGATYWNA A — CAŁKOWICIE niezależny biały szum, bez trendu**:
  `x_i(t) = N(0, σ²)`, każdy kanał NIEZALEŻNY, przez CAŁY czas, ŻADEN
  wspólny składnik. Przewidywanie: `spectral_concentration` bliska
  `1/N` (z rozrzutem próbkowym, §4.1) PRZEZ CAŁY CZAS, BEZ trendu →
  `membrane_spectral_ratio` bliski `1`, bez istotnej różnicy względem
  (c). **To jest kluczowa kontrola przeciw fałszywemu sygnałowi z
  samego szumu** — analogicznie do tego, co przeszło w v0.1/v0.2, ale
  zawiodło w v0.3 (człon nieujemny/wyłącznie wzmacniający generował
  fałszywy trend nawet na czystym szumie) — sprawdzane tu starannie,
  PRZED realnymi danymi, na CAŁEJ siatce rozmiarów okna.
- **(c) DODATKOWA — niezależny szum + STAŁY (nie rosnący) współdzielony
  składnik**: `x_i(t) = N(0, σ²) + K·sin(ω·t)`, `K` STAŁE (ta sama
  amplituda przez cały czas, w odróżnieniu od (a)). Przewidywanie:
  `spectral_concentration` PODNIESIONA względem (b) (bo jest trwałe
  sprzężenie) ale STAŁA w czasie (bez trendu wewnątrz okna) →
  `membrane_spectral_ratio` bliski `1` (analogicznie do "cylindra" w
  v0.1) — kontrola odróżniająca "stała korelacja" od "rosnąca
  korelacja", tak jak (c) w v0.1 odróżniało stałą amplitudę od rosnącej.

**Test POZYTYWNY**: (a) vs (b), na `membrane_spectral_ratio`,
Mann-Whitney U, oczekiwane `p<0.05`, `|r|≥0.3`, kierunek `median(a) >
median(b)`. **Test NEGATYWNY**: (b) vs (c), na `membrane_spectral_ratio`
(NIE na `spectral_concentration` — (c) ma z definicji WYŻSZĄ
`spectral_concentration` niż (b), to jest oczekiwane i nie jest to co
testujemy; testujemy, czy OBA są PŁASKIE w czasie, czyli czy ich RATIO
jest bliski `1` i nieodróżnialny), oczekiwany BRAK istotnej różnicy —
**jeśli (b) i (c) OKAŻĄ SIĘ istotnie różne na `membrane_spectral_ratio`,
to sam w sobie ważny wynik** (oznaczałoby, że stały poziom korelacji
generuje fałszywy trend rangowy), zgłoszone wprost.

**Dodatkowa kontrola opisowa** (nie klasyfikacyjna): mediana
`spectral_concentration` (b) vs (c) — oczekiwana `median(c) >
median(b)` (bo (c) ma trwałe sprzężenie, (b) nie) — to jest test
SANITY, że sama koncentracja poprawnie wykrywa STAN sprzężenia,
niezależnie od tego, czy jest w niej trend.

**Siatka**: `WINDOW_SIZES=(128, 256, 512)` — podzbiór zalecanego
`{48,128,256,512,1024}` (§ zadania), wybrany z uzasadnieniem: `48` jest
ZBYT MAŁE dla `N=3` (przy `EDGE_FRACTION=0.2`, `n_edge=max(6,
round(0.2·48))=10` próbek na kanał do policzenia macierzy korelacji
3×3 — na granicy stabilności, wysokie ryzyko artefaktu analogicznego do
v0.3), `1024` pominięte jako redundantne względem `512` dla tego
mechanizmu (korelacja nie wymaga wielu okresów oscylacji jak
`peak_referenced_phase` v0.1-v0.3 — nie ma tu analogicznego powodu
strukturalnego, żeby iść wyżej niż `512`) — decyzja PRZED uruchomieniem
czegokolwiek. `N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05` — konwencja repo,
bez zmian.

**Kolejność wykonania (jak w v0.3 — RYZYKO najpierw)**: kontrola (b) vs
(c) (czy stały szum generuje fałszywy trend) jest uruchamiana RAZEM z
(a) vs (b) w JEDNEJ bramce (jak v0.1/v0.2, nie osobną fazą jak v0.3 —
bo tu NIE MA członu z natury "wyłącznie wzmacniającego nieujemnego"
jak w v0.3; ryzyko jest niższe, ale sprawdzane z tą samą starannością).
Jeśli bramka NIE przejdzie zgodnie z przewidywaniem — ZATRZYMANIE,
zgłoszenie jako wynik na etapie kontroli, BEZ realnych danych.

## 6. Krok 5: realne dane (URUCHAMIANE WYŁĄCZNIE, jeśli §5 przejdzie)

### 6.1 Test PRIMARNY (N=2, DE+FE, normal vs fault) — decyduje o klasyfikacji

Pliki (§2): `1797_Normal.npz` (tło/zdrowe) vs `1797_IR_21_DE12.npz` I
`1797_OR@6_21_DE12.npz` (dwa oddzielne typy uszkodzenia, NIE mieszane).
Segmentacja: nieprzecinające się okna (ten sam wzorzec `_segment_pool`
co v0.1-v0.3), `WINDOW_SIZES=(128, 256, 512)` (identyczne z siatką
syntetyczną §5, dla porównywalności). Przy najkrótszym pliku (IR,
122 136 próbek) i `window_size=128` → 954 dostępnych segmentów (dużo
więcej niż `N_WINDOWS=30` — REUŻYCIE NIE jest tu problemem, w
odróżnieniu od BTC w v0.1-v0.3). `N_WINDOWS=30` losowych (bez powtórzeń,
gdy dostępnych ≥30) segmentów na grupę, `SEED=0`.

Metryki testowane: `spectral_concentration`, `participation_ratio`
(primarne, liczone na CAŁYM oknie, NIE brzeg/brzeg),
`membrane_spectral_ratio` (sekundarna, brzeg/brzeg). Mann-Whitney U +
rank-biserial `r`, `SUPPORTED` = `p<0.05` i `|r|≥0.3` — **klasyfikacja
oparta na `spectral_concentration`** (primarna metryka tej sesji,
zgodnie z konkretnym przewidywaniem poniżej); `participation_ratio` i
`membrane_spectral_ratio` raportowane obok jako diagnostyka, nie
zmieniają klasyfikacji per komórka.

**KONKRETNE przewidywanie kierunku, zapisane PRZED danymi**: fault (IR,
OR@6) pokaże WYŻSZĄ `spectral_concentration` / NIŻSZĄ
`participation_ratio` niż normal — uzasadnienie fizyczne: uszkodzenie
łożyska wprowadza silne, współdzielone zaburzenie mechaniczne
(uderzenia/impulsy propagujące się przez obudowę do WSZYSTKICH
czujników jednocześnie, niezależnie od miejsca montażu), widoczne
SYMULTANICZNIE na obu osiach (DE, FE) — podczas gdy normalna praca ma
bardziej niezależny/rozproszony szum tła między osiami (brak
wspólnego, silnego źródła wzbudzenia). Kierunek zapisany PRZED
uruchomieniem; jeśli wynik pójdzie w przeciwną stronę, to jest
zgłoszone wprost jako wynik SPRZECZNY z przewidywaniem, nie
przemianowany po fakcie.

**Test stabilności znaku** (GŁÓWNE pytanie metodologiczne tej sesji, ta
sama dyscyplina co v0.1/v0.2): rank-biserial `r` (na
`spectral_concentration`) porównany między `WINDOW_SIZES=(128,256,512)`
dla TEGO SAMEGO pliku uszkodzenia. **ZNAK STABILNY** = ten sam znak we
wszystkich trzech rozmiarach okna. **ZNAK NIESTABILNY** = różny znak
między rozmiarami — dokładnie ten wzorzec, który obalił v0.1/v0.2 na
metryce primarnej, sprawdzany tu wprost, bez zakładania z góry wyniku.

### 6.2 Test SEKUNDARNY, diagnostyczny (N=3, DE+FE+BA, fault vs fault)

`1797_IR_21_DE12.npz` (DE,FE,BA) vs `1797_OR@6_21_DE12.npz` (DE,FE,BA)
— NIE normal-vs-fault (normal nie ma BA), więc to NIE wchodzi do
klasyfikacji SUPPORTED/NOT_SUPPORTED §6.1. Cel: sprawdzić, czy dodanie
trzeciego, jednocześnie dostępnego kanału (BA) zmienia obraz między
dwoma typami uszkodzenia — czysto eksploracyjne, raportowane osobno,
NIE zastępuje ani nie waży testu primarnego. Te same `WINDOW_SIZES`,
`N_WINDOWS=30`, `SEED=0`.

## 7. Klasyfikacja końcowa (ustalona z góry)

**SUPPORTED** (dla danego pliku uszkodzenia, N=2, `spectral_concentration`)
= `p<0.05`, `|r|≥0.3`, kierunek zgodny z przewidywaniem §6.1 (fault >
normal), I ZNAK STABILNY między WSZYSTKIMI trzema rozmiarami okna.
**NOT_SUPPORTED** = `p≥0.05` przy wystarczającej liczbie obserwacji
(≥10 w grupie, jak konwencja repo) LUB kierunek przeciwny do
przewidywania. **NIESTABILNY** (osobna, jawnie nierozstrzygająca
kategoria, jak w v0.1/v0.2) = formalnie `SUPPORTED` przy `sigma`/oknie
ale znak zmienia się między rozmiarami okna — traktowane jako BRAK
potwierdzenia stabilnej struktury geometrycznej, zgodnie z precedensem
v0.1/v0.2 (formalny odsetek `SUPPORTED` per komórka NIE wystarcza bez
sprawdzenia stabilności znaku). **INCONCLUSIVE** = <10 ważnych
obserwacji w którejś grupie.

## 8. Status

Zamrożone. Kolejność wykonania: (1) `core/chrono_membrane_bridge.py`
— konstrukcja + generatory + kontrole syntetyczne (§5), uruchomione
NAJPIERW; (2) jeśli kontrole PASSED: `core/real_chrono_membrane_bridge.py`
— test na realnych danych CWRU (§6); (3)
`docs/geometry/RESULT_CHRONO_MEMBRANE_BEARING_v0.1.md` z pełnymi
liczbami, łącznie z wynikiem negatywnym/niejednoznacznym, bez
retuningu po fakcie. Jeśli kontrole NIE przejdą: zatrzymanie,
zgłoszenie na etapie kontroli, BEZ realnych danych — dokładnie tak, jak
w całej rodzinie v0.1-v0.3.
