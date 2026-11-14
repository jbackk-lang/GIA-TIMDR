# Generator, kanał czy odbiornik? — problem identyfikowalności

**Data:** 2026-11-14. **Status:** krytyczna uwaga metodologiczna; hipotezy do sprawdzenia, brak wyników.

## Problem

W eksperymencie zwykle mierzymy `y(t)`, a nie bezpośrednio sygnał źródłowy `s(t)`. Model ogólny:

```text
generator / źródło s(t) --> kanał H --> wejście odbiornika r(t) --> odbiornik R --> obserwacja y(t)
                                  ^                                      ^
                               zakłócenia                          szum, filtracja,
                                                                    próbkowanie, AGC
```

W wariancie liniowym `y(t) = R[H[s(t)] + n_c(t)] + n_r(t)`, lecz rzeczywiste `H` i `R` mogą być nieliniowe, zależne od czasu i sprzężone ze źródłem. Zmiana geometrii trajektorii obserwowanej `y(t)` może być skutkiem zmiany źródła, kanału, odbiornika albo ich interakcji. Bez dodatkowych założeń **rozdział przyczyn może być nieidentyfikowalny**: różne pary `(s,H,R)` mogą wytwarzać to samo `y`.

## Konsekwencja interpretacyjna

- „Informacja sygnału” musi być zawsze indeksowana przez **punkt pomiaru, odbiornik, rozdzielczość, pasmo, skalę czasu i model szumu**.
- Krzywizna, skręt i entropia obserwacji nie są automatycznie niezmiennikami generatora.
- Zdolność detekcji zmiany nie przesądza, czy zmiana zaszła w źródle, czy w torze obserwacji.
- „Cząstka informacji” nie może być uznana za własność źródła na podstawie pojedynczego kanału odbioru.

## Macierz eksperymentów rozdzielających

| Wariant | Generator | Kanał | Odbiornik | Co testujemy |
|---|---|---|---|---|
| G | zmienny | stały | stały | Wrażliwość na zmianę źródła |
| H | stały | zmienny | stały | Fałszywe przypisanie zmiany kanału źródłu |
| R | stały | stały | zmienny | Fałszywe przypisanie zmiany odbiornika źródłu |
| GH | zmienny | zmienny | stały | Rozdzielanie źródła i kanału |
| GR | zmienny | stały | zmienny | Rozdzielanie źródła i odbiornika |
| ALL | zmienny | zmienny | zmienny | Granice identyfikowalności |

Zmiany kanału: filtr dolnoprzepustowy, opóźnienie, pogłos/konwolucja, szum. Zmiany odbiornika: gain/AGC, kwantyzacja, obcięcie amplitudy, dryft zegara, zmiana próbkowania. Kontrola: niezależny pomiar sygnału `s(t)` przed kanałem oraz, jeśli możliwe, `r(t)` przed odbiornikiem.

## Hipotezy

- **H-G:** geometryczne cechy wykrywają zmianę generatora przy ustalonym kanale i odbiorniku.
- **H-R:** zmiana samego odbiornika może imitować „zdarzenie informacyjne” w `y(t)`.
- **H-ID:** przy dodatkowym kanale referencyjnym lub kalibracji toru da się poprawić przypisanie źródła zmiany względem analizy pojedynczego `y(t)`.

## Warunki testowania

1. Przed testem ustalić osobne etykiety: **zmiana źródła**, **zmiana kanału**, **zmiana odbiornika**, **brak zmiany**, oraz możliwość **nierozstrzygalne**.
2. Wykorzystać niezależne sesje i konfiguracje toru; nie mieszać okien z jednego przebiegu między train i test.
3. Raportować macierz pomyłek z naciskiem na błędne przypisanie zdarzenia do generatora.
4. Porównać analizę jednego odbiornika, dwóch niezależnych odbiorników i pomiaru referencyjnego.
5. Jeżeli różne przyczyny dają nierozróżnialne obserwacje, raportować **nieidentyfikowalność**, nie wymuszać klasyfikacji.

## Powiązanie z Chronoprocesem

Trzeba rozróżnić czas źródła `t_s`, czas propagacji `t_h` i czas/próbkowanie odbiornika `t_r`. Zgodność czasowa jest hipotezą kalibracyjną, nie danym faktem. Zmiana geometrii przy reparametryzacji czasu może być artefaktem zegara odbiornika.

## Następny krok

Przed wykonaniem testu końcowego dopisać do protokołu syntetycznego kontrolę G/H/R i wskazać, czy podstawowym celem jest wykrywanie zmiany w **obserwacji**, czy identyfikacja jej **źródła**. Obecny pilot AR(1) testuje tylko pierwszy cel przy ustalonym torze i nie rozstrzyga drugiego.
