# Ogólny czworościan: czterokrokowa periodyczność śrubowa (v0.1)

**Data:** 2026-11-09  
**Status:** twierdzenie geometryczne dla rekurencji odbicia ścianowego; dowód oparty na dokładnej permutacji metryki i niezmienniczości odbicia względem izometrii. Test regresyjny dodany do testów BC.  
**Zakres:** dowolny niekoplanarny czworościan, bez założenia foremności.

## 1. Wynik

Dla rekurencji
\[
v_{n+4}=\operatorname{Reflect}\big(v_n,\operatorname{plane}(v_{n+1},v_{n+2},v_{n+3})\big)
\]
nie istnieje na ogół jedna izometria przenosząca uporządkowane okno \((v_n,v_{n+1},v_{n+2},v_{n+3})\) na następne okno przesunięte o jeden punkt.

Istnieje natomiast jedna stała, właściwa izometria \(T\), która przenosi okno o cztery pozycje:
\[
T(v_n)=v_{n+4}\quad\text{dla każdego }n.
\]

Jeżeli \(T\) nie jest identycznością, jest ruchem śrubowym (w szczególnych przypadkach czystym obrotem lub translacją). W konsekwencji łańcuch rozkłada się na cztery przeplatane orbity:
\[
\{v_{4k}\},\quad\{v_{4k+1}\},\quad
\{v_{4k+2}\},\quad\{v_{4k+3}\},
\]
z których każda jest orbitą tej samej izometrii śrubowej \(T\). Dla niezerowego postępu osiowego każda orbita jest dyskretnym śladem helisy; wszystkie cztery mają wspólną oś, ale mogą mieć różne promienie i fazy.

To jest **czterogałęziowa periodyczność śrubowa**, a nie automatycznie fraktalność.

## 2. Dowód — permutacja sześciu krawędzi

Dla uporządkowanego czworościanu \(W_n=(v_n,v_{n+1},v_{n+2},v_{n+3})\) oznaczmy kwadraty długości krawędzi w kolejności:
\[
E_n=(d_{01}^2,d_{02}^2,d_{03}^2,d_{12}^2,d_{13}^2,d_{23}^2).
\]

Odbicie \(v_n\) względem płaszczyzny trzech pozostałych wierzchołków zachowuje odległości nowego punktu od każdego z tych trzech wierzchołków. Stąd:
\[
E_{n+1}=(d_{12}^2,d_{13}^2,d_{01}^2,
d_{23}^2,d_{02}^2,d_{03}^2).
\]
Jest to stała permutacja sześciu pozycji:
\[
P(a,b,c,d,e,f)=(d,e,a,f,b,c).
\]
Bezpośrednio:
\[
P^2(a,b,c,d,e,f)=(f,b,d,c,e,a),
\]
\[
P^3(a,b,c,d,e,f)=(c,e,f,a,b,d),
\qquad P^4=I.
\]
Zatem:
\[
E_{n+4}=E_n
\]
dla każdego niekoplanarnego wejściowego czworościanu.

Po czterech krokach wszystkie sześć krawędzi wraca do tych samych pozycji uporządkowanego czworościanu. Dwa uporządkowane czworościany \(W_n\) i \(W_{n+4}\) mają więc identyczną macierz odległości. Istnieje dokładnie jedna izometria euklidesowa przenosząca pierwszy uporządkowany czworościan na drugi.

Znak zorientowanej objętości również pozostaje taki sam: każde odbicie odwraca orientację bryły, a przesunięcie okna o jeden indeks jest permutacją cykliczną czterech wierzchołków, która także odwraca znak. Dwa odwrócenia dają zachowanie orientacji. Izometria \(T\) jest więc właściwa, \(\det R=+1\).

## 3. Dlaczego operator jest stały dla całego łańcucha

Odbicie jest ekwiwariantne względem izometrii właściwych: dla dowolnej takiej izometrii \(T\):
\[
T(\operatorname{Reflect}(x,\Pi))
=\operatorname{Reflect}(T(x),T(\Pi)).
\]

Z definicji \(T\) przenosi \(W_n\) na \(W_{n+4}\). Następny punkt w obu oknach powstaje tą samą regułą odbicia. Ekwiwariantność daje:
\[
T(v_{n+4})=v_{n+8}.
\]
Indukcyjnie:
\[
T(v_n)=v_{n+4}\quad\forall n.
\]
Nie jest to dopasowanie numeryczne do skończonej próbki, lecz konsekwencja rekurencji i czterokrokowej identyczności uporządkowanej metryki.

