# Pre-rejestracja: chrono_sphere_bridge — kierunek + promień wektora trzech jednoczesnych kanałów łożyska CWRU jako obiekt G (sfera S²)

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> danych (kod jeszcze nie napisany w chwili zapisania tego dokumentu).
> Data: 2026-09-22. Piąta iteracja wątku M/S↔G przez Chronoproces (po
> `chrono_cone_ratio` v0.1, `chrono_pendulum_ratio`/`net_turn` v0.2,
> `chrono_centrifugal_ratio` v0.3 — wszystkie odrzucone na kontroli —
> oraz `chrono_membrane_bridge` v0.1/v0.2 — potwierdzony, częściowa
> replikacja). Konstrukcja NIE reużywa żadnej z poprzednich metryk;
> dzieli z membraną wyłącznie fundament (Γ jako prawdziwa rodzina wielu
> jednoczesnych kanałów, nie jeden sygnał), inny obiekt geometryczny.

## 0. Skąd to się bierze

Rozwinięcie formalizmu Chronoprocesu `Ξ=(T,x,Γ,φ)`: gałęzie jako
projekcje jednego wspólnego nośnika (M/S: `x(t)`, G: `Γ(t,s)`, K:
`φ(t)`), most jako właściwe przekształcenie `T:(S_M/S,S_G,S_K)→
(S_M/S',S_G',S_K')` między przestrzeniami stanów gałęzi, nie ad hoc
łatana konstrukcja na jednym sygnale. Tu formalizujemy konkretną parę
`(S_G, S_G')` i konkretne `T_G` między nimi.

**Warunek wbudowany w definicję `S_G` (wprost, nie empirycznie)**:
`Γ:T×C→ℝ`, `Γ(t,c_i)=x_{c_i}(t)`, należy do `S_G` tylko wtedy, gdy `C`
zawiera ≥3 kanały, których niezależność (§3.1) jest liczbowo
sprawdzona — nie kopie jednego sygnału, nie sztucznie zanurzony jeden
kanał. To jest bezpośrednia lekcja z porażki v0.1-v0.3 (fałszywa
rodzina jednoelementowa) i sukcesu membrany (prawdziwa rodzina),
zapisana tym razem jako warunek DEFINICYJNY, nie diagnoza post-hoc.

## 1. Audyt nazw PRZED użyciem

Sprawdzone grepem na całym drzewie `GIA-TIMDR` (kod + docs):
`chrono_sphere`, `sphere_bridge` — **zero kolizji**. `T_G`, `S_G`,
`S_G'` są notacją formalną z `docs/theory/TIMDR_Chronoprocess.md`,
używaną tu po raz pierwszy jako nazwa konkretnej, policzalnej
konstrukcji, nie nowym obiektem konkurencyjnym wobec niego.

## 2. Co jest dostępne (zbadane PRZED projektowaniem metryk)

Źródło: `TIMDR-Industrial-Predict/data/cwru_bearing/b4_raw/source_mirror/
Data/1797 RPM/`, mirror `srigas/CWRU_Bearing_NumPy`.

| plik | klasa | kanały | próbki | SHA-256 (skrót) |
|---|---|---|---|---|
| `1797_Normal.npz` | zdrowe | **DE, FE** (brak BA) | 243 938 | `4cd7f6…c0e26` |
| `1797_IR_21_DE12.npz` | uszkodzenie bieżni wewnętrznej, 0.021" | DE, FE, BA | 122 136 | `4fe4b0…8b9c33` |
| `1797_OR@6_21_DE12.npz` | uszkodzenie bieżni zewnętrznej, 0.021" | DE, FE, BA | 122 426 | `068d40…824c8c` |
| `1797_B_21_DE12.npz` | uszkodzenie kulki (ball fault), 0.021" | DE, FE, BA | 121 991 | `114755…1ea1818` |

Czwarty plik (`B_21`) dopisany 2026-09-22, pobrany przez właściciela
projektu z `github.com/srigas/CWRU_Bearing_NumPy` (mirror publiczny),
skopiowany do `source_mirror` i zweryfikowany hashem SHA-256 (zgodność
kopii lokalnej i pobranej: potwierdzona, identyczny skrót).

