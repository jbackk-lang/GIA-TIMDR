# TIMDR — wyniki drzewa odbić i podgrupy dwóch ścian

**Data:** 2026-11-09  
**Status:** eksperyment dokładny na liczbach wymiernych; wyniki geometryczne potwierdzone przez GitHub Actions.

## 1. Cel

Sprawdzić, czy enumeracja wszystkich czterech lokalnych odbić foremnego czworościanu szybko tworzy powtarzające się konfiguracje, helisę/węzeł albo zmianę skali. Nie przypisujemy gałęziom prawdopodobieństw ani nie wprowadzamy kontrakcji.

## 2. Dokładna enumeracja drzewa

Stanem jest nieuporządkowany zbiór czterech wierzchołków foremnego czworościanu. Jedno przejście odbija jeden wierzchołek przez płaszczyznę ściany przeciwległej. Cztery wybory dają cztery lokalne kontynuacje. BFS kanonizuje konfiguracje przez sortowanie czterech dokładnych punktów Fraction i pomija stany widziane wcześniej.

| Głębokość n | Nowe czworościany na poziomie |
|---:|---:|
| 0 | 1 |
| 1 | 4 |
| 2 | 12 |
| 3 | 36 |
| 4 | 108 |
| 5 | 324 |
| 6 | 972 |
| 7 | 2916 |

Liczba nowych stanów dla n>=1 w badanym zakresie:

\[N_n=4\cdot3^{n-1}.\]

Liczba wszystkich stanów od poziomu 0 do n:

\[S_n=1+\sum_{k=1}^{n}4\cdot3^{k-1}=2\cdot3^n-1.\]

Dla n=7 otrzymujemy 4373 różne czworościany. Środki czworościanów również są różne na każdym poziomie i między poziomami w tym zakresie. Wynik jest potwierdzony do głębokości 7, nie jest dowodem braku relacji na wszystkich głębokościach.

## 3. Korekta intuicyjnego liczenia

Nie należy liczyć naiwnie 4 -> 16 -> 64. W każdym stanie jedno z czterech odbić cofa bezpośrednio do rodzica. Po deduplikacji otrzymujemy 4 -> 12 -> 36 -> 108..., a nie pełne drzewo 4-arne.

## 4. Podgrupa generowana przez dwie ściany

Bierzemy dwie płaszczyzny ścian początkowego foremnego czworościanu. Przecinają się wzdłuż wspólnej krawędzi. Odbicie kolejno w tych dwóch stałych płaszczyznach daje złożenie dwóch odbić płaszczyznowych, czyli obrót wokół wspólnej krawędzi.

Dla foremnego czworościanu kwadrat cosinusa kąta między normalnymi tych płaszczyzn wynosi:

\[\cos^2\alpha=\frac{1}{9}.\]

Kąt obrotu złożenia spełnia:

\[\cos\varphi=2\cos^2\alpha-1=-\frac79.\]

W 24 kolejnych krokach otrzymano 24 różne środki czworościanów, a kwadrat odległości każdego środka od osi wspólnej krawędzi pozostaje dokładnie równy 1.

Ponieważ -7/9 jest wymierne, a nie należy do zbioru możliwych wymiernych wartości cosinusa kąta będącego wymierną wielokrotnością pi, kąt phi/(2 pi) jest niewymierny. Wynika stąd, że iteracje tego obrotu są gęste na okręgu dla każdego punktu poza osią. Jest to ścisły wniosek matematyczny o tej dwuściennej podgrupie, nie tylko obserwacja 24 próbek.

**Interpretacja:** z odbić mogą powstawać orbity o gęstym rozmieszczeniu na okręgu, bez losowości i bez skalowania. To uporządkowana dynamika izometryczna, nie fraktal.

## 5. Relacja do helisy BC

Istniejąca dokładna referencja BC ma stałą mapę śrubową o cos(theta)=-2/3; oś i przesunięcie osiowe są opisane w core/boerdijk_coxeter_tetrahelix.py.

To osobna sekwencja uporządkowanych odbić i rzeczywiście daje helisę. Dwuścienna sekwencja naprzemienna daje natomiast czysty obrót wokół krawędzi. Różne słowa w tych samych operacjach odbicia mogą więc dawać różne typy ruchu: śrubowy albo obrotowy.

## 6. Czy powstał fraktal?

Na razie nie. Każdy krok jest izometrią i zachowuje wszystkie sześć krawędzi czworościanu (kwadraty długości równają się 8). Nie występuje zmniejszanie skali. Eksponencjalny wzrost liczby stanów nie jest sam w sobie fraktalnością.

Wyniki sugerują raczej drzewo orbit grupy odbić, podgrupy o ruchu obrotowym z niewymiernym kątem oraz specjalne uporządkowane słowa dające ruch śrubowy (BC). Do hipotezy fraktalnej wrócimy po znalezieniu niezależnego mechanizmu zmiany skali lub wykazaniu niebanalnego prawa samopodobieństwa.

## 7. Reprodukcja

Kod: experiments/reflection_branch_tree.py, experiments/reflection_transition_bc_bridge.py, core/reflection_transition.py.

Uruchomienie: `python experiments/reflection_branch_tree.py`

CI: https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42600585012

Wynik CI: 15/15 testów jednostkowych PASS; most BC PASS; dokładna enumeracja drzewa do głębokości 7 PASS; 24 różne środki orbity dwuściennej i niezmiennik odległości od osi PASS.

## 8. Następny test

Następnie sklasyfikujemy krótkie słowa generatorów odbić (okresowe słowa długości 2, 3, 4, 5), wyznaczymy typ izometrii: obrót, przesunięcie śrubowe, translację lub odbicie, wyznaczymy warunki zerowego i niezerowego przesuwu osiowego oraz porównamy klasy słów z geometrią helikalną i węzłową.

To bada geometrię globalną bez dopisywania nieuzasadnionej siły, prawdopodobieństwa ani fraktalnego skalowania.