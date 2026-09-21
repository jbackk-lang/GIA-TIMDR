# Pre-rejestracja v0.2: chrono_pendulum_ratio — kierunek θ zależny od trendu (test hipotezy użytkownika o niestabilności znaku w v0.1)

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> danych (nawet syntetycznych — kod jeszcze nie napisany w chwili
> zapisania tego dokumentu). Data: 2026-09-21. Kontynuacja
> `PREREG_CHRONO_CONE_MS_BRIDGE_v0.1.md` / `RESULT_CHRONO_CONE_MS_BRIDGE_v0.1.md`
> (wynik v0.1: mechanizm poprawny na syntetyce, ale NIEWIARYGODNY na
> realnych danych — kierunek efektu Manna-Whitneya odwracał się przy
> samej zmianie rozmiaru okna). v0.1 NIE jest nadpisywane — pozostaje
> udokumentowanym, uczciwym wynikiem negatywnym.

## 0. Skąd to się bierze

Użytkownik, usłyszawszy o niestabilności kierunku w v0.1, zauważył:
"jeśli kierunek jest zły, to jasne że obrót leja musi być w drugą
stronę". Diagnoza: w v0.1 `θ(t)` rośnie MONOTONICZNIE o dokładnie `2π`
między kolejnymi SZCZYTAMI, niezależnie od tego, czy sygnał akurat
wznosi się czy opada w danej chwili (koło zamachowe, zawsze w jedną
stronę) — pierwotna propozycja użytkownika (sprzed jakiejkolwiek
implementacji) mówiła o czymś innym: wznoszenie i opadanie jako DWA
PRZECIWNE kierunki obrotu. v0.2 formalizuje i testuje DOKŁADNIE tę
zmianę, jako jedyną zmienną różniącą się od v0.1 (protokół: jedna
zmienna na raz, punkt 3 skilla).

## 1. WAŻNE odkrycie mechanizmu, PRZED jakąkolwiek zmianą kodu (audyt v0.1)

Zanim cokolwiek zaimplementowano, przeczytano ponownie
`core/chrono_cone_bridge.py::chrono_cone_ratio()`. Kluczowa obserwacja,
zapisywana tutaj PRZED napisaniem v0.2, bo determinuje, jak w ogóle
interpretować wynik testu poniżej:

```
def chrono_cone_ratio(x, ...):
    theta = peak_referenced_phase(x, ...)
    if theta is None: return nan          # <- JEDYNE uzycie theta
    r = anomaly_radius(x)
    r_start = mean(r[:n_edge]); r_end = mean(r[-n_edge:])
    return r_end / r_start                 # <- wartosc NIE zalezy od theta
```

`θ(t)` wchodzi do wzoru `chrono_cone_ratio` WYŁĄCZNIE jako **bramka
istnienia** (czy jest ≥2 szczyty) — sama WARTOŚĆ liczbowa `ratio` jest
funkcją WYŁĄCZNIE `r(t)` (średnia `|x-mean|/std` w pierwszych/ostatnich
20% okna), nie zależy od kierunku ani wartości `θ`. Konsekwencja: dla
KAŻDEGO okna, które przechodzi bramkę istnienia w OBU wersjach (v0.1 i
v0.2), `chrono_cone_ratio`/`chrono_pendulum_ratio` zwróci **dokładnie tę
samą liczbę** — zmiana kierunku θ per se NIE MOŻE zmienić wartości
metryki dla takiego okna. Zmiana kierunku θ może wpłynąć na wynik
WYŁĄCZNIE przez zmianę SKŁADU zbioru okien przechodzących bramkę (v0.2
liczy ekstrema OBU typów — szczyty i doliny — więc bramka jest z natury
bardziej permisywna niż v0.1, który liczył tylko szczyty).

