# Ogólny czworościan: czterokrokowa periodyczność śrubowa (v0.1)

**Data:** 2026-11-09  
**Status:** twierdzenie geometryczne dla rekurencji odbicia ścianowego; dowód oparty na dokładnej permutacji metryki i niezmienniczości odbicia względem izometrii. Test regresyjny dodany do testów BC.  
**Zakres:** dowolny niekoplanarny czworościan, bez założenia foremności.

## 1. Wynik

Dla rekurencji
\[
v_{n+4}=\operatorname{Reflect}\big(v_n,\operatorname{plane}(v_{n+1},v_{n+2},v_{n+3})\big)
\]
nie istnieje na ogół jedna izometria przenosząca uporządkowane okno \((v_n,v_{n+1},v_{n+2},v_{n+3})\) na następne okno przesunięte o jeden punkt.

Istnieje natomiast jedna stała, właściwa izometria \(T\), która przenosi okno o cztery pozycje:
\[
T(v_n)=v_{n+4}\quad\text{dla każdego }n.
\]

Jeżeli \(T\) nie jest identycznością, jest ruchem śrubowym (w szczególnych przypadkach czystym obrotem lub translacją). W konsekwencji łańcuch rozkłada się na cztery przeplatane orbity:
\[
\{v_{4k}\},\quad\{v_{4k+1}\},\quad
\{v_{4k+2}\},\quad\{v_{4k+3}\},
\]
z których każda jest orbitą tej samej izometrii śrubowej \(T\). Dla niezerowego postępu osiowego każda orbita jest dyskretnym śladem helisy; wszystkie cztery mają wspólną oś, ale mogą mieć różne promienie i fazy.

To jest **czterogałęziowa periodyczność śrubowa**, a nie automatycznie fraktalność.

## 2. Dowód — permutacja sześciu krawędzi

Dla uporządkowanego czworościanu \(W_n=(v_n,v_{n+1},v_{n+2},v_{n+3})\) oznaczmy kwadraty długości krawędzi w kolejności:
\[
E_n=(d_{01}^2,d_{02}^2,d_{03}^2,d_{12}^2,d_{13}^2,d_{23}^2).
\]

Odbicie \(v_n\) względem płaszczyzny trzech pozostałych wierzchołków zachowuje odległości nowego punktu od każdego z tych trzech wierzchołków. Stąd:
\[
E_{n+1}=(d_{12}^2,d_{13}^2,d_{01}^2,
d_{23}^2,d_{02}^2,d_{03}^2).
\]
Jest to stała permutacja sześciu pozycji:
\[
P(a,b,c,d,e,f)=(d,e,a,f,b,c).
\]
Bezpośrednio:
\[
P^2(a,b,c,d,e,f)=(f,b,d,c,e,a),
\]
\[
P^3(a,b,c,d,e,f)=(c,e,f,a,b,d),
\qquad P^4=I.
\]
Zatem:
\[
E_{n+4}=E_n
\]
dla każdego niekoplanarnego wejściowego czworościanu.

Po czterech krokach wszystkie sześć krawędzi wraca do tych samych pozycji uporządkowanego czworościanu. Dwa uporządkowane czworościany \(W_n\) i \(W_{n+4}\) mają więc identyczną macierz odległości. Istnieje dokładnie jedna izometria euklidesowa przenosząca pierwszy uporządkowany czworościan na drugi.

Znak zorientowanej objętości również pozostaje taki sam: każde odbicie odwraca orientację bryły, a przesunięcie okna o jeden indeks jest permutacją cykliczną czterech wierzchołków, która także odwraca znak. Dwa odwrócenia dają zachowanie orientacji. Izometria \(T\) jest więc właściwa, \(\det R=+1\).

## 3. Dlaczego operator jest stały dla całego łańcucha

Odbicie jest ekwiwariantne względem izometrii właściwych: dla dowolnej takiej izometrii \(T\):
\[
T(\operatorname{Reflect}(x,\Pi))
=\operatorname{Reflect}(T(x),T(\Pi)).
\]

