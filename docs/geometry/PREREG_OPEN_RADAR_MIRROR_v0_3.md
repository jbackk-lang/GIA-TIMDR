# PREREG — Open Radar: most K↔G „lustro” i „cień” (stereoskopia połówek lustrzanych), v0.3

Data: 2026-09-27. Zamrożone PRZED ekstrakcją cech ze śladów ewaluacyjnych. Jedno uruchomienie:
`python core/radar_or_mirror.py eval && python core/radar_or_mirror_eval.py`.

## Idea (autor)
Radar mierzy **odbicie**: ruch jest zapisany w fazie nośnej, a kierunek skrętu I/Q = znak prędkości radialnej.
Względem wibracji odwraca się (1) kolejność gałęzi — radar daje od razu K i rurę, M/S jest wtórne, (2) kierunek skrętu —
pole w układzie linii ciała ma dwie lustrzane połówki (+d szybciej niż ciało, −d wolniej). Stereoskopia: nałożenie
połówek znosi część wspólną S = (E₊ + E₋)/2; to, co zostaje, A = (E₊ − E₋)/2, to **cień**. v0.1 i v0.2 liczyły
pasma osobno (moduły) i relacji lustrzanej nie używały.

## Dane i podział
Open Radar „Outdoor Moving Object Dataset” (jak v0.1), podział bez zmian (`split_v0_1.json`): dev 210, eval 140
(person 21, bicycle 19, uav 20, vehicle 80). **Ślady eval użyte trzeci raz** (v0.1, v0.2) — wynik rozpoznawczy.
Nowość: **całe ślady** (do 600 klatek ≈ 30 s) zamiast kawałków 2 s. Cache `full_{dev,eval}` (moc w siatce 100 Hz
±8 kHz względem linii ciała, zawinięcie modulo PRF) zbudowany dla obu części przed zamrożeniem — bez cech i bez oglądania eval.

## Ujawnienia z rozwoju (dev, 5-krotna CV po śladach)
1. Klatki mają luki (ts co 50 ms, ale zdarzają się 100–200 ms; mediana udziału luk: auto 0,29, dron 0,26, osoba 0,14,
   rower 0,04) → równa siatka 50 ms, interpolacja liniowa log-mocy.
2. Pierwsza wersja (Welch 128 klatek): koherencja = 1 dla krótkich śladów (jeden segment — artefakt) i α* przyklejone do
   dolnej granicy (nachylenie 1/f). Poprawki: segment 64 klatki (3,2 s), koherencja tylko przy ≥ 3 segmentach
   (n ≥ 128, inaczej brak danych — reguła wykonalności), normalizacja widma modulacji lokalnym tłem (mediana 9 binów).
   To samo tło w klasycznym CVD.
3. Wykonalność (policzona): N_cyk ≥ 10 w 90% śladów osób, 86% rowerów, 50% dronów, 28% aut. Łopaty drona (setki Hz)
   niedostępne przy ~20 klatkach/s.
4. Wyniki dev (CV, macro-F1 / AUC osoba, rower, dron): A_v01 0,65 / 0,84 0,88 0,90; C_full 0,46 / 0,92 0,79 0,55;
   M 0,53 / 0,90 0,93 0,66; A+C 0,71 / 0,94 0,93 0,89; A+C+M 0,78 / 0,94 0,96 0,90.
5. Mediany dev: osoba — dalekie pasma lustrzane **w fazie** (cos_far 0,96) i mały cień (R_far 0,21 vs 0,42–0,46);
   rower — największy cień (R_all 0,49 vs 0,32–0,37) i najsłabsza koherencja lustra.

## Cechy
- **M — lustro/cień (TIMDR):** pasma |d| po 500 Hz (100–6100 Hz), E± = log mocy połówki; rytm z samokorektą
  α* = argmax Σ modulacji obu połówek (1× + 2×), 0,5–9,5 Hz, na całym śladzie; przy α* dla pasm bliskich (100–2100 Hz)
  i dalekich (2100–6100 Hz): koherencja lustra |S₊₋|²/(S₊₊S₋₋), faza lustra cos(arg S₊₋), udział cienia R = P_A/(P_A+P_S);
  plus R_all (cień w całym paśmie rytmu), Q, α*. 9 cech.
- **C_full — klasyka na całym śladzie:** CVD (szczyt kadencji i jego siła), rozrzut Dopplera, entropia, szerokość −20 dB.
- **A_v01 — klasyka v0.1** (rozrzut, cepstrum JEM, CVD na kawałkach 2 s; cechy z v0.1, bez zmian).
- Zestawy: A_v01, C_full, M, C+M, A+C, A+C+M. LDA ze skurczem 0,1 (jak v0.1), uczenie na całym dev, test na eval.

## Hipotezy i reguły (bootstrap 2000× w klasach, CI 95%)
- **H1 (most dodaje do klasyki):** macro-F1 A+C+M − A+C: CI > 0 → SUPPORTED; punkt > 0, CI obejmuje 0 → MIXED; inaczej NOT.
- **H2 (rower — cień):** AUC rower-vs-reszta, M − A_v01: ta sama reguła. Raport pomocniczy M − C_full.
- **H3 (stereoskopia, kierunki z dev):** Mann-Whitney jednostronny p < 0,05: osoba cos_far > reszta; osoba R_far < reszta;
  rower R_all > reszta. 3/3 → SUPPORTED, 1–2 → MIXED, 0 → NOT.
- **H4 (wykonalność — przewidywana porażka):** dron-vs-reszta AUC zestawu M < 0,70 → przewidywanie potwierdzone.
- Kontrole: permutacja etykiet dev 200× (macro-F1 A+C+M, mediana i p95); podzbiór 220 MHz (ślad konfiguracji).

## Przewidywanie
H1 MIXED lub SUPPORTED (dev +0,07), H2 SUPPORTED (dev +0,05), H3 ≥ 2/3, H4 potwierdzone. Każdy wynik trafia do README.
