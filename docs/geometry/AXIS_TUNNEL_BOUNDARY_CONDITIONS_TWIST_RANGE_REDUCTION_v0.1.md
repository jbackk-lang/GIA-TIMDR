# Priorytet badawczy: tunel osi, warunki brzegowe i zakres skrętu jako granica redukcji (v0.1)

**Data:** 2026-11-09  
**Status:** program formalizacji; nie jest jeszcze zwalidowanym modelem fizycznym.

## 1. Decyzja kierunkowa

Autor wskazuje, że diagonalne relacje √2 i √3 mają prawdopodobnie jedynie szczątkowy wpływ na właściwości helisy. Nie powinny być obecnie głównym mechanizmem konstrukcyjnym. Główny kierunek badania przesuwa się na:

1. tunel osi;
2. warunki brzegowe tego tunelu i przebiegów helikalnych;
3. dopuszczalny zakres skrętu;
4. granicę zakresu, przy której następuje redukcja.

Relacje √2/√3 pozostają pomocniczą hipotezą konstrukcyjną / kontrolą geometryczną, bez statusu źródła helisy.

## 2. Co rozumiemy przez tunel osi

Nie utożsamiamy osi z pojedynczą linią. Roboczo tunel osi to otoczenie wyróżnionej krzywej osiowej (A(s)), z lokalnym przekrojem poprzecznym i ograniczeniami dopuszczalnych trajektorii.

Dla promienia tunelu (r(s)>0):
[
\mathcal T_A=\{x\in\mathbb R^3:\operatorname{dist}(x,A)\le r(s)\}.
]

W obszarze, gdzie istnieje regularna rama poprzeczna (N(s),B(s)), punkt tunelu można lokalnie zapisać:
[
x(s,u,v)=A(s)+uN(s)+vB(s),\qquad u^2+v^2\le r(s)^2.
]

Rama Freneta nie może być używana bezwarunkowo w punktach zerowej krzywizny; w takich miejscach należy użyć stabilnej ramy Bishop/Fermi albo jawnych lokalnych przekrojów. Tunel może być prosty, zakrzywiony lub zamknięty; jego topologia i przekrój pozostają do wyprowadzenia z TIMDR.

## 3. Warunki brzegowe tunelu

Warunki należy rozdzielić na:

### 3.1. Brzeg poprzeczny
- ograniczenie odległości gałęzi od osi: (\rho_i(s)\le r(s));
- minimalny luz między gałęziami i ścianą tunelu;
- brak niedozwolonych przecięć;
- ciągłość / jawna reguła zmiany przekroju.

### 3.2. Brzeg osiowy
Dla tunelu otwartego określić wejście i wyjście. Dla zamkniętego sprawdzić:
[
A(0)=A(L),
]
oraz osobno zgodność stycznej, przekroju, ramy i orientacji po obiegu. Sama zgodność pozycji nie wystarcza.

### 3.3. Warunki sklejenia
Na każdym szwie zapisać:
- pozycję;
- styczną;
- ramę poprzeczną / holonomię;
- fazę;
- indeks gałęzi i ewentualną permutację;
- znak orientacji i odbicia;
- jednostronne wartości skrętu przed i po szwie.

### 3.4. Warunki regularności
Dla zakrzywionego tunelu promień przekroju musi być zgodny z lokalną geometrią osi. W szczególności lokalne współrzędne rurowe mogą tracić jednoznaczność, gdy przekrój jest zbyt szeroki względem promienia krzywizny osi lub gdy dalsze części osi zbliżają się do siebie. Należy mierzyć:
- krzywiznę osi (\kappa_A(s));
- promień krzywizny (1/\kappa_A(s)), gdy (\kappa_A>0);
- minimalną odległość między nieprzyległymi fragmentami osi;
- lokalną i globalną jednoznaczność projekcji na oś.

Nie przyjmujemy arbitralnego promienia tunelu.

## 4. Zakres skrętu jako zmienna sterująca

Wprowadzić zorientowaną, ciągłą wielkość kąta skrętu (\theta(s)) właściwą dla wybranego obiektu (np. obrót przekroju tunelu względem ramy transportowanej). Nie utożsamiać jej automatycznie z torsją Freneta ani skrętem powierzchniowym.

Lokalne tempo skrętu:
[
\omega(s)=\frac{d\theta}{ds}.
]

Dla każdej konfiguracji mierzyć:
- zakres (\theta(s)) i jego unwrapped value (bez redukcji modulo (2\pi));
- znak (\omega(s));
- zmianę znaku i punkty ekstremalne;
- skręt względny względem ramy Bishop / ramy źródłowej;
- holonomię po zamknięciu;
- zachowanie fazy na szwach.

