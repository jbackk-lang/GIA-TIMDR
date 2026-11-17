# 51B.22 — odporność prioru geometrycznego (syntetyczny test)

## Status i odtwarzalność

Kod: `research/51B22_PRIOR_ROBUSTNESS.py`. Wykonanie lokalne potwierdzone; ponownie wygenerowany JSON jest bajtowo identyczny z zapisanym wynikiem. Uruchomienie: `python research/51B22_PRIOR_ROBUSTNESS.py > 51B22_RESULTS.json`. Brak zależności zewnętrznych. Wyniki generowane deterministycznie dla `SEED=51222026`.

**Nie jest to test operacyjnego GIAFilter ani `gia_select`.** Prior jest niezależną wskazówką na poziomie zadania, poprawną z narzuconym prawdopodobieństwem `q`. Nie jest estymowany z geometrii.

## Protokół

- Trzy procesy: `(P(S=1), P(F=1|S=1), P(F=1|S=0))` = `(0.05,0.99,0.01)`, `(0.1,0.9,0.1)`, `(0.2,0.8,0.2)`.
- Jeden sygnał `S` i jeden niezależny zakłócacz `D`, budżet jednego zdarzenia.
- P wybiera cechę z większą estymowaną informacją wzajemną, z wygładzaniem Jeffreysa.
- H dodaje preferencję `lambda=0.02` do cechy wskazanej przez prior; `q` = 0.5, 0.6, 0.75, 0.9, 1.0.
- `n` = 10, 20, 40, 80, 160, 320; po 600 powtórzeń na punkt.
- Populacyjna strata przy wyborze zakłócacza to `I(F;S)`; przy wyborze sygnału wynosi 0. Wartości średnie to ta strata pomnożona przez częstość błędnego wyboru.
- `n_epsilon` = pierwszy punkt badanej siatki, gdzie *punktowa* górna granica 95% Wilsona na średnią stratę nie przekracza `epsilon`; brak korekty na wielokrotne testowanie i przeszukiwanie siatki.

## Wyniki dla epsilon = 0.005, proces 0

| q | n(P) | n(H) | n(P)/n(H) |
|---:|---:|---:|---:|
| 0.50 | 20 | 20 | 1.00 |
| 0.60 | 20 | 80 | 0.25 |
| 0.75 | 20 | 40 | 0.50 |
| 0.90 | 20 | 10 | 2.00 |
| 1.00 | 20 | 10 | 2.00 |

Przy `q=0.75` prior częściej trafia niż się myli, lecz H potrzebuje na badanej siatce dwukrotnie więcej próbek. Sama dodatnia trafność prioru nie wystarcza.

Dla `q=0.90`, `epsilon=0.005`: proces 0 ma `20/10=2`, proces 1 `40/40=1`, proces 2 `80/40=2`. Brak jednolitej przewagi w całej rodzinie.

## Wniosek i granice

Geometria może działać jako prior indukcyjny, ale jej korzyść próbkowa zależy od zgodności z procesem i od kosztu błędnego wskazania. Nie dowodzi to przewagi GIA, zysku asymptotycznego ani zwiększenia informacji względem historii. Deterministyczna reprezentacja historii podlega nierówności przetwarzania danych.

Ważne: `q` jest losowane na poziomie zadania/próby treningowej, a nie dla każdego zdarzenia. Sformułowanie „75% trafności” nie oznacza dokładnie 75% poprawnych wyborów operatora H.

## Następny test

51B.23: wygenerować prior przez rzeczywisty `core.trm_gia_projections.gia_select`, z kalibracją geometrii wyłącznie na danych treningowych, a następnie porównać z P i H przy kontrolowanym koszcie reprezentacji. Rozróżnić operator referencyjny od produkcyjnego `filters/_vendor_senscore_gia_filter.py::GIAFilter`.
