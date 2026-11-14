# TIMDR — prognoza dwóch interferujących fal, wynik negatywny (2026-11-14)

Eksperyment rzeczywiście uruchomiony lokalnie: `wave_phase_prediction.py`, seed 202611140809. 3600 syntetycznych sygnałów: 2400 trening, 400 niewykorzystanych, 800 test. Dwie tłumione sinusoidy o losowych częstotliwościach 5–9 Hz i odstępie .3–1.8 Hz, fazach, amplitudach i tłumieniu. fs=100 Hz, 160 obserwowanych próbek, prognoza próbki 25 kroków później. Szum wejścia .16, celu .12. Wspólny StandardScaler+Ridge(alpha=100).

| Reprezentacja | R² test |
|---|---:|
| 6 lokalnych trójek MIN/MAX/Δt | -.00248 |
| trójki + 4 cechy Hilberta | -.00373 |
| 4 cechy Hilberta | -.00154 |
| zespolone FFT 8 wybranych prążków | -.00633 |
| surowy przebieg 160 próbek | .08418 |
| surowy + Hilbert | .08428 |
| trójki + przemieszany Hilbert | -.00152 |

Komplet sześciu lokalnych maksimów wykryto w 100% przebiegów według kryterium algorytmu, lecz to nie dowodzi prawidłowej identyfikacji fizycznych zdarzeń. SD celu .64564.

**Interpretacja:** Żadna badana reprezentacja z regresją liniową nie osiągnęła dobrej prognozy. Nie jest to dowód, że faza nie niesie informacji. Kąt fazowy ma topologię kołową i powinien być kodowany sin/cos; wybrane prążki FFT mają różne indeksy między przykładami, których nie podano modelowi. Należy porównać z estymacją parametrów dwóch sinusoid, modelem dynamicznym i wieloma horyzontami. Nie twierdzić, że reprezentacja TIMDR jest uniwersalnie wystarczająca.