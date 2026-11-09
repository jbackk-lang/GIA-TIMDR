# Redukcja indukowana dodaniem elementu: trójkąt → czworościan → próg redukcji (v0.1)

**Data:** 2026-11-09  
**Status:** hipoteza konstrukcyjna autora; formalizacja do testowania, nie twierdzenie fizyczne.

## 1. Korekta mechanizmu

Poprzednia wersja 4→3 zakładała, że redukcję inicjuje odpadnięcie całej helisy podczas rozszerzania/kurczenia. To nie jest mechanizm bazowy wskazany przez autora i należy traktować go jako błędną gałąź roboczą.

Mechanizm bazowy jest **indukowany dodaniem kolejnego elementu**:

\[
\triangle_3
\xrightarrow{+e_4}
T_4
\xrightarrow{+e_5}
\text{przekroczenie warunków brzegowych}
\xrightarrow{\mathcal R}
\text{stan zredukowany}.
\]

Interpretacja:
- trzy elementy tworzą konfigurację trójkątną;
- dodanie czwartego elementu rozszerza ją do konfiguracji czworościennej;
- próba dodania kolejnego elementu do czworościanu przekracza ograniczenia dopuszczalnej konfiguracji;
- to przekroczenie uruchamia operator redukcji \(\mathcal R\).

Nie zakładamy jeszcze, czy piąty element zostaje odrzucony, czy też jego dodanie wymusza reorganizację całego układu i redukcję liczby niezależnych elementów/gałęzi. To rozstrzygną niezmienniki grafu i geometria po transformacji. W szczególności nie wolno utożsamiać tego automatycznie z mechanicznym odpadnięciem jednej helisy.

## 2. Kula jako geometria bazowa

Kula jest przyjętą przestrzenią odniesienia. Elementy są rozmieszczane według fazy kątowej, nie według długości łuku. Dla czterech równomiernych kierunków:

\[
\Delta\phi_4=\frac{2\pi}{4}=90^\circ.
\]

Piąty element nie jest po prostu kolejnym sektorem równomiernego podziału 4π/5. Jest próbą rozszerzenia konfiguracji już ograniczonej czworościenną geometrią. Należy sprawdzić, czy warunki brzegowe pozwalają na zachowanie wszystkich pięciu elementów bez przecięcia, degeneracji lub naruszenia reguły zamknięcia.

Jajo pozostaje wariantem kontrolnym; w nim osobno porównujemy miarę fazową i długość powierzchniową. Nie zmieniamy jednak bazowej definicji fazy kulistej.

## 3. Abstrakcyjny operator dodania i redukcji

Niech \(X_n\) oznacza konfigurację n-elementową, \(B(X_n)\) jej warunki brzegowe, a \(A_e\) operator dodania nowego elementu.

\[
X_4=A_{e_4}(X_3),\qquad
X_5^*=A_{e_5}(X_4).
\]

Definiujemy funkcję dopuszczalności:

\[
g(X)=
\begin{cases}
\geq 0 & \text{konfiguracja dopuszczalna},\\
<0 & \text{naruszenie warunków brzegowych}.
\end{cases}
\]

Przejście krytyczne zachodzi, gdy:

\[
g(X_5^*)<0.
\]

Operator redukcji:

\[
X_{\mathrm{red}}=\mathcal R(X_5^*;B,\Phi,\sigma),
\]

musi jawnie określać:
- które elementy pozostają niezależne;
- czy nowy element zostaje odrzucony, scalony, czy zmienia reprezentację;
- które węzły/krawędzie grafu są kontraktowane;
- jak zachowuje się faza \(\Phi\) i orientacja \(\sigma\);
- które warunki brzegowe są zachowane, a które ulegają zmianie.

Nie przypisujemy z góry \(X_{\mathrm{red}}=X_3\). To hipoteza do sprawdzenia, zgodna z wcześniejszym zainteresowaniem przejściem czterowęzła do trójwęzła, ale nie wynika wyłącznie z faktu dodania piątego elementu.

## 4. Dlaczego poprzedni model 4→3 nie wystarcza

Model fazowy v0.2 usuwał jedną z czterech zamkniętych krzywych z listy i równomiernie rozstawiał trzy pozostałe. Nie modelował:
- dodania piątego elementu;
- geometrii czworościanu jako stanu pośredniego;
- funkcji dopuszczalności warunków brzegowych;
- mechanizmu wyzwalającego redukcję;
- rzeczywistych połączeń elementów w grafie przestrzennym.

Wyniki v0.2 (90°→120°) są wyłącznie kontrolą fazowego rozstawienia, a nie testem proponowanego mechanizmu. Nie wolno używać ich jako dowodu redukcji.

## 5. Plan eksperymentu

### E1 — geometria stanów 3 i 4
Zbudować trójkąt jako stan bazowy, następnie dodać czwarty element i sprawdzić warunki zamknięcia, symetrię, fazę, orientację i warunki brzegowe czworościanu.

### E2 — próba dodania elementu 5
Dodać kolejny element do stanu czworościennego. Nie wymuszać redukcji z góry. Zmierzyć:
- naruszenie warunków brzegowych;
- minimalną odległość element–element;
- samoprzecięcia;
- degenerację objętości / orientacji;
- niezgodność fazy i stycznych na szwach;
- zmianę liczby niezależnych cykli i stopni swobody.

### E3 — operator redukcji
Jeśli E2 wykryje przekroczenie, zastosować jawnie zdefiniowany operator redukcji. Porównać możliwe wyniki:
1. odrzucenie dodanego elementu (bez redukcji stanu 4);
2. kontrakcja / scalenie elementów;
3. projekcja do trzech niezależnych kanałów;
4. zmiana typu topologicznego osadzenia, jeśli dopuszczona jest osobliwość/rozcięcie/sklejenie.

### E4 — zachowanie orientacji
Przechowywać podpisaną orientację fazową i torsję osobno. Redukcja nie może kasować znaku skrętu przez użycie wartości bezwzględnej.

### E5 — kula i jajo
Kula jest podstawową geometrią. Jajo jest testem wrażliwości: sprawdzić, czy próg i rodzaj redukcji zależą od asymetrii powierzchni.

## 6. Kryterium rozstrzygające

Hipoteza „dodanie piątego elementu wywołuje redukcję czteroelementowej konfiguracji do trójdzielnej” uzyska wsparcie w modelu dopiero wtedy, gdy:
- stan 3→4 jest geometrycznie i grafowo poprawny;
- dodanie elementu 5 narusza jawny warunek brzegowy;
- operator redukcji jest określony bez ręcznego wskazywania wyniku;
- wynik ma trzy niezależne kanały/gałęzie;
- zachowane i utracone niezmienniki są jawnie wypisane;
- wynik jest stabilny dla małych zmian parametrów i rozdzielczości.

Jeśli piąty element można dodać bez naruszenia ograniczeń, hipoteza w tej postaci jest sfalsyfikowana dla przyjętej geometrii i warunków.

## 7. Decyzja robocza

**Nie zaczynamy od usuwania helisy. Zaczynamy od dodawania elementów.** Czworościan jest stanem pośrednim; kolejny element jest próbą przekroczenia jego warunków brzegowych; redukcja jest odpowiedzią całego układu na tę próbę. Kula jest geometrią bazową, a faza jest pierwotną miarą podziału.
