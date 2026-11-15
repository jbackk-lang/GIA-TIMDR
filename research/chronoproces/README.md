# Chronoproces — indeks badań nad bezpieczną diagnozą i certyfikacją regulatorów

**Status 2026-11-15:** aktywna linia badawcza 51B.15u–51B.16r. To indeks twierdzeń, prototypów i granic, a nie deklaracja produkcyjnego certyfikatu bezpieczeństwa.

## Odkrycia matematyczne
1. **Gra przekonań i warunki bezpiecznej diagnozy (15u–15z, 16a, 16g):** największy punkt stały bezpieczeństwa, osiągalność pewnej diagnozy, rozróżnienie etykiety bieżącej od niezmiennego pochodzenia; pułapka epistemiczna może wykluczyć dowolną pamięć.
2. **Sterowanie przy ograniczonej informacji (16b–16d, 16j):** regulator ma wyłącznie dostęp do pamięci i obserwacji; numer komórki abstrakcji nie jest dodatkowym kanałem pomiarowym.
3. **Geometria i abstrakcja (16e–16f):** nadaproksymacja wspiera dodatnie dowody bezpieczeństwa, lecz ujemne świadectwo wymaga realizowalności konkretnej trajektorii.
4. **Dowody dodatnie i ujemne (16h–16k):** rangi i domknięcie indukcyjne dla strategii dodatniej; bezpieczne niediagnostyczne lasso albo niebezpieczny prefiks dla porażki ustalonego regulatora; wyczerpujący dowód negatywny dla klasy k-memory.
5. **Symboliczna synteza i niewykonalność (16l–16m):** formuła CNF reprezentuje rodzinę tablic regulatorów, a dowód UNSAT może wykluczyć ją bez jawnego wypisywania tablic; nie ma gwarancji wielomianowej długości dowodu.

## Prototypy i pomiary
| Etap | Empiryczny rezultat | Ważne ograniczenie |
|---|---|---|
| [16i](TIMDR_51B16I_CHECKPOINT_2026-11-15.md)–[16k](TIMDR_51B16K_CHECKPOINT_2026-11-15.md) | Exact belief checker, k-memory i enumeracyjny negative checker; lokalne testy jednostkowe | Skończone modele; brak formalnej weryfikacji implementacji |
| [16m](TIMDR_51B16M_CHECKPOINT_2026-11-15.md) | 36 zgodnych porównań SAT/enumeracja dla małych gier; RUP-LRAT | Ograniczony korpus; naiwny generator dowodów |
| [16n](TIMDR_51B16N_CHECKPOINT_2026-11-15.md) | Eksperymentalny checker RUP/RAT i testy parsera | Niepełna walidacja zgodności LRAT |
| [16p](TIMDR_51B16P_CHECKPOINT_2026-11-15.md) | SHA-256 manifest; 2500 mutacji bez nieobsłużonych wyjątków | Mutacyjny smoke-fuzzing nie dowodzi odporności |
| [16q](TIMDR_51B16Q_CHECKPOINT_2026-11-15.md) | Proces potomny, limity zasobów, 12/12 testów | Izolacja procesu ≠ niezależny checker |
| [16r](TIMDR_51B16R_CHECKPOINT_2026-11-15.md) | Reprodukowalny harness dla zewnętrznego LRAT, 12/12 testów regresyjnych | **Zewnętrzna walidacja nie została wykonana**; brak narzędzia w środowisku |

## Krytyczna bramka niezależnej walidacji
Zainstalować rzeczywiście niezależny [lrat-check](https://github.com/marijnheule/drat-trim) lub formalnie weryfikowany [cake_lpr](https://github.com/tanyongkiam/cake_lpr); uruchomić dokładnie te same DIMACS/LRAT, zapisać wersję i SHA-256 binarki, stdout/stderr, kod wyjścia, limity i różnice. Nie uznawać braku narzędzia, timeoutu ani błędu parsowania za dowód UNSAT.

## Zasada dokumentacyjna
Główne [README](../../README.md) prezentuje kluczowe odkrycia i uczciwy status dowodowy. Tutaj pozostają techniczne checkpointy. Raporty łożyskowe i inne domenowe są powiązanymi eksperymentami, nie zastępują rdzenia matematycznego.
