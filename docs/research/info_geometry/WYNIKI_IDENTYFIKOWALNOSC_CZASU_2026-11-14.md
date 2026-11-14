# Test identyfikowalności czasu obiektu i obserwatora — 2026-11-14

**Status:** wykonany lokalnie eksperyment konstrukcyjny, bez danych rzeczywistych. Nie jest to dowód ontologiczny ani pełna walidacja TIMDR.

## Dwa mechanizmy, ta sama obserwacja

Czas obserwatora `t∈[0,1]`, 1001 próbek; `f₀=8 Hz`, `β=0.30`, `ψ(t)=t+(β/2)t²`.

- **A (zmiana źródła):** zegar identycznościowy, `y_A(t)=sin(2π f₀ ψ(t))`; faza źródła przyspiesza w czasie obserwatora.
- **B (zmiana mapy czasu):** `x_B(τ)=sin(2π f₀ τ)` o stałej częstotliwości w czasie obiektu; `τ=ψ(t)`; `y_B(t)=x_B(ψ(t))`.

**Tożsamość algebraiczna:** `y_A(t)≡y_B(t)`. Nie istnieje detektor, który na podstawie samego `y(t)` odróżni te mechanizmy bez dodatkowych założeń. To obejmuje wszystkie cechy MIN/MAX i wszystkie widma obliczone z tego samego `y`.

## Wynik wykonania

```text
N 1001
signal_max_abs_difference 0
minmax_A -0.9999999108608927 0.9999858456341979
minmax_B -0.9999999108608927 0.9999858456341979
reference_rate_A_first_last 1.0 1.0
reference_rate_B_first_last 1.0001499999999999 1.2998499999998792
reference_based_A CLOCK_IDENTITY reference_based_B CLOCK_WARP
PASS: observational equivalence; independent clock distinguishes clock warp
```

Wariant A ma referencję czasu obiektu `τ=t`, wariant B `τ=ψ(t)`. Różnicowy estymator `Δτ/Δt` rozróżnia referencje, ponieważ w A wynosi 1, a w B rośnie do ok. 1.3. Kod pokazuje wykrycie *zmiany zegara* w B; w A identyfikacja „source chirp” wymaga dodatkowo modelu referencyjnego źródła (np. wiedzy, że nie jest stałym oscylatorem). Nazwa `CLOCK_IDENTITY` w wyniku A jest zamierzona.

**Ważne:** referencja jest w tym eksperymencie dostarczona bez szumu i niezależnie od sygnału. Nie wyprowadzamy jej z samego przebiegu, co byłoby błędnym kołem. Jeśli oba zegary mają wspólny dryft lub nie istnieje referencja czasu obiektu, rozdzielenie może być niemożliwe.

## Wniosek dla MIN–MAX–CZAS i Chronoprocesu

Sama trójka `(MIN,MAX,t_obs)` nie może identyfikować mechanizmu, skoro nawet pełne `y(t)` nie może. Trzecia cecha czasu może stać się diagnostyczna, gdy reprezentuje **niezależnie zmierzoną relację** `Δτ/Δt` (lub inną jasno zdefiniowaną wielkość), a nie czas odczytany wyłącznie z tego samego sygnału. Nie jest to uniwersalny dowód, że czas stanowi dodatkową niezależną informację: pokazuje rolę dodatkowego pomiaru.

## Kolejny test

Dodać szum i dryft obu zegarów, nieznane `f₀`, dwie sesje, niezależny zegar referencyjny, fałszywe alarmy i decyzję `UNKNOWN`. Raportować identyfikowalność, nie tylko trafność klasyfikacji. Nie utożsamiać zmiany czasu obiektu z dylatacją relatywistyczną bez modelu fizycznego.

Kod: `clock_identifiability.py`.
