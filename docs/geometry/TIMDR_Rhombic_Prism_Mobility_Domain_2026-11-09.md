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


## 10. Rozpoznanie loci symetrii i punktów rezonansowych

Rozszerzony skan (17 konfiguracji, w tym punkty lustrzane i kontrole po obu stronach) zakończył się powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42628189983

Zwiększono precyzję deduplikacji numerycznej z 8 do 10 miejsc po przecinku. Dla (u=1/2) wyniki są następujące:

| Warunek / (v) | Kąty ostre rombów | Różne mapy długości 4 | Obroty | Śruby |
|---|---|---:|---:|---:|
| (v=0) | (60,75.522,75.522\degree) | 161 | 116 | 36 |
| (v=+1/(2\sqrt3)) | (60,90,60\degree) | 245 | 176 | 60 |
| (v=-1/(2\sqrt3)) | (60,60,90\degree) | 245 | 176 | 60 |
| (v=+1/\sqrt3) | (60,75.522,41.410\degree) | 292 | 212 | 72 |
| (v=-1/\sqrt3) | (60,41.410,75.522\degree) | 292 | 212 | 72 |
| próbki ogólne | brak równych kątów | 302 | 222 | 72 |

### Dwie rodziny loci równych kątów

Ponieważ:
[
c_1=u,\quad c_2=\frac{-u+\sqrt3v}{2},\quad
c_3=\frac{-u-\sqrt3v}{2},
]
równość ostrych kątów dwóch rombów oznacza (|c_i|=|c_j|), a więc dwa różne przypadki:

- (c_i=c_j): dwie ściany mają ten sam kąt i trzeci cosinus jest przeciwny do ich sumy. W badanych próbkach tej rodziny otrzymujemy 161 map, 116 obrotów i 36 śrub.
- (c_i=-c_j): trzeci cosinus jest zerowy, czyli jedna ściana boczna jest kwadratem, a dwie pozostałe mają równe kąty ostre. W badanych próbkach tej rodziny otrzymujemy 245 map, 176 obrotów i 60 śrub.

Są to linie w dwuwymiarowej przestrzeni parametrów, a nie pojedyncze punkty. Skan sprawdził kilka punktów na każdej z tych rodzin; pełna identyfikacja wszystkich relacji grupowych na całych liniach wymaga dowodu symbolicznego.

### Izolowane punkty dodatkowej degeneracji

Punkty (u=1/2, v=\pm1/\sqrt3) dają 292 mapy, mimo że nie mają pary równych kątów ostrych. Przesunięcie (v) o zaledwie (10^{-5}) w dowolną stronę przywraca 302 mapy. Ich lustrzane odpowiedniki dają ten sam wynik.

Dla dodatniego punktu ten wynik 292 map jest dodatkowo zgodny z wcześniejszym dokładnym, symbolicznym przypadkiem B ((c_1=1/2,c_2=1/4,c_3=-3/4)). Ujemny punkt jest jego odbiciem lustrzanym.

### Co można już powiedzieć

- 302 mapy to wynik typowy w przebadanych konfiguracjach ogólnych.
- Linie równych kątów są loci symetrii z wyraźnie zmienionym widmem długości 4.
- Istnieją również szczególne konfiguracje bez równych kątów, w których liczba map spada do 292.
- W pobliżu tych miejsc widmo wraca do wartości typowej; nie jest to ciągły spadek liczby transformacji.

To jest mocniejszy obraz niż hipoteza o pojedynczym „rezonansie”: w przestrzeni kształtów widać co najmniej dwie rodziny loci symetrii i dodatkowe punkty szczególne. Nadal nie jest to pełna klasyfikacja wszystkich rezonansów ani całej nieskończonej grupy odbić.


## 11. Mapa loci szczególnych — rozszerzenie skanu 2D

Rozszerzono skan o wszystkie sześć prostych równości kątów oraz kandydacką elipsę:
[
u^2+4v^2=1.
]
Na tej elipsie, z warunku (u^2+v^2+w^2=1), wynika:
[
w^2=3v^2,qquad w=\sqrt3|v|.
]

### A. Linie równych kątów

