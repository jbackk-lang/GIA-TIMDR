# Niepewność zegara i decyzja UNKNOWN — 2026-11-14

**Status:** rzeczywiście wykonany lokalnie test Monte Carlo na syntetycznych znacznikach czasu. To nie jest test pełnego TIMDR.

## Protokół

N=101 znaczników `t=i/100`. Stabilny zegar: `τ=t`; zmiana tempa: `τ=t+0.15t²`. Niezależny szum Gaussa `N(0,σ²)` na znacznikach referencyjnych. Statystyka detekcji: różnica współczynników regresji liniowej `τ(t)` w drugiej i pierwszej połowie. Próg: empiryczny 99. percentyl `|statystyka|` na 300 **oddzielnych** stabilnych przebiegach kalibracyjnych. Test: 300 stabilnych i 300 ze zmianą, nowe ziarna. Decyzja `WARP` tylko gdy statystyka przekracza próg; w przeciwnym razie `UNKNOWN`, a nie automatycznie `SOURCE`.

## Wyniki wykonania

```text
sigma,threshold,false_alarms_300,warp_detected_300,warp_unknown_300
0,0.00000,0,300,0
0.002,0.00728,0,300,0
0.01,0.03640,0,300,0
0.03,0.10920,0,268,32
0.1,0.36401,0,26,274
```

Dla wszystkich pięciu poziomów szumu w tym konkretnym zestawie testowym nie wystąpił fałszywy alarm. Nie znaczy to, że prawdopodobieństwo alarmu jest równe zeru. Próba 300 kalibracji jest mała dla stabilnej estymacji 99. percentyla.

## Granice wnioskowania

- Test korzysta z **niezależnej referencji czasu obiektu**; nie odtwarza jej z obserwowanego sygnału.
- Wariant bez wykrytej zmiany zegara pozostaje `UNKNOWN`: brak dowodu warp nie jest dowodem zmiany źródła.
- Szum dotyczy znaczników czasu, nie kanału sygnałowego. Nie badano jeszcze dryftu wspólnego ani nieznanej synchronizacji.
- Zakładana funkcja zmiany jest gładka i monotoniczna; nie badano skoków ani utraty próbek.
- Eksperyment wspiera operacyjną rolę pomiaru czasu w identyfikowalności mechanizmu, nie uniwersalną ontologiczną tezę o informacji.

## Następny test

Wprowadzić dryft zegara referencyjnego, niezależny trzeci zegar i scenariusze wspólnego dryftu. Raportować macierz pomyłek oraz pokrycie UNKNOWN na sesjach, także przy błędnej specyfikacji modelu.

Kod: `clock_uncertainty_test.py`.