**To jest zarejestrowane wprost jako ograniczenie testu, nie ukryte.**
Zgodnie z instrukcją priorytetu (uczciwe porównanie z v0.1 na TEJ SAMEJ
metryce promienia, zmieniając TYLKO regułę kierunku), test w §7 poniżej
jest zaprojektowany świadomie jako test **efektu bramki** (czy
symetryczne liczenie ekstremów zmienia, które okna są oceniane, i czy to
stabilizuje znak), NIE jako bezpośredni test geometrycznej rotacji.
Żeby dać hipotezie użytkownika UCZCIWĄ szansę zadziałania przez sam
mechanizm rotacji (nie tylko przez efekt bramki), §6 dodaje DRUGĄ,
jawnie eksploracyjną metrykę (`chrono_pendulum_net_turn`), która
faktycznie używa wartości `θ`, nie tylko jej istnienia.

## 2. Audyt nazw PRZED użyciem

- `chrono_cone_ratio`, `peak_referenced_phase`, `anomaly_radius`,
  `chrono_cone_curve` — istniejące, audytowane obiekty v0.1
  (`core/chrono_cone_bridge.py`). NIE nadpisywane, NIE importowane
  ponownie pod nową definicją — v0.2 żyje w nowym pliku
  `core/chrono_cone_bridge_v2.py` z własnymi nazwami.
- Nowa nazwa metryki: **`chrono_pendulum_ratio`** (zamiast
  `chrono_cone_ratio_v2`) — uzasadnienie: v0.1 dawało kształt
  spirali/koła zamachowego (θ rośnie monotonicznie, jak stożek/lej,
  patrz nazwa "cone"); v0.2 daje kształt OGRANICZONEJ oscylacji kątowej
  (θ wraca w pobliże tej samej wartości po symetrycznym cyklu
  wznoszenie-opadanie, jak wahadło) — nazwa ma jawnie sygnalizować, że
  to INNY obiekt geometryczny, nie wariant tego samego. Druga,
  jawnie eksploracyjna metryka: `chrono_pendulum_net_turn`.
- "skręt" — jak w v0.1, NIE używane w kodzie/nazwach (już 8 kolizji
  symbolu wg punktu 2 skilla); `theta_v2`/`phase` w kodzie.

## 3. θ(t) w wersji 2 — konstrukcja (zamrożona)

**Wspólne z v0.1**: wygładzenie `xs = moving_average(x, smooth_window=5)`
(ten sam `smooth_window`, dla porównywalności — jedyna zmienna to
kierunek). Ekstrema — ścisłe lokalne maksima I ścisłe lokalne minima
wygładzonego sygnału, tylko punkty wewnętrzne.

**Reguła kierunku (zamrożona, główna wersja pre-rejestrowana)**: między
kolejnymi ekstremami `e_k`, `e_{k+1}` (niezależnie od typu — szczyt czy
dolina), kierunek segmentu określa ZNAK zmiany wartości:
`direction = +1 jeśli xs[e_{k+1}] > xs[e_k] (WZNOSZENIE), -1 jeśli
xs[e_{k+1}] < xs[e_k] (OPADANIE)`. Faza w segmencie rośnie/maleje
LINIOWO o dokładnie `direction · 2π` (interpolacja liniowa indeksu
próbki wewnątrz segmentu, dokładnie jak w v0.1, tylko ze znakiem):

```
theta[e_k : e_{k+1}] = cum_k + direction * 2*pi * (t_local / span)
cum_{k+1} = cum_k + direction * 2*pi
```

Przed pierwszym ekstremum: faza=0 (płasko, jak w v0.1). Po ostatnim:
faza zamrożona na `cum_final` (płasko). Jeśli <2 ekstrema (dowolnego
typu) → `θ` NIEZDEFINIOWANE (`None`), jak w v0.1.

**Wybór wzoru skalującego — DWIE rozważone możliwości, JEDNA wybrana:**

- **Opcja A (WYBRANA, główna)**: stała "prędkość kątowa" w obrębie
  segmentu (liniowa rampa `2π/span` próbek), ZNAK zależny WYŁĄCZNIE od
  kierunku trendu (wznoszenie/opadanie), NIEZALEŻNIE od tempa
  (`|dx/dt|`) ani amplitudy zmiany. Każdy pełny segment
  ekstremum→ekstremum to dokładnie jeden pełny obrót `±2π`,
  niezależnie od tego, jak stromo/płasko przebiegał.
