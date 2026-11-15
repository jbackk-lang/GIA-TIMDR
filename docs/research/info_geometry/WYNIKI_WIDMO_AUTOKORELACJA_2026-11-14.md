# Widmo, autokorelacja i relacje ekstremów — 2026-11-14

## Cel
Sprawdzić, czy widmo częstotliwościowe i autokorelacja niosą więcej informacji o przyszłej dynamice niż pojedyncza para MIN–MAX–CZAS, zwłaszcza gdy fałszywe impulsy zakłócają detekcję.

## Protokół
3000 syntetycznych przykładów treningowych, po 1500 przykładów testowych w warunkach zgodnych z treningiem, trudnych oraz z niezależną etykietą (kontrola negatywna). Obserwacja: 160 próbek, dwa właściwe przeciwne impulsy Gaussa, ich odstęp 16..24 albo 43..51 próbek, losowe położenie. Dodatkowe impulsy: 0..2 w treningu i łatwym teście, 2..7 w trudnym. Braki: 5% albo 22%, interpolowane; szum Gaussa 0.1 albo 0.2. Nieliniowy zegar `f(t)=(t/159)^p`, p losowane ze wskazanych w kodzie zakresów. Przyszłość: 128 próbek AR(1), α=.2 albo .8; etykieta wyznaczona z autokorelacji przyszłego fragmentu >.5.

Cechy: `temporal` = maksimum i minimum wygładzonego sygnału, znormalizowany odstęp między nimi w nieliniowym zegarze i flaga poprawnej detekcji (4 cechy; **nie dokładnie trzy**); `spectrum` = log(1+|rFFT(x−mean(x))|²), 80 dodatnich częstotliwości bez DC; `autocorr` = znormalizowane iloczyny opóźnień 1..64; konkatenacje temporal+spectrum i temporal+autocorr. Klasyfikatory: standaryzowana regresja logistyczna C=.1 oraz las losowy 180 drzew, min_samples_leaf=8. Trening tylko na łagodnych zakłóceniach. W teście trudnym **widmo i autokorelacja są liczone względem indeksów próbek**, a nie nieregularnego czasu fizycznego; nieliniowy zegar wpływa wyłącznie na cechę odstępu. To ważne ograniczenie porównania.

## Rzeczywiste wyniki
```
DATA matched pair_correct 1.0 positive_rate 0.5
matched temporal logistic acc 1.0 auc 1.0
matched temporal forest acc 1.0 auc 1.0
matched spectrum logistic acc 0.9933 auc 0.9998
matched spectrum forest acc 0.996 auc 0.9999
matched autocorr logistic acc 0.9933 auc 0.9999
matched autocorr forest acc 0.9973 auc 1.0
matched temporal+spectrum logistic acc 1.0 auc 1.0
matched temporal+spectrum forest acc 1.0 auc 1.0
matched temporal+autocorr logistic acc 1.0 auc 1.0
matched temporal+autocorr forest acc 1.0 auc 1.0
DATA hard pair_correct 0.4827 positive_rate 0.5
hard temporal logistic acc 0.7133 auc 0.6859
hard temporal forest acc 0.718 auc 0.7513
hard spectrum logistic acc 0.752 auc 0.8211
hard spectrum forest acc 0.7327 auc 0.8109
hard autocorr logistic acc 0.788 auc 0.866
hard autocorr forest acc 0.802 auc 0.8879
hard temporal+spectrum logistic acc 0.744 auc 0.783
hard temporal+spectrum forest acc 0.7387 auc 0.822
hard temporal+autocorr logistic acc 0.7693 auc 0.8498
hard temporal+autocorr forest acc 0.814 auc 0.888
DATA negative pair_correct 0.4913 positive_rate 0.4853
negative temporal logistic acc 0.4813 auc 0.4745
negative temporal forest acc 0.48 auc 0.4834
negative spectrum logistic acc 0.49 auc 0.5001
negative spectrum forest acc 0.5 auc 0.4941
negative autocorr logistic acc 0.488 auc 0.4829
negative autocorr forest acc 0.4847 auc 0.48
negative temporal+spectrum logistic acc 0.478 auc 0.4797
negative temporal+spectrum forest acc 0.48 auc 0.4857
negative temporal+autocorr logistic acc 0.478 auc 0.4738
negative temporal+autocorr forest acc 0.4833 auc 0.474
```

## Interpretacja
W trudnym teście cechy spektralne i autokorelacyjne wyprzedziły naiwną selekcję najsilniejszej pary. Najlepsza trafność w porównaniu to 81.4% dla połączenia temporal+autocorr (las losowy), wobec 71.8% dla temporal (las losowy). W kontroli negatywnej wszystkie reprezentacje są blisko losowości. Przy poprawnym wykryciu pary w łatwych warunkach sama cecha czasowa wystarcza.

**Zastrzeżenia:** 81.4% to maksimum po porównaniu wielu wariantów na tym samym zbiorze testowym — nie jest niezależną oceną po selekcji modelu. Porównanie 4 cech temporalnych, 80 widmowych i 64 autokorelacyjnych nie jest wyrównane budżetem wymiarów. Magnituda FFT traci fazę, ale zachowuje informację o odległościach zdarzeń w mocy widma; autokorelacja jest matematycznie związana z widmem mocy (twierdzenie Wienera–Chinczyna), więc nie stanowią niezależnych kanałów dowodowych. Żaden wynik nie dowodzi ogólnej wystarczalności MIN/MAX/CZAS ani uniwersalnej przewagi widma.

## Następny test
Porównanie na tym samym budżecie cech (np. 3, 8, 16), walidacyjny wybór modeli, odłożony test, widmo liczone po fizycznym czasie przy nieliniowym zegarze, niezależna kontrola generatora. Sprawdzić widmo fazowe i lokalne STFT, które zachowują kolejność zdarzeń.
