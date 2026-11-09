# Ograniczenie otoczenia: podwójna reprezentacja czworościanu na sferze albo powierzchnia jajowata

**Data:** 2026-11-09  
**Status:** hipoteza konstrukcyjna autora zapisana; rozdzielono dwa warianty do testu. Nie jest to jeszcze dowód fizycznego mechanizmu TIMDR.

## 1. Warunek przekazany przez autora

Czworościan reprezentowany przez cztery wierzchołki nie może być badany wyłącznie jako izolowany łańcuch odbić. Trzeba uwzględnić jego ograniczenie przez otoczenie:
- wariant sferyczny: potrzebna może być **podwójna reprezentacja** czworościanu;
- wariant alternatywny: otoczeniem jest **powierzchnia jajowata**, której asymetria może zmieniać dopasowanie i transport modułu.

Nie utożsamiamy jeszcze „podwójnej reprezentacji” z jedną interpretacją fizyczną. Pierwszą testowalną interpretacją matematyczną jest para czworościanów związanych inwersją względem środka sfery.

## 2. Wariant S: para antypodyczna na sferze

Niech środek sfery będzie (c), a promień (R). Czworościan ma wierzchołki (v_i), leżące na sferze:
[
|v_i-c|=R,quad i=0,1,2,3.
]
Druga reprezentacja to obraz centralnie symetryczny:
[
v_i^*=2c-v_i.
]
Wtedy automatycznie (|v_i^*-c|=R). Otrzymujemy osiem punktów, czyli dwa sprzężone czworościany na tej samej sferze.

**Szczególny fakt dla regularnego czworościanu:** dla wierzchołków ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)) ich antypody uzupełniają brakujące cztery naroża sześcianu. Suma obu czworościanów daje osiem naroży sześcianu wpisanego w sferę o promieniu (sqrt3). To dokładna własność tej konkretnej orientacji regularnego czworościanu, nie własność dowolnego czworościanu.

Pytania testowe:
1. Czy druga reprezentacja jest dokładnie inwersją centralną (v_i^*=2c-v_i), czy inną dualnością?
2. Czy oba czworościany są równocześnie aktywnymi modułami, czy drugi przechowuje stan/orientację?
3. Czy reguła odbicia BC działa osobno na obu czworościanach, czy przeplata ich wierzchołki?
4. Czy przejście zachowuje parowanie antypodyczne po każdym kroku?

## 3. Wariant E: powierzchnia jajowata jako ograniczenie

Jajo nie jest po prostu kulą o innym promieniu. W używanym w GIA modelu powierzchnia ma parametry:
[
S_{R,c,epsilon}(	heta,phi)=
egin{pmatrix}
Rsin	heta(1+epsiloncos	heta)cosphi\
Rsin	heta(1+epsiloncos	heta)sinphi\
Rccos	heta
end{pmatrix}.
]
Kula jest przypadkiem (c=1,epsilon=0). Dla (epsilon
e0) powierzchnia jest asymetryczna względem równika i nie ma zwykłej symetrii antypodycznej (xmapsto -x). Dlatego pary (v_i,v_i^*) nie muszą jednocześnie leżeć na tej samej powierzchni jajowatej.

W wariancie E nie wolno bez uzasadnienia przenosić sferycznego parowania antypodycznego. Należy zdefiniować osobno mapę ograniczenia/projekcji i sprawdzić, czy jest jednoznaczna, ciągła i odwracalna.

## 4. Co musi pozostać rozdzielone

- czworościan jako moduł (cztery wierzchołki);
- jego druga reprezentacja / partner dualny;
- powierzchnia ograniczająca (sfera albo jajo);
- oś/tunel wewnętrzny;
- reguła odbicia wierzchołka i przejścia do następnego modułu.

Nie wolno utożsamiać podwójnej reprezentacji z podwójnym pokryciem topologicznym, dodatkowym czworościanem, odbiciem lustrzanym ani stanem antycząstki bez osobnej definicji.

## 5. Minimalny eksperyment porównawczy

### S1 — regularny czworościan na sferze
- znormalizować cztery wierzchołki do wspólnej sfery;
- utworzyć antypodyczny czworościan;
- sprawdzić, że suma wierzchołków daje osiem naroży sześcianu w przypadku regularnym;
- sprawdzić parowanie po kolejnych krokach reguły BC.

### S2 — ogólny czworościan na jego sferze opisanej
- wyznaczyć środek i promień sfery opisanej;
- utworzyć parę antypodyczną;
- sprawdzić, które własności zachowuje odbicie modułowe;
- nie zakładać, że suma tworzy sześcian lub stałą helisę.

### E1 — ten sam moduł w otoczeniu jajowatym
- zdefiniować mapę umieszczającą moduł na/w powierzchni jajowatej;
- zmierzyć odchylenie partnera antypodycznego od powierzchni;
- porównać lokalny luz, odległości, obrót ramy, fazę i podpisany skręt;
- sprawdzić, czy potrzebna jest deformacja modułu, czy zmiana mapy reprezentacji.

### Kontrole
- brak otoczenia;
- kula bez partnera;
- kula z partnerem antypodycznym;
- jajo z jedną reprezentacją;
- jajo z jawnie zdefiniowaną drugą reprezentacją (jeśli istnieje niezależna reguła).

## 6. Kryterium wniosku

Nie wybieramy między kulą i jajem na podstawie wyglądu. Porównujemy:
- zachowanie sześciu krawędzi czworościanu;
- zgodność obu reprezentacji;
- ciągłość i jednoznaczność transportu;
- luz do granicy i kolizje;
- stałość osi, promienia i kroku helikalnego;
- zachowanie znaku orientacji/fazy;
- odwracalność mapy i informację utraconą w projekcji.

**Wynik, którego wolno użyć teraz:** dla regularnego czworościanu para antypodyczna dokładnie uzupełnia osiem naroży sześcianu wpisanego w sferę. Wariant jajowaty łamie tę prostą symetrię, więc wymaga osobnego operatora. Nie przesądza to jeszcze, który wariant jest właściwym modelem TIMDR.
