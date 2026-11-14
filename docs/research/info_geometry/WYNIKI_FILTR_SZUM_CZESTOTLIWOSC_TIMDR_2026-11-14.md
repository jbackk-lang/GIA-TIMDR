# TIMDR — rekonstrukcja po filtrze: częstotliwość × szum (2026-11-14)

**Eksperyment uruchomiony lokalnie**: `filter_noise_sweep.py`, seed 202611140817, N=1800 (1100 trening, 400 test), fs=200 Hz, 400 próbek. Suma fali 4 Hz i fali f∈{10,16,22,28,34} Hz, niezależne losowe amplitudy i fazy; Butterworth LP 8 Hz rząd 4, przyczynowy sosfilt; szum pomiarowy σ∈{.005,.02,.08}. Cel: dwie kwadratury amplitudowo-fazowe drugiej fali. Ridge(alpha=10)+StandardScaler; pełne wyjście (400), projekcje Fourier (4), osiem trójek MIN/MAX/Δt (24).

| f | σ | |H(f)| | R² pełne | R² Fourier | R² trójki |
|---:|---:|---:|---:|---:|---:|
|10|.005|.3751688|1.0000|.9999|.0366|
|10|.02|.3751688|1.0000|.9999|.0268|
|10|.08|.3751688|.9992|.9990|.0013|
|16|.005|.0585043|.9991|.9997|.0082|
|16|.02|.0585043|.9975|.9976|.0107|
|16|.08|.0585043|.9750|.9665|-.0094|
|22|.005|.0151583|.9888|.9974|-.0079|
|22|.02|.0151583|.9648|.9632|.0141|
|22|.08|.0151583|.7917|.6355|-.0290|
|28|.005|.0051944|.9576|.9711|-.0117|
|28|.02|.0051944|.8613|.7431|.0047|
|28|.08|.0051944|.5217|.2127|-.0315|
|34|.005|.0020821|.8904|.8840|.0064|
|34|.02|.0020821|.6883|.3074|-.0025|
|34|.08|.0020821|.3648|.0204|-.0195|

**Interpretacja**: tłumienie i szum pogarszają rekonstrukcję, a wybrane lokalne trójki nie zachowują użytecznej informacji o tłumionej składowej. To nie dowodzi całkowitej utraty informacji: dla niezerowej transmitancji odwracanie jest formalnie możliwe, lecz niestabilne przy szumie. Ograniczenia: znane częstotliwości w projekcjach Fouriera, nierówna liczba cech, jeden seed, brak przedziałów ufności, generator wyłącznie dwóch sinusoid, detektor trójek nieoptymalizowany.