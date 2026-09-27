# PREREG — Open Radar (mikro-Doppler): sito rezonansowe TIMDR vs klasyczne cechy, v0.1

Data: 2026-09-27. Zamrożone PRZED ekstrakcją cech ze śladów ewaluacyjnych (commit tego pliku poprzedza
`feat_v0_1_eval`). Jedno uruchomienie: `python core/radar_or_extract.py dev` i `... eval`, potem
`python core/radar_or_eval.py`.

## Dane
Open Radar Initiative, „Outdoor Moving Object Dataset” (Gusland i in., IEEE RADAR 2021, CC BY-NC).
Radar 77 GHz, 350 śladów: vehicle 201, person 52, uav 50, bicycle 47. Każda klatka to zespolone widmo
Dopplera (1008 binów), ok. 20 klatek/s. Plik wczytywany unpicklerem dopuszczającym tylko klasy numpy
(sprawdzone skanem opkodów: jedynie `_reconstruct`, `ndarray`, `dtype`).

**Podział** (commit c6efe81, `SPLIT_OPEN_RADAR_v0_1.json`): w każdej klasie ślady po czasie pierwszej
klatki, pierwsze 60% → dev (210), reszta → eval (140: person 21, bicycle 19, uav 20, vehicle 80).
Z każdego śladu do 5 ciągłych kawałków po 40 klatek (2 s).

## Ujawnienia z rozwoju (na dev)
1. Pierwsza wersja sita działała w czasie wolnym wewnątrz klatki (odwrotna FFT widma = I/Q, 30 ms).
   Odpadła: okno czyni efektywnie ok. 12 ms, rozdzielczość rytmu ok. 80 Hz, α* przyklejało się do
   dolnej granicy (artefakt okna). Przeniesiono pole do skali klatek.
2. Cache przebudowany z 20×10 klatek na 5×40 klatek (rytm chodu potrzebuje ≥ 2 s); podział bez zmian
   (sprawdzone równością list).
3. Ślad akwizycji: klasy nagrywano w blokach czasowych, a trzy konfiguracje radaru (pasmo 66/220/264 MHz)
   nie są rozłożone równo po klasach (vehicle głównie 66 MHz). Kontrola: AUC na podzbiorze 220 MHz.
4. Kinematyka trackera (|v|, zasięg, SNR) rozdziela klasy (dev CV: F1 0,63, AUC 0,83) — raportowana
   jako kontrola kontekstu, nie jako konkurent; cechy A i B jej nie używają.

## Cechy (tylko mikro-Doppler)
Wspólnie: każda klatka przesunięta tak, by pik ciała (bez binu zerowego) był w środku.
- **A — klasyczne:** rozrzut Dopplera, entropia widmowa, szerokość −20 dB (mediana i p90 po klatkach);
  cepstrum JEM (grzebień linii wirnika, odstępy 100–2500 Hz); diagram prędkości kadencji CVD
  (szczyt i jego częstość, 0,5–9,5 Hz).
- **B — TIMDR (drogowskazy):** pole = klatki × pasma 500 Hz względem ciała (−6…+6 kHz, log energii);
  rezonans = widmo rytmu każdego pasma (0,5–9,5 Hz), mapa Rz z medianą 1; sito samokorygujące: α* =
  argmax Σ oczek (1× + 2×); cechy Q, skupienie oczek, α*, średnie przesunięcie oczek. Krok 0: L (udział
  pasma ciała), P (udział energii pozaciałowej w 5% najsilniejszych klatek), M (siła modulacji).
- **AB = A + B.** Klasyfikator: LDA ze skurczem 0,1 (numpy), równe priory. Metryki: 4 klasy macro-F1;
  UAV vs reszta AUC (osobne binarne LDA).

## Wyniki rozwoju (5-krotna CV na dev, podział po śladach)
A: F1 0,681, AUC 0,901 · B: F1 0,616, AUC 0,771 · AB: F1 0,717, AUC 0,949 · K: F1 0,625, AUC 0,832.

## Hipotezy i reguły decyzji (eval, 140 śladów)
- **H1 (główna): TIMDR dodaje do klasyki.** ΔAUC(AB − A) dla UAV vs reszta, bootstrap warstwowy po
  śladach (2000×). SUPPORTED: dolna granica 95% CI > 0. MIXED: Δ > 0, CI obejmuje 0. NOT SUPPORTED: Δ ≤ 0.
  To samo raportowane dla ΔF1 (drugorzędnie).
- **H2: B samo działa.** AUC(B) > 0,5 z dolną granicą CI > 0,5 i F1(B) > 0,25.
- **H3 (przewidywanie, nie sukces): B samo < A** (tak było w dev). TIMDR nie zastępuje klasyki.
- **H4 (dualność, przewidywanie z dev): wirnik drona w skali klatek jest „polowy”, nie „cząsteczkowy”.**
  Mediana P dla uav najniższa z klas, P_AUC_uav_lower > 0,5. Rytm człowieka najszybszy: mediana α*
  person > pozostałych klas.
- **Reguła sufitu:** jeśli AUC(A) ≥ 0,98, H1 = INCONCLUSIVE.
- **Kontrola negatywna:** permutacja etykiet dev 200× → AUC(AB) na eval; oczekiwane ok. 0,5.
- **Kontrola akwizycji:** AUC na podzbiorze 220 MHz dla każdego zestawu.
Wynik negatywny zostanie opisany tak samo jak pozytywny.
