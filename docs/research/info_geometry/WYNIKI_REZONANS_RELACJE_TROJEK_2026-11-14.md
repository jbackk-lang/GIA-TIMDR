# TIMDR — rezonans i relacje trójek (2026-11-14)

Uruchomiony lokalnie skrypt `resonance_triplets.py` (seed 202611140805), 4200 trajektorii, 2400 trening, 600 pominiętych, 1200 test. Trzy lokalne impulsy MIN–MAX Δt=3, odstępy (18,38) lub (38,18). Rezonator q[t+1]=2r cos(ω)q[t]-r²q[t-1]+max(u[t],0), r~U(.94,.985), ω~U(.14,.36). Sonda 24 próbek swobodnego wygaszania, szum .08, cel po 24 krokach z szumem .06. Szum obserwacji historii .12. Automatyczna detekcja trójek find_peaks. Ridge(alpha=5) i HGB(max_iter=90,max_leaf_nodes=12,l2_regularization=5).

| Cechy | Ridge R² | HGB R² |
|---|---:|---:|
| Same odstępy | -.00014 | -.00014 |
| Trójki+odstępy | .00004 | -.04794 |
| Sonda 1 | .00004 | .05467 |
| Sonda 2 | .01067 | .08908 |
| Sonda 8 | .45011 | .67123 |
| Sonda 24 | .96325 | .96627 |
| Sonda 2+odstępy | .01025 | .13074 |
| Sonda 8+odstępy | .45024 | .67313 |
| Sonda 24+odstępy | .96324 | .96586 |
| Sonda 24+trójki+odstępy | .96314 | .96609 |
| Sonda 24+estymator AR2 | .96351 | .96598 |
| Sonda 24+oracle r,ω | .96411 | .96907 |
| Surowa historia | -.02504 | -.04770 |
| Surowa historia+sonda 24 | .96164 | .96293 |

Detekcja 99.917%; SD celu .49454.

**Sparowany test kolejności**: 1500 par z tymi samymi r,ω i przesunięciem; tylko zamiana (18,38)↔(38,18). Średnia różnica -0.024288, średnia wartość bezwzględna .196088, RMS .377340; 46.267% różnic dodatnich. RMS różnicy według częstotliwości: ω=.14–.21 n456 RMS .599835; .21–.28 n481 RMS .300504; .28–.36 n563 RMS .103855. Zależność nie jest uniwersalnym prawem rezonansu, lecz wynikiem tych parametrów i momentu pomiaru.

**Wnioski:** relacje dodają wartość przy krótkiej sondzie (HGB R² .089→.131 dla 2 próbek), przy 24 próbkach nie dodają. Zmienna faza i rezonans wpływają na to, jak historia zdarzeń zapisuje się w przyszłym stanie. To syntetyczny mechanizm, nie dowód fizycznej sprawczości informacji. Naiwna estymacja ω z szumnej sondy miała MAE .17896, więc nie można twierdzić, że odzyskano ω. Nie badano periodycznego wymuszenia dopasowanego do częstotliwości własnej; to osobny następny test. Pełny wykonywalny kod i wyniki dostępne jako pliki rozmowy.