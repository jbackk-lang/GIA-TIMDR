# Utrzymanie repozytorium GIA-TIMDR

Ten katalog zawiera audyty techniczne i porządkowe repozytorium. Nie jest źródłem prawdy o wynikach naukowych; te pozostają w prerejestracjach, raportach RESULT, kodzie i danych właściwych linii badawczych.

## Audyty

- [Audyt porządkowy — 23.11.2026](AUDYT_PORZADKOWY_2026-11-23.md) — zasady bezpiecznego sprzątania, mapa ryzyk i kolejność prac.\n- [Audyt ekstrakcji fazy modalnej — 23.11.2026](AUDYT_EKSTRAKCJI_FAZY_MODALNEJ_2026-11-23.md) — ograniczenia pojedynczego binu FFT, przenoszenia fazy i porównywania stacji.

## Zasady zmian

1. Prace porządkowe wykonuj na osobnej gałęzi i przedstawiaj przez pull request.
2. Nie usuwaj danych, prerejestracji, wyników ani kodu badawczego wyłącznie z powodu wieku lub nazwy.
3. Przed przeniesieniem pliku sprawdź odwołania w Markdown, Pythonie, workflow i skryptach uruchomieniowych.
4. Dla plików binarnych porównuj SHA-256; podobna nazwa nie jest dowodem duplikatu.
5. Po zmianie uruchom właściwe testy i odnotuj dokładny commit oraz wynik. Brak uruchomienia CI nie oznacza sukcesu.
6. Nie zmieniaj interpretacji naukowej w ramach mechanicznego porządkowania.

## Zakres

Katalog służy do dokumentowania audytów, checklist i decyzji utrzymaniowych. Nie należy tu kopiować pełnych raportów eksperymentalnych ani tworzyć równoległego backlogu badań.
