# TIMDR — niezależna sonda pamięci a relacje lokalnych trójek (2026-11-14)

Uruchomiony kod: `relations_independent_probe.py`. 6000 przebiegów, 3500 trening, 1000 niewykorzystanych, 1500 test. Seed 202611140758. Trzy lokalne pary impulsów MIN–MAX (odstęp 3), porządek odstępów (18,38) albo (38,18), losowe przesunięcie 5–12, amplituda .8–1.2. Pamięć z[t+1]=αz[t]+max(x[t],0), α~U(.82,.94). Szum surowego przebiegu .12. Automatyczne find_peaks; lokalne trójki i uporządkowane odstępy maksimów. Osiem sond p[k]=z[96]α^k+N(0,.018), k=0..7. Cel y=z[96]α^8+N(0,.015). Ridge(alpha=1), HistGradientBoosting(max_iter=100,max_leaf_nodes=12,l2_regularization=5).

| Cechy | Ridge R² | HGB R² |
|---|---:|---:|
| Lokalne trójki | .00286 | -.01500 |
| Uporządkowane relacje | .00132 | .00092 |
| Trójki + relacje | .00436 | -.01588 |
| Sama sonda | **.81557** | .81190 |
| Trójki + relacje + sonda | .81530 | .81188 |
| Surowy sygnał | -.02121 | -.02657 |
| Surowy sygnał + sonda | .80930 | .80944 |
| Sonda przemieszana w teście | -.86195 | -.91431 |
| Relacje + prawdziwe α (oracle) | .57830 | .78817 |

Komplet zdarzeń wykryto w 99.6% testu. SD celu .03676. Wniosek: sonda pamięci przywraca predykcję, relacje trójek nie poprawiają jej ponad sondę w tym generatorze. Kontrola przemieszanej sondy potwierdza zależność predykcyjną, nie przyczynowość. Ograniczenia: sonda mierzy stan blisko celu; generator bez wymuszenia podczas sondy; nie jest to dowód fizycznej siły informacji. Następny test: 1–2 sondy i kontrola przy stałym horyzoncie.