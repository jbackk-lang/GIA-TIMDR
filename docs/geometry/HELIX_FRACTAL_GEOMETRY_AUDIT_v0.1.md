# Audyt geometryczny: helisa a możliwość struktury fraktalnej (v0.1)

**Data:** 2026-11-09  
**Zakres:** pierwszy etap badania — geometria przed analizą liczb i estymacją wymiaru.  
**Status:** wynik analityczny dla HC-01 i dokładnego wzorca BC; hipoteza fraktalna struktury TIMDR pozostaje otwarta.  
**Zasada ciągłości:** dokument rozwija istniejący HELIX-CHAR-01 i program HELIX_TIMDR_RESEARCH_PROGRAM; nie zastępuje ich nowym programem.

## 1. Pytanie

Czy geometria helisy i istniejących konstrukcji modułowych daje matematyczną podstawę do przypuszczenia, że poza rzutem helikalnym występuje organizacja fraktalna?

Na tym etapie nie estymujemy wymiaru fraktalnego z danych. Najpierw sprawdzamy, czy istniejące obiekty mają samopodobieństwo, rekurencję między skalami albo mechanizm kontrakcyjny.

## 2. HC-01: helisa kołowa

Dla
\[
\gamma(t)=(a\cos t,a\sin t,ht),\qquad a>0
\]
krzywizna i torsja Freneta–Serreta są stałe:
\[
\kappa=\frac{a}{a^2+h^2},\qquad
\tau_{FS}=\frac{h}{a^2+h^2}.
\]
W konsekwencji:
\[
\frac{\tau_{FS}}{\kappa}=\frac{h}{a},\qquad
p=2\pi h,\qquad
L_{1\,turn}=2\pi\sqrt{a^2+h^2}.
\]

**Wniosek geometryczny:** HC-01 jest gładką, regularną krzywą o stałej krzywiźnie i stałej torsji. Nie ma w samej definicji hierarchii skal, rozgałęzień ani rekurencji. Jako klasyczna krzywa regularna ma wymiar geometryczny 1. Nie jest przez to fraktalem.

### 2.1. Skalowanie nie jest fraktalnością

Dla jednorodnej homotetii:
\[
(a,h)\mapsto(\lambda a,\lambda h),\quad \lambda>0,
\]
kształt bezwymiarowy pozostaje ten sam, ponieważ \(\eta=h/a\) jest niezmienne. Jednocześnie:
\[
p\mapsto\lambda p,\quad L\mapsto\lambda L,\quad
\kappa\mapsto\kappa/\lambda,\quad
\tau_{FS}\mapsto\tau_{FS}/\lambda.
\]
Jest to zwykła kowariancja względem zmiany jednostki/skali, nie dowód samopodobieństwa fraktalnego. W szczególności nie występuje tu nietrywialna rekurencja ani niecałkowity wymiar.

### 2.2. Projekcje

Rzut HC-01 na płaszczyznę prostopadłą do osi jest okręgiem; rzut na płaszczyznę zawierającą oś jest sinusoidą (zależnie od kierunku rzutu). Są to gładkie obiekty jednowymiarowe. Sama projekcja helisy nie generuje fraktala.

## 3. BC: dokładna tetrahelisa jako konstrukcja modułowa

W repozytorium istnieje dokładna rekurencja odbicia najstarszego wierzchołka czworościanu względem płaszczyzny pozostałych trzech. Dla regularnego czworościanu:
- wszystkie moduły są przystające;
- jeden stały operator śrubowy przenosi każdy wierzchołek na następny;
- wierzchołki leżą na dyskretnym próbkowaniu jednej helisy kołowej HC-01;
- centroidy kolejnych czworościanów również leżą na helisie o tej samej osi i mniejszym promieniu.

Operator śrubowy składa się z obrotu i translacji, czyli jest izometrią: zachowuje odległości i nie kurczy przestrzeni. Nie jest kontrakcją iterowanego układu funkcji. Regularna tetrahelisa BC nie ma więc samoczynnie mechanizmu generującego fraktalną hierarchię skal.

**Ważne ograniczenie:** zbiór samych dyskretnych wierzchołków jest próbką krzywej, a nie ciągłą krzywą ani fraktalnym domknięciem. Łańcuch czworościanów ma stałą skalę modułu. Nie wolno wywodzić fraktalności z samego faktu powtarzania modułów.

