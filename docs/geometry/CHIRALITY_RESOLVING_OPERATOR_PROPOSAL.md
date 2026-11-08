# Kandydujący operator rozróżniający chiralność — notatka GIA-TIMDR

**Status:** propozycja matematyczna do falsyfikacji. Nie jest aksjomatem, poprawką G5 ani walidacją empiryczną. Powiązany eksperyment syntetyczny znajduje się w repozytorium [Helix-Lock](https://github.com/jbackk-lang/Helix-Lock/tree/experiment/chirality-resolving-operator).

## 1. Problem źródłowy

Aksjomat G5 i implementacja `core/geometric_resonance_operator.py` budują rzeczywistą, symetryczną macierz sztywności pierścienia. Dla węzłów o krzywiźnie `kappa_i` i segmentów o torsji `tau_i` sprzężenie krawędziowe wykorzystuje `|tau_i|`:

`K_ii = k_scale*kappa_i + kc_scale*(|tau_(i-1)| + |tau_i|)`

`K_(i,i+1) = -kc_scale*|tau_i|`.

To jest świadoma konstrukcja G5. Ma ważną konsekwencję: odbicie lustrzane, które zmienia znak torsji, ale zachowuje jej moduł, nie jest rozróżnialne przez tę macierz. Nie jest to błąd implementacji; jest to informacja, której ten konkretny operator nie koduje.

## 2. Proponowany kanał orientacji

Dla zorientowanego pierścienia N-węzłowego definiujemy rzeczywistą macierz antysymetryczną A(tau):

- A[i,(i+1) mod N] += tau_i
- A[(i+1) mod N,i] -= tau_i
- A^T = -A.

Następnie jako osobny operator diagnostyczny proponujemy:

`H(tau) = K_abs(tau) + i*gamma*A(tau)`, `gamma >= 0`.

Ponieważ A jest antysymetryczna, `i*A` jest hermitowska:

`(iA)^* = (-i)A^T = iA`.

Przy odbiciu lustrzanym `tau -> -tau`:

`K_abs(-tau) = K_abs(tau)`

`A(-tau) = -A(tau)`

`H(-tau) = conjugate(H(tau))`.

Wynik: widma obu operatorów są identyczne, lecz same macierze są sprzężone zespolenie, a nie identyczne. Wybrana obserwabla zespolona może zachować znak orientacji. To rozdziela dwie rzeczy, które łatwo pomylić: **niezmienniczość widma względem lustra** i **utratę informacji o chiralności w operatorze**.

## 3. Obserwabla rozróżniająca

Dla ustalonego trybu Fouriera:

`q_m[j] = exp(2*pi*i*m*j/N)/sqrt(N)`

można mierzyć odpowiedź kanału chiralnego:

`C_m = Re(q_m^* (i*gamma*A(tau)) q_m)`.

Dla jednorodnego pierścienia z niezerową torsją i nietrywialnym trybem `m`, `C_m` zmienia znak po odwróceniu torsji. W eksperymencie Helix-Lock jest to testowane niezależnie od wartości własnych.

To jest obserwabla wybranego modelu dyskretnego, nie uniwersalny niezmiennik geometryczny. Dla niejednorodnych profili torsji, innych warunków brzegowych i innych trybów odpowiedź należy policzyć, a nie zakładać.

## 4. Granica względem aksjomatu G5

**Nie zastępujemy macierzy K w G5 przez H.** Obecny G5 opisuje mechaniczny układ drugiego rzędu:

`M x'' + Gamma x' + K x = F(t)`.

Macierz K jest rzeczywistą macierzą sztywności. Dodanie zespolonego składnika antysymetrycznego do tego równania zmieniłoby domenę fizyczną, warunki energii i analizę stabilności. Nie wolno robić tego przez prostą podmianę symbolu.

Na tym etapie H jest odrębnym, hermitowskim operatorem diagnostycznym na przestrzeni cyklicznych stopni swobody. Zanim można go połączyć z G5, trzeba zdefiniować:
- co reprezentuje zespolony stan i jego faza;
- jednostki `gamma` i zgodność wymiarową obu składników;
- sens fizyczny lub informacyjny kanału antysymetrycznego;
- relację z masą M, tłumieniem Gamma i odpowiedzią wymuszoną;
- warunki dodatniej określoności / stabilności dla zastosowania docelowego.

Hermitowskość sama w sobie nie gwarantuje dodatniej określoności. Dla dowolnie dużego `gamma` dodatniość nie może być przyjęta bez dowodu.

## 5. Dwie różne operacje orientacji

Nie wolno utożsamiać:

1. **Odbicia geometrycznego** przy zachowaniu parametryzacji krzywej i kolejności węzłów — dla lustrzanej helisy torsja zmienia znak.
2. **Odwrócenia indeksowania pierścienia** — zmienia się kierunek przejścia i etykiety krawędzi. To jest transformacja współrzędnych / orientacji grafu, nie samo odbicie w przestrzeni.

Testy muszą sprawdzić obie transformacje osobno i ich złożenie. W przeciwnym razie znak kanału chiralnego może być artefaktem konwencji indeksowania.

## 6. Status dowodu i eksperymentu

W gałęzi Helix-Lock dodano eksperyment syntetyczny i testy sprawdzające:
- hermitowskość H;
- sprzężenie zespolone operatorów lustrzanych;
- równość ich widm;
- zmianę znaku odpowiedzi ustalonego trybu Fouriera;
- powrót do operatora bazowego przy `gamma=0`.

To potwierdza własności algebraiczne konkretnej konstrukcji numerycznej. Nie potwierdza:
- że H jest jedynym lub właściwym rozszerzeniem G5;
- że `gamma` ma uzasadnioną wartość fizyczną;
- że operator działa na realnych, zmierzonych krzywych 3D;
- że zachodzi rekonstrukcja sygnału, fazy lub payloadu;
- że istnieje mechanizm samonaprawy informacji.

## 7. Plan falsyfikacji

1. Zbadać niejednorodne profile `tau_i`, w tym profile zmieniające znak na pierścieniu.
2. Osobno wykonać odbicie geometryczne, odwrócenie indeksowania oraz ich złożenie.
3. Przeskanować `gamma` i wyprowadzić granice dodatniej określoności H dla klas profili `kappa,tau`.
4. Zbudować równoważną reprezentację rzeczywistą na podwojonej przestrzeni stanu; sprawdzić, czy wnioski nie zależą od samej notacji zespolonej.
5. Porównać wynik z istniejącym G5 na tej samej geometrii, bez zmiany jego macierzy mechanicznej.
6. Dopiero po tych krokach rozważyć formalny most do gałęzi K lub META-DYNAMICS.

## 8. Decyzja na teraz

Pozostawić aksjomaty G5 i K bez zmian. Traktować `H` jako jawnie oznaczony kandydat badawczy. Wnioski promować dopiero po przejściu testów algebraicznych, stabilnościowych, wymiarowych i niezależnych kontroli geometrycznych.
