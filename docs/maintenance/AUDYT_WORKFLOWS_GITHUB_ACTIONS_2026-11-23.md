# Audyt workflow GitHub Actions

Data: 2026-11-23  
Gałąź audytowa: `maintenance/repo-hygiene-audit-2026-11-23`  
Zakres: przegląd konfiguracji workflow w `.github/workflows/`; bez uruchamiania zewnętrznych eksperymentów i bez zmiany ich wyników.

## Wynik inwentaryzacji

Przejrzano 26 plików workflow. Zawierają trzy zasadnicze rodzaje automatyzacji:
- regresje i testy formalizmów,
- uruchamiane ręcznie analizy badawcze publikujące artefakty,
- wąskie eksperymenty geometrii/odbicia uruchamiane po zmianie wskazanych plików.

Nie ma podstaw, by usuwać je zbiorczo. Wiele z nich jest celowo wąskich i odpowiada konkretnym protokołom badawczym.

## Znaleziska

### A. Powtarzające się uruchomienia tych samych eksperymentów

1. `reflection-transition-bc-bridge.yml` uruchamia `experiments/bc_opposite_direction_pair.py`; ten sam skrypt jest uruchamiany także przez `bc-opposite-strands.yml`. Przy zmianach w ścieżkach wspólnych oba workflow mogą uruchomić tę samą analizę.
2. `rhombic-prism-axis-geometry-audit.yml` oraz `rhombic-prism-mobility-screw.yml` uruchamiają `rhombic_prism_axis_geometry_limit_audit.py`; drugi workflow uruchamia ponadto `rhombic_prism_axis_limit_study.py`, który jest też uruchamiany przez `rhombic-prism-center-orbit.yml`.
3. `rhombic-prism-mobility-screw.yml` i `rhombic-prism-center-orbit.yml` mają nakładające się zakresy `experiments/rhombic_prism/**` i część wspólnych skryptów. To powoduje możliwe wielokrotne uruchomienia po jednej zmianie.

To jest nadmiar kosztu CI, ale nie dowód błędności wyników. Bezpieczniejszym rozwiązaniem jest późniejsze scalenie odpowiedzialności lub rozdzielenie filtrów ścieżek, a nie usunięcie testów.

### B. Dwa ręczne workflow CHF RTE

- `chf-rte-electrical.yml` uruchamia pilot na bieżącym checkoutcie i przyjmuje parametr `max_pairs`.
- `chf-rte-pilot.yml` wykonuje podobny skrypt, ale jawnie checkoutuje gałąź `research/chrono-helix-fusion` i nie przyjmuje parametru.

Nie są równoważne: drugi workflow jest przypięty do konkretnej gałęzi badawczej. Zachować oba do czasu potwierdzenia, że gałąź badawcza została scalona lub świadomie porzucona.

### C. Niejednolita obsługa Pull Request

Część workflow badawczych działa tylko na `push` do `main` lub ręcznie (`workflow_dispatch`), bez `pull_request`. Inne mają osobny, lżejszy zestaw testów dla PR. To może być świadomy kompromis kosztów, ale oznacza, że sam PR nie zawsze waliduje wszystkie eksperymenty, które później uruchomi push do main.

Szczególnie warto jawnie opisać politykę dla workflow uruchamiających długie skany geometrii i analizy pobierające dane zewnętrzne.

### D. Zewnętrzne dane i zależności

- `mage-temporal-phase-history.yml` pobiera dodatkowe repozytorium `MAGE-IN-IMAGE-DECODER` bez przypięcia do konkretnego commita/tagu. Wynik może się zmienić bez zmiany GIA-TIMDR.
- `chf-rte-electrical.yml`, `chf-rte-pilot.yml` i `paderborn-real-data.yml` pobierają dane lub zależą od zewnętrznych źródeł. To powinny pozostać zadania ręczne lub jawnie oznaczone jako zależne od dostępności źródła.
- `timdr-cloud-checks.yml` ma kontrolę danych Paderborn bez pobierania danych w kroku inwentarza; to odrębne od ręcznego pobierania realnego archiwum.

### E. Bezpieczeństwo uprawnień

W przejrzanych workflow deklarowane jest minimalne `permissions: contents: read` (albo brak jawnego bloku uprawnień w części starszych, wąskich workflow). Nie znaleziono potrzeby przyznawania tokenowi zapisu repozytorium. W ramach dalszego ujednolicania warto dodać jawne `permissions: contents: read` tam, gdzie go brakuje, po sprawdzeniu zależności.

## Zalecane porządki — bezpieczna kolejność

1. Dodać wspólną politykę: PR = szybkie testy deterministyczne; ręczne uruchomienie = kosztowne analizy i pobieranie danych; push do main = tylko niezbędne regresje.
2. Usunąć podwójne uruchamianie `bc_opposite_direction_pair.py` z jednego z workflow albo zawęzić filtry tak, by analiza miała jednego właściciela.
3. Rozdzielić zakresy workflow rhombic-prism: pojedynczy workflow integracyjny dla wspólnych skryptów i wąskie workflow tylko dla niezależnych eksperymentów.
4. Przypiąć zewnętrzne repozytorium MAGE do SHA lub taga po sprawdzeniu, który stan danych/implementacji jest referencyjny. Nie wybierać arbitralnie najnowszego commita.
5. Ujednolicić jawne minimalne uprawnienia i wersje Pythona/zależności bez podbijania ich „przy okazji”.
6. Po każdej zmianie sprawdzić workflow przez `actionlint` lub równoważną walidację składni oraz uruchomić testy właściwe dla zmienionych ścieżek.

## Czego ten audyt nie potwierdza

- Nie potwierdza, że workflow uruchomiły się poprawnie na aktualnym HEAD.
- Nie potwierdza naukowej poprawności wyników eksperymentów.
- Nie dowodzi, że wszystkie skrypty i dane zewnętrzne są dostępne w każdym środowisku.
- Nie zmienia ani nie usuwa żadnego workflow.

Status: inwentaryzacja i rekomendacje; bez zmian w plikach workflow.
