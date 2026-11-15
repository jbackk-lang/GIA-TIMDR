# TIMDR — dynamiczna pamięć relacji z interwencją resetu (2026-11-14)

Wykonany eksperyment: `dynamic_relational_memory.py`, seed 202611140803, 6000 przebiegów, 3500 trening, 1000 pominiętych, 1500 testowych. Trzy lokalne trójki (-1,+1,3), minima w [8,26,64] albo [8,46,64]. Zatem uporządkowane odstępy (18,38) lub (38,18), nieuporządkowany zbiór identyczny. Ukryta pamięć jest liczona **dynamicznie z surowych impulsów**, bez wstrzykiwania etykiety: h[t+1]=.965*h[t]+max(x[t],0), h[0]=0. Drugi, obserwowalny stan z~N(.5,.07), niezależny od historii, sonda [z+N(0,.018), αz+N(0,.018)] z α~U(.82,.94). Cel y=.6z+.8h+N(0,.035). Interwencja resetu ukrytej pamięci y_reset=.6z+N(0,.035). Ridge(alpha=.01).

| Reprezentacja | R² naturalne | R² reset |
|---|---:|---:|
| Sonda | .31949 | .59374 |
| Trójki | -.00029 | -.00147 |
| Nieuporządkowane odstępy | -.00029 | -.00147 |
| Uporządkowane odstępy | .40944 | -.00210 |
| Sonda + odstępy | .72999 | .59332 |
| Sonda + trójki + odstępy | .72999 | .59332 |
| Surowy przebieg | .40944 | -.00210 |
| Sonda + surowy przebieg | .72999 | .59332 |

Średni ukryty stan h: (18,38) 0.592918, (38,18) 0.707043. Różnica efektu na y: -0.0913. Średnia różnica y-y_reset: 0.520557. **Uwaga: reset pamięci zmienia także rozkład celu, więc R² między kolumnami nie jest bezpośrednio porównywalne jako bezwzględna poprawa.** Najważniejsza jest różnica wartości dodatkowej relacji względem sondy w obrębie każdej kolumny.

Ograniczenia: to wciąż syntetyczny liniowy filtr pamięci z ustalonym współczynnikiem .965, bez szumu wejścia i bez automatycznej detekcji trójek. Obserwowalny stan z jest niezależnie losowany, a nie sprzężony z dynamiką h. Surowy przebieg osiąga identyczny wynik jak relacje; brak dowodu przewagi kompresji TIMDR. Wniosek dotyczy mechanizmu zaprogramowanego w symulacji, nie nowej fizycznej siły informacji. Następny test: zmienna stała pamięci, szum, automatyczne wykrywanie lokalnych trójek, silny surowy baseline, kontrola interwencji przy tej samej skali celu.