- **Opcja B (ODRZUCONA)**: `|dθ/dt| ∝ |dx/dt|` znormalizowane (ciągła
  akumulacja proporcjonalna do chwilowego nachylenia). Odrzucona z
  trzech powodów zapisanych PRZED wyborem: (1) wymaga NOWEJ, dowolnej
  stałej normalizującej (skala nachylenia → skala kątowa) — dodatkowy
  wolny parametr, którego v0.1 nie miał, łamiący zasadę "jedna zmienna
  na raz"; (2) matematycznie, całkowanie `dθ = c·(dx/dt)·dt` po prostu
  daje `θ(t) ≈ c·x(t) + const` — embedding `(r·cosθ, r·sinθ)` zredukowałby
  się do reparametryzacji SUROWEGO sygnału `x(t)` samego w sobie, tracąc
  ideę "jeden pełny obrót ~ jeden pełny cykl oscylacji", która była
  sednem geometrycznej intuicji v0.1/v0.2; (3) niepotrzebna złożoność
  wobec wprost sformułowanej w zadaniu zasady "nie komplikuj ponad
  potrzebę" — Opcja A jest MINIMALNĄ zmianą v0.1 (ten sam mechanizm
  "jeden segment = jeden pełny obrót", tylko teraz symetrycznie
  ±, zamiast zawsze +).

**Efekt fizyczny, jawnie przewidziany PRZED uruchomieniem**: dla
symetrycznego cyklu dolina→szczyt→dolina o tej samej "drodze" w górę i
w dół, `θ` przechodzi `0 → +2π → +2π-2π = 0` — WRACA dokładnie do tej
samej wartości (mod nic, nie tylko mod 2π — dokładnie ta sama liczba),
zamiast robić pełny obrót `+4π` jak zrobiłby v0.1 (dwa szczyty
policzone jako dwa pełne obroty w tę samą stronę). To JEST bezpośrednio
testowalna, ilościowa różnica między v0.1 a v0.2 — sprawdzana w §6 jako
kontrola sanity, PRZED realnymi danymi.

## 4. r(t), z(t) — BEZ ZMIAN względem v0.1 (zamrożone)

`r(t) = |x(t)-mean(x_window)|/std(x_window)` (ciągła anomalia,
identyczna z v0.1 §3). `z(t)=t` (Chronoproces, jednoelementowe
uproszczenie, identyczne z v0.1 §4). Żadna stała, żaden wzór tutaj nie
zmienia się — jedyna zmienna eksperymentu to reguła kierunku θ (§3).

## 5. Metryki (zamrożone)

**Primarna, dla bezpośredniej porównywalności z v0.1**:

```
chrono_pendulum_ratio(x) = mean(r[last edge_fraction]) / mean(r[first edge_fraction])
```

Identyczny wzór co `chrono_cone_ratio` (`edge_fraction=0.2`,
`n_edge=max(2, round(0.2n))`), gated na `theta_v2 is not None` (≥2
ekstrema DOWOLNEGO typu — różnica od v0.1, który wymagał ≥2 SZCZYTÓW).
`NaN` jeśli `θ` niezdefiniowane LUB `r_start<1e-9`, identycznie jak
v0.1.

**Sekundarna, jawnie eksploracyjna (NIE używana do klasyfikacji
SUPPORTED/NOT_SUPPORTED w §7, tylko raportowana obok)**:

```
chrono_pendulum_net_turn(x) = (theta_v2[-1] - theta_v2[0]) / (2*pi)
```

Liczba NETTO pełnych obrotów zakumulowanych w oknie — w odróżnieniu od
`ratio`, ta wielkość FAKTYCZNIE zależy od wartości `θ`, nie tylko jej
istnienia. Dodana, żeby dać hipotezie użytkownika (rotacja jako nośnik
informacji) uczciwą szansę zadziałania przez sam mechanizm geometryczny,
nie tylko przez efekt bramki (§1). Traktowana jako DIAGNOSTYKA
dodatkowa, nie zastępuje ani nie zmienia klasyfikacji głównej metryki.

## 6. Kontrole syntetyczne (zamrożone, PRZED implementacją) — uruchomić NAJPIERW

