# 54A.26 — Wspólny ruch w hierarchii trójwęzłów

## Cel
Sprawdzić, czy nadrzędny model wspólnego ruchu pozwala zapisać mniej informacji niż niezależne różnicowanie współrzędnych węzłów.

## Wykonanie
16 konfiguracji, cztery deterministyczne strumienie syntetyczne po 16384 chwilach × trzy 16-bitowe współrzędne (98304 B), 512 chwil na blok. Porównano:
- temporal: niezależne różnice czasowe wszystkich trzech węzłów;
- star: czasowa różnica węzła 0 i przestrzenne różnice węzłów 1/2 względem węzła 0;
- common: różnica czasowa węzła 0 i reszty węzłów 1/2 względem poprzedniego, **już odtworzonego** ruchu węzła 0;
- adaptive: kompresja wszystkich trzech wariantów na każdym bloku i wybór najmniejszego wyniku.

Wszystkie kodowane reszty są 16-bitowe modulo 65536. Kodek zlib level 1, nagłówek strumienia 8 B i każdego bloku 7 B. Dekoder nie korzysta z danych przyszłych; każdy wariant przeszedł exact roundtrip.

## Wyniki w bajtach
| Dane | temporal | star | common | adaptive |
|---|---:|---:|---:|---:|
| shared | **31383** | 33320 | 34716 | **31383** |
| split | **41905** | 54457 | 46780 | **41905** |
| independent | **48588** | 66174 | 53649 | **48588** |
| random | 98888 | 98888 | 98888 | 98888 |

Wszystkie bloki adaptive wybrały temporal (32/32 dla każdego zbioru). Czas kodowania adaptive ok. 0.034–0.039 s, temporal ok. 0.012 s (jednorazowe pomiary, Python, nie należy traktować ich jako stabilnych pomiarów wydajności).

## Wniosek
W badanych danych wspólny ruch nie przekłada się na mniejszy koszt reprezentacji po uwzględnieniu zlib. Wynik negatywny dla tej implementacji; nie obala kompozycji geometrycznej TIMDR. Model 'common' używa poprzedniej prędkości węzła 0, nie formalnego stanu META TIMDR.

## Dalszy kierunek
Sprawdzić predykcję wspólnego ruchu na szumie skorelowanym, trajektoriach rzeczywistych i przy różnym koszcie modelu, z porównaniem do mocnego kodeka kolumnowego. Ustalić, czy reprezentacja hierarchiczna może uniknąć powtórzeń, których zwykły zlib nie usuwa.

Kod wykonany lokalnie: `54A26_SHARED_MOTION.py`; pełny wynik: `54A26_RESULTS.json`. Pliki lokalne są dołączone do rozmowy.
