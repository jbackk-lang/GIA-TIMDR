# Wynik — Paderborn, uszkodzenia naturalne, niewidziane łożyska, v0.1 (2026-09-26)

Pre-rejestracja: `PREREG_PADERBORN_REAL_DAMAGE_v0.1.md` (commit ba33005, przed odczytem danych; definicja pola/rezonansu/sita
zaakceptowana przez autora idei). Liczby: `RESULT_PADERBORN_REAL_DAMAGE_v0.1.json`. Bez zmian po zamrożeniu.
Kontrole: topologia 1,00, sito AUC 1,00, negatywna 0,28 — przeszły. 15 łożysk (5/klasę), 5 foldów, łożyska testowe nigdy
w uczeniu; macro-F1, 3 klasy (losowo ≈ 0,33).

| Zestaw cech | średni F1 | foldy |
|---|---|---|
| klasyczne + widmo obwiedni (B) | 0,58 | 0,71 / 0,41 / 0,70 / 0,45 / 0,63 |
| topologia TIMDR sama (T) | 0,25 | poniżej losowego |
| B + topologia | 0,59 | zysk 0,00 / +0,01 / −0,01 / +0,08 / −0,03 |
| sito z nałożenia 3 pól (S3) | 0,37 | |
| sito z samego pola drgań (Sv) | 0,54 | |
| B + sito S3 | 0,56 | zysk −0,13 / −0,06 / +0,10 / +0,05 / −0,06 |

- **A (topologia jako uzupełnienie): MIESZANY** — średni zysk +0,009; w praktyce brak efektu.
- **S1 (nałożenie pól lepsze niż samo pole drgań): NOT SUPPORTED** — 0,37 wobec 0,54; dołożenie pól prądów pogarsza.
- **S2 (klasyczne + sito): NOT SUPPORTED** — 0,56 wobec 0,58.

**Co to znaczy.** Na najtrudniejszym i najbardziej realistycznym teście (naturalne uszkodzenia, łożyska spoza uczenia)
zysk z topologii TIMDR, który przeszedł na sztucznych uszkodzeniach jednego łożyska (`RESULT_PADERBORN_VIBRATION_COMPLEMENT_v0.1.md`),
nie przenosi się. Rezonans jako nałożenie pól drgań i prądów w tej definicji nie działa jako sito — pola prądów rozmywają
informację z drgań. Opisowo: samo pole obwiedni drgań (Sv, 0,54) jest blisko klasycznych cech (0,58), więc reprezentacja
„pola” nie jest bezwartościowa, ale nie była tu hipotezą i nie przewyższa baseline'u.
