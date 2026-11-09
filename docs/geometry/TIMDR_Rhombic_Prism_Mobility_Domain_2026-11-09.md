# TIMDR — podatność geometryczna graniastosłupa trójkątnego z trzema rombami

**Data:** 2026-11-09  
**Model:** dwa przystające trójkąty równoboczne i trzy boczne romby; wszystkie krawędzie długości 1.  
**Status:** dokładny opis przestrzeni konfiguracji i ograniczeń kątowych.

## 1. Doprecyzowanie modelu

Topologicznie jest to graniastosłup trójkątny (nie zwykły ostrosłup). Dolny i górny trójkąt są przystające i równoboczne. Każda ściana boczna jest rombem, czyli równoległobokiem o czterech równych bokach.

Ustawiamy dolny trójkąt w płaszczyźnie (z=0), o wierzchołkach:
[
(0,0,0),quad (1,0,0),quad (1/2,\sqrt3/2,0).
]
Górny trójkąt jest przesunięciem dolnego o wektor:
[
t=(u,v,w),qquad u^2+v^2+w^2=1,quad w>0.
]
Warunek (|t|=1) zapewnia, że krawędzie boczne mają tę samą długość co krawędzie trójkątów. Każda ściana boczna jest więc rombem.

## 2. Dwa stopnie swobody

Po pominięciu globalnego przesunięcia i obrotu całej bryły jedynym parametrem kształtu jest kierunek jednostkowego wektora (t). Wybór (w>0) daje górną półsferę:
[
u^2+v^2<1,qquad w=\sqrt{1-u^2-v^2}.
]
Jest to dwuwymiarowa przestrzeń konfiguracji. Bryła ma zatem **2 wewnętrzne stopnie swobody** w tej klasie deformacji.

Nie jest to materiałowa miękkość ani dowód sprężystości. To podatność kinematyczna: istnieje ciągła rodzina nieprzystających kształtów z tymi samymi długościami wszystkich dziewięciu krawędzi.

## 3. Ograniczenia kątów rombów

Kierunki trzech krawędzi dolnego trójkąta:
[
e_1=(1,0,0),quad
e_2=(-1/2,\sqrt3/2,0),quad
e_3=(-1/2,-\sqrt3/2,0).
]
Niech (c_i=t\cdot e_i). Wtedy:
[
c_1=u,quad
c_2=\frac{-u+\sqrt3v}{2},quad
c_3=\frac{-u-\sqrt3v}{2}.
]
Z geometrii wynikają zależności:
[
\boxed{c_1+c_2+c_3=0}
]
oraz
[
\boxed{c_1^2+c_2^2+c_3^2=\frac32(u^2+v^2)<\frac32}.
]
Jeżeli \(\alpha_i\) jest ostrym kątem i-tego rombu, to:
[
\cos\alpha_i=|c_i|.
]
Każdy kąt może przyjmować wartości:
[
0^\circ<\alpha_i\le90^\circ,
]
ale trzy kąty nie są niezależne. Zmiana jednego ogranicza możliwe wartości pozostałych dwóch.

Równoważny warunek dopuszczalności dla dwóch parametrów (c_1,c_2):
[
c_1^2+\frac{(c_1+2c_2)^2}{3}<1,qquad c_3=-c_1-c_2.
]
To wnętrze elipsy w płaszczyźnie (c_1+c_2+c_3=0). Brzeg oznacza (w=0), czyli zerową wysokość i zdegenerowaną bryłę.

## 4. Pole i objętość

Pole każdego rombu:
[
A_i=\sqrt{1-c_i^2}.
]
Pole trójkąta końcowego jest stałe:
[
A_\triangle=\frac{\sqrt3}{4}.
]
Objętość:
[
V=\frac{\sqrt3}{4}w
=\frac{\sqrt3}{4}\sqrt{1-u^2-v^2}.
]
Maksimum występuje dla (u=v=0), gdy (t) jest pionowy, wszystkie ściany boczne są kwadratami, a:
[
V_{\max}=\frac{\sqrt3}{4}.
]
Przy zbliżaniu się do brzegu dopuszczalnej dziedziny wysokość i objętość dążą do zera.

## 5. Ważne rozróżnienie: pole a sztywność

Stałe pole trójkąta samo w sobie nie czyni go sztywnym — trójkąt może zmieniać boki i kąty, zachowując pole. W tym modelu sztywność ścian trójkątnych oznacza zachowanie ich kształtu, czyli wszystkich trzech długości boków (tu: trójkąty równoboczne o boku 1).

Podobnie romb zachowuje długości boków, ale jego pole i kąty zmieniają się. To precyzyjny sens „miękkiej” figury: stałe krawędzie, zmienna konfiguracja i zmienne pola ścian.

## 6. Co należy zbadać dalej

1. Przenieść tę dwuwymiarową przestrzeń konfiguracji na mapę kątów ((\alpha_1,\alpha_2,\alpha_3)).
2. Dla każdej konfiguracji zbudować pięć płaszczyzn odbić i śledzić widmo obrotów oraz skoki śrubowe.
3. Szukać punktów szczególnych: symetrii, zerowego skoku, zbieżności osi i ewentualnych zmian typu grupy.
4. Oddzielić osobliwości geometryczne (zanik wysokości) od rezonansów grupy odbić.

## 7. Reprodukcja

`python experiments/rhombic_prism_mobility_domain.py`