Te same trzy generatory co v0.1 (`make_growing_amplitude`,
`make_white_noise`, `make_constant_amplitude`, `core/chrono_cone_bridge.py`,
`OMEGA=2π/15`, bez zmian) — reużyte 1:1, nie definiowane od nowa.

- **(a) POZYTYWNA — amplituda rosnąca**: przewidywanie: `chrono_pendulum_ratio`
  istotnie WYŻSZY niż (b), mediana wyraźnie >1 — **identyczne
  przewidywanie jak w v0.1**, bo `ratio` nie zależy od kierunku θ dla
  okien przechodzących bramkę (§1) — to jest OCZEKIWANY null-result
  względem v0.1 na tej konkretnej kontroli, zapisany wprost PRZED
  uruchomieniem, nie niespodzianka po fakcie.
- **(b) NEGATYWNA A — szum biały**: przewidywanie: `ratio` bliski 1,
  identyczne jak v0.1.
- **(c) NEGATYWNA B — stała amplituda**: przewidywanie: `ratio` bliski 1
  (jak v0.1) ORAZ dodatkowa kontrola sanity (nowa w v0.2, §3 efekt
  fizyczny): `chrono_pendulum_net_turn` dla (c) powinien być bliski 0
  (wahadło wraca blisko startu każdy pełny cykl), WYRAŹNIE bliższy 0 niż
  odpowiadający mu narastający `θ_v1_final/(2π)` z v0.1 na tym samym
  sygnale (który rośnie z liczbą szczytów, bez ograniczenia). To jest
  bezpośredni, ilościowy test twierdzenia z §3 o "wahadle vs kole
  zamachowym" — jeśli NIE potwierdzi się nawet na tej najprostszej
  syntetyce, to podważa samą konstrukcję θ_v2 i zatrzymujemy się tu,
  zanim dotkniemy realnych danych.

**Bramka**: jak w v0.1 — kontrola POZYTYWNA: (a) vs (b), oczekiwane
p<0.05, duży efekt. Kontrola NEGATYWNA: (b) vs (c), oczekiwany brak
istotnej różnicy. `MIN_VALID_FRAC=0.5` (jak v0.1). Jeśli bramka NIE
przejdzie zgodnie z przewidywaniem — ZATRZYMANIE, zgłoszenie jako wynik
na etapie kontroli, BEZ przechodzenia do realnych danych (jak w v0.1
§10).

Siatka: `WINDOW_SIZES=(128, 256)`, `N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05`
— identyczne z v0.1 §7 (bez zmian, dla porównywalności).

## 7. GŁÓWNE PYTANIE testowane na realnych danych (zamrożone PRZED uruchomieniem)

**Dokładne pytanie**: czy zmiana kierunku θ (v0.1→v0.2) sprawia, że
ZNAK efektu (rank-biserial `r` testu Manna-Whitneya na
`chrono_pendulum_ratio`) przestaje się odwracać między rozmiarami okna
na TYCH SAMYCH realnych sygnałach, gdzie w v0.1 się odwracał — **NIE
jest to pytanie "czy wynik końcowy (SUPPORTED/NOT_SUPPORTED) jest
pozytywny"** — to jest inne, węższe i bardziej precyzyjne pytanie,
testowane niezależnie od tego, czy ogólny wynik na łożyskach/sejsmice/
BTC wypadnie pozytywnie czy negatywnie.

**Konkretna przewidywana odpowiedź (zapisana PRZED uruchomieniem, na
podstawie analizy mechanizmu z §1)**: **przewidujemy, że niestabilność
znaku NIE zniknie w pełni** — bo `chrono_pendulum_ratio` dla okna, które
przechodzi bramkę w OBU wersjach, zwraca DOKŁADNIE tę samą liczbę co
`chrono_cone_ratio` (§1); zmiana kierunku θ może zmienić znak WYŁĄCZNIE
pośrednio, przez zmianę składu zbioru ważnych okien (bramka licząca też
doliny, nie tylko szczyty). Jeśli niestabilność znaku w v0.1 wynikała
głównie z samego zachowania `r(t)` na typowych oknach (niezależnie od
tego, które konkretnie okna przeszły bramkę), znak POZOSTANIE
niestabilny w v0.2 w tym samym stopniu. Jeśli natomiast niestabilność
była napędzana głównie oknami BLISKO granicy bramki (mało
ekstremów, więc losowo wchodzące/wypadające z próby), zmiana bramki MOŻE
ją zmniejszyć. **Testujemy to bezpośrednio, nie zakładamy z góry, która
możliwość jest prawdziwa** — obie są jawnie dopuszczone jako wynik.
Dodatkowo raportujemy `chrono_pendulum_net_turn` (§5) na tych samych
oknach jako niezależną, eksploracyjną sprawdzian, czy metryka faktycznie
używająca wartości θ (nie tylko bramki) zachowuje się inaczej.

