# Audyt repozytoriów koncepcyjnych: wskazówki dla tunelu osi i granicy redukcji (2026-11-09)

**Cel:** odzyskać wcześniejsze pojęcia i ograniczenia z TIMDR-Concept-Archive oraz Helix-Lock, które mogą ukierunkować badanie geometrycznego tunelu helisy, warunków brzegowych i progu redukcji.

**Status:** audyt źródeł i hipotez. Archiwalne repozytoria TRM jawnie opisują się jako koncepcyjne, nie jako zwalidowana teoria empiryczna. Wnioski poniżej nie są dowodem fizycznym.

## 1. Najważniejsze znalezisko: geometria koła i kwadratów współosiowych

Źródło: `TIMDR-Concept-Archive/TRM-Geometry-Core/README.md`, `docs/core.md`, `docs/quadrature.md`, `docs/proof.md`.

Rdzeń geometryczny nie zaczyna się od √2/√3, lecz od:
- koła jako cyklu / pełnej rotacji;
- kwadratu wpisanego i opisanego na tym samym okręgu jako dwóch różnych granic geometrycznych;
- Λ jako struktury / maksymalnego zasięgu;
- τ jako stanu przejściowego / minimalnego zasięgu;
- ρ jako różnicy/defektu między stanami.

Dokumenty postulują brak izometrii między kwadratem wpisanym a opisanym bez zmiany skali lub orientacji. To nie jest jeszcze formalny dowód skrętu ani tunelu, ale jest znacznie bliższą wskazówką do modelu przekroju i jego granic niż sama suma przekątnych.

Dla koła promienia r:
- kwadrat wpisany ma bok (a_{in}=\sqrt2 r) (jego przekątna to średnica (2r));
- kwadrat opisany ma bok (a_{out}=2r);
- stosunek boków wynosi (a_{out}/a_{in}=\sqrt2).

Ta relacja daje konkretną, ścisłą parę granic przekroju. Uwaga: jest to różnica rozmiaru dwóch kwadratów, a nie dowód że geometria ma fizyczny skręt. Orientacja kwadratów jest różna tylko wtedy, gdy taką orientację jawnie zadamy; sam wpisany/opisany kwadrat osiowo symetryczny nie wyznacza unikalnego skrętu.

W archiwalnym core występuje też kwadratura koła (a=r\sqrt\pi). To bok kwadratu o polu równym polu koła, ale nie konstrukcja cyrklem i linijką; nie mieszać tego operatora z √2/√3 ani z przekątnymi.

## 2. Druga wskazówka: kula i sześcian jako obwiednia / ograniczenie przestrzenne

Źródła: `TRM-Geometry-Core/docs/sphere.md`, `docs/cube.md`, `docs/core.md`.

Sześcian wpisany w kulę spełnia:
[
a\sqrt3=2r,\qquad a=\frac{2r}{\sqrt3}.
]
To określa maksymalny sześcienny moduł mieszczący się w kuli o promieniu r. Jest to relacja osadzenia i granicy przestrzennej, nie przekątna czworościanu.

W połączeniu z kołem/kwadratami sugeruje to program: badać przekrój poprzeczny i przestrzenną obwiednię tunelu jako ograniczenia dopuszczalnej konfiguracji. Nie narzucać jeszcze, że sześcian jest przekrojem tunelu ani że kula generuje skręt.

## 3. Wskazówka z TRM: skręt krytyczny i gęstość ρ

Źródła: `Topological-Reduction-Model-TRM/README.md`, `core/topological-wave.md`, `core/operators.md`, `core/twist-reduction-law.md`, `math/reduction-equations.md`.

Archiwalna logika ma postać:
- τ: poziom skrętu / złożoności;
- ρ: gęstość informacji / nasycenie kształtu;
- Λ: skala;
- J: punkt przejścia;
- fala (	au(x,t)=	au_0+\delta\tau(x,t));
- przejście przy (|\tau|>\tau_{krit});
- redukcja (R(\tau)=k|\tau|^n) (w części plików znak wartości bezwzględnej nie jest jawny);
- narracyjny warunek przeciążenia ρ i niemożności dalszego wzrostu gęstości / rozproszenia gradientu.

