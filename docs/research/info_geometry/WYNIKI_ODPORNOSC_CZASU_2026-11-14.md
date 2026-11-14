# Odporność definicji CZAS na zmianę zegara — 2026-11-14

**Status:** rzeczywiście wykonany syntetyczny eksperyment obliczeniowy. Bez predykcji przyszłego stanu; to test niezmienniczości reprezentacji.

## Protokół
3000 niezależnych losowań par różnych indeksów ekstremów z zakresu 5..95 w oknie 101 próbek na każdy rodzaj zegara. Kierunek kolejności losowy. Ziarno 20261114. Zegar pierwotny `t∈[0,100]`.

Zmiany czasu: (1) `f(t)=c+t`; (2) `f(t)=c+s t`; (3) `f(t)=c+100s(t/100)^p`. `c~U(-100,100)`, `s=exp(U(-1.2,1.2))`, `p=exp(U(-1.2,1.2))`. Wszystkie są ściśle rosnące.

Porównane cechy: `Δt=t_max−t_min`; `sgn(Δt)`; `Δt/T`, `T=t_end−t_start`. Błąd `Δt` mierzony jako `|Δt_transformed−Δt_original|/100`, a błąd `Δt/T` jako różnica bezwzględna. Nie symulowano zaszumionego wyznaczania ekstremów.

## Wynik uruchomienia
```text
offset mean_abs_delta_error_window_units 0.0 sign_flips 0 mean_abs_normalized_error 0.0
affine mean_abs_delta_error_window_units 0.209 sign_flips 0 mean_abs_normalized_error 0.0
nonlinear mean_abs_delta_error_window_units 0.1926 sign_flips 0 mean_abs_normalized_error 0.0618
```

## Dowód niezmienniczości i granice
Dla dowolnej ściśle rosnącej mapy `f`, `sgn(f(t_max)−f(t_min))=sgn(t_max−t_min)`. Dla afinicznej `f(t)=a t+b`, `a>0`, iloraz `(f(t_max)−f(t_min))/(f(t_end)−f(t_start))` jest równy pierwotnemu `Δt/T`. Surowe `Δt` zachowuje się jedynie dla przesunięcia (`a=1`). W ogólnej nieliniowej mapie `Δt/T` nie jest niezmiennicze.

Wniosek: **odporność nie jest tożsama z ilością informacji predykcyjnej**. Znak zachowuje jedynie kolejność, a odstęp zachowuje dodatkową informację o odległości czasowej. Nie wykazano, że jedna z trzech reprezentacji najlepiej przewiduje przyszłość. Wszystkie testy zachowują kolejność i nie uwzględniają błędów detekcji ekstremów.

## Następny eksperyment
Predykcja przyszłego parametru zależnego od odległości zdarzeń, a nie tylko kolejności; porównanie `sgn(Δt)`, `Δt`, `Δt/T` przy przesunięciach, skalowaniu, nieliniowym warp i szumie lokalizacji ekstremów, z kontrolą negatywną.
