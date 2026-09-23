# Mapa repozytorium GIA-TIMDR

Stan mapy: 23 września 2026 r. Ten plik służy do nawigacji, nie nadaje nowego statusu hipotezom.

## Gdzie szukać

| Miejsce | Zawartość | Uwaga |
|---|---|---|
| [README.md](README.md) | Krótki, aktualny punkt wejścia | Zacznij tutaj |
| [HISTORIA_README.md](HISTORIA_README.md) | Zachowany dawny README | Miesza opisy koncepcyjne i wyniki z różnych dat |
| [PODSUMOWANIE_PROJEKTU_2026-09-23.md](PODSUMOWANIE_PROJEKTU_2026-09-23.md) | Pełne podsumowanie formalizmów i aplikacji na wskazany dzień | Przy nowych wynikach utworzyć nową wersję datowaną |
| [docs/theory](docs/theory/) | Aksjomaty, Chronoproces, reguły metodologiczne i szkice | Sprawdzaj status konkretnego dokumentu |
| [docs/geometry](docs/geometry/) | Prerejestracje, manifesty, wyniki i notatki mostów | Wynik czytaj razem z planem i danymi |
| [docs/diagrams](docs/diagrams/) | Diagramy i wizualizacje | Ilustracje, nie niezależny dowód |
| [core](core/) i [tests](tests/) | Operatory i ich testy | Test jednostkowy nie zastępuje testu real-data |
| [TIMDR-Math-Formalism](TIMDR-Math-Formalism/) | Gałąź sygnałowa M/S | Podkatalog włączony przez `git subtree` |
| [TIMDR-Geometry-Formalism](TIMDR-Geometry-Formalism/) | Gałąź geometryczna G | Podkatalog włączony przez `git subtree` |
| [TIMDR-Modal-Formalism](TIMDR-Modal-Formalism/) | Gałąź modalna K | Podkatalog włączony przez `git subtree` |
| [TIMDR-Time-Formalism](TIMDR-Time-Formalism/) | Chronoproces i most Fouriera | Podkatalog włączony przez `git subtree` |
| [MAGE-IN-IMAGE-DECODER](MAGE-IN-IMAGE-DECODER/) | Kopia trzech modułów obrazu/wideo | Nie zawiera pełnych danych ani historii repo źródłowego |
| [timdr_visualizer](timdr_visualizer/) i [filters](filters/) | Narzędzia pomocnicze | Nie są dodatkowymi gałęziami |
| [TIMDR-fusion-tools](https://github.com/jbackk-lang/TIMDR-fusion-tools) | Osobne repo aplikacyjne: diagnostyka plazmy TCABR | Nie jest podkatalogiem ani piątą gałęzią formalną; wyniki i dane czytać w jego README |

Inne istotne aplikacje — trzy wersje Synoptyka, diagnostyka przemysłowa, energetyczna, sejsmiczna, obrazowa i AI — mają odnośniki w [README](README.md#powiązane-zastosowania). Pełny spis repozytoriów jest utrzymywany w [katalogu ekosystemu](https://github.com/jbackk-lang/jbackk-lang.github.io/blob/main/KATEGORIE.md), zamiast dublowania go tutaj.

## Źródła prawdy

- Definicje i statusy gałęzi: [specyfikacja](docs/theory/TIMDR_Branch_Specification.md), właściwe pliki `Axioms_*` w `docs/theory/` oraz [słownik](docs/GLOSSARY_EN_PL.md).
- Status pojedynczego testu: jego dokument `RESULT_*` czytany z wcześniejszym `PREREG_*`, manifestem i kodem. Ogólny opis w README nie zastępuje tych artefaktów.
- Granica kalibracji i potwierdzenia: [reguła zamrożenia](docs/theory/TIMDR_CALIBRATION_FREEZE_RULE.md).
- Opisy trójkąta i TRM zachowane w historii README są warstwą koncepcyjną. Nie przenoszą automatycznie swoich twierdzeń na wyniki testów gałęzi formalnych.

Przy nowym eksperymencie dodaj osobny PREREG, zamroź kod i kryteria, a po teście zapisz nowy RESULT. Nie zastępuj historycznego werdyktu. Przed commitem sprawdź `git status --short` i dodaj tylko pliki odpowiadające danemu tematowi.
