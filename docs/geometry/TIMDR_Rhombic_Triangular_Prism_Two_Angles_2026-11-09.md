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
