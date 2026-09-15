# Wynik: most M/S↔topologia/K na REALNYCH danych finansowych (BTC/USD 720h) + szum syntetyczny

> Streszczenie `PREREG_REAL_BTC_NOISE_ROBUSTNESS.md`. Kod:
> `core/real_btc_noise_robustness_bridge.py`. Reżim zmienności: mediana
> std 29 bloków 24h → 15 bloków "wysoka zmienność" (pozytyw), 14
> bloków "niska zmienność" (negatyw). Siatka: 5 metryk × 2 okna × 5
> poziomów szumu = 50 komórek. Data: 2026-09-15. Czas: 3,7 s.

## Wynik surowy — **6/50 komórek siatki przeszło (12%)**

Mimo świadomego zaprojektowania regionu pozytywnego jako jednorodnego
(okna nigdy nie przecinają granicy bloku 24h, lekcja z mostu
sejsmicznego) — wynik jest BLIŻSZY porażce serii syntetycznej (1/50,
2%) niż sukcesowi łożysk (123/150, 82%) czy nawet częściowemu
sukcesowi sejsmiki (47/100, 47%).

Tylko `crossing_number` daje jakikolwiek powtarzalny sygnał: `passed`
w 6 z 10 swoich komórek (r zwykle -0,30 do -0,43, "średni"), przy OBU
rozmiarach okna i różnych poziomach szumu — jedyna metryka z
niezerowym, spójnym kierunkowo efektem. Pozostałe cztery metryki
(`torsion`, `winding_number`, `h1_persistence`, `phase_winding`) nie
przeszły ANI RAZU (0/10 każda) — efekty głównie "pomijalne"/"małe",
bez spójnego kierunku.

## Kluczowy wniosek — **jednorodność regionu pozytywnego była KONIECZNA, ale NIE WYSTARCZAJĄCA**

To jest najważniejszy, uczciwy wynik tego mostu. Oczekiwanie a priori
(sekcja 5 pre-rejestracji) było jawnie warunkowe: "oczekuję wyniku
bliższego łożyskom POD WARUNKIEM że hipoteza o roli jednorodności
faktycznie uogólnia się na nową domenę — to jest właśnie testowane,
nie zakładane". **Wynik testuje i w dużej mierze OBALA nadmierne
uogólnienie tej hipotezy**: sama jednorodność (spełniona tu z
konstrukcji, twardo, nie przez przypadek) nie wystarczyła do
odtworzenia silnego efektu z łożysk. Musi istnieć coś jeszcze —
najbardziej prawdopodobny kandydat: reżim zmienności BTC (mierzony
odchyleniem standardowym zwrotów) po normalizacji `(x-mean)/std`
może w ogóle nie zostawiać śladu w KSZTAŁCIE znormalizowanego okna —
w odróżnieniu od defektu łożyska, gdzie kształt fali (nie tylko jej
amplituda) był realnie inny między klasami (silna kurtoza lokalna dla
2 z 3 defektów, inny typ modulacji dla trzeciego). "Wysoka zmienność"
w finansach może być bliżej "tej samej kształtem fali, tylko głośniej"
niż "innej kształtem fali" — a normalizacja `(x-mean)/std` z definicji
usuwa różnice czystej głośności/amplitudy, zostawiając niewiele do
wykrycia.

## `crossing_number` jako częściowy wyjątek — nie przeceniać

Jedyny słaby, ale spójny sygnał. Rozmiar efektu ("średni", r≈-0,3 do
-0,43) jest wyraźnie mniejszy niż w łożyskach (r≈0,9-1,0) i nie
wystarcza do przejścia bramki kontrolnej w większości komórek (tylko
6/10). To jest sygnał WARTY odnotowania (jedyny spójny przez cały
zakres szumu i oba okna), ale zbyt słaby, żeby budować na nim dalsze
wnioski bez replikacji na innej parze aktywo/okres.

## Ograniczenia — jawnie

1. **n=1 instrument, n=1 okres (720h)** — jeden szereg cenowy, jeden
   przedział czasu. Podział reżimu na 15 vs 14 bloków to i tak mało
   punktów danych na poziomie bloku (mediana z 29 obserwacji).
2. **Silne reużycie bloków** przy `window_size=24` (tylko 14-15
   unikalnych bloków < `N_WINDOWS=30`) — każdy z ~15 realnych bloków
   użyty średnio 2x z różnym szumem. Przy `window_size=12` reużycie
   minimalne (28-30 dostępnych sub-okien).
3. Nie wykonano tu dodatkowego porównania z kurtozą/entropią widmową
   (jak w `AUDIT_G_COMPLEXITY_HYPOTHESIS.md` dla łożysk) — przy tak
   słabym wyniku głównym (6/50) uznano to za niski priorytet
   informacyjny względem kosztu; można dopisać, jeśli przyszła praca
   tego wymaga.

## Aktualizacja tabeli porównawczej (cztery przebiegi na realnych danych do tej pory)

| przebieg | przeszło | region pozytywny | kierunek | odporność na szum |
|---|---|---|---|---|
| Seria syntetyczna (5 mostów) | 1/50 (2%) | n/d (syntetyczny) | niespójny/odwrócony | krucha |
| Łożyska CWRU | 123/150 (82%) | jednorodny (defekt stały w czasie) | spójny (4/5 metryk) | duża (do σ=1,0) |
| Sejsmika Ridgecrest | 47/100 (47%) | NIEjednorodny (impuls+zanikanie) | niespójny między stacjami | krucha (znika σ≥0,3-0,5) |
| BTC/USD (reżim zmienności) | 6/50 (12%) | jednorodny (skonstruowany celowo) | tylko crossing_number, spójny ale słaby | n/d (efekt zbyt słaby by ocenić) |

**Zaktualizowany wniosek metodologiczny**: jednorodność regionu
pozytywnego (potwierdzona w `AUDIT_G_COMPLEXITY_HYPOTHESIS.md` jako
przyczynowo istotna W IZOLACJI na JEDNEJ domenie) jest warunkiem
KONIECZNYM dla silnego, odpornego na szum efektu — ale wynik BTC
pokazuje, że nie jest WYSTARCZAJĄCA. Czy dana domena w ogóle niesie
wykrywalny sygnał zależy też od tego, czy różnica między klasami
przejawia się w KSZTAŁCIE znormalizowanego sygnału, nie tylko w jego
skali/energii — a to jest pytanie specyficzne dla każdej domeny z
osobna, nie uniwersalna właściwość "danych realnych".
