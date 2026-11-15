# TIMDR — geometryczny filtr relacji trójek, 2026-11-14

Uruchomiony skrypt: `geometry_filter_test.py`; seed 202611140825. N=2400, trening 1600, test 600. Cztery identyczne trójki przyczynowe o odstępach będących permutacją [9,16,25] próbek; osiem zakłócających. Oscylator q[t+1]=2r cos(w)q[t]-r²q[t-1]+u[t], r=.975, w=.31. Cel: stan po 12 próbkach, szum σ=.035.

Filtr przegląda 495 czwórek i minimalizuje błąd posortowanych odstępów względem **znanego wzorca [9,16,25]**. Następnie HistGradientBoostingRegressor(max_iter=160,max_leaf_nodes=15,l2_regularization=3) przewiduje stan.

| Wybór | R² | MAE |
|---|---:|---:|
| Losowy | .07213 | .73795 |
| Amplituda (remis: pierwsze 4) | .07826 | .72249 |
| Geometryczny | **.73588** | **.35015** |
| Oracle | .84437 | .25240 |

Średni odzysk właściwych zdarzeń 96.083%, dokładna czwórka 85.667%. **Ograniczenie krytyczne**: wzorzec odstępów został przekazany filtrowi; nie jest to samodzielne odkrywanie geometrii. Trójki są zadane, nie wykrywane. Jeden generator, seed, brak CI i testów nowych wzorców. Kod i stdout dostępne jako lokalne pliki rozmowy.