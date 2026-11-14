# Wspólny dryft wszystkich zegarów — nieidentyfikowalność (2026-11-14)

**Status:** kod uruchomiony lokalnie, syntetyczny test; nie walidacja fizyczna TIMDR.

## Pytanie
Czy wspólny dryft czterech zegarów można wykryć z ich wzajemnych różnic, bez zewnętrznego odniesienia?

## Protokół
Cztery zegary: `c_i(t)=t+o_i+g(t)+η_i(t)`, stałe offsety `o=(0,0.1,-0.15,0.23)`, niezależne szumy Gaussa `σ=0.004`, `t=0,...,1` w 101 punktach. Scenariusz stabilny `g(t)=0`; wspólny dryft `g(t)=0.15t²`. Dla porównań wewnętrznych badano maksimum z sześciu bezwzględnych różnic nachyleń regresji w dwóch połówkach sesji dla `c_i-c_j`. Dla zewnętrznej referencji badano zmianę nachylenia średniej czterech zegarów po usunięciu offsetów względem niezależnego idealnego `t`.

Progi obu detektorów ustalone na osobnych 2000 sesjach kalibracyjnych, empiryczny 99. percentyl. Test: po 500 odłożonych sesji na scenariusz. **Referencja zewnętrzna jest idealna w tym pilocie**; nie jest odzyskiwana z sygnału.

## Wynik wykonania
```text
threshold_internal 0.023706 threshold_external 0.007145
scenario,internal_detect,external_detect,total
STABLE,6,5,500
COMMON_DRIFT,6,500,500
max_pairwise_gauge_error 2.22e-16
```

Detektor wewnętrzny przy wspólnym dryfcie alarmuje 6/500, dokładnie tyle samo co przy braku dryftu. Detektor z niezależną referencją wykrywa 500/500 dryftów; 5/500 fałszywych alarmów przy stabilnych zegarach. Liczby dotyczą konkretnej amplitudy dryftu, szumu i modelu.

## Twierdzenie o symetrii wspólnej
Dla dowolnej funkcji `g(t)`, `[c_i(t)+g(t)]-[c_j(t)+g(t)]=c_i(t)-c_j(t)`. Zatem dane złożone wyłącznie z różnic między zegarami są niezmiennicze na wspólne przesunięcie funkcjonalne. Żaden algorytm oparty **wyłącznie na tych różnicach** nie może identyfikować `g` bez dodatkowego ograniczenia. To nie oznacza, że wspólny dryft jest zawsze niewykrywalny przy innych rodzajach pomiaru (np. niezależnych sygnałach fizycznych).

## Interpretacja dla TIMDR
Trzecia współrzędna `CZAS` w MIN–MAX–CZAS wymaga jawnej semantyki: czas względny względem czego? Informacja o relacjach wewnętrznych jest różna od informacji o wspólnej zmianie skali względem zewnętrznego wzorca. Nie jest to dowód ontologiczny, że czas jest „substancją informacji”.

## Następny krok
Zastąpić idealną referencję zegarem z szumem i dryftem; testować, czy klasyfikator potrafi jawnie zwrócić `UNKNOWN` dla nierozstrzygalnych klas, a następnie powiązać dane zegarowe z sygnałem i trzema cechami.
