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


---

## 14. KOREKTA MODELU ODBIĆ — rzeczywiste położenie ścian bocznych

**Ta sekcja zastępuje wcześniejsze numeryczne wyniki widma z sekcji 9–13 tam, gdzie użyto błędnego położenia płaszczyzn bocznych.**

Wcześniejszy skrypt umieszczał wszystkie trzy płaszczyzny boczne w początku układu. To niepoprawne: każda ściana boczna leży na innej krawędzi dolnego trójkąta. Dla krawędzi o kierunku (e_i), przechodzącej przez punkt (p_i), normalna jest (n_i=e_i\times t), ale odbicie afiniczne ma również translację:

\[
R_i=I-2\frac{n_i n_i^T}{n_i\cdot n_i},\qquad b_i=2n_i\frac{n_i\cdot p_i}{n_i\cdot n_i}.
\]

Pominięcie (b_i) zachowywało orientację płaszczyzny, lecz przesuwało dwie ściany boczne do niewłaściwych miejsc. W konsekwencji wcześniejsze liczby 161, 229, 245, 280, 292 i 302 z tamtego skanu nie mogą być traktowane jako wyniki dla rzeczywistej bryły.

Kod `rhombic_prism_mobility_screw_coupling.py` został poprawiony i uwzględnia wszystkie trzy rzeczywiste krawędzie podstawy.

### 14.1. Poprawione widmo długości 4

W poprawionym modelu jest 320 zredukowanych słów długości 4.

| Konfiguracja | Różne mapy | Obroty | Śruby | Translacje | Identyczność |
|---|---:|---:|---:|---:|---:|
| Ogólna | 320 | 192 | 120 | 8 | 0 |
| Typowy punkt na jednej z trzech elips Coxetera | 308 | 180 | 120 | 8 | 0 |
| Szczególny punkt elipsy z dodatkową relacją | 298 | 170 | 120 | 8 | 0 |
| Typowy punkt na linii ściany prostopadłej do podstaw | 245 | 148 | 84 | 12 | 1 |
| Szczególny punkt tej linii, promień poziomy (1/2) | 235 | 142 | 80 | 12 | 1 |

Są to wyniki dla różnych map otrzymanych ze zredukowanych słów długości 4, nie liczba elementów całej grupy.

### 14.2. Trzy elipsy Coxetera pozostają poprawne

Warunek kąta dwuściennego (60^\circ) między ścianą boczną a trójkątną nie zależy od przesunięcia płaszczyzny. Trzy elipsy pozostają:

\[
u^2+4v^2=1,
\]
\[
13u^2+6\sqrt3uv+7v^2=4,
\]
\[
13u^2-6\sqrt3uv+7v^2=4.
\]

Na typowym punkcie każdej elipsy zachodzą dokładne relacje braid dla odpowiedniej pary odbić dolnej/górnej ściany i ściany bocznej. Dają one 12 identyfikacji słów: (320\to308).

### 14.3. Trzy linie relacji prostopadłości

Jeżeli pozioma część przesunięcia (h=(u,v)) jest równoległa do jednej z trzech krawędzi podstawy, odpowiednia ściana boczna jest pionowa. Jest prostopadła do obu poziomych ścian trójkątnych, co daje dwie relacje komutacji:

\[
s_0s_i=s_is_0,\qquad s_1s_i=s_is_1.
\]

Odpowiadają im trzy linie:

\[
v=0,\qquad v=\sqrt3u,\qquad v=-\sqrt3u.
\]

W typowym punkcie tych linii poprawny skan daje 245 różnych map. Nie należy ich mylić z liniami, na których jedynie jedna ściana rombowa staje się kwadratem.

### 14.4. Dodatkowa relacja glide-reflection przy promieniu (1/2)

Na linii (v=0), dla

\[
(u,v,w)=\left(\frac12,0,\frac{\sqrt3}{2}\right),
\]

izometria (G=s_2s_1s_0) sprzęga dwie pozostałe refleksje boczne:

\[
G s_3 G^{-1}=s_4.
\]

Jest to dokładna relacja afiniczna, sprawdzona z niezerowymi przesunięciami płaszczyzn bocznych. Poprawiony skan ma wtedy 235 różnych map. Przez symetrię trójkąta istnieje sześć takich punktów: promień poziomy (1/2), trzy kierunki krawędzi i dwa zwroty.

### 14.5. Dodatkowy punkt na elipsie: prostopadłość po sprzężeniu

Na pierwszej elipsie (u^2+4v^2=1), normalna płaszczyzny będącej obrazem dolnej ściany przez (s_2) jest (R_2k), gdzie (k=(0,0,1)). Jej iloczyn skalarny z normalną sąsiedniej ściany bocznej ma licznik:

\[
F=\sqrt3u^3-u^2v+2\sqrt3uv^2-\sqrt3u+v.
\]

Po ograniczeniu do elipsy:

\[
F|_{E_1}=2v^2(2v-\sqrt3u).
\]

Poza zdegenerowanym brzegiem otrzymujemy punkty:

\[
(u,v)=\left(\frac12,\frac{\sqrt3}{4}\right),\quad
\left(-\frac12,-\frac{\sqrt3}{4}\right).
\]

W dodatnim punkcie (w=3/4) odbicia (s_2s_0s_2) i (s_3) komutują dokładnie. To dodatkowa relacja poza zwykłą relacją braid elipsy; poprawiony skan daje 298 map zamiast 308. Pozostałe punkty otrzymujemy przez obroty trójkąta.

### 14.6. Co zostało odrzucone

- Punkt ((0,1/2)), wcześniej opisywany jako 229 map, ma teraz 308 map i jest zwykłym punktem elipsy.
- Punkt ((1/2,1/\sqrt3)), wcześniej opisywany jako 292 mapy, ma teraz 320 map i jest ogólną konfiguracją w poprawnym modelu.
- Wcześniejsze przypisanie szczególnych liczb map samym równym kątom rombów było nieuzasadnione. O relacjach odbić decyduje położenie i kąt rzeczywistych płaszczyzn, nie tylko kąty ścian.

### 14.7. Testy

Dodano `experiments/rhombic_prism_exceptional_affine_relations.py`, który sprawdza dwie komutacje na liniach prostopadłości, dodatkowe sprzężenie glide-reflection przy promieniu (1/2), wielomianowy warunek dodatkowej komutacji na elipsie oraz dokładną komutację afinicznych odbić w szczególnym punkcie.

Skan i testy symboliczne:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42631778651


## 15. Dodatkowe loci Coxetera między ścianami bocznymi

Poza trzema elipsami (kąt (60^\circ) ściana boczna–ściana trójkątna) i trzema liniami prostopadłości (kąt (90^\circ) ściana boczna–ściana trójkątna), sprawdzono także kąty między parami ścian bocznych.

Dla dwóch krawędzi podstawy (e_i,e_j) zachodzi (e_i\cdot e_j=-1/2). Przy (c_i=e_i\cdot h), (c_j=e_j\cdot h), normalne ścian bocznych spełniają:

\[
n_i\cdot n_j=-\frac12-c_ic_j,\qquad \|n_i\|^2=1-c_i^2.
\]

### 15.1. Trzy krzywe kąta (90^\circ) między ścianami bocznymi

Warunek prostopadłości (n_i\cdot n_j=0) daje (c_ic_j=-1/2). Dla trzech par otrzymujemy:

