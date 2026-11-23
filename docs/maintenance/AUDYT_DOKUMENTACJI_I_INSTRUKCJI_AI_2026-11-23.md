# Audyt dokumentacji i instrukcji AI — 23.11.2026

## Zakres

Porównano główny README, mapę repozytorium, historyczny stan projektu, trzy pliki skill TIMDR, addendum rdzenia, atlas paradoksów oraz dostępne notatki przekazania. Sprawdzono też obecność standardowych punktów wejścia dla agentów (AGENTS.md, CLAUDE.md, GEMINI.md, CODEX.md i instrukcje Copilot).

## Wynik: pliki o podobnych nazwach nie są duplikatami

| Plik | Rola | Decyzja |
|---|---|---|
| `timdr-signal-framework-SKILL.md` | Pełny, przekrojowy skill dla TIMDR i wielu repozytoriów/domen; 29 sekcji i rozbudowana pamięć pułapek | Zachować jako kanoniczny skill cross-repo |
| `SKILL_timdr-signal-framework.md` | Długi, polskojęzyczny skrót ograniczony do teorii, formalizmu i sygnałów GIA-TIMDR; jawnie opisuje odmienny zakres | Zachować; nie zastępować pełnego skilla |
| `docs/SKILL_timdr-signal-framework.md` | Krótka ściąga z metadanymi, przeznaczona do szybkiego użycia przez agenta | Zachować jako skrót operacyjny; sprawdzać datę i aktualność przed użyciem |
| `timdr-signal-framework-ADDENDUM.md` | Uzupełnienie ograniczone do audytu rdzenia `core/`, z problemami i rozwiązaniami | Zachować jako addendum; nie scalać automatycznie, bo wskazuje odrębny zakres i odwołuje się do konkretnych zmian/testów |
| `docs/handoffs/AUDIT_CLAUDE_SKILL_TIMDR_SIGNAL_FRAMEWORK_2026-11-09.md` | Datowana notatka przekazania wniosków geometrycznych | Zachować jako zapis historyczny, nie jako instrukcję nadrzędną |

## Bezpieczna korekta wykonana

W pełnym pliku `timdr-signal-framework-SKILL.md` początkowy blok YAML front matter występował dwa razy pod rząd i był identyczny. Usunięto wyłącznie drugi, powtórzony blok. Treść właściwego skilla pozostała bez zmian. Korekta nie scalała plików i nie usuwała żadnych ustaleń.

## Punkty wejścia AI

W sprawdzonym drzewie gałęzi nie znaleziono `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CODEX.md`, `AI_INSTRUCTIONS.md` ani `.github/copilot-instructions.md`. Nie dodano nowego globalnego pliku instrukcji: jego treść dublowałaby istniejące skille, a nie ma dowodu, że repozytorium korzysta z jednego wspólnego formatu instrukcji agentów.

Zalecana kolejność odczytu dla pracy nad repo:
1. `README.md` — aktualny opis projektu i główny kontekst.
2. `REPOZYTORIUM.md` — mapa katalogów oraz wskazanie źródeł prawdy.
3. Właściwa specyfikacja, prerejestracja, wynik, kod i testy konkretnej linii.
4. Pełny skill cross-repo tylko wtedy, gdy zadanie dotyczy wzorców TIMDR lub transferu między domenami; krótką ściągę GIA-TIMDR traktować jako indeks, nie zamiennik źródeł.

## Dokumenty, których nie należy „odświeżać” mechanicznie

- `STAN_PROJEKTU.md` już jawnie oznacza się jako migawka z 30.09.2026 i historyczny bilans z 28.09.2026. Pozostawiono bez zmian.
- `REPOZYTORIUM.md` jest aktualną mapą na 23.11.2026; nie dublować jej w nowym pliku.
- `TRIGGER.md` opisuje metodę atlasu paradoksów, a `KATEGORIE.md` jawnie przekierowuje do kanonicznego katalogu zewnętrznego i zachowuje treść historyczną. To różne funkcje, nie duplikaty.
- Główny `README.md` jest szerokim opisem koncepcji, wyników i zastosowań. Nie zastępuje dokumentów źródłowych eksperymentów.

## Ograniczenia audytu

Sprawdzenie dotyczyło wskazanych plików i nazw punktów wejścia w drzewie repozytorium na gałęzi utrzymaniowej. Nie oznacza walidacji wszystkich instrukcji w zewnętrznych repozytoriach ani automatycznej aktualności wszystkich datowanych wyników. Nie zmieniano statusu żadnej hipotezy ani wyniku badawczego.
