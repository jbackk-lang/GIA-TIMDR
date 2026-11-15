# Wyniki pilota porównawczego: jeden i dwa odbiorniki

**Data:** 2026-11-14. **Status:** wykonany eksperyment syntetyczny, eksploracyjny; nie jest testem potwierdzającym formalnych mostów TIMDR.

## Procedura
Odtworzono generator, scenariusze, cechy i klasyfikator z `multibranch_receiver_test.py` oraz warianty pojedynczych odbiorników z `compare_receivers.py`. Uruchomienie lokalne Python (biblioteka standardowa). Trening: 100 ziaren 1000–1099 × 5 klas. Test: 50 ziaren 9000–9049 × 5 klas = 250 przypadków na wariant. Jedna instancja testowa na klasę i ziarno. Klasy: NONE, SOURCE, COMMON_CHANNEL, RECEIVER_A, RECEIVER_B.

**Uwaga reprodukcyjna:** obliczenia przeprowadzono lokalnie przez samodzielny skrypt odtwarzający logikę obu plików; nie uruchomiono bezpośrednio plików pobranych z GitHub. Dla pełnego potwierdzenia należy uruchomić repozytoryjne skrypty i porównać wyjście. Kod źródłowy repozytorium nie został zmodyfikowany w celu uzyskania wyników.

## Wyniki

| Odbiornik | Cechy | Accuracy | Macro-F1 | SOURCE→COMMON_CHANNEL | COMMON_CHANNEL→SOURCE |
|---|---|---:|---:|---:|---:|
| A | MS | 0.7760 | 0.7093 | 2 | 4 |
| A | ALL | 0.8000 | 0.7333 | 0 | 0 |
| B | MS | 0.7760 | 0.7093 | 2 | 4 |
| B | ALL | 0.8000 | 0.7333 | 0 | 0 |
| AB | MS | 0.9760 | 0.9760 | 2 | 4 |
| AB | ALL | 1.0000 | 1.0000 | 0 | 0 |

`ALL` = M/S (std i autokorelacja) + K_PROXY (energia różnic) + G_PROXY (kąt zwrotu krzywej opóźnieniowej). Te cechy **nie są formalnymi operatorami K/G ani zatwierdzonymi mostami TIMDR**.

## Interpretacja

- W tej konkretnej symulacji dwa odbiorniki umożliwiają znacznie lepsze rozróżnienie pięciu etykiet niż pojedynczy odbiornik. Jest to zgodne z intuicją: zdarzenie RECEIVER_A/B pozostawia inny ślad w obu torach.
- ALL poprawia wynik względem MS w tej konfiguracji, ale może to być skutek dodatkowych cech lub szczególnych parametrów symulacji, nie dowód na wartość mostów TIMDR.
- Perfect accuracy = 1.0000 dotyczy **wyłącznie tych 250 syntetycznych przypadków** i nie oznacza ogólnej identyfikowalności generatora i kanału.
- Pojedynczy odbiornik A i B mają takie same metryki z powodu symetrycznej konstrukcji scenariuszy i torów.
- Nie obliczono przedziałów ufności, kalibracji klasy UNKNOWN ani testów poza rozkładem. Nie ma podstaw do wniosków o ontologicznej kategorii informacji.

## Weryfikacja następnego kroku

1. Uruchomić bezpośrednio `compare_receivers.py` oraz `multibranch_receiver_test.py` i porównać wyjścia.
2. Przeprowadzić test na niewidzianych filtrach, nieliniowościach, szumie i dryfcie zegara.
3. Dodać przypadki konstrukcyjnie nieidentyfikowalne, np. SOURCE i COMMON_CHANNEL produkujące tę samą obserwację.
4. Dodać UNKNOWN/abstencję, kalibrację i bootstrap po ziarnach.
5. Zastąpić proxy operatorami TIMDR zgodnymi z aksjomatami, z jawnie testowanymi mostami.