\[
u^2-\sqrt3uv=1,
\]
\[
u^2+\sqrt3uv=1,
\]
\[
3v^2-u^2=2.
\]

Na tych krzywych odpowiednie odbicia boczne komutują: (s_is_j=s_js_i). Są to dodatkowe krzywe algebraiczne w dysku konfiguracji.

### 15.2. Trzy krzywe kąta (60^\circ) między ścianami bocznymi

Warunek kąta Coxetera (\pi/3) to:

\[
4(n_i\cdot n_j)^2=\|n_i\|^2\|n_j\|^2.
\]

Po podstawieniu otrzymujemy trzy kwartykowe krzywe:

\[
u^4-2\sqrt3u^3v+3u^2v^2-u^2+2\sqrt3uv+v^2=0,
\]
\[
u^4+2\sqrt3u^3v+3u^2v^2-u^2-2\sqrt3uv+v^2=0,
\]
\[
u^4-6u^2v^2+8u^2+9v^4-8v^2=0.
\]

Na nich odpowiednia para odbić bocznych spełnia relację braid długości 3.

### 15.3. Kontrola numeryczna

Skan dodano do `rhombic_prism_mobility_screw_coupling.py`: dla każdej pary ścian wybierane są punkty na krzywych (m=2) i (m=3), a także kontrole przesunięte promieniowo o (10^{-5}).

W reprezentatywnych próbkach:
- krzywe (m=2): 286 różnych map długości 4 (175 obrotów, 102 śruby, 8 translacji, 1 identyczność);
- krzywe (m=3): 314 różnych map długości 4 (186 obrotów, 120 śrub, 8 translacji).

Punkty poza krzywą wracają w tych próbkach do 320 map. Przecięcia tych krzywych z wcześniej opisanymi loci mogą dawać jeszcze większe degeneracje. Wartości są numeryczne; same warunki kątowe i równania krzywych zostały wyprowadzone symbolicznie.

### 15.4. Aktualna mapa relacji Coxetera

W przestrzeni ((u,v)) mamy teraz co najmniej:
- 3 elipsy (m=3) dla par ściana boczna–ściana trójkątna;
- 3 linie (m=2) dla tych samych typów par;
- 3 krzywe (m=2) dla par ściana boczna–ściana boczna;
- 3 krzywe (m=3) dla par ściana boczna–ściana boczna.

To jest mapa podstawowych relacji par odbić, a nie pełna klasyfikacja wszystkich możliwych relacji wyższych rzędów.

Dokładne równania sprawdza `experiments/rhombic_prism_exceptional_affine_relations.py`; numeryczny skan uruchamia workflow:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42632173337


## 14. Korekta modelu afinicznego i mapa przecięć loci (wersja poprawiona)