Z definicji \(T\) przenosi \(W_n\) na \(W_{n+4}\). Następny punkt w obu oknach powstaje tą samą regułą odbicia. Ekwiwariantność daje:
\[
T(v_{n+4})=v_{n+8}.
\]
Indukcyjnie:
\[
T(v_n)=v_{n+4}\quad\forall n.
\]
Nie jest to dopasowanie numeryczne do skończonej próbki, lecz konsekwencja rekurencji i czterokrokowej identyczności uporządkowanej metryki.

## 4. Dlaczego krok pojedynczy jest na ogół inny

Dla jednego kroku wektor krawędzi zmienia się przez \(P\), a nie pozostaje taki sam. Izometria przenosząca \(W_n\) na \(W_{n+1}\) istnieje tylko wtedy, gdy:
\[
(a,b,c,d,e,f)=(d,e,a,f,b,c).
\]
To wymusza:
\[
a=c=d=f,\qquad b=e.
\]
Jest to szczególne ograniczenie na sześć długości krawędzi, którego ogólny czworościan nie spełnia. Regularny czworościan jest przypadkiem szczególnym, w którym operator może działać już co jeden krok.

Dlatego wcześniejsze stwierdzenie „ogólny czworościan nie ma stałego operatora śrubowego” wymaga doprecyzowania: **na ogół nie ma stałego operatora na jeden krok; ma stały operator na cztery kroki.**

## 5. Przykład liczbowy — ogólny czworościan

Dla wejściowych wierzchołków:
\[
v_0=(0,0,0),\quad
v_1=(2,0.2,0.1),\quad
v_2=(0.3,3,0.2),\quad
v_3=(0.1,0.4,4)
\]
numeryczne wyznaczenie właściwej izometrii z \(W_0\mapsto W_4\) daje przykładowo:
- kąt obrotu około \(162.3959355^\circ\);
- jednostkowy kierunek osi około \((-0.662527,-0.563342,-0.493663)\);
- podpisany postęp osiowy na cztery kroki około \(-3.391762\);
- maksymalny błąd predykcji kolejnych punktów przy arytmetyce zmiennoprzecinkowej około \(5.5\cdot10^{-14}\).

Wartości te dotyczą wyłącznie podanego przykładu i konwencji orientacji. Dowód ogólny nie zależy od tych liczb. Dla innych czworościanów kąt, oś, postęp i promienie czterech orbit będą inne.

## 6. Co to oznacza geometrycznie

- Łańcuch nie musi być pojedynczą próbkowaną helisą.
- Co czwarty wierzchołek leży na jednej orbicie \(T\); analogicznie trzy pozostałe klasy reszt modulo 4.
- Wszystkie cztery orbity są generowane przez tę samą oś i ten sam kąt/postęp, lecz mogą być przesunięte względem siebie.
- Złożenie czterech orbit daje dyskretny łańcuch z czteropunktowym motywem wewnętrznym.
- Dla szczególnych danych możliwy jest czysty obrót, translacja albo przypadek zdegenerowany; należy raportować parametry \(T\), a nie zakładać z góry niezerową helikalność.

## 7. Czy to fraktal?

Nie. Stała izometria śrubowa zachowuje odległości i nie jest kontrakcją. Cztery przeplatane orbity tworzą strukturę o skończonym motywie i jednej regule ruchu. To odkrycie jest matematycznie istotne, ale samo nie daje nieskończonej hierarchii skal ani niecałkowitego wymiaru.

Potencjalny dalszy kierunek to dopiero:
1. porównać cztery promienie i fazy orbit;
2. zbadać, kiedy orbity pokrywają się, są rozłączne lub przecinają się;
3. zbadać rodzinę operatorów \(T\) w przestrzeni kształtów czworościanów;
4. sprawdzić, czy dodatkowe sprzężenie/zmienna reguła modułu wprowadza rekurencję skalową.

Nie nazywać tych własności fraktalnymi bez odrębnego dowodu.

## 8. Reprodukowalność i zmiany w repozytorium

