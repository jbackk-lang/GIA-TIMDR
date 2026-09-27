# RESULT — Hell Bridge: reguła kierunku + stosunki częstotliwości, v0.5

Pre-rejestracja: `PREREG_HBTA_LATERAL_RATIOS_v0_5.md` (commit 45330ab). Jedno uruchomienie.
Liczby: `RESULT_HBTA_LATERAL_RATIOS_v0_5.json`. Test: pozycja P1; Y nowe dane, Z użyte drugi raz (v0.4).

Stosunek przesunięcia (DSk vs UDS_01) do przesunięcia UDS_02 vs UDS_01 (> 1 = uszkodzenie większe niż zmiana między dniami):

| Stan | Y bieguny | Y bieguny norm. | Y zera norm. | Z bieguny | **Z bieguny norm.** | **Z zera norm.** |
|---|---|---|---|---|---|---|
| DS1 podłużnica–poprzecznica | 0,98 | 1,06 | 0,80 | 1,04 | **1,78** | 0,93 |
| DS2 j.w., wiele | 0,68 | 0,77 | 1,08 | 2,76 | **6,34** | **2,68** |
| DS3 poprzeczka | 0,67 | 0,50 | 1,14 | 0,56 | **1,08** | **1,26** |
| DS4 poprzeczki | 0,61 | 0,56 | 0,96 | 0,68 | **1,75** | **1,06** |
| DS5 stężenie | 0,42 | 0,74 | 1,46 | 1,86 | **4,42** | **1,55** |
| DS6 stężenia | 1,22 | 1,54 | 1,35 | 1,45 | **4,71** | **1,39** |
| DS7 stężenia | 1,02 | 0,98 | 1,52 | 1,35 | **4,56** | **1,42** |
| DS8 poprzecznica–dźwigar | 1,00 | 1,07 | 1,73 | 2,63 | **2,31** | **1,46** |

Null (względne przesunięcie między dniami, P1: 22.09, 11 °C vs 23.09, 15 °C): Z bieguny 0,0055 → po normalizacji 0,0026;
Z zera 0,0087 → 0,0068; Y bieguny 0,0110 → 0,0096; Y zera 0,0132 → 0,0099.

- **H1 (kierunek): MIXED** — w Y stężenia > null w 2/3 (DS6 1,22, DS7 1,02 — na granicy), ale średnio Y 0,89 < Z 1,55.
- **H1b (pionowe słabną w Y): SUPPORTED** — DS1–2 Y 0,83 vs Z 1,90.
- **H2 (stosunki znoszą zmianę między dniami): SUPPORTED** — null mniejszy po normalizacji w 4/4 komórkach,
  **wbrew przewidywaniu z rozwoju** (na P2 1/4).

## Wniosek
1. Stosunki częstotliwości (idea autora: odniesienie z samej stali) działają, gdy zmiana między dniami jest równym
   skalowaniem — na P1 (4 °C różnicy) null biegunów spadł o połowę, a w pionie wszystkie 8 uszkodzeń przekroczyło null,
   stężenia 4,4–4,7 ×. Zera po normalizacji: 7/8 (surowe w v0.4: 0/8) — antyrezonanse przegrały przez temperaturę, nie
   przez brak informacji. Na P2 zmiana między dniami nie była równym skalowaniem (różne znaki, przeskok bliskiego modu) i
   stosunki nie pomogły — warunek fizyczny: normalizacja znosi tylko równomierną zmianę sztywności.
2. Kierunek: pionowe uszkodzenia słabną w Y zgodnie z fizyką, ale stężenia nie są w Y lepiej widoczne niż w Z; po
   normalizacji widać je wyraźnie w pionie. „Niewidoczność” stężeń w v0.3 wynikała z metody (tryb szumu, kształt z siatki
   pionowej), a nie z samego kierunku pomiaru.
3. Z P1 użyte drugi raz, jeden null na pozycję — wynik rozpoznawczy, ale H2 zamrożone przed uruchomieniem i przewidziane
   przeciwnie, więc nie jest dopasowane do danych.
