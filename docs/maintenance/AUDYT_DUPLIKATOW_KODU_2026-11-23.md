# Audyt duplikatów kodu i skryptów — 23.11.2026

## Zakres i metoda

Przeanalizowano rekurencyjne drzewo gałęzi `maintenance/repo-hygiene-audit-2026-11-23`: 1 186 plików, w tym 507 plików kodu/skryptów (Python, YAML, shell, PowerShell, JavaScript/TypeScript). Porównano identyfikatory Git blob dla plików kodowych, a następnie sprawdzono kontekst wszystkich grup identycznych plików.

To jest audyt identyczności bajtowej, nie pełna analiza semantyczna wszystkich 479 plików Python. Identyczny blob nie oznacza automatycznie zbędnego pliku: nazwa i ścieżka mogą być publicznym interfejsem lub punktem zgodności.

## Wyniki

### 1. Pięćdziesiąt dwa identyczne pliki w `experiments/` — celowe punkty zgodności

Znaleziono 52 pliki o identycznej treści i identycznym blob SHA. Nie są to 52 kopie eksperymentu. Każdy jest małym adapterem uruchomieniowym, który:

- odczytuje własną nazwę pliku (`__file__`);
- wybiera katalog tematyczny z mapy `_GROUP`;
- uruchamia odpowiadający mu skrypt kanoniczny przez `runpy.run_path`;
- przy imporcie przekazuje symbole z przestrzeni skryptu docelowego.

Zweryfikowano wszystkie 52 wpisy mapy: wszystkie 52 pliki-adaptery są zarejestrowane, a wszystkie 52 odpowiadające im cele istnieją w drzewie repozytorium. Rozkład celów:
- `experiments/reflections/`: 8;
- `experiments/chronoprocess/`: 6;
- `experiments/rhombic_prism/`: 38.

**Decyzja: zachować wszystkie adaptery.** Usunięcie lub mechaniczne scalenie ich w jeden plik uszkodziłoby nazwy poleceń, które mogą być używane przez workflow, użytkowników, skrypty zewnętrzne i starsze instrukcje. Właściwy kod kanoniczny znajduje się w katalogach tematycznych.

### 2. Dwa pliki puste (0 bajtów)

- `filters/__init__.py` — pusty znacznik pakietu Pythona. Pusty plik może być celowy i wpływa na rozpoznawanie pakietu w starszych środowiskach oraz narzędziach. **Zachować.**
- `docs/research/info_geometry/selective_clock_distractors.py` — pusty plik o nazwie sugerującej kod eksperymentalny. Historia Git wskazuje commit `cf604312` z komunikatem `research: placeholder` z 14.11.2026. To świadomy placeholder, nie przypadkowy duplikat. **Zachować do czasu, gdy badanie zostanie wdrożone albo jawnie zamknięte.**

### 3. Czy znaleziono bezpieczne usunięcia?

Nie. Jedyna duża grupa identycznych plików to jawne adaptery zgodności; drugi przypadek to dwa pliki puste o różnych rolach. Nie wykonano zmian w kodzie źródłowym.

## Zalecenia następnego etapu

1. Przejść od identyczności bajtowej do porównania AST i wspólnych fragmentów funkcji w wybranych modułach, szczególnie w `core/`, `filters/` i `applications/`.
2. Dla każdego potencjalnego duplikatu ustalić, czy jest wspólnym algorytmem, historyczną implementacją, testowym fixture, czy świadomym wariantem eksperymentu.
3. Przed usuwaniem/przenoszeniem sprawdzić importy, wywołania z workflow, dokumentację i historię Git.
4. Adaptery w `experiments/` utrzymać jako stabilne ścieżki zgodności, dopóki istnieją konsumenci tych nazw.

## Ograniczenia

GitHub code search nie zwrócił wiarygodnych wyników referencji dla badanych nazw, więc nie potraktowano go jako dowodu braku użycia. Historia `filters/__init__.py` prowadzi do commita z 12.09.2026 związanego z odzyskaniem poprawionego GIAFilter; pusty plik pozostaje poprawnym znacznikiem pakietu. Audyt potwierdza istnienie celów adapterów, ale nie jest pełnym przeszukaniem wszystkich repozytoriów zewnętrznych ani lokalnych kopii użytkowników. Nie uruchamiano eksperymentów ani testów numerycznych, ponieważ ten etap dotyczył wyłącznie struktury i identyczności plików.
