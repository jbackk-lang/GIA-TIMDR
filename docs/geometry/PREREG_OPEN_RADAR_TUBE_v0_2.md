# PREREG — Open Radar: radar jako rura (zwinięte pole), v0.2

Data: 2026-09-27. Idea J. Kielicha: zamiast badać pole (widma), zwinąć je z powrotem w sygnał i badać go jak w rurze.
Zamrożone PRZED ekstrakcją cech rury ze śladów eval. Kod: `core/radar_or_tube.py`, `radar_or_tube_extract.py`,
`radar_or_tube_eval.py`.

## Ujawnienie: ten sam podział eval co v0.1
Ślady eval (140) zostały już raz użyte w v0.1 (cechy A, B, K). Cechy rury nigdy na nich nie były liczone, ale
werdykt jest słabszy niż przy danych całkiem nieotwieranych. Innych danych z tego radaru nie ma.

## Zwinięcie pola → rura
Klatka (widmo Dopplera, bez cluttera ±2 biny) → odwrotna FFT → z(t) = I + iQ w czasie wolnym (środek okna, ok. 12 ms,
podzielony przez okno). Demodulacja Dopplerem ciała. **Oś** (|f| < 300 Hz) → C(t) = (t, Re, Im): zgięcie (krzywizna),
skręt osi (torsja). **Szybka rura** (|f| ≥ 1 kHz): grubość (log energii szybkiej / całej), cząsteczkowość promienia
(udział 5% najsilniejszych próbek), rytm błysków (autokorelacja promienia, opóźnienie 1,5–8 ms), drgania skrętu.
Mediana i p90 po klatkach → 12 cech (T).

## Rozwój (5-krotna CV na dev)
A 0,901 · T 0,855 · A+T 0,905 · B+T (sam TIMDR: pole + rura) 0,914 (AUC UAV vs reszta).
Obserwacja z dev: szybka rura jest na poziomie szumu we wszystkich klasach (cząsteczkowość ≈ 0,20 = wartość dla szumu
gaussowskiego; drgania skrętu stałe). Informację niesie tylko grubość rury (≈ rozmycie widma).

## Hipotezy (eval, bootstrap warstwowy po śladach, 2000×)
- **H1: rura dodaje do klasyki.** ΔAUC(A+T − A): SUPPORTED gdy dolna granica CI > 0; NOT SUPPORTED gdy Δ ≤ 0; inaczej MIXED.
  Przewidywanie z dev: brak zysku.
- **H2: model zbudowany wyłącznie z TIMDR (pole B + rura T) nie gorszy od klasyki.** ΔAUC(B+T − A): SUPPORTED (nie gorszy)
  gdy dolna granica CI > −0,05; NOT SUPPORTED gdy górna < 0; inaczej MIXED.
- **H3: dron = cząsteczki w rurze.** AUC cząsteczkowości (p90) dla UAV vs reszta, dolna granica CI > 0,5.
  Przewidywanie z dev: NOT SUPPORTED (poziom szumu — dane nie rozdzielają błysków łopat).