**Audyt katalogu źródła (`source_mirror/Contents.md`, wszystkie
udokumentowane RPM: 1730/1750/1772/1797)**: plik `Normal` **nigdy nie
ma kanału BA, przy żadnej prędkości obrotowej** — to jest strukturalna
cecha całego zbioru CWRU (inny zestaw czujników przy nagrywaniu
zdrowej pracy), nie luka w pobranych danych. **Konsekwencja: porównanie
NORMAL vs uszkodzenie z pełną trójką kanałów (DE,FE,BA) jako osiami
sfery jest niewykonalne z tym zbiorem, niezależnie od tego, ile
dodatkowych plików pobierzemy.** To odnotowane wprost jako ograniczenie
danych, zmieniające plan testu real-data z pierwotnie ustalonego
(NORMAL vs IR, NORMAL vs BF) na plan §6 poniżej — decyzja podjęta PRZED
policzeniem czegokolwiek na tych plikach, nie po zobaczeniu wyniku.

## 3. Obiekt geometryczny — konstrukcja (zamrożona)

### 3.1 Bramka niezależności kanałów (warunek wejścia do `S_G`, liczbowy)

Dla trzech kanałów `(c_x,c_y,c_z)` na oknie: macierz korelacji Pearsona
`R∈ℝ^{3×3}`, wartości własne `λ_1≥λ_2≥λ_3≥0` (`eigvalsh`, ujemne
wartości rzędu błędu numerycznego przycięte do 0 — macierz korelacji
jest PSD z konstrukcji, tak jak w membranie §3.2 jej preregu).

```
warunek wejścia:  λ_1 / (λ_1+λ_2+λ_3) < α,   α = 0.9
```

Jeśli `λ_1/Σλ ≥ 0.9`, kanały są funkcjonalnie jednym sygnałem — okno
ODRZUCONE z `S_G`, nie liczone dalej. Reużywa `channel_correlation_matrix`
/ `spectrum_from_correlation` z `timdr_geometry.spectral_family`
(ten sam kod co membrana), nie nowa implementacja.

### 3.2 Transformacja `T_G: S_G → S_G'`

```
v(t) = (|x_DE(t)|, |x_FE(t)|, |x_BA(t)|) ∈ ℝ³      (rektyfikacja, patrz zastrzeżenie niżej)
r(t) = ‖v(t)‖
u(t) = v(t) / r(t)   dla r(t) > 0;   u(t) = u_0 (kierunek bazowy (1,1,1)/√3) dla r(t) = 0
S_G' = {(u(t), r(t)) | u(t) ∈ S², r(t) ∈ ℝ_{≥0}}
```

**Zastrzeżenie zapisane wprost (skorygowane względem pierwszej wersji
propozycji)**: rektyfikacja `|x_c(t)|` NIE stabilizuje `r(t)` — `r(t) =
√(x_DE²+x_FE²+x_BA²)` jest identyczne z wersją bez wartości bezwzględnej,
bo podniesienie do kwadratu usuwa znak niezależnie od kolejności.
Rzeczywisty efekt rektyfikacji: `u(t)` jest ograniczone do DODATNIEGO
OKTANTU sfery (każda współrzędna ≥0), więc maksymalny możliwy kąt
między dwoma punktami `u(t)` wynosi `π/2`, nie `π`. To świadoma decyzja
interpretacyjna — `u(t)` reprezentuje względną dominację kanałów
(który kanał niesie najwięcej amplitudy w danej chwili), nie kierunek
wychylenia ze znakiem. Stabilizację `r(t)` zapewnia WYŁĄCZNIE
mechanizm progu+maski (§3.3), nie rektyfikacja.

### 3.3 Stabilizacja `r(t)` (próg + maska)

Na każdym oknie: `r_min = percentyl 20% rozkładu r(t) w tym oknie`,
maska `M(t) = 1` jeśli `r(t) ≥ r_min`, inaczej `0`. Metryki na `u(t)`
liczone WYŁĄCZNIE dla `M(t)=1`; agregacje ważone przez `r(t)`.

