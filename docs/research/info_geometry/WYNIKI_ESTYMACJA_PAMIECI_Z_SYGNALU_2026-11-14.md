# TIMDR — estymacja pamięci z odpowiedzi wygaszania (2026-11-14)

## Pytanie
Czy nieznany współczynnik zanikania pamięci α da się odtworzyć z obserwacji sygnału i czy poprawia to przewidywanie przyszłości na podstawie lokalnych trójek MIN–MAX–Δt i ich relacji?

## Generator
4000 trening, 2000 test, ziarno 2026111408. Dwa homometryczne zestawy zdarzeń A=[0,1,4,10,12,17] i B=[0,1,8,11,13,17], sześć par impulsów MIN=-0.4a, MAX=a, Δt=2, a~U(.8,1.2). Długość 128, losowy początek 17..29, zdarzenia co 5 jednostek wzorca. Pamięć z[t+1]=α z[t]+x[t], α~U(.82,.94). Historia obserwowana z szumem σ=.10; detekcja find_peaks(prominence=.40,distance=4) i lokalnych minimów w poprzednich 3 próbkach. Następnie dostępne osiem próbek niezależnie obserwowanego wygaszania z*α^k+N(0,.018), k=0..7. Cel: przewidzieć przyszłą próbkę z*α^8+N(0,.045). α estymowane z regresji log(próbki) względem k, z ograniczeniem [0.70,.99], a przy mniej niż czterech dodatnich pomiarach przyjmowane .88. Modele Ridge i HistGradientBoostingRegressor trenowane wyłącznie na treningu, test niezależny.

## Faktyczne wyniki
```
samples 4000 2000 detector_complete 1.0
alpha_mae 0.03498856218194941 alpha_rmse 0.04740633477136495
relations ridge r2 0.001 rmse 0.07351
relations hgb r2 -0.0306 rmse 0.07466
true_alpha ridge r2 0.4291 rmse 0.05557
true_alpha hgb r2 0.5142 rmse 0.05126
estimated_alpha ridge r2 0.0536 rmse 0.07155
estimated_alpha hgb r2 0.2355 rmse 0.06431
probe ridge r2 0.6153 rmse 0.04562
probe hgb r2 0.5973 rmse 0.04668
relations_probe ridge r2 0.6112 rmse 0.04586
relations_probe hgb r2 0.5982 rmse 0.04662
oracle_state_alpha ridge r2 0.6083 rmse 0.04603
oracle_state_alpha hgb r2 0.6154 rmse 0.04561
physics_probe_last_times_alpha r2 0.578 rmse 0.04778
identical_history_alpha 0.82 final_state 0.013921 future_k8 0.002846
identical_history_alpha 0.94 final_state 0.254682 future_k8 0.155246
```

## Interpretacja
Historia impulsów nie identyfikuje α: dla identycznego wejścia można uzyskać różne stany końcowe i różną przyszłość, zależnie od nieznanego parametru układu. Krótka obserwacja wygaszania niesie informację zarówno o stanie, jak i o dynamice; daje lepszą prognozę niż wyodrębnianie jednego szumnego oszacowania α. Model korzystający z próbek odpowiedzi uzyskał R²=0.6153, praktycznie tyle samo co kontrola ze znanym stanem i α (R²=0.6154 dla HGB). Dodanie relacji nie poprawiło wyniku w tym generatorze.

## Ograniczenia
To syntetyczny liniowy filtr, nie fizyczny pomiar ani dowód autonomicznej sprawczości informacji. Osiem próbek wygaszania jest dodatkowym pomiarem stanu, a nie informacją możliwą do odczytania z samej historii wejściowej. Porównanie Ridge i HGB ma nierówną pojemność modelu; przyczyną niskiego wyniku relacji może być niedopasowanie i ograniczona identyfikowalność. Detektor nie miał fałszywych zdarzeń. Brak osobnego zestawu walidacyjnego do doboru hiperparametrów. Lokalna trójka zachowana jako MIN, MAX, Δt, a relacje jako osobne cechy.

## Następny test
Kontrolowane porównanie: (a) sam sygnał wejściowy, (b) trójki i relacje, (c) obserwacja wygaszania, (d) estymacja α i stanu przy różnych poziomach szumu oraz liczbie próbek; z oddzielną walidacją, fałszywymi zdarzeniami i brakującymi pomiarami.