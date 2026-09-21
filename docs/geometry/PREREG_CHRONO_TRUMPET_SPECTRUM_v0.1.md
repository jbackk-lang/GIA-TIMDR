# Pre-rejestracja: chrono_trumpet_spectrum — widmo macierzy korelacji zwinięte w "trąbkę", siatka pól krzywizny (dyskretny operator Weingartena)

> Status: PRE-REJESTRACJA, zamrożona PRZED uruchomieniem
> `core/chrono_trumpet_spectrum.py` na realnych danych. Data: 2026-09-21.
> NOWY obiekt geometryczny, NIEZALEŻNY od `chrono_membrane_bridge`
> v0.1/v0.2 (`PREREG_CHRONO_MEMBRANE_BEARING_v0.{1,2}.md`) — reużywa te
> same surowe dane (widmo macierzy korelacji DE/FE/BA łożysk CWRU) i te
> same funkcje budujące widmo (`channel_correlation_matrix`,
> `spectrum_from_correlation` z `core/chrono_membrane_bridge.py`, BEZ
> ZMIAN), ale buduje z nich PRAWDZIWĄ POWIERZCHNIĘ 2D (siatka
> indeks×czas), nie krzywą 1D jak cała rodzina `chrono_cone`/
> `chrono_membrane` v0.1-v0.3. Osobny plik nazewniczy ("trumpet" po
> angielsku), żeby uniknąć kolizji z polskimi znakami w nazwie ("trąbka")
> i pomyłki z istniejącą linią "membrana/kotara".

## 0. Skąd to się bierze

Właściciel projektu: "nie zdziwiłbym się gdyby widmo czytać trzeba było
jako zwinięte w trąbkę, a na jego powierzchni utworzyłaby się siatka
pól". Operacjonalizacja uzgodniona PRZED napisaniem kodu (poniżej, §2) —
zwinięcie oznacza dosłownie: indeks widma `i=1..N` rozłożony po
obwodzie okręgu (kąt), amplituda widma (`λ_i` znormalizowane) jako
promień, czas jako oś pionowa — klasyczny kształt "trąbki/lejka",
którego promień na obwodzie zależy od czasu. To PIERWSZA konstrukcja w
tej rodzinie, która daje prawdziwą siatkę punktów 2D (`N` punktów na
obwodzie × `T` kroków czasowych), więc pierwsza, do której w ogóle da
się zastosować dyskretny operator Weingartena z
`TIMDR-Geometry-Formalism/timdr_geometry/weingarten.py` (wymaga
dwuwymiarowej siatki trójkątnej — G8-G9, punkt 6 skilla) — wszystkie
poprzednie konstrukcje (`chrono_cone_ratio`, `chrono_pendulum_ratio`,
`chrono_centrifugal_ratio`, `membrane_spectral_ratio`) były krzywą 1D
(jeden parametr czasu), na której operator kształtu powierzchni nie ma
zastosowania.

**Ważne odróżnienie od `B4_BEARING_DATA_FREEZE.md`**: ta zamrożona
notatka blokuje liczenie krzywizny z FIZYCZNYCH współrzędnych czujników
DE/FE/BA (bo trzy czujniki dają najwyżej jeden trójkąt, bez
dwuwymiarowego sąsiedztwa) — i ten zakaz POZOSTAJE W MOCY, nie jest tu
naruszany. Siatka budowana w tej sesji NIE używa fizycznych
współrzędzeń czujników jako wierzchołków; wierzchołkami są punkty
SKONSTRUOWANE z WARTOŚCI WIDMA (λ_i(t)) w sztucznie zdefiniowanym
układzie (kąt+promień+czas), z jawną, gęstą, prerejestrowaną
triangulacją regularnej siatki (§3.3) — to jest inny obiekt matematyczny
niż to, czego zakazuje freeze (interpolacja/wymyślanie współrzędnych
CZUJNIKÓW). Odnotowane wprost, żeby nie było wrażenia obchodzenia
zamrożonej bramki.

## 1. Audyt nazw