Kąty modulo (360^\circ) nie wystarczą, bo mogą ukryć liczbę pełnych obrotów i orientację.

## 5. Redukcja jako zdarzenie na granicy dopuszczalności

Nie wpisujemy z góry wartości krytycznej. Definiujemy zbiór stanów dopuszczalnych:
[
\mathcal A=\{X: g_j(X)\ge0,\ j=1,\ldots,m\},
]
gdzie (X) zawiera oś, przekrój tunelu, gałęzie, fazy i ramy. Funkcje (g_j) reprezentują jawne warunki: luz poprzeczny, regularność, brak kolizji, zgodność fazy, domknięcie i ciągłość szwów.

Redukcja jest kandydatem na zdarzenie graniczne:
[
X(s)\in\mathcal A\quad\text{do chwili }s_c,
\qquad
\min_j g_j(X(s_c))=0.
]
Po przekroczeniu granicy stan może:
- utracić dopuszczalność;
- zmienić gałąź / orientację;
- wymagać zmiany topologii opisu;
- przejść do zredukowanej reprezentacji.

To, która możliwość zachodzi, musi wynikać z operatora redukcji. Nie zakładamy, że każda granica daje 4→3.

## 6. Hipoteza progu 90° — test, nie aksjomat

Wcześniejsza uwaga autora o punktach kardynalnych związanych z kątem przekraczającym 90° pozostaje hipotezą. Teraz należy ją testować jako możliwy próg dopuszczalności tunelu / ramy:
- zdefiniować dokładnie, między jakimi wektorami lub przekrojami mierzymy (\theta);
- odróżnić kąt lokalny, całkowity obrót i holonomię;
- porównać zachowanie dla (\theta<90^\circ), (=90^\circ) i (>90^\circ);
- sprawdzić, czy przy 90° znika luz, pojawia się osobliwość, kolizja lub niezgodność warunków brzegowych;
- wykonać perturbacje geometrii i rozdzielczości, aby sprawdzić stabilność progu.

Jeśli nie pojawia się żaden niezależny warunek graniczny przy 90°, kąt nie jest progiem redukcji w tym modelu.

## 7. Minimalny eksperyment obliczeniowy

### E1 — oś i tunel bez helikalnych gałęzi
Zbudować źródłową oś (A(s)), przekroje i miarę promienia tunelu. Sprawdzić regularność oraz jednoznaczność projekcji.

### E2 — jedna gałąź w tunelu
Wprowadzić jedną trajektorię poprzeczną. Mierzyć luz, fazę, orientację i skręt względem ramy transportowanej.

### E3 — trzy / cztery gałęzie
Dodać gałęzie bez narzucania równomiernego rozstawu. Sprawdzić kolizje, indeksy, permutacje, warunki szwów i domknięcie.

### E4 — sweep zakresu skrętu
Zwiększać ciągły parametr skrętu, zachowując pozostałe warunki. Wykreślić (g_j) względem kąta i znaleźć pierwszą utratę dopuszczalności.

### E5 — test redukcji
Dopiero po zidentyfikowaniu granicy sprawdzić, czy naturalna zmiana reprezentacji prowadzi do trzech gałęzi. Porównać niezmienniki przed/po i raportować utraconą informację.

### E6 — kontrole
Porównać oś prostą i zakrzywioną, tunel otwarty i zamknięty, ramę Freneta i Bishop, orientację lewą i prawą oraz geometrię kulistą i bez ograniczenia kulistego.

## 8. Kolejność priorytetów

1. Źródłowa definicja osi TIMDR.
2. Geometria tunelu osi i przekroju.
3. Warunki brzegowe wejścia/wyjścia i szwów.
4. Zorientowana miara skrętu i jej zakres dopuszczalny.
5. Lokalizacja granicy / punktów kardynalnych.
6. Operator redukcji na granicy.
7. Dopiero potem wpływ √2/√3, kuli i liczby modułów.

## 9. Kryterium sukcesu

Model będzie wnosił coś nowego dopiero wtedy, gdy:
- tunel osi jest wyprowadzony z pierwotnej konstrukcji TIMDR;
- warunki brzegowe są jawne i testowalne;
- zakres skrętu ma określoną definicję, orientację i jednostki;
- granica dopuszczalności jest wykrywana bez ręcznego ustawiania wyniku;
- redukcja zachodzi jako konsekwencja przekroczenia tej granicy;
- wynik jest stabilny na perturbacje i zachowuje pełny zapis orientacji/fazy.

**Decyzja:** główny wysiłek przenieść z relacji przekątnych √2/√3 na tunel osi, warunki brzegowe i zakres skrętu jako możliwy mechanizm wyzwalający redukcję.