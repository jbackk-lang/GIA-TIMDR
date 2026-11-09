# Próg redukcji 4-węzła: element piąty mieści się, szósty wymusza reorganizację (v0.1)

**Data:** 2026-11-09  
**Status:** hipoteza konstrukcyjna autora; formalizacja do testów. Nie jest jeszcze wynikiem geometrii ani topologii.

## 1. Korekta progu

Korygujemy poprzednią specyfikację, która zakładała, że już piąty element przekracza warunki brzegowe.

Nowa hipoteza:
- elementy 1–3 tworzą konfigurację trójkątną;
- dodanie elementu 4 daje czworościenny stan pośredni / 4-węzeł;
- element 5 nadal mieści się w granicach 4-węzła;
- dopiero dodanie elementu 6 rozpycha lub destabilizuje 4-węzeł;
- odpowiedzią układu jest reorganizacja do konfiguracji trójdzielnej / trójwęzła.

Zapis skrócony:
\[
X_3\xrightarrow{+e_4}X_4
\xrightarrow{+e_5}X_5\in\mathcal A_4
\xrightarrow{+e_6}X_6^*\notin\mathcal A_4
\xrightarrow{\mathcal R}X_3'.
\]

\(\mathcal A_4\) oznacza zbiór konfiguracji dopuszczalnych w 4-węźle. Kluczowy warunek do wykazania:
\[
X_5\in\mathcal A_4,\qquad X_6^*\notin\mathcal A_4.
\]

Nie zakładamy jeszcze, że wynik redukcji jest identyczny z pierwotnym trójkątem. \(X_3'\) ma być trójwęzłem tylko wtedy, gdy wynika to z grafu połączeń i osadzenia przestrzennego.

## 2. Ważne rozróżnienie nazewnicze

W tym dokumencie „piąty” i „szósty” oznaczają roboczo liczbę dodanych elementów / wierzchołków konstrukcji, nie liczbę ścian wielościanu. W geometrii „sześciościan” zwykle oznacza bryłę o sześciu ścianach (np. sześcian), co nie jest tym samym co dowolna bryła z sześcioma wierzchołkami. Nie wolno mieszać:
- liczby wierzchołków;
- liczby krawędzi;
- liczby ścian;
- liczby niezależnych cykli grafu;
- liczby gałęzi helikalnych;
- liczby składowych / węzłów topologicznych.

Przed przypisaniem nazwy bryły trzeba określić, co dokładnie jest „elementem” w konstrukcji TIMDR.

## 3. Warunek brzegowy zamiast arbitralnego progu

Nie wprowadzamy reguły „sześciościan zawsze redukuje” jako aksjomatu. Definiujemy funkcję dopuszczalności:
\[
g(X)=\min\{g_{\rm sep},g_{\rm closure},g_{\rm curvature},
g_{\rm phase},g_{\rm embedding}\}.
\]
Składowe mają reprezentować, odpowiednio:
- minimalny odstęp między elementami;
- zgodność zamknięcia / szwów;
- ograniczenia krzywizny lub energii deformacji;
- zgodność fazową;
- możliwość osadzenia bez niedozwolonych przecięć / osobliwości.

Dla konkretnej rodziny geometrii hipoteza wymaga wykazania:
\[
g(X_5)\geq0,\qquad g(X_6^*)<0.
\]
Jeżeli oba stany są dopuszczalne albo oba niedopuszczalne, próg 5→6 nie został potwierdzony.

## 4. Co oznacza „rozpychanie”

W modelu geometrycznym dodanie elementu 6 powinno powodować mierzalny wzrost co najmniej jednego z parametrów:
- maksymalnej deformacji istniejących gałęzi;
- energii / długości potrzebnej do zachowania warunków połączenia;
- lokalnego zagęszczenia lub konfliktu przestrzennego;
- błędu domknięcia fazy i stycznych;
- liczby naruszonych ograniczeń.

Samo zwiększenie liczby wierzchołków grafu nie dowodzi rozpychania. Potrzebne są współrzędne, metryka i reguła dopuszczalnego osadzenia.

## 5. Co musi oznaczać redukcja do trójwęzła

Po przekroczeniu ograniczenia nie usuwamy ręcznie jednej helisy. Operator \(\mathcal R\) ma reorganizować cały graf / osadzenie. Porównujemy:
1. odrzucenie szóstego elementu (układ wraca do X5);
2. lokalną kontrakcję / scalenie;
3. zmianę połączeń grafu przy zachowaniu liczby elementów;
4. przejście do trzech niezależnych gałęzi lub cykli;
5. powstanie rzeczywistego trójwęzła po osadzeniu 3D.

Dla każdego wariantu zapisujemy, co zachowano: połączenia, orientację, fazę, kierunek obiegu, znak skrętu ramy i warunki brzegowe. Szczególnie nie wolno zgubić informacji o orientacji środkowego płata sygnału.

## 6. Plan badań

### E1 — zdefiniować element
Ustalić, czy elementem jest wierzchołek, ściana, krawędź, płat sygnału, czy gałąź helikalna. Bez tego „piąty/szósty” jest wieloznaczny.

### E2 — zbudować stany 3, 4, 5, 6
Dla każdego stanu utworzyć jawny graf incydencji i osadzenie 3D. Zachować osobno liczbę V, E, F, składowych i cykli.

### E3 — test pojemności 4-węzła
Sprawdzić, czy stan 5 ma poprawne osadzenie w ograniczeniach 4-węzła, a próba dodania 6 narusza co najmniej jeden wcześniej zdefiniowany warunek.

### E4 — wyprowadzić reorganizację
Nie wymuszać wyniku 3. Zastosować operator reorganizacji i sprawdzić, czy naturalnie daje trzy gałęzie / trójwęzeł. Porównać z kontrolą, w której szósty element można dodać bez naruszenia.

### E5 — geometria i orientacja
Powtórzyć na kuli (model bazowy) oraz jajowatej powierzchni (kontrola asymetrii). Mierzyć fazę, punkty kardynalne, warunki szwu C0/C1, orientację ramy, krzywiznę, torsję i niezmienniki grafu / węzła.

## 7. Kryterium potwierdzenia

Hipoteza pięciościan mieści się / sześciościan wymusza redukcję otrzymuje wsparcie dopiero wtedy, gdy:
- kombinatoryczny typ pięcio- i sześciościanu jest jawnie określony;
- stany 3–5 mają dopuszczalne osadzenie;
- stan 6 przekracza jawny warunek, a nie tylko zadany limit licznika;
- operator reorganizacji nie koduje z góry odpowiedzi;
- wynik ma trzy gałęzie i spełnia definicję trójwęzła;
- wynik jest stabilny dla perturbacji parametrów i rozdzielczości.

## 8. Zasada robocza

**Pięciościan (5 ścian) nadal mieści się w 4-węźle. Badamy, czy dopiero sześciościan (6 ścian) wymusza reorganizację całej struktury do trójwęzła.**