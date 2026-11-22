# Skrypty pomocnicze

Skrypty repozytorium są pogrupowane według celu. Uruchamiaj je z katalogu głównego repozytorium, chyba że opis wskazuje inaczej.

## Stan projektu

- [`stan_projektu.py`](stan_projektu.py) — odświeża automatyczną część `STAN_PROJEKTU.md` na podstawie tabeli wyników w README.
- [`aktualizuj_stan.bat`](../aktualizuj_stan.bat) — wygodny launcher Windows pozostawiony w katalogu głównym.

## Walidacja i dane Paderborn

- [`check_paderborn_data.py`](check_paderborn_data.py) — kontrola danych Paderborn.
- [`hash_paderborn_archives.py`](hash_paderborn_archives.py) — obliczanie sum kontrolnych archiwów.
- [`validate_paderborn_lc.py`](validate_paderborn_lc.py) — walidacja danych LC dla Paderborn.

## Narzędzia GUI

- [`github_traffic_window.py`](github_traffic_window.py) — okno Tkinter do podglądu statystyk ruchu GitHub; wymaga Pythona z Tkinter i tokenu GitHub podanego przez użytkownika w oknie.

Plik [`StatOkenkoGit.py`](../StatOkenkoGit.py) pozostaje jako cienki launcher zgodności dla dotychczasowej ścieżki.
