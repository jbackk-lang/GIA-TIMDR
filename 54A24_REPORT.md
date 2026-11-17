# 54A.24 — Kompozycja geometryczna trzech węzłów

## Hipoteza
Jeżeli trzy węzły współdzielą ruch lub strukturę, kodowanie jednego węzła odniesienia oraz dwóch relacji względem niego może być mniejsze niż niezależne kodowanie wszystkich trzech.

## Metoda i wykonanie
Uruchomiono lokalnie skrypt odpowiadający `54A24_COMPOSITION.py` dla 8192 chwil i trzech 16-bitowych wartości na chwilę (49152 B danych źródłowych). Cztery deterministyczne zbiory syntetyczne: shared, independent, switching, random. Baseline: temporalna pierwsza różnica każdego węzła. Hierarchia: pierwsza różnica węzła 0 oraz pierwsze różnice relacji (węzeł1−węzeł0) i (węzeł2−węzeł0), modulo 65536. Wszystkie warianty zlib poziom 6; dekoder odtwarza dokładnie wszystkie 3 serie.

## Wyniki
| Zbiór | raw+zlib B | niezależnie+zlib B | hierarchicznie+zlib B | zmiana względem niezależnych |
|---|---:|---:|---:|---:|
| shared | 3764 | 133 | **113** | −15.04% |
| independent | 31741 | **136** | 137 | +0.74% |
| switching | 19673 | 703 | **641** | −8.82% |
| random | **48185** | 48960 | 49100 | +0.29% |

## Interpretacja
Kodowanie relacji ma mierzalną korzyść przy wspólnej strukturze, lecz nie na każdym zbiorze. Maksymalny zysk absolutny to 62 bajty (switching); dla shared 20 bajtów. Niezależne przebiegi są silnie deterministyczne i łatwe do kompresji, więc nie są reprezentatywne dla niezależnego ruchu z szumem.

## Granice
Topologia gwiazdy jest znana z góry, nie jest przesyłana, a dane nie obejmują energii, czasów ani grafu krawędzi z pełnego modelu TRM/TIMDR. Brak kosztu dynamicznego wyboru węzła odniesienia i informacji o strukturze. Złożenie relacji przestrzennych nie jest automatycznie formalną kompozycją gałęzi M/S, G, K TIMDR. Brak pomiarów czasu i rzeczywistych danych.

## Następny test
Porównać stałą gwiazdę, łańcuch i wybór rodzica dla każdego bloku, uwzględnić pełny koszt indeksów rodziców i zmian topologii, a także dane przestrzenne z szumem i ruchami wspólnymi. Sprawdzić, czy geometria rzeczywiście pozwala przewidzieć optymalną strukturę grafu bez podglądu przyszłych bloków.
