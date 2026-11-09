# Redukcja helisy czterowęzłowej do trójwęzłowej na kuli i bryle jajowatej

**Wersja:** 0.1  
**Data:** 2026-11-09  
**Status:** jawny model konstrukcyjny + kod numeryczny + testy; nie jest jeszcze identyfikacją fizycznej geometrii TIMDR.

## 1. Korekta interpretacji zadania

Nie przypisujemy trzech grafów do trzech helis. Obiektem wyjściowym jest jedna przestrzenna struktura czterowęzłowa z czterema helikalnymi przebiegami. Operacja polega na:

1. wskazaniu jednej helisy;
2. wykonaniu dwóch cięć ograniczających wybrany obieg/łuk;
3. usunięciu fragmentu między cięciami;
4. połączeniu dwóch powstałych końców mostkiem leżącym na powierzchni nośnej;
5. dopasowaniu trzech pozostałych helis do nowej symetrii obwodowej.

**Ważne rozróżnienie topologiczne:** zamknięty okrąg nie ma końców. Aby „połączyć miejsca rozcięcia”, trzeba wskazać co najmniej dwa punkty cięcia. W tym modelu wycinany jest łuk jednej zamkniętej helisy między parametrami (u_a,u_b), a jego dwa końce łączy mostek. Jeśli intencją jest wycięcie całej osobnej składowej kołowej, trzeba najpierw określić, gdzie ta składowa jest połączona z resztą grafu — to inna operacja topologiczna.

## 2. Dwie przestrzenie otoczenia

Używamy wspólnej parametryzacji:

[
S_{R,c,\epsilon}(\theta,\phi)=
\begin{pmatrix}
R\sin\theta(1+\epsilon\cos\theta)\cos\phi\\
R\sin\theta(1+\epsilon\cos\theta)\sin\phi\\
Rc\cos\theta
\end{pmatrix},
\quad 0\leq\theta\leq\pi,\quad 0\leq\phi<2\pi.
]

Parametry:
- (R>0) — skala;
- (c>0) — spłaszczenie/wydłużenie osi;
- (|\epsilon|<1) — asymetria jajowata.

**Kula:** (c=1,\epsilon=0).  
**Jajo:** w implementacji kontrolnej (c=1.08,\epsilon=0.28). To jawny wybór modelowy, nie wartość wywnioskowana z danych.

Promień równoleżnika:

[
\rho(\theta)=R\sin\theta(1+\epsilon\cos\theta).
]

Metryka powierzchni ma postać:

[
ds^2=E\,d\theta^2+2F\,d\theta d\phi+G\,d\phi^2,
]

gdzie (E=\langle S_\theta,S_\theta\rangle), (F=\langle S_\theta,S_\phi\rangle), (G=\langle S_\phi,S_\phi\rangle=\rho(\theta)^2). Dla tej powierzchni obrotowej (F=0). To daje pierwszą zależność, której nie wolno zgubić: odległość między helisami zależy od położenia na kuli/jaju, a w jaju także od asymetrii (\epsilon).

## 3. Konstrukcja czterech helis

Wersja referencyjna używa czterech krzywych:

[
H_j(u)=S(\theta(u),\phi_j(u)),\quad j=0,1,2,3,
]

[
\theta(u)=\frac{\pi}{2}+a\sin(2u),\qquad
\phi_j(u)=m u+\frac{2\pi j}{4}.
]

(a) jest amplitudą odchylenia od równika, a (m) liczbą obiegów azymutalnych. Implementacja ustawia (a=0.22,m=1). To model testowy; parametry powinny być później estymowane lub prerejestrowane na podstawie właściwej konstrukcji TIMDR.

Cztery fazy początkowe są rozdzielone o:

[
\Delta\phi_4=\frac{2\pi}{4}=\frac{\pi}{2}.
]

## 4. Operacja cięcia i ponownego połączenia

Na czwartej helisie wybieramy przedział ([u_a,u_b]). Punkty cięcia:

[
P_a=H_3(u_a),\qquad P_b=H_3(u_b).
]

Usuwamy fragment (H_3([u_a,u_b])), zachowując resztę helisy, a (P_a,P_b) łączymy mostkiem (B(q)) leżącym na tej samej powierzchni. Wersja 0.1 interpoluje liniowo parametry ((\theta,\phi)), przy czym różnica azymutu jest zawijana do przedziału ((-\pi,\pi]).

To jest **mostek powierzchniowy-kandydat**, nie geodezyjna. Wersja 0.2 powinna wyznaczać geodezyjną albo mostek minimalizujący energię, z kontrolą samoprzecięć. Nie wolno nazywać obecnego mostka najkrótszym bez takiego obliczenia.

## 5. Przejście 4 → 3 i warunek kolistości

Po usunięciu wybranego przebiegu pozostają trzy helisy. Minimalny warunek równomiernego rozłożenia wokół osi to:

[
\Delta\phi_3=\frac{2\pi}{3}.
]

