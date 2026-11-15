# TIMDR — rzadka sonda pamięci a relacje trójek (2026-11-14)

Wykonany skrypt: `sparse_probe_relations.py`. 6000 syntetycznych trajektorii, 3500 trening, 1000 niewykorzystanych, 1500 test; seed 202611140800. Trzy pary impulsów MIN–MAX o lokalnym Δt=3; odstępy między parami (18,38) lub (38,18); przesunięcie 5–12. α~U(.82,.94), stan z[t+1]=αz[t]+max(x[t],0). Obserwacja historii z szumem σ=.12, sonda k=0..7 z szumem σ=.018, cel zawsze z[96]α^8+N(0,.015). Detekcja scipy.find_peaks. Ridge(alpha=1) i HGB(max_iter=90,max_leaf_nodes=10,l2_regularization=5). Bez strojenia na teście.

## R² na zbiorze testowym

| k | Ridge: sonda | Ridge: sonda+odstępy | HGB: sonda | HGB: sonda+odstępy | HGB: sonda+trójki+odstępy |
|---:|---:|---:|---:|---:|---:|
| 1 | .75866 | .75787 | .79003 | .79023 | .78360 |
| 2 | .79127 | .79072 | .80107 | .80157 | .79794 |
| 4 | .81043 | .81005 | .81483 | .81528 | .81360 |
| 8 | .82279 | .82242 | .82328 | .82221 | .82144 |

Ridge z sondą+surowym sygnałem: k=1 .75318, k=2 .78687, k=4 .80588, k=8 .81752. Ridge z sondą+trójkami+odstępami: .75777, .79090, .81024, .82239. Kontrola przemieszanych odstępów: k=1 .75863, k=2 .79112 (Ridge). Detekcja kompletu zdarzeń 99.133%; SD celu .037265.

## Interpretacja

Relacje trójek nie wnoszą w tym generatorze wyraźnej wartości predykcyjnej ponad sondę, nawet gdy dostępna jest jedna lub dwie próbki. Niewielkie różnice HGB (do .0005) nie uzasadniają wniosku o rzeczywistej przewadze; nie wyliczano przedziałów ufności. Nie dowodzi to braku użyteczności TIMDR w innych dynamikach. Sonda jest bardzo blisko celu, co uprzywilejowuje bezpośredni pomiar stanu. Cel jest zaszumiony, a pamięć zaprogramowana w generatorze. Następny krok: test, w którym sonda i relacje zawierają rzeczywiście komplementarną informację, ale nie zakładać przewagi z góry; kontrolować przeciek informacji i porównać z surowym sygnałem.
