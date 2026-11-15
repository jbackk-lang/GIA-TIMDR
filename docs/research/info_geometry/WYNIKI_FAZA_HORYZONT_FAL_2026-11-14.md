# TIMDR — faza i horyzont prognozy fal (2026-11-14)

Eksperyment wykonany lokalnie: `wave_phase_horizon_check.py`, seed 202611140810. N=2200; trening 1400, pominięte 300, test 500. Dwie tłumione sinusoidy z losowymi częstotliwościami (f1 4–8 Hz, f2=f1+0.4–1.5 Hz), fazami i amplitudami; szum wejścia σ=.12. 160 próbek przy fs=80 Hz, cele 2, 10, 30 próbek w przyszłości. Ridge StandardScaler(alpha=100), ekstrapolacja dwóch częstotliwości znalezionych FFT z oknem Hanna.

| Reprezentacja | h=2 R² | h=10 R² | h=30 R² |
|---|---:|---:|---:|
| 6 lokalnych trójek MIN/MAX/Δt | -.0177 | -.0334 | -.0281 |
| Trójki + kwadratury fazowe | .0987 | -.0238 | -.0465 |
| Same kwadratury fazowe | .1125 | .0007 | -.0217 |
| Zespolone FFT | .7424 | .3100 | -.0186 |
| Surowy sygnał | **.9274** | **.6089** | -.0133 |
| Dopasowanie dwóch harmonicznych | .3684 | .2558 | .0302 |

Wniosek: prognoza gwałtownie pogarsza się z horyzontem. Surowy sygnał jest silniejszy od lokalnych trójek i FFT dla krótkich horyzontów. Nie jest to dowód niemożności prognozy ani uniwersalnej niewystarczalności TIMDR. Ograniczenia: tylko jedna losowa realizacja podziału, brak CI; kwadratury na czterech stałych częstotliwościach, pierwsze 16 prążków FFT nie obejmuje optymalnie całego pasma, estymator harmoniczny nie modeluje tłumienia. Pełny skrypt i stdout dostępne jako pliki eksperymentu.