# Trójwęzeł z naprzemiennego znaku sinusoidy (+ − +): hipoteza sygnałowa v0.1

**Data:** 2026-11-09  
**Status:** hipoteza autora do formalizacji i testu; nie jest jeszcze dowodem konstrukcji topologicznego węzła.

## 1. Obserwacja konstrukcyjna

Autor wskazuje sekwencję znaku sygnału:

\[
+\quad -\quad +
\]

czyli trzy kolejne płaty sinusoidy: pierwszy dodatni, drugi ujemny, trzeci dodatni. Trójwęzeł ma powstawać z tej naprzemienności, a nie przez arbitralne rozstawienie trzech helis co 120°.

Ważne: znak płata jest informacją orientacyjną. Nie wolno zastępować sygnału jego wartością bezwzględną, ponieważ wtedy sekwencja \((+,-,+)\) staje się \((+,+,+)\) i znika informacja o odwróceniu środkowego płata.

## 2. Minimalny model sygnału

Dla sygnału bazowego:

\[
s(t)=A\sin(\omega t+\varphi)
\]

wyodrębniamy kolejne płaty między zerami sygnału. Dla trzech kolejnych płatów zapisujemy:

\[
\mathbf{p}=(p_0,p_1,p_2)=(+1,-1,+1).
\]

To jest kod znaków trzech półfal, nie trzy niezależne sinusoidy. Granice płatów są zerami sygnału; punkty ekstremalne są kandydatami na lokalne punkty kardynalne, ale ich status musi wynikać z dalszej geometrii.

## 3. Hipoteza mapowania na trójwęzeł

Każdy płat może generować jedną gałąź / część struktury trójwęzłowej. Znak płata określa orientację lokalnego przebiegu:

\[
\sigma_i=\operatorname{sign}(s(t_i^*)),
\qquad
(\sigma_0,\sigma_1,\sigma_2)=(+1,-1,+1),
\]

gdzie \(t_i^*\) jest ekstremum i-ego płata.

Nie przyjmujemy jeszcze, że trzy płaty są już trzema zamkniętymi komponentami topologicznymi. Aby powstał rzeczywisty węzeł, potrzebna jest mapa łącząca płaty w przestrzeni, z określonymi punktami połączeń, stycznymi, fazą i regułą domknięcia.

Hipoteza robocza: środkowy płat o przeciwnym znaku tworzy odwrócenie orientacji względem dwóch zewnętrznych płatów. To odwrócenie może być kluczowe dla skrętu i ręczności struktury. Należy sprawdzić, czy po osadzeniu w 3D prowadzi do trójwęzła, czy jedynie do trójpłatowej trajektorii.

## 4. Związek z redukcją indukowaną dodawaniem

Łączymy tę hipotezę z sekwencją:
\[
\triangle_3 \to T_4 \xrightarrow{+e_5} \text{próg brzegowy} \to \mathcal R.
\]

Pytanie badawcze: czy operator redukcji po przekroczeniu warunków brzegowych pozostawia trzy płaty sygnału o znakach \((+,-,+)\), które następnie zamykają się jako trójwęzeł?

Nie zakładamy, że piąty element jest automatycznie środkowym płatem ani że znak sekwencji jest z góry ustalony. Trzeba wyprowadzić to z sygnału źródłowego i operatora redukcji.

## 5. Zachowanie informacji o znaku i orientacji

Przechowywać osobno:
- znak płata \(p_i\);
- orientację parametryzacji czasu / przebiegu;
- fazę na wejściu i wyjściu płata;
- kierunek stycznej w punktach przejścia przez zero;
- torsję Freneta (jeśli krzywa 3D jest dostatecznie gładka);
- skręt ramy / pasma, jeśli rama zostanie zdefiniowana;
- znak obiegu osiowego.

Nie utożsamiać znaku sygnału z torsją Freneta ani z ręcznością topologiczną. Są to różne wielkości, które mogą być powiązane dopiero przez jawny operator mapowania.

Odwrócenie czasu lub kierunku parametryzacji należy testować oddzielnie: może odwrócić kolejność płatów i pochodne, a niekoniecznie dać tę samą reprezentację znaku.

## 6. Testy falsyfikujące

1. Wygenerować trzy kolejne półfale sinusoidy i odzyskać dokładnie sekwencję znaków \((+,-,+)\).
2. Zastosować wartość bezwzględną i potwierdzić, że niszczy informację o znaku środkowego płata.
3. Odwrócić kierunek parametryzacji i zapisać transformację sekwencji.
4. Zbudować jawne osadzenie 3D z trzech płatów; sprawdzić domknięcie pozycji i stycznych.
5. Sprawdzić, czy osadzenie ma trzy gałęzie i rzeczywiste połączenia w węźle, czy tylko trzy płaty krzywej.
6. Porównać niezmienniki grafu / osadzenia przed i po redukcji.
7. Zbadać, czy zmiana znaku środkowego płata wpływa na orientację i ręczność, bez utożsamiania tego z antycząstką.

## 7. Kryterium sukcesu

Hipoteza „naprzemienność + − + generuje trójwęzeł” otrzyma wsparcie dopiero wtedy, gdy:
- znak trzech płatów jest zachowany przez operator redukcji;
- mapa sygnał→krzywa 3D jest jednoznaczna;
- warunki brzegowe i szew są spełnione;
- powstaje jawna trójgałęziowa struktura z określonymi połączeniami;
- orientacja środkowego płata ma mierzalny skutek w niezmiennikach lub geometrii;
- wynik nie jest artefaktem wybranego rysunku/projekcji.

## 8. Powiązanie z osią i punktami kardynalnymi

Kandydaci na punkty kardynalne:
- dwa przejścia przez zero, które ograniczają środkowy płat;
- trzy ekstrema płatów;
- punkty, w których mapa sygnał→gałąź zmienia orientację;
- punkty domknięcia lub sprzężenia gałęzi.

Nie ustalamy jeszcze, które z nich są rzeczywistymi punktami kardynalnymi. Najpierw trzeba sprawdzić ich stabilność przy zmianie amplitudy, częstotliwości, fazy i małych perturbacjach.

## 9. Zasada robocza

**Trójwęzeł badamy jako geometryczne rozwinięcie trzech kolejnych płatów sygnału o znakach +, −, +. Znak środkowego płata jest informacją, której redukcja nie może zgubić.**