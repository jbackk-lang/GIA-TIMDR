# Prerejestracja: operator trójkątny TIMDR → następny moduł → helisa (v0.1)

**Data:** 2026-11-09  
**Status:** CZĘŚCIOWO ODBLOKOWANY — autor wskazał, że obiektem są wierzchołki reprezentujące czworościan. Pozostałe parametry przejścia wymagają jawnego ustalenia lub testu wariantów.  
**Cel:** zdefiniować i przetestować operator generujący moduł helikalny z pierwotnego obiektu trójkątnego TIMDR, bez dopasowania wyniku po fakcie.  
**Punkt odniesienia:** BC exact reference oraz HC-01; nie są one założeniem wyniku TIMDR.

## 1. Co wiemy, a czego nie wiemy

Źródła GIA-TIMDR definiują trójkąt jako obiekt źródłowy/asymetrię (G2), zmianę pola normalnych powierzchni (G3) oraz operator kształtu Weingartena (G9). Archiwum TRM podaje relację boku a=r√3 i interpretację trzech stanów. Żadne z tych źródeł nie określa jeszcze jednoznacznego 3D operatora odbicia i sklejenia modułu.

Dlatego nie wpisujemy do prerejestracji wartości ani geometrii, których nie ma w źródle.

## 2. Pola definicji — muszą być jawne przed uruchomieniem

| Pole | Wartość / status |
|---|---|
| Obiekt reprezentowany | **USTALONE PRZEZ AUTORA:** wierzchołki jako reprezentacja czworościanu (cztery punkty definiujące bryłę), nie sam trójkąt ani sama rama |
| Współrzędne modułu bazowego | OPEN: cztery punkty w R³, kolejność/indeksacja, skala i jednostki |
| Czy moduł jest równoboczny czy asymetryczny | OPEN: parametry boków/kątów; nie zakładać asymetrii ani symetrii |
| Płaszczyzna odbicia | OPEN: trzy punkty/normalna i offset albo jawna reguła wyznaczenia |
| Strona odbicia | OPEN: reguła znaku/orientacji; nie wybierać po wyniku |
| Interfejs sklejenia | OPEN: wspólny wierzchołek, krawędź, ściana lub inna jawna relacja |
| Reguła transportu orientacji | OPEN: macierz/izometria albo jawna mapa nieliniowa |
| Reguła przyrostu fazy | OPEN: definicja i konwencja znaku |
| Reguła osi A(s) | OPEN: jak oś wynika z modułów, nie jako linia dopasowana po fakcie |
| Warunki szwu | OPEN: pozycja, styczna, rama, faza, indeks gałęzi |
| Jednostki / normalizacja | OPEN: jawne dla każdej długości, kąta i parametru |

**Ważne doprecyzowanie:** obiekt bazowy jest już określony jako czwórka wierzchołków reprezentująca czworościan. Kandydatem referencyjnym dla przejścia jest reguła BC: dla uporządkowanej czwórki (vₙ,vₙ₊₁,vₙ₊₂,vₙ₊₃) odbić vₙ względem płaszczyzny (vₙ₊₁,vₙ₊₂,vₙ₊₃), otrzymując vₙ₊₄, a następnie przesunąć okno o jeden wierzchołek. To jest jawna hipoteza operatora do przetestowania, nie automatycznie prawo TIMDR. Nie zakładamy jeszcze, że czworościan jest foremny. Wariant foremny daje znany wzorzec BC; wariant ogólny należy zbadać osobno.

**Pozostałe otwarte parametry:** współrzędne i metryka czworościanu bazowego, wybór/porządek wierzchołków (czy istnieje wyróżniony wierzchołek), oraz czy przejście ma być dokładnie odbiciem BC czy inną regułą wyprowadzoną z TIMDR.

## 3. Hipotezy do rozdzielenia

- **H-A (moduł):** helikalność wynika z lokalnej asymetrii pojedynczego modułu.
- **H-G (gluing/transport):** helikalność wynika z globalnej reguły odbicia, sklejenia lub transportu orientacji, nawet gdy moduł jest symetryczny.
- **H-AG:** potrzebne są oba mechanizmy.
- **H-0:** zadana reguła nie generuje helisy; otrzymujemy płaską, zamkniętą, chaotyczną lub nieciągłą trajektorię.

BC jest przykładem H-G w innym obiekcie: jego ściany są równoboczne, a obrót śrubowy wynika z reguły łączenia tetraedrów. Nie zakładamy, że TIMDR ma ten sam mechanizm.

## 4. Zamrożone kontrole i baseline'y

