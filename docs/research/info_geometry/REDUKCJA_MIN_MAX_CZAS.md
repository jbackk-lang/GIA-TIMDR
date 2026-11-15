# Redukcja do trzech cech: MIN, MAX, CZAS

**2026-11-14. Status:** doprecyzowanie autora i propozycja formalizacji; nie nowy aksjomat TIMDR.

Autor wyjaśnił, że **wynik ma dokładnie trzy cechy: minimum, maksimum i czas**. Poprzednia interpretacja jako trzy dowolne współrzędne projekcji 9D→3D była zbyt ogólna.

## Operator okienny

Dla sygnału skalarnego `x:T→R` i okien `W_k⊂T`:

```text
m_k = min{x(t):t∈W_k}
M_k = max{x(t):t∈W_k}
τ_k = znacznik czasu okna W_k
R_W[x](k) = (m_k,M_k,τ_k)
```

Wariant strumieniowy może używać czasu końca okna `τ_k=max W_k`, by nie korzystać z przyszłych próbek. Znaczniki czasu powinny mieć jawny zegar i jednostki. Dla sygnału wielokanałowego trzeba dopiero ustalić, czy `min/max` liczymy per kanał, na normie, czy na wielkości skalarnej zdefiniowanej przez TIMDR. **Nie zakładać automatycznie, że dziewięć oznacza dziewięć kanałów.**

Trajektoria `k↦R_W[x](k)` żyje w `R³`, ale jest **krzywą 1D**, nie powierzchnią. Sama nie uzasadnia operatora kształtu gałęzi G ani metafory rurki. Aby otrzymać powierzchnię `Γ(t,s)`, trzeba jawnie zdefiniować dodatkowy parametr rodziny `s` i sprawdzić regularność.

## Rozróżnienie: wynik i widmo

`R_W` jest stratnym operatorem. Nawet w jednym oknie różne przebiegi (i różne widma) mogą mieć identyczne `min`, `max`, `τ`. Zatem widmo `R_W[x]` nie jest w ogólności widmem oryginalnego `x`. Jeśli zadaniem jest badanie oryginalnego spektrum, zachować dostęp do `x(t)` i oddzielnie analizować K; jeśli badamy spektrum ewolucji ekstremów, jasno nazwać to widmem trajektorii MIN/MAX.

## Przykład kontrujący odwracalność

W jednym oknie próbkowanym w równych odstępach: `x=[-1,1,-1,1]` i `y=[-1,-1,1,1]`. Oba mają `min=-1`, `max=1` i ten sam czas końca okna, lecz różną strukturę oscylacji i inne DFT. Po redukcji `R_W[x]=R_W[y]`.

## Następne decyzje

1. Czy czas to koniec okna, czas minimum, czas maksimum czy czas zdarzenia? **Jedna** współrzędna czasu nie koduje obu chwil ekstremów; można zachować je jako metadane, jeśli potrzebne.
2. Jak powstaje wejściowe „9” i co jest jednostką sygnału? Bez tej definicji nie należy pisać o dowiedzionej redukcji 9→3.
3. Czy „rurka” oznacza trajektorię trójek `(m,M,τ)`, czy faktyczną powierzchnię wokół niej?
4. Jakie niezmienniki spektralne redukcja powinna zachować? Trzeba je wskazać i testować, zamiast zakładać pełną bezstratność.

## Eksperyment

Porównać detekcję zmian na surowym `x` oraz `R_W[x]` w scenariuszach, w których min/max/czas pozostają identyczne, a częstotliwość/faza się zmienia. Raportować także przypadki nierozstrzygalne, nie przypisywać ich automatycznie do generatora.

Źródła zgodności: `docs/theory/TIMDR_Branch_Specification.md` i `docs/theory/TIMDR_Chronoprocess.md`.
