# TIMDR — operator przejścia zdarzenie–powierzchnia–odbicie–kształt (v0.1)

**Data:** 2026-11-09  
**Status:** propozycja formalizacji i plan testu; nie jest jeszcze prawem fizycznym ani potwierdzonym mechanizmem fraktalnym.

## 1. Cel i miejsce w architekturze

Dokument łączy istniejące elementy repozytorium:
- graf zdarzeń TRM/GIA: energia, czas i położenie;
- Chronoproces: rodzina trajektorii i powierzchnia zależna od czasu;
- geometria z grafu: krzywa, wstęga/rura i ramy normalne;
- dokładne odbicie punktu względem płaszczyzny oraz rekurencję czworościenną BC;
- gałęzie META/K/G jako miejsca zapisu obserwabli i wyników.

Brakującym elementem jest jawny operator przejścia, który określa, jak stan zdarzenia i kontakt z powierzchnią ograniczają następny moduł oraz — jeśli istnieje wiele dopuszczalnych kontynuacji — jak przypisuje się im prawdopodobieństwa.

## 2. Stan zdarzenia

Dla kroku n zapisujemy:

\[
X_n=(t_n,p_n,u_n,\Sigma_n,n_n,M_n,h_n),
\]

gdzie:
- t_n — czas zdarzenia;
- p_n — położenie zdarzenia w R^3;
- u_n — jednostkowy kierunek wejściowy;
- Sigma_n — lokalna powierzchnia kontaktu;
- n_n — jednostkowa normalna powierzchni w punkcie kontaktu;
- M_n — bieżący moduł/konfiguracja geometryczna;
- h_n — historia stanów i przejść potrzebna do sprawdzenia zależności od pamięci.

Graf zdarzeń już dostarcza t_n i p_n. Kierunek u_n można estymować z dwóch kolejnych pozycji tylko wtedy, gdy Δt_n>0 i p_n-p_(n-1) jest niezerowe. Jeżeli dostępna jest niezależna prędkość lub kierunek pomiarowy, należy użyć jej zamiast estymacji.

## 3. Powierzchnia i normalna

Jeśli Chronoproces daje regularną parametryzację powierzchni:

\[
\Gamma(t,s),
\]

to w punkcie (t_n,s_n) kandydacka normalna wynosi:

\[
n_n=\frac{\partial_t\Gamma\times\partial_s\Gamma}
{\|\partial_t\Gamma\times\partial_s\Gamma\|}.
\]

Warunek regularności to niezerowy iloczyn wektorowy. Gdy znika, normalna nie jest określona i operator musi zwrócić stan osobliwy/nieokreślony, a nie zgadywać kierunek.

Orientację normalnej trzeba zamrozić jedną konwencją. Odwrócenie znaku normalnej nie zmienia idealnego wzoru odbicia, ale ma znaczenie dla znakowanych kątów, stron powierzchni i klasyfikacji wejścia/wyjścia.

## 4. Geometria odbicia

Dla jednostkowego kierunku padającego u_n i jednostkowej normalnej n_n idealne odbicie zwierciadlane ma postać:

\[
u_n^{+}=u_n^{-}-2(u_n^{-}\cdot n_n)n_n.
\]

Kąt padania i odbicia mierzymy względem normalnej:

\[
\theta_i=\arccos(|u_n^{-}\cdot n_n|),\qquad
\theta_r=\arccos(|u_n^{+}\cdot n_n|),
\]

więc dla idealnego odbicia zachodzi theta_i=theta_r. To prawo jest deterministyczne. Nie jest samo w sobie rozkładem prawdopodobieństwa i nie tworzy automatycznie fraktala.

## 5. Zbiór dopuszczalnych kontynuacji

Niech B(X_n) oznacza skończony zbiór kandydackich następnych modułów/gałęzi. Kandydat b należy do B(X_n) tylko wtedy, gdy spełnia jawne warunki:
1. zgodność topologiczna połączeń;
2. warunki brzegowe i dopuszczalność geometryczna;
3. brak niedozwolonej degeneracji;
4. jawna reguła orientacji i sklejenia;
5. ograniczenia modelu źródłowego, w tym ewentualny mechanizm dodawania elementu.

