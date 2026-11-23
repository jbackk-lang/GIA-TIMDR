# RESULTS 007 — Pamięć po impulsie: kontrola negatywna

Data: 2026-11-19. Lokalnie wykonany eksperyment syntetyczny. Model dwóch harmonicznych (9 Hz i 18 Hz) przy fs=200 Hz; wcześniejszy stan wywołuje przesunięcie fazy 0.55 rad, wykładniczo zanikające od t=2 s ze stałą czasową 2 s. Pomiar dopiero od t=2.5 do 4.5 s, tj. po wywołaniu zmiany. 100 par o wspólnym szumie, amplitudzie i fazie bazowej; 20 podziałów GroupShuffleSplit, całe pary rozdzielone między treningiem i testem.

| Cechy | AUROC średnia | SD |
|---|---:|---:|
| RMS | 0.4989 | 0.0024 |
| Pełne amplitudy FFT | **1.0000** | 0.0000 |
| Sin/cos względnej fazy harmonicznych | **1.0000** | 0.0000 |

**Wynik:** ślad historii nie zmienia znacząco całkowitej energii, ale jest dostępny zarówno w fazie, jak i w amplitudach FFT. Modulacja fazowa zmienia rozkład energii w widmie, więc ten przypadek nie stanowi dowodu nowej cechy sygnału.

**Ograniczenia:** mechanizm pamięci jest wprost zaszyty w modelu; brak danych fizycznych, brak pełnych cech CHF, brak testów artefaktów i dowodu nowości. 1.0 AUROC oznacza łatwy problem syntetyczny, nie przewagę metody.

**Następny warunek testu:** dopasować nie tylko energię całkowitą, lecz także amplitudy widmowe, rozkład amplitud i znane miary fazy, a następnie badać opóźnienia i ślady zdarzeń w niezależnych sygnałach rzeczywistych. Wymagane porównanie CHF helix/trinode/bridges z bispektrum, STFT, matrix profile, IAAFT i detektorami zmian.
