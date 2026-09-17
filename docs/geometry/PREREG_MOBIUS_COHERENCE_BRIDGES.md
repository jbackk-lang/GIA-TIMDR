# Pre-rejestracja: dwa kandydujące (NIE ustalone) mosty 2-gałęziowe wyrosłe z propozycji `MöbiusCoherence(S)` — `MC_{K↔G}` i `MC_{M/S↔G}` na REALNYCH danych (3 domeny × 2 mosty)

> **Kolejność, jawnie.** W odróżnieniu od mostu łożyskowego
> (`PREREG_REAL_BEARING_NOISE_ROBUSTNESS.md`, napisanego PO fakcie na
> wyraźną prośbę użytkownika), ten dokument wraca do standardowej
> kolejności ekosystemu: freeze → run. Ten plik zamraża wszystkie
> parametry PRZED napisaniem `core/real_mobius_kg_bridge.py` i
> `core/real_zero_mode_topology_bridge.py` oraz PRZED jakimkolwiek
> uruchomieniem ich na realnych danych. Zadanie #64 (uruchomienie) nie
> zaczyna się, dopóki ten dokument nie jest zacommitowany.

## 0. Kontekst i pochodzenie

Dwa kandydujące mosty powstałe 2026-09-17 z rozbicia 3-gałęziowej
propozycji użytkownika `MöbiusCoherence(S)` (złamała zasadę
nieredukowalności gałęzi — patrz punkt 21 skilla, `AskUserQuestion`,
użytkownik wybrał rozbicie na niezależne kandydaty 2-gałęziowe):

- **`MC_{K↔G}`** (Kandydat B, "czysty") — dopisek w
  `Axioms_K_TIMDR.md` i `Axioms_G_TIMDR_Geometry.md` (most G↔K,
  doprecyzowany operator `MC_{K↔G}(k,n)=T(k,n)·(ω_{k,n}/ω_ref)`).
  Kod: `core/mobius_kg_bridge.py` (13/13 testów syntetycznych —
  "czy operator robi to, co mówi", zero realnych danych).
- **`MC_{M/S↔G}` #1** (Kandydat A po usunięciu ω1, na wyraźny wybór
  użytkownika) — dopisek w `Axioms_S_TIMDR_Signal.md` i
  `Axioms_G_TIMDR_Geometry.md` (tłumienie trybu zerowego `Z0` vs
  koherencja topologiczna `G_i`). Kod:
  `core/zero_mode_topology_bridge.py` (13/13 testów syntetycznych,
  w tym JEDEN jawnie zaraportowany wynik negatywny — `G_i` nie
  separuje na naiwnej konstrukcji syntetycznej, dokładnie powtórzenie
  ustalenia z punktu 19 skilla).