Jeśli zbiór B(X_n) jest pusty, przejście jest niedopuszczalne. Nie wolno sztucznie normalizować prawdopodobieństwa na pustym zbiorze.

## 6. Jądro prawdopodobieństwa

Jeżeli istnieje więcej niż jedna dopuszczalna kontynuacja, definiujemy jądro:

\[
P(b\mid X_n)=0\quad\text{dla }b\notin B(X_n),
\]

\[
P(b\mid X_n)\geq0,\qquad
\sum_{b\in B(X_n)}P(b\mid X_n)=1.
\]

Sam kąt nie wyznacza tego rozkładu. Potrzebny jest mechanizm: zmierzona częstość, jawny model fluktuacji albo wcześniej określona funkcja kosztu/energii.

Jako model zerowy do testów można użyć rozkładu jednostajnego na B(X_n). Jako rodzinę modeli alternatywnych można prerejestrować:

\[
P_\beta(b\mid X_n)=
\frac{\exp[-\beta C(b\mid X_n)]}
{\sum_{c\in B(X_n)}\exp[-\beta C(c\mid X_n)]},
\]

gdzie C jest zdefiniowanym przed eksperymentem kosztem, a beta parametrem dopasowywanym wyłącznie na zbiorze treningowym. Ten zapis jest rodziną hipotez, nie twierdzeniem, że natura wybiera rozkład Boltzmanna. Wyniki trzeba porównać z modelem jednostajnym i deterministycznym.

## 7. Aktualizacja kształtu

Po wyborze b_następny stan wynosi:

\[
X_{n+1}=F(X_n,b_{n+1}).
\]

Mapa F musi jawnie zwracać co najmniej: nowy czas, położenie, kierunek, moduł, połączenia grafu, orientację i zapis historii. Jeżeli model przewiduje dodawanie elementów, operacja dodania musi poprzedzać test dopuszczalności i ewentualną redukcję; nie wolno zastępować jej arbitralnym usuwaniem helisy.

## 8. Test fraktalności — warunek konieczny

Powtarzane odbicia izometryczne zachowują skalę. Sama rekurencja odbicia nie dowodzi fraktalności.

Aby mówić o mechanizmie fraktalnym, trzeba wykazać rekurencyjne generowanie struktur na wielu skalach. Jednym z możliwych modeli jest rodzina map kontrakcyjnych:

\[
F_b: M\mapsto M_b,\qquad 0<r_b<1,
\]

z regułą wyboru b określoną przez jądro P. Następnie należy zbadać:
- czy istnieje zakres skal z powtarzalnym prawem;
- czy wymiar pudełkowy lub inny właściwy wymiar stabilizuje się przy zmianie rozdzielczości;
- czy wynik jest odporny na obrót, translację, zmianę próbkowania i małe perturbacje;
- czy wynik przewyższa kontrole: czyste izometrie BC, losowe rozgałęzianie bez geometrii oraz model niehelikalny.

Jeżeli nie ma kontrakcji ani innego wykazanego mechanizmu zmiany skali, wynik klasyfikujemy jako geometrię rekurencyjną, nie fraktalną.

## 9. Minimalny eksperyment rozstrzygający

1. Wczytać graf zdarzeń z (e_i,t_i,p_i) i zamrozić kalibrację GIA.
2. Zbudować powierzchnię z Chronoprocesu; zapisać parametryzację, domenę i konwencję normalnej.
3. Wyznaczyć u_n i n_n; odrzucić lub oznaczyć przypadki osobliwe.
4. Zastosować deterministyczne prawo odbicia i wygenerować zbiór dopuszczalnych kontynuacji.
5. Porównać trzy modele wyboru: deterministyczny, jednostajny i prerejestrowane jądro alternatywne.
6. Zastosować operator aktualizacji F, zachowując pełną historię przejść.
7. Zmierzyć geometrię, topologię, rozkłady kątów, skalę i stabilność; wykonać kontrole oraz walidację na danych niewykorzystanych do dopasowania.

## 10. Kryteria falsyfikacji

