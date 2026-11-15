# TIMDR — surowy sygnał, lokalne trójki, top-8

Eksperyment: 1200 walidacyjnych i 1800 testowych przebiegów; trzy właściwe pary MIN–MAX i trzy silne fałszywe pary, szum σ=0.16, brakujący blok 8–17 próbek, nieliniowy zegar, 12 zaszumionych znaczników kalibracyjnych.

| Metryka | Walidacja | Test |
|---|---:|---:|
| Pokrycie detekcji | 93.33% | 95.50% |
| Trafność top-1 (warunkowa) | 71.16% | 72.89% |
| Trafność ważonego top-8 (warunkowa) | 71.07% | 72.77% |
| Właściwy zestaw zdarzeń top-1 | 51.88% | 50.84% |
| Właściwy zestaw zdarzeń top-8 | 59.20% | 57.77% |

Na walidacji brak progu osiągającego 75%, 80% lub 85% trafności przy minimum 50 zaakceptowanych przykładach. Ranking wykorzystuje znane z generatora odstępy 30/60, więc wyniki nie dowodzą generalizacji. Klasa oznacza układ zdarzeń, nie niezależną przyszłość. Porównanie z poprzednim eksperymentem na gotowych znacznikach nie jest kontrolowanym porównaniem tego samego generatora.

Następny test: rozdzielić niewykrycie właściwych zdarzeń od odrzucenia ich przez ranking hipotez.