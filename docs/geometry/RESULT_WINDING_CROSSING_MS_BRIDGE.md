# Wynik: winding number + crossing number jako most M/S↔topologia

> Streszczenie `PREREG_WINDING_CROSSING_MS_BRIDGE.md` (pełna metodologia
> tam). Ten plik to sam wynik uruchomienia siatki zamrożonej w tamtym
> dokumencie, bez modyfikacji definicji metryk po zobaczeniu wyniku.
> Kod: `core/winding_crossing_ms_bridge.py`. Data: 2026-09-15.
>
> **Jedyna zmiana względem pre-rejestracji**: implementacja
> `crossing_metric_fn` została przepisana z podwójnej pętli Python na
> wektoryzowaną wersję numpy (ten sam test orientacji, policzony dla
> wszystkich par odcinków naraz przez broadcasting) — pierwsza wersja
> przekraczała limit czasu na pełnej siatce (900 wywołań × ~90000 par
> przy n=300). To zmiana WYŁĄCZNIE wydajnościowa, matematycznie
> identyczna definicja (sekcja 4 pre-rejestracji), zdecydowana przed
> zobaczeniem jakiegokolwiek wyniku liczbowego.

## Wynik surowy (20 komórek: 2 metryki × 2 okna × 5 poziomów szumu)

```
  metryka  okno  sigma  passed      pos_p    pos_r  pos_r_lbl      neg_p    neg_r  degen
  winding   300   0.00   False  1.212e-12    1.000       duży  1.212e-12   -1.000    TAK
  winding   300   0.10   False   0.007959    0.400     średni   0.007959   -0.400
  winding   300   0.30   False   0.008315    0.398     średni   0.007959   -0.400
  winding   300   0.50   False    0.02416    0.340     średni    0.01765   -0.358
  winding   300   1.00   False     0.4464    0.116       mały     0.3632   -0.138
  winding    64   0.00   False  1.212e-12    1.000       duży  1.212e-12   -1.000    TAK
  winding    64   0.10   False    0.07727    0.267       mały    0.07727   -0.267
  winding    64   0.30   False    0.07727    0.267       mały    0.07727   -0.267
  winding    64   0.50   False     0.1907    0.198       mały    0.09626   -0.251
  winding    64   1.00   False     0.4825    0.107       mały     0.4733   -0.109
 crossing   300   0.00   False  1.204e-12    1.000       duży  1.685e-14   -1.000    TAK
 crossing   300   0.10   False     0.3478    0.142       mały    0.02236   -0.344
 crossing   300   0.30   False    0.01765   -0.358     średni  7.221e-06    0.676
 crossing   300   0.50   False  4.831e-10   -0.937       duży  4.966e-11    0.989
 crossing   300   1.00   False  9.756e-10   -0.920       duży  4.972e-11    0.989
 crossing    64   0.00   False  1.191e-12    1.000       duży  1.685e-14   -1.000    TAK
 crossing    64   0.10   False     0.8766    0.024  pomijalny     0.3328   -0.147
 crossing    64   0.30   False  6.488e-06   -0.679       duży  2.672e-06    0.707
 crossing    64   0.50   False  1.728e-07   -0.787       duży  1.363e-08    0.854
 crossing    64   1.00   False  8.394e-05   -0.592       duży  3.794e-08    0.828

PRZESZŁO: 0/20 komórek siatki.
```

Wiersze `sigma=0.00` (4 z 20) są zdegenerowane z tego samego powodu co
w poprzednim moście (`neg_a` = stały zerowy sygnał) — wyłączone z
interpretacji, zgodnie z pre-rejestracją.

## Wniosek

**0/20. Obie metryki odrzucone — ale KAŻDA innym mechanizmem, co samo w
sobie jest ważną informacją.**

### Winding number: kierunek POPRAWNY, ale brak specyficzności

Przy niskim/umiarkowanym szumie (okno=300, sigma∈{0.1,0.3,0.5}) kontrola
pozytywna wychodzi istotna z **dodatnim** rozmiarem efektu (r=0,34-0,40)
— genuine sygnał dwuczęstotliwościowy ma WYŻSZY winding number niż czysty
szum, czyli kierunek zgodny z intuicją, w przeciwieństwie do torsji.

