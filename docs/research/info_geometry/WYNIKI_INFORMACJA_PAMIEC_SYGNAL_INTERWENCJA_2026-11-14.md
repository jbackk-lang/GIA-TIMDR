# TIMDR: informacja relacyjna, pamięć i interwencja przyczynowa — 2026-11-14

## Pytanie
Czy informacja zakodowana w historii zdarzeń jest jedynie predyktorem, czy jej odpowiednik jako stan pamięci może wpływać przyczynowo na przyszły sygnał?

## Konstrukcja
Dwie historie długości 128, jedna jest dokładnym odwróceniem czasowym drugiej. Końcowy stan obu jest równy zero, a widma mocy identyczne z dokładnością numeryczną (maksymalna różnica 7.1054e-15). Historia ma impulsy w pozycjach 20,30,70,86, wygładzone symetrycznym jądrem. 6000 przykładów, szum obserwacji σ=.035, 70% trening / 30% test, losowanie ziarno 341, podział ziarno 13.

Losowa klasa historii H∈{0,1}; stan pamięci M=H bez interwencji. W około połowie przykładów wykonywana jest randomizowana interwencja: M otrzymuje nową niezależną wartość 0 albo 1, a historia H pozostaje bez zmian. Przyszły sygnał: Y=0.6(2M−1)+ε, ε~N(0,.35); zadanie: przewidzieć znak Y.

Reprezentacje: bieżąca próbka, globalna trójka (minimum,maksimum,podpisana odległość czasowa ekstremów), widmo mocy, osiem próbek uporządkowanej historii, rzeczywisty stan pamięci (oracle). Model: StandardScaler+LogisticRegression trenowany na mieszance obu trybów. Wyniki oddzielnie dla przykładów naturalnych i interwencyjnych.

## Faktyczne wyniki uruchomienia
```
exact_base_power_diff 7.105427357601002e-15
same_present [0.0, 0.0]
subset all count 1800 history_memory_agreement 0.7333333333333333
instantaneous acc 0.5067 auc 0.5
global_triplet acc 0.7178 auc 0.7229
power_spectrum acc 0.52 auc 0.5162
ordered_history acc 0.7178 auc 0.7255
true_memory acc 0.9644 auc 0.9644
subset natural count 894 history_memory_agreement 1.0
instantaneous acc 0.4989 auc 0.5
global_triplet acc 0.9664 auc 0.9615
power_spectrum acc 0.5067 auc 0.5002
ordered_history acc 0.9664 auc 0.9588
true_memory acc 0.9664 auc 0.9664
subset intervened count 906 history_memory_agreement 0.47019867549668876
instantaneous acc 0.5143 auc 0.5
global_triplet acc 0.4724 auc 0.4736
power_spectrum acc 0.5331 auc 0.5327
ordered_history acc 0.4724 auc 0.4836
true_memory acc 0.9625 auc 0.9624
do_history 0 do_memory 0 n 733 mean_future -0.5816
do_history 0 do_memory 1 n 742 mean_future 0.6016
do_history 1 do_memory 0 n 795 mean_future -0.604
do_history 1 do_memory 1 n 708 mean_future 0.5883
future_effect_do_memory 1.1884
```

## Interpretacja
Obserwacyjnie historia przewiduje przyszłość, bo M=H w trybie naturalnym. Randomizowana zmiana M przy zachowaniu H odcina tę korelację: historia przestaje przewidywać, ale znajomość M nadal wystarcza. Różnica średniej przyszłego sygnału między interwencjami do(M=1) i do(M=0) wynosi 1.1884, zgodnie z wbudowaną do generatora różnicą 1.2.

**Ważne zastrzeżenie:** przyczynowość nie została odkryta w danych, lecz została zdefiniowana w równaniu generatora i potwierdzona przez test. Nie dowodzi to, że informacja jest niezależną siłą fizyczną. Ponadto globalna trójka w tym generatorze koduje historię i działa tak samo dobrze jak uporządkowane cechy — to nie jest test wyłącznej przewagi lokalnych relacji. Oba wzorce mają takie samo widmo tylko bez szumu; losowy szum w pojedynczych realizacjach zmienia widmo.

## Następny eksperyment
Zastosować dwa procesy o identycznych globalnych trójkach i widmach, ale różnych relacjach lokalnych, a następnie przeprowadzić interwencję na relacji z kontrolą stanu ukrytego. Porównać rzeczywistą manipulację informacją z czysto obserwacyjną zmianą etykiety.
