# RESULT — budynek LANL jako pole + sito cząsteczkowości, v0.2

Pre-rejestracja: `PREREG_LANL_FIELD_SIEVE_v0_2.md` (commit 1496514). Jedno uruchomienie. Liczby: `RESULT_LANL_FIELD_SIEVE_v0_2.json`.

| | Sito Q (pole + cząsteczkowość) | Klasyczne SHM B (v0.1) |
|---|---|---|
| AUC uszkodzenie, fold A / B | 0,83 / 0,85 | 0,995 / 0,993 |
| Fałszywe alarmy, stany 2–9 (masa, sztywność) | **0,025** | 0,063 |
| Wykrycie, stany 10–17 | 0,35 | 0,98 |
| Ciężkość, Spearman ρ (stany 10–14) | **−0,57** | +0,97 |

- **H1 (AUC ≥ 0,90): NOT SUPPORTED** — 0,83 / 0,85. Lepiej niż stare operatory TIMDR (0,45 / 0,53), ale poniżej progu.
- **H2 (swoistość): NOT SUPPORTED** — mniej fałszywych alarmów, ale wykrywa tylko 35% uszkodzeń (próg 0,8).
- **H3 (ciężkość): NOT SUPPORTED** — korelacja ujemna.

## Co pokazały dane (obserwacja po fakcie, nie wynik)
Sito alarmuje prawie zawsze przy szczelinie 0,15 i 0,13 mm (stany 11–12), a prawie nigdy przy 0,10 i 0,05 mm (13–14),
choć tam zderzak uderza najczęściej. Możliwe wyjaśnienie w języku mapy dualności: **rzadkie uderzenia są cząsteczkami**
(wystają ponad tło), a **uderzenia w każdym cyklu drgań zlewają się w falę** (okresowy sygnał, żadne nie wystaje).
Miara cząsteczkowości widzi tylko pierwszy przypadek. To hipoteza do osobnego testu (np. cecha „rytmu uderzeń” na
harmonicznych modu), nie wniosek z tego testu.
