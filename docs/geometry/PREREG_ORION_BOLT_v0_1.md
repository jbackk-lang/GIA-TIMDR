# PREREG — ORION-AE: luzowanie śruby, droga reżimów (fala → K, cząsteczka → emisja akustyczna), v0.1

Data: 2026-09-27. Kod: `core/orion_bolt.py`. Zamrożone przed ekstrakcją cech z serii D i E.

## Dane
Ramasso i in., ORION-AE (FEMTO-ST), Harvard Dataverse 10.7910/DVN/FBRDU0, CC0. Konstrukcja śrubowa na wibratorze
(118,4 Hz, amplituda sterowana), śruba luzowana w 7 krokach: 60, 50, 40, 30, 20, 10, 5 cNm. Pobrane po 3 pliki (~0,9 s)
na poziom z serii B (rozwój), D i E (test — inne kampanie). Każdy plik dzielony na 4 odcinki.

## Rozwój (seria B, oglądana)
Linie przy kotwicy wymuszenia H rosną przy luzowaniu (60 cNm: −10,65; 5 cNm: −9,64; niemonotonicznie po drodze).
Cząsteczkowość emisji akustycznej P najwyższa przy 20 cNm (0,33–0,40), przy pozostałych poziomach 0,22–0,26.

## Reguła wykonalności
Wibrometr: fala z kotwicą stałą (wymuszenie), N_cyk w odcinku 0,22 s ≈ 26 — droga przez linie K. Emisja akustyczna:
zdarzenia mikropoślizgu — droga przez cząsteczkowość P i gęstość D.

## Hipotezy (serie D i E)
- **H1:** Spearman ρ(H, moment dokręcenia) ≤ −0,6 w obu seriach (linie K rosną przy luzowaniu).
- **H2:** macro-F1 (7 klas, LDA uczone na B, standaryzacja w obrębie serii bez etykiet) zestawu TIMDR {H, P, D} >
  zestawu klasycznego {RMS emisji, liczba przekroczeń progu, kurtoza prędkości} (średnio D i E).
- **H3 (reżim cząsteczki pośrodku):** maksimum mediany P nie wypada przy najluźniejszym poziomie (5 cNm) w obu seriach.
Jedno uruchomienie; wynik do README niezależnie od werdyktu.
