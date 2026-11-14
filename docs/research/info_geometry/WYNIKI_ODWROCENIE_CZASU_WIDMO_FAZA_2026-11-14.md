# Kierunek czasu: odwrócenie sygnału, widmo mocy, faza, STFT i trójka MIN–MAX–CZAS

Data: 2026-11-14. Kod: `time_reversal_phase_test.py`.

## Hipoteza falsyfikowalna
Dla rzeczywistego dyskretnego sygnału x oraz jego odwrócenia x[::-1] widmo mocy |FFT|² i autokorelacja są identyczne, ale faza widma i podpisany odstęp między ekstremami mogą rozróżnić kierunek. Jest to własność matematyczna, nie tylko empiryczna korelacja.

## Metoda
128 próbek, dwa impulsy Gaussa o przeciwnych znakach, losowe amplitudy, szerokość, położenie i odstęp; szum N(0,0.1). Klasa 0 = kolejność ujemny→dodatni, klasa 1 = dokładne odwrócenie całego sygnału, włącznie z szumem. Trening 2400, test 1200, różne ziarna. Modele: StandardScaler + LogisticRegression(C=1). Reprezentacje: log-widmo mocy FFT, 32 opóźnienia autokorelacji, zespolone FFT (real/imag), trójka (min,max,podpisane Δt/128), trójka bez znaku, STFT-moc w oknach 32, krok 16, zachowana kolejność okien, pełny sygnał.

## Faktyczne wyniki uruchomienia
```
power 0.4925
autocorr 0.48
complex_fft 1.0
ordered_extrema 1.0
unordered_extrema 0.5167
stft_time 1.0
raw 0.9992
exact_power_reversal_error 5.684341886080802e-14
exact_autocorr_reversal_error 3.3306690738754696e-16
paired_power_max_abs 3.1086244689504383e-15
paired_autocorr_max_abs 8.881784197001252e-16
```

## Interpretacja
Widmo mocy i autokorelacja nie zawierają informacji o kierunku czasu w tej konstrukcji: pary odwrócone są identyczne pod względem obu reprezentacji, co potwierdzają różnice rzędu błędu zmiennoprzecinkowego. Trójka MIN–MAX–podpisane Δt rozróżnia kierunek perfekcyjnie, ponieważ generowane impulsy mają konsekwentną kolejność. Zespolone FFT i STFT z zachowaniem kolejności okien także zachowują informację o kierunku. STFT-moc nie zawiera globalnej fazy FFT, lecz zachowuje **położenie energii w czasie**. Surowy przebieg zawiera wystarczającą informację, a 99.92% jest wynikiem konkretnego liniowego klasyfikatora.

## Ograniczenia
Syntetyczny generator świadomie koduje etykietę przez odwrócenie czasu; nie jest to predykcja przyszłości ani empiryczny dowód fizycznej strzałki czasu. Nie ma przypadków, gdzie ekstrema globalne mają identyczny porządek, a rozstrzygają dopiero relacje wyższego rzędu. Trójka jest wystarczająca **tylko dla tej rodziny sygnałów**. Nie porównano modeli przy wyrównanej liczbie cech; to test identyfikowalności, nie ogólny ranking jakości metod.

## Następny krok
Wygenerować sygnały o jednakowym globalnym MIN–MAX–podpisanym Δt i identycznym widmie mocy, ale różnych relacjach lokalnych. Testować fazę, STFT i uporządkowane lokalne zdarzenia, rozdzielając tożsamość widmową od identyfikowalności procesu.