Ponieważ:
[
c_1=u,quad c_2=(-u+\sqrt3v)/2,quad c_3=(-u-\sqrt3v)/2,
]
warunki (|c_i|=|c_j|) rozkładają się na sześć prostych:

- (c_i=c_j): (v=0), (v=\sqrt3u), (v=-\sqrt3u);
- (c_i=-c_j): (u=0), (v=u/\sqrt3), (v=-u/\sqrt3).

W próbkach poza przecięciami:
- gałęzie (c_i=c_j): 161 różnych map długości 4;
- gałęzie (c_i=-c_j): 245 różnych map długości 4.

### B. Nowa elipsa degeneracji

Dla punktów:
[
(u,v)=\left(u,\pm\frac{\sqrt{1-u^2}}{2}\right)
]
sprawdzono dziewięć wartości (u=0.1,0.2,\ldots,0.9), a także próbki po obu stronach elipsy z przesunięciem (v\mapsto v\pm10^{-5}).

W ośmiu punktach poza szczególnym (u=0.5) otrzymano:
- 290 różnych map;
- 210 obrotów;
- 72 ruchy śrubowe;
- 8 translacji.

Dla (u=0.5), (v=\pm\sqrt3/4), otrzymano 280 map: 200 obrotów, 72 śruby i 8 translacji.

W każdym zbadanym punkcie po obu stronach elipsy liczba map wracała do 302: 222 obroty, 72 śruby i 8 translacji. To wspiera interpretację elipsy jako szczególnego locus, a nie szerokiego obszaru.

Przecięcia elipsy z innymi loci są bardziej zdegenerowane:
- ((u,v)=(0,\pm1/2)): 229 map (160 obrotów, 60 śrub, 8 translacji i identyczność);
- ((u,v)=(\pm1/2,\pm\sqrt3/4)): 280 map w zbadanych znakowych wariantach.

### C. Dodatkowy punkt rezonansowy

Punkt ((u,v)=(1/2,1/\sqrt3)) oraz jego odbicia znakowe dają 292 mapy (212 obrotów, 72 śruby i 8 translacji). Próbki przesunięte o (10^{-5}) w kierunku (v) dają 302 mapy. Punkt ten leży poza elipsą (u^2+4v^2=1) i poza prostymi równych kątów.

### D. Uwaga o dokładności numerycznej

Deduplikacja map wykorzystuje zaokrąglenie współczynników do 7 miejsc po przecinku. Wcześniejsza wersja używała 10 miejsc; dla wyrażeń z (\sqrt3) powodowało to niestabilność rozpoznawania teoretycznie identycznych map przy niektórych wejściach zmiennoprzecinkowych. Kontrole po obu stronach loci ((10^{-5})) pozostają od nich wyraźnie oddzielone.

Z tego powodu liczby z tego skanu są **wynikami numerycznymi z ustaloną tolerancją**, a nie dowodem dokładnych relacji grupowych. Następny etap powinien wyprowadzić równości transformacji symbolicznie, w pierścieniu algebraicznym z relacją (w^2=1-u^2-v^2).

### E. Reprodukcja

Rozszerzony skan i CI:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42629227737

Kod:
`experiments/rhombic_prism_mobility_screw_coupling.py`


## 12. Dokładne wyjaśnienie elipsy: relacje Coxetera

Najważniejszy krok: elipsa nie jest już tylko numerycznie wykrytym zbiorem punktów. Dla jej dodatniej gałęzi:
[
u^2+4v^2=1,\quad v>0,\quad w=\sqrt3v
]
normalna do ściany bocznej opartej na krawędzi (e_1=(1,0,0)) ma postać:
[
n=e_1\times t=(0,-w,v)=(0,-\sqrt3v,v).
]
Normalna do dolnego i górnego trójkąta jest równoległa do osi (z). Po unormowaniu:
[
\left|\widehat n\cdot(0,0,1)\right|
=\frac{v}{\sqrt{w^2+v^2}}
=\frac12.
]
Zatem kąt między normalnymi wynosi (60^\circ) (z dokładnością do wyboru orientacji), a kąt dwuścienny między płaszczyznami jest równy (60^\circ).

