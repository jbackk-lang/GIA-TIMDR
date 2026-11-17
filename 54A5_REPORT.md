# 54A.5 — Porównanie predykcji statycznej, adaptacyjnej i fazowej

## Metoda
- Cztery syntetyczne strumienie, po 131072 bajty; deterministyczne generatory.
- Predyktory przyczynowe: poprzedni bajt, bajt sprzed trzech pozycji, bajt sprzed 256 pozycji.
- Statyczny wybiera opóźnienie 256; adaptacyjny wybiera predyktor o najniższym całkowitoliczbowym wygładzanym błędzie; fazowy rozstrzyga remisy na podstawie indeksu modulo 3.
- Różnice modulo 256, jeden gzip.compress(..., compresslevel=9, mtime=0) na cały strumień. Każdy wynik zweryfikowano dekoderem.
- Brak nagłówków identyfikujących kodek, zatem wyniki są porównaniem potencjału transformacji, a nie gotowych formatów plików.

## Wyniki (bajty)
| Dane | gzip | Statyczna | Adaptacyjna | Fazowa |
|---|---:|---:|---:|---:|
| Losowe | 131130 | 131130 | 131130 | 131130 |
| Powtarzalne | 822 | 440 | 174 | 178 |
| Powolne zmiany | 1018 | 547 | 273 | 273 |
| Trzy skorelowane kanały | 53932 | 33539 | 25089 | 25088 |

## Interpretacja
Adaptacja daje korzyści na tych syntetycznych zbiorach. Reguła fazowa nie daje znaczącej dodatkowej korzyści. **To nie jest implementacja oryginalnej macierzy J(Lambda) ani pełnej dynamiki TIMDR.** Nie można z tego wnioskować o skuteczności TIMDR.

## Kolejny krok
Zidentyfikować źródłowe równania aktualizacji stanu, sprzężenia i parametru Lambda. Zaimplementować predyktor dynamiczny, w którym dekoder wylicza identyczny stan bez bocznej informacji, a następnie testować na rzeczywistych plikach z uwzględnieniem nagłówków i kosztów modelu.
