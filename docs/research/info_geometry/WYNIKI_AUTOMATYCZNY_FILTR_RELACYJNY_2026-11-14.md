# TIMDR — automatyczny filtr relacyjny, 2026-11-14

Wykonany eksperyment: 5000 procesów, trening 3200, test 1200; seed 202611140822. Każdy proces zawiera 12 identycznych trójek (-1,+1,0.05 s): 4 pobudzają oscylator, 8 stanowi zakłócenia. Odstępy czterech zdarzeń przyczynowych to permutacja (9,16,25). Model wybiera stałe 4 indeksy spośród 12 na podstawie pięciokrotnej walidacji krzyżowej wyłącznie na treningu, a następnie testuje Ridge i HistGradientBoostingRegressor.

| Cechy | R² |
|---|---:|
| Same trójki, Ridge | -0.00217 |
| Wszystkie odstępy, Ridge | 0.02322 |
| Wszystkie odstępy posortowane, Ridge | 0.00006 |
| Automatycznie wybrane 4 pozycje, Ridge | 0.01436 |
| Automatycznie wybrane 4 pozycje, HGB | 0.02797 |
| Wszystkie odstępy, HGB | 0.23065 |
| Oracle 4 zdarzenia, Ridge | 0.35339 |
| Oracle 4 zdarzenia, HGB | 0.99567 |
| Znana dynamika | 0.99568 |

Wybrane pozycje (indeksowane od zera): (1,4,7,9); CV R²=0.02270. **Wniosek negatywny**: filtr wybierający stałe indeksy nie odnajduje prawidłowych zdarzeń przyczynowych. Relacje prawdziwych zdarzeń pozwalają na skuteczną prognozę, ale są podane oracle. Nie jest to ogólny test filtrów adaptacyjnych, ponieważ filtr nie może wybrać różnych indeksów w różnych procesach. Generator syntetyczny, jeden seed, brak CI. Kod i stdout dostępne lokalnie.