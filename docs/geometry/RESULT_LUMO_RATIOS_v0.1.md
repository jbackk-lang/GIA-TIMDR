# RESULT — LUMO: stosunki częstotliwości w porach roku + usunięte stężenia, v0.1

Pre-rejestracja: `PREREG_LUMO_RATIOS_v0_1.md` (commit 1875024). Jedno uruchomienie. Liczby: `RESULT_LUMO_RATIOS_v0_1.json`.
Baza: 5 zdrowych bloków z X 2020 (7–15 °C). Test: 25 zdrowych + 25 uszkodzonych bloków, XI 2020 – VI 2021, −3,7 … 40,4 °C.

| Wariant | AUC wszystkie | DAM3 pręt | DAM4 pręt | DAM6 pręt | DAM3 poziom | DAM4 poziom | fałszywe alarmy (p95) |
|---|---|---|---|---|---|---|---|
| surowe | **0,99** | 1,00 | 0,99 | 0,97 | 0,99 | 0,99 | 0,52 |
| stosunki | 0,96 | 0,97 | 0,93 | 0,96 | 0,97 | 0,98 | **0,20** |
| termometr (regresja) | 0,88 | 0,94 | 0,82 | 0,78 | 1,00 | 0,84 | 0,88 |

- **H1 (stosunki odporniejsze na porę roku): NOT SUPPORTED** — AUC −0,027 (przewidziane w prereg: zmiana temperaturowa
  tej wieży nie jest równym skalowaniem; ρ(s, T) na zdrowych testowych −0,29).
- **H2 (pojedynczy pręt): NOT SUPPORTED** — stosunki > surowe w 0/3.
- Opisowo: przy progu z bazy stosunki mają najmniej fałszywych alarmów (20% vs 52% surowe, 88% termometr), ale
  uszkodzenia są tu tak duże względem zmian sezonowych, że ranking (AUC) wygrywają surowe częstotliwości.

## Wniosek
Warunek fizyczny stosunków potwierdzony trzeci raz, tym razem po stronie porażki: gdy temperatura (tu także słońce na
stali, do 40 °C) przesuwa mody w różne strony, wspólny czynnik skali nie znosi zmiany. Termometr z krótkiej bazy
ekstrapoluje najgorzej. Reguła: przed użyciem stosunków sprawdzić na danych bazowych, czy mody idą z temperaturą w tę
samą stronę (znaki ρ) — to jest liczba do reguły wykonalności.
