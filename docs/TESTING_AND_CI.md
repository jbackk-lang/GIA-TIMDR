# Testy i ciągła integracja

Ten dokument opisuje aktualne, jawnie skonfigurowane zestawy testów. Nie zakłada, że wszystkie testy repozytorium można uruchomić jednym poleceniem ani że każde środowisko ma dostęp do danych eksperymentalnych.

## Wymagania

- Python 3.11 — wersja używana przez opisane workflow GitHub Actions.
- Zależności instaluj zgodnie z konkretnym zestawem:
  - testy rdzenia: `numpy`, `pytest`;
  - regresje eksperymentów: `numpy`, `scipy`, `pytest`;
  - testy inwentarza i walidacji danych TIMDR: `numpy>=1.24,<3`.
- Repozytorium nie ma obecnie jednego głównego pliku `requirements.txt` ani `pyproject.toml` deklarującego komplet zależności dla wszystkich eksperymentów. Nie instaluj arbitralnie wszystkich bibliotek do jednego środowiska.

## Zestawy CI

### Core regression tests

Workflow: `.github/workflows/core-regression-tests.yml`

Uruchamia:
```powershell
python -m pytest -q tests/test_modal_self_repair.py
python -m pytest -q tests/test_operators_wiring.py
```

Wymagania: NumPy i pytest.

### Repository regression checks

Workflow: `.github/workflows/experiment-relocation-checks.yml`

Obejmuje:
- kompilację przeniesionych eksperymentów;
- testy punktów zgodności starszych ścieżek;
- testy chronoprocesu i pętli;
- 23 testy regresji syntetycznej/jednostkowej, w tym mosty chronogeometryczne, perturbacje, rezonans i walidację filtrów.

Wymagania: NumPy, SciPy i pytest. Pełne polecenia znajdują się bezpośrednio w workflow, aby lista testów była jednoznaczna i audytowalna.

### TIMDR cloud checks

Workflow: `.github/workflows/timdr-cloud-checks.yml`

Uruchamia testy:
- projekcji TRM/GIA;
- inwentarza danych Paderborn;
- walidacji plików NPZ;
- manifestu pochodzenia archiwów.

Workflow tworzy artefakt inwentarza. Nie pobiera ani nie fabrykuje zewnętrznych danych eksperymentalnych.

## Uruchamianie lokalne

W PowerShell, z katalogu głównego repozytorium:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy scipy pytest
python -m pytest -q
```

Ostatnie polecenie jest próbą uruchomienia całego katalogu testów, a nie gwarancją, że każdy test jest samowystarczalny. Testy zależne od zewnętrznych archiwów lub ścieżek danych mogą wymagać osobnego przygotowania i mogą zostać pominięte zgodnie z warunkami w samym teście.

Aby odtworzyć dokładnie to, co sprawdza CI, uruchamiaj polecenia z odpowiedniego pliku workflow. Zielony wynik jednego zestawu nie oznacza automatycznie, że wszystkie 38 plików testowych zostało wykonanych.

## Interpretacja statusu

- **Workflow skonfigurowany** — istnieje definicja zadania.
- **Test wykonany** — GitHub Actions lub lokalny proces faktycznie go uruchomił.
- **Test zaliczony** — wynik konkretnego uruchomienia jest sukcesem.

Nie należy utożsamiać tych trzech stanów. Szczególnie testy oparte na rzeczywistych danych wymagają jawnego potwierdzenia, że dane były dostępne i test nie został pominięty.