## 4. Metryka: ważona prędkość kątowa `Ω_win` (zamrożona)

```
ω(t) = arccos(u(t)·u(t+Δt))     jeśli M(t)=1 i M(t+Δt)=1, inaczej brak wartości
Ω_win = Σ_{t∈oknie} r(t)·ω(t)  /  Σ_{t∈oknie} r(t)      (suma tylko po t z ważną ω(t))
```

Interpretacja: niska `Ω_win` → kierunek dominacji kanałów stabilny w
oknie; wysoka `Ω_win` → kierunek "skacze" między kanałami, potencjalnie
odpowiadając defektowi/zmianie reżimu.

**Trzy wartości `Δt` sprawdzane dla stabilności znaku (nie jedna)**:
`Δt ∈ {1, 10, 50}` próbek (przy fs=12kHz: ≈83µs, 833µs, 4.2ms). Efekt
uznany za stabilny tylko jeśli kierunek (który typ uszkodzenia ma
wyższe `Ω_win`) i istotność są spójne we wszystkich trzech — ta sama
dyscyplina co przy rozmiarach okna w membranie/cone.

**Okno**: `T_win = 1.0 s` (12000 próbek przy fs=12kHz), nakładanie 50%
(krok 0.5 s). Bramka niezależności (§3.1) liczona osobno na każdym
oknie 1.0 s — okna, które jej nie przejdą, są odrzucane z analizy
(nie całe nagranie na raz).

## 5. Kontrole syntetyczne (zamrożone PRZED implementacją)

`N_CHANNELS=3`, `WINDOW_SIZES` syntetyczne w próbkach zgodne z 1.0 s
przy założonym `fs=1000` (skala syntetyczna niezależna od CWRU, jak w
membranie): `{500, 1000, 2000}`. `SEED=0`, `N_WINDOWS=30`, `ALPHA=0.05`.

- **(a) POZYTYWNA — trzy niezależne kanały szumu + wstrzyknięty NAGŁY
  skok kierunku w połowie okna**: `x_i(t) = N(0,σ²)` dla `t<T/2`, po
  czym w drugiej połowie jeden z trzech kanałów dostaje dodany trwały
  offset (`+K`, `K` duże względem `σ`), zmieniając dominujący kierunek
  `u(t)` skokowo. Przewidywanie: `Ω_win` istotnie WYŻSZE niż (b), bo
  pojawia się jeden duży skok `ω(t)` w połowie okna, ważony wysokim
  `r(t)` w tym momencie (offset zwiększa też `r(t)`).
- **(b) NEGATYWNA — trzy NIEZALEŻNE kanały szumu, bez żadnego
  wspólnego składnika ani skoku, przez cały czas**: `x_i(t) =
  N(0,σ²)`, każdy kanał niezależny. Przewidywanie: bramka niezależności
  (§3.1) będzie PRZEPUSZCZAĆ większość takich okien (trzy niezależne
  szumy nie są z definicji silnie skorelowane) — sprawdzane wprost, nie
  zakładane; `Ω_win` powinno być znacząco niższe niż (a), bez
  systematycznego trendu.
- **(c) BRAMKA — trzy kopie tego samego sygnału + znikomy szum**:
  `x_i(t) = s(t) + N(0, ε²)`, `ε` małe. Przewidywanie: bramka
  niezależności (§3.1) ODRZUCI niemal wszystkie takie okna
  (`λ_1/Σλ ≈ 1`) — to jest test SANITY samej bramki, osobny od testu
  na `Ω_win`, uruchamiany PRZED testem (a) vs (b). Jeśli bramka NIE
  odrzuci (c), zatrzymanie — sama bramka jest wadliwa, nie ma sensu
  testować dalej.

**Kolejność**: najpierw (c) — sanity bramki; jeśli przejdzie, dopiero
wtedy (a) vs (b) na `Ω_win`, Mann-Whitney U + rank-biserial `r`,
oczekiwane `p<0.05`, `|r|≥0.3`, kierunek `median(a) > median(b)`,
sprawdzone dla wszystkich trzech `Δt` z §4. Jeśli którykolwiek etap nie
przejdzie zgodnie z przewidywaniem — ZATRZYMANIE, zgłoszenie na etapie
kontroli, bez dotykania danych CWRU (ta sama dyscyplina co v0.3
chrono_cone).

