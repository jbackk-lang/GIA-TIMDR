# 54A.19 — Adaptacyjny kodek blokowy: kompresja vs szybkość

## Test
Wykonano lokalnie `python 54A19_HYBRID.py --records 1048576` na czterech deterministycznych, **niepowtarzanych** syntetycznych plikach po 11 MiB. Rekord ma 11 bajtów: czas uint32, x/y/z int16, energia uint8. Blok: 32768 rekordów. Hybryda na podstawie pierwszych 4096 rekordów wybiera shuffle+zlib1, jeśli próbka po kompresji zajmuje mniej niż 20% wejścia, w przeciwnym razie LZ4. Selekcja jest zapisana w 9-bajtowym nagłówku bloku, więc dekoder odtwarza strumień bez dostępu do oryginału. Porównano gzip1, zstd1, LZ4, zawsze shuffle+zlib1 i hybrydę. Sprawdzono SHA-256 po dekompresji każdej kombinacji. Jeden przebieg z I/O, bez rozgrzewki.

## Wyniki (bajty / MiB/s kompresji)
| Dane | gzip1 | zstd1 | LZ4 | shuffle+zlib1 | hybryda |
|---|---|---|---|---|---|
| trajectory | 5101850 / 110.50 | 4310636 / 246.26 | 8472361 / 305.02 | **169251 / 501.62** | 169251 / 464.52 |
| regime | 6419785 / 77.55 | 3381225 / 305.37 | 10864152 / 492.32 | **217858 / 531.07** | 217858 / 485.67 |
| random | 9425928 / 48.29 | 10644885 / 343.60 | 11535051 / 581.25 | **7363871 / 70.15** | 11479131 / 306.70 |
| mixed | 7597412 / 59.02 | 8301078 / 272.14 | 10597992 / 846.30 | **3780218 / 127.84** | 5837902 / 407.03 |

## Wybory blokowe
- trajectory: 32/32 shuffle+zlib
- regime: 32/32 shuffle+zlib
- random: 32/32 LZ4
- mixed: 16 shuffle+zlib, 16 LZ4

## Interpretacja
Na mieszanych danych hybryda jest ok. 3.18x szybsza od stałego shuffle+zlib, ale produkuje ok. 54.4% większy plik. Na losowych rekordach ok. 4.37x szybsza kosztem ok. 55.9% większego pliku. Na uporządkowanych strumieniach selekcja dodaje narzut czasu i nie zmienia rozmiaru. To test heurystyki kompromisu, nie dowód wyższości TIMDR. Rekordy random nadal mają monotoniczny czas, nie są losowymi bajtami.

## Kolejny eksperyment
54A.20: zamiast stałego progu 20% użyć modelu kosztu `rozmiar + lambda * czas`, z próbkowaniem obu kandydatów i krzywą Pareto. Dodać korpus rzeczywistych danych z niezależnego źródła, wielokrotne przebiegi i pomiar RSS.

Reprodukcja: `python 54A19_HYBRID.py --records 1048576 --output 54A19_RESULTS.json`. Wymaga `pip install lz4` i narzędzia `zstd` w PATH.
