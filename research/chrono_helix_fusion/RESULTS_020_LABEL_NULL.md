# RESULTS 020 — Permutacje etykiet w parach impuls–kontrola

Data: 2026-11-19. **Uruchomiono** na 16 rzeczywistych nagraniach CWRU, po 5 dopasowanych par z każdego, łącznie 80 par. Cechy wyłącznie z następnego okna (lag=1). Leave-one-recording-out, skalowanie wyłącznie treningowe. Null: losowa zamiana etykiet impuls/kontrola w każdej parze i pełne ponowne trenowanie klasyfikatora; seed 20261119.

| Metoda | AUROC | Trafność w parach | Losowania | Jednostronne p |
|---|---:|---:|---:|---:|
| RMS | 0.6375 | 0.6625 | 399 | 0.0025 |
| Relacje fazowe | 0.6125 | 0.6250 | 399 | 0.0350 |
| Wszystkie 20 cech | 0.6025 | 0.5875 | 99 | 0.0500 |

Wyniki kontrolne: RMS null mean 0.4946, 95% [0.3575,0.5976]; faza null mean 0.5038, 95% [0.3699,0.6153]; wszystkie null mean 0.5019, 95% [0.3698,0.6066].

**Wniosek:** predykcja z kolejnego okna jest silniejsza niż losowe przypisanie etykiet w parach, szczególnie dla RMS. Nie jest to dowód fizycznej pamięci, gdyż impulsy zdefiniowano przez crest factor i dopasowanie RMS/czasu nie gwarantuje wymienności par. Brak przewagi fazy lub połączonych cech nad RMS. Wyniki eksploracyjne, wielokrotne testy i brak niezależnej walidacji.

**Ograniczenia:** null permutacyjny nie zachowuje fizycznych własności sygnału i nie jest IAAFT; w parze może być zależność między sąsiednimi oknami; część zdarzeń i kontroli może być blisko siebie. Nie testowano pełnego CHF. Następny krok: surogaty IAAFT lub dopasowane procesy stochastyczne na oryginalnych próbkach, a następnie ponowny wybór impulsów i całego procesu oceny.

Reprodukcja: `python research/chrono_helix_fusion/chf_stage_020.py CWRU_CHF.zip`. Lokalny kod i JSON udostępniono jako pliki do pobrania w rozmowie.
