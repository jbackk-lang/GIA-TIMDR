# TIMDR — graniastosłup trójkątny z trzema rombami: dwa przypadki kątowe

**Data:** 2026-11-09  
**Kod:** `experiments/rhombic_triangular_prism_two_angles.py`  
**Status:** dokładne obliczenia symboliczne; dwa zestawy kątów; CI uruchomione.

## 1. Ważne ograniczenie geometrii

Dla zamkniętej bryły o topologii graniastosłupa trójkątnego, jeśli wszystkie trzy ściany boczne są dokładnymi rombami, oba trójkątne końce muszą być przystające i równoboczne.

Uzasadnienie: każda ściana boczna jest równoległobokiem złożonym z krawędzi trójkąta i wspólnej krawędzi łączącej oba końce. Warunek rombu wymusza równość długości tych krawędzi. Dla wszystkich trzech ścian oznacza to, że wszystkie trzy boki trójkąta mają tę samą długość. Odpowiednie boki drugiego końca są równe im z własności rombu.

Zatem nie można jednocześnie zachować dokładnych trzech rombów i dowolnie zdeformować trójkątów do niesymetrycznych. Można natomiast zmieniać skręcenie/przesunięcie jednego równobocznego końca względem drugiego. To właśnie parametrów używa eksperyment.

## 2. Parametryzacja

Długość krawędzi przyjmujemy równą 1. Kierunki boków dolnego trójkąta:
[
e_1=(1,0,0),quad e_2=(-1/2,sqrt3/2,0),quad
e_3=(-1/2,-sqrt3/2,0).
]
Wektor przesunięcia dolnego trójkąta do górnego to (t), przy czym (|t|=1). Wtedy każda ściana boczna jest rombem.

Niech:
[
c_i=tcdot e_i=cos	heta_i.
]
Ponieważ (e_1+e_2+e_3=0), mamy warunek:
[
oxed{c_1+c_2+c_3=0}.
]
Aby istniała rzeczywista wysokość graniastosłupa, musi być spełniony warunek:
[
t_z^2=1-c_1^2-rac{(2c_2+c_1)^2}{3}>0.
]
Zatem dwa kąty nie są niezależne od trzeciego; geometria wymusza trzeci.

## 3. Dwa dokładne przypadki

**Przypadek A:** (c_1=1/2, c_2=0). Wtedy (c_3=-1/2). Ostre kąty rombów to (60^circ,90^circ,60^circ). Wysokość:
[
h=sqrt{2/3}.
]

**Przypadek B:** (c_1=1/2, c_2=1/4). Wtedy (c_3=-3/4). Ostre kąty rombów to (60^circ,arccos(1/4),arccos(3/4)), czyli w przybliżeniu (60^circ,75.522^circ,41.410^circ). Wysokość:
[
h=sqrt{5/12}.
]

## 4. Odbicia

Dla każdego przypadku tworzymy pięć dokładnych płaszczyzn odbicia:
- dwie równoległe płaszczyzny trójkątów;
- trzy płaszczyzny bocznych rombów.

Dla 10 par płaszczyzn sprawdzamy typ złożenia odbić, cosinus kąta obrotu oraz translację między równoległymi ścianami. Wyniki liczone są symbolicznie w (mathbb Q(sqrt3,sqrt{2/3})) lub (mathbb Q(sqrt3,sqrt{5/12})), bez przybliżeń zmiennoprzecinkowych.

## 5. Pytanie badawcze

Czy zmiana dwóch kątów rombów zmienia:
- widmo kątów obrotów generowanych przez pary odbić;
- długość translacji wzdłuż osi;
- możliwość powstawania ruchów śrubowych w złożeniach wielokrotnych?

Nie zakładamy z góry, że odpowiedź jest taka sama dla obu przypadków.


## 6. Wyniki dokładnych testów par odbić

CI zakończyło się powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42607218699

W obu przypadkach występuje jedna translacja (złożenie odbić w dwóch równoległych płaszczyznach końcowych) i dziewięć obrotów (pozostałe pary płaszczyzn).

**Przypadek A** — kąty ostre rombów (60^circ,90^circ,60^circ):
- wysokość: (sqrt6/3);
- długość translacji: (2sqrt6/3);
- cosinusy kątów obrotu: (-7/9) (5 par) oraz (-1/3) (4 pary).

**Przypadek B** — kąty ostre rombów (60^circ,arccos(1/4),arccos(3/4)), czyli około (60^circ,75.522^circ,41.410^circ):
- wysokość: (sqrt{15}/6);
- długość translacji: (sqrt{15}/3);
- cosinusy kątów obrotu: (-1/9) (2 pary), (1/9) (3 pary), (-19/21) (3 pary), (-11/21) (1 para).

Zmiana dwóch parametrów kątowych zmienia więc całe widmo obrotów generowanych przez pary odbić, a nie tylko długość translacji. W obu przypadkach niektóre kąty obrotu są inne niż w symetrycznym graniastosłupie z kwadratami.

Wyniki są dokładne i symboliczne; nie rozstrzygają jeszcze, czy złożenia trzech lub większej liczby odbić dają ruchy śrubowe. To następny test.


