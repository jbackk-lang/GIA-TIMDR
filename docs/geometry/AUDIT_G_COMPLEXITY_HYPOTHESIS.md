# Audyt trzech propozycji po wyniku mostu łożyskowego: aksjomat jednorodności, "G-complexity", nowy most

> Użytkownik zaproponował (2026-09-15, po `RESULT_REAL_SEISMIC_NOISE_
> ROBUSTNESS.md`): (1) sformalizować "jednorodność regionu
> pozytywnego" jako nowy aksjomat metodologiczny w Logic Core, (2)
> nazwać `winding`/`crossing`/`phase_winding` nowym obiektem
> matematycznym "G-complexity" (globalna złożoność geometryczna,
> niezależna od torsji/topologii/kurtozy/impulsowości/lokalnej
> nieregularności), (3) zbudować nowy most M/S↔G-complexity. Ten
> dokument to trzy tanie kontrole wykonane PRZED formalizacją
> którejkolwiek z tych propozycji — zgodnie z zasadą "nie promuj do
> aksjomatu na podstawie n=2".

## Kontrola 1: czy winding/crossing/phase_winding to jeden obiekt?

Korelacja Spearmana między trzema metrykami na 96 realnych segmentach
łożyskowych (normal + 3 defekty, okno=64, bez szumu):

```
winding   vs crossing:       rho=+0.843  p=5.0e-27
winding   vs phase_winding:  rho=+0.929  p=1.7e-42
crossing  vs phase_winding:  rho=+0.834  p=4.6e-26
```

**Silnie potwierdzone**: to jest jeden, wspólny sygnał, nie trzy
niezależne, przypadkowo zbieżne proxy. Ta część hipotezy użytkownika
jest dobrze uzasadniona.

## Kontrola 2: czy jednorodność regionu pozytywnego to realny, izolowany efekt przyczynowy?

Test w IZOLACJI: ta sama domena (łożyska, `ir_0021` vs `normal`,
okno=64, σ=0,0), ale region pozytywny SZTUCZNIE zanieczyszczony
rosnącym udziałem okien zdrowych (`mix_frac`), symulując heterogeniczność
(analogia do "impuls + wygaszanie" w sejsmice) BEZ zmiany domeny:

```
mix_frac  winding(r)  crossing(r)  phase_winding(r)  passed
0.00      1.000       1.000        1.000             wszystkie TAK
0.25      0.781       0.888        0.743             wszystkie TAK
0.50      0.610       0.608        0.534             wszystkie TAK
0.75      0.233       0.289        0.202             wszystkie NIE
```

**Potwierdzone empirycznie, w kontrolowany sposób** (nie tylko przez
porównanie dwóch różnych domen jak poprzednio) — rosnąca
heterogeniczność regionu pozytywnego monotonicznie degraduje rozmiar
efektu, w TEJ SAMEJ domenie. To silniejszy dowód niż n=2 porównanie
łożysk vs sejsmiki.

**Ale ważne zastrzeżenie o mechanizmie, żeby nie przereklamować**: to
jest oczekiwany, ogólny efekt statystyczny testu Manna-Whitneya —
"rozcieńczenie" próby testowej próbkami z rozkładu tła zawsze redukuje
moc/rozmiar efektu, dla DOWOLNEJ metryki różnicującej klasy, nie tylko
dla tych trzech. To NIE jest nowe odkrycie geometryczne specyficzne
dla TIMDR — to jest własność samego testu statystycznego. Wniosek
praktyczny (jednorodność regionu pozytywnego jest WYMOGIEM
projektowym dla wiarygodnego mostu) jest słuszny i wart zapisania —
ale jako **regułę protokołu/metodologii** (obok istniejących reguł w
skill §2, jak kontrola mocy czy korekta Bonferroniego), NIE jako nowy
aksjomat gałęzi geometrycznej G — to nie jest twierdzenie o geometrii,
to jest twierdzenie o statystyce testowania.

## Kontrola 3: czy to NIE jest kurtoza/impulsowość ani znana "globalna złożoność" (entropia widmowa)?

Dwie dodatkowe klasyczne cechy (obok kurtozy z poprzedniego audytu),
policzone PO tej samej normalizacji `(x-mean)/std`, na TEJ SAMEJ siatce
3 defekty × 2 okna × 5 sigm (30 komórek):

