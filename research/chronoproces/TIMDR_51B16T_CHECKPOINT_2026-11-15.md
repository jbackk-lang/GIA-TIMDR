# TIMDR 51B.16t — Pakiet porównawczy LRAT i uczciwy status bramki zewnętrznej

Data: 2026-11-15.

## Wykonane
- Zbudowano `run_cross_validation.py` — deterministyczne cztery przypadki DIMACS/LRAT: poprawny certyfikat i mutacja uszkodzonej wskazówki dla k=1 oraz k=2.
- Raport `CROSS_VALIDATION.json` zapisuje skróty SHA-256 tekstów DIMACS/LRAT, wynik checkera lokalnego, wynik checkera zewnętrznego i `cross_validation_completed`.
- Lokalnie: `python -m unittest -q` → **20/20 PASS**. Dwa poprawne dowody przyjęte, dwie mutacje odrzucone przez lokalny checker.
- `python run_cross_validation.py` → cztery wyniki zewnętrzne `UNVERIFIED`, `cross_validation_completed=false`.
- Sprawdzono dostępność `gcc`; brak `lrat-check` w PATH. Próba pobrania `lrat-check.c` z `raw.githubusercontent.com` nie powiodła się (DNS). Źródło `lrat-check.c` z `marijnheule/drat-trim` było dostępne do przeglądu przez integrację GitHub, ale nie jako kompilowalny plik w środowisku wykonawczym.

## Wniosek
Nie ma podstaw do deklaracji niezależnej walidacji LRAT. Dostępny jest odtwarzalny zestaw wejść i harness do uruchomienia po pozyskaniu referencyjnej binarki. Po uruchomieniu konieczna analiza rzeczywistych kodów wyjścia i rozbieżności, zwłaszcza przypadków odrzuconych; brak akceptacji nie jest dowodem poprawności odrzucenia.

## Artefakty
Lokalne: `/mnt/data/timdr_51b16t_prototype.zip`, `/mnt/data/timdr_51b16t/CROSS_VALIDATION.json`. Kod nie został dodany do repozytorium GitHub; repozytorium zawiera checkpoint badawczy. Brak pełnej zgodności RAT i formalnego dowodu soundness.
