# CHF — wynik pierwszego testu syntetycznego (2026-11-19)

Uruchomiono lokalną reprodukcję algorytmu z `benchmark.py` (NumPy 2.3.5, SciPy 1.17.0, scikit-learn 1.8.0). Seed=42, 480 okien, 60 grup, 45 grup treningowych i 15 testowych, jeden podział GroupShuffleSplit.

| Konfiguracja | AUROC | AUPRC |
|---|---:|---:|
| FFT + statystyki | 0.5581 | 0.5487 |
| + Chronoproces | 0.5272 | 0.5346 |
| + Helisa | 0.5522 | 0.5513 |
| + M/S G K | 0.6183 | 0.5991 |
| + Trójwęzeł | 0.6247 | 0.6104 |

Różnica pełnego wariantu względem FFT+statystyki: +0.0666 AUROC; przyrost samego trójwęzła względem poprzedniego wariantu: +0.0064 AUROC.

**Interpretacja: INCONCLUSIVE.** Jeden podział syntetyczny nie uzasadnia przewagi ogólnej. Brak niezależnych zbiorów rzeczywistych, powtórzeń seedów, przedziałów ufności, silnej fuzji bazowej i kontroli topologii Möbiusa. To nie jest wynik kliniczny ani dowód matematyczny. Konieczne testy na wielu podziałach i rzeczywistych sygnałach.