Test dokładny test_general_tetrahedron_has_exact_four_step_ordered_congruence sprawdza identyczność sześciu uporządkowanych kwadratów krawędzi oraz zachowanie zorientowanej objętości między \(W_n\) i \(W_{n+4}\) dla wielu okien. Test test_generic_tetrahedron_does_not_have_one_step_ordered_congruence kontroluje, że dla przykładowego ogólnego czworościanu zgodność jednego kroku nie zachodzi.

Testy dopisano do:
experiments/helix_characterization/tests/test_boerdijk_coxeter_tetrahelix.py.

**Status:** twierdzenie geometryczne — wyprowadzone; testy regresyjne — dodane; pełny CI po tym commicie — do sprawdzenia.


## 9. Interpretacja topologiczna: plecionka, węzeł i splot

Cztery klasy reszt modulo 4 są orbitami tej samej izometrii śrubowej:
\[
\mathcal H_j=\{T^k(v_j):k\in\mathbb Z\},\quad j=0,1,2,3.
\]

Jeśli składowa translacyjna wzdłuż osi \(T\) jest niezerowa, każda orbita jest niezamkniętą, nieskończoną helisą. W takim przypadku cztery orbity mogą tworzyć geometrię plecionkową (cztery nici o wspólnej osi), ale ich suma nie jest węzłem ani splotem w standardowym sensie teorii węzłów, ponieważ nie składa się z zamkniętych krzywych.

Należy rozdzielić:
- **plecionkę:** otwarte lub nieskończone nici, które wzajemnie się owijają;
- **węzeł:** jedna zamknięta krzywa osadzona w 3D;
- **splot:** kilka zamkniętych, rozłącznych krzywych;
- **domknięcie okresowe:** dodatkowa reguła identyfikacji/połączenia końców, która może przekształcić fragment plecionki w kandydata na węzeł lub splot.

Dla izometrii śrubowej z niezerowym postępem osiowym żadna pojedyncza orbita nie zamyka się. Jeśli postęp osiowy jest zerowy, operator jest obrotem wokół osi (lub przypadkiem szczególnym); orbity zamykają się dopiero, gdy kąt obrotu jest wymierną wielokrotnością \(2\pi\). Wtedy należy osobno sprawdzić, czy różne orbity są rozłączne i jaki typ splotu tworzą.

Samo przeplatanie wizualne nie dowodzi niezerowego niezmiennika splotowego. Do klasyfikacji potrzebne będą: dokładne parametry osi, kąta i przesunięcia, analiza przecięć/rozłączności, jawna reguła domknięcia oraz niezmiennik topologiczny odpowiedni dla otrzymanej krzywej/splotu (np. liczba łącznościowa dla dwóch składowych lub grupa podstawowa dopełnienia w trudniejszych przypadkach).

**Status:** hipoteza plecionki — uzasadniona do zbadania; hipoteza węzła/splotu — wymaga domknięcia i testu topologicznego. Nie nazywać obecnych nieskończonych orbit węzłem.


## 10. Wspólny początek i więź czterech orbit — hipoteza sprzężonego obiektu

Sugestia badawcza autora: cztery orbity należy traktować tak, jakby rozpoczęły ruch jednocześnie i pozostawały ze sobą związane przez wspólną strukturę, a być może także przez oddziaływanie przypominające grawitację. Nie jest to jeszcze twierdzenie o fizycznej sile. Poniżej rozdziela się to, co wynika z geometrii BC, od możliwego rozszerzenia dynamicznego.

### 10.1. Wspólny parametr i wspólny operator

Niech początkowy czworościan ma uporządkowane wierzchołki \(X_j(0)=v_j\), \(j=0,1,2,3\). Wszystkie cztery trajektorie mają ten sam parametr ewolucji \(s\) i ten sam początek:
\[
X_j(s)=\exp(s\Xi)X_j(0),
\]
gdzie \(\exp(s\Xi)\in SE(3)\) jest jednoparametrową grupą ruchów śrubowych, a jej próbka przy \(s=1\) jest operatorem \(T\). Wtedy:
\[
X_j(k)=T^k(v_j),\qquad k\in\mathbb Z.
\]
To jest precyzyjny sens jednoczesnego startu i wspólnego ruchu. Cztery nici nie są niezależnie parametryzowane; mają wspólną fazę, prędkość kątową i postęp osiowy, a ich różnice są zakodowane w czterech punktach początkowych.

