# RESULTS 010 — Podziały helisy: liczby pierwsze i zera dzeta

2026-11-19. Lokalny test syntetyczny: 100 par sygnałów, 10 podziałów grupowych, 17 segmentów. Sygnał 8/16 Hz z binarną informacją w fazie harmonicznej. Dla każdego segmentu mierzono średnią i odchylenie sygnału oraz krzywizny helisy Hilberta. Granice segmentów znormalizowano do tej samej liczby punktów. LogisticRegression + StandardScaler.

| Reprezentacja | AUROC średnia | SD |
|---|---:|---:|
| Równomierna | 0.47424 | 0.05520 |
| Liczby pierwsze | 0.47168 | 0.05618 |
| Nietrywialne zera dzeta | 0.48400 | 0.05079 |
| Losowa (9 realizacji) | 0.47040–0.52368 | różne |
| Amplituda FFT | 0.49504 | 0.01382 |
| Klasyczna faza harmoniczna | 1.00000 | 0.00000 |

**Wynik negatywny:** nie znaleziono przewagi podziałów opartych na liczbach pierwszych ani zerach dzeta. To nie obala ogólnej hipotezy o możliwej strukturze informacji na helisie. Nie wykazano fizycznego związku zer dzeta z sygnałem. W badaniu użyto prostych statystyk segmentów, nie pełnego CHF, i wyłącznie danych syntetycznych.

Następny test: podziały w numerach rzeczywistych zwojów, a nie arbitralnych indeksach próbek, z kontrolą klasycznych cech i niezależnymi nagraniami.
