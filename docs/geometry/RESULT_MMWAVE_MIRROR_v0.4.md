# RESULT — radar mmWave 77 GHz: lustro i cień (dane spełniające regułę wykonalności), v0.4

Pre-rejestracja: `PREREG_MMWAVE_MIRROR_v0_4.md` (commit 294350f). Jedno uruchomienie. Liczby: `RESULT_MMWAVE_MIRROR_v0_4.json`.
Test: nagrania 12–20, po 9 na klasę (ukryta butelka / utykanie / machanie rękami).

| Zestaw | macro-F1 | AUC butelka | AUC utykanie | AUC machanie |
|---|---|---|---|---|
| C — klasyka (CVD, rozrzut Dopplera) | 0,81 | 0,99 | 1,00 | 0,99 |
| **M — lustro/cień** | **0,89** | 0,99 | 0,94 | 1,00 |
| C+M | **0,93** | 0,97 | 0,98 | 1,00 |

- **H1 (most dodaje do klasyki): MIXED** — macro-F1 +0,11, CI [0,00; +0,26] (dolna granica dokładnie na zerze).
- **H2 (cień lepszy w asymetrii rąk): NOT SUPPORTED** — sufit: obie metody AUC 0,99.
- **H3 (stereoskopia, kierunki z rozwoju): SUPPORTED 3/3** —
  cień R_all: butelka 0,61 vs reszta 0,57 (p 0,0008);
  faza dalekich połówek: butelka −0,81 (przeciwfaza) vs machanie −0,08 (p 0,002);
  spójność bliskich połówek: machanie 0,18 vs reszta 0,46 (p 0,0001).
- **H4 (rytm): SUPPORTED** — utykanie α* < 1,2 Hz w 8/9 (krok podwójny), pozostałe > 1,2 Hz w 18/18.

## Wniosek
Idea autora działa, gdy spełniona jest reguła wykonalności. Na Open Radar (za krótkie ślady) wzór z rozwoju się nie
powtórzył; tu powtórzył się w całości: jedna nieruchoma ręka zostawia **cień** (część, której nałożenie połówek nie znosi)
i przeciwfazę dalekich połówek, a swobodne machanie rozprzęga bliskie połówki. Samo lustro klasyfikuje lepiej niż klasyka
(0,89 vs 0,81), razem 0,93 — przewaga na granicy istotności przy 27 nagraniach testowych.
Zastrzeżenia: przypisanie nagrań do osób nieznane (możliwy przeciek osób między rozwojem i testem); wada zbioru
(nagrania 5–8 zduplikowane) wykluczona; mała próba.

## Odtworzenie
Surowe archiwa i pliki pośrednie (`DATA/mmwave/proc/*.npz`) zostały usunięte po teście (miejsce na dysku). Odtworzenie:
pobrać część 2 zbioru (Zenodo 10.5281/zenodo.3897234: HidingBottle, Limping, SlowWalk_SwingingHands), uruchomić
`core/mmwave_extract.py` (odczyt strumieniowy, wykluczyć nagrania 5–8 z Limping i SlowWalk_SwingingHands), potem
`core/mmwave_mirror.py`.
