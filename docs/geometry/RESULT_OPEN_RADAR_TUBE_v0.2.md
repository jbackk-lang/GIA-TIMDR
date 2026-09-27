# RESULT — Open Radar: radar jako rura (zwinięte pole), v0.2

Pre-rejestracja: `PREREG_OPEN_RADAR_TUBE_v0_2.md` (commit 818242b, przed cechami rury na eval). Jedno uruchomienie.
Liczby: `RESULT_OPEN_RADAR_TUBE_v0_2.json`. Ślady eval te same co w v0.1 (ujawnione w prereg).

| Zestaw | AUC UAV vs reszta [95% CI] | macro-F1 |
|---|---|---|
| A — klasyczne | **0,898** [0,83; 0,96] | **0,521** |
| T — rura | 0,760 [0,67; 0,84] | 0,385 |
| A+T | 0,870 | 0,408 |
| B+T — sam TIMDR (pole + rura) | 0,848 [0,76; 0,92] | 0,487 |

- **H1 (rura dodaje do klasyki): NOT SUPPORTED** — ΔAUC −0,028 [−0,076; +0,024].
- **H2 (sam TIMDR nie gorszy od klasyki): MIXED** — ΔAUC −0,050 [−0,120; +0,010]. Model zbudowany wyłącznie z pola
  i rury jest w granicach błędu od klasyki, ale punktowo słabszy; nie da się ogłosić równoważności.
- **H3 (dron = cząsteczki w rurze): NOT SUPPORTED** — AUC 0,26, czyli odwrotnie: dron ma najmniej błysków
  (mediana 0,23, blisko szumu 0,20), najwięcej rower (0,43 — prawdopodobnie szprychy i pedały).

## Wniosek
Zwinięcie pola w rurę jest poprawne i coś niesie (rura sama AUC 0,76, tyle co sito na polu), ale w tych danych
szybka część rury drona to szum: okno ok. 12 ms i dostępna rozdzielczość nie pokazują błysków łopat. Rura i pole
razem zbliżają się do klasyki, lecz jej nie przewyższają. Test „dron = cząsteczki” wymaga surowego I/Q z długim
zapisem, np. radaru ciągłego (CW) nagrywającego drona — tych danych nie mamy.
