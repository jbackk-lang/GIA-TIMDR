# Pre-rejestracja: chrono_membrane_bridge v0.2 — odwrócony kierunek (normal > fault w `spectral_concentration`), test na CZASOWO ODOSOBNIONEJ drugiej połowie każdego nagrania

> Status: PRE-REJESTRACJA, zamrożona PRZED uruchomieniem
> `core/real_chrono_membrane_bridge_v0_2.py`. Data: 2026-09-21. Piąta
> iteracja wątku (po `chrono_cone_ratio` v0.1, `chrono_pendulum_ratio`/
> `net_turn` v0.2, `chrono_centrifugal_ratio` v0.3, `chrono_membrane_bridge`
> v0.1 — `docs/geometry/RESULT_CHRONO_MEMBRANE_BEARING_v0.1.md`). Kontynuacja
> BEZPOŚREDNIA v0.1: sama konstrukcja (`membrane_window_metrics`,
> `spectral_concentration`), ten sam kod (`core/chrono_membrane_bridge.py`,
> BEZ ZMIAN), TYLKO odwrócony kierunek przewidywania i NOWY protokół
> podziału danych (§1).

## 0. Skąd to się bierze

`RESULT_CHRONO_MEMBRANE_BEARING_v0.1.md` §7 zostawił otwarty punkt:
formalna pre-rejestracja v0.2 z ODWRÓCONYM kierunkiem przewidywania
(`normal > fault` w `spectral_concentration`, zamiast `fault > normal`
z v0.1) — na PODSTAWIE uzasadnienia post-hoc z v0.1 §3.1 (zdrowe
łożysko: stabilny tryb obrotowy, wibracja propaguje się do DE/FE w
spójny, silnie skorelowany sposób; uszkodzenie: impulsowe, asymetryczne
zaburzenia docierające różnymi ścieżkami tłumienia do DE/FE →
rozprzęganie kanałów). v0.1 odnotował wprost: to NIE byłby niezależny
test, bo dane (te same trzy pliki NPZ) już zostały zobaczone w całości
przy formułowaniu tego kierunku.

## 1. Ograniczenie uczciwości — rozwiązanie przyjęte tutaj

Nie mamy świeżych plików CWRU lokalnie (inne RPM/obciążenie/typ defektu
nie są dostępne w tym repo — sprawdzone w v0.1 §1, bez zmian). Test na
TYCH SAMYCH trzech plikach z odwróconym kierunkiem, bez żadnego
podziału, byłby CYRKULARNY — przemalowanie już zaobserwowanego wyniku
na "potwierdzenie", nie prawdziwy test.

**Przyjęte częściowe rozwiązanie — podział CZASOWY każdego nagrania na
dwie nienachodzące się połowy** (pierwsza/druga połowa próbek, w
kolejności czasu akwizycji, granica w połowie długości pliku):

- **PIERWSZA połowa** każdego z trzech plików = zbiór KALIBRACYJNY.
  Może być użyta do potwierdzenia, że kierunek/próg jest sensowny — ale
  **NIE do raportowania wyniku końcowego**. Jawnie odnotowane: ponieważ
  kierunek `normal > fault` już WIADOMO z v0.1 (który użył CAŁYCH
  plików, więc w tym także pierwszej połowy), wynik na pierwszej
  połowie NIE JEST nowym odkryciem — jest z definicji oczekiwany.
  Uruchamiany i raportowany OSOBNO, jawnie oznaczony jako
  nie-rozstrzygający.
- **DRUGA połowa** każdego pliku = zbiór TESTOWY. To jest jedyna część
  tej sesji, która liczy się jako wynik. Kluczowa własność: druga
  połowa próbek NIE była nigdy osobno analizowana w v0.1 (v0.1 testował
  losowo próbkowane segmenty z CAŁEGO pliku, w tym niektóre z drugiej
  połowy, ale nigdy nie wydzielił drugiej połowy jako samodzielnego,
  izolowanego zbioru do własnego testu Manna-Whitneya) — więc ten
  konkretny test (Mann-Whitney U wyłącznie na segmentach z drugiej
  połowy) jest operacją nową, nie powtórzeniem.

