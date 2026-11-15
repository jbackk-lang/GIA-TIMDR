# Niedoskonały znacznik czasu obiektu — test identyfikowalności

Data: 2026-11-14. Status: wykonano lokalnie skrypt Python `timdr_imperfect_marker.py`, seed 20261114. Eksperyment syntetyczny, nie walidacja fizyczna TIMDR.

## Model
Cztery scenariusze: brak zmian, warp czasu obiektu, wspólny dryft dwóch odbiorników, obie zmiany. 500 testów na scenariusz; 101 punktów czasowych. `t∈[0,1]`; warp kwadratowy `0.15t²`. Dwa odbiorniki A/B i niezależny zegar C: szum Gaussa σ=0.008. Fizyczny marker M czasu obiektu: szum 2σ=0.016, niezależny; znacznik niedostępny z prawdopodobieństwem 0.25. Parametr krzywizny czasu estymowany jako współczynnik przy `t²` w regresji kwadratowej. Progi: 99. percentyl absolutnej statystyki na 3000 osobnych próbach zerowych. Decyzja dryftu odbiorników wymaga przekroczenia progu przez A-C i B-C; decyzja o warp obiektu wymaga M-C. Brak M => UNKNOWN dla **pełnej dwuwymiarowej etykiety**, nawet gdy sam dryft odbiorników można określić.

## Wyniki uruchomienia
```text
thresholds 0.0391 0.06166
NO_OBJECT_NO_RECEIVER {'correct': 364, 'unknown': 134, 'wrong': 2, 'marker_missing': 134}
OBJECT_NO_RECEIVER {'correct': 372, 'unknown': 128, 'wrong': 0, 'marker_missing': 128}
NO_OBJECT_RECEIVER {'correct': 378, 'unknown': 121, 'wrong': 1, 'marker_missing': 121}
OBJECT_RECEIVER {'correct': 386, 'unknown': 114, 'wrong': 0, 'marker_missing': 114}
```

Razem: 1500 poprawnych, 497 UNKNOWN, 3 błędne na 2000 prób. Pokrycie 75.15%, poprawność warunkowa wśród decyzji 1500/1503 = 99.8004%. UNKNOWN jest **deterministycznie wywoływany przez brak markera**, a nie adaptacyjną ocenę niskiej pewności przy dostępnych danych. Nie wolno interpretować 99.8% jako dowodu skalibrowanej niepewności.

## Ograniczenia i istotny kontrprzykład
Zegar C jest niezależny i nie dryfuje. Marker M jest niedoskonały, ale bez systematycznego błędu. Nie testowano wspólnego dryftu A/B/C/M: bez zewnętrznego punktu odniesienia globalny dryft może pozostać niewykrywalny. Przebiegi sygnału amplitudowego nie były tu użyte do klasyfikacji; badano **identyfikowalność relacji czasowych**, a nie spektrum ani pełny Chronoproces.

## Następny krok
Przypadek wspólnego dryftu wszystkich zegarów, brak referencji absolutnej, opóźnienie kanału, brak danych i niepewność oszacowania; wyprowadzić formalną klasę transformacji nieidentyfikowalnych. Następnie powiązać zegary z dynamiczną trajektorią sygnału i publiczną reprezentacją MIN–MAX–CZAS.
