# RESULTS 009 — Helisa i odczyt informacji

2026-11-19. Lokalny eksperyment syntetyczny: 100 par, 8 i 16 Hz, fs=256 Hz, N=512. Bit zakodowany w fazie względnej; w parze amplitudy FFT identyczne (maks. różnica 5.68e-14). 12 podziałów grupowych, StandardScaler + LogisticRegression.

| Cechy | AUROC średnia | SD |
|---|---:|---:|
| Amplitudy FFT | 0.4580 | 0.0396 |
| Znana relacja faz harmonicznych | 1.0000 | ~0 |
| Kwantyle krzywizny i skręcenia helisy Hilberta | 0.4571 | 0.0329 |
| Mediany geometrii helisy w ośmiu odcinkach czasu | 0.4784 | 0.0557 |

**Wniosek:** testowana prosta geometria helisy nie odzyskała narzuconego kodu, który klasyczna faza odzyskała. Wynik ~0.5 to brak rozróżniania; nie jest dowodem, że helisa nigdy nie niesie informacji. Konstrukcja helisy (Re Hilbert, Im Hilbert, czas) nie dowodzi fizycznej pierwotności tej geometrii. Brak testu pełnego CHF, realnych nagrań i naturalnej pamięci układu.

Dalsze dwa tory: (A) naturalne ślady po impulsie i czas zaniku informacji, kontrola FFT/STFT/fazy; (B) relacje między zwojami, rekonstrukcja trajektorii stanów, odporność na zmianę współrzędnych, kontrola surogatów IAAFT. Nie ogłaszać odkrycia przed walidacją.
