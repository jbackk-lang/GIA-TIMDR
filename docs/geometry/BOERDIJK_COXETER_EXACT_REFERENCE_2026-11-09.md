# Boerdijk–Coxeter tetrahelix — dokładny wzorzec geometryczny

**Data:** 2026-11-09  
**Status:** dokładna konstrukcja algebraiczna i testy regresyjne; nie jest dowodem tożsamości z helisą TIMDR ani walidacją fizyczną.  
**Źródło wskazówki:** `timdr-signal-framework-SKILL.md`, §12.  
**Implementacja:** `core/boerdijk_coxeter_tetrahelix.py`  
**Testy:** `experiments/helix_characterization/tests/test_boerdijk_coxeter_tetrahelix.py`

## 1. Konstrukcja

Punkty początkowe:
`v0=(1,1,1), v1=(1,-1,-1), v2=(-1,1,-1), v3=(-1,-1,1)`.

Każda krawędź ma długość (2\sqrt2). Dla kolejnego kroku odbijamy najstarszy wierzchołek (v_i) względem płaszczyzny przechodzącej przez pozostałe trzy punkty (v_{i+1},v_{i+2},v_{i+3}). Otrzymujemy (v_{i+4}). Operacja jest wykonywana dokładnie na liczbach wymiernych; nie ma parametrów dopasowania.

## 2. Dokładna transformacja śrubowa

Dla tej konwencji współrzędnych jeden i ten sam operator odwzorowuje każdy punkt łańcucha na następny:
[
v_{i+1}=v_i R+t,
]
gdzie (wektory są wierszowe):
[
R=\frac13
\begin{pmatrix}
2&2&-1\\
2&-1&2\\
1&-2&-2
\end{pmatrix},
\qquad
t=\left(-\frac23,-\frac23,-\frac23\right).
]

Dokładnie zachodzi (R^TR=I), (det R=1), a testy sprawdzają (S(v_i)=v_{i+1}) dla 60 kolejnych wierzchołków. Ta sama transformacja przenosi centroid każdego czworościanu na centroid następnego.

## 3. Oś i parametry helisy wierzchołków

Dla powyższej konwencji:
- kierunek osi: (d=(2,1,0)/\sqrt5);
- punkt osi: (c=(0,0,-2/5));
- promień wierzchołków od osi: (r=3\sqrt6/5);
- podpisany postęp osiowy na krok: (h_s=-2/\sqrt5);
- kąt obrotu śrubowego: (\theta=\arccos(-2/3)\approx131.8103149^\circ).

Wierzchołki leżą więc dokładnie na jednej helisie kołowej jako dyskretne próbki o stałym przyroście fazy i stałym przyroście osiowym. Odcinki proste łączące wierzchołki są cięciwami; nie należy mylić ich z ciągłą krzywą osiową.

## 4. Ważne rozróżnienie kątów

W regularnym czworościanie:
- wewnętrzny kąt dwuścienny ma (\cos\alpha=1/3), czyli (\alpha\approx70.5287794^\circ);
- kąt obrotu transformacji śrubowej na jeden wierzchołek ma (\cos\theta=-2/3), czyli (\theta\approx131.8103149^\circ).

To różne wielkości. Żadna z nich nie jest automatycznie ciągłą torsją Freneta–Serreta (\tau_{FS}). W dokumentach i kodzie należy używać pełnych nazw: kąt dwuścienny czworościanu, kąt obrotu śrubowego, dyskretny kąt dwuścienny/skrętu oraz torsja Freneta–Serreta.

## 5. Porównanie z HC-01 — co jest wspólne, a co nie

HC-01 opisuje ciągłą helisę kołową:
[
r(t)=(a\cos t,a\sin t,ht).
]
BC daje dokładną dyskretną sekwencję punktów, która leży na takiej helisie po odpowiednim sztywnym ustawieniu osi. Dla BC można zatem zdefiniować ciągły odpowiednik przez:
[
a=3\sqrt6/5,\qquad h=\frac{-2/\sqrt5}{\arccos(-2/3)}.
]
Jest to porównanie geometryczne, nie utożsamienie całej struktury: BC zawiera również łańcuch przystających czworościanów, ich ściany i regułę odbicia. HC-01 nie ma automatycznie tej struktury modułowej ani warunków sklejenia.

Wniosek: HC-01 może służyć do niezależnego sprawdzenia krzywizny i torsji ciągłej helisy wyznaczonej przez punkty BC; BC dostarcza natomiast dyskretnego operatora generującego moduły.

## 6. Czego wynik NIE dowodzi

Nie dowodzi:
- że moduł TIMDR jest czworościanem foremnym;
- że trójkątny moduł TIMDR musi generować tetrahelisę;
- że oś TIMDR, kula/jajo lub redukcja 4→3 wynikają z BC;
- że torsja geometryczna jest fizycznym kanałem sygnałowym;
- że istnieje pamięć, samonaprawa lub przewaga informacyjna;
- że kąty BC są progami kardynalnymi TIMDR.

Skill §12 wyraźnie mówi, że analog 4-gonu i odwrotna rekonstrukcja helisa→czworościan nie zostały formalnie skonstruowane. Nie będziemy zakładać takiej mapy.

## 7. Następne porównanie TIMDR

Należy zdefiniować moduł TIMDR jako jawny zestaw danych:
[
M_i=(\text{wierzchołki},\text{orientacja},\text{operator odbicia},\text{faza},\text{szew}).
]
Następnie sprawdzić, czy istnieje jeden sztywny operator (S_{TIMDR}), który:
1. przenosi moduł (M_i) na (M_{i+1});
2. zachowuje wskazane długości/kąty;
3. ma stały przyrost fazy i osi;
4. przewiduje moduły niewykorzystane do wyznaczenia operatora;
5. zachowuje poprawną orientację po odbiciu i sklejeniu.

Porównać hipotezę operatora stałego z wariantem zmiennym; nie dopasowywać go na wszystkich modułach i potem nie przedstawiać dopasowania jako predykcji.

## 8. Status

- BC exact rational recurrence: **DEFINED / IMPLEMENTED**.
- Jedna sztywna transformacja przewiduje kolejne wierzchołki: **EXACTLY VERIFIED** dla konstrukcji i konwencji współrzędnych w tym pliku.
- Równoważność BC ↔ TIMDR: **UNKNOWN**.
- Mapa moduł trójkątny TIMDR → BC: **UNKNOWN**.
- Mapa BC → fizyczny kanał odpowiedzi G: **UNKNOWN**.

## 9. Reprodukowalność

Uruchomienie testów:
`python -m unittest experiments.helix_characterization.tests.test_boerdijk_coxeter_tetrahelix -v`

Testy używają wyłącznie standardowej biblioteki Pythona i dokładnej arytmetyki `Fraction`; nie wymagają SciPy ani NumPy.