```
crest_factor (max|x_znormalizowane|):  21/30 -- podobne do kurtozy (22/30)
spectral_entropy (entropia Shannona widma mocy):  27/30 -- BLISKO wyniku
    winding/crossing/phase_winding (30/30)
```

Na pierwszy rzut oka `spectral_entropy` wygląda niebezpiecznie blisko
— to JEST dokładnie klasyczna, dobrze znana formalizacja "globalnej
złożoności sygnału" (entropia widmowa, używana w analizie sygnałów od
dekad), więc gdyby korelowała silnie z `winding`/`crossing`/
`phase_winding`, hipoteza "G-complexity" sprowadzałaby się do
przemalowanej entropii widmowej. **Sprawdzone wprost**:

```
winding        vs spectral_entropy: rho=-0.023  p=0.83  (brak korelacji)
crossing       vs spectral_entropy: rho=+0.250  p=0.014 (slaba)
phase_winding  vs spectral_entropy: rho=+0.010  p=0.92  (brak korelacji)

winding        vs kurtoza: rho=+0.222  p=0.030  (slaba)
crossing       vs kurtoza: rho=+0.120  p=0.25   (brak, nieistotna)
phase_winding  vs kurtoza: rho=+0.217  p=0.034  (slaba)
```

**Kluczowy, precyzyjny wniosek**: `winding`/`crossing`/`phase_winding`
NIE są przemalowaną kurtozą ANI przemalowaną entropią widmową — mimo
że entropia widmowa ma PODOBNĄ moc klasyfikacyjną (27/30 vs 30/30), to
jest praktycznie NIESKORELOWANA z naszą rodziną (|rho|<0,25 we
wszystkich sześciu porównaniach). **To jest ważne rozróżnienie
metodologiczne**: podobna moc klasyfikacyjna NIE oznacza pomiaru tej
samej wielkości — dwie różne, prawie niezależne cechy sygnału mogą
osobno nieść informację o tym samym zjawisku fizycznym (uszkodzeniu
łożyska), nie kolidując ze sobą.

## Werdykt — co jest uzasadnione, a co przedwczesne

1. **Reguła jednorodności regionu pozytywnego**: TAK, zapisać —
   ale jako regułę protokołu (`docs/theory/PROTOCOL.md` w
   TIMDR-Math-Formalism, obok istniejących 9 reguł anty-
   numerologicznych), nie jako aksjomat gałęzi G. Mechanizm jest
   statystyczny (rozcieńczenie próby), nie geometryczny.
2. **"G-complexity" jako nazwany, sformalizowany obiekt matematyczny
   gałęzi G**: JESZCZE NIE. Mamy dobry dowód, że `winding`/`crossing`/
   `phase_winding` mierzą coś WSPÓLNEGO (kontrola 1) i coś INNEGO niż
   kurtoza i entropia widmowa (kontrola 3) — ale to są dopiero DWIE
   odrzucone alternatywy klasyczne, nie wyczerpujące przeszukanie.
   Lista użytkownika "nie jest to torsja/topologia/kurtoza/
   sinusoidalność/impulsowość/lokalna nieregularność" jest częściowo
   nieuzasadniona: "sinusoidalność" i "lokalna nieregularność" nigdy
   nie zostały przetestowane jako osobne metryki kontrolne, tylko
   założone z dyskusji o entropii w serii syntetycznej. Przed
   formalizacją nazwy i promocją do nowej gałęzi potrzeba: (a) więcej
   klasycznych baseline'ów (autokorelacja, widmo obwiedni/envelope
   spectrum — klasyczny standard wibrodiagnostyki łożysk, permutation
   entropy), (b) powtórzenia korelacji na danych sejsmicznych (czy ten
   sam brak korelacji z kurtozą/entropią widmową utrzymuje się w innej
   domenie).
3. **Nowy most M/S↔"G-complexity"**: rozsądny NASTĘPNY krok
   eksploracyjny, ale bez zakładania z góry, że mierzymy już
   scharakteryzowany, nazwany obiekt — to dalej jest eksploracja
   nieznanego, nie testowanie znanej definicji.