Dla wspólnego ruchu sztywnego:
\[
\|X_i(s)-X_j(s)\|=\|X_i(0)-X_j(0)\|.
\]
Zachowane są więc wszystkie sześć odległości między czterema punktami. W każdej chwili tworzą one przystający, współporuszający się czworościan. To daje więź geometryczną bez postulowania dodatkowej siły.

### 10.2. Ważne rozróżnienie: więź kinematyczna a oddziaływanie

**Model A — więź kinematyczna:** jeden operator \(SE(3)\) przenosi cały czteropunktowy motyw. Wzajemne odległości są niezmiennikami. Jest to dokładna konsekwencja czterokrokowego twierdzenia dla rekurencji BC.

**Model B — sprzężenie dynamiczne:** każda nić ma własny stan \(X_j,V_j\), a równania ruchu zawierają człony zależne od pozostałych nici:
\[
m_j\ddot X_j=F^{\mathrm{self}}_j+
\sum_{i\ne j}F_{ij}.
\]
Przykładowy, wyłącznie fenomenologiczny potencjał wiążący mógłby zależeć od odchyleń od odległości odniesienia:
\[
U_{\mathrm{bind}}=
\frac12\sum_{i<j}k_{ij}
\left(\|X_i-X_j\|-d_{ij}^{(0)}\right)^2.
\]
Taki model przypomina więź sprężystą, nie grawitację. Model grawitacyjny wymagałby osobnego uzasadnienia potencjału, źródła, znaku, jednostek i zasady sprzężenia.

Modele A i B nie są tym samym. W modelu A odległości są zachowane z definicji ruchu sztywnego; w modelu B odległości mogą się zmieniać, a wspólny ruch śrubowy przestaje być dokładny, chyba że symetria i siły gwarantują jego zachowanie.

### 10.3. Co znaczyłoby „pole czasoprzestrzenne”?

Na obecnym etapie można wprowadzić jedynie roboczą nazwę **pole więzi / pole sprzężenia czterech orbit**. Jego minimalna rola byłaby taka, że stan jednej nici wpływa na dopuszczalny stan pozostałych. Aby nazwać je polem fizycznym, trzeba określić:
- zmienne pola i ich dziedzinę (przestrzeń, czas lub czasoprzestrzeń);
- równanie ewolucji i źródła;
- prawo oddziaływania z czterema trajektoriami;
- jednostki, symetrie i prawa zachowania;
- granicę, w której model odtwarza znaną teorię albo daje testowalną nową predykcję.

Nie utożsamiać analogii do grawitacji z grawitacją fizyczną.

### 10.4. Minimalny test rozstrzygający

1. Ustawić cztery punkty początkowe jako jeden czworościan i uruchomić je ze wspólnym parametrem \(s=0\).
2. W modelu A zastosować ten sam generator śrubowy do wszystkich czterech punktów; sprawdzić zachowanie sześciu odległości i wspólnej fazy.
3. W modelu B włączyć jawne sprzężenie parami, mierzyć zmianę odległości, faz i osi; porównać z modelem A oraz kontrolą bez sprzężenia.
4. Sprawdzić, czy istnieje niezerowe sprzężenie, które zachowuje lub stabilizuje strukturę czteroniciową bez ręcznego wymuszania jej geometrii.
5. Dopiero po tym badać, czy trajektorie tworzą plecionkę, a po jawnej regule domknięcia — węzeł lub splot.

**Status:** wspólny start i wspólny ruch sztywny — ścisła konstrukcja kinematyczna; oddziaływanie między nićmi — hipoteza dynamiczna; analogia grawitacyjna — intuicja do formalizacji, nie wynik fizyczny.
