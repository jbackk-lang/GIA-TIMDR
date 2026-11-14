# Trzy zegary i wspólny dryft — 2026-11-14

**Status:** lokalnie wykonany eksperyment syntetyczny; kod do pobrania jako artefakt rozmowy `three_clocks.py`. Nie jest to walidacja pełnego TIMDR.

## Model

101 znaczników na sesję, 300 sesji kalibracyjnych oraz po 300 testowych na każdy z czterech scenariuszy. Dwa zegary odbiorników A i B mają niezależny szum Gaussa σ=0.004, ale mogą dzielić identyczny dryft kwadratowy `0.15t²`. Trzeci zegar referencyjny ma niezależny szum σ=0.004 i nie dzieli tego dryftu. Osobno **udostępniono bezszumowy znacznik czasu obiektu** z opcjonalnym warp `0.15t²`; to silne założenie eksperymentu, nie obserwacja uzyskana z sygnału.

Statystyka: różnica nachyleń regresji liniowej w dwóch połowach sesji. Progi: 99. percentyl wartości bezwzględnej z 300 niezależnych sesji stabilnych, osobno dla porównań A–B, referencja–A, referencja–obiekt. Progi: 0.018126, 0.020244, 0.013848. Test na odłożonych ziarnach.

## Wyniki rzeczywistego wykonania

```text
thresholds 0.018126 0.020244 0.013848
scenario,AB_detect,anchor_receiver_detect,anchor_object_detect,correct_joint,total
STABLE,10,3,3,295,300
OBJECT_WARP,5,7,300,293,300
SHARED_DRIFT,2,300,5,295,300
BOTH,2,300,300,300,300
```

`AB_detect` jest dwustronnym testem różnicy A–B; jego sporadyczne alarmy wynikają z szumu. `correct_joint` oznacza poprawną czteroklasową klasyfikację na podstawie dwóch porównań do niezależnego zegara. Wariant nie ma jawnego `UNKNOWN` w klasyfikacji czteroklasowej; to ograniczenie, które należy naprawić przed stosowaniem do realnych danych.

## Wniosek

Wspólny dryft odbiorników nie jest identyfikowalny z samego ich wzajemnego porównania. Trzeci niezależny zegar pozwala wykryć dryft odbiorników. **Rozdzielenie zmiany czasu obiektu od zmiany zegarów odbiorników wymagało w tym eksperymencie dodatkowo niezależnie dostępnego czasu obiektu** — trzy zegary obserwacyjne same nie wystarczają automatycznie.

To test warunkowej identyfikowalności, nie dowód, że czas jest odrębną substancją informacji.

## Kolejne zadanie

Usunąć idealny znacznik czasu obiektu; zastosować realistyczny zaszumiony marker fizyczny i jawny `UNKNOWN`, zmierzyć identyfikowalność przy brakującej referencji, wspólnym dryfcie wszystkich zegarów i opóźnieniu kanału. Osobno porównać trajektorie MIN/MAX/czas.