To daje dwuczynnikową hipotezę granicy: nie sam kąt skrętu, lecz skręt w relacji do dostępnego luzu / pojemności przekroju i nasycenia ρ może uruchamiać przejście. Warto więc rozdzielić:
1. geometryczny limit tunelu (luz, samoprzecięcia, regularność);
2. orientacyjny limit ramy (obrót i holonomia);
3. limit nasycenia/pojemności modelu (ρ);
4. punkt J, w którym zmienia się reżim.

Zastrzeżenie: archiwalne (R=k\tau^n), (\tau_{krit}) i przykłady makroskopowe są postulowane koncepcyjnie. Nie są wyprowadzonym prawem dla helisy. W GIA-TIMDR należy najpierw zdefiniować wielkości geometryczne i dopiero sprawdzić, czy istnieje analogiczny próg.

## 4. Ważne doprecyzowanie z Helix-Lock: tunel jest geometryczny, sygnał jest na nim układany

Źródła: `Helix-Lock/docs/HELIX_LOOP_PARAMETER_BOUNDS.md`, `experiments/helical_tunnel_chirality.py`, `tests/test_helical_tunnel_chirality.py`.

Dokument Helix-Lock jawnie doprecyzowuje, że tunel to geometryczny tunel helisy, nie tunel informacyjny. Sygnał jest mapowany/układany na geometrii tunelu z uwzględnieniem orientacji. To rozróżnienie powinno być kanoniczne w dokumentacji GIA-TIMDR.

Eksperyment syntetyczny na helisie:
[
r(t)=(a\cos t,a\sin t,ht)
]
pokazuje:
- (kappa=a/(a^2+h^2));
- (	au_{FS}=h/(a^2+h^2));
- odbicie lustrzane zachowuje krzywiznę, odwraca znak torsji;
- sygnał z fazą zależną od handedness jest kowariantny względem odbicia;
- stały znak fazy nie jest;
- aktualny G5 używa (|\tau|), więc macierz i widmo są identyczne dla helisy prawej i lewej — znak/chiralność ginie.

Testy sprawdzają te własności numerycznie dla modelu syntetycznego. To nie dowodzi odzyskiwania dowolnego sygnału ani modelu fizycznego TIMDR, ale daje bezpośrednią wskazówkę implementacyjną: orientacja tunelu musi sterować orientacją lokalnej ramy i znakiem kierunku fazy sygnału.

Nie wolno wstawiać ujemnego τ bezpośrednio jako ujemnej wagi sprężyny G5; może to naruszyć dodatnią określoność macierzy. Chiralność powinna być przenoszona jako osobna zmienna orientacji/operator transportu, a nie jako nieprzemyślany znak sprzężenia.

## 5. Co audyt mówi o „zakresie skrętu”

Dokument Helix-Lock podkreśla, że standardowa helisa nie ma uniwersalnego limitu liczbowego κ lub τ bez określenia skali, promienia i skoku. Ponadto w obecnym G5 dodatnia określoność M, K, Γ nie daje górnej granicy (|τ|), gdy sprzężenia są dodatnimi wagami laplasjanu pierścienia.

Wniosek: nie szukać jednej uniwersalnej liczby kąta bez modelu tunelu i jego wymiarów. Próg redukcji powinien wynikać z konkretnego warunku geometrycznego (np. utrata jednoznaczności przekroju, kolizja gałęzi, zerowy luz, niesklejalna rama/faza) lub jawnego prawa dynamiki.

Kąt 90° pozostaje testem autora, nie potwierdzonym progiem. W szczególności kąt dwuścienny sześcianu 90° nie ustanawia automatycznie limitu skrętu helisy.

## 6. Synteza: kandydat na model granicy tunelu

Niech:
- (A(s)) — oś geometryczna;
- (r_t(s)) — promień / funkcja przekroju tunelu;
- (q_i(s)) — położenie gałęzi względem osi i ramy;
- (\theta_i(s)) — zorientowana faza/obrót przekroju;
- (\chi\in\{-1,+1\}) — handedness;
- (\rho(s)) — wskaźnik nasycenia, dopiero do zdefiniowania operacyjnie.

