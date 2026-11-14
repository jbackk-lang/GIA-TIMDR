# TIMDR — porównanie z dopasowaniem dwóch tłumionych fal (2026-11-14)

Skrypt uruchomiony lokalnie: `compare_damped_waves.py`; seed 202611140812. N=600 (400 trening, 50 niewykorzystanych, 150 test), fs=80 Hz, obserwowane 160 próbek. Generator: suma dwóch sinusoid tłumionych, f1~U(4,8), f2=f1+U(.4,1.5), amplitudy .65..1.2, fazy -π..π, tłumienie .03..20, szum wejścia i celu σ=.12. Horyzont 2,10,30 próbek po końcu obserwacji. Model klasyczny: nieliniowe least_squares, wiele startów na podstawie FFT z zerowym dopełnieniem, dopasowanie dwóch tłumionych sinusoid wyłącznie z przeszłego sygnału. Baselines: Ridge(alpha=100) ze standaryzacją, surowe 160 próbek lub 55 zespolonych prążków FFT z oknem Hanna. Wszyscy mają identyczny zbiór testowy.

| Horyzont | Surowy Ridge R² | FFT Ridge R² | Dwie tłumione fale R² |
|---:|---:|---:|---:|
| 2 | .8403 | -.0349 | **.8828** |
| 10 | .4258 | -.1150 | **.8401** |
| 30 | -.0320 | -.0466 | **.8326** |

Wniosek: model z poprawną klasą równań dynamicznych skutecznie ekstrapoluje fazę i tłumienie; poprzedni negatywny wynik nie dowodził nieprzewidywalności fal. **To porównanie nie testuje jeszcze nowej reprezentacji TIMDR** — nie uwzględnia automatycznych lokalnych trójek. Model jest zgodny z konstrukcją generatora, co daje mu przewagę indukcyjną; nie dowodzi, że dwa tłumione oscylatory pasują do rzeczywistych fal. FFT baseline jest regresją liniową na stałych prążkach, a nie optymalnym modelem widmowym. Test tylko jednego podziału i 150 przykładów, bez przedziałów ufności. Następny test: relacyjne trójki + estymowana faza kontra dopasowanie oscylatorów, oraz przypadki niezgodne z generatorem.