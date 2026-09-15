# Pre-rejestracja: most M/S↔topologia/K na REALNYCH danych sejsmicznych (Ridgecrest 2019) + szum syntetyczny

> Drugi most na realnych danych (po `PREREG_REAL_BEARING_NOISE_ROBUSTNESS.md`
> / `RESULT_REAL_BEARING_NOISE_ROBUSTNESS.md` — 123/150, silny efekt
> odporny na szum, ale częściowo wyjaśniony kurtozą). Tym razem
> STANDARDOWA kolejność (freeze→build), nie odwrócona jak poprzednio —
> ten dokument powstaje PRZED uruchomieniem kodu.

## 0. Dane i definicja pozytyw/negatyw (zamrożona, weryfikowalna niezależnie od danych)

Realny sejsmogram mainshocku M7.1 Ridgecrest, dwie stacje, kanał HHZ,
100Hz, 36001 próbek (360s), plik `t,amplituda`:
`TIMDR-Earthquake-Core/data/ridgecrest_2019/real_waveform_CLC_RIO/
{CLC_HHZ,RIO_HHZ}.csv`.

**Punkt podziału pozytyw/negatyw NIE jest wybrany z danych** — jest
obliczony z realnego, publicznie znanego czasu mainshocku
(`2019-07-06T03:19:53.040Z`, katalog USGS) względem realnego czasu
startu śladu (`2019-07-06T03:18:52.998Z`, ten sam sposób co w
istniejącym `scripts/real_waveform_test.py` tego repo-siostry, gdzie
`event_idx` był już raz policzony tą samą metodą):

```
event_idx = round((mainshock - starttime) * fs) = round(60.042 * 100) = 6004
```

Zweryfikowane w sandboxie PRZED napisaniem reszty tej pre-rejestracji
(dopuszczalne: to jest weryfikacja arytmetyki znanej daty, nie
podglądanie wyniku testu).

- **Region negatywny (tło)**: próbki `[0, 6004)` — 60s PRZED
  mainshockiem, sejsmicznie ciche.
- **Region pozytywny (koda/wstrząs)**: próbki `[6004, 36001)` — od
  mainshocku do końca śladu, obejmuje silne wstrząsanie i kodę.

## 1. Metryki (bez zmian względem wszystkich poprzednich mostów)

Reużyte 1:1: `torsion_max|tau|`, `winding_number`, `crossing_number`,
`h1_persistence`, `phase_winding`.

## 2. Generator: okno realnego regionu + szum (identyczna konstrukcja co w moście łożyskowym)

Segmentacja regionu na NIEZACHODZĄCE bloki `window_size` próbek.
Segment wybierany deterministycznie z `seed` (modulo liczba dostępnych
segmentów w danym regionie). Szum gaussowski
`N(0, sigma_frac·std(segment))` dodany PO wyborze segmentu.
`positive_injector` losuje z regionu pozytywnego, `negative_generator_
a`/`negative_generator_b` losują OBA z regionu negatywnego (tła) —
tak jak w moście łożyskowym, jedyna niezależność między nimi to
przesunięcie seeda +1 wewnątrz `run_controls()`; mamy tylko jeden
ciągły region tła na stację.

## 3. Siatka (zamrożona)

`WINDOW_SIZES=(64,128)` — przy 100Hz to 0,64s i 1,28s; region tła
(6004 próbek) daje 93/46 dostępnych segmentów, region pozytywny
(29997 próbek) daje 468/234 — oba regiony mają WIĘCEJ segmentów niż
`N_WINDOWS=30` dla obu rozmiarów okna, więc (w odróżnieniu od mostu
łożyskowego przy oknie=64) reużycie tego samego segmentu NIE powinno
być konieczne — jeśli jednak wystąpi, zostanie to odnotowane w
wyniku tak jak poprzednio, nie ukryte.
`SIGMAS=(0.0,0.1,0.3,0.5,1.0)` — ułamek własnego std segmentu,
identyczna siatka nominalna co w poprzednich mostach.
`N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05` — bez zmian.
Dwie stacje (`CLC`, `RIO`) — DWA NIEZALEŻNE przebiegi (różne
instrumenty, różna odległość/kierunek od epicentrum), nie mieszane —
to najbliższe temu ekosystemowi pojęcie replikacji między
"egzemplarzami" tego samego zdarzenia.

Łącznie: 2 stacje × 5 metryk × 2 okna × 5 sigm = **100 komórek**.

## 4. Oczekiwania a priori — PRZED uruchomieniem

**Pesymistyczne co do interpretacji, niepewne co do surowego wyniku.**
Region pozytywny obejmuje silne wstrząsanie o amplitudzie rzędu
10-100× większej niż tło (widoczne już w nagłówku pliku — `t=0`:
amplituda ~18754, ale nie sprawdzałem amplitud W REGIONIE POZYTYWNYM
przed napisaniem tego dokumentu, żeby nie podglądać). Ponieważ
`metric_fn` normalizuje `(x-mean)/std` PRZED liczeniem, różnica samej
SKALI amplitudy jest usuwana — ale, dokładnie jak w moście łożyskowym,
silne wstrząsanie sejsmiczne ma inny KSZTAŁT statystyczny niż szum tła
(inna gęstość widmowa, możliwa impulsowość/kurtoza fal P/S vs szum
mikrosejsmiczny) — **a priori oczekuję, że separacja (jeśli wystąpi)
będzie przynajmniej częściowo wyjaśnialna tym samym mechanizmem co w
moście łożyskowym (kurtoza/kształt), nie automatycznie czymś
specyficznie topologicznym** — ta sama kontrola porównawcza (kurtoza
jako osobna `metric_fn` przez `run_controls()`) zostanie wykonana
PO głównym wyniku, zanim sformułuję wniosek końcowy.

Co do SUROWEGO wyniku (przejdzie/nie przejdzie): brak pewnej
prognozy ilościowej — w przeciwieństwie do mostu OAM. Zgodnie z
wynikiem łożyskowym, spodziewam się, że przynajmniej część komórek
przejdzie (bo obie serie "realne dane" dotąd dawały nietrywialny
sygnał, w przeciwieństwie do czysto syntetycznej serii pięciu prób).

## 5. Ograniczenie zdefiniowane z góry

n=1 zdarzenie (ten sam mainshock na obu stacjach — nie są to dwa
niezależne trzęsienia, więc "replikacja między stacjami" jest słabsza
niż prawdziwa replikacja między zdarzeniami). Nie będzie to ukryte w
wyniku.
