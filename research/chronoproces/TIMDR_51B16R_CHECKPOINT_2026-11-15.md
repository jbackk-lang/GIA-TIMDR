# TIMDR 51B.16r — Zewnętrzny harness LRAT i priorytet odkryć w README

Data: 2026-11-15.

## Zrealizowane
- Zaktualizowano główne `README.md` GIA-TIMDR: dodano tabelę odkryć 51B.15u–51B.16q, zakres matematyczny, wyniki testów i otwartą bramkę cross-validation; raport łożyskowy zachowano jako link do archiwum.
- Utworzono `research/chronoproces/README.md` jako indeks teorii, kodu i checkpointów.
- Dodano lokalny prototyp `external_validation.py` do reprodukowalnego uruchamiania niezależnego programu LRAT na tych samych plikach DIMACS/LRAT, z hashami i jawnymi statusami.
- `python -m unittest -q` w katalogu `timdr_51b16r`: 12/12 PASS.
- `python external_validation.py`: k=1 i k=2 zwróciły UNVERIFIED z przyczyną external_checker_not_installed. Nie było rzeczywistej zewnętrznej walidacji.

## Kontekst źródłowy
Referencyjne narzędzia: marijnheule/drat-trim (`lrat-check`), tanyongkiam/cake_lpr (formalnie weryfikowany LRAT/LPR checker). Zgodność formatu i protokołu wyjścia wymagają osobnej walidacji po instalacji.

## Ograniczenia
Nie wykonano niezależnej cross-validation; testy regresyjne sprawdzają nasz prototyp, nie zewnętrzny checker. Harness jest eksperymentalny, nie stanowi bezpiecznego sandboxa. Skróty plików nie dowodzą poprawności modelu fizycznego. Repozytorium GitHub zawiera checkpointy, lokalny ZIP jest do pobrania w rozmowie.

## Następny warunek
Zainstalować/pozyskać niezależną binarkę, uruchomić harness na dokładnie tych samych wejściach, porównać wyniki, udokumentować rozbieżności.
