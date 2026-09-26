# Wynik — CWRU, test na niewidzianych łożyskach z baseline'em obwiedni, v0.1 (2026-09-26): MIESZANY

Pre-rejestracja: `PREREG_CWRU_CROSS_BEARING_ENVELOPE_v0.1.md` (commit f45038e). Liczby: `RESULT_CWRU_CROSS_BEARING_ENVELOPE_v0.1.json`.
Bez zmian po zamrożeniu. Kontrole: pozytywna 1,00, negatywna 0,30 — przeszły.

Typ uszkodzenia (IR / kulka / OR), uczenie na łożyskach 7 i 14 milsów, test na łożyskach 21 milsów (macro-F1):

| RPM | klasyczne + obwiednia | TIMDR sam | razem | zysk |
|---|---|---|---|---|
| 1797 | 1,00 | 0,29 | 0,98 | −0,02 |
| 1772 | 0,92 | 0,36 | **0,98** | +0,06 |
| 1750 | 0,94 | 0,56 | **1,00** | +0,06 |
| 1730 | 1,00 | 0,54 | 1,00 | 0,00 |

Średni zysk +0,027, dodatni w 2/4 → **MIESZANY** (sufit klasycznych tylko w 2 warunkach, więc reguła sufitu nie zadziałała).

**Co to znaczy.** Na fizycznie innych łożyskach klasyczne cechy z obwiednią prawie rozwiązują zadanie; tam, gdzie zostawiają
margines (1772, 1750), topologia TIMDR domyka go do 0,98–1,00, ale sama na nowych łożyskach działa słabo (0,29–0,56).
Wynik zgodny z Paderborn co do kierunku (TIMDR jako uzupełnienie), ale nie potwierdza go wg kryterium — głównie dlatego,
że przy mocnym baseline'ie zostaje niewiele do poprawienia.
