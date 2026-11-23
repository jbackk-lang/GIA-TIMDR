# Audyt odwołań, importów i pokrycia testami — 23.11.2026

## Zakres

Przegląd wykonano na gałęzi `maintenance/repo-hygiene-audit-2026-11-23`, przed zmianami w tym etapie: `c05331630575e1b45af0c466df57ca8735f12548`.

Sprawdzono drzewo repozytorium, listę testów, importy w wybranych testach oraz ścieżki uruchamiania w trzech workflow. Nie wykonano pełnego parserowego grafu importów dla wszystkich plików ani runtime'owego importu wszystkich modułów. Wyniki należy traktować jako audyt statyczny wybranego zakresu, nie dowód braku wszystkich osieroconych plików.

## Ustalenia

### 1. Wersje metryk chronologicznych mają bezpośrednie testy

- `tests/test_chrono_cone_bridge.py` importuje `core.chrono_cone_bridge`.
- `tests/test_chrono_cone_bridge_v2.py` importuje v2 oraz używa `chrono_cone_ratio` z v1 jako punktu odniesienia.
- `tests/test_chrono_cone_bridge_v3.py` importuje v3 oraz używa `anomaly_radius` z v1 i `trend_referenced_phase` z v2.
- `tests/test_chrono_membrane_bridge.py` importuje `core.chrono_membrane_bridge`.

To są rzeczywiste zależności między wersjami, a nie tylko historyczne nazwy. Nie usuwać starszych funkcji bez aktualizacji testów i zależnych wersji.

### 2. Testy mostów membranowych potwierdzają odrębne protokoły

- `tests/test_real_chrono_membrane_bridge_v0_2.py` sprawdza podział sygnałów na połowy, segmentację, próbkowanie i klasyfikację.
- `tests/test_real_chrono_membrane_bridge_independent.py` sprawdza mechanikę niezależnej walidacji na świeżych danych.
- Oba pliki testowe wprost dokumentują, że nie uruchamiają pełnego eksperymentu na rzeczywistych danych. Testują mechanikę pomocniczą; wyniki pełnych eksperymentów są przechowywane w dokumentacji wynikowej.
- Część testowanych helperów ma analogiczną logikę w obu wariantach, ale testy sprawdzają osobne moduły i parametry API.

Decyzja: zachować oba zestawy testów. Nie przenosić testów do jednego pliku bez zachowania jawnego sprawdzenia obu publicznych ścieżek.

### 3. Filtr vendor ma bezpośredni test

`tests/test_vendor_senscore_gia_filter.py` importuje `Hit`, `Event` i `GIAFilter` z `filters._vendor_senscore_gia_filter`. Modułu nie należy traktować jako osieroconego tylko dlatego, że jego nazwa zaczyna się od podkreślenia.

### 4. Nie wszystkie skrypty badawcze mają osobny test jednostkowy

W widocznym drzewie nie znaleziono bezpośrednich plików testowych o nazwach odpowiadających:
- `core/real_chrono_cone_bridge.py` i `core/real_chrono_cone_bridge_v2.py`;
- `core/real_modal_band_energy_bridge.py` i `core/real_modal_band_energy_bridge_v2.py`.

To nie dowodzi, że są nieużywane: mogą być uruchamiane jako skrypty badawcze, a ich protokoły i wyniki mogą być opisane w prerejestracjach oraz raportach. W tym audycie nie znaleziono wystarczających podstaw, by uznać je za osierocone lub je usuwać.

Zalecenie: jeśli te skrypty mają pozostać odtwarzalnymi punktami wejścia, dodać lekkie testy kontraktowe dla funkcji pomocniczych i formatu wyniku, bez uruchamiania kosztownych analiz na danych zewnętrznych.

### 5. Workflow CI są selektywne, nie stanowią pełnego testu całego core

- `.github/workflows/core-regression-tests.yml` uruchamia testy `test_modal_self_repair.py` i `test_operators_wiring.py`; jego ścieżki wyzwalające obejmują odpowiadające im moduły.
- `.github/workflows/timdr-cloud-checks.yml` obejmuje wybrane testy projekcji i walidacji danych Paderborn oraz kompilację wybranych skryptów.
- `.github/workflows/paderborn-real-data.yml` wykonuje kontrole zasobów i danych Paderborn, ale nie jest ogólnym testem wszystkich modułów `core/`.

Wniosek: brak uruchomienia danego pliku testowego w jednym z tych workflow nie jest równoznaczny z brakiem testu w repozytorium; odwrotnie, zielony wynik jednego workflow nie potwierdza poprawności całego repo.

## Decyzje porządkowe

1. Nie usunięto żadnego pliku kodu ani testu.
2. Nie wykryto w sprawdzonym zakresie importu wskazującego jednoznacznie na nieistniejący moduł.
3. Nie oznaczono skryptów real-data jako osieroconych wyłącznie z powodu braku testu jednostkowego.
4. Najbardziej użytecznym następnym krokiem jest uzupełnienie testów kontraktowych dla skryptów real-data, a następnie pełny automatyczny graf importów (AST) dla całego repozytorium.

## Ograniczenia

Nie wykonano testów, `pytest`, `py_compile` ani CI. GitHub code-search nie zwrócił użytecznych wyników dla wyszukiwań symboli w tym repozytorium, dlatego wnioski o referencjach oparto na drzewie plików, jawnych importach sprawdzonych testów i konfiguracjach workflow. Nie jest to kompletna enumeracja odwołań tekstowych w całym repo.
