# Homometryczny kontrprzykład TIMDR: identyczne widmo mocy i globalne MIN–MAX–CZAS

Data: 2026-11-14. Skrypt: `homometric_relations_test.py`.

## Konstrukcja
Weź dwie skończone sekwencje A=[1,-2,-1,2,-1,0,0] i B=[1,-1,1,-1,2,2,-2]. Zdefiniuj X=A*B i Y=A*reverse(B), gdzie * oznacza splot liniowy. Z twierdzenia o transformacie Fouriera: |FFT(X)|²=|FFT(Y)|² dla każdego wspólnego dopełnienia zerami, ponieważ odwrócenie B nie zmienia modułu jego transformaty. Autokorelacje X i Y są identyczne.

Konkretnie:
- X=[1,-3,2,0,0,2,-11,7,4,-6,2,0,0]
- Y=[-2,6,0,-11,7,0,-2,2,-4,3,-1,0,0]
- Oba: MIN=-11, MAX=7, podpisane Δt=t_MAX−t_MIN=1.
- Oba: to samo widmo mocy, choć różnią się lokalną sekwencją.
- Weryfikacja numeryczna: maksymalna różnica widm mocy po dopełnieniu do N=64: 2.8421709430404007e-13.

## Protokół
Dane treningowe: 2000; testowe: 1000. Dla każdej próbki losowa wspólna translacja wzorca o 8..39 próbek i dodatnie skalowanie 0.5..2.0. Klasa 0: X, klasa 1: Y. Klasy zrównoważone. Cechy: globalna trójka (min,max,podpisane Δt/N), widmo mocy FFT, autokorelacja opóźnień 1..23, 12 kolejnych próbek w otoczeniu automatycznie wykrytego globalnego minimum, zespolone FFT (część rzeczywista i urojona), surowe 64 próbki. Każda reprezentacja: StandardScaler + LogisticRegression(max_iter=3000). Oddzielne ziarna treningu i testu.

## Faktyczne wyniki
```
global3 0.479
power 0.485
autocorr 0.48
relative_local_sequence 1.0
complex_fft 0.767
full_signal 0.682
global_triple_X -11 7 1
global_triple_Y -11 7 1
max_power_difference 2.8421709430404007e-13
```

## Interpretacja
To **ścisły kontrprzykład** do tezy, że globalne (MIN,MAX,Δt) wraz z widmem mocy jednoznacznie identyfikuje każdy proces. Lokalne uporządkowanie może nieść informację, której oba globalne podsumowania nie zawierają. Zespolone FFT i pełny przebieg są informacyjnie wystarczające do odtworzenia X/Y, ale użyta regresja logistyczna nie jest odporna na losowe przesunięcia; ich wynik poniżej 100% nie oznacza braku informacji.

## Ograniczenia
Syntetyczne deterministyczne wzorce, bez szumu i braków próbek; etykieta to tożsamość wzorca, nie przyszły proces fizyczny. Lokalna reprezentacja ma 12 współrzędnych, a nie 3. Losowe skalowanie zachowuje równość widm między sparowanymi wariantami, nie pomiędzy wszystkimi przykładami. Globalne MIN i MAX po skalowaniu zmieniają się, ale identycznie dla obu klas i niezależnie od etykiety. Nie badano odporności na pomiarowy zegar nieliniowy.

## Następny krok
Zastąpić 12 próbek kilkoma lokalnymi trójkami i relacjami między nimi; wprowadzić szum, braki próbek i nieliniowy zegar. Oddzielnie ocenić identyfikację procesu od predykcji przyszłości.