## 4. Ogólny czworościan: co już wynika z rekurencji

Kod core/boerdijk_coxeter_tetrahelix.py obsługuje dowolny niekoplanarny czworościan: kolejne czworościany zachowują dokładnie sześć długości krawędzi modułu bazowego. Kod jawnie zastrzega, że nie implikuje to stałej transformacji śrubowej dla dowolnego czworościanu.

Zachowanie kongruencji modułów nie jest jeszcze samopodobieństwem fraktalnym. To zachowanie jednej skali. Dla przypadku ogólnego trzeba najpierw ustalić, czy istnieje stały operator, czy orientacja zmienia się nieregularnie, czy powstaje inna struktura geometryczna. Żaden z tych wariantów nie jest automatycznie fraktalem.

## 5. Co mogłoby dać rzeczywistą podstawę do hipotezy fraktalnej

W ramach istniejących obiektów TIMDR warto rozważyć — bez przyjmowania wyniku — następujące źródła hierarchii skal:

1. **Rekurencyjne moduły:** reguła przejścia zmienia rozmiar lub strukturę modułu według jawnego prawa na kolejnych poziomach.
2. **Zmienna geometria helisy:** promień, skok lub oś zmieniają się według reguły zależnej od skali, a nie tylko od parametru łuku.
3. **Sprzężenie sygnał–geometria:** sygnał aktualizuje geometrię, a odpowiedź wraca jako wejście następnego kroku; dopiero taka pętla mogłaby wytworzyć rekurencję wieloskalową.
4. **Zagnieżdżone projekcje/defekty:** struktura zawiera powtarzalne relacje na kilku poziomach, które przeżywają zmianę rozdzielczości.

To są kandydackie mechanizmy do sprawdzenia, nie ustalenia o TIMDR. W szczególności §37–39 programu helisy wskazuje, że sprzężenie sygnał→stan helisy→odpowiedź nie jest jeszcze zintegrowane; nie należy więc zakładać, że istniejąca pętla już generuje fraktalność.

## 6. Rozstrzygnięcie pierwszego etapu

- **HC-01:** gładka krzywa 1D; brak fraktalności w definicji.
- **Projekcje HC-01:** gładkie krzywe; brak fraktalności wynikającej z rzutu.
- **BC regularny:** dokładna, modułowa konstrukcja śrubowa o stałej skali; nie jest sama przez się fraktalem.
- **BC dla ogólnego czworościanu:** zachowanie kongruencji kolejnych modułów jest zdefiniowane i testowane; globalna struktura wymaga osobnego rozpoznania, ale nie ma jeszcze podstaw do nazwania jej fraktalną.
- **Struktura nadrzędna TIMDR:** status fraktalny UNKNOWN. Nie można go wywnioskować z helisy ani z BC.

Najważniejszy wynik negatywny: prosta helisa i regularna tetrahelisa BC nie dostarczają same z siebie dowodu fraktalności. To zawęża poszukiwanie do ewentualnej struktury rekurencyjnej/wieloskalowej poza samą helisą.

## 7. Następny etap — liczby, bez restartu

Dopiero po tym rozstrzygnięciu geometrycznym przejść do ilościowego porównania na istniejących konstrukcjach:

1. Wyznaczyć dokładne bezwymiarowe parametry HC-01: \(\eta=h/a\), \(a\kappa\), \(a\tau_{FS}\), obrót na krok i przesunięcie osiowe na krok.
2. Zmierzyć zachowanie tych wielkości przy homotetii i zmianie liczby próbek — kontrola, że estymator nie tworzy pozornej skali.
3. Dla BC porównać promień wierzchołków i centroidów, przyrost fazy i osiowy na krok oraz błędy względem ciągłej HC-01.
4. Dla ogólnego czworościanu sprawdzić, czy istnieje stały operator śrubowy i czy odchylenia mają strukturę systematyczną.
5. Dopiero jeśli pojawi się powtarzalność na wielu skalach, wykonać analizę box-counting z zakresem skal, przedziałem niepewności i kontrolami niefraktalnymi.

Nie estymować wymiaru fraktalnego dla HC-01 ani BC regularnego jako głównego wyniku — z góry znana gładka geometria czyniłaby to testem poprawności estymatora, nie odkryciem fraktala.