1. **BC:** dokładna konstrukcja referencyjna, która musi przejść test zachowania krawędzi i jednej transformacji śrubowej.
2. **HC-01:** analityczna helisa kołowa do kontroli κ, τ_FS, promienia i skoku.
3. **Null:** ta sama liczba modułów z losową/niehelikalną regułą orientacji, jawnie wygenerowaną z ustalonym seedem; nie wolno jej stroić po wyniku.
4. **Mirror:** lustrzane odbicie całej konstrukcji i sprawdzenie transformacji miar orientowanych.
5. **No-glue / broken-seam:** kontrola, w której warunek sklejenia jest celowo naruszony; nie może być błędnie klasyfikowana jako regularna helisa.

## 5. Protokół po uzupełnieniu definicji

1. Zbudować bazowy czworościan z czterech uporządkowanych wierzchołków.
2. Wyznaczyć operator S_TIMDR wyłącznie z minimalnego prefiksu (np. pierwszych 3–4 modułów).
3. Zamrozić operator i przewidzieć kolejne co najmniej 20 modułów bez ponownego dopasowania.
4. Zmierzyć błąd predykcji, zachowanie długości/kątów, ciągłość szwów, fazę i orientację.
5. Sprawdzić, czy operator jest sztywną izometrią, transformacją śrubową, czy zależy od stanu.
6. Wyznaczyć oś z operatora i sprawdzić stałość promienia oraz postępu osiowego.
7. Porównać krzywą osi z HC-01; obliczyć κ, podpisaną τ_FS, długość łuku i pitch.
8. Powtórzyć dla odbicia lustrzanego; nie usuwać znaku torsji.
9. Wykonać oddzielne warianty: symetryczny moduł/stałe sklejenie, asymetryczny moduł/stałe sklejenie oraz stały moduł/zmienione sklejenie.
10. Raportować wynik negatywny, jeśli nie powstaje regularna helisa lub operator nie przewiduje holdoutu.

## 6. Metryki i kryteria

- błąd predykcji kolejnych modułów;
- odchylenie długości krawędzi i kątów od wartości zadanych;
- błąd domknięcia C0/C1 na szwach;
- obrót ramy i holonomia;
- przyrost fazy (unwrapped) i jego wariancja;
- promień osi i postęp osiowy na krok;
- krzywizna i podpisana torsja ciągłej osi, jeśli oś jest gładka;
- minimalna odległość nieprzyległych fragmentów;
- niezmienniki grafu/połączeń, jeśli obiekt jest grafem lub węzłem.

Kryterium „helisa” nie może być jedynie wizualne. Co najmniej: operator ma przewidywać moduły holdout, istnieje regularna oś/krzywa, a promień i przyrost osiowy są stałe w granicach tolerancji prerejestrowanych przed testem.

## 7. Czego nie robić w tym eksperymencie

- nie zakładać progu 90°, 120°, 5→6 ani 4→3;
- nie dodawać kuli/jaja jako mechanizmu, zanim istnieje oś i moduł;
- nie stroić reguły odbicia, fazy lub tolerancji na holdoucie;
- nie utożsamiać kąta dwuściennego, kąta śrubowego, τ_FS, T_S i pola MetaState.tau;
- nie podawać otwartego łańcucha do cyklicznego G5 przez sztuczne połączenie końców;
- nie interpretować wyniku geometrycznego jako dowodu fizycznego sprzężenia lub pamięci informacji.

## 8. Decyzja i następny krok

Autor ustalił, że czworościan jest reprezentowany przez swoje wierzchołki. W następnym kroku testujemy jawnie wariant BC: odbicie jednego wierzchołka przez płaszczyznę przeciwległej ściany i przesunięcie uporządkowanego okna o jeden punkt. Równolegle nie zakładamy foremności: należy porównać czworościan foremny z ogólnym czworościanem i sprawdzić, kiedy istnieje stała transformacja śrubowa.

Eksperyment jest odblokowany dla tego wariantu referencyjnego. Wynik BC nie może być przedstawiony jako wynik TIMDR, dopóki autor nie potwierdzi, że właśnie ta reguła odbicia/sklejania jest zamierzona. Pozostałe parametry geometryczne należy zamrozić przed testem holdout.


## 9. Aktualizacja implementacyjna po decyzji autora (2026-11-09)

Autor potwierdził reprezentację czworościanu przez jego wierzchołki. W `core/boerdijk_coxeter_tetrahelix.py` uogólniono rekurencję do `generate_tetrahedral_chain(initial_vertices, count)`: wejściem jest dokładnie cztery niekoplanarne punkty; najstarszy punkt jest odbijany względem płaszczyzny pozostałych trzech, a okno czterech wierzchołków przesuwa się o jeden. Arytmetyka pozostaje dokładna (`Fraction`).