**Uczciwe zastrzeżenie, zapisane wprost i nieukrywane**: to NIE jest
pełnoprawna niezależna replikacja w sensie "zupełnie nowe dane,
zupełnie inny dzień pomiaru, zupełnie inne łożysko". Same fizyczne
nagranie (to samo łożysko, ten sam przebieg eksperymentu CWRU) generuje
obie połowy — jeśli istnieje jakikolwiek DRYF w czasie trwania
nagrania (np. narastające zużycie, zmiana temperatury) wspólny obu
połowom, test nie jest w pełni odporny na taki confound. Mimo to jest
to WYRAŹNIE silniejszy standard niż "ten sam zbiór, przemalowany
kierunek" — segmenty drugiej połowy nie zostały nigdy osobno
zaraportowane jako samodzielny wynik przed tą sesją.

## 2. Hipoteza (zamrożona)

**`spectral_concentration`: normal > fault** (odwrócona względem v0.1,
która przewidywała `fault > normal`). Uzasadnienie: WYŁĄCZNIE wynik
v0.1 (§3.1, silny, stabilny, konsekwentny na 6/6 komórkach) — **to NIE
jest niezależnie wyprowadzona hipoteza fizyczna sprzed jakichkolwiek
danych; to jest formalizacja JUŻ ZAOBSERWOWANEGO kierunku, w celu
sprawdzenia go na fragmencie danych, który nie był wcześniej
raportowany osobno (§1).** Ten fakt jest zapisany wprost w klasyfikacji
końcowej (§5) — SUPPORTED tutaj oznacza "kierunek utrzymuje się na
odizolowanej drugiej połowie", NIE "niezależnie odkryty efekt".

Metryka: WYŁĄCZNIE `spectral_concentration` (metryka primarna v0.1).
`participation_ratio` i `membrane_spectral_ratio` NIE są tu retestowane
— przy N=2 (test primarny) `participation_ratio` jest zdeterminowaną
funkcją `spectral_concentration` (v0.1 §3.1, odnotowane wprost, nie
niesie dodatkowej informacji), a `membrane_spectral_ratio` już dała
6/6 NOT_SUPPORTED w v0.1 (brak sygnału w metryce brzeg/brzeg) — nie ma
podstaw, żeby oczekiwać innego wyniku na podzbiorze tych samych danych,
więc jej ponowne testowanie tutaj byłoby tylko zwiększeniem liczby
porównań bez uzasadnionego a priori pytania. Odnotowane jako świadome
zawężenie zakresu, nie przeoczenie.

## 3. Metoda (zamrożona)

### 3.1 Konstrukcja — BEZ ZMIAN względem v0.1

`core/chrono_membrane_bridge.py` używany 1:1, bez modyfikacji:
`channel_correlation_matrix`, `spectrum_from_correlation`,
`spectral_concentration`, `membrane_window_metrics`. Kontrole
syntetyczne (v0.1 §2) NIE są powtarzane — mechanizm jest identyczny,
tylko dane wejściowe i podział są nowe; nie ma nowego ryzyka
mechanicznego do sprawdzenia kontrolą syntetyczną, bo żadna nowa
metryka/formuła nie jest tu wprowadzana.

### 3.2 Podział na połowy

Dla każdego z trzech plików (`1797_Normal.npz`, `1797_IR_21_DE12.npz`,
`1797_OR@6_21_DE12.npz`), po wczytaniu przez
`load_synchronous_cwru_channels` (bez zmian): `n = len(sygnału)`,
`half = n // 2`. Każdy kanał: `first = sygnał[:half]`,
`second = sygnał[half:]`. Podział stosowany PRZED segmentacją na okna
— czyli żadne okno nie przecina granicy połowy (okna są budowane
osobno wewnątrz `first` i osobno wewnątrz `second`).

### 3.3 Segmentacja i próbkowanie okien

