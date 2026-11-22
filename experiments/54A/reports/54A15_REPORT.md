# 54A.15 — Bezstratna kompresja strumieni czasowo-przestrzennych i szybkość

## Cel
Porównać stopień kompresji i przepustowość dużych strumieni zdarzeń przy wykorzystaniu odwracalnej transformacji różnicowej po polach rekordu.

## Protokół
262144 rekordów na zbiór, 11 bajtów na rekord (uint32 czas, int16 x/y/z, uint8 energia), 2883584 bajty na zbiór. Trzy deterministyczne syntetyczne zbiory: trajectory, regime, random. Metody: gzip level 1 i 6 całego strumienia; zlib level 1 w blokach 4096 rekordów; transformacja różnicowa pól + zlib level 1 w tych samych blokach. Transformacja resetuje stan na początku każdego bloku. Nagłówek strumienia i długości bloków wliczone w metody blokowe. Pełne sprawdzenie round-trip. Kompresja: mediana trzech pomiarów; dekompresja: jeden pomiar. Python, standardowa biblioteka.

## Wyniki
| Dane | gzip 1 (B) | gzip 6 (B) | zlib bloki (B) | delta+zlib (B) | gzip 1 (MiB/s) | delta+zlib (MiB/s) |
|---|---:|---:|---:|---:|---:|---:|
| trajectory | 1275331 | 1230070 | 1305186 | **62033** | 129.47 | 12.71 |
| regime | 1592501 | 1609001 | 1580425 | **28196** | 83.99 | 13.43 |
| random | 2356497 | 2395487 | 2359484 | **2175768** | 51.31 | 10.28 |

## Wnioski
Transformacja różnicowa rekordów daje znaczącą poprawę rozmiaru: ok. 95.1% mniejszy wynik od gzip 1 dla trajectory i 98.2% dla regime. Dla losowych rekordów poprawa to ok. 7.7%. To przewaga wykorzystania znanego schematu danych, **nie dowód przewagi TIMDR**. Pythonowa transformacja działa od ok. 4 do 10 razy wolniej od gzip 1. Nie wykazano szybszego kompresowania dużych plików.

## Ograniczenia
Brak rzeczywistych plików, brak LZ4/zstd, brak eksperymentów na 100 MiB–1 GiB, brak porównania z innymi transformacjami kolumnowymi i delta-only. Generator danych jest mocno regularny; nie generalizować wyniku na dowolne pliki. Pomiary czasu zależą od maszyny i obciążenia. Format prototypowy ma ograniczoną obsługę błędów.

## Następny test 54A.16
Porównać delta+zlib z columnar+zstd/LZ4 oraz natywną/wektorową transformacją, osobno mierząc czas transformacji, entropię, I/O i dekompresję. Dane rzeczywiste i skale 10–1000 MiB.

Reprodukcja: `python 54A15_STREAM_BENCH.py --records 262144 --repeats 3`.