- Jeśli normalna powierzchni nie jest jednoznaczna lub niestabilna, hipoteza o odbiciu na tej powierzchni nie jest jeszcze testowalna.
- Jeśli tylko jedna kontynuacja spełnia warunki, model probabilistyczny redukuje się do deterministycznego wyboru.
- Jeśli częstości przejść nie różnią się od modelu jednostajnego/deterministycznego w prerejestrowanym teście, nie ma wsparcia dla postulowanego prawa probabilistycznego.
- Jeśli iteracje zachowują skalę, nie ma dowodu fraktalności.
- Jeśli wynik zależy od arbitralnego doboru promienia rury, ramki, progu lub zakresu skal, trzeba raportować tę zależność; nie jest to niezmiennik teorii.

## 11. Powiązanie z istniejącymi plikami

- docs/theory/TIMDR_EventGraph_Branch_Construction.md
- docs/theory/TIMDR_Geometry_From_EventGraph.md
- docs/theory/TIMDR_Chronoprocess.md
- core/boerdijk_coxeter_tetrahelix.py
- docs/geometry/ADDITION_INDUCED_REDUCTION_TRIANGLE_TETRAHEDRON_v0.1.md
- docs/geometry/TETRAHEDRON_CUBE_TWIST_ANGLE_PROOF_2026-11-09.md

## 12. Decyzja robocza

Najpierw implementujemy i testujemy deterministyczny łańcuch zdarzenie–powierzchnia–odbicie–kontynuacja. Dopiero gdy zbiór dopuszczalnych kontynuacji jest większy niż jeden i istnieją dane lub jawny mechanizm losowości, dodajemy jądro prawdopodobieństwa. Fraktalność pozostaje osobną hipotezą wymagającą wykazania zmiany skali.

**Wniosek:** brakującym ogniwem nie jest kolejny kąt, lecz dobrze określony operator przejścia F wraz z warunkami dopuszczalności i — opcjonalnie — jądrem P. To on połączy istniejący graf zdarzeń, Chronoproces i odbicie BC bez utożsamiania geometrii, prawdopodobieństwa i fraktalności.

## 13. Pierwsza implementacja operatora — 2026-11-09

Dodano:
- `core/reflection_transition.py` — normalną z dwóch stycznych powierzchni, deterministyczne odbicie kierunku, obiekt zdarzenia oraz opcjonalny softmax po jawnie podanym zbiorze kosztów gałęzi;
- `tests/test_reflection_transition.py` — testy zachowania normy prędkości, odwrócenia składowej normalnej, równości kątów, niezmienniczości względem skali normalnej, degeneracji powierzchni i normalizacji jądra gałęzi.

Ważne rozróżnienie: odbicie punktu czworościanu w `core/boerdijk_coxeter_tetrahelix.py` jest konstrukcyjną regułą generowania kolejnego wierzchołka. Odbicie wektora kierunku w `core/reflection_transition.py` jest prawem zwierciadlanego odbicia kierunku na powierzchni. Są matematycznie spokrewnione przez geometrię płaszczyzny, ale opisują różne obiekty i nie wolno ich utożsamiać bez dodatkowego mapowania stanu.

Softmax jest jedynie kandydacką rodziną rozkładów po dostarczonych kosztach. Nie jest wyprowadzony z kąta, nie jest jeszcze skalibrowany na danych i nie stanowi postulatu o fizycznej losowości.

**Status wykonania:** pliki zostały zapisane i ponownie odczytane z repozytorium. Testy zostały dodane, ale w tej sesji nie uruchomiono środowiska Pythona z pełnym checkoutem repozytorium; wynik testów pozostaje `NOT RUN`, a nie `PASS`.

## 14. Połączenie z rekurencją BC i enumeracja gałęzi — 2026-11-09

### 14.1. Tożsamość operatorów

Dla płaszczyzny Pi przechodzącej przez punkt a i mającej normalną n, odbicie punktu ma postać:

p' = a + [(p-a) - 2 ((p-a)·n)/(n·n) n].

To jest dokładnie przesunięcie początku układu do punktu a, zastosowanie odbicia wektora p-a, a następnie powrót do pierwotnego układu. Zatem odbicie punktu BC i odbicie wektora w operatorze przejścia są tym samym przekształceniem afinicznym, gdy wektor wejściowy jest liczony od punktu leżącego na płaszczyźnie.

