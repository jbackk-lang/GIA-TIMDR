# RESULT — most K↔G: kształt modu z fazą + krzywizna, Hell Bridge Test Arena, v0.2

Pre-rejestracja: `PREREG_HBTA_MODAL_CURVATURE_v0_2.md` (commit e2d7d1c). Jedno uruchomienie. Liczby: `RESULT_HBTA_MODAL_CURVATURE_v0_2.json`.

| Stan | Krzywizna (K↔G) | Kształt z fazą (1 − MAC) | AR(5) |
|---|---|---|---|
| DS1 podłużnica–poprzecznica, 1 | 0,81 | 0,81 | 0,91 |
| DS2 podłużnica–poprzecznica, wiele | 0,93 | 0,93 | 0,93 |
| DS3 poprzeczka, 1 | 0,82 | 0,84 | 0,87 |
| DS4 poprzeczki, wiele | 0,88 | 0,83 | 0,89 |
| DS5 stężenie, 1 | 0,32 | 0,48 | 0,59 |
| DS6 stężenia, wiele | 0,51 | 0,69 | 0,64 |
| DS7 stężenia, najwięcej | 0,56 | 0,72 | 0,66 |
| DS8 poprzecznica–dźwigar | 0,94 | 0,93 | 0,93 |
| **średnio** | **0,72** | **0,78** | **0,80** |

(v0.1: kotwica + kształt z samych amplitud — 0,65.)

- **H1 (krzywizna > AR): NOT SUPPORTED** (0,72 vs 0,80).
- **H2 (krzywizna ≥ 0,75): NOT SUPPORTED** (0,72; poprawa o 0,07 względem v0.1).
- **H3 (uszkodzenia pionowe > stężenia): SUPPORTED** (0,88 vs 0,46).
- Rozpoznawczo: maksimum zmiany krzywizny przy x = −5,25 m dla DS1–2 i x = +5,25 m dla DS3–5, 7, 8 — bez danych o dokładnym
  położeniu uszkodzeń nie oceniamy lokalizacji.

## Wniosek
Faza jest właściwym łącznikiem K→G: kształt modu z fazą podniósł wynik z 0,65 do 0,78 i zrównał się z AR (0,80); przy
uszkodzeniach połączeń pionowych (DS2, DS8) jest na poziomie AR. Krzywizna — klasyczny krok lokalizacyjny — średnio nic nie
dodała, a przy stężeniach pogorszyła wynik (druga różnica wzmacnia szum w punktach słabo wzbudzonych). Most K↔G w tej postaci:
nie przewaga, ale domknięcie luki z v0.1.
