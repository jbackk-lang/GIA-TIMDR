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


## 8. Walidacja

Dokładne sprawdzenia symboliczne przeszły w GitHub Actions:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42626682712

Zweryfikowano relacje między trzema kątami, dwuwymiarowość przestrzeni konfiguracji, pola rombów, stałe pole trójkątów oraz wzór na objętość.


## 9. Sprzężenie podatności z widmem ruchów śrubowych

Dodano skan numeryczny całej rodziny konfiguracji:
`experiments/rhombic_prism_mobility_screw_coupling.py`.

Parametry ((u,v)) opisują dwa stopnie swobody, (u^2+v^2<1). Dla każdej próbki konstruujemy pięć płaszczyzn odbić i enumerujemy wszystkie zredukowane słowa długości 4 (320 słów). Następnie porównujemy uzyskane izometrie afiniczne i klasyfikujemy je jako obroty, ruchy śrubowe, translacje lub identyczność.

### Skan przekroju (u=1/2)

| (v) | Kąty ostre rombów (°) | Różne mapy | Obroty | Śruby | Translacje |
|---:|---|---:|---:|---:|---:|
| 0 | 60; 75.522; 75.522 | 161 | 116 | 36 | 8 |
| 0.05 | 60; 78.071; 72.944 | 302 | 222 | 72 | 8 |
| 0.10 | 60; 80.596; 70.330 | 302 | 222 | 72 | 8 |
| 0.20 | 60; 85.596; 64.963 | 302 | 222 | 72 | 8 |
| 0.288675 | 60; 90; 60 | 245 | 176 | 60 | 8 |
| 0.35 | 60; 86.956; 56.419 | 302 | 222 | 72 | 8 |
| 0.50 | 60; 79.455; 46.920 | 302 | 222 | 72 | 8 |
| 0.577350 | 60; 75.522; 41.410 | 292 | 212 | 72 | 8 |
| 0.60 | 60; 74.359; 39.681 | 302 | 222 | 72 | 8 |
| 0.70 | 60; 69.132; 31.105 | 302 | 222 | 72 | 8 |

Dodatkowy punkt poza tą linią, ((u,v)=(0.1,0.1)), również dał 302 mapy: 222 obroty, 72 śruby i 8 translacji.

### Co z tego wynika — ostrożnie

1. W próbkach ogólnych widmo długości 4 jest stabilne: 302 różne mapy, w tym 72 ruchy śrubowe.
2. W szczególnych konfiguracjach pojawiają się dodatkowe zbieżności transformacji: liczba różnych map spada, np. do 245 lub 292.
3. W punkcie (v=0) na badanym przekroju występuje dodatkowa symetria i liczba śrub spada do 36.
4. Próbki (v=1/(2\sqrt3)) i (v=1/\sqrt3) odtwarzają wcześniej badane przypadki A i B.

To wspiera hipotezę, że podatność geometryczna steruje nie tylko wymiarami bryły, lecz także strukturą relacji odbić. Szczególne kąty mogą odpowiadać konfiguracjom rezonansowym, w których różne słowa odbić dają tę samą izometrię.

**Ograniczenie:** skan jest numeryczny (deduplikacja z tolerancją (10^{-8})) i obejmuje wyłącznie słowa długości 4. Nie dowodzi globalnej klasyfikacji grupy ani nie wskazuje jeszcze pełnego zbioru krzywych rezonansowych w dysku ((u,v)). Wymaga to dokładnej analizy symbolicznej.

### Status reprodukcji

GitHub Actions: https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42627185257