Dodano adapter `reflect_tetrahedron_step` w `core/reflection_transition.py`. Dla okna `(oldest, face_a, face_b, face_c)` wyznacza normalną ściany i odbija najstarszy wierzchołek. Oryginalny `core/boerdijk_coxeter_tetrahelix.py` pozostaje dokładnym wzorcem `Fraction`; adapter jest numerycznym mostem, a nie zamiennikiem dokładnej implementacji.

### 14.2. Cztery geometryczne kontynuacje jednego czworościanu

Dodano `tetrahedron_face_reflection_candidates`. Dla nieosobliwego czworościanu enumeruje cztery kandydaty: odbicie każdego z czterech wierzchołków względem ściany przeciwległej. Każdy kandydat zachowuje wszystkie sześć długości krawędzi czworościanu. Dla czworościanu foremnego kandydaci są różni i symetryczni.

To daje ważne rozróżnienie:
- geometria dopuszcza cztery lokalne kontynuacje;
- reguła BC wybiera jedną z nich przez uporządkowanie historii (odbija najstarszy wierzchołek);
- sama geometria foremnego czworościanu nie wyróżnia jednej z czterech możliwości;
- dlatego z symetrii nie wynika niejednorodny rozkład prawdopodobieństwa. Rozkład jednostajny byłby dodatkowym założeniem symetrii, nie odkrytym prawem fizycznym.

### 14.3. Test reprodukowalny

Dodano `experiments/reflection_transition_bc_bridge.py`, uruchamiany z katalogu głównego:
`python experiments/reflection_transition_bc_bridge.py`

Skrypt sprawdza:
1. zgodność adaptera z dokładną rekurencją BC dla 36 kolejnych przejść w łańcuchu 40 wierzchołków;
2. istnienie czterech różnych kandydatów dla czworościanu foremnego;
3. zachowanie sześciu krawędzi w każdym kandydacie;
4. zgodność odbicia punktu i wektora dla ściany BC.

### 14.4. Wynik niezależnej kontroli algebraicznej

Kontrola na dokładnej arytmetyce wymiernej potwierdziła zerowy błąd między odbiciem punktu a wzorem odbicia punktu względem płaszczyzny dla 36 przejść BC. Osobna kontrola numeryczna kandydatów regularnego czworościanu dała cztery różne punkty:

(-5/3,-5/3,-5/3), (-5/3,5/3,5/3), (5/3,-5/3,5/3), (5/3,5/3,-5/3).

Każdy z czterech czworościanów potomnych ma sześć kwadratów długości krawędzi równych 8.

**Status testów po poprawkach:** GitHub Actions uruchomił testy w pełnym checkoutcie repozytorium. `python -m unittest tests.test_reflection_transition -v`: 15/15 PASS. Skrypt `python experiments/reflection_transition_bc_bridge.py`: PASS. Workflow: https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42600138401. Maksymalny błąd adaptera zmiennoprzecinkowego względem dokładnej rekurencji Fraction dla 36 kroków: 3.664e-15.

### 14.5. Konsekwencja dla hipotezy fraktalnej

Jeden krok daje cztery geometryczne kandydaty, ale wszystkie są pojedynczymi odbiciami izometrycznymi i zachowują skalę. Rozgałęzianie liczby stanów nie jest jeszcze fraktalem. Fraktalność wymaga wykazania rekurencyjnej samopodobności na wielu skalach, np. przez kontrakcje albo inny jawny mechanizm zmiany skali. Następny test powinien zatem iterować wszystkie cztery gałęzie z deduplikacją stanów i mierzyć liczbę odrębnych konfiguracji, kolizje, nakładanie oraz ewentualną zmianę skali — bez nadawania im z góry prawdopodobieństw.

**Wniosek po CI:** połączenie operatora odbicia z BC jest zweryfikowane numerycznie na dokładnym wzorcu geometrycznym w granicach tolerancji testu. Enumeracja czterech kandydatów również przeszła testy. Nie zweryfikowano jeszcze iteracji wielogałęziowej, prawa wyboru gałęzi ani fraktalności.
