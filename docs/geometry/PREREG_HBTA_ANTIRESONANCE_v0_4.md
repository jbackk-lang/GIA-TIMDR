# PREREG — Hell Bridge: antyrezonanse (zera funkcji przenoszenia) jako lokalny ślad uszkodzenia, v0.4

Data: 2026-09-27. Kod: `core/hbta_antiresonance.py` (`final()`). Zamrożone PRZED jakimkolwiek liczeniem odpowiedzi
na rejestracjach P1. Jedno uruchomienie: `python core/hbta_antiresonance.py`.

## Fizyka i pytanie
Rezonanse (bieguny FRF) są globalne — te same w każdym punkcie. Antyrezonanse (zera H_i = S_iA / S_AA) powstają z
wygaszania się modów i zależą od miejsca pomiaru i wzbudzenia — są lokalne; przy lokalnym uszkodzeniu powinny
przesuwać się mocniej niż bieguny. Gałąź K od strony zer (idea: „przerwa na czymś ciągłym” + antyrezonans).

## Dane — nowe (nieużywane w v0.1–v0.3)
Rejestracje **sweep** (przemiatanie sinusem 2 → ~48 Hz w górę i w dół, ~10 min), pionowo (Z), 40 czujników AL,
wzbudnik AS. Dotąd używano wyłącznie trybu szumu P2 (NM). **Rozwój:** pozycja wibratora P2 (x = 0 m).
**Test:** pozycja P1 (x = 7 m) — inna pozycja wzbudzenia, więc inne zera; z P1 oglądana była tylko częstotliwość
chwilowa sygnału wibratora (kształt przemiatania: UDS_01, UDS_02, DS1), bez odpowiedzi mostu.

## Ujawnienia z rozwoju
1. Tryb szumu (P2 NM, okna 60 s): zera słabe (średnio AUC ~0,59 vs bieguny ~0,74), jeden czujnik (AL11) dominował —
   zera leżą tam, gdzie odpowiedź najmniejsza, więc potrzebują wysokiego SNR. Przejście na sweep.
2. Sweep P2: powtarzalność zer góra/dół w jednej rejestracji 0,003–0,014 Hz, ale różnica między dniami dużo większa —
   skala z jednej rejestracji zawyża z-score; zamiast tego stosunek do przesunięcia UDS_02 vs UDS_01 (null).
3. Większość „zer” to płaskie minima bez prawdziwego antyrezonansu. Wybór: głębokość (log|H| przy biegunach − przy zerze)
   ≥ 2 w obu sweepach referencji (74 z 200 par czujnik × odcinek na P2). Sprawdzone progi 1/2/3 — wybrany środkowy.
4. Wynik rozwoju P2 (zera/null, bieguny/null): DS1 2,13/1,03; DS2 4,59/3,28; DS3 1,54/0,67; DS4 1,15/1,07;
   DS5 0,78/0,40; DS6 1,74/0,74; DS7 1,54/0,64; DS8 4,27/1,58. Zera > null 7/8, zera > bieguny 8/8.

## Metoda (zamrożona)
FRF H1 z całego sweepu (Welch 4096 próbek), osobno góra i dół, średnia. Bieguny: szczyt Σ|H|² w ±4% wokół kotwic
6,86 / 7,42 / 17,26 / 24,12 / 30,08 / 32,32 Hz. Zera: minimum log|H_i| między sąsiednimi biegunami (margines 10%),
interpolacja paraboliczna. Statystyka: mediana względnego przesunięcia wybranych zer (DSk vs UDS_01) podzielona przez to
samo dla UDS_02 vs UDS_01; dla biegunów mediana względnego przesunięcia 6 biegunów, tak samo.

## Hipotezy (test P1)
- **H1:** zera/null > 1 w ≥ 7/8 stanów → SUPPORTED (5–6 MIXED, ≤ 4 NOT). Losowo P(≥7/8) = 0,035.
- **H2:** zera/null > bieguny/null w ≥ 7/8 → SUPPORTED (5–6 MIXED, ≤ 4 NOT).
- **H3:** stężenia (DS5–7, dotąd niewidoczne dla wszystkich metod): zera/null > 1 w ≥ 2/3 → SUPPORTED.
- Raport: czujnik i odcinek z największym przesunięciem zera (lokalizacja rozpoznawcza, bez danych o położeniu).

## Ograniczenia (z góry)
Jedna para rejestracji nieuszkodzonych na pozycję (null z jednej różnicy dni/temperatury: P1 UDS_02 22.09, 11 °C;
UDS_01 23.09, 15 °C); po 2 sweepy na stan. Wynik testu jest pierwszym użyciem P1, ale sam most i uszkodzenia są te same
co w v0.1–v0.3 (wiedza o tym, które uszkodzenia są łatwe, istnieje).
