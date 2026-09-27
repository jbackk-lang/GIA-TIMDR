# PREREG — radar mmWave 77 GHz: lustro i cień na danych spełniających regułę wykonalności, v0.4

Data: 2026-09-27. Kod: `core/mmwave_matstream.py`, `core/mmwave_extract.py`, `core/mmwave_mirror.py` (`final()`).
Zamrożone przed liczeniem cech na nagraniach testowych. Jedno uruchomienie: `python core/mmwave_mirror.py`.

## Po co
Open Radar v0.3: most „lustro/cień” (idea autora: odbicie odwraca skręt; nałożenie połówek znosi część wspólną, zostaje
cień) był NOT SUPPORTED, a diagnoza wskazała regułę wykonalności (za krótkie ślady osób, brak rytmu w oknie). Tu dane,
które ją spełniają: „Millimeter wave radar data of people walking” (Data in Brief 2020, CC-BY 4.0), AWR1642, surowe I/Q,
klatki ciągłe co 40 ms, 16 s (N_cyk kroku ~ 30), chód wprost od radaru i z powrotem (kąt stały).

## Dane i podział
Część 2: HidingBottle (jedna ręka nieruchoma — asymetria rąk), Limping (utykanie), SlowWalk_SwingingHands (machanie).
Odczyt strumieniowy tabeli MATLAB (bez ładowania całości), 4 Rx, FFT zasięgu → usunięcie tła statycznego → FFT Dopplera,
suma mocy po zasięgu 0,25–10 m → P[400 klatek, 128 binów].
**Rozwój:** nagrania 1–11; **test:** 12–20 (po 9 na klasę). Przypisanie nagrań do osób nieznane — możliwy przeciek osób.

## Ujawnienia z rozwoju
1. Cel leży w ujemnej połówce FFT zasięgu (zasięg = 512 − bin) — pierwsza wersja brała złą połówkę; poprawione.
2. **Wada zbioru:** w Limping i SlowWalk_SwingingHands nagrania 5–8 to cztery identyczne pliki (ten sam rozmiar i dane w
   obu klasach) — wykluczone. HidingBottle 5–8 są różne i zostają.
3. Dwie błędne ekstrakcje ręczne (pliki z innych archiwów w folderze „hiding”) wykryte po rozmiarach i odrzucone;
   HidingBottle odczytane bezpośrednio z właściwego archiwum. Brak duplikatów po sprawdzeniu.
4. Cechy M jak Open Radar v0.3 (pasma w binach: |d| 1–40, bliskie 1–12, dalekie 13–40); rytm 0,5–5 Hz, Welch 128 klatek.
   Klasyka C: CVD (szczyt kadencji, siła), rozrzut i entropia Dopplera wokół ciała. LDA (skurcz 0,1).
5. Rozwój (LOO, n = 11/7/7): macro-F1 M 0,91, C 0,87, C+M 1,00; AUC butelka-vs-reszta M 0,97, C 0,92.
   Mediany: butelka — dalekie połówki w przeciwfazie (cos_far −0,77 vs machanie −0,23), największy cień (R_all 0,60 vs
   0,54–0,55); machanie — bliskie połówki prawie niezależne (coh_near 0,13 vs 0,49–0,54); utykanie — rytm 0,78 Hz
   (krok podwójny) zamiast 1,76 Hz.

## Hipotezy (test, bootstrap 2000× w klasach)
- **H1:** macro-F1 (C+M) − C: CI > 0 → SUPPORTED; punkt > 0 → MIXED; inaczej NOT.
- **H2 (cień = asymetria rąk):** AUC butelka-vs-reszta, M − C: ta sama reguła.
- **H3 (kierunki z rozwoju, Mann-Whitney jednostronny p < 0,05):** R_all butelka > reszta; cos_far butelka < machanie;
  coh_near machanie < reszta. 3/3 SUPPORTED, 1–2 MIXED.
- **H4 (fizyka rytmu):** α* < 1,2 Hz dla ≥ 7/9 utykań i α* > 1,2 Hz dla ≥ 14/18 pozostałych.
