# CHF — zweryfikowana walidacja 20 podziałów (2026-11-19)

Źródło: [GitHub Actions, run 44547235506](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/44547235506), zakończony **success**. Dwa testy jednostkowe 12 kHz: **OK**. Raport: [artefakt 14539478788](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/44547235506/artifacts/14539478788).

| Wariant | AUROC mean ± SD | AUPRC mean ± SD |
|---|---:|---:|
| FFT + statystyki | 0.56993 ± 0.04811 | 0.58588 ± 0.04784 |
| Fuzja bez mostów | 0.66486 ± 0.04914 | 0.66564 ± 0.06112 |
| Oryginalny trójwęzeł | 0.65618 ± 0.05070 | 0.66099 ± 0.06033 |
| Mosty z opóźnieniem | 0.66465 ± 0.04950 | 0.66478 ± 0.05739 |

Średnia różnica AUROC (mosty minus fuzja bez mostów) = **−0.0002083**, SD różnic = **0.02766**. Mosty lepsze w **12 z 20** podziałów, ale średnia różnica nie jest dodatnia.

**Wniosek:** obecny syntetyczny test nie potwierdza przyrostowej korzyści z mostów. Fuzja cech wypada lepiej niż FFT+statystyki, lecz nie należy przypisywać tej różnicy samym mostom. Wyniki dotyczą syntetycznych zaburzeń fazy, nie rzeczywistych łożysk.

**Następna hipoteza falsyfikowalna:** sprawdzić mosty na niezależnych pomiarach CWRU, z rozdzieleniem obciążeń i pełnym próbkowaniem 12 kHz. Potrzebne również silniejsze kontrole, np. cechy opóźnione bez struktury trójwęzła i kontrola permutacyjna.
