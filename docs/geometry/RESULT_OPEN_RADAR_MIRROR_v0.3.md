# RESULT — Open Radar: most K↔G „lustro” i „cień”, v0.3

Pre-rejestracja: `PREREG_OPEN_RADAR_MIRROR_v0_3.md` (commit 2ad9cec, przed cechami eval). Jedno uruchomienie.
Liczby: `RESULT_OPEN_RADAR_MIRROR_v0_3.json`. Ślady eval użyte trzeci raz — wynik rozpoznawczy.

| Zestaw | macro-F1 | AUC osoba | AUC rower | AUC dron |
|---|---|---|---|---|
| A_v01 — klasyka (kawałki 2 s) | 0,52 | 0,54 | 0,76 | **0,90** |
| C_full — klasyka, cały ślad (CVD) | 0,25 | 0,61 | 0,49 | 0,59 |
| **M — lustro/cień** | 0,37 | **0,77** | **0,77** | 0,47 |
| A+C | **0,55** | 0,65 | 0,75 | 0,92 |
| A+C+M | 0,50 | 0,74 | 0,78 | 0,84 |

- **H1 (most dodaje do klasyki): NOT SUPPORTED** — macro-F1 A+C+M − A+C = −0,047 [−0,12; +0,03] (dev: +0,07).
- **H2 (rower — cień): MIXED** — AUC M − A_v01 = +0,01 [−0,17; +0,15]; względem klasyki na tym samym całym śladzie
  (C_full) +0,28.
- **H3 (stereoskopia, kierunki z dev): NOT SUPPORTED** — osoba cos_far 0,36 vs reszta 0,50 (p 0,42; na dev 0,96);
  osoba R_far bez różnicy (p 0,47); rower R_all 0,41 vs 0,35 (p 0,057 — kierunek zgodny, poniżej progu).
- **H4 (wykonalność — przewidywana porażka dla drona): potwierdzone** — AUC M 0,47.
- Kontrole: permutacja etykiet — macro-F1 mediana 0,22, p95 0,33 (A+C+M 0,50 powyżej). Podzbiór 220 MHz: M osoba 0,68,
  rower 0,76 (klasyka osoba 0,32–0,38).

## Diagnostyka po teście (nie hipoteza)
Osoby w eval mają ślady 2,5× krótsze niż w dev (mediana 237 vs 614 klatek siatki) i więcej luk (0,21 vs 0,14);
rytm kroku (α* > 0,7 Hz) znaleziony w 24% śladów osób vs 65% w dev. Wzór „dalekie połówki w fazie przy rytmie kroku”
z dev nie mógł się powtórzyć tam, gdzie rytmu nie było w oknie — ta sama przyczyna co w v0.1 (wykonalność), tym razem
po stronie danych testowych. Klasyka też straciła osoby (A_v01 0,54), a lustro trzyma się najlepiej (0,77) — obserwacja
spoza hipotez, nie wynik.

## Wniosek
Odwrócenie (pierwszy trybik = faza/linia ciała, skręt = połówki lustrzane) jest poprawnie zbudowane i niesie informację
niedostępną klasyce na tym samym całym śladzie (rower +0,28 vs CVD), ale nie dodaje do klasyki v0.1, a przewidywania
stereoskopii z dev nie powtórzyły się. Radar pozostaje NOT SUPPORTED. Sprawdzian wymagałby śladów osób z ≥ 10 cyklami
kroku w teście (reguła wykonalności liczona na danych testowych przed testem) albo surowego I/Q z ciągłą fazą między klatkami.
