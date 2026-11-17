# 54A.18 — Benchmark plikowy 110 MiB vs gzip, zstd i LZ4

Wykonano lokalnie `python 54A18_BENCH.py` dla trzech zbiorów syntetycznych po 115343360 bajtów. Każdy plik powstał przez dziesięciokrotne powtórzenie 11 MiB deterministycznego strumienia rekordów. Zapis i odczyt plików, pojedynczy przebieg bez rozgrzewki. gzip level 1, zstd CLI -1 -T1, lz4.frame level 0, GIA17: shuffle pól rekordu + zlib 1 w blokach 65536 rekordów. Po każdej dekompresji sprawdzono SHA-256 oryginału i odtworzonego pliku.

| Dane | gzip 1 B / MiB/s | zstd 1 B / MiB/s | LZ4 B / MiB/s | GIA17 B / MiB/s |
|---|---|---|---|---|
| trajectory | 51009350 / 123.95 | 38333588 / 290.35 | 84718495 / 456.37 | **1318740 / 567.23** |
| regime | 64178441 / 84.03 | 16514545 / 399.50 | 108640331 / **818.92** | **1624900 / 550.35** |
| random | 94260544 / 47.48 | 106439869 / 338.81 | 115350411 / **1955.83** | **73551020 / 69.05** |

GIA17 jest jednocześnie najszybszy i najmniejszy tylko na trajektoriach. Na regime najskuteczniejszy rozmiarowo, ale LZ4 szybszy. Na random najskuteczniejszy rozmiarowo, ale dużo wolniejszy niż zstd/LZ4. Wniosek dotyczy transformacji kolumnowej danych o znanym schemacie, nie dowodzi przewagi formalnej dynamiki TIMDR.

Ograniczenia: powtórzone syntetyczne dane, brak realnego korpusu, tylko jeden przebieg i brak kontroli cache. Konieczne niezależne dane i wiele powtórzeń z raportem rozrzutu oraz pomiarem RSS. Dane random mają monotoniczne pole czasu, nie są losowymi bajtami.

Kod: `54A18_BENCH.py`; zależności: `54A17_STREAM.py`, zstd CLI, lz4.frame.
