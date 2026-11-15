# Dwa odbiorniki — protokół rozróżniania przyczyn

**Data:** 2026-11-14. **Status:** eksperyment eksploracyjny, bez wyników i bez dowodu przyczynowego.

## Schemat
```text
                  +-- kanał wspólny H0 --+-- tor A / odbiornik RA --> yA
generator S ------+                      |
                  +----------------------+-- tor B / odbiornik RB --> yB
```
Rozróżniamy: zmianę S, zmianę H0, zmianę RA, zmianę RB, brak zmiany. Dwa odbiorniki nie rozdzielą w ogólności S od wspólnego H0; potrzebna jest dodatkowa referencja przed H0, kalibracja lub niezależny kanał.

## Wykonywalna demonstracja
`python docs/research/info_geometry/two_receivers.py`

Skrypt (bez zależności zewnętrznych) tworzy 8192 próbki ze wspólnego generatora AR(1), dzieli je na dwie połowy i symuluje pięć scenariuszy: NONE, SOURCE, COMMON_CHANNEL, RECEIVER_A, RECEIVER_B. Oba odbiorniki mają niezależny szum. Raportuje zmianę odchylenia standardowego i autokorelacji lag-1 między połowami. To **cechy kontrolne**, jeszcze nie geometryczne.

## Przewidywania do weryfikacji
- SOURCE: zmiana statystyk w obu odbiornikach.
- COMMON_CHANNEL: zmiana statystyk w obu odbiornikach — wzór podobny jakościowo do SOURCE, więc współwystępowanie nie dowodzi zmiany generatora.
- RECEIVER_A/B: zmiana silniejsza w jednej gałęzi; może sugerować zmianę lokalnego toru.
- NONE: tylko fluktuacje estymacji.

Wzory te nie są gwarantowane dla wszystkich realizacji, filtrów i szumów. Nie interpretować ich bez analizy niepewności.

## Kolejny właściwy test
1. Wiele niezależnych sesji, z randomizacją zmian i konfiguracji odbiorników.
2. Cechy geometryczne osobno dla `yA` i `yB`, plus cechy wspólne (korelacja, koherencja, opóźnienie).
3. Model klasyfikacji pięciu scenariuszy oraz klasa „nierozstrzygalne”; osobny test na niewidzianych parametrach toru.
4. Trzeci pomiar `s(t)` lub sygnału przed kanałem wspólnym, aby przetestować identyfikowalność przy dodatkowej informacji.
5. Porównać jakość decyzji: jeden odbiornik vs dwa odbiorniki vs referencja; raportować macierz pomyłek i błędy przypisania źródła.

## Uwaga o informacji
Wspólna zmiana obserwowana przez dwa odbiorniki jest świadectwem wspólnego wpływu, **nie** dowodem, że informacja „powstała” w generatorze. Pytanie o ontologiczną naturę informacji pozostaje otwarte.
