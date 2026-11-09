# TIMDR — program badania anomalii jako relacji konstrukcyjnych (v0.1)

**Data:** 2026-11-09
**Status:** synteza robocza; hipotezy rozdzielone od wyników. Nie stanowi potwierdzenia fizycznej teorii.

## 1. Zasada metodologiczna

W TIMDR anomalia nie jest automatycznie błędem pomiaru ani odchyleniem do usunięcia. Jest obserwacją, której relacje z innymi obserwacjami należy zachować. Nie zakładamy, że wszystkie anomalie mają jedną przyczynę. Szukamy wspólnych niezmienników i operatorów, które potrafią przewidywać niezależne przypadki.

Każdy wpis badawczy ma mieć cztery etykiety:
- **OBSERVED:** co dokładnie zmierzono/udowodniono w kodzie lub geometrii;
- **INTERPRETATION:** możliwe znaczenie, jeszcze niepotwierdzone;
- **MISSING LAW:** jaka reguła jest potrzebna, aby przejść od obserwacji do mechanizmu;
- **FALSIFIER:** jaki wynik obaliłby interpretację.

## 2. Mapa obecnych anomalii i punktów styku

| Zjawisko | Co jest ustalone | Czego nie wolno jeszcze twierdzić |
|---|---|---|
| Środek czworościanu względem środka kuli | Przesunięcie wprowadza zależność warunku ograniczenia od orientacji, jeśli czworościan jest traktowany jako sztywny moduł | Że przesunięcie samo wytwarza ruch obrotowy |
| Sześcian/czworościan względem sfery | Bryły dyskretne i sfera mają różne grupy symetrii; okrągły przekrój nie zachowuje pełnej relacji 3D | Że każda niezgodność symetrii wymusza tę samą rotację |
| Obrót i przejście 2D→3D | Potrzebna jest mapa osadzenia/lift; sam obrót SO(2) lub SO(3) nie zmienia wymiaru | Że sam obrót jest kompletnym operatorem redukcji |
| Faza/chiralność | Reprezentacja (cos φ, sin φ) zachowuje znak winding w syntetycznym teście; interpolacja kąta zawiniętego go gubi | Że pole fazowe fizycznie napędza helisę |
| Historia sygnału MAGE | Uporządkowane przyrosty fazy kodują historię sekwencji; tasowanie ją niszczy | Że to dowód autonomicznej pamięci helisy |
| Redukcja 4→3 | Model powierzchniowy ma jawny warunek rozstawu faz 90°→120° i osobny mostek po cięciu | Że model testowy jest już rzeczywistą regułą TIMDR |
| G-Rezonans | Istnieje mechaniczny operator odpowiedzi, ale wejście jest siłą zewnętrzną, a |τ| usuwa znak chiralności | Że to pełny operator informacji→geometria |

## 3. Wspólny szkielet matematyczny do sprawdzenia

Niech stan TIMDR będzie zbiorem, a nie pojedynczą liczbą:

X = (G, C, F, φ, b, h)

gdzie:
- G — geometria modułu i jego graf połączeń;
- C — relacja środków / położenie względem otoczenia;
- F — rama orientacji i jej transport;
- φ — faza wraz z unwrapped winding i znakiem;
- b — warunki brzegowe i dopuszczalność;
- h — historia poprzednich stanów/sygnałów.

Przejście robocze:

X_(n+1) = T(X_n, u_n),

gdzie u_n jest sygnałem albo kolejnym zdarzeniem geometrycznym. Redukcja nie jest na tym etapie funkcją skalarną; to zmiana reprezentacji/struktury, która powinna zachować jawnie wybrane niezmienniki.

Potencjalny łańcuch:

źródłowy stan 2D + faza → lift do ramy 3D → ograniczenie przez otoczenie → zmiana orientacji/holonomii → przejście modułu/topologii.

To jest hipoteza kolejności zależności, nie gotowe prawo. Test ma ustalić, które strzałki istnieją i w jakich warunkach.

## 4. Najważniejszy eksperyment: rozdzielić bias orientacyjny od rzeczywistej rotacji

### E1 — geometria bez dynamiki
Ustawić czworościan wewnątrz kuli. Wprowadzić wektor przesunięcia d między środkiem kuli i jasno zdefiniowanym środkiem modułu. Dla wielu orientacji Q obliczyć luz:

