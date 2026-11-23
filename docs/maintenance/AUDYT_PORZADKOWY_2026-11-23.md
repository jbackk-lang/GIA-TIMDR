# Audyt porządkowy repozytorium GIA-TIMDR

Data: 2026-11-23  
Audytowany punkt: `main` / `87ec18f1b4bd7b14923b36efe5fed70f3e95533e`  
Cel: uporządkowanie artefaktów i dokumentacji bez zmiany znaczenia naukowego projektu.

## Zasady

- Nie przepisywać historii Git i nie wykonywać force-push.
- Nie usuwać danych, wyników, prerejestracji ani kodu tylko dlatego, że wygląda na stary.
- Nie łączyć gałęzi formalnych ani nie zmieniać statusu hipotez.
- Każde przeniesienie pliku musi zachować starą ścieżkę przez odnośnik lub kompatybilny alias, jeśli istnieją odwołania.
- Zmiany porządkowe wykonywać na tej gałęzi roboczej i przedstawiać jako PR; nie zastępować bezpośrednio `main`.

## Stan techniczny

- Domyślna gałąź: `main`.
- Audytowany HEAD: `87ec18f1b4bd7b14923b36efe5fed70f3e95533e`.
- Drzewo Git: 1262 wpisy; odpowiedź GitHub nie była oznaczona jako ucięta.
- Repozytorium jest publiczne i dostępne do zapisu przez bieżące połączenie.
- Dla badanego SHA endpoint połączonego statusu zwrócił pustą listę statusów, a lista workflow runs powiązanych z commitem była pusta. To oznacza **brak potwierdzonego wyniku CI w tym odczycie**, nie sukces testów.
- W repozytorium znajdują się cztery katalogi formalizmów: `TIMDR-Math-Formalism`, `TIMDR-Geometry-Formalism`, `TIMDR-Modal-Formalism`, `TIMDR-Time-Formalism`.

## Ustalenia porządkowe

### 1. Dokumentacja architektury w dwóch ścieżkach

- `ARCHITEKTURA_TIMDR.md` w katalogu głównym jest krótkim punktem zgodności ze starą ścieżką i odsyła do `docs/architecture/ARCHITEKTURA_TIMDR.md`.
- To nie jest zbędna kopia: plik główny pełni rolę aliasu nawigacyjnego. Należy go zachować.

### 2. Kilka warstw instrukcji/skill

W drzewie istnieją m.in.:

- `SKILL_timdr-signal-framework.md` — uproszczony skrót;
- `docs/SKILL_timdr-signal-framework.md` — krótsza ściąga z metadanymi;
- `timdr-signal-framework-SKILL.md` — rozbudowana wersja;
- `timdr-signal-framework-ADDENDUM.md` — dodatek.

To różne artefakty o różnych deklarowanych zakresach i datach, nie wolno ich mechanicznie scalać ani usuwać. Wymagają jawnego indeksu: który plik jest kanoniczny dla jakiego zastosowania, które są archiwalne i jak są synchronizowane.

### 3. Dokumenty statusowe mają różne daty i role

- `README.md` jest głównym punktem wejścia i zawiera nowsze aktualizacje.
- `REPOZYTORIUM.md` jest mapą nawigacyjną; poprawnie ostrzega, że `STAN_PROJEKTU.md` jest migawką historyczną.
- `STAN_PROJEKTU.md` sam deklaruje stan ręcznej części z 2026-09-30 i bilans automatyczny z 2026-09-28. Nie należy przedstawiać go jako bieżącego statusu.
- `docs/archiwum/README.md` jest indeksem materiałów historycznych.

Problemem nie jest samo istnienie tych dokumentów, lecz ryzyko, że czytelnik potraktuje starszy dokument jako aktualny.

### 4. Katalogi domenowe i eksperymentalne

Repo zawiera osobne obszary `applications/`, `experiments/`, `research/`, `core/`, `filters/`, `scripts/`, `tests/` oraz `timdr_visualizer/`. Ten podział ma sens i nie powinien być zmieniany bez sprawdzenia importów, ścieżek danych, skryptów i linków Markdown.

### 5. Zewnętrzny projekt skopiowany do repo

`MAGE-IN-IMAGE-DECODER/` jest opisany w mapie repozytorium jako kopia trzech modułów, nie pełne repo źródłowe ani pełna historia. Należy sprawdzić, czy ma być adapterem/fixture'em tego repo, czy tylko odsyłaczem do osobnego projektu. Do czasu wyjaśnienia zachować.

## Plan bezpiecznego sprzątania

1. Dodać jeden kanoniczny indeks dokumentacji i statusów, bez usuwania dotychczasowych plików.
2. Oznaczyć w nagłówkach dokumenty statusowe jako: aktualny punkt wejścia, migawka historyczna albo archiwum.
3. Zrobić audyt wszystkich lokalnych linków Markdown i odwołań w kodzie przed jakimkolwiek przenoszeniem.
4. Zidentyfikować duplikaty binarne i tekstowe przez sumy SHA-256; identyczne pliki można dopiero wtedy rozważyć do deduplikacji.
5. Sprawdzić zależności i konfiguracje CI dla każdego formalizmu osobno. Nie uznawać braku workflow run za pozytywny wynik.
6. Dopiero po tych kontrolach przygotować małe, tematyczne commity i PR do `main`.

## Czego ten audyt nie stwierdza

- Nie stwierdza, że pliki w archiwum są zbędne.
- Nie stwierdza, że dwa dokumenty o podobnej nazwie są identyczne.
- Nie stwierdza, że wszystkie testy przechodzą.
- Nie potwierdza empirycznie rezonansu modalnego ani poprawności fizycznej formalizmu.
- Nie zmienia żadnego wyniku badawczego ani statusu hipotezy.

---
Ten plik jest zapisem audytu porządkowego, nie certyfikatem naukowym ani raportem zaliczonych testów.
