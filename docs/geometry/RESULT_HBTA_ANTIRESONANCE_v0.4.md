# RESULT — Hell Bridge: antyrezonanse (zera FRF), v0.4

Pre-rejestracja: `PREREG_HBTA_ANTIRESONANCE_v0_4.md` (commit 0d01cf5). Jedno uruchomienie.
Liczby: `RESULT_HBTA_ANTIRESONANCE_v0_4.json`. Test na nowych danych: sweep, wibrator w pozycji P1.

| Stan | P2 (rozwój) zera / bieguny | **P1 (test) zera / bieguny** |
|---|---|---|
| DS1 podłużnica–poprzecznica | 2,13 / 1,03 | **0,79** / 1,04 |
| DS2 j.w., wiele | 4,59 / 3,28 | **0,93** / 2,76 |
| DS3 poprzeczka | 1,54 / 0,67 | **0,93** / 0,56 |
| DS4 poprzeczki | 1,15 / 1,07 | **0,79** / 0,68 |
| DS5 stężenie | 0,78 / 0,40 | **0,73** / 1,86 |
| DS6 stężenia | 1,74 / 0,74 | **0,84** / 1,45 |
| DS7 stężenia | 1,54 / 0,64 | **0,59** / 1,35 |
| DS8 poprzecznica–dźwigar | 4,27 / 1,58 | **0,66** / 2,63 |

(Stosunek przesunięcia DSk vs UDS_01 do przesunięcia UDS_02 vs UDS_01; > 1 = uszkodzenie większe niż zmiana między dniami.)

- **H1 (zera > null w ≥ 7/8): NOT SUPPORTED** — 0/8.
- **H2 (zera > bieguny w ≥ 7/8): NOT SUPPORTED** — 2/8; bieguny > null w 6/8.
- **H3 (stężenia widoczne w zerach): NOT SUPPORTED** — 0/3.

## Wniosek
Wzór z rozwoju (P2: zera 7/8, lepsze od biegunów 8/8, stężenia widoczne) nie przeniósł się na inną pozycję wzbudzenia.
Na P1 zmiana zer między dwoma dniami bez uszkodzenia (ΔT 4 °C) jest większa niż zmiana od każdego uszkodzenia.
To zgodne z fizyką: zera są lokalne — ale lokalne na wszystko, także na warunki brzegowe, temperaturę i drogę
wzbudnik → czujnik; zależą od pozycji wibratora, więc wybór zer z jednej pozycji nie mówi nic o drugiej. Bieguny
(globalne) okazały się stabilniejszym śladem. Ograniczenie z góry: jeden null na pozycję — wynik rozwojowy P2 był
najpewniej przypadkiem tego jednego nulla. Lokalność uszkodzenia lepiej łapie kształt modu z przerwą ciągłości (v0.3)
niż zera FRF.
