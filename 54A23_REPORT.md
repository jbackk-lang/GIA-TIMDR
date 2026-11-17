# 54A.23 — Czy trójwęzeł może się składać?

## Rozróżnienie matematyczne
Składanie funkcji/transformacji jest dobrze określone, gdy przeciwdziedzina pierwszej pasuje do dziedziny drugiej. Dla afinicznych map f(x)=ax+b ich złożenie jest łączne: (f∘g)∘h=f∘(g∘h). Natomiast kaskada operatorów różnicowych D^3 x_n=x_n−3x_(n−1)+3x_(n−2)−x_(n−3) jest **inną** konstrukcją: składaniem operatorów liniowych działających na sekwencjach. Nie należy utożsamiać jej ze składaniem trzech gałęzi TIMDR.

W formalnym chronoprocesie TIMDR trzy rzuty M/S, G i K są odrębne i mają wspólny indeks czasu, lecz nie są automatycznie kompozycyjnymi mapami tego samego typu. Składanie obiektów TIMDR wymagałoby określenia przestrzeni stanów, interfejsu, operatora i zachowywanych niezmienników, a także testu nieredukowalności gałęzi.

## Uruchomiony test
Wykonano lokalny benchmark `python /tmp/t23.py` dla 65536 16-bitowych próbek w czterech syntetycznych seriach. Porównano raw, D, D², D³ z zlib level 1. Kod reprodukcyjny zapisano jako `54A23_COMPOSITION.py` (ten skrypt zawiera dodatkowe testy odwracalności i łączności map afinicznych).

| Dane | raw B | D B | D² B | D³ B |
|---|---:|---:|---:|---:|
| linear | 37626 | 732 | **730** | 732 |
| quadratic | 2965 | **2518** | 4281 | 6461 |
| piecewise | 39039 | 1099 | **1023** | 1063 |
| random | 131118 | 131118 | 131118 | 131118 |

Wniosek: wyższy rząd nie daje ogólnej przewagi; na tych danych D³ nie jest najlepszy. Różnicowanie modulo 65536 jest odwracalne. W testach algebraicznych łączność składania afinicznego jest osobną własnością, nie dowodem przewagi kompresyjnej.

## Ważna korekta interpretacyjna
W skrypcie `54A23_COMPOSITION.py` komentarz o trzech węzłach ma status analogii. Kaskada różnicowa nie reprezentuje pełnej kompozycji chronoprocesów. Formalny TIMDR wymaga rozdzielenia gałęzi M/S, G, K. Żadnej z nich nie wolno zredukować do samego D³.

## Proponowany następny krok
Zdefiniować kompozycję dwóch trójwęzłów jako grafów zdarzeń z jawnymi interfejsami, wspólnymi znacznikami czasu i mapami zachowującymi energię oraz geometrię. Sprawdzić łączność, idempotencję (jeśli oczekiwana), zachowanie informacji i koszt kodowania granic między węzłami. Dopiero potem porównać kompresję z kontrolą bez struktury hierarchicznej.