Grep na całym drzewie repo: `chrono_trumpet`, `trumpet_spectrum`,
`spectral_trumpet` — zero kolizji. Nowe nazwy. `chrono_membrane_bridge`,
`spectral_concentration`, `participation_ratio` (v0.1/v0.2) — reużyte
WYŁĄCZNIE jako źródło surowego widma `λ_i(t)` (import funkcji, nie
duplikacja kodu), NIE jako część klasyfikacji tej sesji — konstrukcja
tutaj jest fundamentalnie inna (powierzchnia 2D, nie skalar na oknie).
`weingarten.py` (G8-G9) — reużyty BEZ ZMIAN, zgodnie z zadaniem: "użyjesz
go, nie pisz nowego".

## 2. Obiekt geometryczny — konstrukcja (zamrożona)

Dla łożyska o `N` jednocześnie dostępnych kanałach (N=2 dla `Normal`:
DE,FE; N=3 dla `IR_21`/`OR6@6`: DE,FE,BA — PRZETESTOWANE OSOBNO, bez
mieszania, zgodnie z zadaniem), sygnał dzielony na kolejne,
NIEPRZECINAJĄCE SIĘ okna w czasie (ten sam wzorzec `_segment_pool` co
`chrono_membrane_bridge`, ale w KOLEJNOŚCI czasowej — nie losowo
próbkowane — bo ta konstrukcja potrzebuje CIĄGŁEJ trajektorii w czasie,
nie próbki 30 losowych okien). Dla okna `t` (indeks 0..T-1):

```
C(t) = corrcoef(kanały w oknie t)                      # core/chrono_membrane_bridge.channel_correlation_matrix
λ_1(t) ≥ ... ≥ λ_N(t) ≥ 0 = eigvalsh(C(t))              # spectrum_from_correlation, BEZ ZMIAN
```

**Kąt** (stały w czasie, jeden na indeks widma): `θ_i = 2π(i-1)/N` dla
`i=1..N`.

**Promień** (zależny od czasu): `r_i(t) = λ_i(t) / Σ_j λ_j(t)` —
**ZMIANA względem surowego `λ` użytego w v0.1/v0.2**: normalizacja
konieczna, żeby porównywać KSZTAŁT powierzchni niezależnie od amplitudy
sygnału (surowe `λ_i` zależą od skali sygnału na danym kanale/pliku —
bez normalizacji "trąbka" zmieniałaby rozmiar między plikami z powodów
niezwiązanych z jej kształtem, mieszając dwa różne zjawiska, dokładnie
jak uzasadnienie korelacji-nie-kowariancji w v0.1 §3.1). To jest
DOKŁADNIE `spectral_concentration`-style unormowanie, tylko
zastosowane do KAŻDEGO `λ_i`, nie tylko `λ_1`.

**Wysokość**: `z(t) = t` — Chronoproces, czas w sekundach od początku
nagrania (`t = numer_okna · window_size / fs`), jak w poprzednich
konstrukcjach tej rodziny.

**Powierzchnia**: punkty `(i,t) → (r_i(t)·cosθ_i, r_i(t)·sinθ_i, t)` —
to jest PRAWDZIWA siatka 2D (dyskretny indeks widma `i` × czas `t`),
różna od WSZYSTKICH poprzednich konstrukcji rodziny `chrono_cone`/
`chrono_membrane` (v0.1-v0.3 miały krzywą 1D — jeden parametr czasu —
nie powierzchnię).

## 3. Adaptacja do interfejsu `weingarten.py` (bez przepisywania operatora)

### 3.1 Co operator wymaga

`weingarten.py::Mesh` wymaga `vertices (M,3)` i `faces (K,3)` (siatka
TRÓJKĄTNA, patrz `make_cylinder_mesh` jako gotowy wzorzec regularnej
siatki walcowej — dokładnie ten kształt, jakiego tu potrzeba: `i`
zawinięte na obwodzie [analogicznie do `theta` walca], `t` otwarte
[analogicznie do `z` walca]). `discrete_shape_operator(mesh, normals,
point_idx, rings)` wymaga ≥2 sąsiadów w 1-ringu i rzutów stycznych o
pełnym rzędzie (2) — RZUCA `ValueError` w przeciwnym razie (nie zwraca
cichej wartości zerowej).

### 3.2 Wierzchołki

`T` okien czasowych × `N` indeksów widma → `T·N` wierzchołków,
indeksowanych `v = t_idx·N + i_idx` (ten sam porządek co
`make_cylinder_mesh` w `weingarten.py`: `t` zewnętrzna pętla, `i`
wewnętrzna, zawinięta modulo `N`).

