# Wynik: chrono_sphere_bridge v0.2 — ODRZUCONY na etapie kontroli syntetycznej (drugi raz, ten sam kierunek)

> Zgodnie z `PREREG_CHRONO_SPHERE_BRIDGE_v0.2.md`: zatrzymanie na
> etapie kontroli, bez dotykania danych CWRU. Uruchomione: 2026-09-22.

## Wynik bramki sanity (c)

Bez zmian względem v0.1 — 100% odrzuconych okien (30/30) na wszystkich
trzech rozmiarach okna. **PASSED**.

## Wynik testu głównego (a: kopnięcia periodyczne, vs b: szum)

| window_size | p | r | mediana (a) kopnięcia | mediana (b) szum | kierunek |
|---|---|---|---|---|---|
| 500 | 3.02e-11 | -1.000 | 0.470 | 0.6628 | odwrotny |
| 1000 | 3.02e-11 | -1.000 | 0.458 | 0.6622 | odwrotny |
| 2000 | 3.02e-11 | -1.000 | 0.454 | 0.6657 | odwrotny |

Mediana (a) wzrosła względem v0.1 (~0.176→~0.46), czyli krótkie,
ciągłe kopnięcia rzeczywiście osłabiły efekt "zamrożenia" — ale wciąż
nie wystarczająco, żeby przekroczyć poziom czystego szumu. Efekt
pozostaje idealnie stabilny (`r=-1.000` na wszystkich trzech oknach),
czyli nie jest szumem próbkowania — jest systematyczny.

## Diagnoza mechanizmu — DRUGI niezależny generator, TEN SAM kierunek błędu

v0.1 (skok trwały) i v0.2 (kopnięcia trójkątne, krótkie, bez płaskiego
szczytu) mają zupełnie inny kształt czasowy, a mimo to dają identyczny
kierunek odchylenia. To wskazuje na przyczynę geometryczną, nie na
niefortunny kształt impulsu:

Gdy jeden kanał (`c_x`) zaczyna dominować nad pozostałymi — niezależnie
od tego, czy przez trwały offset czy przez krótki, symetryczny
impuls — wektor `v(t)` zbliża się do osi `c_x`, a znormalizowany
kierunek `u(t)` SATURUJE: dalszy wzrost `c_x` coraz mniej zmienia już
prawie jednostkowy wektor bliski `(1,0,0)`. W tym samym momencie
`r(t)=‖v(t)‖` jest DUŻE (bo `c_x` dominuje), czyli dokładnie ta chwila
dostaje NAJWYŻSZĄ wagę w średniej ważonej `Ω_win`. Powstaje
systematyczna antykorelacja: chwile o wysokiej wadze `r(t)` to chwile
o NISKIEJ prędkości kątowej (bo kierunek już się nasycił), niezależnie
od tego, jak szybko czy wolno narastało dominujące wychylenie.
Odwrotnie, czysty szum bez dominacji żadnego kanału ma kierunek
"skaczący" swobodnie po oktancie na każdej próbce, z umiarkowanym,
względnie stałym `r(t)` — brak tej antykorelacji, więc ważona średnia
wychodzi wyżej.

**To jest właściwość GEOMETRYCZNA konstrukcji `T_G`/`Ω_win`, nie wada
konkretnego generatora kontrolnego.** Trzeci wariant kształtu impulsu
(np. gaussowski, inna szerokość) prawdopodobnie zawiódłby z tego
samego powodu — dowolne zdarzenie, w którym jeden kanał zaczyna
dominować, będzie saturować kierunek dokładnie wtedy, gdy dostaje
najwyższą wagę.

## Status

**v0.2 ODRZUCONY.** Dwie niezależne, dobrze skontrolowane próby
(różny kształt kontroli pozytywnej) zawiodły w tym samym kierunku, z
tą samą siłą efektu (`r=-1.000`) — spójne z jedną, wspólną przyczyną
geometryczną, nie z przypadkową niefortunną konstrukcją kontroli.
Rekomendacja: NIE próbować v0.3 z kolejnym kształtem impulsu w tej
samej definicji `Ω_win` — diagnoza wskazuje, że zawiodłoby identycznie.
Jeśli wątek sfery ma być kontynuowany, wymaga to zmiany SAMEJ metryki
(np. bez ważenia przez `r(t)`, albo miary opartej na czymś innym niż
prędkość kątowa w chwilach dominacji jednego kanału) — czyli nowej
konstrukcji, nie łatki na `Ω_win`. Kod obu wariantów kontroli
pozytywnej (`make_direction_jump`, `make_periodic_kicks`) zostaje w
`core/chrono_sphere_bridge.py` jako udokumentowana historia, bez
kasowania.
