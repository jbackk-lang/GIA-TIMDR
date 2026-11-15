# TIMDR — zmienna pamięć, szum i automatyczne lokalne trójki (2026-11-14)

Uruchomiono `dynamic_relations_robust.py`, seed 202611140804; 4500 przebiegów, 2700 trening, 600 niewykorzystanych, 1200 test. Trzy lokalne pary MIN–MAX, odstępy (18,38) albo (38,18), przesunięcie 7–14. Dynamika ukrytej pamięci h[t+1]=αh[t]+max(x[t],0), α~U(.94,.985); szum historii .14, sondy niezależnego stanu z .02. Cel y=.6z+.8h+N(0,.04), reset h=0. Detekcja scipy.find_peaks, Ridge(alpha=1) i HGB(90 iteracji, 12 liści, regularyzacja 5).

| Cechy | Naturalne Ridge R² | Naturalne HGB R² | Reset Ridge R² |
|---|---:|---:|---:|
| Sonda | .04208 | .00330 | .55485 |
| Trójki | .01530 | -.02498 | -.00435 |
| Nieuporządkowane odstępy | -.00003 | -.00003 | -.00147 |
| Uporządkowane odstępy | .03309 | .03309 | -.00716 |
| Sonda + odstępy | .07490 | .03273 | .55227 |
| Sonda + trójki + odstępy | .08871 | .04424 | .55237 |
| Surowy sygnał + sonda | .05011 | .03440 | .54228 |
| Sonda + odstępy + prawdziwe α | .50191 | .91675 | .55222 |

Detekcja trzech zdarzeń: 98.583%. Przemieszane odstępy+sonda: R²=.04275 wobec .04208 samej sondy. Po resecie relacje nie poprawiają prognozy. Reset zmienia rozkład celu, dlatego nie porównujemy bezpośrednio R² między naturalną dynamiką a resetem.

Ograniczenia: model syntetyczny, α losowe między przebiegami, sonda mierzy osobny stan z, nie ukryte h. Oracle α jest niedostępne w rzeczywistym zastosowaniu. Brak CI, surowy baseline zależny od modelu, nie wykazano fizycznej siły informacji. Kod i pełne wyniki udostępnione jako pliki rozmowy.