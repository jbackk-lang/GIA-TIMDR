# Wynik — replikacja sita samokorygującego + kurtogram, Paderborn, v0.2 (2026-09-26): replikacja CZĘŚCIOWA

Pre-rejestracja: `PREREG_PADERBORN_RESONANCE_SIEVE_REPLICATION_v0.2.md` (commit 879cdee, przed otwarciem pomiarów 11–15).
Liczby: `RESULT_PADERBORN_RESONANCE_SIEVE_REPLICATION_v0.2.json`. Sito bez zmian od v0.1; jedno uruchomienie.
Kontrola negatywna 0,24 — przeszła.

| Zestaw (macro-F1) | średnio | foldy |
|---|---|---|
| klasyczne + obwiednia (B) | 0,56 | 0,71 / 0,26 / 0,73 / 0,53 / 0,56 |
| obwiednia pełnopasmowa (ENV) | 0,61 | 0,97 / 0,26 / 0,98 / 0,56 / 0,30 |
| kurtogram uproszczony (KURT) | 0,55 | 0,29 / 0,66 / 0,66 / 0,78 / 0,35 |
| **sito Q** | **0,65** | 0,90 / 0,46 / 0,86 / 0,57 / 0,44 |

- **H1 (sito vs klasyczne): SUPPORTED** — +0,088, lepsze w 4/5 (drugi raz z rzędu).
- **H2 (sito vs zwykła obwiednia): MIESZANY** — +0,033 (lepsze w 3/5, ale średnio poniżej progu 0,05).
- **H3 (sito vs kurtogram): SUPPORTED** — +0,10, lepsze w 3/5.

Według pre-rejestracji replikacja jest udana tylko przy H1 i H2 SUPPORTED — więc jest **częściowa**.

**Wniosek z obu prób (pomiary 6–10 i 11–15, niewidziane łożyska, uszkodzenia naturalne):** sito samokorygujące dwukrotnie
pokonało klasyczne cechy (+0,12, +0,09) i raz uproszczony kurtogram (+0,10). Przewaga nad samą obwiednią pełnopasmową jest
dodatnia w obu próbach (+0,075, +0,033), ale w drugiej za mała, by ją ogłosić. Najmocniejsza cecha sita to stabilność między
łożyskami: najsłabszy fold 0,44–0,45 wobec 0,26–0,30 dla obwiedni.
