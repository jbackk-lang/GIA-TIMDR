# TIMDR — odtwarzanie informacji z sygnału po filtrze (2026-11-14)

Wykonano lokalnie skrypt `filter_inverse_timdr.py`, seed 202611140816, N=2200 (trening 1400, test 500). fs=200 Hz, 400 próbek, wejście sinus 4 Hz o amplitudzie .6–1.4 + sinus 28 Hz o amplitudzie .25–.95, losowe fazy, szum wejścia .07. Wyjście: przyczynowy filtr Butterwortha 4. rzędu LP 8 Hz + szum pomiarowy .025. Regresja StandardScaler+Ridge(alpha=10) odtwarza cztery kwadratury Fouriera wejścia.

| Reprezentacja | R² 4 Hz | R² 28 Hz |
|---|---:|---:|
| 8 lokalnych trójek wyjściowych (24 cechy) | .65834 | -.02644 |
| Pełne wyjście (400 próbek) | .99999 | .72191 |
| 4 kwadratury Fouriera wyjścia | .99989 | .62463 |

Detektor znalazł 7–8 maksimów, mediana 8. |H(4Hz)|=.99811323; |H(28Hz)|=.00519440. Odwracanie tłumienia 28 Hz wzmacnia szum ~192.5 razy. Wyniki nie dowodzą pełnej odwracalności ani uniwersalnej wystarczalności trójek. Wiedza o częstotliwościach jest wbudowana w cele i projekcje, a modele mają różną liczbę cech. Pliki wykonywalne i stdout znajdują się w załącznikach rozmowy.