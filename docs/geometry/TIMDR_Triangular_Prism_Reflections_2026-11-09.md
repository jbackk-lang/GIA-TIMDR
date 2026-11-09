# TIMDR — regularny graniastosłup trójkątny: 3 kwadraty + 2 trójkąty

**Data:** 2026-11-09  
**Model:** graniastosłup prosty o podstawie trójkąta równobocznego; wysokość równa bokowi podstawy, więc ściany boczne są kwadratami.  
**Status:** dokładny model z `sqrt(3)`, sprawdzony w CI.

## 1. To nie jest ta sama bryła co ścięty czworościan

Obie bryły mają pięć ścian, ale inną geometrię:
- ścięty czworościan: dwa trójkąty o różnych rozmiarach i trzy trapezy;
- badany tutaj graniastosłup: dwa przystające trójkąty równoboczne i trzy kwadraty.

Współrzędne trójkąta podstawy:
[
(0,0),quad (1,0),quad (1/2,sqrt3/2).
]
Górna podstawa leży na (z=1). Pięć płaszczyzn odbicia:
[
z=0,quad z=1,quad y=0,quad sqrt3x+y=sqrt3,quad sqrt3x-y=0.
]

## 2. Złożenia par odbić

Wszystkich par ścian jest 10:
- 3 pary ścian bocznych: obroty o (120^circ), rząd 3;
- 6 par ściany bocznej i trójkątnej: półobroty (180^circ), rząd 2;
- 1 para równoległych trójkątów: translacja o długości 2 wzdłuż osi graniastosłupa.

Zatem:
[
oxed{9 	ext{obrotów} + 1 	ext{translacja}}
]
Cosinusy kątów obrotów:
[
cos 120^circ=-1/2,qquad cos 180^circ=-1.
]
W przeciwieństwie do poprzedniej bryły, wszystkie obroty pochodzące z par ścian bocznych są okresowe.

## 3. Struktura całej grupy odbić

Trzy pionowe płaszczyzny boczne generują grupę odbić trójkątnego parkietażu równobocznego — afiniczną grupę Coxetera (widetilde A_2). Jej działanie w płaszczyźnie podstawy zawiera dwuwymiarową sieć translacji.

Dwie równoległe płaszczyzny (z=0) i (z=1) generują nieskończoną grupę dwuścienną: odbicia i translacje w osi (z).

Odbicia poziome komutują z pionowymi, więc cała grupa rozkłada się jako:
[
oxed{widetilde A_2	imes D_infty}.
]
Podgrupa translacji ma rangę 3: dwa niezależne kierunki w płaszczyźnie trójkątnego parkietażu i jeden wzdłuż osi graniastosłupa.

## 4. Czy powstają helisy?

W tym idealnym modelu — nie z samych odbić ścian. Powód jest strukturalny:
- pionowe odbicia zmieniają tylko współrzędne (x,y);
- poziome odbicia zmieniają tylko (z);
- oba rodzaje działań komutują i nie mieszają osi z płaszczyzną.

Dlatego każda otrzymana izometria rozdziela się na ruch w płaszczyźnie podstawy i niezależny ruch wzdłuż osi. Nie powstaje składowa śrubowa, czyli obrót sprzężony z przesunięciem wzdłuż własnej osi.

To ważny kontrast wobec ściętego czworościanu, gdzie płaszczyzny nie rozdzielały się na taki ortogonalny układ i pojawiały się ruchy śrubowe z parametrem skoku.

## 5. Wniosek porównawczy dla TIMDR

Sama liczba ścian (2 trójkąty + 3 czworokąty) nie wyznacza zachowania odbić. Decyduje wzajemne ustawienie płaszczyzn:
- w ściętym czworościanie: translacja + obroty o nieokresowych kątach w niektórych złożeniach wielokrotnych; pojawiają się ruchy śrubowe;
- w graniastosłupie z kwadratami: regularny trójkątny parkietaż w poziomie i niezależne odbicia w pionie; brak ruchów śrubowych.

To wskazuje, że dla TIMDR należy klasyfikować nie tylko typy ścian, lecz przede wszystkim kąty dwuścienne, przecięcia osi oraz to, czy odbicia mieszają kierunek osiowy z kierunkami poprzecznymi.

## 6. Reprodukcja

`python experiments/triangular_prism_reflections.py`

Workflow:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42606597353