Dla każdego s mierzyć geometryczny luz:
[
g(s)=r_t(s)-\max_i\|q_i(s)\|.
]
Warunek dopuszczalności podstawowej: (g(s)>0), wraz z osobnymi warunkami braku kolizji gałęzi, regularności osi, jednoznaczności projekcji i zgodności szwów.

Kandydat na punkt graniczny:
[
s_c=\inf\{s:g(s)=0\ \text{lub inny jawny warunek brzegowy przestaje być spełniony}\}.
]
Nie utożsamiać (g=0) z redukcją automatycznie. To najpierw utrata luzu; następnie trzeba sprawdzić, czy model ma określony operator reorganizacji 4→3, zmianę gałęzi czy tylko awarię geometrii.

Do tego dołączyć test krytycznego skrętu:
[
|\theta(s)|\ge\theta_{krit}
]
ale (\theta_{krit}) musi być wyznaczony z geometrii i warunków brzegowych, nie przyjęty z góry. Zachować (chi) i znak torsji; nie redukować do wartości bezwzględnej na etapie analizy.

## 7. Najbardziej użyteczne wskazówki do dalszych badań

1. Zacząć od dwóch granic przekroju kołowego: kwadratu wpisanego i opisanego (stosunek boków √2); potraktować to jako model Λ/τ/ρ z archiwum, nie jako dowód skrętu.
2. Dodać przestrzenną obwiednię kuli i wpisanego sześcianu (a=2r/√3) jako niezależny test ograniczenia 3D.
3. Zdefiniować geometryczny tunel osi i transport ramy Bishop/parallel, nie polegać na Frenecie w punktach małej krzywizny.
4. Mapować sygnał na tunel, z fazą i kolejnością zgodną z chiralnością.
5. Zmierzyć osobno luz geometryczny, kąt skrętu, holonomię, fazę, kolizje i ρ.
6. Zdefiniować J jako wykrywalne zdarzenie przejścia (np. pierwsza utrata warunku brzegowego), a nie używać nieuzasadnionej formuły (d^2I/dt^2=0) bez definicji I dla geometrii tunelu.
7. Dopiero po wykryciu granicy sprawdzić, czy redukcja 4→3 wynika z operatora i które niezmienniki zachowuje.

## 8. Źródła przejrzane

- TIMDR-Concept-Archive: `TRM-Geometry-Core/README.md`, `docs/core.md`, `docs/transitions.md`, `docs/circle.md`, `docs/quadrature.md`, `docs/sphere.md`, `docs/triangle.md`, `docs/cube.md`, `docs/proof.md`, `mapa.md`.
- TIMDR-Concept-Archive: `Topological-Reduction-Model-TRM/README.md`, `core/operators.md`, `core/topological-wave.md`, `core/twist-reduction-law.md`, `core/phi-limit.md`, `math/reduction-equations.md`.
- TIMDR-Concept-Archive: `topologia-informacji/operators/Tau.md`, `operators/Tw.md`, `operators/Rho.md`, `axioms/R1-R7.md`, `axioms/R8-R10.md`, `docs/PROCES_TOPOLOGII.md`.
- Helix-Lock: `docs/HELIX_LOOP_PARAMETER_BOUNDS.md`, `experiments/helical_tunnel_chirality.py`, `tests/test_helical_tunnel_chirality.py`.

## 9. Konkluzja

Najbardziej obiecujący trop z repozytoriów koncepcyjnych to **para granic przekroju (wpisany/opisany kwadrat) + przestrzenna obwiednia (kula/sześcian) + krytyczny skręt τ i nasycenie ρ**. To może pomóc zdefiniować geometryczny tunel i warunek jego przeciążenia. Dodatkowo Helix-Lock potwierdza, że sygnał musi respektować chiralność tunelu, a aktualny G5 ją gubi przez (|τ|).

To nadal program badawczy. Żadne z tych źródeł nie dowodzi jeszcze, że geometryczna utrata luzu wywołuje naturalną redukcję czterech gałęzi do trzech.
