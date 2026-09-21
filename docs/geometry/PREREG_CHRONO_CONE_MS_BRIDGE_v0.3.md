# Pre-rejestracja v0.3: chrono_centrifugal_ratio — siła odśrodkowa (nagromadzony θ² wzmacnia promień)

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> danych REALNYCH (kontrole syntetyczne, w tym kalibracja stałej `k`,
> są dozwolone i wykonane PRZED zapisaniem tego dokumentu w formie
> finalnej — patrz §3, dokładnie ta sama konwencja co kalibracja
> `Q_crit`/`ω_ref` z tła w punktach 16/22 skilla, nie "dotykanie
> danych" w sensie zakazanym przez protokół). Data: 2026-09-21.
> Kontynuacja `PREREG_CHRONO_CONE_MS_BRIDGE_v0.2.md` /
> `RESULT_CHRONO_CONE_MS_BRIDGE_v0.2.md`. v0.1/v0.2 NIE są
> nadpisywane — pozostają udokumentowanymi wynikami (v0.1: negatywny na
> realnych danych; v0.2: prymarna metryka negatywna, sekundarna
> eksploracyjna obiecująca na 4/5 kotwic).

## 0. Skąd to się bierze

Użytkownik zaproponował uwzględnienie **siły odśrodkowej**: utrzymujące
się w czasie kręcenie samo z siebie napędza/powiększa promień —
analogicznie do `F=m·ω²·r` klasycznej mechaniki — NIEZALEŻNIE od tego,
czy sama anomalia sygnału rośnie. Osobno wspomniana została luźna
analogia "spinu fotonu na elektronie".

**Jedno zdanie zastrzeżenia (jak przy odrzuconej wcześniej
`TIMDR_Gravity_Speculative.md`, skill punkt 9)**: analogia
"F=m·ω²·r"/"spin fotonu" jest tu WYŁĄCZNIE inspiracją językową, nie
twierdzeniem fizyki klasycznej/kwantowej budowanym dosłownie w
matematykę — `k` poniżej jest kalibrowaną stałą skalującą tego repo,
nie masą ani stałą fizyczną, `θ` nie jest kątem fizycznego obrotu ciała
w przestrzeni.

## 1. Audyt nazw PRZED użyciem

- `θ_unwrapped(t)` = DOKŁADNIE `core.chrono_cone_bridge_v2.trend_referenced_phase`
  — bez zmian, reużywane. Nazwane "unwrapped" tutaj tylko opisowo: ta
  funkcja JUŻ zwraca kąt nagromadzony (nie modulo `2π`) — to nie jest
  nowy obiekt, tylko nowe zastosowanie istniejącego.
- `r_anomalia(t)` = DOKŁADNIE `core.chrono_cone_bridge.anomaly_radius` —
  bez zmian.
- `chrono_centrifugal_ratio` — sprawdzone grepem: brak kolizji nazwy w
  repo. Nazwa uzasadniona wprost analogią użytkownika ("siła
  odśrodkowa"), odróżniona od `chrono_cone_ratio` (v0.1, koło
  zamachowe) i `chrono_pendulum_ratio`/`net_turn` (v0.2, wahadło).
- "skręt" — jak w v0.1/v0.2, nie używane w kodzie/nazwach.

## 2. Konstrukcja r_total(t) (zamrożona)

**Jedna nowa zmienna względem v0.2** (protokół "jedna zmienna na
raz"): TYLKO wzór na promień. `θ(t)` — bez zmian, dokładnie
`trend_referenced_phase` z v0.2 (kierunek zależny od trendu,
wznoszenie `+2π`/cykl, opadanie `-2π`/cykl, ekstrema zamiast tylko
szczytów).

```
r_total(t) = r_anomalia(t) · (1 + k · θ_unwrapped(t)²)
```

`θ_unwrapped(t)²` zawsze `≥0` — CZŁON WYŁĄCZNIE WZMACNIAJĄCY
(`r_total ≥ r_anomalia` zawsze, nigdy nie zmniejsza promienia).
Fizyczne uzasadnienie: im dłużej i intensywniej sygnał "się kręci"
(naprzemiennie wznosi/opada wg reguły v0.2), tym większy `|θ_unwrapped|`
się nagromadził, i tym silniej wzmacniany jest promień, niezależnie od
samej anomalii `r_anomalia(t)`.

**Alternatywa rozważona i ODRZUCONA**:

```
r_total(t) = r_anomalia(t) + k·ω(t)²,   ω(t) = dθ/dt
```

(chwilowa prędkość kątowa, bliżej dosłownego `F=m·ω²·r`).
**Uzasadnienie odrzucenia**: `ω(t)` jest wielkością CHWILOWĄ (lokalne
tempo zmiany fazy w obrębie segmentu ekstremum-ekstremum — w
konstrukcji v0.2 to stała `±2π/span` w obrębie segmentu, skokowo
zmieniająca się między segmentami), więc TRACI dokładnie tę własność,
którą użytkownik podkreślił wprost słowem "wpadające **w czasie** w
obrót" — akumulację historii kręcenia w oknie, nie tylko stanu w danej
chwili. Sygnał, który obracał się intensywnie przez większość okna, a
uspokoił się tuż przed końcem, miałby w wersji `ω²` mały człon
odśrodkowy na końcu (mimo długiej historii obrotu) — sprzeczne z
intuicją "im dłużej się kręci, tym silniejszy efekt". Wersja
`θ_unwrapped²` (WYBRANA) zachowuje pełną historię przez kumulację.
Dodatkowo `ω(t)` jest tu z definicji stałe kawałkami (schodkowe) w
obrębie segmentu — mnożenie przez nie wprowadziłoby nieciągłości
`r_total(t)` na granicach segmentów, których `θ_unwrapped(t)` (ciągła,
kawałkami liniowa) nie ma.

## 3. Kalibracja stałej `k` (zamrożona METODA, wykonana PRZED realnymi danymi)

**Wymaganie zadania**: `k` musi być dobrane tak, żeby na oknie
syntetycznej kontroli POZYTYWNEJ sam człon odśrodkowy nie dominował nad
`r_anomalia` o więcej niż rząd wielkości — metoda opisana tutaj PRZED
uruchomieniem na realnych danych, bez retuningu po fakcie.

**Operacjonalizacja** ("rząd wielkości" → czynnik `A_MAX=10`,
pre-rejestrowana stała): dla każdego rozmiaru okna `w` używanego
gdziekolwiek w tej rodzinie testów (unia siatek v0.1/v0.2:
`ALL_WINDOW_SIZES = (48, 128, 256, 512, 1024)` — syntetyczna 128/256,
łożyska 256/512, sejsmika 512/1024, BTC 48):

```
k(w) = A_MAX / M(w)
M(w) = mediana, po CALIB_N=30 niezależnych realizacjach kontroli
       POZYTYWNEJ (make_growing_amplitude, core/chrono_cone_bridge.py,
       bez zmian), z max_t θ_unwrapped(t)² w oknie rozmiaru w
```

Seedy kalibracji: `CALIB_SEED=1000`, **rozłączne** z seedami testowymi
(`0..N-1` używanymi w kontrolach/teście głównym) — konwencja identyczna
z kalibracją `ω_ref`/`GiRanges` w punkcie 22 skilla (kalibracja z
osobnej puli, nie z tych samych próbek co test). Mechaniczna,
deterministyczna procedura — zero swobody po zobaczeniu wyniku.

**Wynik kalibracji (wykonanej, zamrożonej, PRZED realnymi danymi)**:

| window_size | M(w) = mediana max θ² | k(w) = 10/M(w) |
|---|---|---|
| 48 | 39.4784 | 0.253303 |
| 128 | 39.4784 | 0.253303 |
| 256 | 39.4784 | 0.253303 |
| 512 | 39.4784 | 0.253303 |
| 1024 | 39.4784 | 0.253303 |

**Nietrywialna, jawnie odnotowana obserwacja PRZED interpretacją
czegokolwiek dalej**: `M(w)` jest identyczne (do 4 miejsc po przecinku)
dla WSZYSTKICH pięciu rozmiarów okna i równe dokładnie `(2π)²=4π²≈39.478`
— tzn. mediana szczytowej wartości `|θ_unwrapped|` na kontroli
pozytywnej wynosi dokładnie `2π` (jeden pełny wychył), NIEZALEŻNIE od
długości okna. To potwierdza ilościowo obserwację z RESULT v0.2 §2
("wahadło, nie koło zamachowe"): `θ_v2` na sygnale oscylacyjnym o
rosnącej OBWIEDNI nie akumuluje się nieograniczenie z liczbą okresów w
oknie (naprzemienne `+2π`/`-2π` w większości się znoszą, z lekkim
neto-dryfem od asymetrii wznoszenie/opadanie przy rosnącej amplitudzie)
— stąd JEDNA stała `k=0.253303` obowiązuje identycznie na całej
siatce, NIE jest to przypadek pięciu różnych wartości, które
"przypadkiem wyszły podobne".

**Jawnie odnotowane ograniczenie kalibracji**: `k` skalibrowane na
SYNTETYCZNEJ kontroli pozytywnej (okres oscylacji `~15` próbek, gładki
sinus + umiarkowany szum) — jeśli realny sygnał (np. wibracje łożysk
przy `fs=12kHz`) ma znacznie więcej/inaczej rozłożonych ekstremów niż
syntetyk tej samej długości okna, `θ_unwrapped` na realnych danych może
osiągać inne typowe wartości szczytowe niż `2π` założone w kalibracji —
`k` NIE jest retuningowane pod realne dane (byłoby to złamaniem
dyscypliny), ale to ograniczenie jest tu odnotowane wprost, PRZED
zobaczeniem, czy ma znaczenie.

## 4. Metryka `chrono_centrifugal_ratio` (zamrożona)

Identyczna konstrukcja brzeg/brzeg co `chrono_cone_ratio` (v0.1) /
`chrono_pendulum_ratio` (v0.2), na `r_total(t)` zamiast `r_anomalia(t)`:

```
chrono_centrifugal_ratio(x) = mean(r_total[last 20%]) / mean(r_total[first 20%])
```

`edge_fraction=0.2`, `NaN` jeśli `θ` niezdefiniowana (<2 ekstrema) LUB
`r_start<1e-9` — identycznie jak v0.1/v0.2.

## 5. Kontrole syntetyczne — KOLEJNOŚĆ ZAMROŻONA: Kontrola #0 (RYZYKO) NAJPIERW

### 5.0 Kontrola #0 (RYZYKO, priorytet — uruchamiana PRZED wszystkim innym)

**Najważniejsze ryzyko tej konstrukcji, zidentyfikowane w zadaniu
PRZED implementacją**: kontrolka NEGATYWNA (czysty szum biały) ma dużo
losowych ekstremów → dużo losowej akumulacji `θ` → `θ_unwrapped(t)²`
jest zawsze `≥0` i WYŁĄCZNIE wzmacnia (nigdy nie tłumi) — więc sam
człon odśrodkowy MOŻE generować fałszywy "lej" z samego szumu,
niezależnie od jakiegokolwiek prawdziwego wzorca.

**Test (PAROWY, nie niezależny)**: dla każdego `w ∈ ALL_WINDOW_SIZES`
(ryzyko rośnie z długością okna — losowy spacer `θ` ma większy typowy
wychył przy większej liczbie kroków, więc test na CAŁEJ siatce okien,
nie tylko syntetycznej 128/256): `N_WINDOWS=30` niezależnych realizacji
`make_white_noise(w, seed)` (te same seedy co konwencja
`SEED=0..N-1`), na KAŻDEJ policzone DWIE wartości — `chrono_pendulum_ratio`
(v0.2, BEZ członu odśrodkowego) i `chrono_centrifugal_ratio` (v0.3, Z
członem) — **na tej samej realizacji szumu**, więc dane są SPAROWANE.

**Uzasadnienie wyboru testu**: dane sparowane (ta sama realizacja
szumu, dwie formuły) łamałyby założenie niezależności Manna-Whitneya —
użyty jest zamiast tego **Wilcoxon signed-rank** (test dla par,
`scipy.stats.wilcoxon`, `alternative="two-sided"`), z analogicznym do
rank-biserial rozmiarem efektu dla par dopasowanych
(`r = (W+-W-)/(W++W-)` na rangach `|różnic|`, zbudowany ręcznie w
`core/chrono_cone_bridge_v3.py::_matched_pairs_rank_biserial`, bo
`pipeline.py` ma gotowy tylko rank-biserial dla Manna-Whitneya, nie dla
par). To jest ŚWIADOMA zmiana statystyki dla INNEGO pytania (czy dwie
formuły na TYCH SAMYCH danych się różnią) niż gdziekolwiek indziej w
tej rodzinie testów (gdzie zawsze porównywano dwie NIEZALEŻNE grupy) —
odnotowane wprost, nie ukryte.

**Decyzja (zamrożona PRZED uruchomieniem)**: `FALSE_SIGNAL` dla danego
`w` = `p<0.05` I `|r_eff|≥0.3` (te same progi co wszędzie w tej
rodzinie testów). Dodatkowo raportowane opisowo: mediany obu metryk i
`spread_inflation = IQR(centrifugal)/IQR(pendulum)` (czy sam człon
odśrodkowy poszerza rozrzut wyniku na czystym szumie, niezależnie od
przesunięcia mediany).

**Jeśli `FALSE_SIGNAL=True` dla KTÓREGOKOLWIEK `w`** (jeden wystarczy —
to jest test na ryzyko, nie na przewagę głosów): **ZATRZYMANIE.**
Zgłoszenie jako wynik na etapie kontroli w
`docs/geometry/RESULT_CHRONO_CONE_MS_BRIDGE_v0.3.md`, BEZ przechodzenia
do kontroli strukturalnej (§5.1) ani do realnych danych (§6).

### 5.1 Kontrola #1 (STRUKTURALNA, jak w v0.1/v0.2) — uruchamiana TYLKO jeśli §5.0 przejdzie

Te same trzy generatory syntetyczne (a: rosnąca amplituda, b: szum
biały, c: stała amplituda), `SYN_WINDOW_SIZES=(128,256)`,
`N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05` — identyczne z v0.1/v0.2, teraz
na `chrono_centrifugal_ratio`. Bramka: pozytywna (a vs b) `p<0.05` duży
efekt; negatywna (b vs c) `p≥0.05`. Jeśli NIE przejdzie zgodnie z
przewidywaniem — ZATRZYMANIE, zgłoszenie na etapie kontroli, bez
realnych danych (jak w v0.1/v0.2).

## 6. Realne dane (URUCHAMIANE WYŁĄCZNIE, jeśli §5.0 I §5.1 obie przejdą)

Te same trzy domeny, te same pliki, te same rozmiary okien co v0.1/v0.2
(dla bezpośredniej porównywalności stabilności znaku):

1. **Łożyska CWRU**: `WINDOW_SIZES=(256,512)`, te same 4 pliki.
2. **Sejsmika Ridgecrest**: `WINDOW_SIZES=(512,1024)`, stacje CLC/RIO,
   `EVENT_IDX=6004`.
3. **BTC/USD**: `BLOCK_SIZE=48h`, `WINDOW_SIZES=(48,)`.

`SIGMAS=(0.0,0.1,0.3,0.5,1.0)`, `N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05`,
`MIN_VALID_PER_GROUP=10` — bez zmian.

**GŁÓWNE pytanie tej sesji (zamrożone)**: czy dodanie członu
odśrodkowego (zależnego od nagromadzonego obrotu) do promienia
POPRAWIA/POGARSZA stabilność znaku efektu WZGLĘDEM v0.2-sekundarnej
(`chrono_pendulum_net_turn`), na tych samych kotwicach: `or6_0021`
(256/512), CLC i RIO (512/1024) — NIE jest to pytanie ogólne "czy
działa".

Klasyfikacja per komórka: `SUPPORTED` = `p<0.05` i `|r|≥0.3` (jak
zawsze). Stabilność znaku: ten sam znak `r` (przy `sigma=0.0`) między
rozmiarami okna tej samej domeny/pliku.

## 7. Status

Zamrożone. Kolejność wykonania: (1) kalibracja `k` — WYKONANA, §3; (2)
Kontrola #0 (ryzyko fałszywego sygnału z szumu, §5.0) — uruchamiana
jako PIERWSZA, wynik decyduje, czy iść dalej; (3) jeśli #0 przejdzie:
Kontrola #1 (strukturalna, §5.1); (4) jeśli obie przejdą: realne dane
(§6), raport w `docs/geometry/RESULT_CHRONO_CONE_MS_BRIDGE_v0.3.md` z
jawnym porównaniem v0.1 (niestabilne) vs v0.2-sekundarna (stabilne na
4/5) vs v0.3 (?) na tych samych kotwicach. Jeśli #0 NIE przejdzie:
zatrzymanie na etapie kontroli, zgłoszenie w RESULT bez realnych
danych, zgodnie z §5.0.
