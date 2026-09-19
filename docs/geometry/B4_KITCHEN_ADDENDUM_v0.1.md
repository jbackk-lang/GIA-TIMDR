# B4-Kitchen v0.1 — addendum wykonawcze

Ten dokument zamraża parametry pierwszego przebiegu **przed** odczytem jego
wyniku. Obowiązuje wyłącznie dla `CMU_KITCHEN_S13_BROWNIE_v0.1` i odwołuje
się do B3-Kitchen v0.1 oraz `kitchen_triangulation.json`.

## Wejście

- Geometria: rekordy `1..82219` z `brownie_1.V.global`; rekord `0` jest
  wykluczonym AMC frame 0, a `82220` nie ma źródłowego `T_(i+1)`.
- META Q: `Q_i = RMSE` surowych próbek PCM z `AudioTrack.wav` w przedziale
  `[ceil((T_i-T_audio_start)f_s), ceil((T_(i+1)-T_audio_start)f_s))`.
- Geometria: dla każdej klatki `H_i` jest średnią skończonych wartości H
  istniejącego dyskretnego operatora Weingartena dla zamrożonego czworościanu.
- Bloki: kolejno, rozłącznie, po 50 próbek; ostatni blok może być krótszy.

## Statystyka

W każdym bloku i dla obu śladów stosuje się tę samą zamrożoną funkcję:

```text
Lambda(x) = std(x, ddof=0) / (std(x, ddof=0) + abs(mean(x)) + 1e-9)
```

Test główny to dwustronny Spearman `rho(Lambda_G, Lambda_META,disp)`.
Wartość p jest dwustronną permutacyjną p-wartością dla `abs(rho)`, z 10 000
permutacji i generatorem `numpy.default_rng(20260919)`:

```text
p = (1 + count(abs(rho_perm) >= abs(rho_observed))) / 10001
```

Próg wynosi `alpha = 0.05`.

## Kontrole implementacyjne

Są wykonywane tą samą funkcją Spearmana i tym samym testem permutacyjnym,
przed raporowaniem wyniku głównego.

- (+) dwa identyczne monotoniczne wektory długości 1 645, ze stałym seedem
  `20260919`; musi dać `p < 0.05`.
- (-) dwa niezależne szeregi AR(1), długości 1 645, `phi=0.8`, seedy
  `20260917` i `20260918`; musi dać `p >= 0.05`.

Kontrole sprawdzają implementację testu, nie są drugą analizą danych Kitchen.

## Werdykt

- **SUPPORTED**: obie kontrole przechodzą i `p < 0.05`.
- **NOT SUPPORTED**: obie kontrole przechodzą i `p >= 0.05`.
- **INCONCLUSIVE**: dane są nieważne albo dowolna kontrola nie przechodzi.

Nie są dozwolone kolejne przebiegi z innym seedem, oknem, mikrofonem,
triangulacją, metodą Q, orientacją hipotezy ani filtrowaniem klatek.
