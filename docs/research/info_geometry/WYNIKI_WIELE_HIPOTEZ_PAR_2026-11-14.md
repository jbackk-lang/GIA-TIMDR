# Selekcja wielu hipotez par zdarzeń — 2026-11-14

## Metoda
Eksperyment syntetyczny uruchomiony lokalnie. Reprodukuje generator `false_events_clock_test.py` (wymagany obok skryptu) z dwoma właściwymi impulsami, fałszywymi impulsami, brakami próbek i nieliniowym zegarem. Trening: 3000 przebiegów z łagodnymi zakłóceniami, walidacja: 1000 przebiegów z silnymi zakłóceniami, test: 1500 przebiegów z silnymi zakłóceniami. Osobna kontrola negatywna: 1500 przebiegów z etykietami niezależnymi od przyszłości.

Detektor znajduje wszystkie lokalne maksima dodatnie i minima ujemne po wygładzeniu; tworzy pary dodatni–ujemny i szereguje je według kontrastu amplitud. Porównanie: (1) tylko najsilniejsza para; (2) osiem par z wagami softmax od kontrastu. Regresja logistyczna ze standaryzacją. Dla wariantu wielu par cechy to ważona średnia odstępów, ważany drugi moment odstępów i maksymalna waga. Model nie otrzymuje prawdziwej pary.

Walidacyjny próg abstencji wybierany z siatki 0..0.49 dla celu >=90% trafności zaakceptowanych decyzji. **Żaden próg nie spełnił tego celu**, dlatego użyto awaryjnego 0.49. Nie należy nazywać go skalibrowanym.

## Wynik uruchomienia
```
sets 3000 1000 1500
strongest validation_threshold 0.49 validation_90pct_feasible False
shifted accuracy 0.7187 coverage 0.7407 covered_accuracy 0.7255 correct_pair_in_topk 0.4967
negative accuracy 0.506 coverage 0.7513 covered_accuracy 0.4889 correct_pair_in_topk 0.4993
multipair validation_threshold 0.49 validation_90pct_feasible False
shifted accuracy 0.6713 coverage 0.398 covered_accuracy 0.8007 correct_pair_in_topk 0.9633
negative accuracy 0.4793 coverage 0.4 covered_accuracy 0.4833 correct_pair_in_topk 0.9667
```

## Wniosek
Zachowanie wielu hipotez zwiększa *oracle recall* właściwej pary z 49.7% do 96.3%, ale naiwna agregacja odstępów pogarsza trafność predykcji z 71.9% do 67.1%. Zatem dostępność właściwej pary w zbiorze kandydatów nie oznacza jej identyfikowalności. W kontroli negatywnej wynik bliski 50%. Przy abstencji trafność na pokrytej części to 80.1%, lecz pokrycie tylko 39.8% i cel walidacyjny 90% nie został spełniony.

## Ograniczenia
Zadanie jest konstrukcyjne: ukryty reżim przyszłości zależy od odstępu dwóch właściwych impulsów. Oś czasu jest przekształcana nieliniowo, a algorytm nie ma niezależnego zegara odniesienia. Liczba par ograniczona do 30, ranking wyłącznie amplitudowy; nie przetestowano uczenia rankingu par, pełnego grafu ani kalibracji prawdopodobieństw. *correct_pair_in_topk* to diagnostyka z dostępem do prawdziwych centrów i nie jest cechą modelu.

## Następny test
Uczenie wyboru pary z relacji sąsiedztwa, znaku, kształtu i spójności temporalnej na danych treningowych, następnie test odłożony i kalibracja abstencji bez użycia testowych etykiet.