## 8. Źródła w GIA-TIMDR

- docs/geometry/HELIX_CHARACTERIZATION_PROTOCOL_HC01_v0.1.md
- docs/geometry/BOERDIJK_COXETER_EXACT_REFERENCE_2026-11-09.md
- docs/geometry/COMPARISON_BC_HC01_TIMDR_2026-11-09.md
- core/boerdijk_coxeter_tetrahelix.py
- docs/geometry/HELIX_SIGNAL_RESPONSE_COUPLING_v0.1.md
- docs/theory/HELIX_TIMDR_RESEARCH_PROGRAM.md

**Konkluzja:** geometria HC-01 i BC nie jest fraktalna sama z siebie. Matematycznie interesujący kierunek pozostaje jednak otwarty: sprawdzić, czy szersza struktura TIMDR zawiera niezależny, rekurencyjny lub wieloskalowy mechanizm, którego helisa jest tylko jednym rzutem.


## 9. Liczby dla dokładnego wzorca BC — kontrola ilościowa

Dla dokładnego operatora BC:
\[
\theta=\arccos(-2/3)\approx2.3005239830\ \mathrm{rad}
=131.8103148958^\circ,
\]
\[
a=\frac{3\sqrt6}{5}\approx1.4696938457,\qquad
\Delta z=-\frac{2}{\sqrt5}\approx-0.8944271910.
\]
Ciągły parametr helisy odpowiadającej próbkowaniu BC:
\[
h=\frac{\Delta z}{\theta}\approx-0.3887928131.
\]

| Wielkość | Wartość | Znaczenie |
|---|---:|---|
| \(\eta=h/a\) | \(-0.2645400022\) | bezwymiarowy kształt helisy |
| \(\alpha=\arctan(\eta)\) | \(-14.8175977181^\circ\) | podpisany kąt nachylenia stycznej względem płaszczyzny poprzecznej |
| \(a\kappa=1/(1+\eta^2)\) | \(0.9345956744\) | bezwymiarowa krzywizna |
| \(a\tau_{FS}=\eta/(1+\eta^2)\) | \(-0.2472379417\) | bezwymiarowa, podpisana torsja |
| \(\kappa\) | \(0.6359118106\) | krzywizna w jednostkach odwrotnych do przyjętej długości |
| \(\tau_{FS}\) | \(-0.1682241117\) | podpisana torsja w tych samych jednostkach |
| \(p=2\pi h\) | \(-2.4428572909\) | podpisany skok na pełny obrót |
| \(L_{1\,turn}\) | \(9.5520120273\) | długość jednego pełnego obrotu |

Promień centroidowej helisy jest dokładnie \(r_c=2/5=0.4\), podczas gdy promień helisy wierzchołków wynosi \(r_v=3\sqrt6/5\). Ich stosunek:
\[
\frac{r_c}{r_v}=\frac{\sqrt6}{9}\approx0.2721655270.
\]
To jest dokładna relacja dwóch orbit geometrycznych tej samej konstrukcji BC, nie wymiar fraktalny ani dowód hierarchii nieskończenie wielu skal.

### 9.1. Co te liczby mówią o fraktalności

1. \(\eta\), \(a\kappa\) i \(a\tau_{FS}\) są niezmiennikami jednorodnej zmiany skali HC-01. Potwierdzają, że porównanie należy prowadzić bezwymiarowo.
2. BC ma jeden stały przyrost fazy \(\theta\) i jeden stały przyrost osiowy \(\Delta z\) na krok. To regularność śrubowa, nie skalowanie rekurencyjne.
3. Dwa promienie (wierzchołków i centroidów) nie wystarczają do uznania konstrukcji za wieloskalową: są dwoma wyróżnionymi orbitami o stałym stosunku, a nie rodziną poziomów samopodobieństwa.
4. Wartości liczbowe nie dają podstaw do estymacji niecałkowitego wymiaru. Dla HC-01 znana jest gładka krzywa 1D; dla BC mamy dyskretny łańcuch modułów stałej skali.

**Status liczb:** wartości wynikają analitycznie z dokładnego operatora BC i wzorów HC-01; są kontrolą geometryczną. Nie są pomiarem fraktalności struktury TIMDR.
