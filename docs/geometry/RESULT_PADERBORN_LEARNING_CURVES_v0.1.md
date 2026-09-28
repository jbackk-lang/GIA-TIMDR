# RESULT — Paderborn: TIMDR jako warstwa porządkująca przed siecią z uwagą (krzywe uczenia), v0.1

Pre-rejestracja: `PREREG_PADERBORN_LEARNING_CURVES_v0_1.md` (commit d0ecec4). Jedno uruchomienie (pomiary 11–20,
5 foldów łożysk rozłącznych × 3 losowania). Liczby: `RESULT_PADERBORN_LEARNING_CURVES_v0_1.json`.
Miara: macro-F1 na łożyskach spoza uczenia (3 klasy, los = 0,33).

| N na klasę | 4 | 8 | 16 | 32 | 64 | 128 | 160 |
|---|---|---|---|---|---|---|---|
| sieć na surowym przebiegu (raw) | 0,34 | 0,32 | 0,31 | 0,32 | 0,36 | 0,42 | 0,44 |
| sieć na log-spektrogramie (spec) | 0,43 | 0,41 | 0,41 | 0,44 | 0,44 | 0,45 | 0,43 |
| **sieć na polu TIMDR** | **0,63** | 0,61 | 0,68 | 0,66 | 0,68 | 0,69 | 0,68 |
| **cechy sita TIMDR + LDA** | 0,55 | 0,62 | **0,70** | **0,70** | **0,74** | **0,73** | **0,74** |

- **H1 (efektywność względem spektrogramu): SUPPORTED** — poziom, który spec osiąga przy 32 przykładach na klasę
  (i nie przekracza do 160), sieć na polu TIMDR osiąga przy 4: stosunek 8×.
- **H1b (względem surowego przebiegu): SUPPORTED** — 40× (raw dochodzi do 0,44 dopiero przy 160).
- **H2 (przy małym N): SUPPORTED** — TIMDR > spec w 57/60 par (N ≤ 32).
- **H3 (sieć niewiele dokłada do struktury TIMDR): SUPPORTED** — przy N = 160 LDA na cechach sita 0,74 vs sieć na polu 0,68.

## Wniosek
Tak, jako warstwa porządkująca TIMDR zmniejsza liczbę potrzebnych przykładów — tu nie „kilka razy”, lecz tak, że sieć
bez TIMDR w ogóle nie uogólnia na nowe łożyska w zakresie do 160 przykładów na klasę (surowy przebieg i spektrogram
zostają blisko losu, mimo że zapamiętują dane uczące). Najlepszy wynik daje najprostszy klasyfikator na cechach TIMDR:
struktura (pole + kotwica w rzędach obrotu + odniesienie do tła) wykonuje pracę, sieć z uwagą nic ponad nią nie dodaje
przy tej skali danych.
Zastrzeżenia: jedna mała sieć i stałe hiperparametry (bez strojenia żadnego ramienia); większa sieć lub znacznie więcej
danych mogłyby zmniejszyć różnicę dla raw/spec; pomiary Paderborn używane wcześniej w testach sita (inne pytanie);
2 s nagrania; generalizacja między łożyskami to trudne przesunięcie domeny i właśnie je mierzymy.
