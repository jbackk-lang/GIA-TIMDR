# RESULT — Open Radar (mikro-Doppler): sito TIMDR vs klasyczne cechy, v0.1

Pre-rejestracja: `PREREG_OPEN_RADAR_MICRODOPPLER_v0_1.md` (commit 91391db, przed cechami eval).
Jedno uruchomienie, 140 śladów eval (person 21, bicycle 19, uav 20, vehicle 80). Surowe liczby:
`RESULT_OPEN_RADAR_MICRODOPPLER_v0_1.json`. Bez poprawek po zamrożeniu.

| Zestaw | macro-F1 (4 klasy) | AUC UAV vs reszta [95% CI] | AUC, tylko 220 MHz |
|---|---|---|---|
| A — klasyczne (Doppler, cepstrum JEM, CVD) | **0,521** | **0,898** [0,83; 0,96] | 0,924 |
| B — TIMDR (sito w polu klatki × pasma + krok 0) | 0,396 | 0,760 [0,64; 0,86] | 0,822 |
| AB | 0,433 | 0,888 [0,78; 0,97] | 0,907 |
| K — kinematyka trackera (kontrola kontekstu) | 0,457 | 0,958 [0,92; 0,99] | 0,943 |

Kontrola negatywna (permutacja etykiet dev 200×, AB): mediana AUC 0,52, p95 0,74.

## Werdykty
- **H1 (TIMDR dodaje do klasyki): NOT SUPPORTED.** ΔAUC = −0,010 [−0,081; +0,053]; ΔF1 = −0,088
  [−0,185; +0,015]. W rozwoju AB było lepsze (0,949 vs 0,901) — nie przeniosło się na późniejsze sesje.
- **H2 (B samo działa): SUPPORTED.** AUC 0,76, dolna granica CI 0,64 > 0,5; F1 0,40 > 0,25.
- **H3 (B < A): potwierdzone.** Sito samo nie zastępuje klasycznych cech mikro-Dopplera.
- **H4 (dualność): MIXED.** Rytm człowieka najszybszy (α* 0,94 Hz vs 0,63 Hz) — potwierdzone.
  „Wirnik polowy, nie cząsteczkowy”: P dla uav niższe niż dla reszty (AUC 0,63), ale najniższe ma człowiek,
  nie dron — część przewidywania nie przeszła.
- Sufit nie zadziałał (A 0,898 < 0,98).

## Co to znaczy
- Na tym zbiorze TIMDR nie daje przewagi. Klasyczne cechy są lepsze, a dodanie sita pogarsza F1
  (więcej cech, mało śladów, przesunięcie między sesjami: F1 spadło z 0,68 w dev do 0,52 w eval dla A).
- Kinematyka trackera (prędkość, zasięg) rozdziela drona najlepiej (0,96): klasy nagrywano w różnych
  warunkach (dron blisko radaru). To ślad akwizycji, nie mikro-Doppler.
- Ograniczenie danych: widma są liczone z oknem 30 ms przy 20 klatkach/s. Błyski łopat (setki Hz) są
  niewidoczne w skali klatek, a w czasie wolnym (wewnątrz klatki) za krótkie. Wirnik widać tylko jako
  rozmycie widma — dlatego pomaga entropia widmowa, a nie rytm. Ten zbiór nie nadaje się do testu
  „błyski wirnika = cząsteczki”; do tego potrzebny surowy I/Q o długim oknie.
- Porażka zgodna z wcześniejszym obrazem: sito wygrywa, gdy szukany rytm jest znany z fizyki
  (BPFO, rzędy turbiny). Tu rytm był nieznany i sito musiało go zgadywać (α*) — samokorekta bez
  kotwicy nie wystarczyła.