Dodano test dla ogólnego, nierównego czworościanu, który sprawdza, że wszystkie sześć długości krawędzi każdego kolejnego czworościanu jest identyczne z bazowym. Dodano też odrzucanie koplanarnego zestawu wejściowego. To potwierdza zachowanie kongruencji kolejnych modułów przy tej regule odbicia, ale **nie** dowodzi stałej transformacji śrubowej dla dowolnego czworościanu. Stała transformacja BC jest potwierdzona dla regularnego czworościanu.

CI dla najnowszego commita testowego: `42590580686` (w toku w chwili aktualizacji; wynik należy sprawdzić przed uznaniem testów za zaliczone).

**Status:** decyzja o reprezentacji obiektu — ustalona; reguła odbicia BC — zaimplementowana jako kandydat referencyjny; zgodność tej reguły z zamierzoną regułą TIMDR — wymaga jeszcze potwierdzenia autora. Następny test porówna regularny i ogólny czworościan pod kątem istnienia stałego operatora śrubowego, zamiast zakładać, że każdy łańcuch odbić jest helisą o stałym skoku.


**Wynik CI po uogólnieniu:** run `42590580686` — SUCCESS, **9/9 testów**. Dwa nowe testy obejmują ogólny czworościan (zachowanie wszystkich sześciu krawędzi w kolejnych oknach) oraz odrzucenie koplanarnego wejścia. Link: https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42590580686


## 10. Nowe ograniczenie autora: otoczenie sferyczne wymaga podwójnej reprezentacji albo wariantu jajowatego

Autor zwrócił uwagę, że czworościan musi być badany w swoim otoczeniu: w wariancie kuli może wymagać podwójnej reprezentacji, alternatywnie należy rozważyć powierzchnię jajowatą. Nie wolno więc kończyć analizy na swobodnym łańcuchu BC.

Zapisano dwa warianty w `docs/geometry/SPHERICAL_ENCLOSURE_DOUBLE_TETRAHEDRON_OR_EGG_v0.1.md`:
- S: czworościan i partner antypodyczny względem środka sfery, (v_i^*=2c-v_i). Dla regularnego czworościanu w znanej orientacji suma obu zestawów daje dokładnie osiem naroży sześcianu wpisanego w sferę.
- E: asymetryczna powierzchnia jajowata jako ograniczenie. Nie ma ona zwykłej symetrii antypodycznej, więc nie można przenieść parowania z kuli bez nowej mapy.

To są dwa warianty testowe, nie rozstrzygnięcie, co autor rozumie przez „podwójną reprezentację”. Nie utożsamiać jej z podwójnym pokryciem topologicznym, odbiciem lustrzanym ani antycząstką.


**Korekta geometrii otoczenia:** nie interpretować „podwójnej reprezentacji” jako pary antypodycznej. Autor wskazał anomalię przesunięcia środków (d=C_t-C_s). Przed generowaniem operatora należy określić, jaki środek czworościanu jest używany oraz uwzględnić ograniczenie (\|d+Qp_i\|\le R). Orientacyjna zależność wynika z geometrii; reguła dynamiczna generująca rotację pozostaje do wyprowadzenia. Szczegóły: `docs/geometry/SPHERICAL_ENCLOSURE_DOUBLE_TETRAHEDRON_OR_EGG_v0.1.md` §8.


## 11. Aktualizacja po twierdzeniu czterokrokowym dla czworościanu ogólnego — 2026-11-09

Wcześniejszy zapis w §9, że zachowanie krawędzi nie dowodzi stałej transformacji śrubowej dla dowolnego czworościanu, należy teraz czytać precyzyjnie: nie dowodzi on operatora **jednokrokowego**. Nowy wynik w `docs/geometry/GENERAL_TETRAHEDRON_FOUR_STEP_SCREW_THEOREM_v0.1.md` wykazuje, że dla dowolnego niekoplanarnego czworościanu uporządkowana metryka okna wraca po czterech przesunięciach, co daje jedną właściwą izometrię `T` z `T(v_n)=v_{n+4}` dla całego łańcucha.

To jest własność matematyczna referencyjnej rekurencji BC. Nie przesądza, że TIMDR używa tej reguły odbicia; nadal wymaga to potwierdzenia autora. Jeżeli reguła BC zostanie przyjęta jako model, należy badać cztery przeplatane orbity wspólnego operatora, nie zakładać pojedynczej helisy ani fraktalności.