## 6. Realne dane (URUCHAMIANE WYŁĄCZNIE, jeśli §5 przejdzie)

**Plan skorygowany względem pierwotnych ustaleń** (§2): brak trzeciego
kanału w `Normal` uniemożliwia NORMAL vs fault z pełną trójką osi.
Primarny test v0.1 to **trzy porównania fault-vs-fault**, ten sam RPM
(1797) i ta sama średnica defektu (0.021") we wszystkich trzech
plikach — uczciwe porównanie, bo jedyna różnica to TYP uszkodzenia:

1. IR_21 vs OR@6_21 (bieżnia wewnętrzna vs zewnętrzna)
2. IR_21 vs B_21 (bieżnia wewnętrzna vs kulka)
3. OR@6_21 vs B_21 (bieżnia zewnętrzna vs kulka)

Segmentacja: nieprzecinające się okna 1.0 s / 50% nakładania (§4),
`N_WINDOWS=30` losowych segmentów na plik (bez powtórzeń, gdy dostępne
≥30 — przy najkrótszym pliku B_21, 121 991 próbek, 12000/okno,
~50% overlap → ~19 nieprzecinających się bloków niezależnych plus
nakładające się, wystarczająco), `SEED=0`.

Metryka: `Ω_win`, liczona dla `Δt∈{1,10,50}` próbek (§4). Mann-Whitney U
+ rank-biserial `r` dla każdej z trzech par i każdego `Δt` (9 testów
łącznie) — **korekta Bonferroniego**: próg istotności `α_corr =
0.05/9 ≈ 0.0056` dla klasyfikacji SUPPORTED per para, żeby nie
zawyżać liczby "odkryć" przez wielokrotne porównania.

**Kierunek NIE jest przewidziany a priori dla par fault-vs-fault** (w
odróżnieniu od membrany, gdzie kierunek normal-vs-fault miał fizyczne
uzasadnienie) — nie ma z góry oczywistego powodu, dlaczego jeden typ
uszkodzenia miałby dawać wyższe `Ω_win` niż inny. Test jest więc
DWUSTRONNY (`alternative="two-sided"`), a wynik zgłoszony jako "różnią
się" / "nie różnią się", bez z góry narzuconego kierunku — uczciwie
eksploracyjny na poziomie kierunku, ale zamrożony na poziomie metryki i
progu.

## 7. Klasyfikacja końcowa (ustalona z góry)

**SUPPORTED** (dla danej pary plików) = `p<0.0056` (po korekcie
Bonferroniego) i `|r|≥0.3`, ORAZ znak/kierunek spójny między wszystkimi
trzema `Δt`. **NIESTABILNY** = istotne przy części `Δt`, ale znak się
zmienia między nimi — traktowane jako BRAK potwierdzenia, nie
promowane. **NOT_SUPPORTED** = `p≥0.0056` przy ≥10 ważnych oknach w
grupie. **INCONCLUSIVE** = <10 ważnych okien (po odrzuceniu przez
bramkę §3.1 i maskę §3.3) w którejś grupie — odnotowane wprost jako
brak mocy, nie jako potwierdzony brak efektu (dyscyplina z
Krakow_Centrum, §2 protokołu w skillu).

## 8. Status

Zamrożone. Kolejność wykonania: (1) `core/chrono_sphere_bridge.py` —
konstrukcja + bramka + generatory syntetyczne + kontrole (§5),
uruchomione NAJPIERW; (2) jeśli kontrole PASSED:
`core/real_chrono_sphere_bridge.py` — trzy porównania fault-vs-fault na
CWRU (§6); (3) `docs/geometry/RESULT_CHRONO_SPHERE_BRIDGE_v0.1.md` z
pełnymi liczbami dla wszystkich 9 testów, łącznie z wynikami
negatywnymi/niestabilnymi, bez retuningu po fakcie. Jeśli kontrole NIE
przejdą: zatrzymanie, zgłoszenie na etapie kontroli, bez realnych
danych.
