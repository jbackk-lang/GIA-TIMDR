# TIMDR — relacje trójek, pamięć i interwencja (2026-11-14)

6000 symulacji, 4000 trening, 2000 test; seed 20261114. Trzy identyczne trójki (-1,+1,3), lokalne minima w [8,26,64] albo [8,46,64]. Odstępy (18,38) albo (38,18). Stan początkowy z=0; dynamika z[t+1]=.97 z[t]+max(x[t],0), przyszłość y=z[90]+N(0,.025). Kontrola resetu pamięci: y_reset=N(0,.025). Ridge(alpha=.01).

| Cechy | R² naturalnie | R² po resecie |
|---|---:|---:|
| Trójki | -.00030 | -.00013 |
| Uporządkowane odstępy | .87123 | -.00015 |
| Nieuporządkowane odstępy | -.00030 | -.00013 |
| Trójki + odstępy | .87123 | -.00015 |

RMSE naturalne: trójki .07305, relacje .02621. Średni stan z[90]: klasa 0 .765401, klasa 1 .900307; różnica .134906. Średni efekt usunięcia całej pamięci .832873 (nie należy mylić go z efektem przestawienia odstępów).

Wniosek: w tym generatorze relacje kolejności wpływają na przyszłość poprzez zaprogramowany stan pamięci. Nie jest to odkrycie fizycznej siły informacji. Kontrole są celowo mocne, ale generator zna mechanizm i nie uwzględnia szumu wejścia, losowych przesunięć, automatycznej detekcji ani porównania z surowym przebiegiem.