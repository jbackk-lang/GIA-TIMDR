# TIMDR 51B.16s — Audyt protokołu zewnętrznego checkera LRAT

Data: 2026-11-15.

## Odkrycie inżynieryjne
W adapterze 51B.16r warunek `'VERIFIED' in output.upper()` akceptował także podciąg w `NOT VERIFIED` przy kodzie zakończenia 0. Jest to luka interpretacyjna na granicy zewnętrznego checkera, niezależna od poprawności algorytmu LRAT.

## Poprawka
W `external_validation.py` wymagamy teraz: kod zakończenia 0, osobna linia `c VERIFIED`, brak osobnej linii `c NOT VERIFIED`. Format wynika z komunikatów źródłowego `lrat-check.c` w `marijnheule/drat-trim`. Dodatkowe komunikaty mogą wymagać wersjonowanego adaptera. Zapisujemy hash binarki, CNF i dowodu.

## Pomiary
`python -m unittest -q`: **17/17 PASS** (12 regresyjnych i 5 nowych testów protokołu).
Nowe testy: marker pozytywny, marker negatywny, podciąg pozornie pozytywny, kod niezerowy, brak binarki. Użyto kontrolowanych stubów, nie niezależnego checkera LRAT.
`python external_validation.py`: k=1 i k=2 → `UNVERIFIED` (`external_checker_not_installed`).

## Status
Bramka rzeczywistej cross-validation nadal otwarta. Wynik testów stubów nie jest dowodem poprawności LRAT. Prototyp lokalny: `/mnt/data/timdr_51b16s_prototype.zip`. Główne README i indeks Chronoprocesu aktualizowane na `main`.

## Źródło referencyjne
https://github.com/marijnheule/drat-trim/blob/master/lrat-check.c — końcowe komunikaty `c VERIFIED` oraz `c NOT VERIFIED`, kod zakończenia odpowiednio 0/1.