Identyczna jak w v0.1 (`_segment_pool`/`_sample_windows` z
`core/real_chrono_membrane_bridge.py`, reużyte bez zmian, importowane
nie przepisywane): nieprzecinające się okna wewnątrz DANEJ połowy,
`WINDOW_SIZES=(128, 256, 512)` (IDENTYCZNE z v0.1, dla porównywalności,
zgodnie z wymaganiem zadania), `N_WINDOWS=30` losowych (bez powtórzeń,
gdy dostępnych ≥30) segmentów na grupę, `SEED=0` dla kalibracji,
`SEED=100` dla testu (rozdzielone jawnie, żeby losowanie testu NIE
odtwarzało identycznych indeksów co losowanie kalibracji — nieistotne
dla samego wyniku, bo grupy są rozłączne z definicji przez podział
czasowy, ale odnotowane dla przejrzystości).

Sprawdzenie dostępności PRZED uruchomieniem: najkrótszy plik po
podziale na pół to IR (122136/2 ≈ 61068 próbek na połowę); przy
`window_size=512` daje to ≈119 segmentów na połowę — nadal wielokrotnie
więcej niż `N_WINDOWS=30`, więc reużycie NIE jest tu problemem w żadnej
komórce (analogicznie do v0.1).

### 3.4 Test statystyczny

Mann-Whitney U + rank-biserial `r` (`timdr_formalism.pipeline.
mann_whitney_test`, bez zmian). Grupa "pozytywna" (`pos`) = `normal`,
grupa "tło" (`neg`) = `fault` — odwrócone względem v0.1 (gdzie
`pos=fault`), żeby znak `r>0` odpowiadał wprost przewidywaniu tej sesji
(`normal > fault`). `SUPPORTED (kalibracja)` / `SUPPORTED (test)` =
`p<0.05`, `|r|≥0.3`, `r>0` (median(normal) > median(fault)).

**Test stabilności znaku**: `r` (na drugiej połowie, `spectral_concentration`)
porównany między `WINDOW_SIZES=(128,256,512)` dla KAŻDEGO typu
uszkodzenia osobno, identycznie jak v0.1 §6.1/§7.

## 4. Klasyfikacja końcowa (ustalona z góry, DOTYCZY WYŁĄCZNIE DRUGIEJ POŁOWY)

**SUPPORTED** = na DRUGIEJ połowie: `p<0.05`, `|r|≥0.3`, `r>0`
(normal > fault), I znak `r` stabilny (ten sam, dodatni) na wszystkich
trzech rozmiarach okna, dla DANEGO typu uszkodzenia.
**NOT_SUPPORTED** = `p≥0.05` przy ≥10 ważnych obserwacji w grupie, LUB
`r<0` (kierunek przeciwny — czyli zgodny z ORYGINALNYM przewidywaniem
v0.1, nie z odwróconym v0.2).
**NIESTABILNY** = formalnie `SUPPORTED` na części rozmiarów okna, ale
znak zmienia się między rozmiarami — traktowane jako BRAK potwierdzenia,
zgodnie z precedensem v0.1/v0.2 (rodzina `chrono_cone`) i v0.1
`chrono_membrane_bridge`.
**INCONCLUSIVE** = <10 ważnych obserwacji w którejś grupie.

Wynik na PIERWSZEJ (kalibracyjnej) połowie jest raportowany OBOK, jawnie
oznaczony jako nie-rozstrzygający, niezależnie od tego, co pokaże —
nie wpływa na klasyfikację SUPPORTED/NOT_SUPPORTED tej sesji.

## 5. Status

Zamrożone. Kolejność wykonania: (1)
`core/real_chrono_membrane_bridge_v0_2.py` — wczytanie, podział na
połowy, kalibracja (pierwsza połowa) + test (druga połowa) dla obu
typów uszkodzenia, trzech rozmiarów okna; (2)
`docs/geometry/RESULT_CHRONO_MEMBRANE_BEARING_v0.2.md` z pełnymi
liczbami dla OBU połówek, wynik raportowany NIEZALEŻNIE od tego, czy
potwierdza hipotezę — zgodnie z całym protokołem repo (punkt 3 skilla:
"wynik negatywny jest pełnoprawną odpowiedzią"). Nic w kodzie nie
zostanie zmienione po zobaczeniu wyniku testowego (drugiej połowy).
