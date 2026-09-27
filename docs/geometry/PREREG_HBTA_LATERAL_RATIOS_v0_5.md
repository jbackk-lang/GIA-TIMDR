# PREREG — Hell Bridge: reguła kierunku (sweep poprzeczny) + stosunki częstotliwości, v0.5

Data: 2026-09-27. Kod: `core/hbta_lateral.py` (`final()`). Zamrożone PRZED liczeniem odpowiedzi na rejestracjach P1 Y.
Jedno uruchomienie: `python core/hbta_lateral.py`.

## Pytania
1. **Kierunek** (wniosek z mostów): stężenia wiatrowe (DS5–7) przenoszą obciążenia poprzeczne — mierzone i wzbudzane
   pionowo były niewidoczne dla przerwy ciągłości (v0.3). Przewidywanie: w wzbudzeniu poprzecznym (sweep Y) i czujnikach
   poprzecznych na pasach dźwigarów (AG, oś y, 17 kanałów; AG09 bez osi y) stężenia stają się widoczne, a uszkodzenia
   pionowe (DS1–2) słabną.
2. **Stosunki** (idea autora: temperatura wolna → odniesienie z samej stali): równa zmiana E skaluje wszystkie
   częstotliwości jednym czynnikiem; po podzieleniu przez wspólny czynnik skali (mediana stosunków biegunów do
   referencji) zmiana między dniami powinna się skrócić, a uszkodzenie zostać.

## Dane (nowe)
Sweep Y (poprzeczny), pozycje P2 (rozwój) i P1 (test) — dotąd nieużywane. Porównanie pionowe: sweep Z P1 (użyte raz,
w v0.4 — tam bieguny/null dla DS5–7: 1,86 / 1,45 / 1,35, średnio 1,55; DS1–2: 1,04 / 2,76). Null: UDS_02 vs UDS_01.
Temperatury P1 Y i Z patrz atrybuty rejestracji (raport w RESULT).

## Ujawnienia z rozwoju (P2)
1. Kotwice Y z P2 UDS_01 Y: szczyty Σ|H|², koherencja mediana i p10 ≥ 0,8, odstęp ≥ 8% (zachłannie od najsilniejszego):
   7,23 / 8,59 / 11,33 / 12,52 / 14,94 / 16,19 / 18,63 / 20,97 / 23,41 / 26,22 / 29,57 / 32,57 / 38,4 Hz (13).
2. Kierunek na P2 (bieguny/null): Y stężenia 0,87 / 1,33 / 2,46 (2/3 > 1, średnio 1,55) vs Z 0,40 / 0,74 / 0,64 (0/3);
   pionowe DS1–2: Y 1,43 / 0,78 vs Z 1,03 / 3,28.
3. Stosunki na P2: **nie działają** — zmiana między dniami nie jest równym skalowaniem (bieguny Y: +1,6 … −1,5%, różne
   znaki; w Z przeskok modu 7,42 → 6,86 o −16% — bliskie mody, artefakt samokorekty). Normalizacja średnią geometryczną
   zawyżała null (Z: 0,012 → 0,033), zmieniona na medianę stosunków (odporną na przeskok); nadal null_norm < null_surowy
   tylko w 1/4 komórek (Y bieguny).
4. Zera w Y: stężenia 1,08 / 1,40 / 1,27 — słabiej różnicujące niż bieguny; statystyką główną H1 są bieguny surowe.

## Hipotezy (test P1)
- **H1 (kierunek):** bieguny/null w Y > 1 dla ≥ 2/3 stężeń (DS5–7) ORAZ średnia Y dla DS5–7 > średnia Z (1,55, z v0.4,
  liczona tym samym kodem w tym przebiegu). Oba → SUPPORTED, jedno → MIXED, żadne → NOT.
- **H1b:** pionowe DS1–2: średnia Y < średnia Z → SUPPORTED.
- **H2 (stosunki znoszą zmianę między dniami):** null_norm < null_surowy w ≥ 3/4 komórek (Y/Z × bieguny/zera) →
  SUPPORTED; 2/4 MIXED. **Przewidywanie z rozwoju: NOT SUPPORTED.**

## Ograniczenia
Jeden null na pozycję i kierunek; 2 sweepy na stan. Most i uszkodzenia te same co w v0.1–v0.4.
