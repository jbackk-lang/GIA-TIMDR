# TIMDR — impuls diagnostyczny: pamięć kontra wymuszenie (2026-11-14)

## Protokół
6000 syntetycznych układów, po 2000 bez zmiany, ze zmianą α, ze zmianą u. z[t+1]=αz[t]+u+p[t], α0~U(.78,.93), u0~U(-.05,.05), z0~U(-.5,.5); |Δα|~U(.055,.12), |Δu|~U(.035,.09). Dwie sparowane odpowiedzi **tego samego układu z identycznego stanu**: bez impulsu oraz z p[0]=0.7. 16 kroków, szum σ=.005,.02,.05. Pierwsze 3000 przykładów walidacyjnych do wyboru progów, ostatnie 3000 testowych; seed 20261114. Wspólne wymuszenie znika w różnicy d[k+1]=αd[k]. OLS na d[1:7] daje α; u szacowane z trajektorii bez impulsu. Pasywny punkt odniesienia: OLS z pojedynczej trajektorii i osobno zaszumiona kalibracja α0,u0.

## Zmierzone wyniki
| Szum | Trafność pasywna | Trafność impulsowa | MAE α impuls | MAE α pasywnie |
|---|---:|---:|---:|---:|
| .005 | 71.90% | 99.47% | .0028 | .0867 |
| .020 | 50.80% | 66.97% | .0116 | .1577 |
| .050 | 43.43% | 42.70% | .0313 | .2880 |

Macierze pomyłek metody impulsowej, klasy [brak, α, u]:
- σ=.005: [[972,1,9],[0,1018,0],[6,0,994]]
- σ=.020: [[613,144,225],[192,721,105],[274,51,675]]
- σ=.050: [[407,268,307],[325,444,249],[344,226,430]]

## Wnioski i ograniczenia
Kontrolowany impuls może poprawić rozpoznawanie mechanizmu, jeśli istnieje możliwość wykonania **dwóch powtarzalnych pomiarów przy identycznym stanie początkowym i wymuszeniu**. To bardzo mocne założenie; bez niego różnica odpowiedzi nie usuwa u. Przy największym szumie nie ma poprawy. Pasywny baseline jest heurystyczny, nie optymalny. To syntetyczna identyfikacja układu, a nie odkrycie autonomicznej siły informacji. W tym podteście nie badano automatycznej detekcji trójek MIN–MAX–Δt.

Kod do pobrania z rozmowy: `diagnostic_pulse.py`. Następny krok: pojedyncza ciągła trajektoria z randomizowanymi impulsami bez resetowania stanu i porównanie przy tym samym budżecie pomiarowym.