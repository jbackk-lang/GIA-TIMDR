# TIMDR — ukryty stan relacyjny komplementarny względem sondy (2026-11-14)

## Metoda
Wykonano `hidden_relational_state.py`, seed 202611140801; 6000 prób, 3500 trening, 1000 pominiętych, 1500 test. Historia: trzy pary MIN–MAX z Δt=3, odstępy (18,38) albo (38,18), losowe przesunięcie 8..14, amplituda .85..1.15, szum .10. Detektor scipy.find_peaks automatycznie identyfikuje zdarzenia. Niezależny od klasy obserwowalny stan z~N(.5,.08), α~U(.82,.94), dwie sondy z+szum i αz+szum, szum sondy .018. **Ukryty stan h jest jawnie zadany przez klasę relacji**: h=.12 dla (18,38), h=-.12 dla (38,18). Cel y=.6z+.8h+N(0,.035). To sztucznie zaprogramowana komplementarność, a nie wynik samoistnej dynamiki.

## Wyniki testowe
| Reprezentacja | Ridge R² | HGB R² |
|---|---:|---:|
| Sama sonda | .18385 | .16978 |
| Same trójki | -.00196 | -.02477 |
| Uporządkowane odstępy | .71590 | .71591 |
| Nieuporządkowane odstępy | -.00031 | -.00030 |
| Sonda + odstępy | **.89760** | .89635 |
| Sonda + trójki + odstępy | .89727 | .89590 |
| Surowy przebieg | .58748 | .69575 |
| Sonda + surowy przebieg | .77316 | .88063 |
| Sonda + przemieszane odstępy | .18372 | nie badano |

Detekcja 100%. Średnia y dla klas 0/1: .39570/.20416. Zadany kontrfaktyczny efekt h na y: +.096 dla klasy 0, -.096 dla klasy 1; różnica .192.

## Interpretacja i krytyczne ograniczenie
To pozytywna kontrola konstrukcyjna: jeżeli istnieje ukryty stan przechowujący informację o relacjach i sonda go nie mierzy, relacje mogą uzupełnić sondę. **Nie wykazano, że relacje same wytworzyły taki stan w naturalnym układzie**: h przypisano bezpośrednio na podstawie etykiety generatora. Nie ma tu równania ewolucji h, dlatego nie można mówić o odkrytej przyczynowości informacji ani o niezależnej fizycznej sile. Kolejny, rozstrzygający test powinien użyć dynamicznie ewoluującego h z kontrolowanym resetem, zamiast bezpośrednio wpisywać etykietę klasy do celu.