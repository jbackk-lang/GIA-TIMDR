# TIMDR — sygnał po przejściu przez filtry

Seed 202611140814; fs=200 Hz, 4 s. Sygnał wejściowy: sin(2π4t)+0.65 sin(2π28t+0.7)+0.13 szum Gaussa. Trzy filtry Butterwortha 4. rzędu (pasmowy 4. rzędu na każdej krawędzi), przyczynowa filtracja sosfilt. Lokalny ekstremum: find_peaks prominence=0.25, distance=3; Δt jako odstęp od ostatniego minimum przed maksimum.

| Wariant | RMS | Maksima | Minima | Mediana Δt [s] |
|---|---:|---:|---:|---:|
| Wejście | .85750 | 112 | 112 | .020 |
| Dolnoprzepustowy 8 Hz | .70184 | 16 | 15 | .125 |
| Górnoprzepustowy 15 Hz | .48115 | 112 | 112 | .020 |
| Pasmowy 25–31 Hz | .45790 | 109 | 109 | .020 |

Wzmocnienie amplitudy na 4 i 28 Hz: LP [0.99811,0.00519], HP [0.00472,0.99771], BP [~0,1]. Przesunięcia fazy w radianach: LP [-1.35482,.70885], HP [-.69158,1.3912], BP [-.088,-.10197].

Interpretacja: filtr zmienia widmo, fazę i reprezentację zdarzeniową MIN–MAX–Δt. Nie jest to dowód, że filtr tworzy nowe informacje: deterministyczny filtr nie może zwiększyć informacji o wejściu w sensie teorii informacji bez dodatkowych założeń. Zmiana liczby ekstremów zależy od progów detektora i transjentów. Filtrowanie przyczynowe różni się od zero-phase filtfilt. Filtr pasmowy nie jest rezonatorem z niezależnym wymuszeniem.