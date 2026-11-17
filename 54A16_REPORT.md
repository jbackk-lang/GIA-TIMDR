# 54A.16 — Szybkie kodowanie kolumnowe rekordów czasowo-przestrzennych

## Weryfikowalny eksperyment
Wykonano lokalnie `python 54A16_BENCH.py --records 65536 --repeats 3`. Trzy syntetyczne zbiory po 720896 bajtów (65536 rekordów po 11 B: uint32 czas, int16 x/y/z, uint8 energia). Porównano gzip poziomy 1/6, odwracalne przestawienie bajtów do kolumn + zlib 1/6, delta + zlib 1, delta + przestawienie + zlib 1/6. Pomiar czasu: mediana 3 powtórzeń; bez dysku i kosztów ładowania danych. W każdej próbie sprawdzono dokładny round-trip.

## Najważniejsze pomiary
| Zbiór | gzip 1: B / MiB/s | shuffle+zlib 1: B / MiB/s | delta+shuffle+zlib 6: B / MiB/s |
|---|---|---|---|
| trajectory | 318385 / 114.91 | **8234 / 549.60** | 3268 / 29.39 |
| regime | 388293 / 83.03 | **9822 / 576.83** | 1017 / 30.37 |
| random | 589108 / 50.87 | **459707 / 71.25** | 459790 / 18.64 |

## Wnioski
Odwracalne przegrupowanie bajtów z rekordów do kolumn pozwala uzyskać równocześnie mniejsze pliki i wyższą przepustowość w tych syntetycznych próbach. Względem gzip 1: trajektorie ok. 38.7x mniejszy plik i 4.8x szybsza kompresja; zmienne reżimy ok. 39.5x mniejszy i 6.9x szybsza; losowe ok. 1.28x mniejszy i 1.4x szybsza. Delta+shuffle+zlib 6 daje jeszcze mniejszy rozmiar na danych regularnych, lecz dużo wolniejszą kompresję i dekompresję. Przestawienie kolumnowe nie wymaga formalizmu TIMDR; wynik dowodzi korzyści transformacji danych o znanym schemacie, nie szczególnej przewagi teorii TIMDR.

## Ograniczenia
Test nie obejmuje narzutu opisu schematu/formatu pliku, operacji dyskowych, wielogigabajtowych danych, innych formatów, ani nowoczesnych kompresorów LZ4/zstd. Zbiory syntetyczne są regularne i mogą zawyżać korzyść. Czas jest specyficzny dla maszyny. Wartość zlib vs gzip jest porównywana wraz z różnymi małymi nagłówkami kontenerów.

## Następny etap
54A.17: blokowy, strumieniowy kodek kolumnowy z samowystarczalnym nagłówkiem, testy 64–512 MiB, pamięć szczytowa i rzeczywisty transfer na dysk; jeśli dostępne, porównanie z zstd i LZ4. Osobno test transformacji w kodzie natywnym.
