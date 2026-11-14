# TIMDR — osiem hipotez relacji i selektywna decyzja (2026-11-14)

## Cel
Sprawdzić, czy zachowanie wielu hipotez trzech zdarzeń poprawia identyfikację i czy heurystyczna pewność nadaje się do decyzji UNKNOWN.

## Protokół
Trzy rzeczywiste zdarzenia o odstępach źródłowych (30,60) lub (60,30); pięć fałszywych znaczników. Początek U(25,65); zegar f(t)=255(t/255)^p, p=exp(U(-1.6,1.6)). Rzeczywiste obserwowane czasy zaburzone szumem σ=1.5. Dwanaście niezależnych znaczników czasu z szumem σ=1.5; monotoniczne wymuszenie i odwrotna interpolacja. Spośród kombinacji trzech spośród ośmiu kandydatów pozostaje osiem najlepszych według dopasowania do sumy odstępów 90 i wzorców 30/60. Wagi exp(-score/1.5), głosowanie na klasę. Pewność = maksymalna ważona frakcja głosów. Walidacja 3000 prób (2999 poprawnych rekordów), test 5000 prób, oddzielne ziarna. Próg UNKNOWN dobierany wyłącznie na walidacji, maksymalizując pokrycie przy docelowej trafności i min. 100 zaakceptowanych przykładach.

**Uwaga:** generator podaje algorytmowi bezpośrednio osiem kandydackich znaczników czasu, a nie surowy sygnał. Nie jest to test detekcji trójek MIN–MAX w szumie. Wynik dotyczy wyłącznie selekcji relacji pomiędzy zdarzeniami.

## Faktycznie zmierzone wyniki
```
validation 2999 test 5000
top1_accuracy 0.7008
top8_vote_accuracy 0.6884
true_in_top1 0.5372 true_in_top8 0.9072
target 0.75 threshold 0.605 validation_coverage 0.6329 validation_acc 0.7571 test_coverage 0.6376 test_acc 0.7578
target 0.8 threshold 0.655 validation_coverage 0.4912 validation_acc 0.8011 test_coverage 0.501 test_acc 0.7932
target 0.85 threshold 0.775 validation_coverage 0.2758 validation_acc 0.8537 test_coverage 0.2802 test_acc 0.8458
target 0.9 no_valid_threshold
confidence_bin 0.5 0.6 n 1737 mean_confidence 0.545 accuracy 0.564
confidence_bin 0.6 0.7 n 1204 mean_confidence 0.645 accuracy 0.653
confidence_bin 0.7 0.8 n 824 mean_confidence 0.746 accuracy 0.762
confidence_bin 0.8 0.9 n 522 mean_confidence 0.844 accuracy 0.835
confidence_bin 0.9 1.01 n 713 mean_confidence 0.977 accuracy 0.86
```

## Wnioski
Top-8 obejmuje poprawny zestaw zdarzeń w 90.7% prób, lecz naiwne głosowanie ośmiu hipotez osiąga 68.84%, mniej niż 70.08% przy top-1. Oznacza to, że wysoki *oracle inclusion* nie przekłada się automatycznie na lepszą decyzję. Heurystyczna pewność jest zawyżona w najwyższym przedziale: średnia 0.977 przy trafności 0.86. Zatem nie należy interpretować jej jako skalibrowanego prawdopodobieństwa poprawności. Przy celu 85% na walidacji test osiąga 84.58% przy pokryciu 28.02%. Brak gwarancji ryzyka selektywnego.

## Ograniczenia
Syntetyczne znaczniki, nie surowe przebiegi. Funkcja punktacji zna możliwe odstępy generatora, co ogranicza interpretację generalizacji. Brak niezależnej przyszłości. Zdarzenia nie mają tu mierzonej pełnej trójki MIN–MAX–Δt; badana jest wyłącznie relacja między ich czasami. Brak kalibracji probabilistycznej i przedziałów ufności.

## Następny krok
Ocenić prawdopodobieństwa poprawności hipotez na walidacji, osobno skalibrować pewność decyzji, i sprawdzić na surowym sygnale, czy top-k rzeczywiście pomaga przy wykrywaniu lokalnych trójek.
