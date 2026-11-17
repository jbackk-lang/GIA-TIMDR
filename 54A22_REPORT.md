# 54A.22 — Adaptacja modelu predykcji a geometria

## Test wykonany
Uruchomiono `python /mnt/data/54A22.py` na 4 syntetycznych strumieniach (linear, curve, noise, mixed), każdy 65536 rekordów po 11 B. Rozmiar bloku 512 rekordów. Porównano pięć metod: raw (bez predykcji), fixed1 (pierwsza różnica współrzędnych), fixed2 (druga różnica), causal (wybór najlepszego modelu na podstawie kosztu **poprzedniego zakończonego bloku**) oraz geometry (wybór na podstawie zgodności kierunków wektorów w poprzednim bloku). Reszty są kodowane odwracalnie modulo 2^16, następnie byte shuffle + zlib1. Model bloku jest zapisany w nagłówku (1 B + 4 B rozmiaru), więc dekoder nie wymaga przewidywania decyzji. Każdy wariant przeszedł pełny roundtrip.

## Wyniki — bajty
| Zbiór | raw | fixed1 | fixed2 | causal | geometry |
|---|---:|---:|---:|---:|---:|
| linear | 68699 | **50341** | 50695 | 50347 | 50696 |
| curve | 113200 | 56934 | **54330** | 54360 | 54360 |
| noise | **501101** | 502141 | 502211 | 502129 | 502141 |
| mixed | 190149 | 165029 | 164817 | **164705** | 164759 |

Na mixed adaptacja causal jest o 112 B (0.068%) lepsza od najlepszego modelu stałego. Na pozostałych zbiorach nie wygrywa. Geometry nie poprawia causal w żadnym zbiorze.

## Szybkość (MiB/s)
| Zbiór | fixed1 | fixed2 | causal | geometry |
|---|---:|---:|---:|---:|
| linear | 16.51 | 14.43 | 5.49 | 6.57 |
| curve | 16.36 | 13.80 | 4.88 | 6.50 |
| noise | 13.43 | 11.28 | 4.11 | 6.00 |
| mixed | 11.83 | 13.18 | 4.95 | 6.58 |

Koszt adaptacji w Pythonie jest wysoki. Jednorazowe pomiary czasu nie są stabilnym benchmarkiem. Dane są syntetyczne, bez rzeczywistych źródeł. Wariant geometry to **heurystyka zgodności kierunków**, nie formalny stan TIMDR (Lambda, tau, rho, J). Model causal jest wybierany po poprzednim bloku, bez przyszłego przecieku.

## Wniosek
Zysk adaptacji na mixed jest realny, ale znikomy. Sama geometria nie wykazuje dodatkowej przewagi. Mocniejszy test: zmiany modelu na granicach bloków, jawny koszt bitów reszt oraz silne baselines (columnar + zstd); przede wszystkim prawdziwe dane przestrzenne.

Kod źródłowy `54A22.py` i pełny plik `54A22_RESULTS.json` są dostępne jako pliki rozmowy. Wyniki w repo są przepisane bezpośrednio z wykonanego testu.