## 7. Wielokrotne odbicia: osie obrotów i ruchy śrubowe

Rozszerzono eksperyment poza pary odbić. Enumerujemy wszystkie zredukowane słowa generatorów długości 2 i 4 (bez sąsiedniego powtórzenia tego samego odbicia), łącznie odpowiednio 20 i 320 słów dla każdego przypadku. Transformacje afiniczne są porównywane dokładnie, a nie numerycznie.

### Liczba różnych transformacji

| Przypadek | Długość słowa | Słowa | Różne mapy | Kolizje |
|---|---:|---:|---:|---:|
| A | 2 | 20 | 18 | 2 |
| A | 4 | 320 | 245 | 75 |
| B | 2 | 20 | 20 | 0 |
| B | 4 | 320 | 292 | 28 |

### Klasy izometrii dla różnych map długości 4

| Przypadek | Obroty | Ruchy śrubowe | Translacje | Identyczność |
|---|---:|---:|---:|---:|
| A | 176 | 60 | 8 | 1 |
| B | 212 | 72 | 8 | 0 |

To jest kluczowy wynik: **w obu zamkniętych graniastosłupach z trzema rombami pojawiają się ruchy śrubowe w złożeniach czterech odbić**, mimo że dla par odbić otrzymywaliśmy wyłącznie czyste obroty lub translację.

### Kierunki osi

Liczba różnych kierunków osi (kierunek, nie położenie konkretnej osi):
| Przypadek | Osie obrotów | Kierunki osi ruchów śrubowych |
|---|---:|---:|
| A | 27 | 8 |
| B | 37 | 8 |

W obu przypadkach osie śrubowe nie redukują się do jednego kierunku. W drugim przypadku widmo osi obrotów jest bogatsze, ale liczba kierunków osi śrubowych pozostaje taka sama.

### Skok ruchu śrubowego

Dla wektora kierunku osi (u) wyznaczamy niezmiennik:
[
p^2=\frac{(u\cdot b)^2}{u\cdot u},
]
gdzie (x\mapsto Mx+b) jest badaną izometrią. To kwadrat przesunięcia wzdłuż osi na jedno zastosowanie transformacji, niezależny od skali i znaku wektora (u).

**Przypadek A:**
| (p^2) | Liczba różnych map |
|---:|---:|
| (16/9) | 36 |
| (16/13) | 16 |
| (16/7) | 8 |

**Przypadek B:**
| (p^2) | Liczba różnych map |
|---:|---:|
| (25/36) | 48 |
| (25/76) | 8 |
| (25/28) | 8 |
| (25/46) | 8 |

Wyniki pokazują, że zmiana geometrii rombów zmienia zarówno widmo kątów, jak i skoki ruchów śrubowych. Nie jest to wyłącznie zmiana wysokości graniastosłupa.

### Granice wniosku

To są dokładne wyniki dla słów długości najwyżej 4. Nie dowodzą, że cała grupa ma tylko te osie lub skoki, ani że trajektorie tworzą zamknięte węzły. Kierunki osi nie określają jeszcze położenia osi w przestrzeni: do badania wzajemnego splątania potrzebne będą również linie osi, a nie tylko ich wektory kierunkowe.

Kod eksperymentu został rozszerzony o klasyfikację map, kierunków osi i niezmienników skoku.


### Położenie osi: równoległe, przecinające się czy skośne?

Samo liczenie kierunków osi nie wystarcza. Wyznaczyliśmy więc dla każdej śruby również konkretną prostą osiową, reprezentowaną przez kierunek oraz punkt tej prostej najbliższy początkowi układu. Następnie porównaliśmy wszystkie nieuporządkowane pary różnych osi.

| Relacja między osiami | A: 60°/90° | B: niesymetryczne kąty |
|---|---:|---:|
| Różne proste osiowe | 26 | 36 |
| Pary równoległe | 57 | 174 |
| Pary przecinające się | 18 | 24 |
| Pary skośne | 250 | 432 |

Liczności sumują się odpowiednio do (inom{26}{2}=325) i (inom{36}{2}=630). Nie ma par osi pokrywających się, ponieważ identyczne proste zostały scalone.

To istotna różnica między wariantami. Wariant B ma więcej osi i znacznie więcej relacji równoległości oraz skośności. Nie powstaje jedna wspólna oś helikalna; pojawia się wieloosiowa sieć prostych w przestrzeni. To może być właściwszy obiekt do dalszego badania niż pojedyncza helisa.

Wynik dotyczy osi 60 i 72 różnych ruchów śrubowych znalezionych w enumeracji długości 4; nie jest klasyfikacją całej nieskończonej grupy.


## 8. Walidacja końcowa

Pełny eksperyment — łącznie z wyznaczaniem prostych osiowych i klasyfikacją każdej pary osi — zakończył się powodzeniem w GitHub Actions:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42611238641

CI potwierdziło dokładnie:
- A: 26 prostych osiowych; 57 par równoległych, 18 przecinających się, 250 skośnych;
- B: 36 prostych osiowych; 174 pary równoległe, 24 przecinające się, 432 skośne.

Wszystkie relacje obliczono symbolicznie, bez progów tolerancji numerycznej.
