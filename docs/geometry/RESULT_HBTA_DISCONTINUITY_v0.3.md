# RESULT — lokalne uszkodzenie jako przerwanie ciągłości (K → G → M/S), Hell Bridge Test Arena, v0.3

Pre-rejestracja: `PREREG_HBTA_DISCONTINUITY_v0_3.md` (commit 882a98a). Jedno uruchomienie. Liczby: `RESULT_HBTA_DISCONTINUITY_v0_3.json`.
Czwarte użycie danych — wynik rozpoznawczy.

| Stan | Przerwa ciągłości (DISC) | AR(5) | kształt z fazą v0.2 | bez fazy v0.1 |
|---|---|---|---|---|
| DS1 podłużnica–poprzecznica, 1 | **0,94** | 0,91 | 0,81 | 0,91 |
| DS2 podłużnica–poprzecznica, wiele | **0,93** | 0,93 | 0,93 | 0,81 |
| DS3 poprzeczka, 1 | **0,93** | 0,87 | 0,84 | 0,79 |
| DS4 poprzeczki, wiele | **0,93** | 0,89 | 0,83 | 0,75 |
| DS5 stężenie, 1 | 0,44 | 0,59 | 0,48 | 0,33 |
| DS6 stężenia, wiele | 0,56 | 0,64 | 0,69 | 0,36 |
| DS7 stężenia, najwięcej | 0,72 | 0,66 | 0,72 | 0,49 |
| DS8 poprzecznica–dźwigar | **0,94** | 0,93 | 0,93 | 0,76 |
| **średnio** | **0,80** | **0,80** | 0,78 | 0,65 |

- **H1 (DISC > AR średnio): NOT SUPPORTED** — remis 0,801 vs 0,802.
- **H2 (DS1–2: DISC > kształt z fazą): SUPPORTED** — 0,94 vs 0,87.
- **H3 (w poprzek > wzdłuż): NOT SUPPORTED** — 0,78 vs 0,80.
- Uwaga: 0,933 = 14/15 to praktyczny sufit tego układu (jedno okno UDS_02 odstaje); uszkodzenia pionowe są przy suficie.
- Rozpoznawczo: maksimum zerwania współbieżności — DS1 i DS2 w tym samym miejscu (środkowa para podłużnic, x = −5,25 m),
  DS3 i DS4 w tym samym (para 2, x = −15,75 m). Spójne w obrębie typu uszkodzenia; bez danych o położeniu nie oceniamy.

## Wniosek
Traktowanie lokalnego uszkodzenia jako przerwy na czymś ciągłym (skok M/S na kształcie modu z G, zakotwiczonym w K) dało
najlepszy wynik TIMDR na tym moście: wszystkie 5 uszkodzeń pionowych wykryte z AUC 0,93–0,94, w każdym przypadku ≥ AR.
Średnio remis z AR, bo stężeń (DS5–7) pionowe czujniki siatki nie widzą. Kluczowe były: faza (K→G) i maksimum zamiast sumy
(osobliwość zamiast średniej).
