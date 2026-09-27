# RESULT — budynek LANL: kotwica modalna K → linie w reżimie fali, v0.3

Pre-rejestracja: `PREREG_LANL_MODAL_ANCHOR_v0_3.md` (commit 4147368). Jedno uruchomienie. Liczby: `RESULT_LANL_MODAL_ANCHOR_v0_3.json`.
Dane użyte trzeci raz (v0.1, v0.2) — ujawnione.

| | H (linie przy kotwicy K) | C = max(P, H) | Klasyczne SHM B |
|---|---|---|---|
| AUC fold A / B | 0,966 / 0,964 | 0,954 / 0,960 | 0,995 / 0,993 |
| Ciężkość ρ (stany 10–14) | **+0,98** | +0,98 | +0,97 |
| Fałszywe alarmy 2–9 | — | 0,050 | 0,063 |
| Wykrycie 10–17 | — | 0,79 | 0,98 |

- **H1 (odwrócenie ciężkości): SUPPORTED.** ρ = +0,98 (v0.2 sito cząsteczkowości: −0,57). Przejście z reżimu cząsteczki
  do reżimu fali z kotwicą modalną naprawiło kierunek miary.
- **H2 (dwa reżimy razem): SUPPORTED** wg progów (AUC ≥ 0,95, fałszywe alarmy ≤ B). Wykrycie przy progu 95% niższe niż B
  (0,79 vs 0,98) — poza kryteriami, raportowane.
- **H3 (D rośnie z ciężkością): NOT SUPPORTED** (ρ = 0,29). Mediana D: nieuszkodzone 1,4–3,2 (szerokopasmowe wymuszenie =
  tło „polowe”), uszkodzone 0,4–1,4. Uderzenia obniżają D względem tła; w stanach 11 → 14 D rośnie monotonicznie
  (0,43 → 0,48 → 0,79 → 1,37), ale stan 10 (najrzadsze uderzenia, 1,04) łamie trend.

## Wniosek
Reguła reżimów wskazała właściwą drogę: przy częstych uderzeniach linie przy kotwicy modalnej (tony 2fa, 2fb, fa+fb)
mierzą ciężkość tak dobrze jak klasyczne cechy SHM. Uczciwie: ta miara to w istocie klasyczny wskaźnik nieliniowości
(harmoniczne wyższe); wkład TIMDR to reguła, która ją wybrała, i kotwica wyznaczana z danych. Sam parametr D wymaga
poprawki: przy szerokopasmowym wymuszeniu tło ma wysokie D, więc D trzeba liczyć względem tła, nie bezwzględnie.
