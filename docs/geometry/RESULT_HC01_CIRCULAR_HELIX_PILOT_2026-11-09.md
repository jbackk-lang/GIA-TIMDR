# HC-01 — raport pilotażowy helisy kołowej

**Data:** 2026-11-09  
**Status:** PILOT ANALITYCZNY + NUMERYCZNY; nie jest to jeszcze walidacja fizyczna ani pełny atlas helisy TIMDR.  
**Kod:** `experiments/helix_characterization/hc01_circular_helix.py`  
**Testy:** `experiments/helix_characterization/tests/test_hc01_circular_helix.py`

## 1. Model i zakres

Badany obiekt:
`r(t)=(a cos t, a sin t, h t)`, z `a=1`, `η=h/a`.

Zastosowano wzory analityczne krzywizny i podpisanej torsji Freneta–Serreta oraz niezależny estymator numeryczny oparty na kolejnych pochodnych wyznaczanych przez `numpy.gradient`. Próbkowanie obejmuje dwa pełne obroty. Do statystyk błędu pominięto osiem próbek z każdego końca.

## 2. Wynik analityczny

| η | κ | τ_FS | τ_FS/κ | skok p | długość jednego obrotu |
|---:|---:|---:|---:|---:|---:|
| -2 | 0.2 | -0.4 | -2 | -4π | 2π√5 |
| -1 | 0.5 | -0.5 | -1 | -2π | 2π√2 |
| -0.5 | 0.8 | -0.4 | -0.5 | -π | π√5 |
| 0 | 1 | 0 | 0 | 0 | 2π |
| 0.5 | 0.8 | 0.4 | 0.5 | π | π√5 |
| 1 | 0.5 | 0.5 | 1 | 2π | 2π√2 |
| 2 | 0.2 | 0.4 | 2 | 4π | 2π√5 |

Dla `η=0` obiekt jest okręgiem, czyli granicznym przypadkiem helisy o zerowym skoku.

## 3. Naturalne ekstremum — co rzeczywiście wynika z matematyki

Bezwymiarowa torsja:
`a τ_FS = η/(1+η²)`.

Jej wartość bezwzględna osiąga maksimum przy `|η|=1`:
- `|a τ_FS| = 1/2`;
- `a κ = 1/2`;
- kąt stycznej względem płaszczyzny poprzecznej wynosi `±45°`;
- skok ma wartość bezwzględną `2πa`;
- długość jednego obrotu wynosi `2πa√2`.

To jest potwierdzony ekstremum bezwymiarowej torsji w rodzinie idealnych helis kołowych. **Nie jest** to dowód punktu kardynalnego TIMDR, progu redukcji, osobliwości ani utraty stabilności. Nie wynika z tego szczególna rola 90°.

## 4. Znak i chiralność

Zmiana `h → -h`:
- zachowuje krzywiznę;
- odwraca znak torsji Freneta;
- odwraca znak skoku i kąta nachylenia;
- zachowuje długość obrotu i wartości bezwzględne wielkości nieorientowanych.

Zatem znak torsji niesie informację o orientacji helisy, której nie wolno usuwać przez zastąpienie `τ_FS` przez `|τ_FS|`. To stwierdzenie dotyczy przyjętej orientacji parametryzacji i konwencji Freneta.

## 5. Kontrola numeryczna dla η=1

Mediana bezwzględnego błędu krzywizny w części wewnętrznej domeny:

| N | błąd κ |
|---:|---:|
| 256 | 2.024e-4 |
| 512 | 5.040e-5 |
| 1024 | 1.257e-5 |
| 2048 | 3.141e-6 |

Błąd krzywizny maleje w przybliżeniu czterokrotnie przy podwojeniu liczby próbek, zgodnie z zachowaniem estymatora drugiego rzędu w tym gładkim przypadku.

Dla torsji błąd jest znacznie mniejszy, ale przy dużej liczbie próbek pojawia się poziom błędu zaokrągleń/odejmowania numerycznego. To ostrzeżenie, że trzecia pochodna wymaga osobnego badania stabilności i nie należy raportować nadmiernej liczby cyfr.

## 6. Wnioski i ograniczenia

