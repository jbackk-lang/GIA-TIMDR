# TIMDR 51B.16n — Utwardzenie parsera LRAT i eksperymentalna obsługa RAT

Checkpoint: 2026-11-15.

## Cel i formalna reguła
Kontynuacja 51B.16m: od RUP-only do eksperymentalnego tekstowego checkera LRAT z RUP, RAT i rekordami usuwania klauzul. Dla dodatku klauzuli C z pivotem p, każda aktywna klauzula D zawierająca -p wymaga wykazania RUP rezolwenty (C\{p}) ∪ (D\{-p}). Dla bezpośredniego RUP sprawdza się konflikt propagacji jednostkowej pod negacją C. Akceptacja UNSAT wymaga wyprowadzenia klauzuli pustej. Nie mylić testów różnicowych z dowodem formalnej poprawności.

## Implementacja i testy
Lokalny moduł /mnt/data/timdr_51b16n/hardened_lrat.py: parser tekstowy, dodatki RUP/RAT, usuwanie klauzul, kontrola składni/identyfikatorów/duplikatów grup RAT i ograniczenia wejścia. test_hardened.py: 4 testy unittest, ostatni wynik 4/4 PASS. Poprzednie symbolic.py, base_checker.py, memory_checker.py, negative_checker.py dołączone bez zmian. Archiwum /mnt/data/timdr_51b16n_prototype.zip. Podczas prac testy ujawniły i pomogły poprawić błędy parsera.

## Ograniczenia
Nie ma jeszcze niezależnej walidacji z zewnętrznym checkerem LRAT ani pełnej zgodności formatowej. Brak binary LRAT, formalnej weryfikacji, fuzzingu na dużą skalę, izolacji procesu, limitu CPU, parsera strumieniowego i kanonicznego hash modelu/CNF. Nie deklarować produkcyjnej odporności na wrogie wejście. 36 porównań z 51B.16m potwierdza wyłącznie badane przypadki.

## Następny etap
51B.16o — Walidacja między niezależnymi implementacjami LRAT, generatywny fuzzing, kontrola zasobów i związanie świadectwa z kanonicznym modelem.
