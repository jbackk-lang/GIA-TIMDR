# Paderborn w chmurze — plan odtwarzalności (2026-11-17)

## Co działa obecnie
- GitHub Actions wykonuje testy matematycznego modelu referencyjnego i testy skryptu inwentaryzacji.
- Skrypt `scripts/check_paderborn_data.py` wykrywa obecność plików po nazwie. **Nie sprawdza poprawności archiwów ani zawartości NPZ.**
- Runner GitHub Actions jest efemeryczny: nie ma dostępu do dysku autora ani do plików z poprzednich uruchomień.
- Artefakt `paderborn-inventory.json` opisuje wyłącznie środowisko runnera. Brak danych na runnerze **nie oznacza**, że autor usunął dane.

## Co jest potrzebne do eksperymentu na realnych danych
1. Ustalić oficjalne źródło i warunki dostępu/licencję zbioru Paderborn; nie umieszczać surowych archiwów w publicznym repozytorium bez weryfikacji warunków.
2. Umieścić 15 wymaganych archiwów `K*.rar` w autoryzowanym magazynie obiektowym lub pobierać je w zadaniu z oficjalnego źródła. Zapewnić SHA-256, rozmiar i źródło dla każdego pliku.
3. Odtworzyć dane pochodne na runnerze o wystarczającej przestrzeni, CPU/RAM i limicie czasu. Kod odczytuje archiwa RAR przez `unrar.cffi` i pliki MATLAB przez SciPy.
4. Zweryfikować integralność danych pochodnych: 15 plików NPZ, 80 pomiarów na łożysko, `raw` o długości 64000, `tok` o kształcie 15 × 230, `cond` i `meas`; dodatkowo `rs_feats_all.json` o zgodnych identyfikatorach.
5. Zamrozić protokół eksperymentu, zapisać wersje pakietów, seedy, identyfikatory podziałów i hashe wejść. Uruchomić benchmark w osobnym zadaniu.
6. Publikować w repozytorium tylko raporty, metadane i wyniki zgodne z licencją; duże dane w zewnętrznym magazynie.

## Krytyczny warunek porównania
`core/paderborn_lc_io.py` oblicza `tokens(x, rpm(cond))`. TIMDR ma zatem informację o prędkości obrotowej w preprocessing; ramiona raw/spec nie otrzymują jej jawnie. Przed twierdzeniem o przewadze reprezentacji wymagane są kontrole z tym samym dostępem do RPM (np. raw+RPM i spec+RPM), przy rozdziale łożysk i identycznych danych treningowych. HMM i LSTM nie zostały jeszcze uruchomione w tym benchmarku.

## Status naukowy
Wyniki historyczne są dokumentacją wcześniejszych pomiarów, a nie nową niezależną walidacją. Nie deklarować odtworzenia Paderborn ani sukcesu benchmarku dopóki nie ma logów wykonania na prawdziwych danych.
