# 51B.23 — wynik testu referencyjnego gia_select

## Status

Kod: `research/51B23_REFERENCE_GIA_PRIOR.py`, commit `88ee9f17`.

Lokalna rekonstrukcja skryptu i używanych funkcji referencyjnych zakończyła się statusem `REFERENCE_GIA_SELECT_PASS`. Nie jest to wykonanie oryginalnego checkoutu: bezpośrednie pobranie GitHub z kontenera zakończyło się błędem DNS. Rekonstrukcja zachowuje algorytm PCA i selekcji używany w tym eksperymencie, ale nie obejmuje pełnych walidacji klas oryginalnego modułu.

Parametry: `seed=51232026`, `n=(10,20,40,80,160)`, `q=(0.5,0.75,0.9,1.0)`, `repeats=300`, `lambda=0.02`, `epsilon=0.005`. Budżet: jedno zdarzenie. Kalibracja osi PCA na pięciu punktach osi x, bez etykiet. Każdy syntetyczny graf zawiera dwa zdarzenia, a `gia_select` zachowuje dokładnie jedno.

## Wyniki — pierwszy punkt siatki z punktową górną granicą 95% Wilsona <= epsilon

| q | n(G) | n(P) | n(H) | n(P)/n(H) |
|---:|---:|---:|---:|---:|
| 0.50 | brak | 20 | 80 | 0.25 |
| 0.75 | brak | 20 | 40 | 0.50 |
| 0.90 | brak | 20 | 20 | 1.00 |
| 1.00 | 10 | 20 | 20 | 1.00 |

`brak` oznacza nieosiągnięcie progu na siatce, a nie dowód niemożliwości.

## Interpretacja

W tym przebiegu hybryda H nie wykazuje przewagi próbkowej nad P. Dla q=0.5 i 0.75 geometria szkodzi. Sam G jest idealny przy q=1, ponieważ zadano mu korzystne położenie sygnału, ale H z określoną funkcją decyzyjną nie wykazuje przewagi nad P.

**Ograniczenie kluczowe:** `q` jest narzucone przez syntetyczne przypisywanie pozycji. Wywołanie rzeczywistej funkcji referencyjnej `gia_select` nie jest dowodem, że operator odkrywa trafną geometrię. Nie uruchomiono operacyjnego `GIAFilter`.

Granice Wilsona są punktowe i nie korygują wielokrotnego porównywania. `n_epsilon` jest minimum na skończonej siatce. Brak niezależnych danych rzeczywistych i walidacji transferu.

## Następny krok

51B.24: wyznaczyć geometrię z niezależnych danych kalibracyjnych, bez ręcznego sterowania trafnością q; kontrolować koszt reprezentacji i oceniać `gia_select` na danych odłożonych. Następnie oddzielnie przetestować operacyjny `GIAFilter`.
