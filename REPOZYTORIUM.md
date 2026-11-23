# Mapa repozytorium GIA-TIMDR

Stan mapy: 22 listopada 2026 r. Ten plik służy do nawigacji, nie nadaje nowego statusu hipotezom.

## Gdzie szukać

| [Dokumentacja](docs/README.md) | Indeks dokumentów tematycznych | Architektura, formalizacja, audyty, teoria, geometria, badania, archiwum i [indeks materiałów binarnych](docs/assets/README.md) |

| Miejsce | Zawartość | Uwaga |
|---|---|---|
| [README.md](README.md) | Krótki, aktualny punkt wejścia | Zacznij tutaj |
| [Konstrukcja TRM/GIA → gałęzie](docs/theory/TIMDR_EventGraph_Branch_Construction.md) | Graf zdarzeń, selekcja GIA, sygnał, geometria, modalność i META | Kod w `core/trm_gia_projections.py`; 17 kontroli syntetycznych w `tests/test_trm_gia_projections.py` |
| [HISTORIA_README.md](docs/archiwum/HISTORIA_README.md) | Zachowany dawny README | Miesza opisy koncepcyjne i wyniki z różnych dat |
| [STAN_PROJEKTU.md](STAN_PROJEKTU.md) | Migawka ręcznej oceny z 30.09.2026 i bilans historyczny z 28.09.2026; nie jest bieżącym statusem całego repozytorium | Późniejsze aktualizacje: główny README i datowane checkpointy; generator bilansu wstrzymuje zapis, jeśli brakuje tabeli źródłowej |
| [Indeks archiwum](docs/archiwum/README.md) | Datowane podsumowania historyczne i zasady ich zachowania | Do wglądu; bieżące aktualizacje: główny README i datowane checkpointy |
| [Indeks materiałów binarnych](docs/assets/README.md) | PDF-y, DOCX, obrazy i istniejące diagramy | Dokumenty źródłowe w `docs/assets/source-documents/`, obrazy w `docs/assets/images/` |
| [docs/theory](docs/theory/) | Aksjomaty, Chronoproces, reguły metodologiczne i szkice | Sprawdzaj status konkretnego dokumentu |
| [scripts](scripts/README.md) | Skrypty do stanu projektu, walidacji danych i narzędzia GUI | Indeks uruchamiania i przeznaczenia |
| [docs/geometry](docs/geometry/) | Prerejestracje, manifesty, wyniki i notatki mostów | Wynik czytaj razem z planem i danymi |
| [docs/diagrams](docs/diagrams/) | Diagramy i wizualizacje | Ilustracje, nie niezależny dowód |
| [experiments](experiments/) | Skrypty eksperymentalne pogrupowane według linii badawczych | Indeks serii [54A](experiments/54A/README.md); kod, raporty i wyniki są rozdzielone |
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

## Astronomia

- [Podsumowania nowych aplikacji](docs/astronomy/ASTRONOMIA_2026-09-30.md).
- [Wybrane źródła, pochodzenie i sumy kontrolne](applications/astronomy/README.md).
