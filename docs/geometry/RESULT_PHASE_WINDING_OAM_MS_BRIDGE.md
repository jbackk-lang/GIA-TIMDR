# Wynik: winding fazy (Hilbert, inspirowane OAM fotonu) jako most M/S↔K

> Streszczenie `PREREG_PHASE_WINDING_OAM_MS_BRIDGE.md`. Wynik
> uruchomienia siatki zamrożonej w tamtym dokumencie, bez modyfikacji
> definicji metryki po zobaczeniu wyniku. Kod: `core/phase_winding_
> oam_ms_bridge.py`. Data: 2026-09-15.

## Wynik surowy (10 komórek: 2 okna × 5 poziomów szumu)

```
 okno  sigma  passed      pos_p    pos_r  pos_r_lbl      neg_p    neg_r  degen
  300   0.00   False  1.212e-12    1.000       duży  1.212e-12   -1.000    TAK
  300   0.10   False     0.6735   -0.064  pomijalny     0.6843    0.062
  300   0.30   False     0.5493   -0.091  pomijalny     0.7731    0.044
  300   0.50   False     0.3403   -0.144       mały     0.5493    0.091
  300   1.00   False     0.8883    0.022  pomijalny     0.7618   -0.047
   64   0.00   False  1.212e-12    1.000       duży  1.212e-12   -1.000    TAK
   64   0.10   False     0.9823   -0.004  pomijalny     0.9587   -0.009
   64   0.30   False     0.7731   -0.044  pomijalny     0.9117   -0.018
   64   0.50   False     0.7394   -0.051  pomijalny     0.8534    0.029
   64   1.00   False     0.9587    0.009  pomijalny     0.6735    0.064

PRZESZŁO: 0/10 komórek siatki.
```

## Wniosek — 0/10, ale INNY tryb porażki niż poprzednie cztery

W przeciwieństwie do torsji/crossing (kierunek odwrócony) i winding-po-
-trajektorii/homologii (niestabilne, czasem odwrócone) — tu efekt jest
po prostu **praktycznie zerowy wszędzie** (poza zdegenerowanym
`sigma=0`): wszystkie `p` duże (0,34–0,98), rozmiary efektu pomijalne
lub małe, bez systematycznego kierunku w żadną stronę. To jest czysty
brak rozróżnialności, nie mylący fałszywy sygnał.

## Diagnoza — sprawdzona bezpośrednio na surowych wartościach metryki

Wyciągnięto 10 przykładowych wartości metryki per grupa (okno=300,
sigma=0,1 i 0,5) zamiast tylko patrzeć na wynik testu:

```
oczekiwane w1*N/(2π) = 47,75  (N=300, w1=1,0)

sigma=0,1:
  pozytywna (2 częst.): 47,6  47,6  47,7  47,6  47,8  47,6  47,5  47,6  47,8  47,7
  negatywna A (szum):   41,7  49,8  47,0  46,5  48,9  48,0  45,8  50,1  49,8  43,9
  negatywna B (1 częst.):47,7  47,7  47,7  47,7  47,7  47,7  47,7  47,7  47,7  47,7
```

**Znaleziono jasny mechanizm**: `negatywna B` (czysta częstotliwość
`w1`) jest niemal dokładnie stała na wartości teoretycznej
`w1·N/(2π)=47,75` — zgodnie z przewidywaniem z sekcji 3
pre-rejestracji. ALE `pozytywna` (suma `sin(w1·t)+0,5·sin(w2·t+φ)`)
jest PRAKTYCZNIE IDENTYCZNA z `negatywną B` — bo `w1` ma większą
amplitudę (1,0) niż `w2` (0,5), więc całkowita akumulacja fazy w oknie
jest zdominowana przez składową `w1`, a druga częstotliwość ledwo
zaburza sumę. **Winding fazy Hilberta liczy w praktyce „ile cykli
dominującej częstotliwości", nie „czy sygnał ma genuine strukturę
wieloskładnikową"** — więc z definicji nie odróżnia kontroli
pozytywnej od negatywnej B, niezależnie od poziomu szumu.

Dodatkowo (częściowo zgodnie z przewidywaniem sekcji 3, częściowo nie):
`negatywna A` (czysty szum) ma rzeczywiście WYŻSZĄ wariancję
(41,7–50,1) niż obie pozostałe grupy (przewidziane poprawnie —
błądzenie fazowe szumu jest mniej systematyczne), ALE jej ŚREDNIA
wypada w tym samym zakresie co sygnał strukturalny (~47), nie wyraźnie
niżej, jak zakładało nieformalne oczekiwanie — więc mimo wyższej
wariancji, rozkłady się w większości nakładają i test Manna-Whitneya
nie ma się na czym oprzeć.

## Co to oznacza dla dalszej pracy

- **Metryka odrzucona w tej postaci** — nie dlatego, że mechanizm
  (systematyczna akumulacja fazy) był złym pomysłem, tylko dlatego, że
  KONKRETNA operacjonalizacja (winding CAŁEGO sygnału złożonego)
  jest, jak się okazuje, praktycznie ślepa na obecność drugiej
  częstotliwości przy nierównych amplitudach — zmierzono to wprost, nie
  zgadnięto.
- To NIE jest ten sam mechanizm porażki co w poprzednich czterech
  próbach (tam: szum wygrywał entropią). Tu: sam sygnał pozytywny
  okazał się nieodróżnialny od kontroli negatywnej B z powodu
  matematycznej własności superpozycji częstotliwości o różnych
  amplitudach — inna, nowa informacja, wcześniej niezaobserwowana.
- Otwarta, NIE podjęta teraz ścieżka: gdyby ktoś chciał kontynuować w
  tym kierunku, naturalną poprawką (WYMAGAJĄCĄ własnej pre-rejestracji,
  nie retuningu tej) byłoby liczenie winding OSOBNO dla poszczególnych
  pasm częstotliwości (np. filtracja pasmowoprzepustowa przed
  Hilbertem) zamiast dla całego sygnału naraz — ale to jest już inny,
  bardziej złożony most, nie poprawka do tego.
- Piąty kandydat zamyka na tym etapie serię prób mostu M/S↔topologia/K
  przez pojedynczy skalar ekstrahowany z okna sygnału — wszystkie pięć
  (torsja, winding-trajektorii, crossing, homologia, winding fazy) dało
  wynik odrzucający, każdy z innej, konkretnej, zdiagnozowanej
  przyczyny, nie z jednego uniwersalnego błędu.
