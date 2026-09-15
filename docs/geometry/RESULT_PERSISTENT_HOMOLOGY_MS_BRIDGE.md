# Wynik: homologia perzystentna (β₁) jako most M/S↔topologia

> Streszczenie `PREREG_PERSISTENT_HOMOLOGY_MS_BRIDGE.md` (pełna
> metodologia tam). Wynik uruchomienia siatki zamrożonej w tamtym
> dokumencie, bez modyfikacji definicji metryki po zobaczeniu wyniku.
> Kod: `core/persistent_homology_ms_bridge.py`. Data: 2026-09-15.

## Wynik surowy (10 komórek: 2 okna × 5 poziomów szumu)

```
 okno  sigma  passed      pos_p    pos_r  pos_r_lbl      neg_p    neg_r  degen
  300   0.00   False  1.212e-12    1.000       duży  1.212e-12   -1.000    TAK
  300   0.10   False   9.26e-09   -0.864       duży   3.02e-11    1.000
  300   0.30   False  7.088e-08   -0.811       duży   3.02e-11    1.000
  300   0.50   False     0.7618   -0.047  pomijalny  2.439e-09    0.898
  300   1.00   False     0.9117   -0.018  pomijalny     0.5395    0.093
   64   0.00   False  1.212e-12    1.000       duży  1.212e-12   -1.000    TAK
   64   0.10    True  2.783e-07    0.773       duży    0.05555    0.289
   64   0.30   False   0.007959    0.400     średni   0.001058    0.493
   64   0.50   False    0.01327    0.373     średni    0.01383    0.371
   64   1.00   False     0.6843    0.062  pomijalny     0.3871    0.131

PRZESZŁO: 1/10 komórek siatki.
```

## Wniosek — 1/10 PRZESZŁO formalnie, ale to NIE jest wynik pozytywny

Jest dokładnie JEDNA komórka, która spełniła zamrożone kryterium
`pipeline.run_controls()`: okno=64, sigma=0,1 (`pos_p=2,8×10⁻⁷`,
`pos_r=+0,77`, duży i we właściwym kierunku; `neg_p=0,056`).

**Ta jedna komórka NIE jest traktowana jako potwierdzony wynik** —
zgodnie z protokołem anty-numerologicznym (zasada 9: pojedynczy,
pozornie pozytywny wynik to trop wymagający replikacji, nie ustalony
fakt) z trzech niezależnych powodów widocznych wprost w tej samej
siatce:

1. **Margines kontroli negatywnej jest cienki**: `neg_p=0,05555` przy
   progu `alpha=0,05` — to przejście o mniej niż jeden promil
   p-wartości od NIE zaliczenia. Przy odrobinę innym ziarnie losowym
   ta komórka najpewniej nie przeszłaby.
2. **Brak replikacji w sąsiednich komórkach tej samej siatki**: przy
   tym samym oknie (64) i sąsiednim poziomie szumu (sigma=0,3) kierunek
   pozostaje poprawny (`r=+0,40`) ale kontrola negatywna WYRAŹNIE
   zawodzi (`neg_p=0,001`). Efekt nie jest stabilny nawet w obrębie
   jednego reżimu rozmiaru okna.
3. **Kierunek ODWRACA SIĘ całkowicie przy oknie=300**: przy
   sigma∈{0,1; 0,3} efekt jest silny, istotny, ale UJEMNY (`r=-0,86`,
   `r=-0,81`) — czysty szum ma WYŻSZĄ całkowitą persystencję H1 niż
   genuine sygnał, dokładnie odwrotnie niż przy oknie=64. Ten sam
   obiekt matematyczny, ta sama metryka, przeciwny kierunek zależnie od
   rozmiaru okna — to jest silna przesłanka niestabilności, nie
   przypadkowego szumu pomiarowego.

Przy najwyższym szumie (sigma=1,0) efekt zanika do pomijalnego w obu
oknach — spójne z poprzednimi dwoma mostami.

## Diagnoza

Homologia perzystentna zachowała się INACZEJ niż torsja/winding/
crossing (nie ten sam, monotoniczny wzorzec „szum zawsze wygrywa") —
to potwierdza, że mechanizm odporności na szum przez persystencję
faktycznie coś zmienia. Ale to, co dostaliśmy, to niestabilność
zależna od rozmiaru okna, nie odporność. Prawdopodobny powód: przy
oknie=300 punktów w przestrzeni embeddingu 3D filtracja
Vietorisa-Ripsa na CZYSTYM SZUMIE (300 losowych punktów, żadnej
struktury czasowej) sama z siebie generuje dużo przypadkowych,
umiarkowanie trwałych „dziur" po prostu z gęstości losowego rozkładu
punktów w przestrzeni (znany efekt w TDA — losowe chmury punktów mają
niezerową, czasem sporą H1 persystencję czysto z geometrii gęstości,
nie z genuine topologii) — przy 300 punktach ta „szumowa" persystencja
dominuje. Przy 64 punktach szum ma mniej okazji do przypadkowego
uformowania trwałych pętli, więc genuine sygnał może chwilowo wygrać —
ale niestabilnie, jak pokazuje brak replikacji w sąsiedniej komórce.

## Co to oznacza dla dalszej pracy

- **Ta konstrukcja (całkowita persystencja H1 na surowym embeddingu
  opóźniającym) NIE jest uznana za działającą** — 1/10 przy cienkim
  marginesie i braku replikacji nie spełnia standardu tego ekosystemu
  (rozmiar próby + replikacja, nie pojedynczy przebieg).
- **Trzy z trzech pierwotnie rozważanych kandydatów (torsja, winding/
  crossing, homologia perzystentna) nie dały wiarygodnego, stabilnego
  mostu M/S↔topologia** przy TEJ konstrukcji embeddingu opóźniającego.
  To domyka pierwotną listę trzech opcji z rozmowy, która zainicjowała
  ten wątek.
- Najciekawszy pojedynczy fakt z całej serii: efekt (gdziekolwiek się
  pojawia) silnie zależy od rozmiaru okna/gęstości punktów, nie tylko
  od poziomu szumu — to sugeruje, że przypadkowa gęstość punktów w
  chmurze losowej (nie tylko amplituda szumu) jest istotnym czynnikiem
  mylącym dla metod topologicznych na tego typu danych — warty
  odnotowania wniosek na przyszłość, gdyby ktoś wracał do tego tematu.
- Świadomie NIE podjęte teraz: dalsze warianty (np. subsampling gęstości
  punktów do stałej wartości niezależnie od okna, inne metryki
  redukcji diagramu persystencji) — to byłyby kolejne nowe konstrukcje
  wymagające własnych pre-rejestracji, nie retuning tej.
