# TIMDR — niezależny zegar i odzyskiwanie metrycznych relacji

Data: 2026-11-14. Kod: `reference_clock_recovery.py`.

## Hipoteza
Wspólny silnie nieliniowy zegar zniekształca proporcję odstępów między trzema zdarzeniami. Znaczniki niezależnego czasu źródłowego umożliwiają odwrócenie tego zniekształcenia i poprawiają identyfikację klasy układu odstępów.

## Metoda
Klasa 0: odstępy (24,48); klasa 1: (48,24). Początek losowy U(20,60). Czas obserwowany f(t)=200(t/200)^p, gdzie p=exp(U(-2.2,2.2)) w teście i p=exp(U(-.45,.45)) w treningu. Trening 6000, test 3000 na wariant. Niezależne znaczniki o znanych źródłowych czasach rozmieszczone równomiernie w [10,170], w liczbie 4,8,16,32,64. Obserwowane odczyty znaczników f(t)+N(0,σ), σ=0,1,4. Korekcja: monotoniczne wymuszenie odczytów przez maksimum skumulowane, a następnie liniowa interpolacja odwrotności zegara. Klasyfikator: StandardScaler + LogisticRegression trenowany wyłącznie na niezniekształconej proporcji z treningu. Testowany na proporcji surowej i skorygowanej.

## Wyniki uruchomienia
```
markers noise representation accuracy median_absolute_ratio_error
0 0 raw 0.855 0.0893
4 0 raw 0.858 0.0194
4 0 corrected 0.989 0.0194
4 1 corrected 0.9387 0.0216
4 4 corrected 0.912 0.0421
8 0 raw 0.8623 0.0017
8 0 corrected 1.0 0.0017
8 1 corrected 0.9523 0.0186
8 4 corrected 0.8787 0.0737
16 0 raw 0.8623 0.0009
16 0 corrected 1.0 0.0009
16 1 corrected 0.944 0.0196
16 4 corrected 0.8883 0.0752
32 0 raw 0.8603 0.0002
32 0 corrected 1.0 0.0002
32 1 corrected 0.944 0.0198
32 4 corrected 0.883 0.0684
64 0 raw 0.86 0.0
64 0 corrected 1.0 0.0
64 1 corrected 0.935 0.0207
64 4 corrected 0.886 0.0675
```

## Interpretacja
Przy idealnych znacznikach korekcja z 8 punktów odzyskała 100% rozróżnienia układów czasowych. Przy zaszumionych znacznikach poprawa jest ograniczona, a zwiększanie liczby punktów bez modelu wygładzającego nie musi pomagać. Zatem niezależny zegar może usuwać nieidentyfikowalność metryki czasu, ale tylko w granicach jakości kalibracji.

## Ograniczenia
To **syntetyczne, dokładne czasy trzech zdarzeń**, bez detekcji ekstremów w surowym sygnale. Trójki (MIN,MAX,Δt) pozostają koncepcją zdarzenia, lecz ten eksperyment testuje wyłącznie relację między ich czasami. Przyszłość nie jest generowana; etykieta to klasa układu odstępów. Znaczniki są idealnie zsynchronizowane w czasie źródłowym, co jest silnym założeniem. Wymuszenie monotoniczności odczytów i interpolacja są uproszczonym estymatorem zegara. Nie wykazano uniwersalnej odporności na dowolny warp.

## Następny krok
Dodać wykrywanie trójek z zaszumionego sygnału oraz osobno kalibrować zegar i niepewność detekcji; porównać interpolację z monotoniczną regresją izotoniczną lub modelem gładkiego zegara na osobnym zbiorze walidacyjnym.