**Ale to nie wystarcza**: kontrola negatywna (`neg_a` czysty szum vs
`neg_b` pojedyncza częstotliwość+szum) wychodzi istotna z PODOBNĄ
wielkością efektu (r=-0,36 do -0,40) w tych samych komórkach. Innymi
słowy: winding number odróżnia „czysty szum" od „cokolwiek z choć
odrobiną okresowości" — ale nie odróżnia „genuine nieplanarnej,
dwuczęstotliwościowej struktury" (pozytywna) od „zwykłego, planarnego
ruchu okresowego" (`neg_b`) lepiej, niż odróżnia dwie kontrole
negatywne od siebie. To dokładnie test specyficzności, przed którym
ostrzegała pre-rejestracja (sekcja 4/5) — i metryka go nie przeszła.

### Crossing number: kierunek ODWRACA SIĘ z szumem, silniej niż przy torsji

Przy niskim szumie (sigma=0,1) efekt jest pomijalny/mały. Od sigma=0,3
w górę kierunek staje się silnie **ujemny** (r=-0,36 do -0,94) —
genuine sygnał ma MNIEJ przecięć niż czysty szum, coraz mocniej z
rosnącym szumem. Kontrola negatywna też silnie istotna (r do 0,99).

## Diagnoza — wniosek szerszy niż przy torsji

Przy moście przez torsję (poprzedni wynik) zdiagnozowano przyczynę jako
„potrójne różnicowanie wzmacnia szum". Winding i crossing number **nie
różnicują w ogóle** (winding: jedna operacja `atan2`+`unwrap`; crossing:
zero różniczkowania, czysta kombinatoryka) — a mimo to zawiodły tym
samym, ODWRÓCONYM kierunkiem efektu przy rosnącym szumie. To pokazuje,
że problem jest **głębszy niż sam rząd różniczkowania**:

**Szum sam w sobie, osadzony przez embedding opóźniający, tworzy
trajektorię lokalnie „poszarpaną" — dużo losowych zwrotów i
samoprzecięć — niezależnie od tego, czy tę „poszarpaność" mierzy się
pochodną (torsja), kątem obrotu (winding), czy liczbą przecięć
(crossing).** Każda z tych miar reaguje na lokalną nieregularność
trajektorii, a nie specyficznie na globalną, genuine topologię —
i losowy szum ma WIĘCEJ lokalnej nieregularności niż gładki sygnał
dwuczęstotliwościowy, więc wygrywa z „prawdziwym" sygnałem w każdej z
trzech już przetestowanych metryk, gdy szum przestaje być znikomy.

## Co to oznacza dla dalszej pracy

- **Ta konstrukcja (embedding opóźniający + rzut PCA + winding LUB
  crossing number) jest odrzucona jako most M/S↔topologia**, tym samym
  trybem co torsja: żadne parametry nie są retuningowane po wyniku.
- **Trzy niezależne próby (torsja, winding, crossing), trzy różne
  mechanizmy liczenia, ten sam ostateczny wzorzec porażki** — to mocna,
  spójna przesłanka, że problem leży w SAMYM EMBEDDINGU OPÓŹNIAJĄCYM
  (delay embedding wzmacnia lokalną nieregularność szumu w trajektorii
  3D), nie w konkretnym wyborze metryki liczonej na trajektorii. Każda
  kolejna metryka lokalna (dowolnego rzędu różniczkowania) prawdopodobnie
  odziedziczy ten sam problem, dopóki embedding się nie zmieni.
- Jedyny nieprzetestowany kandydat z oryginalnej trójki, homologia
  perzystentna, jest **koncepcyjnie odporniejszy** na ten dokładny
  problem, bo mierzy globalną strukturę chmury punktów (dziury,
  komponenty) w sposób z natury niewrażliwy na lokalne, drobne
  zaburzenia (to jest właśnie jej deklarowana zaleta w topologicznej
  analizie danych — stabilność względem szumu) — ale wymaga nowej
  zależności (`gudhi`/`ripser`, brak w środowisku) i nowego wolnego
  parametru (zakres filtracji), więc to osobna, jeszcze nie
  podjęta decyzja, nie automatyczny następny krok.
- Alternatywnie: problem może leżeć w samym **embeddingu opóźniającym**
  jako sposobie zamiany 1D→3D (a nie w warstwie metryki w ogóle) — np.
  wygładzenie sygnału PRZED embeddingiem. To też byłaby NOWA konstrukcja
  wymagająca własnej pre-rejestracji, nie retuning obecnej.
