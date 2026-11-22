# 54A.17 — Plikowy kodek strumieniowy

Wykonany lokalnie benchmark: `python 54A17_STREAM.py --records 1048576 --output 54A17_RESULTS.json`. Każdy z trzech deterministycznych syntetycznych plików ma 11534336 bajtów (1048576 rekordów po 11 bajtów). Format GIA17: 20-bajtowy nagłówek (magia, rekordy/blok, długość oryginału), dla każdego bloku 8-bajtowy nagłówek (rozmiar przed i po kompresji) oraz dane zlib level 1 po odwracalnym przestawieniu bajtów do kolumn. Bloki po 65536 rekordów. Dekoder samodzielnie odtwarza strumień; SHA-256 oryginału i dekodowanego pliku są zgodne. Porównanie z gzip level 1 z plikowym I/O.

| Dane | gzip 1 B | GIA17 B | gzip MiB/s | GIA17 MiB/s | GIA17 dekodowanie MiB/s | tracemalloc peak B |
|---|---:|---:|---:|---:|---:|---:|
| trajectory | 5101232 | 131892 | 99.52 | 523.68 | 269.80 | 2181578 |
| regime | 6419392 | 162508 | 82.63 | 515.47 | 728.80 | 2183775 |
| random | 9426025 | 7355120 | 46.92 | 65.05 | 446.94 | 3779458 |

**Wniosek:** Na trzech syntetycznych danych o znanym schemacie kodek strumieniowy uzyskał mniejszy rozmiar i szybszą kompresję od gzip 1, od ok. 1.4x do 6.2x. Nie jest to dowód szczególnej przewagi TIMDR: głównym czynnikiem jest transpozycja bajtów rekordu, standardowa technika byte shuffle. Brak danych rzeczywistych, testów 100 MiB–1 GiB, pomiaru RSS i powtórzeń benchmarku. Prędkość zależy od dysku, cache i środowiska. Dane losowe dotyczą rekordów z losowymi współrzędnymi, ale monotonicznym czasem, nie kryptograficznie losowych bajtów. Kodek nie jest utwardzony do przetwarzania niezaufanych plików.

**Reprodukcja:** kod `54A17_STREAM.py` jako lokalny artefakt; wyniki w `54A17_RESULTS.json`. Następny krok: porównanie z zstd/LZ4 i test na rzeczywistych plikach oraz 100 MiB+.
