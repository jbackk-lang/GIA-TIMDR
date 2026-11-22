# 54A.11 — Dynamiczne przełączanie predyktorów

Pięć deterministycznych strumieni syntetycznych po 32768 bajtów. Kandydaci: opóźnienia 1, 3, 64. Adaptacyjny model wybiera minimum wykładniczo wygładzanego błędu; model przełączający minimum sumy błędów z ostatnich 16 pozycji z karą 8 za zmianę predyktora. Wszystkie decyzje przyczynowe i odtwarzalne przez dekoder. Reszty modulo 256; gzip poziom 9 na całym strumieniu; weryfikacja dokładnego odtworzenia. Wyniki nie zawierają narzutu nagłówka.

| Dane | gzip | statyczna | adaptacyjna | przełączająca | przełączenia adapt. | przełączenia nowa |
|---|---:|---:|---:|---:|---:|---:|
| random | 32796 | 32796 | 32796 | 32796 | 5583 | 4809 |
| periodic | 376 | 249 | 172 | 172 | 1 | 1 |
| regime_512 | 1356 | 1976 | 318 | 318 | 0 | 0 |
| regime_128 | 1135 | 3098 | 809 | 809 | 0 | 0 |
| mixed | 1696 | 299 | 265 | 265 | 1 | 1 |

Brak poprawy kompresji. Brak przełączeń w strumieniach regime_512 i regime_128 oznacza, że nie przetestowano skutecznie hipotezy szybszego wykrywania granic reżimów. Wynik dotyczy predyktora heurystycznego, nie pełnej dynamiki TIMDR.

Następny krok: strumienie z naprzemiennie optymalnymi opóźnieniami, pomiar opóźnienia wykrywania zmiany, rzeczywiste dane, pełny koszt formatu.

Reprodukcja: `python 54A11_SWITCH.py`.