Oba są **jawnie NIE ustalone** — status "kandydat" nie zmienia się
przez sam fakt uruchomienia na realnych danych w tym dokumencie; zmienia
się tylko wtedy, gdy wynik przejdzie test kontrolny (pozytywna+negatywna
kontrola, patrz §5) na co najmniej jednej domenie, i zostanie to jawnie
opisane w `Axioms_*.md` (zadanie #65).

Pytanie użytkownika (roadmap, punkty 2-3): czy `MC_{K↔G}` znajduje coś
sensownego na realnych modalnościach sejsmicznych ("czy jakikolwiek
sygnał modalny zachowuje się Möbiusowo"), i czy `MC_{M/S↔G}` odróżnia
realny sygnał od tła na trzech domenach o różnej OCZEKIWANEJ sile `G_i`
(łożyska silny, sejsmika częściowy, BTC słaby — oczekiwanie użytkownika
sprzed uruchomienia, zapisane tutaj PRZED wynikiem, żeby było
sprawdzalne, czy się potwierdziło).

## 1. Dane (zero nowych plików — reużyte 1:1 z trzech istniejących mostów M/S↔topologia/K)

Zero nowego pozyskiwania danych. Te same trzy domeny, te same pliki, te
same loadery, co w `core/real_{bearing,seismic,btc}_noise_robustness_
bridge.py`:

| Domena | Plik(i) | Loader (reużyty import) | Klasa pozytywna | Klasa negatywna | fs |
|---|---|---|---|---|---|
| Łożyska CWRU | `TIMDR-Industrial-Predict/data/cwru_bearing/*.csv` | `load_real_signals()` | `ir_0021`/`or6_0021`/`b_0021` (defekt) | `normal` (zdrowe) | 12000 Hz |
| Sejsmika Ridgecrest | `TIMDR-Earthquake-Core/data/ridgecrest_2019/.../{CLC,RIO}_HHZ.csv` | `load_station(name)` | `coda` (po `EVENT_IDX`=6004) | `background` (przed) | 100 Hz |
| BTC/USD | `deliverable_timdr_finanse/data/btcusd_1h.csv` | `load_log_returns()` + `split_blocks_by_regime()` | `high_vol` bloki | `low_vol` bloki | brak (zwroty godzinowe, nie sygnał czasowy w sensie fizycznym — patrz §7 zastrzeżenie) |

Trzy niezależne pliki defektu w łożyskach = trzy niezależne
uruchomienia (jak w moście oryginalnym), nie mieszane.

## 2. Generatory (zero nowego kodu generującego — reużyte 1:1)

`make_real_window_injector` (łożyska), `make_region_injector`
(sejsmika), `make_regime_injector` (BTC) — importowane wprost z
istniejących plików mostu M/S↔topologia/K, bez modyfikacji. Ten sam
konwencja: segment deterministyczny z `seed`, szum gaussowski
`sigma_frac·std(segment)` dodany PO wyborze segmentu, `sigma=0.0` = czysty
realny segment (najbardziej informacyjny wiersz siatki, nie
zdegenerowany — patrz uzasadnienie w moście łożyskowym §2).

## 3. Siatka (zero nowych wartości — reużyta 1:1)

| Domena | `WINDOW_SIZES` | `SIGMAS` | `N_WINDOWS` | `SEED` | `ALPHA` |
|---|---|---|---|---|---|
| Łożyska | (32, 64) | (0.0, 0.1, 0.3, 0.5, 1.0) | 30 | 0 | 0.05 |
| Sejsmika | (64, 128) | (0.0, 0.1, 0.3, 0.5, 1.0) | 30 | 0 | 0.05 |
| BTC | (12, 24) | (0.0, 0.1, 0.3, 0.5, 1.0) | 30 | 0 | 0.05 |

Identyczne z trzema istniejącymi mostami — utrzymuje porównywalność
całego ekosystemu (te same okna, ten sam szum, te same seedy).

## 4. Statystyka (zero nowej maszynerii — reużyty 1:1 `run_controls`)

Oba mosty testowane przez ISTNIEJĄCY `timdr_formalism.pipeline.
run_controls()` (Mann-Whitney U + rozmiar efektu rank-biserial,
`passed = (positive.pvalue < alpha) and (negative.pvalue >= alpha)`),
identycznie jak pięć wcześniejszych mostów M/S↔topologia/K. Żadnej nowej
statystyki nie trzeba budować — obie nowe metryki (patrz §5, §6) są
funkcjami `signal_1d -> float`, więc pasują do istniejącego API bez
zmian. Mann-Whitney działa również na metrykach binarnych (0/1) — z
niższą mocą niż na ciągłych, co jest jawnie odnotowane jako ograniczenie
mostu `MC_{K↔G}` (§5), nie ukryte.

## 5. `MC_{K↔G}` — operacjonalizacja na realnych danych (zamrożona)

**Ekstrakcja ω1 (pierwsza istotna częstotliwość, gałąź K).** Reużyty
`timdr_time.fourier_bridge.fft_modalities(window, dt=1/fs,
include_dc=False)` — dokładnie ten sam, już zweryfikowany (10/10
testów) most Fouriera M/S↔K z punktu 5 skilla, nie nowa transformata.
Z listy zwróconych `Modality(f,phi,A)` wybierana jest ta o
NAJWIĘKSZEJ amplitudzie `A` (dominująca częstotliwość); `ω1 = 2π·f_tej_modalności`.

**Siatka `(k,n)` (zamrożona, identyczna z testami syntetycznymi).**
`K_RANGE = range(-6, 7)`, `N_RANGE = range(1, 8)` — te same wartości co
w `tests/test_mobius_kg_bridge.py`, niezmienione.

**Kalibracja `ω_ref` (z tła, PRZED porównaniem pozytywna/negatywna).**
Dla każdej (domena, `window_size`) osobno: `ω_ref := mediana(ω1)`
policzona na 30 oknach klasy NEGATYWNEJ (tło/zdrowe/`low_vol`),
`sigma=0.0`, wybranych generatorem z **seedów 1000–1029** — pula
seedów ROZŁĄCZNA z pulą testową (`seed=0..29` w `run_controls`),
dokładnie ten sam wzorzec rozdziału kalibracja/test co `_CALIB_SEEDS`
w `tests/test_zero_mode_topology_bridge.py`. `ω_ref` liczone RAZ, PRZED
uruchomieniem `run_controls` na klasie pozytywnej, i niezmieniane
potem.

**Metryka (binarna, wejście do `run_controls`).**
```
def mc_k_g_indicator(window):
    modalities, _ = fft_modalities(window, dt=1/fs, include_dc=False)
    f1 = max(modalities, key=lambda m: m.A).f
    omega1 = 2 * pi * f1
    x = omega1 / omega_ref
    k, n = nearest_lattice_point(x, K_RANGE, N_RANGE)
    return 1.0 if is_allowed(k, n) else 0.0
```
Test: czy frakcja "trafień w dozwolony punkt siatki Möbiusa" różni się
istotnie między oknami klasy pozytywnej (defekt/coda/high_vol) a klasy
negatywnej (zdrowe/tło/low_vol) — **nie** test absolutnej frakcji
przeciw modelowi null z losową częstotliwością (to była rozważana
alternatywa, odrzucona na rzecz reużycia istniejącej infrastruktury
pozytywna/negatywna, patrz §4 — słabszy, ale spójny z resztą
ekosystemu wybór, jawnie odnotowany).

## 6. `MC_{M/S↔G}` #1 — operacjonalizacja na realnych danych (zamrożona)

**`Z0`** — bez kalibracji, wzór `Z0=μ²·N/(Σ(S-μ)²+ε)` liczony
bezpośrednio na oknie (już dt/skalo-niezmienniczy, zweryfikowane w
testach syntetycznych).

**`G_i`** — `GiRanges` kalibrowane ODDZIELNIE DLA KAŻDEJ DOMENY (nie
jedna wspólna skala — winding/crossing/phase_winding mają zupełnie
różne rzędy wielkości na wibracjach 12 kHz, sejsmice 100 Hz i
godzinowych zwrotach BTC). Kalibracja: `calibrate_gi_ranges()` na
POŁĄCZONEJ puli 30 okien klasy pozytywnej + 30 okien klasy negatywnej
(ten sam wzorzec "tło mieszane" co `_CALIB_SIGNALS` w
`tests/test_zero_mode_topology_bridge.py`), **seedy 1000–1029**,
`sigma=0.0`, `window_size` = MNIEJSZA wartość z `WINDOW_SIZES` danej
domeny (32 dla łożysk, 64 dla sejsmiki, 12 dla BTC — gęstszy reżim,
już zwalidowany dla winding/crossing/phase w punkcie 19).

**Wagi i `gref` (ciągły wariant) — bez kalibracji, stałe z kodu.**
`w1=w3=0.5`, `gref=1.0` (bo `G_i∈[0,1]` z konstrukcji min-max) —
niezmienione względem domyślnych wartości zamrożonych w
`core/zero_mode_topology_bridge.py`, NIE dostrajane per domena.

**Progi `θ0`, `θG` (binarny wariant) — z tła, per domena.**
`θ0 := mediana(Z0)`, `θG := mediana(G_i)` na TEJ SAMEJ puli
kalibracyjnej (seedy 1000-1029, mieszana pozytywna+negatywna) co
`GiRanges` powyżej — mediana rozkładu tła, nie punkt dostrojony do
maksymalizacji separacji (to złamałoby dyscyplinę anty-numerologii).

**Metryka wejściowa do `run_controls`:** `mc_ms_g_continuous(Z0, G_i,
w1=0.5, w3=0.5, gref=1.0)` — wariant ciągły, większa moc statystyczna
niż binarny na 30 oknach; wariant binarny (`mc_ms_g_binary` z
`θ0`,`θG` powyżej) liczony DODATKOWO i raportowany osobno jako
wartość diagnostyczna (frakcja `True`), nie jako główny test.

## 7. Zastrzeżenia, jawnie, przed zobaczeniem wyniku

1. **BTC nie ma fizycznej częstotliwości w Hz.** Zwroty godzinowe to
   szereg bez ustalonej jednostki czasu fizycznego analogicznej do
   drgań łożyska czy fali sejsmicznej — `ω1` dla BTC jest więc
   częstotliwością kątową PER PRÓBKA (`dt=1` przyjęte umownie), nie
   wielkością fizyczną. Wynik `MC_{K↔G}` na BTC jest z tego powodu
   traktowany jako NAJSŁABSZY dowodowo z trzech domen, niezależnie od
   tego, czy test przejdzie.
2. **`G_i` ma już udokumentowane, dziedziczone ograniczenie**
   (punkt 19/21 skilla): na naiwnej konstrukcji syntetycznej szum
   biały daje WIĘKSZE winding/crossing/phase niż sygnał periodyczny —
   przeciwnie do naiwnej intuicji. Realne dane mogą, ale nie muszą,
   zachowywać się inaczej niż ta synteza; pozytywny wynik na realnych
   danych byłby nowym, dodatkowym ustaleniem, NIE gwarantowanym przez
   konstrukcję operatora.
3. **`MC_{K↔G}` na tle binarnym ma z definicji niższą moc** niż
   metryki ciągłe użyte w pięciu wcześniejszych mostach — 30 okien
   binarnych to mało obserwacji do wykrycia umiarkowanego efektu.
   Wynik "nie przeszło" na tej podstawie NIE jest automatycznie dowodem
   braku efektu (patrz punkt 8 protokołu numerologii w skilu — sprawdź
   moc przed odczytaniem wysokiego p jako potwierdzenia braku efektu).
4. **Oczekiwanie użytkownika sprzed testu** (zapisane w §0): `G_i`
   silny na łożyskach, częściowy na sejsmice, słaby na BTC — spójne z
   już istniejącym wynikiem punktu 19 (łożyska 123/150 w oryginalnym
   moście winding/crossing/phase). Jeśli `MC_{M/S↔G}` powtórzy ten
   wzorzec, to spójność z ustaleniem, NIE nowy, niezależny dowód (te
   same trzy metryki geometryczne wchodzą w skład `G_i`).

## 8. Klasyfikacja selektor vs diagnostyka — odroczona do zadania #65

Zgodnie z lekcją błędu G-Rezonansu (punkt 11 skilla: "rezonans to
diagnostyka na już wybranym kandydacie, nie selektor") — ŻADEN wynik z
tego dokumentu nie będzie użyty do "wybierania" kandydatów wewnątrz
jednej domeny (np. wybierania okna/sigma o najlepszym p). Wynik
raportowany jest w PEŁNEJ siatce (3 domeny × 2 okna × 5 sigm × 2 mosty
= 60 komórek), tak jak w trzech wcześniejszych mostach realnych, nie
jako pojedyncza "najlepsza" liczba. Ostateczna klasyfikacja (czy
`MC_{K↔G}`/`MC_{M/S↔G}` są selektorem czy tylko diagnostyką na już
wybranym kandydacie) następuje PO zobaczeniu pełnej siatki, w zadaniu
#65, i jest zapisywana do `Axioms_S/G/K_TIMDR.md` jawnie, z tym samym
zastrzeżeniem co reszta tych dwóch mostów: kandydat, nie ustalony,
dopóki nie przejdzie kontroli na realnych danych.

## 9. Status

Zamrożone 2026-09-17, PRZED napisaniem `core/real_mobius_kg_bridge.py`
i `core/real_zero_mode_topology_bridge.py`. Żaden parametr powyżej nie
zostanie zmieniony po zobaczeniu wyniku (zadanie #64). Ten plik jest
commitowany OSOBNO, PRZED commitem z kodem/wynikiem — w odróżnieniu od
mostu łożyskowego, tu dowód braku data-snoopingu JEST widoczny w
historii git (kolejność commitów).