g_i(Q) = R² - ||d + Q p_i||².

To wyznacza zbiór dopuszczalnych orientacji i aktywne kontakty. Powtórzyć dla d=0, d≠0, d→−d oraz odbicia lustrzanego.

### E2 — dynamika jawna
Do E1 dodać dokładnie jeden jawny mechanizm: np. bezpoślizgowe toczenie, zadane prawo kontaktu, minimalizację energii albo dyskretny operator przejścia. Nie mieszać tych mechanizmów w jednym teście.

Zmierz:
- obrót ramy Q i jego oś/kąt;
- przyrost fazy Δφ;
- holonomię po zamkniętej pętli;
- znak chiralności;
- pracę/energię, jeśli model ma sens fizyczny;
- czy odwrócenie d odwraca kierunek obrotu.

Jeśli E1 wykazuje orientacyjny bias, ale E2 nie daje ruchu, przesunięcie nie jest samoistnym generatorem rotacji. Jeśli konkretny mechanizm E2 daje stabilny obrót i wynik odwraca się zgodnie z symetrią kontrolną, mamy pierwszy kandydat na prawo.

## 5. Eksperyment sygnał jako geometria

Użyć fazora u(s)=q1(s)+i q2(s), q1=A cos φ, q2=A sin φ. Nie redukować go do zawiniętego kąta.

Zbudować lift:

X(s)=C(s)+q1(s)e1(s)+q2(s)e2(s)+z(s)e3(s).

Trzy warstwy mierzyć oddzielnie:
- fazę sygnału φ i winding;
- transport ramy F(s) oraz holonomię;
- przebieg osiowy z(s).

Test sprzężenia: przy stałej geometrii zmienić tylko fazę/orientację sygnału i sprawdzić, czy operator przejścia zmienia ramę lub odpowiedź brzegową. Następnie przy stałym sygnale zmienić tylko geometrię/offset. Dopiero interakcja obu testów może wskazać sprzężenie sygnał–geometria.

## 6. Redukcja jako utrata dopuszczalności lub zmiana reprezentacji

Nie zakładać progu 90°, 4→3 ani określonego węzła. Najpierw zapisać funkcje ograniczeń g_j(X). Zdarzenie graniczne następuje, gdy min_j g_j(X)=0. Następnie sprawdzić, czy naturalna kontynuacja wymaga zmiany liczby gałęzi, identyfikacji wierzchołków, ramy lub topologii grafu.

Przy redukcji zachować osobno:
- ciągłość położenia i stycznej;
- fazę unwrapped i znak winding;
- orientację ramy / holonomię;
- identyfikację gałęzi i węzłów;
- informację o tym, co zostało usunięte lub scalone.

## 7. Priorytet kolejnych prac

1. Ustalić definicję środka czworościanu używanego w TIMDR (centroid, środek sfery opisanej czy inny konstrukcyjny punkt).
2. Wykonać E1: mapa dopuszczalnych orientacji przy przesunięciu środka; bez dopisywania dynamiki.
3. Dokończyć i utrzymać test geometrycznego liftu 2D→3D; zachować znak orientacji.
4. Zestawić operator liftu z rzeczywistą regułą przejścia wierzchołków czworościanu; nie zakładać, że BC jest automatycznie TIMDR.
5. Dopiero potem wybrać jeden mechanizm E2 i testować rotację.
6. Po każdym wyniku aktualizować tabelę OBSERVED / INTERPRETATION / MISSING LAW / FALSIFIER.

## 8. Kryterium postępu

Postępem nie jest dodanie kolejnej analogii ani dopasowanie krzywej do helisy. Postępem jest znalezienie operatora, który:
- zachowuje wskazane niezmienniki;
- przewiduje następny stan bez strojenia na wyniku;
- rozróżnia orientacje lustrzane, gdy znak ma znaczenie;
- ma jasno określone warunki brzegowe;
- daje wynik negatywny w kontrolach, w których mechanizm nie powinien działać.

**Wniosek roboczy:** nie próbujemy wyjaśnić wszystkich anomalii jednym słowem. Budujemy wspólny stan i sprawdzamy, czy jedna reguła przejścia potrafi odtworzyć kilka niezależnych anomalii bez utraty ich znaków, historii i warunków brzegowych.