Zmiana fazy:

[
\frac{\Delta\phi_3}{\Delta\phi_4}=\frac{4}{3}.
]

Nie oznacza to, że długości helis rosną dokładnie o (4/3): długość zależy również od (d\theta/du), (d\phi/du) oraz metryki (E,F,G). Przy ustalonym (\theta) lokalny odstęp wzdłuż równoleżnika wynosi:

[
d_4(\theta)=\rho(\theta)\frac{2\pi}{4},\qquad
d_3(\theta)=\rho(\theta)\frac{2\pi}{3}.
]

Stąd:

[
\boxed{d_3(\theta)=\frac{4}{3}d_4(\theta)}
]

dla tej samej szerokości geograficznej (\theta). To jest ścisła zależność metryczna modelu równomiernego rozłożenia, zarówno na kuli, jak i na jajowatej powierzchni. Na jaju (\rho(\theta)) jest asymetryczne względem równika, więc odstęp zależy od tego, po której stronie osi znajduje się dana część helisy.

## 6. Co musi zostać zachowane, a co może się zmienić

**Warunki twarde:**
- końce mostka dokładnie pokrywają się z punktami cięcia;
- wszystkie trzy pozostałe helisy leżą na zadanej powierzchni;
- orientacja parametru i znak torsji są jawne;
- brak samoprzecięć musi być osobno sprawdzony;
- zamknięcie każdej krzywej sprawdzamy jako pozycję, styczną i — jeśli wymagane — krzywiznę.

**Warunki do optymalizacji, a nie założenia:**
- długości trzech helis;
- ich krzywizna i torsja;
- fazy lokalne poza wymuszonym równomiernym rozstawem;
- położenie osi i punkty kardynalne;
- rozkład naprężenia/energii deformacji.

W szczególności równe fazy (120^\circ) są minimalnym warunkiem kolistości, nie dowodem, że cała helisa po relaksacji jest kołowa lub symetryczna.

## 7. Skręt i orientacja

Dla każdej krzywej (H_i(u)) liczymy osobno torsję Freneta–Serreta:

[
\tau_i(u)=
\frac{\det(H_i',H_i'',H_i''')}
{\|H_i'\times H_i''\|^2},
]

o ile mianownik jest niezerowy. Znak torsji zależy od orientacji parametryzacji. Dlatego przed i po redukcji porównujemy:
- tę samą orientację obiegu;
- znak torsji;
- profile (\tau_i(u)), a nie tylko ich wartości bezwzględne;
- osobno skoki i punkty, w których torsja jest nieokreślona.

Nie utożsamiamy torsji Freneta z topologicznym skrętem TIMDR, twist pasma, writhe ani linking number.

## 8. Wynik, którego obecnie wolno użyć

Kod `experiments/helix_reduction/four_to_three_surface_reduction.py` generuje ten sam eksperyment dla kuli i jaja. Oblicza punkty cięcia, długość mostka-kandydata, odstępy 4→3, metrykę powierzchni i podpisaną torsję trzech ocalałych krzywych.

Testy sprawdzają:
- promień kuli;
- asymetrię powierzchni jajowatej;
- zmianę rozstawu (90^\circ\to120^\circ);
- zależność odstępu od kształtu;
- dodatnią półokreśloność metryki.

**Ograniczenie:** obecna wersja nie rozwiązuje jeszcze pełnej relaksacji sprężystej trzech helis. Nie wyprowadza też fizycznych punktów kardynalnych. To następny etap, nie wynik, który można dopisać bez obliczeń.

## 9. Następny test rozstrzygający

Uruchomić dokładnie tę samą operację dla:
1. kuli (\epsilon=0,c=1);
2. jaja (\epsilon=0.28,c=1.08).

Następnie porównać:
- długości i krzywizny trzech ocalałych helis;
- podpisane profile torsji;
- lokalne odstępy (d_3(\theta));
- energię mostka;
- minimalne odległości między krzywymi;
- stabilność wyniku przy zmianie (u_a,u_b).

Jeżeli zależności utrzymają się w obu kształtach, będą kandydatami na własności niezależne od konkretnej bryły. Jeżeli zmienią się między kulą a jajem, będą własnościami zależnymi od krzywizny i asymetrii otoczenia. W obu przypadkach otrzymamy falsyfikowalny wynik.


### 5.1. Ważna kontrola: średnia a profil lokalny

Dla przyjętej symetrycznej funkcji szerokości geograficznej \(\theta(u)=\pi/2+a\sin(2u)\) składnik liniowy w \(\epsilon\) znosi się w średniej po pełnym okresie. Dlatego średni odstęp po całym obiegu może być taki sam dla kuli i jaja, mimo że lokalny profil odstępów jest inny. Porównanie kształtów musi więc obejmować minimum, maksimum i profil \(d_3(u)\), a nie samą średnią. To jest kontrola przeciwko fałszywemu wnioskowi z jednej liczby agregowanej.