**Korekta wcześniejszych wyników:** płaszczyzny ścian bocznych nie przechodzą wszystkie przez początek układu. Każda zawiera inną krawędź trójkąta podstawy. Poprawna refleksja w płaszczyźnie o normalnej \(n_i=e_i\times t\), przechodzącej przez punkt \(p_i\), ma postać:
\[
x\longmapsto (I-2n_in_i^T/(n_i\cdot n_i))x
+2n_i(n_i\cdot p_i)/(n_i\cdot n_i).
\]
Kod \`rhombic_prism_mobility_screw_coupling.py\` został poprawiony o te przesunięcia. W konsekwencji **wszystkie wcześniejsze liczby widma liczone dla bocznych płaszczyzn przechodzących przez początek należy uznać za nieaktualne**. Nie wolno ich używać do wniosków o rezonansach.

### 14.1 Dwanaście loci pierwszego i drugiego rodzaju

Rozpatrujemy tylko kąty Coxetera \(\pi/2\) i \(\pi/3\), a nie wszystkie możliwe \(\pi/m\). Wprowadzamy \(X=\sqrt3v\). Wtedy dwanaście warunków jest opisanych wielomianami o współczynnikach wymiernych:

| Para płaszczyzn | \(m=2\) (kąt \(\pi/2\)) | \(m=3\) (kąt \(\pi/3\)) |
|---|---|---|
| Trójkąt – ściana 1 | \(X=0\) | \(3u^2+4X^2-3=0\) |
| Trójkąt – ściana 2 | \(3u+X=0\) | \(39u^2+18uX+7X^2-12=0\) |
| Trójkąt – ściana 3 | \(3u-X=0\) | \(39u^2-18uX+7X^2-12=0\) |
| Ściany 1–2 | \(u^2-uX-1=0\) | \(3u^4-6u^3X+3u^2X^2-3u^2+6uX+X^2=0\) |
| Ściany 1–3 | \(u^2+uX-1=0\) | \(3u^4+6u^3X+3u^2X^2-3u^2-6uX+X^2=0\) |
| Ściany 2–3 | \(u^2-X^2+2=0\) | \(3u^4-6u^2X^2+24u^2+3X^4-8X^2=0\) |

Są to warunki na kąty między normalnymi płaszczyzn, równoważne odpowiednim relacjom Coxetera dla par odbić. Sam warunek kąta jest relacją liniowych części odbić; w przypadku płaszczyzn afinicznych należy dodatkowo sprawdzać pełne przesunięcia, co robią testy afiniczne.

### 14.2 Przecięcia

Dodano \`experiments/rhombic_prism_locus_intersections.py\`. Skrypt:
- buduje wszystkie 12 wielomianów dokładnie w \(\mathbb Q[u,X]\);
- używa resultantów do znalezienia kandydatów przecięć;
- filtruje rozwiązania rzeczywiste wewnątrz dysku \(u^2+X^2/3<1\);
- sprawdza dokładnie konfigurację centralną i sześć punktów potrójnych;
- porównuje długość czwartego poziomu słów odbić przy użyciu poprawnych afinicznych generatorów.

W skanie resultantowym znaleziono 61 izolowanych rzeczywistych przecięć w otwartym dysku: 54 przecięcia dwóch loci, 6 punktów potrójnych i jeden punkt sześciokrotny. Liczba 61 jest wynikiem numerycznej izolacji pierwiastków resultantów, a nie jeszcze formalnym certyfikatem kompletności wszystkich pudełek pierwiastkowych.

### 14.3 Punkty o największej krotności

Punkt centralny:
\[
(u,v)=(0,0)
\]
leży na sześciu loci jednocześnie: trzech warunkach \(m=2\) między ścianami końcowymi i bocznymi oraz trzech warunkach \(m=3\) między parami ścian bocznych.

Sześć punktów potrójnych ma dokładne współrzędne:
\[
(u,X)=\left(\pm\frac2{\sqrt{13}},0\right),
\qquad
(u,X)=\left(\pm\frac1{\sqrt{13}},\pm\frac3{\sqrt{13}}\right).
\]
Każdy leży na jednym locus \(m=2\) i dwóch loci \(m=3\). Ich promień poziomy spełnia:
\[
u^2+v^2=\frac4{13}.
\]

### 14.4 Widmo słów długości 4 — po korekcie afinicznej

Po poprawieniu położeń płaszczyzn bocznych:
- konfiguracja ogólna \((u,v)=(0.31,0.17)\): 320 różnych map;
- punkt centralny \((0,0)\): 65 różnych map;
- każdy z sześciu punktów potrójnych: 213 różnych map.

To są wyniki enumeracji słów długości 4, z numeryczną deduplikacją współczynników afinicznych do 7 miejsc po przecinku. Nie są to liczebności całych grup. Różnica pokazuje, że przecięcia loci rzeczywiście wiążą się z silniejszymi identyfikacjami w krótkich słowach, ale nie dowodzi jeszcze klasyfikacji nieskończonej grupy.

### 14.5 Granice wniosku

1. Dwanaście loci obejmuje wyłącznie \(m=2\) i \(m=3\). Dla \(m\ge4\) mogą istnieć kolejne krzywe Coxetera.
2. Warunek kąta między normalnymi nie wystarcza sam w sobie do ustalenia wszystkich relacji afinicznych; trzeba porównywać także offsety.
3. Liczba 61 przecięć wymaga dalszej certyfikacji algebraicznej (izolacja wszystkich wspólnych pierwiastków w racjonalnych pudełkach).
4. Wcześniejsze wyniki 302, 290, 298 itd. uzyskane dla bocznych płaszczyzn bez właściwych offsetów są wycofane.

### Reprodukcja

\`python experiments/rhombic_prism_locus_intersections.py\`


Walidacja CI dla poprawionego modelu i przecięć:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42633731178

Wynik: PASS. CI odtworzyło 61 przecięć (54 podwójne, 6 potrójnych, 1 sześciokrotne), sprawdziło symbolicznie środek i sześć punktów potrójnych oraz uzyskało 65 map w centrum i 320 w próbce ogólnej.


## 16. Rozwijanie widma śrubowego wokół konfiguracji centralnej

Dodano eksperyment \`experiments/rhombic_prism_central_screw_unfolding.py\`. Dla centrum oraz sześciu kierunków perturbacji o promieniu \(\varepsilon=10^{-3}\) enumeruje on wszystkie 320 zredukowanych słów długości 4 i klasyfikuje wynikowe afiniczne izometrie.

| Konfiguracja | Różne mapy | Śruby | Obroty | Translacje | Identyczność |
|---|---:|---:|---:|---:|---:|
| Centrum \((0,0)\) | 65 | 24 | 30 | 10 | 1 |
| Kierunek \(0^\circ\) | 245 | 84 | 148 | 12 | 1 |
| Kierunek \(30^\circ\) | 320 | 120 | 188 | 12 | 0 |
| Kierunek \(45^\circ\) | 314 | 120 | 186 | 8 | 0 |
| Kierunek \(21.199^\circ\) | 320 | 120 | 192 | 8 | 0 |
| Kierunek \(60^\circ\) | 245 | 84 | 148 | 12 | 1 |
| Kierunek \(90^\circ\) | 320 | 120 | 188 | 12 | 0 |

Wszystkie kierunki poza centrum mają \(\varepsilon=10^{-3}\). W centrum występuje 24 śrubowe mapy długości 4; po perturbacji jest ich 84 na wybranych kierunkach symetrii i 120 w próbkach ogólnych. Rozszczepienie zależy od kierunku.

Wartości bezwzględnego skoku śrubowego pozostają bliskie \(3/2\) i \(2\). Maksymalna zmiana kierunku osi względem najbliższej osi centralnej w tych próbkach wynosi około \(0.1^\circ\). Wynik sugeruje rozszczepienie zdegenerowanych transformacji, a nie gwałtowną zmianę wszystkich kierunków osi.

**Interpretacja:** centrum jest kandydatem na punkt rozgałęzienia (unfolding) rodzin ruchów śrubowych w skończonym widmie odbić. Nie jest to jeszcze dowód bifurkacji całej nieskończonej grupy: zbadano wyłącznie słowa długości 4.

Kod: \`experiments/rhombic_prism_central_screw_unfolding.py\`.

Walidacja CI: https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42635226502 — PASS.


## 17. Test rozszczepienia widma na długościach 2, 4 i 6

Dodano 'experiments/rhombic_prism_screw_unfolding_multidegree.py'. Używa on poprawnych odbić afinicznych i porównuje centrum z perturbacjami o promieniu \(\varepsilon=10^{-2}\). Dla długości 2, 4 i 6 deduplikacja do 11 miejsc daje stabilne wyniki w powtórzonych kierunkach.

### 17.1. Wyniki

| Kierunek perturbacji | Długość słowa | Różne mapy | Ruchy śrubowe |
|---|---:|---:|---:|
| Centrum | 2 | 14 | 0 |
| Centrum | 4 | 65 | 24 |
| Centrum | 6 | 175 | 84 |
| Linie \(0^\circ,60^\circ,120^\circ\) | 2 | 18 | 0 |
| Linie \(0^\circ,60^\circ,120^\circ\) | 4 | 245 | 84 |
| Linie \(0^\circ,60^\circ,120^\circ\) | 6 | 3045 | 1848 |
| Kierunek ogólny \(30^\circ\) lub \(90^\circ\) | 2 | 20 | 0 |
| Kierunek ogólny \(30^\circ\) lub \(90^\circ\) | 4 | 320 | 120 |
| Kierunek ogólny \(30^\circ\) lub \(90^\circ\) | 6 | 5078 | 3400 |
| Kierunek ogólny \(45^\circ\) | 2 | 20 | 0 |
| Kierunek ogólny \(45^\circ\) | 4 | 320 | 120 |
| Kierunek ogólny \(45^\circ\) | 6 | 5102 | 3480 |

Wynik jest zgodny z dokładnymi trzema liniami prostopadłości ściany bocznej do ścian końcowych: \(v=0\), \(v=\sqrt3u\), \(v=-\sqrt3u\). Wzdłuż tych linii widmo jest mniejsze niż w kierunkach ogólnych. Zatem perturbacja centralna nie ma jednego uniwersalnego rozszczepienia — wynik zależy od kierunku.

### 17.2. Osie i skoki

Dla długości 4 i \(\varepsilon=10^{-3}\) największy kąt między osią śruby po perturbacji a najbliższą osią centralną wynosi około \(0.1^\circ\). Przy \(\varepsilon=10^{-2}\) jest około \(1^\circ\), co jest zgodne z małą, w przybliżeniu liniową zmianą osi.

W centrum długości 4 występują wartości bezwzględne skoku \(3/2\) i \(2\). Przy perturbacji długości 4 rozszczepiają się one na bliskie wartości, np. dla kierunku \(u\):
\[
1.49989,\ 1.49994,\ 1.99960,\ 1.99980.
\]
Dla długości 6 pojawiają się już dodatkowe wartości skoków, również małe. Nie wolno więc przenosić wniosku o dwóch wartościach skoku z długości 4 na całe widmo.

### 17.3. Długość 8 — wynik diagnostyczny, nie rozstrzygający

Dla słów długości 8 mamy 327680 zredukowanych słów. W centrum liczba różnych map wynosi 369 i jest stabilna w badanym zakresie precyzji. Po perturbacji deduplikacja zmiennoprzecinkowa staje się wrażliwa na liczbę cyfr: przykładowo dla kierunku ogólnego \(45^\circ\) wynik zmienia się od około 77765 do 81200 przy zmianie zaokrąglenia z 7 do 13 miejsc.

Dlatego liczby długości 8 są raportowane wyłącznie jako test diagnostyczny i **nie są używane jako dowód liczby klas**. Potrzebne są obliczenia z dokładną arytmetyką algebraiczną lub certyfikowanym porównaniem macierzy afinicznych.

### 17.4. Wniosek

Dla długości 2, 4 i 6 istnieje stabilny, kierunkowo zależny obraz rozszczepienia:
- centrum ma największą degenerację spośród przebadanych konfiguracji;
- trzy kierunki szczególne zachowują dodatkowe relacje komutacji;
- kierunki ogólne dają więcej różnych map i ruchów śrubowych;
- przy wzroście długości słowa pojawiają się nowe wartości skoków, więc struktura jest bogatsza niż dwa skoki widoczne na długości 4.

To wspiera obraz centralnej konfiguracji jako punktu wysokiej symetrii w skończonych widmach odbić. Nie dowodzi jeszcze bifurkacji całej nieskończonej grupy.

Reprodukcja:
'experiments/rhombic_prism_screw_unfolding_multidegree.py'


Walidacja GitHub Actions dla całego zestawu testów:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42636469072 — PASS.

W logach CI potwierdzono:
- trzy kierunki szczególne: dla długości 4 = 245 map / 84 śruby; dla długości 6 = 3045 map / 1848 śrub;
- kierunki ogólne 30° i 90°: dla długości 4 = 320 map / 120 śrub; dla długości 6 = 5078 map / 3400 śrub;
- centrum: 14, 65 i 175 map dla długości 2, 4 i 6;
- diagnostykę precyzji długości 8, która potwierdza niestabilność numerycznego deduplikowania poza centrum.


## 18. Przestrzenna organizacja osi śrubowych — wynik wstępny i korekty

Dodano experiments/rhombic_prism_screw_axis_spatial_organization.py. Oś każdej śruby jest rekonstruowana jako prosta w \(\mathbb R^3\): kierunek jednostkowy \(a\) oraz punkt \(p\) najbliższy początkowi układu, z warunkami
\[
(I-M)p=b-(a\cdot b)a,\qquad p\cdot a=0.
\]
Do porównania prostych użyto współrzędnych Plückera \((a,p\times a)\). Różne transformacje mogą dzielić tę samą oś, dlatego raportuje się osobno liczbę map śrubowych i liczbę różnych prostych osi.

### 18.1. Wynik dla długości 4

Przy \(\varepsilon=0.01\), przed odrzuceniem prawie-identycznościowych obrotów, otrzymano:
- centrum: 24 mapy śrubowe, 9 różnych osi;
- trzy kierunki szczególne: 84 mapy śrubowe, 42–44 różne osie;
- kierunki ogólne: 120 map śrubowych, 54–62 różne osie.

To potwierdza, że liczba map śrubowych nie jest liczbą geometrycznie różnych osi.

### 18.2. Długość 6 i problem osi odległych

Dla długości 6 wstępna rekonstrukcja dawała osie o odległościach od początku rzędu \(10^4\)–\(10^5\). To wskazuje na źle uwarunkowane przypadki: gdy kąt części obrotowej zbliża się do zera, oś śruby może odsuwać się bardzo daleko (granica ruchu śrubowego do translacji). Nie należy interpretować takich wartości jako zwartego skupiska osi w pobliżu bryły ani jako dowodu fraktalności.

Dodano filtr minimalnego kąta obrotu \(0.1^\circ\), a następnie zaostrzono go do \(1^\circ\) jako test stabilności. Odrzucone przypadki są liczone osobno jako ill_conditioned_screws; nie są utożsamiane z brakiem śruby. Nawet po filtrze \(0.1^\circ\) część osi pozostawała daleko od początku, co uzasadnia analizę w kilku progach i kontrolę reszt równania osi.

### 18.3. Czy widać fraktal?

Na obecnym etapie **nie ma dowodu fraktalności**. Wykonano tylko skończoną enumerację słów długości 2, 4 i 6. Liczby zajętych pudełek w przestrzeni Plückera rosną na kilku skalach, ale szybko się nasycają; to typowe dla skończonego zbioru punktów i nie wyznacza wymiaru fraktalnego.

Żeby badać fraktalność, trzeba:
1. porównać stabilne osie przy rosnącej długości słów, używając dokładnej lub certyfikowanej arytmetyki;
2. ustalić metrykę na przestrzeni prostych (np. odległość w znormalizowanych współrzędnych Plückera);
3. badać prawo potęgowe \(N(\epsilon)\sim\epsilon^{-D}\) na coraz szerszym zakresie skal, kontrolując zależność od progu kąta;
4. sprawdzić, czy rozkład jest samopodobny, a nie tylko skupiony wokół skończonej liczby osi symetrii.

### 18.4. Korekta liczby słów długości 8

Dla pięciu generatorów i zakazu powtórzenia tego samego generatora bezpośrednio po sobie liczba zredukowanych słów długości \(n\) wynosi:
\[
5\cdot4^{n-1}.
\]
Zatem dla długości 8 jest to \(5\cdot4^7=81920\), a nie 327680. Wcześniejsza liczba 327680 w sekcji 17.3 była błędna i zostaje wycofana.

### 18.5. Walidacja

Pierwsze uruchomienie analizy osi zakończyło się błędem w kontroli typu zwracanej sygnatury; poprawiono go. Poprawione uruchomienie zakończyło się powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42637724150

Dalszy test ze zwiększonym progiem kąta \(1^\circ\) jest osobnym testem stabilności:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42637962973


Test stabilności z progiem \(1^\circ\) również zakończył się PASS:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42637962973

Po zaostrzeniu progu dla długości 6 otrzymano:
- centrum: 30 różnych osi;
- kierunki szczególne: 872–892 osie;
- kierunki ogólne: 1576–1596 osi.

Maksymalne odległości osi od początku nadal dochodzą do około 77 dla kierunków szczególnych i 133 dla ogólnych. To potwierdza, że samo odcięcie obrotów poniżej \(1^\circ\) nie usuwa całego problemu złego uwarunkowania / odległych osi. Box-counting w pięciu skalach pozostaje skończony i szybko się nasyca (np. centrum: 9 pudełek na każdej skali od \(1/4\) wzwyż w dół; nie ma tu zakresu potęgowego wystarczającego do estymacji wymiaru fraktalnego).


## 19. Granica osi obrotów i śrubowych — enumeracja do długości 8

Wprowadzono osobny enumerator experiments/rhombic_prism_axis_limit_study.py. Istotna korekta względem sekcji 18: oś obrotu o zerowym skoku jest również osią geometryczną i musi być liczona. W poprzednim skrypcie była pomijana, bo analizowano tylko śruby z niezerowym skokiem. Nowy skrypt rozdziela:
- rotation_axes: osie obrotów (skok zerowy);
- screw_axes: osie śrub (skok niezerowy);
- translations: translacje, które nie mają skończonej osi;
- near_identity: prawie-identycznościowe części obrotowe, których osie są numerycznie źle uwarunkowane.

### 19.1. Metoda

Dla każdej właściwej izometrii afinicznej \(x\mapsto Mx+b\), z \(M\in SO(3)\) i \(M\ne I\), kierunek osi wyznaczany jest jako wektor osobliwy odpowiadający najmniejszej wartości osobliwej macierzy \(M-I\). Skok osiowy wynosi \(h=a\cdot b\). Punkt osi \(p\), prostopadły do \(a\), spełnia:
\[
(I-M)p=b-ha,\qquad p\cdot a=0.
\]
Wykorzystano SVD i kontrolę reszty równania. Dla porównania prostych użyto współrzędnych Plückera \((a,p\times a)\). Enumeracja dynamicznie zachowuje ostatni generator, więc redukcja słów (zakaz sąsiednich identycznych odbić) jest respektowana, a stany o tej samej transformacji i tym samym ostatnim generatorze mogą być scalane.

### 19.2. Wyniki do długości 8

Próg odrzucenia prawie-identycznościowych obrotów: \(1^\circ\). Liczby unique_lines obejmują teraz zarówno osie obrotów, jak i osie śrub.

| Konfiguracja | Długość 4 | Długość 6 | Długość 8 |
|---|---:|---:|---:|
| Centrum | 30 | 72 | 129 |
| Gałąź symetrii \((u,v)=(0.01,0)\) | 110 | 1395 | 17179 |
| Ogólna \(45^\circ\), \((u,v)=(0.01/\sqrt2,0.01/\sqrt2)\) | 144 | 2285 | 36474 |

W centrum liczba różnych map rośnie od 65 do 175 i 369; w konfiguracji ogólnej od 320 do 5102 i 81173. Na gałęzi symetrii odpowiednio: 245, 3045 i 36889. Dla długości 8 liczba słów zredukowanych wynosi 81920.

### 19.3. Zbieżność zbiorów między głębokościami

Porównano każdą oś z długości \(n\) z najbliższą osią z długości \(n-2\) w sześciowymiarowych współrzędnych Plückera (bez niezależnego przeskalowania zakresów na każdym poziomie).

| Konfiguracja | Porównanie | Mediana najbliższej odległości | Udział osi w odległości < 0.1 |
|---|---|---:|---:|
| Centrum | 4 → 2 | 0.6495 | 30.0% |
| Centrum | 6 → 4 | 0.4330 | 41.7% |
| Centrum | 8 → 6 | \(1.1\cdot10^{-15}\) | 55.8% |
| Gałąź symetrii | 6 → 4 | 0.0200 | 66.0% |
| Gałąź symetrii | 8 → 6 | 0.0113 | 82.7% |
| Ogólna 45° | 6 → 4 | 0.0167 | 68.3% |
| Ogólna 45° | 8 → 6 | 0.00888 | 81.6% |

Dla centrum mediana równa około \(10^{-15}\) oznacza, że ponad połowa osi z długości 8 pokrywa się numerycznie z osią z długości 6. Dla gałęzi symetrii i konfiguracji ogólnej rośnie udział osi leżących blisko zbioru poprzedniej głębokości. Jest to wstępny sygnał zagęszczania skończonych zbiorów osi, ale nie dowód istnienia granicznej powierzchni ani samopodobieństwa.

### 19.4. Rozkład odległości osi i zła kondycja

Maksymalna odległość osi od początku dla długości 8:
- centrum: około 4.09;
- gałąź symetrii: około 174.07;
- konfiguracja ogólna: około 212.12.

Mimo progu kąta \(1^\circ\) pozostają bardzo odległe osie. W długości 8 wykryto 1134 przypadki prawie-identycznościowe na gałęzi symetrii i 4128 w konfiguracji ogólnej. Najmniejszy zaakceptowany kąt wynosił odpowiednio około \(1.98^\circ\) i \(1.19^\circ\). To pokazuje, że próg \(1^\circ\) nie wystarcza do pełnej stabilizacji ogonów rozkładu. Wartości median są znacznie stabilniejsze niż maksima.

Wszystkie zaakceptowane osie przeszły kontrolę reszty: maksymalna reszta wyniosła \(7.73\cdot10^{-14}\), więc problemem nie jest niedomknięcie równania osi, lecz jego uwarunkowanie przy małym kącie obrotu.

### 19.5. Box-counting i interpretacja

Dla stałych skal Plückera \(2,1,1/2,1/4,1/8,1/16\) liczba zajętych pudełek rośnie wraz z głębokością i liczbą osi. Przykładowo dla konfiguracji ogólnej na długości 8 uzyskano:
\[
1514,\ 2419,\ 4185,\ 5183,\ 5845,\ 6326.
\]
To nie jest jeszcze estymacja wymiaru fraktalnego: liczba głębokości jest mała, zbiór jest skończony, a część osi ma duże momenty Plückera. Potrzebne są dalsze głębokości, analiza progów kąta i test stabilności nachylenia \(\log N(\epsilon)\) względem \(\log(1/\epsilon)\).

### 19.6. Status

GitHub Actions zakończył się powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42638629655

Wniosek na dziś: zbiór osi rośnie bardzo szybko poza centrum, a kolejne głębokości coraz bardziej zbliżają się do poprzednich w metryce Plückera. To uzasadnia dalsze badanie granicy, ale nie uprawnia jeszcze do stwierdzenia, że granicą jest fraktal.


## 20. Test stabilności względem progu kąta i widmo kątów

Dodano eksperyment experiments/rhombic_prism_axis_conditioning_sensitivity.py. Dla długości 8 porównano progi odrzucania małych kątów \(1^\circ,2^\circ,5^\circ,10^\circ\). To rozdziela rzeczywistą geometrię zbioru od artefaktów osi bardzo odległych, które powstają przy części obrotowej bliskiej identyczności.

### 20.1. Stabilność osi

| Konfiguracja | Próg | Różne osie | Mediana \(\|p\|\) | 90. percentyl \(\|p\|\) | Maksimum \(\|p\|\) |
|---|---:|---:|---:|---:|---:|
| Gałąź symetrii | 1° | 17179 | 1.083 | 26.00 | 174.07 |
| Gałąź symetrii | 2° | 15133 | 1.020 | 2.039 | 67.66 |
| Gałąź symetrii | 5° | 15041 | 1.015 | 2.030 | 4.10 |
| Gałąź symetrii | 10° | 15041 | 1.015 | 2.030 | 4.10 |
| Ogólna 45° | 1° | 36474 | 1.043 | 24.22 | 212.12 |
| Ogólna 45° | 2° | 33443 | 1.017 | 2.055 | 156.16 |
| Ogólna 45° | 5° | 32100 | 1.014 | 2.038 | 4.10 |
| Ogólna 45° | 10° | 32100 | 1.014 | 2.038 | 4.10 |

Ważna obserwacja: po podniesieniu progu z \(2^\circ\) do \(5^\circ\) maksimum odległości osi spada z 67.7 do 4.10 na gałęzi symetrii i ze 156.2 do 4.10 w konfiguracji ogólnej. Progi \(5^\circ\) i \(10^\circ\) dają identyczne wyniki. Oznacza to, że bardzo odległe osie w tej próbce są związane z małymi kątami obrotu, a nie z typowym rozkładem osi dużych obrotów. Mediany pozostają bliskie 1, więc efekt dotyczy przede wszystkim ogona rozkładu.

### 20.2. Widmo kątów długości 8

Dla dwóch konfiguracji bliskich centrum otrzymano następujące liczby właściwych map z kątem obrotu w kolejnych przedziałach:

| Przedział kąta | Gałąź symetrii | Ogólna 45° |
|---|---:|---:|
| \(0^\circ\)–\(5^\circ\) | 5590 | 12984 |
| \(5^\circ\)–\(30^\circ\) | 0 | 0 |
| \(30^\circ\)–\(60^\circ\) | 0 | 0 |
| \(60^\circ\)–\(90^\circ\) | 0 | 0 |
| \(90^\circ\)–\(120^\circ\) | 3386 | 9364 |
| \(120^\circ\)–\(180^\circ\) | 27470 | 58419 |

W przebadanych konfiguracjach nie występują kąty w przedziale \(5^\circ\)–\(90^\circ\). Próg \(5^\circ\) pozostawia najniższy zaakceptowany kąt około \(119.97^\circ\), a próg \(10^\circ\) nie zmienia już zbioru osi. To wskazuje na rozdzielenie małych kątów, pochodzących od prawie-zanikających relacji centralnych, od dużych obrotów. Jest to obserwacja dla skończonej enumeracji do długości 8 i małych deformacji \(r=0.01\); nie wolno jej uogólniać na całą przestrzeń parametrów.

### 20.3. Następny test konieczny

Ponieważ konfiguracja ogólna z sekcji 19 ma promień zaledwie \(r=0.01\), jest nadal bliska centrum. Dodano zatem skan widma kątów dla większych deformacji \(r=0.3\) i \(r=0.6\), zarówno na gałęzi symetrii, jak i w kierunku \(45^\circ\). Dopiero ten test pokaże, czy obserwowana luka kątowa jest cechą lokalnego rozwinięcia wokół konfiguracji centralnej, czy utrzymuje się dalej w dziedzinie mobilności.

Walidacja testu stabilności i widma kątów:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42639377048


## 21. Mapa widma kątów w dysku parametrów

Skan experiments/rhombic_prism_angle_spectrum_grid.py rozszerzył badanie z trzech punktów do 12 konfiguracji: \(r\in\{0.1,0.3,0.6,0.8\}\), \(\phi\in\{0^\circ,22.5^\circ,45^\circ\}\), gdzie \(u=r\cos\phi,\ v=r\sin\phi\). W każdym punkcie uwzględniono wszystkie różne mapy zredukowanych słów długości 8, a następnie obliczono kąty właściwych części ortogonalnych.

### 21.1. Luka w pobliżu zera jest zależna od położenia w dysku

| \(r\) | \(\phi\) | Liczba kątów < 5° | Największy kąt < 5° | Najmniejszy kąt ≥ 5° |
|---:|---:|---:|---:|---:|
| 0.1 | 0° | 1134 | 1.494° | 19.823° |
| 0.1 | 22.5° | 1758 | 1.670° | 8.656° |
| 0.1 | 45° | 1758 | 1.728° | 5.793° |
| 0.3 | 0° | 32 | 4.159° | 6.935° |
| 0.3 | 22.5° | 586 | 4.099° | 5.826° |
| 0.3 | 45° | 1094 | 4.135° | 7.938° |
| 0.6 | 0° | 0 | — | 12.599° |
| 0.6 | 22.5° | 0 | — | 8.815° |
| 0.6 | 45° | 70 | 3.698° | 12.370° |
| 0.8 | 0° | 0 | — | 11.066° |
| 0.8 | 22.5° | 186 | 3.561° | 11.973° |
| 0.8 | 45° | 0 | — | 5.814° |

Wynik jest wyraźnie anizotropowy: liczba małych kątów zależy nie tylko od promienia deformacji, lecz również od kierunku w płaszczyźnie \((u,v)\). Na osi symetrii \(\phi=0^\circ\) dla \(r=0.6\) i \(0.8\) nie ma w tej próbce kątów poniżej \(5^\circ\). W kierunku \(45^\circ\) przy \(r=0.6\) pozostaje 70 takich przypadków, a przy \(r=0.8\) nie ma ich wcale.

### 21.2. Największe przerwy w całym widmie

Dla małych deformacji i kierunku symetrii pojawiają się duże luki nie tylko przy zerze. Przykładowo dla \(r=0.1,\phi=0^\circ\) największa przerwa między kolejnymi różnymi kątami wynosi około \(77.23^\circ\), od \(39.80^\circ\) do \(117.03^\circ\). Dla \(r=0.1,\phi=45^\circ\) analogiczna przerwa wynosi około \(72.89^\circ\), od \(44.36^\circ\) do \(117.25^\circ\). Wraz z deformacją widmo w kierunkach ogólnych staje się znacznie gęstsze; przy \(r=0.8,\phi=45^\circ\) największa z pięciu raportowanych luk wynosi około \(6.11^\circ\).

### 21.3. Interpretacja i ograniczenia

Nie ma podstaw do stwierdzenia, że istnieje uniwersalna luka kątowa dla całej rodziny. Wartość \(5^\circ\) jest wyłącznie progiem diagnostycznym; w niektórych punktach najmniejszy kąt powyżej progu jest bliski \(5^\circ\), w innych przekracza \(19^\circ\), a w kilku konfiguracjach nie ma żadnych kątów poniżej progu.

Dodatkowo kąty są liczone z części liniowej izometrii, a nie z położenia osi afinicznej. Widmo nie rozstrzyga więc o zbieżności osi ani o strukturze granicznej ich zbioru. Następny krok powinien mapować liczbę małych kątów oraz największe luki na gęstszej siatce parametrów, a także porównywać wyniki dla różnych głębokości słów.

Walidacja pełnego skanu:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42640831774


## 22. Zagęszczenie siatki widma — eksperyment rozszerzony

Zmieniono eksperyment rhombic_prism_angle_spectrum_grid.py z siatki 12 punktów na siatkę polarną 56 punktów:
\[
r\in\{0.1,0.2,\ldots,0.8\},\qquad
\phi\in\{0^\circ,10^\circ,\ldots,60^\circ\}.
\]
Każdy punkt używa enumeracji zredukowanych słów długości 8 i raportuje liczbę różnych map, liczbę kątów poniżej \(5^\circ\), skrajne kąty po obu stronach progu oraz pięć największych przerw między kolejnymi różnymi wartościami kąta.

### 22.1. Status reprodukcji

Kod i workflow zostały zapisane w repozytorium. Przebieg:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42641203910

W chwili zapisu dokumentacji wszystkie wcześniejsze kroki workflow zakończyły się powodzeniem, a ostatni krok — mapa 56-punktowa — pozostawał w toku. Nie przypisuje się więc temu rozszerzonemu skanowi żadnych wyników liczbowych przed pobraniem logów zakończonego kroku.

### 22.2. Pytania, które rozstrzygnie siatka

1. Czy obszary z brakiem małych kątów tworzą spójne sektory, czy są rozdzielone wąskimi krzywymi rezonansowymi?
2. Czy granice tych sektorów pokrywają się z wcześniej wyprowadzonymi loci Coxetera, czy występują niezależnie?
3. Czy liczba kątów bliskich zeru zmienia się skokowo przy przechodzeniu przez szczególne krzywe?
4. Czy największe luki widma są stabilne względem promienia i kierunku, czy znikają po zagęszczeniu siatki?

Ograniczenie: stały próg 5° jest narzędziem diagnostycznym, nie matematyczną granicą widma. W analizie końcowej należy zachować surowe wartości kątów i porównywać widma bez progu, a także wykonać test zbieżności po długości słowa.


## 23. Wyniki siatki 56-punktowej — anizotropia i symetria dihedralna

Skan zakończył się powodzeniem w GitHub Actions 42641203910. Wszystkie 56 punktów zostało policzonych dla zredukowanych słów długości 8.

### 23.1. Liczba kątów poniżej 5°

| \(r\backslash\phi\) | 0° | 10° | 20° | 30° | 40° | 50° | 60° |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 1134 | 4182 | 1758 | 1202 | 1758 | 4182 | 1134 |
| 0.2 | 1024 | 1692 | 1692 | 1124 | 1692 | 1692 | 1024 |
| 0.3 | 32 | 574 | 574 | 0 | 574 | 574 | 32 |
| 0.4 | 0 | 54 | 520 | 0 | 520 | 54 | 0 |
| 0.5 | 0 | 16 | 112 | 0 | 112 | 16 | 0 |
| 0.6 | 0 | 112 | 0 | 0 | 0 | 112 | 0 |
| 0.7 | 2 | 2 | 8 | 160 | 8 | 2 | 2 |
| 0.8 | 0 | 162 | 122 | 0 | 122 | 162 | 0 |

Wartość 0 oznacza, że żadna z właściwych części liniowych w skończonym zbiorze długości 8 nie ma kąta poniżej \(5^\circ\). Nie oznacza to dodatniej luki dla całej nieskończonej grupy.

### 23.2. Luka przy progu 5° może być bardzo mała

Najmniejsza różnica między największym kątem poniżej \(5^\circ\) a najmniejszym kątem powyżej \(5^\circ\) w całej siatce występuje dla \(r=0.4,\phi=20^\circ\) i wynosi zaledwie około \(0.1234^\circ\). Dla \(r=0.8,\phi=20^\circ\) jest to około \(0.5590^\circ\). Są to przykłady, dlaczego nie wolno interpretować progu 5° jako naturalnej granicy widma.

Największa luka przy progu 5° wśród punktów, w których występują kąty po obu stronach progu, wynosi około \(27.97^\circ\) dla \(r=0.7,\phi=0^\circ\) i symetrycznego punktu \(\phi=60^\circ\).

### 23.3. Symetria względem \(\phi=30^\circ\)

Dla każdego promienia wyniki w parach:
\[
0^\circ\leftrightarrow60^\circ,\quad
10^\circ\leftrightarrow50^\circ,\quad
20^\circ\leftrightarrow40^\circ
\]
są identyczne w tabeli liczby kątów poniżej \(5^\circ\). To jest zgodne z odbiciową symetrią równobocznej podstawy, która działa na dysku parametrów jako odbicie względem osi \(\phi=30^\circ\). Punkty na osi symetrii mają dodatkowy stabilizator, co w niektórych promieniach zmienia liczbę różnych map.

To ważny test kontrolny: rozkład nie jest dowolną anizotropią numeryczną, lecz wykazuje wzór zgodny z grupą symetrii \(D_3\) trójkąta. Następny test powinien porównać całe multizbiory kątów dla par odbitych, nie tylko liczbę wartości poniżej progu.

### 23.4. Wniosek

W skończonej głębokości widmo kątowe jest wyraźnie zależne od parametrów i kierunku, a jego statystyki respektują symetrię trójkąta. Widzimy sektory bez małych kątów, sektory z dużą liczbą małych kątów oraz obszary, w których próg 5° przecina widmo niemal bez przerwy.

To jest dowód na bogatą strukturę skończonego widma, nie na fraktalność. Kluczowy następny eksperyment: sprawdzenie pełnej symetrii widm oraz porównanie głębokości 4, 6 i 8 w tych samych punktach parametrów.


## 24. Test pełnego widma pod symetrią \(D_3\)

Sama zgodność liczby kątów poniżej \(5^\circ\) dla par \(\phi\) i \(60^\circ-\phi\) nie wystarcza. Dodano osobny test, który porównuje całe posortowane multizbiory kątów obrotu (po zaokrągleniu do \(10^{-7}\) stopnia) dla 24 par punktów:
\[
r\in\{0.1,\ldots,0.8\},\qquad
\phi\in\{0^\circ,10^\circ,20^\circ\},\qquad
\phi'=60^\circ-\phi.
\]
Test wymaga zgodności liczby różnych map oraz identyczności całego multizbioru kątów. To bezpośrednio sprawdza, czy widmo numeryczne zachowuje odbiciową symetrię trójkąta, a nie tylko jedną statystykę progową.

Kod: experiments/rhombic_prism_angular_spectrum_symmetry_check.py

Workflow:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42642429432

Status: oczekuje na wykonanie CI. Wynik zostanie dopisany po zakończeniu testu.


## 25. Zbieżność rozkładów widma między długościami słów

Dodano eksperyment rhombic_prism_angular_spectrum_depth_convergence.py. Dla sześciu konfiguracji porównuje on długości słów 4, 6 i 8, raportując:
- liczbę różnych map i kątów;
- liczbę kątów poniżej 1°, 5° i 10°;
- kwantyle rozkładu kątów;
- jednowymiarową odległość Wassersteina między empirycznymi rozkładami kątów dla głębokości 4→6 i 6→8.

Wybrane punkty obejmują centrum, oś symetrii, oś \(\phi=30^\circ\) przy trzech promieniach oraz punkt ogólny poza osią symetrii.

Odległość Wassersteina jest użyta jako diagnostyka zmian rozkładu, a nie jako dowód zbieżności grupy lub zbioru osi. Rozkłady mogą się stabilizować statystycznie, mimo że ich nośniki nadal rosną. Z tego powodu w interpretacji należy odróżnić:
1. stabilizację kwantyli i rozkładu kątów;
2. zbieżność zbiorów osi w przestrzeni Plückera;
3. zbieżność całej grupy generowanej przez odbicia.

Kod został dodany do workflow CI; jego wynik będzie oceniony razem z pełnym testem symetrii \(D_3\).


## 26. Korekta testu D3: pojedyncza niezgodność na promieniu r=0.4

Pełny test multizbiorów kątów nie przeszedł w dwóch przebiegach CI. W 23 z 24 par widm uzyskano identyczne liczby map i identyczne multizbiory kątów. Jedyna niezgodność występuje dla:
\[
(r,\phi)=(0.4,0^\circ),\qquad (r,\phi')=(0.4,60^\circ).
\]
Enumerator zwrócił odpowiednio 36 889 i 36 991 różnych map, a liczby kątów wyniosły 36 446 i 36 548. Różnica wynosi 102.

Nie należy traktować tego jako obalenia symetrii D3, ale też nie wolno ignorować niepowodzenia. Możliwe źródła:
- numeryczne rozszczepienie map, które powinny być identyczne w szczególnym punkcie parametrycznym;
- zależność deduplikacji od zaokrągleń STATE_DECIMALS=12 i MAP_DECIMALS=10;
- błędne przyporządkowanie generatorów lub nieprawidłowa macierz sprzężenia symetrii;
- rzeczywista niezgodność modelu, jeśli geometria generatorów nie zachowuje zakładanej akcji D3.

Ważna obserwacja z wcześniejszej siatki: dla obu punktów liczba różnych wartości kątów jest taka sama (49), choć liczby map różnią się. To sugeruje, że nośnik widma może być symetryczny, a problem dotyczyć krotności lub deduplikacji. Jest to wskazówka diagnostyczna, nie rozstrzygnięcie.

Dodano experiments/rhombic_prism_d3_degeneracy_diagnostic.py, który:
1. sprawdza sprzężenie zbioru pięciu generatorów przez odbicie przestrzenne o osi poziomej phi=30 stopni;
2. enumeruje wszystkie zredukowane słowa długości 8 bez scalania stanów pośrednich;
3. porównuje liczbę map przy precyzjach zaokrąglenia 12, 10, 9, 8, 7 i 6 miejsc;
4. porównuje zbiory różnych kątów bez krotności.

Dopiero te testy pozwolą rozdzielić błąd modelu od artefaktu numerycznej deduplikacji. Do czasu ich zakończenia status symetrii pełnego multizbioru pozostaje niepotwierdzony.


## 27. Korekta diagnostyki sprzężenia i rozdzielenie widma od krotności

W pierwszej wersji diagnostyki użyto macierzy \(2dd^\top-I\), która jest obrotem o \(180^\circ\) wokół osi \(d\), a nie odbiciem w pionowej płaszczyźnie zawierającej \(d\) i oś \(z\). Był to błąd testu pomocniczego, nie geometrii generatorów. Poprawna macierz odbicia ma postać:
\[
S=I-2nn^\top,\qquad n=(-\sin30^\circ,\cos30^\circ,0).
\]
Po poprawce reszty dopasowania pięciu generatorów dla punktów \((0.4,0)\) i \((0.2,0.4\sin60^\circ)\) spadły do poziomu \(10^{-16}\).

To pokazuje, że zbiór generatorów jest sprzężony przez właściwe odbicie przestrzenne. Mimo tego liczby różnych map uzyskane przez zaokrąglanie i deduplikację nadal różnią się zależnie od precyzji. Wcześniejsza diagnostyka wykazała jednocześnie identyczny zbiór 49 różnych wartości kątów po obu stronach. Zatem należy rozdzielić:
- **nośnik widma** — zbiór różnych wartości kątów, który można porównywać niezależnie od krotności;
- **krotności map** — zależne od numerycznej identyfikacji przekształceń i wymagające stabilnego grupowania z tolerancją;
- **dokładną symetrię grupy** — najlepiej testowaną przez sprzężenie generatorów i porównanie przekształceń odpowiadających tym samym słowom po permutacji generatorów.

Test D3 zmieniono więc tak, aby jawnie sprawdzał nośnik widma, a osobny test sprawdzał sprzężenie generatorów słowo po słowie. Nie będziemy już nazywać zgodności nośnika zgodnością pełnego multizbioru. Krotności pozostają osobnym otwartym problemem numerycznym.


## 28. Rozstrzygnięcie niezgodności \(D_3\) na \(r=0.4\)

Dedykowany test CI zakończył się sukcesem. Dla odbicia przestrzennego względem pionowej płaszczyzny o kierunku \(\phi=30^\circ\) otrzymano permutację generatorów:
\[
(0,1,2,3,4)\mapsto(0,1,4,3,2).
\]
Maksymalna reszta sprzężenia pojedynczych generatorów wynosi \(6.1\cdot10^{-16}\).

Co ważniejsze, porównano wszystkie 81 920 zredukowanych słów długości 8, stosując powyższą permutację generatorów. Dla odpowiadających sobie słów:
- maksymalna norma różnicy macierzy po sprzężeniu: \(2.22\cdot10^{-15}\);
- maksymalna norma różnicy wektorów przesunięcia: \(4.52\cdot10^{-15}\).

To jest mocny numeryczny dowód, że **działanie \(D_3\) jest zachowane słowo po słowie** w tej parze konfiguracji, z dokładnością maszynową.

Liczby różnych map po niezależnej deduplikacji zaokrąglonych współczynników nadal są różne (np. 36 889 kontra 37 114 przy 12 miejscach). Liczby te zmieniają się niemonotonicznie przy zmianie precyzji zaokrąglenia. Nie są zatem wiarygodnym niezmiennikiem symetrii: ta sama mapa może zostać rozszczepiona na kilka kluczy numerycznych w jednej reprezentacji, a scalona w drugiej.

Zbiory różnych kątów są natomiast identyczne: 49 wartości po obu stronach, maksymalna różnica \(0\) po zaokrągleniu do \(10^{-7}\) stopnia.

**Wniosek:** wcześniejszy czerwony test nie ujawnił złamania symetrii geometrii. Ujawnił niestabilność deduplikacji map przez zaokrąglanie. Test pełnego widma zmieniono na test nośnika widma, a niezależny test słowo-po-słowie weryfikuje sprzężenie generatorów. Krotności różnych map pozostają osobnym zagadnieniem obliczeniowym.

Dedykowany przebieg CI:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42645102180


## 29. Audyt geometrii zbioru osi w przestrzeni Plückera

Rozpoczęto nowy etap: zamiast porównywać same kąty obrotu, analizujemy osie wszystkich właściwych izometrii afinicznych uzyskanych z parzystych zredukowanych słów odbić.

### 29.1. Reprezentacja osi

Dla izometrii
\[
x\mapsto Rx+b
\]
z właściwą częścią obrotową \(R\ne I\), oś śrubowa jest prostą o kierunku jednostkowym \(a\), najbliższym początku punkcie \(p\) spełniającym \(p\cdot a=0\), oraz skoku:
\[
h=a\cdot b.
\]
Prostą można opisać współrzędnymi Plückera:
\[
L=(a,m),\qquad m=p\times a.
\]
Przyjęta konwencja orientuje kierunek prostej kanonicznie, aby uniknąć podwójnego zapisu \((a,m)\sim(-a,-m)\).

Ważne rozróżnienie: obrót ma \(h=0\), a ruch śrubowy ma \(h\ne0\). Oba przypadki mają oś i muszą być analizowane łącznie. Translacje nie mają skończonej osi.

### 29.2. Zbiór kumulacyjny zamiast powłoki dokładnej długości

Poprzednie skrypty porównywały zbiory słów o dokładnych długościach 2, 4, 6 i 8. Takie powłoki nie są zagnieżdżone. Nowy audyt buduje zbiory kumulacyjne: na poziomie n uwzględnia wszystkie właściwe izometrie reprezentowane przez parzyste zredukowane słowa długości nie większej niż n.

To pozwala sensownie pytać, czy nowe osie z kolejnych poziomów:
- zbliżają się do osi już znalezionych;
- wypełniają nowe obszary przestrzeni Plückera;
- zwiększają zasięg zbioru bez oznak stabilizacji.

### 29.3. Metryki i testy

Dodano experiments/rhombic_prism_axis_geometry_limit_audit.py. Dla centrum, punktu bliskiego centrum na gałęzi symetrii oraz dwóch konfiguracji ogólnych oblicza:
- liczbę map i osi w zbiorach kumulacyjnych dla głębokości 2, 4, 6, 8;
- statystyki położenia osi, skoku i kąta;
- odległości najbliższego sąsiada między nowymi i poprzednimi zbiorami w sześciowymiarowej reprezentacji Plückera;
- zajętość komórek w stałej, wspólnej normalizacji dla wszystkich głębokości;
- wrażliwość liczby osi na próg odrzucania niemal identyczności: 0.5°, 1°, 2° i 5°.

Normalizacja komórek jest wspólna dla wszystkich głębokości w danej konfiguracji. Nie dopasowuje się osobnej skali do każdego poziomu, ponieważ mogłoby to sztucznie sugerować stabilizację wymiaru.

### 29.4. Ograniczenia interpretacji

Zajętość komórek w przestrzeni Plückera jest diagnostyką rozkładu skończonego zbioru, nie estymatorem wymiaru Hausdorffa. Mała odległość nowych osi od poprzedniego zbioru nie dowodzi zbieżności Hausdorffa, jeśli jednocześnie rośnie średnica lub pojawiają się rzadkie odległe punkty. Wyniki trzeba interpretować łącznie z ogonami rozkładu odległości, skokami i zależnością od progu kąta.

Kod został włączony do głównego workflow:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42647520695

**Pytanie badawcze tego etapu:** czy rodzina osi tworzy ograniczony, coraz gęściej próbkowany zbiór w przestrzeni prostych, czy też jej zasięg rośnie wraz z długością słów? Dopiero po rozstrzygnięciu tej kwestii ma sens testowanie fraktalności.