### 3.3 Triangulacja — reużycie WZORCA `make_cylinder_mesh` (nie kodu wprost, bo tamta funkcja generuje WŁASNE wierzchołki walca; tu potrzebne własne, z widma)

Dla `j` w `0..T-2`, `i` w `0..N-1`:
`a=j·N+i, b=j·N+(i+1)%N, c=(j+1)·N+i, d=(j+1)·N+(i+1)%N`, dwa trójkąty
`(a,b,d)` i `(a,d,c)` — DOKŁADNIE ta sama reguła co
`make_cylinder_mesh`, zastosowana do wierzchołków trąbki zamiast
wierzchołków walca. `i` zawinięte (siatka zamknięta na obwodzie — kąt
`θ_i` jest okresowy z definicji), `t` NIE zawinięte (czas ma początek i
koniec, jak w `make_cylinder_mesh` — pierwszy/ostatni wiersz `t` mają
niepełny 1-ring, POMIJANE przy liczeniu krzywizny, dokładnie jak
zalecenie dla walca w docstringu `weingarten.py`).

### 3.4 Zastrzeżenie o N=2

Przy `N=2` zawinięcie modulo 2 daje: sąsiad "w prawo" i "w lewo" po
obwodzie to ZAWSZE ten sam, jedyny drugi punkt (multi-krawędź) — 1-ring
kątowy jest zdegenerowany do pojedynczego punktu, nie dwóch różnych
kierunków. Operator może zadziałać (rzuty styczne czasowe + ten jeden
punkt kątowy mogą dać rząd 2), ale to JEST już samo w sobie osłabienie
struktury geometrycznej, nie tylko małą próbą — odnotowane PRZED
uruchomieniem, nie po zobaczeniu wyniku. Jeśli `discrete_shape_operator`
rzuci `ValueError` (zdegenerowany rząd) dla części/całości wierzchołków
N=2, to jest ZGŁASZANE wprost jako wynik (nie obejście/naprawa kodu
operatora — zgodnie z zadaniem "NIE przepisuj operatora od nowa").

## 4. Definicja testu krzywizny PRZED danymi (zamrożona)

### 4.1 Krzywizna Gaussa per wierzchołek

Dla każdego wewnętrznego wierzchołka (`t_idx ∈ [1, T-2]`, wszystkie
`i_idx`, bo `i` jest zawsze zawinięte — pełny 1-ring kątowy istnieje
zawsze): `K(i,t) = κ_1·κ_2` (`weingarten.gaussian_curvature`, iloczyn
krzywizn głównych z dopasowanego operatora kształtu). Wierzchołki, dla
których `discrete_shape_operator` rzuca `ValueError`, dostają `NaN` —
jawnie wykluczone z dalszej analizy tej kolumny `i`, zliczone i
zgłoszone jako `n_degenerate`.

### 4.2 Test "siatki pól" — naprzemienność znaku wzdłuż czasu, per `i` — DOKŁADNA DEFINICJA

Dla ustalonego indeksu widma `i`, sekwencja znaków
`s(t) = sign(K(i,t))` dla WSZYSTKICH ważnych (nie-`NaN`, nie-zerowych —
`K=0` dokładnie jest osobno zliczane jako `n_zero`, wykluczone z testu
znaku, bo `sign(0)=0` nie pasuje do żadnej z dwóch klas) `t`, w
kolejności czasowej.

**Test Walda-Wolfowitza (runs test)** na tej sekwencji: niech `n1` =
liczba `+1`, `n2` = liczba `-1`, `n=n1+n2`. `R` = liczba SERII
(maksymalnych ciągów tej samej wartości) w sekwencji. Pod hipotezą
zerową (sekwencja losowa, iid, przy ustalonych `n1,n2`):

```
E[R] = 2·n1·n2/n + 1
Var[R] = 2·n1·n2·(2·n1·n2 − n) / (n²·(n−1))
z = (R − E[R]) / sqrt(Var[R])
p = 2·(1 − Φ(|z|))            (dwustronny, Φ = dystrybuanta N(0,1))
```

Standardowy wzór testu serii (Wald-Wolfowitz), NIE nowy wymysł.
Interpretacja: `R` ISTOTNIE WYŻSZE niż `E[R]` (`z≫0`, `p<0.05`) =
sekwencja bardziej naprzemienna niż losowa (sygnatura "siatki pól" —
regularna oscylacja znaku krzywizny wzdłuż czasu). `R` ISTOTNIE NIŻSZE
= sekwencja bardziej "sklejona" (długie odcinki jednego znaku) niż
losowa. `p≥0.05` = brak odchylenia od losowej kolejności znaków —
BRAK obserwowalnej struktury okresowej tym testem.

