# Eksperyment wielogałęziowy: dwa odbiorniki i ablacja mostów

**2026-11-14. Status: kod zapisany, nieuruchomiony.** Eksploracja, nie prerejestracja testu potwierdzającego.

## Cel
Sprawdzić, czy łączenie opisów M/S, pomocniczego opisu modalnego i pomocniczego opisu geometrycznego ułatwia rozróżnianie pięciu scenariuszy: NONE, SOURCE, COMMON_CHANNEL, RECEIVER_A, RECEIVER_B.

## Kod
`python docs/research/info_geometry/multibranch_receiver_test.py`

Skrypt używa tylko biblioteki standardowej Python. Dla każdego scenariusza generuje wspólne źródło i dwa odbiorniki z niezależnym szumem; trenuje klasyfikator najbliższego centroidu na ziarnach 1000–1099, testuje na 9000–9049. Zwraca accuracy, macro-F1 i macierz pomyłek wariantu ALL.

## Rzeczywisty status gałęzi
- **MS:** odchylenie standardowe i autokorelacja lag-1 — *proxy cech sygnałowych*, nie pełny operator TIMDR M/S.
- **K_PROXY:** względna energia różnic — *proxy modalności*, nie formalny rezonans K.
- **G_PROXY:** mediana kąta zwrotu krzywej opóźnieniowej 2D — *proxy geometrii*, nie operator powierzchniowy G.
- **ALL:** konkatenacja cech, nie zatwierdzony most formalny. Zysk ALL ponad MS jest jedynie kandydatem na wartość połączenia gałęzi.

Nie nazywać wyników „walidacją mostów TIMDR” bez implementacji rzeczywistych operatorów i kontroli zgodności ze specyfikacją.

## Porównania
MS; MS+K_PROXY; MS+G_PROXY; ALL. Ważne: ALL ma więcej cech niż MS, więc ewentualna poprawa wymaga dodatkowego porównania z modelem MS o podobnej pojemności oraz z cechami losowymi.

## Ograniczenia
- Parametry źródła i torów są z góry znane konstruktorowi symulacji; w rzeczywistym odbiorze zwykle nie są.
- SOURCE i COMMON_CHANNEL mogą być nieidentyfikowalne w innych konfiguracjach; wysoka skuteczność na tych sztucznych przypadkach nie dowodzi identyfikowalności ogólnej.
- Brak kalibracji prawdopodobieństw, klasy UNKNOWN i wielosesyjnego przedziału ufności; to zadania następnej wersji.
- Wykorzystanie wielu ziaren testowych jest kontrolą odtwarzalności, nie substytutem niezależnych danych fizycznych.
- Nie testujemy fundamentalnej natury informacji ani nie wykrywamy jej „cząstki”.

## Warunki interpretacji
Wyniki z tego kodu mogą wyłącznie pokazać zachowanie prostego modelu na sztucznych danych. Wnioski o TIMDR wymagają implementacji rzeczywistych operatorów M/S, G, K, mostów oraz osobnej walidacji. Zachować macierz pomyłek, szczególnie SOURCE vs COMMON_CHANNEL.

## Następne kroki
1. Testy jednostkowe generowania i niezależności szumu.
2. Próg abstencji UNKNOWN wybrany bez dostępu do testu.
3. Niewidziane filtry, dryft zegara, różne parametry odbiorników.
4. Trzeci kanał referencyjny przed wspólnym kanałem.
5. Właściwe operatory TIMDR zgodne z dokumentami aksjomatycznymi.