1. HC-01 daje kontrolny, dokładnie znany związek między promieniem, skokiem, krzywizną i torsją.
2. Bezwymiarowa torsja ma maksimum przy stosunku skoku parametrycznego do promienia równym co do modułu 1.
3. Lewa i prawa orientacja są rozróżnialne przez znak torsji.
4. Zwykła helisa kołowa jest krzywą otwartą z osią osiową; nie jest zamkniętym węzłem. Jej torsji nie należy utożsamiać ze skrętem topologicznym.
5. Eksperyment nie bada jeszcze samoodległości zwojów, maksymalnego promienia rurki, szumu, deformacji, zmiennego skoku ani osi zakrzywionej.
6. Nie wyprowadzono zastosowania ani przewagi użytkowej. To wymaga kolejnych testów i porównań z geometriami kontrolnymi.

## 7. Następne eksperymenty

- HC-01-P2: pełna walidacja zbieżności i odporności na szum oraz zmianę parametryzacji.
- HC-01-TUBE: odległość między nieprzyległymi fragmentami i maksymalny promień tubularnego otoczenia.
- HC-02: helisa o zmiennym skoku, z porównaniem do lokalnego modelu stałego skoku.
- HC-03: helisa stożkowa / zmienny promień.

**Decyzja:** zachować HC-01 jako matematyczny baseline. Nie przenosić jego ekstremum torsji na ogólną helisę TIMDR bez osobnych pomiarów.


## 8. Reprodukowalność CI

GitHub Actions: **success** — run `42570850539`, commit `9667eebe6085cbbd1b692f584e1075c7d5a3311d`. Testy jednostkowe HC-01, pełny sweep parametrów i zapis artefaktów zakończyły się powodzeniem. Artefakt: `hc01-circular-helix-characterization` (artifact ID `13652688302`).

Pierwsze uruchomienie CI ujawniło błąd ścieżki importu w teście; poprawiono ścieżkę, po czym ponowne uruchomienie przeszło pomyślnie. Nie ukrywamy tej korekty — jest częścią historii reprodukowalności.


## 9. HC-01-TUBE — pilot geometrii tunelu

Dodano `experiments/helix_characterization/hc01_tube.py` i testy `tests/test_hc01_tube.py`. Dla idealnej helisy kołowej badane są dwa niezależne ograniczenia promienia rurkowego otoczenia osi:
- lokalne: promień krzywizny (1/\kappa=(a^2+h^2)/a);
- globalne: połowa odległości pary punktów doubly-critical, gdzie cięciwa jest prostopadła do stycznych w obu końcach.

Dla parametrycznej różnicy (Delta) warunek pary doubly-critical redukuje się do:
`sin(Δ)+(h/a)^2 Δ=0`.
Odległość cięciwy:
`d²=2a²(1-cos Δ)+h²Δ²`.
Kod numerycznie lokalizuje niezerowe pierwiastki na skończonym przedziale kilku obrotów i porównuje połowę najmniejszej znalezionej odległości z lokalnym promieniem krzywizny. Wynik jest numerycznym oszacowaniem dla idealnej osi, nie modelem materiału.

Przykładowe wyniki dla (a=1):
| h/a | lokalny promień krzywizny | globalny półdystans (najmniejszy znaleziony) | ograniczenie |
|---:|---:|---:|---|
| 0.2 | 1.04 | 0.6161 | globalne |
| 0.3 | 1.09 | 0.9018 | globalne |
| 0.4 | 1.16 | 1.1603 | lokalne (1.16) |
| 0.6 | 1.36 | brak niezerowej pary w przeszukanym zakresie | lokalne |
| 1.0 | 2.00 | brak niezerowej pary w przeszukanym zakresie | lokalne |

Interpretacja: przy mniejszym skoku globalne zbliżenie odległych części osi może ograniczać grubość tunelu wcześniej niż lokalna krzywizna. Przy większym skoku w tym badaniu ograniczeniem jest lokalny promień krzywizny. To wynik geometrii standardowej helisy; nie stanowi progu redukcji ani automatycznej własności wszystkich rodzin helikalnych.

**CI:** run `42571021232` zakończony sukcesem. Testy HC-01 i HC-01-TUBE, sweep HC-01 i upload artefaktu przeszły. Link do uruchomienia: https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42571021232

Ograniczenie metody: przeszukiwanie pierwiastków jest numeryczne i ograniczone do zadanej liczby obrotów. Przed publikacją wartości jako ścisłego reach należy wykazać, że nie pominięto globalnie mniejszej pary; w następnym kroku zwiększyć zakres, sprawdzić zbieżność siatki i porównać z niezależnym algorytmem odległości.
