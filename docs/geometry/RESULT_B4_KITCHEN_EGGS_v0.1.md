# Wynik B4-Kitchen Eggs v0.1 (2026-09-19) — SUPPORTED (replika na innym przepisie)

Zgodnie z `B3_KITCHEN_PREREG_EGGS_v0.1.md`, zamrożonym PRZED policzeniem
jakiejkolwiek geometrii/audio z tych danych — łącznie z etykietami ziaren
kontroli negatywnej. Metoda statystyczna (`ar1_effective_n_spearman`) jest
w pełni odziedziczona z `PREREG_B4_KITCHEN_v0.3.md`, bez żadnej zmiany
parametru. Pełny surowy wynik: `B4_KITCHEN_RESULT_EGGS_v0.1.json`.

## To NIE jest replika międzyosobnicza

**Ten sam uczestnik (Subject 13), inny przepis (Eggs zamiast Brownie).**
CMU Kitchen Capture nie udostępnia przekonwertowanego mocapu AMC/ASF dla
żadnego innego uczestnika (zweryfikowane na pełnej tabeli 39 uczestników —
patrz `B3_KITCHEN_PREREG_EGGS_v0.1.md` §0). Ten wynik kontroluje zmienność
PRZEPISU, nie zmienność UCZESTNIKA — nie wolno cytować go jako "replika
niezależna" bez tego zastrzeżenia.

## Wynik surowy

| | Brownie v0.3 (referencja) | Eggs v0.1 (ta replika) |
|---|---|---|
| n_geometry_frames | 82219 | 58507 |
| n_blocks | 1645 | 1171 |
| Kontrola pozytywna | p≈0.0 ✓ | p≈0.0 ✓ |
| Kontrola negatywna | p=0.6763 ✓ | p=0.5602 ✓ |
| `controls.passed` | true | **true** |
| Test główny rho | 0.0708 | **0.1249** |
| Test główny p | 0.0093 | **0.0000396** |
| Werdykt | SUPPORTED | **SUPPORTED** |

## Szczegóły testu głównego

```text
rho = 0.12491405630364222
r1x (autokorelacja lag-1 rang Λ_G)     = 0.5811
r1y (autokorelacja lag-1 rang Λ_META)  = 0.0796
n_eff = 1067.46  (z n=1171)
t = 4.1095
p = 0.0000396
```

## Dlaczego to WZMACNIA, ale nie ZAMYKA sprawy

Dwa niezależne uruchomienia TEJ SAMEJ zamrożonej metody, na dwóch różnych
sesjach nagraniowych (różne przepisy, ten sam uczestnik), obie z
przechodzącymi kontrolami i obie SUPPORTED — to silniejsza podstawa niż
sam wynik Brownie v0.3. W szczególności odpowiada wprost na zastrzeżenie
z `RESULT_B4_KITCHEN_v0.3.md` ("trzecia próba na tych samych danych"):
Eggs to CAŁKOWICIE OSOBNY zbiór danych (inna sesja, inne audio, inna
geometria), więc efekt multiple-comparisons z trzech iteracji metody na
Brownie się tu nie stosuje — to pierwsze i jedyne uruchomienie zamrożonej
metody na danych Eggs.

To, czego wciąż brakuje: **inny uczestnik**. Oba dodatnie wyniki (Brownie,
Eggs) dzielą tego samego człowieka, tę samą kuchnię, ten sam dzień
nagraniowy, ten sam sprzęt. Efekt subjectowo-specyficzny (np. rytm
poruszania się akurat tej osoby, akustyka akurat tej kuchni) pozostaje
niewykluczony. Status pozostaje ten sam co dla Brownie: **NIE ustalone w
sensie międzyosobniczym**, ale teraz z dodatkowym, niezależnym (co do
przepisu) potwierdzeniem.

## Rozmiar efektu

`rho=0.1249` — na granicy małego efektu wg skali rank-biserial z
`timdr-signal-framework` (0.1–0.3 = mały). Większy niż Brownie
(`rho=0.0708`, pomijalny), ale wciąż niewielki w bezwzględnych
kategoriach — istotność statystyczna wspierana też przez duże `n_eff≈1067`.

## Klasyfikacja statusu

Wg słownika w `TIMDR_Branch_Specification.md`: **NIE ustalony
międzyosobniczo, wzmocniony sygnał wewnątrz-osobniczy** (2/2 przepisów
tego samego uczestnika SUPPORTED, zero prób NOT SUPPORTED/INCONCLUSIVE na
świeżych danych). Wciąż nie kwalifikuje się do tieru "częściowo
ustalony" w sensie użytym dla mostów M/S↔G/M/S↔K — brak testu na innym
uczestniku.

## Co dalej (otwarte)

1. Prawdziwa replika międzyosobnicza pozostaje niewykonalna z tego zbioru
   (patrz `B3_KITCHEN_PREREG_EGGS_v0.1.md` §0) bez samodzielnej konwersji
   surowego Vicon innego uczestnika do AMC/ASF.
2. Dwa pozostałe przepisy S13 z gotowym mocapem (Salad, Sandwich) mogłyby
   dać 3/3 albo 4/4 jako dalsze wewnątrz-osobnicze wzmocnienie — wciąż nie
   zastępuje repliki międzyosobniczej.
3. Fizyczna interpretacja różnicy `rho` między przepisami (0.0708 vs
   0.1249) — nieinterpretowana tutaj.

## Status: SUPPORTED (Eggs v0.1) — wewnątrz-osobniczo potwierdzone, międzyosobniczo NIE ustalone
