# TIMDR — ukryta zmiana wymuszenia a pamięć, 2026-11-14

## Model i protokół
6000 syntetycznych trajektorii długości 48, ziarno 2026111411. Stan z[t+1]=α*z[t]+u0+δ*I(t≥τ), α~U(.82,.94), u0~N(0,.035), τ losowo 12..35, δ o losowym znaku i wartości bezwzględnej U(.035,.085). Połowa przebiegów bez zmiany (δ=0). Obserwacje z+N(0,.012). Parametry α i u0 estymowane z pierwszych 10 próbek metodą regresji liniowej; algorytm nie zna ich prawdziwych wartości.

Reszta r[t]=z_observed[t+1]−α_hat*z_observed[t]−u0_hat. Algorytm skanuje możliwe chwile zmiany 12..35 i maksymalizuje bezwzględną różnicę średnich reszt przed i po kandydackiej zmianie. Baseline: bez skanowania, bezwzględna średnia reszta po chwili 10. Próg dobrano wyłącznie na walidacji (1000 próbek), maksymalizując F1; test 2000, trening 3000 nie jest wykorzystywany przez algorytm. Wyniki z faktycznego uruchomienia:

```
scan threshold 0.02841 auc 0.9996 accuracy 0.994 precision 0.999 recall 0.989
scan detected n 989 tau_mae 0.525 within3 0.9646
mean_residual threshold 0.02009 auc 0.9673 accuracy 0.913 precision 0.9214 recall 0.903
alpha_mae 0.0977 true_changed_fraction 0.5
local_extrema_mean_peaks_valleys [2.45, 2.44]
nonidentifiability_example [(0.82, 0.0059), (0.94, -0.01277)]
```

## Wnioski
W tym generatorze skanowanie zmiany reszt pozwala odróżnić skok ukrytego wymuszenia od powolnej ewolucji pamięci. Bardzo dobra detekcja (99.4% trafności) współistnieje ze słabą identyfikacją α (MAE 0.0977). To ważne rozdzielenie detekcji zmiany, identyfikacji parametrów i predykcji.

## Ograniczenia
Algorytm zakłada, że przed chwilą 12 wymuszenie jest stałe, a później może nastąpić **co najwyżej jeden skok**; skanowany zakres 12..35 jest znany. Wymuszenie nie jest dowolnym nieznanym sygnałem. Przy dowolnym u[t] parametr α jest nieidentyfikowalny bez dodatkowych ograniczeń, ponieważ dla każdego α można zdefiniować u[t]=z[t+1]−α*z[t]. Nie przeprowadzono tutaj predykcji przyszłego sygnału ani oceny skuteczności relacji między trójkami MIN–MAX–Δt. Średnia liczba wykrytych lokalnych maksimów i minimów to odpowiednio 2.45 i 2.44; nie były użyte do klasyfikacji. Wynik nie dowodzi fizycznego działania abstrakcyjnej informacji.

## Następny test
Zbadać powolny dryf wymuszenia, wiele skoków i zmianę samego α; porównać konkurencyjne modele „zmiana pamięci” oraz „nowe oddziaływanie” na tych samych przebiegach, zachowując lokalne trójki jako opis zdarzeń.
