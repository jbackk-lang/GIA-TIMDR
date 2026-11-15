# Surowy zaszumiony sygnał — estymacja MIN/MAX/CZAS

Data: 2026-11-14. **Status: kod uruchomiony lokalnie na syntetycznych przebiegach.** Biblioteki: numpy, scikit-learn.

## Protokół
Każda próbka obserwacji to 101 wartości sygnału złożonego z dwóch przeciwnych impulsów Gaussa o szerokości 2.2 próbki, oddzielonych odstępem 12–32 albo 58–78 próbek. Kolejność znaków losowa; tło: niezależny szum Gaussa o odchyleniu standardowym σ. Estymator czasu ekstremów działa **wyłącznie na obserwowanym przebiegu**, po wygładzeniu średnią ruchomą z pięciu próbek. Trzy cechy: minimum surowego sygnału, maksimum surowego sygnału, `|t_max−t_min|/100` z wygładzonego sygnału. Bazowy model korzysta tylko z MIN/MAX.

Przyszły sygnał: 128 próbek AR(1) z parametrem 0.2 albo 0.8, zależnie od ukrytego reżimu. Docelowa etykieta **obliczona z przyszłego przebiegu**: empiryczna korelacja opóźnienia 1 > 0.5. Model: regresja logistyczna ze standaryzacją, 1600 przykładów treningowych (seed 1000) i 800 testowych (seed 9000), osobne generatory losowe. Użyto tego samego generatora reżimów dla treningu i testu; nie jest to test generalizacji na inny proces fizyczny.

## Rzeczywisty wynik wykonania
```text
noise,baseline_accuracy,three_feature_accuracy,median_gap_error,unknown_rate,covered_accuracy
0,0.5737,1.0000,0.0,0.0000,1.0000
0.05,0.5025,1.0000,0.0,0.0000,1.0000
0.15,0.4888,1.0000,0.0,0.0000,1.0000
0.3,0.5050,0.9975,1.0,0.0000,0.9975
0.5,0.5100,0.9450,1.0,0.0138,0.9480
```

`median_gap_error` = mediana bezwzględnego błędu oszacowania odstępu względem ukrytych czasów impulsów (wyłącznie metryka diagnostyczna, nie cecha modelu). `unknown_rate` = odsetek prognoz z prawdopodobieństwem w (0.3,0.7); próg jest heurystyczny i nie był kalibrowany na oddzielnym zbiorze walidacyjnym.

## Interpretacja i ograniczenia
W tym generatorze trzecia cecha czasu daje silny wzrost trafności predykcji właściwości przyszłego przebiegu względem MIN/MAX. **Generator celowo koduje przyszły reżim w odległości impulsów**, więc wysoka trafność jest spodziewana i nie dowodzi ogólnej zasady TIMDR. Sygnał ma dwa wyraźne impulsy; nie badano złożonych wieloekstremalnych przebiegów, zakłóceń impulsowych, nierównomiernego próbkowania ani różnych zegarów. Test nie identyfikuje czasu obiektu względem odbiornika, tylko czas zdarzeń w jednym zegarze. Etykieta przyszłości jest bardzo mocno związana z reżimem generatora. Baseline 57.4% przy zerowym szumie może korzystać z subtelnych zależności amplitudowych, np. dyskretnego położenia impulsów, i nie powinien być opisywany jako dokładne 50%.

## Następny krok
Nieregularne próbkowanie, brakujące próbki, impulsy zakłócające, dryft zegara oraz inne szerokości impulsów między treningiem a testem. Ocenić niezależność od konkretnego generatora i kalibrację UNKNOWN.
