# TIMDR — relacje trójek przy nieznanym współczynniku pamięci i szumie (2026-11-14)

## Metoda
Uruchomiony skrypt: `relational_unknown_memory_noise.py`. 6000 niezależnych przebiegów długości 96, seed 202611140756. Trzy pary impulsów (-amp,+amp) w odstępie 3 próbek, amp~U(.8,1.2). Odstępy między parami (18,38) lub (38,18), wspólne losowe przesunięcie 5..12. Pamięć z[t+1]=α z[t]+max(x[t],0), α~U(.82,.94). Cel y=z[96]+N(0,.035). Sygnał obserwowany x+N(0,.12). Detekcja automatyczna scipy.signal.find_peaks(height=.55,distance=9,prominence=.45), trzy najwyższe dodatnie maksima i odpowiadające minima w poprzednich 6 próbkach. Trening 3500, test 1500, indeksy 3500..4499 niewykorzystane. Ridge(alpha=10), HistGradientBoostingRegressor(max_iter=130,max_leaf_nodes=12,l2_regularization=5). Podane są wszystkie wyniki, bez wyboru hiperparametrów na teście.

## Wyniki z wykonania
Detekcja trzech zdarzeń: 99.333% testu. Średnie y klas 0 i 1: .052534 oraz .060355.

| Cechy | Ridge R² | HGB R² |
|---|---:|---:|
| Globalna trójka | .0016 | -.0356 |
| Lokalne trójki | .0025 | -.0542 |
| Nieuporządkowane odstępy | -.0006 | -.0006 |
| Uporządkowane odstępy | .0025 | .0025 |
| Trójki + uporządkowane odstępy | .0053 | -.0528 |
| Trójki + odstępy + prawdziwe α | .2846 | .6769 |
| Surowy przebieg | .0133 | -.0090 |
| Surowy przebieg + prawdziwe α | .2994 | .7103 |

## Wniosek
W tym generatorze nieznany parametr pamięci dominuje prognozę. Odzyskanie samych relacji zdarzeń nie wystarcza. Prawdziwe α jako kontrola oracle daje znaczny wzrost R², ale nie jest dostępne w zastosowaniu. Surowy przebieg z α daje lepszą prognozę niż relacje trójek z α.

## Ważne ograniczenia
W poprzednim eksperymencie α było stałe, a teraz zmienia się między trajektoriami; to inne zadanie. Tutaj klasy różnią się porządkiem odstępów, ale ich wpływ na cel jest słaby względem zmienności α i szumu przyszłości. Brak jawnego resetu pamięci i brak aktywnej sondy w tym teście. Wartość α jest podana jedynie jako oracle, więc jej wykorzystanie nie dowodzi możliwości estymacji. Nie testowano fizycznej sprawczości informacji. Przed kolejnym testem należy zbadać, czy dodatkowa, niezależna sonda stanu pamięci może przywrócić przewidywalność relacji.

## Kod
Lokalny plik `/mnt/data/timdr_experiment/relational_unknown_memory_noise.py`.