Degeneracja `n1=0` lub `n2=0` (wszystkie znaki jednakowe) —
zgłaszana wprost jako `degenerate=True`, `p=None` (test serii
niezdefiniowany, gdy jedna klasa jest pusta — NIE traktowane jako
`p=1` czy `p=0`, tylko jako brak możliwości przeprowadzenia testu).

### 4.3 Parametry zamrożone

Jeden rozmiar okna, reprezentatywny dla porównywalności z
`chrono_membrane_bridge` v0.1/v0.2: **`window_size=256`** (środkowy z
`WINDOW_SIZES=(128,256,512)` tamtej rodziny — wybrany z góry, nie po
zobaczeniu wyników, żeby dać rozsądną liczbę okien `T` na całej
długości pliku bez nadmiernej liczby porównań wielokrotnych po kilku
rozmiarach naraz w zadaniu jawnie oznaczonym jako eksploracyjne).
Wszystkie dostępne, kolejne (nieprzecinające się) okna całego pliku
użyte do budowy trąbki (nie próbka 30 losowych — ta konstrukcja
potrzebuje CIĄGŁEJ osi czasu, nie próbki). Trzy pliki CWRU (§0 danych,
jak w `chrono_membrane_bridge`): `1797_Normal.npz` (N=2),
`1797_IR_21_DE12.npz` (N=3), `1797_OR@6_21_DE12.npz` (N=3) — KAŻDY
OSOBNO, N=2 i N=3 NIE mieszane (zgodnie z zadaniem).

## 5. JAWNE ZASTRZEŻENIE — status eksploracyjny/diagnostyczny, NIE twardy test (zapisane PRZED uruchomieniem)

Przy `N=2` lub `N=3` (tak mało punktów na obwodzie) wykrycie "siatki
pól" w sensie regularnego, GĘSTEGO wzoru geometrycznego jest
statystycznie słabo uzasadnione — trzy albo dwa punkty na obwodzie nie
dają wystarczającej rozdzielczości kątowej, żeby odróżnić prawdziwą
periodyczną strukturę powierzchni od artefaktu małej próby kątowej.
**To zadanie jest DIAGNOSTYCZNE/EKSPLORACYJNE — NIE twardym testem z
formalnym wnioskiem SUPPORTED/NOT_SUPPORTED.** Wynik testu serii z §4.2
(dowolny znak, dowolne `p`) jest ZGŁASZANY W PEŁNI z liczbami, ale
**NIE promowany do statusu potwierdzonego wyniku niezależnie od
tego, co pokaże** — nawet `p<0.05` na 2-3 kolumnach `i` przy tak małej
liczbie niezależnych "obwodów" jest z góry nazwane obserwacją wstępną,
wymagającą ZNACZNIE większego `N` (więcej jednoczesnych kanałów —
niedostępnych lokalnie w tym repo, patrz `B4_BEARING_DATA_FREEZE.md`)
do prawdziwej weryfikacji. Ryzyko numerologii przy `N∈{2,3}` jest
jawnie nazwane tutaj, PRZED zobaczeniem jakiegokolwiek wyniku, zgodnie
z protokołem anty-numerologii repo (punkt 3 skilla).

## 6. Status

Zamrożone. Kolejność wykonania: (1) `core/chrono_trumpet_spectrum.py` —
budowa widma/wierzchołków/siatki/adaptacja do `weingarten.py`, test
serii (§4.2); (2) uruchomienie na trzech plikach CWRU (§4.3); (3)
`docs/geometry/RESULT_CHRONO_TRUMPET_SPECTRUM_v0.1.md` z pełnymi
liczbami (liczba wierzchołków zdegenerowanych, znaki krzywizny, wynik
testu serii per `i` per plik), jawnie oznaczony jako eksploracyjny —
NIE klasyfikacja SUPPORTED/NOT_SUPPORTED. `tests/test_chrono_trumpet_spectrum.py`
sprawdza WYŁĄCZNIE poprawność konstrukcji (kąty, promienie, siatka,
wzór testu serii na znanych przykładach), nie powtarza analizy
realnych danych.