## 4. Dlaczego krok pojedynczy jest na ogół inny

Dla jednego kroku wektor krawędzi zmienia się przez \(P\), a nie pozostaje taki sam. Izometria przenosząca \(W_n\) na \(W_{n+1}\) istnieje tylko wtedy, gdy:
\[
(a,b,c,d,e,f)=(d,e,a,f,b,c).
\]
To wymusza:
\[
a=c=d=f,\qquad b=e.
\]
Jest to szczególne ograniczenie na sześć długości krawędzi, którego ogólny czworościan nie spełnia. Regularny czworościan jest przypadkiem szczególnym, w którym operator może działać już co jeden krok.

Dlatego wcześniejsze stwierdzenie „ogólny czworościan nie ma stałego operatora śrubowego” wymaga doprecyzowania: **na ogół nie ma stałego operatora na jeden krok; ma stały operator na cztery kroki.**

## 5. Przykład liczbowy — ogólny czworościan

Dla wejściowych wierzchołków:
\[
v_0=(0,0,0),\quad
v_1=(2,0.2,0.1),\quad
v_2=(0.3,3,0.2),\quad
v_3=(0.1,0.4,4)
\]
numeryczne wyznaczenie właściwej izometrii z \(W_0\mapsto W_4\) daje przykładowo:
- kąt obrotu około \(162.3959355^\circ\);
- jednostkowy kierunek osi około \((-0.662527,-0.563342,-0.493663)\);
- podpisany postęp osiowy na cztery kroki około \(-3.391762\);
- maksymalny błąd predykcji kolejnych punktów przy arytmetyce zmiennoprzecinkowej około \(5.5\cdot10^{-14}\).

Wartości te dotyczą wyłącznie podanego przykładu i konwencji orientacji. Dowód ogólny nie zależy od tych liczb. Dla innych czworościanów kąt, oś, postęp i promienie czterech orbit będą inne.

## 6. Co to oznacza geometrycznie

- Łańcuch nie musi być pojedynczą próbkowaną helisą.
- Co czwarty wierzchołek leży na jednej orbicie \(T\); analogicznie trzy pozostałe klasy reszt modulo 4.
- Wszystkie cztery orbity są generowane przez tę samą oś i ten sam kąt/postęp, lecz mogą być przesunięte względem siebie.
- Złożenie czterech orbit daje dyskretny łańcuch z czteropunktowym motywem wewnętrznym.
- Dla szczególnych danych możliwy jest czysty obrót, translacja albo przypadek zdegenerowany; należy raportować parametry \(T\), a nie zakładać z góry niezerową helikalność.

## 7. Czy to fraktal?

Nie. Stała izometria śrubowa zachowuje odległości i nie jest kontrakcją. Cztery przeplatane orbity tworzą strukturę o skończonym motywie i jednej regule ruchu. To odkrycie jest matematycznie istotne, ale samo nie daje nieskończonej hierarchii skal ani niecałkowitego wymiaru.

Potencjalny dalszy kierunek to dopiero:
1. porównać cztery promienie i fazy orbit;
2. zbadać, kiedy orbity pokrywają się, są rozłączne lub przecinają się;
3. zbadać rodzinę operatorów \(T\) w przestrzeni kształtów czworościanów;
4. sprawdzić, czy dodatkowe sprzężenie/zmienna reguła modułu wprowadza rekurencję skalową.

Nie nazywać tych własności fraktalnymi bez odrębnego dowodu.

## 8. Reprodukowalność i zmiany w repozytorium

Test dokładny test_general_tetrahedron_has_exact_four_step_ordered_congruence sprawdza identyczność sześciu uporządkowanych kwadratów krawędzi oraz zachowanie zorientowanej objętości między \(W_n\) i \(W_{n+4}\) dla wielu okien. Test test_generic_tetrahedron_does_not_have_one_step_ordered_congruence kontroluje, że dla przykładowego ogólnego czworościanu zgodność jednego kroku nie zachodzi.

Testy dopisano do:
experiments/helix_characterization/tests/test_boerdijk_coxeter_tetrahelix.py.

**Status:** twierdzenie geometryczne — wyprowadzone; testy regresyjne — dodane; pełny CI po tym commicie — do sprawdzenia.
