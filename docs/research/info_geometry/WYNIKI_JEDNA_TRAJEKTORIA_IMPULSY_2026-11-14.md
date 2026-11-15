# TIMDR — jedna trajektoria, losowe impulsy, bez resetu (2026-11-14)

## Protokół
9000 trajektorii długości 72. Model z[t+1]=(alpha+delta_alpha I[t>=36]) z[t]+u+delta_u I[t>=36]+p[t]. Trzy zrównoważone klasy: brak zmiany, skok alpha, skok u. alpha U(.80,.93), u U(-.05,.05), |delta_alpha| U(.055,.105), |delta_u| U(.035,.075). Dwanaście impulsów +/- .35 w losowych chwilach. Jedna trajektoria na próbę, bez resetu. Szum pomiaru sigma .005,.02,.05. Podział 6000 trening, 1500 walidacja, 1500 test; walidacja nieużyta do strojenia. HistGradientBoostingClassifier, 100 iteracji, 12 liści, regularyzacja 3. Cechy z dwóch regresji OLS przed i po znanej chwili 36, przy znanym lub ignorowanym p[t].

## Wyniki wykonania
| Szum | Znane impulsy | Impulsy ignorowane | MAE różnicy alpha | MAE różnicy u |
|---|---:|---:|---:|---:|
| .005 | .9993 | .5073 | .0040 | .0011 |
| .020 | .9807 | .5073 | .0150 | .0042 |
| .050 | .8553 | .4873 | .0463 | .0142 |

Macierze pomyłek dla znanych impulsów, kolejność [brak, zmiana alpha, zmiana u]:
- .005: [[499,0,1],[0,500,0],[0,0,500]]
- .020: [[487,12,1],[16,484,0],[0,0,500]]
- .050: [[430,59,11],[118,367,15],[7,7,486]]

## Interpretacja i ograniczenia
Przy znanym p[t] regresja na z[t+1]-p[t] może oszacować osobno alpha i u w każdym segmencie. Ignorowane impulsy zaburzają regresję. To **nie jest jeszcze kontrolowane porównanie aktywnego pobudzania z bierną obserwacją**: obie kolumny zawierają impulsy, różni się jedynie wiedza o nich. Znana chwila zmiany t=36, znana liniowa postać dynamiki, idealna wiedza o impulsach, brak opóźnienia i nieliniowości. Brak automatycznej detekcji lokalnych trójek MIN–MAX–Delta t; eksperyment dotyczy mechanizmu, nie potwierdzenia nowej fizycznej siły informacji.

## Następny test
Porównać przy tym samym budżecie pomiarowym brak impulsów, znane losowe impulsy i adaptacyjne impulsy. Ukryć chwilę zmiany i dołączyć lokalne trójki do opisu.