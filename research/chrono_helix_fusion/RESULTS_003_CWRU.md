# RESULTS_003 — CWRU 12 kHz, rzeczywiste dane, 2026-11-19

Źródło: 16 oryginalnych plików MAT dostarczonych przez użytkownika, CWRU 12k Drive End; 4 obciążenia (0–3 HP), 4 stany (normal, inner 0.007", ball 0.007", outer @6 0.007"). 25 niepokrywających się okien po 2048 próbek na nagranie; 400 okien łącznie. Kod lokalnej reprodukcji korzysta z cech `benchmark.extract` i `bridges.vector`, z poprawioną pochodną przyspieszenia helisy `1/fs` (poprawka przeniesiona do repozytorium).

Podział: leave-one-load-out, cztery testy. W każdym foldzie 300 okien treningowych, 100 testowych. Standaryzacja dopasowywana wyłącznie na treningu. LogisticRegression, max_iter=2000, random_state=42.

| Zadanie | FFT + statystyki | Fuzja CHF bez mostów | Fuzja CHF + mosty |
|---|---|---|---|
| Normal vs fault, średni AUROC | 1.000 | 1.000 | 1.000 |
| Cztery klasy, średnia accuracy | 1.000 | 1.000 | 1.000 |
| Cztery klasy, średnia macro-F1 | 1.000 | 1.000 | 1.000 |

Wyniki były identyczne w każdym z czterech wyłączonych obciążeń. Zatem **nie ma dowodu na przewagę mostów**; obecne zadania są nasycone także dla bazowego FFT.

**Ograniczenia:** okna z jednego nagrania są skorelowane, a obciążenia nie są niezależnymi egzemplarzami łożysk. Ograniczona liczba plików, jeden rozmiar defektu, laboratoryjne warunki. Wynik 100% nie dowodzi generalizacji do nowych maszyn. Nie wykonano testu hipotezy Möbiusa.

**Dalsze testy:** porównanie po wyrównaniu amplitudy RMS, test na innych rozmiarach defektów, walidacja leave-one-bearing/leave-one-machine-out na niezależnych pomiarach, kontrola permutacyjna mostów. Nie przedstawiać wyników 100% jako dowodu skuteczności CHF w praktyce.
