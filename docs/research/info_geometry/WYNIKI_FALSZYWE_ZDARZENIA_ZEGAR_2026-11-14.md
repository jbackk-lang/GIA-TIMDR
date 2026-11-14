# Fałszywe zdarzenia, braki próbek i nieliniowy zegar — 2026-11-14

## Projekt
Eksperyment wykonany w Pythonie (numpy, scikit-learn), kod lokalny `/mnt/data/timdr_experiment/false_events_clock_test.py`. Trening 3000 syntetycznych sygnałów, testy po 1500. Obserwacja 160 próbek: dwa właściwe impulsy Gaussa o amplitudzie ±2, odległość 16..24 albo 43..51, losowy początek 12..89. Dodatkowe impulsy zakłócające o nieznanej liczbie: trening i test podobny 0..2, test przesunięty 2..7. Zakłócenia amplitudowe: 0.1 versus 0.2; braki próbek: 5% versus 22%, uzupełniane interpolacją. Czas pomiaru transformowany nieliniowo `f(t)=(t/159)^p`, `p=exp(U(-0.12,0.12))` lub `p=exp(U(-0.65,0.65))`.

Detektor: wygładzenie pięciopunktowe, wyszukiwanie lokalnych ekstremów przekraczających próg 0.35; wybór najwyższego maksimum i najniższego minimum. Reprezentacja: (maksimum, minimum, |f(t_max)-f(t_min)|, flaga kompletności). Uwaga: czwarta flaga oznacza brak detekcji, więc jest to technicznie **cztery cechy**, nie ścisłe trzy; w tych warunkach flaga nie wnosi istotnej informacji. Porównano model na amplitudach, na odstępie i fladze, oraz na wszystkich czterech cechach.

Przyszłość: niezależny 128-próbkowy AR(1) z α=0.2 albo 0.8, zgodnie z klasą odstępu; etykieta wyliczona z przyszłej autokorelacji >0.5. Standaryzacja i regresja logistyczna trenowane tylko na danych treningowych. UNKNOWN gdy `|p_pred-0.5|<0.2`; próg niekalibrowany.

## Wynik wykonania
```
matched amplitude_only accuracy 0.4933 coverage 0.0 covered_acc NA
matched time_only accuracy 1.0 coverage 1.0 covered_acc 1.0
matched min_max_time accuracy 1.0 coverage 1.0 covered_acc 1.0
matched pair_recall 1.0 mean_candidates 2.81
shifted amplitude_only accuracy 0.4967 coverage 0.0313 covered_acc 0.5319
shifted time_only accuracy 0.714 coverage 0.9593 covered_acc 0.7234
shifted min_max_time accuracy 0.714 coverage 0.9587 covered_acc 0.7253
shifted pair_recall 0.4967 mean_candidates 5.52
negative amplitude_only accuracy 0.502 coverage 0.0333 covered_acc 0.46
negative time_only accuracy 0.5053 coverage 0.96 covered_acc 0.5035
negative min_max_time accuracy 0.5073 coverage 0.9673 covered_acc 0.5017
negative pair_recall 0.4993 mean_candidates 5.56
```

`pair_recall` oznacza poprawność rozpoznania obu zdarzeń z tolerancją ±4 próbek względem prawdziwych centrów i błędu odstępu ≤5 próbek. Jest to **dokładność identyfikacji pary**, nie standardowy recall wszystkich kandydatów. `coverage` oznacza odsetek prognoz bez UNKNOWN.

## Wniosek
Przy silnym przesunięciu rozkładu skuteczność predykcji spadła do 71.4%, a rozpoznanie właściwej pary do 49.7%. Dobre cechy czasu nie naprawiają błędnego wyboru zdarzeń. Kontrola negatywna 50.7%. Test jest konstrukcyjny: klasa przyszłości została świadomie powiązana z odstępem właściwych impulsów, a model nie był walidowany na sygnałach fizycznych.

## Następny eksperyment
Porównać wybór najsilniejszych ekstremów z metodą wielu hipotez par zdarzeń i odrzucaniem UNKNOWN; oddzielnie oceniać detekcję, identyfikację pary i prognozę. Dodać kalibrację abstencji na osobnej walidacji.
