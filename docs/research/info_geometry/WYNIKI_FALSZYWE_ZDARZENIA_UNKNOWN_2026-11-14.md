# TIMDR — silne fałszywe zdarzenia i UNKNOWN (2026-11-14)

Test rzeczywiście wykonany lokalnie, skrypt `distractor_unknown_test.py`. 1500 przykładów na wariant, 256 próbek, trzy zdarzenia MIN–MAX: odstępy (30,60) albo (60,30). Prawdziwe zdarzenia: impuls -2 i po 8 próbkach +2. Wariant łatwy: szum σ=.12, dwa słabe fałszywe zdarzenia. Wariant trudny: szum σ=.23, trzy fałszywe zdarzenia o porównywalnej amplitudzie 1.65–2.25 oraz blok 10–24 brakujących próbek uzupełnionych interpolacją. Detektor lokalnych minimów i maksimów, wybór najlepiej pasującej trójki spośród kandydatów. Ocena dopasowania: |d1+d2−90| + 0.3 min(|d1−30|+|d2−60|,|d1−60|+|d2−30|). Jeśli wynik przekracza próg, zwracane jest UNKNOWN.

| Warunek | Próg | Pokrycie | Trafność wśród zaakceptowanych | Poprawne / wszystkie |
|---|---:|---:|---:|---:|
| Łatwy | 5 | 100% | 100% | 100% |
| Trudny | 5 | 50.40% | 89.95% | 45.33% |
| Trudny | 12 | 63.67% | 81.78% | 52.07% |
| Trudny | 25 | 75.40% | 77.54% | 58.47% |
| Trudny | 1000 | 93.13% | 71.73% | 66.80% |

**Wniosek:** fałszywe zdarzenia o sile zbliżonej do prawdziwych psują identyfikację relacji. Heurystyczna abstencja zwiększa trafność odpowiedzi kosztem pokrycia. To nie jest probabilistycznie skalibrowana niepewność.

**Ograniczenia:** brak nieliniowego zegara w tym teście; reguła zna docelowe odstępy generatora; próg nie został dobrany na osobnej walidacji; syntetyczne dane, brak predykcji rzeczywistej przyszłości. Wskaźnik `true_events_in_candidates` w skrypcie jest liczony tylko w zaakceptowanych próbach i nie jest pełną czułością detektora. Kolejny test: walidacja progów, ryzyko selektywne, jednoczesny warp zegara i fałszywe zdarzenia.