Dwie refleksje w płaszczyznach przecinających się pod kątem (\pi/3) spełniają relację Coxetera:
[
s_i s_j s_i=s_j s_i s_j,\qquad (s_i s_j)^3=1.
]
W naszym przypadku zachodzą dwie dokładne afiniczne relacje:
[
s_0s_2s_0=s_2s_0s_2,
\qquad
s_1s_2s_1=s_2s_1s_2,
]
gdzie (s_0,s_1) są odbiciami w dolnej i górnej płaszczyźnie trójkąta, a (s_2) jest odbiciem w wybranej ścianie bocznej.

To wyjaśnia, dlaczego na elipsie liczba map długości 4 spada o 12 względem typowego wyniku 302: dwie relacje braid generują dodatkowe identyfikacje słów długości 4. Niezależny enumerator kombinatoryczny potwierdza, że te dwie relacje łączą 320 zredukowanych słów w 308 klas, czyli wymuszają dokładnie 12 identyfikacji. Pozostałe 18 identyfikacji obecnych w próbce ogólnej pozostają odrębnym zjawiskiem.

**Ważne:** dowód relacji Coxetera jest dokładny. Przypisanie całej różnicy (302\to290) wyłącznie tym relacjom jest zgodne z enumeracją długości 4; pełna klasyfikacja wszystkich możliwych relacji w całej grupie nadal nie została przeprowadzona.

### Reprodukcja symboliczna

`python experiments/rhombic_prism_ellipse_braid_relation.py`

Skrypt sprawdza dokładnie macierze afinicznych odbić i liczy wymuszone identyfikacje słów.


Walidacja GitHub Actions zakończona powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42629739921

CI potwierdziło dokładnie obie afiniczne relacje braid oraz 12 dodatkowych identyfikacji wśród 320 zredukowanych słów długości 4.


## 13. Trzy elipsy Coxetera — pełna symetria trzech ścian bocznych

Warunek kąta (60^\circ) można zapisać bez wybierania układu współrzędnych dla konkretnej ściany. Dla krawędzi podstawy:
[
e_i=(a_i,b_i,0),\quad h=(u,v,0),\quad t=h+(0,0,w),
]
definiujemy:
[
c_i=e_i\cdot h=a_i u+b_i v,
\qquad
q_i=a_i v-b_i u.
]
Normalna do ściany bocznej to (n_i=e_i\times t), więc:
[
\|n_i\|^2=1-c_i^2,\qquad (n_i)_z=q_i.
]
Kąt między normalną ściany bocznej a normalną poziomej ściany końcowej ma cosinus bezwzględny:
[
\frac{|q_i|}{\sqrt{1-c_i^2}}.
]
Warunek kąta (60^\circ) jest zatem równoważny:
[
\boxed{4q_i^2=1-c_i^2}.
]
Po podstawieniu trzech kierunków krawędzi trójkąta otrzymujemy dokładnie trzy elipsy:
[
\boxed{u^2+4v^2=1},
]
[
\boxed{13u^2+6\sqrt3uv+7v^2=4},
]
[
\boxed{13u^2-6\sqrt3uv+7v^2=4}.
]

Każda elipsa odpowiada jednej ze ścian bocznych. Na jej dopuszczalnych łukach odpowiednia ściana boczna spotyka się pod kątem (60^\circ) z obiema równoległymi ścianami trójkątnymi. W konsekwencji dla każdej z trzech ścian bocznych powstają dwie relacje braid: z odbiciem dolnej i górnej ściany końcowej.

Skan numeryczny rozszerzono na wszystkie trzy obrócone elipsy, ich obie gałęzie oraz punkty kontrolne przesunięte poza loci. W typowych próbkach każdej elipsy widmo długości 4 ma 290 map (210 obrotów, 72 śruby, 8 translacji). Szczególne przecięcia elips z innymi loci mogą mieć mniejszą liczbę map.

Dokładne sprawdzenie symboliczne:
`experiments/rhombic_prism_ellipse_braid_relation.py`

Skan numeryczny:
`experiments/rhombic_prism_mobility_screw_coupling.py`

GitHub Actions — oba testy zakończone powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42629995606


Dodatkowy test symboliczny rozszerzono o sprzężenie obrotami (\pm120^\circ) wokół osi (z). CI potwierdza relacje braid dla wszystkich trzech ścian bocznych, każdej z dolną i górną ścianą trójkątną:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42630116584