**Te same trzy domeny, te same rozmiary okien co v0.1** (dla
bezpośredniej porównywalności testu stabilności znaku):

1. **Łożyska CWRU**: `WINDOW_SIZES=(256, 512)`, te same 4 pliki
   (`normal_1797_de_first1536.csv` vs `ir_0021`/`or6_0021`/`b_0021`).
   Przykład-kotwica z v0.1: `or6_0021` zmienił znak między oknem 256
   (`r=-0.189`) a 512 (`r=+0.267`).
2. **Sejsmika Ridgecrest**: `WINDOW_SIZES=(512, 1024)`, te same 2
   stacje (CLC, RIO), ten sam `event_idx=6004`. Przykład-kotwica z
   v0.1: OBIE stacje zmieniły znak między oknem 512 a 1024 (CLC:
   `+0.271→-0.164`, RIO: `+0.393→-0.216`).
3. **BTC/USD**: `BLOCK_SIZE=48h`, `WINDOW_SIZES=(48,)` (jedyny rozmiar
   — jak v0.1, brak testu stabilności międzyokiennej dla tej domeny z
   tego samego powodu strukturalnego co w v0.1 §8.3).

`SIGMAS=(0.0, 0.1, 0.3, 0.5, 1.0)`, `N_WINDOWS=30`, `SEED=0`,
`ALPHA=0.05`, `MIN_VALID_PER_GROUP=10` — bez zmian względem v0.1 §8-9.

## 8. Klasyfikacja wyniku (ustalona z góry)

Per komórka: **SUPPORTED** = `p<0.05` i `|r|≥0.3` (jak v0.1).
**Stabilność znaku** (GŁÓWNA miara tej sesji, per sygnał/domena,
niezależna od SUPPORTED/NOT_SUPPORTED): znak `r` przy `sigma=0.0`
porównany między dostępnymi rozmiarami okna dla tego samego
pliku/stacji. **ZNAK STABILNY** = ten sam znak we wszystkich rozmiarach
okna tej domeny. **ZNAK NIESTABILNY** = różny znak między rozmiarami.
Ostateczny werdykt tej sesji: **hipoteza użytkownika POTWIERDZONA**
jeśli odsetek sygnałów ze STABILNYM znakiem w v0.2 jest wyraźnie wyższy
niż w v0.1 (gdzie było to: łożyska 2/3 stabilne co do znaku wśród
`SUPPORTED`, ale globalnie 16/14 na 30 blisko losowego; sejsmika 0/2
stabilne — OBIE stacje flipowały); **NIEPOTWIERDZONA** jeśli odsetek
jest podobny lub gorszy — **niezależnie** od tego, czy ogólny odsetek
SUPPORTED jest wyższy czy niższy niż w v0.1.

## 9. Status

Zamrożone. Następny krok: implementacja `core/chrono_cone_bridge_v2.py`,
testy jednostkowe `tests/test_chrono_cone_bridge_v2.py`, uruchomienie
NAJPIERW kontroli syntetycznych (§6) — jeśli bramka kontrolna LUB
sanity-check "wahadło wraca do zera" nie przejdą zgodnie z
przewidywaniem, ZATRZYMANIE i zgłoszenie jako wynik na etapie kontroli,
BEZ realnych danych. Jeśli kontrole przejdą: §7-8 na trzech domenach,
raport w `docs/geometry/RESULT_CHRONO_CONE_MS_BRIDGE_v0.2.md` z pełnym,
jawnym porównaniem stabilności znaku v0.1 vs v0.2 na tych samych
przykładach-kotwicach.
