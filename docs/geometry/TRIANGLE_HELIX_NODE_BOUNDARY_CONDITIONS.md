# Trójkąt → redukcja → węzeł trójhelikalny: warunki brzegowe, skręt i punkty kardynalne

**Status:** program formalizacji; hipotezy użytkownika zapisane bez uznawania ich za dowiedzione  
**Wersja:** 0.1 · 2026-11-09  
**Repozytorium nadrzędne:** GIA-TIMDR  
**Powiązane dokumenty:**
- `../theory/HELIX_TIMDR_RESEARCH_PROGRAM.md`
- `HELIX_SENSITIVITY_REPRODUCIBILITY.md`
- źródła archiwalne w `TIMDR-Concept-Archive/TRM-Geometry-Core` i `Topological-Reduction-Model-TRM`

## 0. Teza robocza przekazana przez autora TIMDR

Badanie helisy ma uwzględniać jej genezę sygnałową, a nie zaczynać od dowolnej krzywej 3D.

Roboczy ciąg koncepcyjny:

**trajektoria trójkąta → redukcja → struktura trójhelikalna / węzeł trójhelikalny → oś i punkty kardynalne → sygnał / reprezentacje pola i struny.**

Dodatkowa hipoteza: redukcja może prowadzić do postaci trójwęzłowej z postaci czterowęzłowej. Należy sprawdzić, czy jest to:
- redukcja opisu lub liczby niezależnych stopni swobody;
- kontrakcja grafu / kompleksu;
- projekcja geometryczna;
- rzeczywista zmiana typu topologicznego osadzenia;
- czy też przejście wymagające dodatkowych założeń o przestrzeni lub „rzeczywistości” modelu.

To są różne operacje i nie wolno ich utożsamiać. W szczególności samo uproszczenie rysunku czworowęzła do trzech widocznych ramion nie dowodzi topologicznej równoważności z trójwęzłem.

## 1. Źródła odnalezione w repozytoriach

### 1.1. TRM-Geometry-Core

W `TIMDR-Concept-Archive/TRM-Geometry-Core/docs/triangle.md` trójkąt równoboczny jest interpretowany jako trzy stabilne stany, trzy fazy cyklu i trzy punkty stabilizacji w polu skrętu. Podano relację boku do promienia okręgu opisanego (a=\sqrt{3}r).

W `docs/proof.md` wyprowadzono tę relację z klasycznej geometrii trójkąta równobocznego. To jest poprawna relacja geometryczna, ale sama nie dowodzi jeszcze, że trajektoria sygnału TIMDR jest trójkątna ani że redukcja generuje helisę.

W `docs/core.md` i `docs/transitions.md` zapisano przejścia między figurami jako transformacje skali bez utraty informacji. Ten mocniejszy postulat wymaga osobnej definicji mapy, dziedziny, przeciwdziedziny i dowodu zachowania informacji. Równoważność pól lub długości skali nie implikuje automatycznie bijekcji ani zachowania topologii.

### 1.2. Topological-Reduction-Model-TRM

W archiwum TRM znajduje się prawo skrętu i redukcji (R=k\tau^n), sekwencja poziomów (	au_3\to\tau_2\to\tau_1\to\phi), oraz opis fali jako zmiany skrętu (	au(x,t)=\tau_0+\delta\tau(x,t)).

README TRM wyraźnie oznacza ten model jako koncepcyjny / narzędzie do myślenia, nie zweryfikowaną teorię empiryczną. Dlatego te równania traktujemy jako hipotezy modelowe, a nie potwierdzone prawa fizyczne.

### 1.3. Istniejąca geometria trefoil w GIA-TIMDR

`docs/geometry/TIMDR_Trefoil_FrenetTorsion.md` i kod `core/trefoil_frenet_torsion.py` opisują konkretną zamkniętą krzywą trefoil oraz jej krzywiznę i torsję Freneta-Serreta. To użyteczny obiekt testowy, ale nie należy zakładać, że jest to dokładnie ten sam obiekt co postulowany przez autora „węzeł trójhelikalny”.

## 2. Rozdzielenie terminów

W całym dalszym badaniu należy rozróżniać:

1. **Trójkąt** — figura / trajektoria bazowa; należy ustalić, czy chodzi o trójkąt geometryczny, trajektorię po jego krawędziach, czy cykliczną trajektorię stanów.
2. **Redukcja** — operator, który musi być jawnie określony. Może zmniejszać wymiar opisu, liczbę stanów, liczbę węzłów grafu albo złożoność reprezentacji; te znaczenia nie są równoważne.
3. **Węzeł trójhelikalny** — postulowana struktura trzech helikalnych gałęzi / ramion. Trzeba odróżnić ją od klasycznego węzła matematycznego trefoil.
4. **Oś helisy** — wyróżniona linia lub krzywa odniesienia. Należy określić, czy jest osią geometryczną, osią ewolucji parametru, czy osią sygnału.
5. **Punkty kardynalne** — wyróżnione punkty na osi lub względem osi. Ich liczba, definicja i reguła orientacji są na razie otwarte.
6. **Skręt w węźle** — może oznaczać torsję Freneta-Serreta, skręt pasma, liczbę skręcenia, linking, crossing lub fazowy obrót modalny. Każda wielkość musi mieć własną definicję.
7. **Sygnał** — obserwowana wielkość pochodząca z trajektorii / projekcji. Trzeba wskazać operator obserwacji i to, które informacje zostają utracone.

## 3. Model bazowy: trajektoria trójkąta

Przed przejściem do helisy należy formalnie określić trajektorię bazową.

Kandydat minimalny: trzy stany (q_0,q_1,q_2) i trzy przejścia cykliczne (q_0\to q_1\to q_2\to q_0). W geometrii euklidesowej może to być trójkąt równoboczny, ale model nie może zakładać równych boków, równych czasów ani symetrii, jeśli nie wynikają z kodu lub aksjomatów źródłowych.

Do zapisu trajektorii wymagane są:
- współrzędne wierzchołków / stanów;
- parametryzacja każdego odcinka;
- reguła przejścia na wierzchołku;
- orientacja obiegu;
- czas lub parametr ewolucji;
- warunek zamknięcia;
- ewentualne opóźnienie, skok fazy lub pamięć przejścia;
- operator mapujący trajektorię na sygnał.

### 3.1. Warunek zamknięcia i szew

Dla trajektorii zamkniętej (q(0)=q(T)). Jeżeli sygnał zawiera pochodne lub fazę, samo domknięcie pozycji nie wystarcza: trzeba osobno sprawdzić zgodność stycznej, krzywizny, torsji i fazy na szwie.

Testy szwu:
- (q(0)=q(T));
- (q'(0)=q'(T)), jeśli wymagana jest gładkość klasy (C^1);
- (q''(0)=q''(T)), jeśli wymagana jest (C^2);
- zgodność fazy modulo (2\pi);
- zgodność orientacji i reguły przejścia przez punkt kardynalny.

Jeżeli trajektoria jest otwarta, należy jawnie podać warunki początkowe i końcowe zamiast wymuszać periodyczność.

## 4. Redukcja czworowęzła do trójwęzła — hipoteza R-43

Hipoteza autora: redukcja może naturalnie przekształcać strukturę czterowęzłową w trójwęzłową.

Nie przyjmujemy z góry, że jest to „usunięcie jednego węzła”. Należy zbadać co najmniej cztery modele:

### R-43a. Redukcja stopni swobody
Cztery zmienne / stany mają więź, symetrię lub zależność, przez którą jedna kombinacja nie jest niezależna. Po ilorazowaniu pozostają trzy niezależne stopnie swobody. Liczba węzłów geometrycznych nie musi się zmienić.

### R-43b. Kontrakcja grafu
Czwarty węzeł grafu jest kontraktowany lub identyfikowany z innym węzłem. Trzeba określić, co dzieje się z krawędziami, orientacją, wagami, cyklami i lokalnym stopniem wierzchołka. Kontrakcja może zmienić topologię grafu.

### R-43c. Projekcja / obserwacja
Czteroelementowa struktura jest obserwowana w trzech wymiarach lub przez trzy kanały. Wtedy „czwarty węzeł” może być ukryty, nakładać się na inny albo być nierozróżnialny w projekcji. To nie oznacza, że zniknął z obiektu źródłowego.

### R-43d. Redukcja topologiczna osadzenia
Zmienia się samo osadzenie / klasa węzła. Taka zmiana wymaga jawnej rodziny deformacji i wskazania, czy dopuszcza się przecięcia, rozcięcia, sklejenia lub osobliwości. W zwykłej izotopii węzłów nie można zmienić typu węzła przez gładką deformację bez samoprzecięcia.

**Kryterium rozstrzygające:** zdefiniować niezmienniki przed i po redukcji (np. liczba składowych, stopnie wierzchołków grafu, liczba cykli, linking, liczba skręcenia pasma, grupa podstawowa dopełnienia — tylko jeśli właściwy obiekt topologiczny został zdefiniowany). Następnie wykazać, które z nich są zachowane, a które celowo tracone.

## 5. Węzeł trójhelikalny: osie, gałęzie i skręty

Minimalny model powinien oddzielać:
- oś centralną (A(s));
- trzy gałęzie (H_i(s)), (i=0,1,2);
- lokalne ramy normalne / bazę poprzeczną;
- fazę każdej gałęzi (	heta_i(s));
- promień lub odległość od osi (r_i(s));
- skok / tempo osiowe;
- regułę spotkania, przejścia lub rozdzielenia gałęzi w węźle.

Nie zakładać, że trzy gałęzie są równomiernie rozmieszczone o (120^\circ). To hipoteza symetrii do testu, nie warunek domyślny.

### 5.1. Rozróżnienie skrętów

Dla każdego węzła / gałęzi rejestrować oddzielnie:
- torsję Freneta-Serreta (	au_{FS}(s)) osi lub krzywej;
- skręt geometryczny pasma (twist);
- writhe osi / krzywej;
- linking number par gałęzi, jeśli gałęzie tworzą rozłączne krzywe zamknięte;
- fazę modalną (	heta_i(s));
- skok fazy na węźle / punkcie kardynalnym.

Nie wolno utożsamiać ich symbolicznie jako jednego (	au). Dla zamkniętej wstęgi relacja typu Călugăreanu–White–Fuller (Lk=Tw+Wr) może być rozważana wyłącznie po zdefiniowaniu właściwej wstęgi i jej krawędzi; nie jest automatycznie relacją dla dowolnych trzech helis.

### 5.2. Węzeł jako obszar, nie tylko punkt

Jeśli węzeł oznacza obszar sprzężenia trzech gałęzi, określić:
- rozmiar obszaru wzdłuż osi;
- wejścia i wyjścia każdej gałęzi;
- ciągłość pozycji i stycznej;
- dopuszczalne skoki fazy;
- lokalny bilans / regułę zachowania;
- minimalną odległość między gałęziami;
- warunki braku samoprzecięć, jeżeli wymagane.

## 6. Oś helisy i punkty kardynalne

Oś jest obiektem pierwotnym modelu, a nie pomocniczą linią dodaną po wygenerowaniu helisy.

Punkty kardynalne należy zdefiniować jako wyróżnione zdarzenia na osi lub w jej ramie lokalnej. Dla każdego punktu (C_j) zapisać:
- parametr osiowy (s_j) i czas (t_j), jeśli występuje;
- pozycję (A(s_j));
- lokalną ramę (styczna, normalna, binormalna lub inna baza TIMDR);
- fazę każdej gałęzi;
- wartości i znaki wszystkich odrębnych miar skrętu;
- rolę punktu: początek, koniec, przejście, ekstremum, przecięcie, synchronizacja lub granica redukcji;
- warunki brzegowe przed i za punktem.

Na tym etapie nie ustalamy liczby punktów kardynalnych ani ich nazw, bo nie zostały jeszcze odczytane z formalnej definicji / kodu TIMDR. Nie wolno arbitralnie przyjąć czterech punktów świata ani trzech punktów węzła bez źródła.

## 7. Warunki brzegowe — obowiązkowa macierz

| ID | Warunek | Co sprawdzać | Dlaczego ważne |
|---|---|---|---|
| BC-01 | zamknięta oś | (A(0)=A(L)) | geometria cykliczna |
| BC-02 | styczna na szwie | (T(0)=T(L)) | brak załamania osi |
| BC-03 | rama normalna | zgodność ramy / holonomia po obiegu | obrót bazy może generować pozorny skręt |
| BC-04 | faza gałęzi | (	heta_i(L)-	heta_i(0)=2\pi m_i) lub jawny skok | domknięcie helisy |
| BC-05 | trzy gałęzie | zgodność indeksów i permutacji (i\mapsto\sigma(i)) na szwie | gałęzie mogą zamieniać etykiety |
| BC-06 | punkt kardynalny | warunki jednostronne (s_j^-\), (s_j^+\) | skok / zmiana reguły |
| BC-07 | węzeł | ciągłość pozycji, stycznych i relacji faz | prawidłowe sprzężenie |
| BC-08 | redukcja | zgodność obrazu i jądra mapy redukcji na granicy | brak sztucznego utraty / duplikacji |
| BC-09 | sygnał | ciągłość lub jawny model skoku na okresie | artefakty na szwie |
| BC-10 | otwarta trajektoria | jawne dane wejściowe/wyjściowe zamiast periodyczności | warunki końcowe nie mogą być domyślne |

Dla trajektorii odcinkowej (trzy krawędzie trójkąta) należy sprawdzić, czy naroża są rzeczywistymi niegładkościami, czy przejścia są wygładzane, czy też naroża są punktami kardynalnymi. Nie wolno stosować wzorów Freneta w punktach, w których wymagane pochodne nie istnieją.

## 8. Pochodzenie sygnału z trajektorii trójkąta

Trzeba jawnie zdefiniować operator obserwacji (S=\mathcal{O}[q]), który przekształca trajektorię (q) w sygnał.

Możliwe kanały do rozważenia (nie są jeszcze zatwierdzone):
- pozycja / odległość od osi;
- prędkość i tempo przejścia między stanami;
- faza obiegu;
- orientacja lokalnej ramy;
- krzywizna / torsja na gładkich odcinkach;
- zdarzenia w punktach kardynalnych;
- relacje fazowe trzech gałęzi.

Dla każdego kanału sprawdzić, czy redukcja zachowuje:
1. amplitudę;
2. fazę;
3. kolejność zdarzeń;
4. orientację;
5. okres / częstotliwość;
6. informację o przejściu przez węzeł;
7. możliwość rekonstrukcji trajektorii.

Nie zakładać, że jeden skalar (	au) wystarcza do odtworzenia całego sygnału. Jeśli obserwacja jest wieloznaczna, należy zachować wektor kanałów lub jawnie opisać utratę informacji.

## 9. Testy falsyfikujące / eksperymenty P0

1. **Test bazowy trójkąta:** wygenerować cykl trzech stanów; sprawdzić zamknięcie pozycji, stycznej i fazy.
2. **Test orientacji:** odwrócić kierunek obiegu; zapisać, które wielkości zmieniają znak, a które pozostają.
3. **Test naroży:** porównać trajektorię z ostrymi narożami, wygładzoną i z osobnym modelem skoku.
4. **Test osi:** zrekonstruować oś z trzech gałęzi i porównać z osią zadaną.
5. **Test punktów kardynalnych:** przesuwać ich położenie / fazę i sprawdzić stabilność sygnału.
6. **Test BC:** naruszać każdy warunek brzegowy osobno; mierzyć artefakty na szwie i w węźle.
7. **Test R-43:** utworzyć jawny model czterowęzłowy, zastosować każdą z redukcji R-43a–d i porównać niezmienniki.
8. **Test rekonstrukcji:** zredukowana reprezentacja ma odtworzyć trajektorię źródłową w zakresie informacji, który deklaruje jako zachowany.
9. **Test null:** losowa trajektoria trzech stanów bez struktury helikalnej nie powinna automatycznie wykazywać tych samych własności.
10. **Test szumu:** powtórzyć przy różnych N, jitterze czasu, szumie i dropoutach.

Każdy test wymaga prerejestracji parametrów, seedów, tolerancji i kryterium porażki.

## 10. Ograniczenia i ostrzeżenia interpretacyjne

- Równanie (a=\sqrt{3}r) jest faktem geometrii trójkąta równobocznego wpisanego w okrąg; nie dowodzi samo w sobie generowania sygnału ani helisy.
- TRM w archiwum oznacza się jako model koncepcyjny. Prawa (R=k\tau^n) i fale (	au(x,t)) są hipotezami modelowymi, dopóki nie zostaną operacyjnie zdefiniowane i zweryfikowane.
- Zachowanie pola, skali lub długości nie implikuje zachowania topologii, informacji ani odwracalności.
- Torsja Freneta-Serreta nie jest automatycznie skrętem pasma, skrętem topologicznym ani fazą modalną.
- Redukcja liczby zmiennych nie musi oznaczać redukcji liczby węzłów geometrycznych.
- Zmiana klasy topologicznej wymaga jawnego wskazania operacji, która dopuszcza osobliwość, przecięcie, rozcięcie lub sklejenie.

## 11. Rejestr hipotez

| ID | Hipoteza | Status | Wymagany dowód |
|---|---|---|---|
| H-TRI-01 | sygnał TIMDR może być wyprowadzony z trajektorii trójkąta | HYPOTHESIS | definicja operatora obserwacji i walidacja |
| H-RED-43 | redukcja struktury czterowęzłowej może prowadzić do trójwęzłowej | HYPOTHESIS | jawna mapa i analiza niezmienników |
| H-HEL-3 | zredukowana trajektoria generuje węzeł trójhelikalny | HYPOTHESIS | konstrukcja osi i trzech gałęzi |
| H-AXIS-01 | oś jest pierwotnym elementem struktury helikalnej TIMDR | HYPOTHESIS autora / do formalizacji | definicja osi i relacji gałęzi |
| H-CARD-01 | punkty kardynalne organizują przejścia, fazę lub redukcję | HYPOTHESIS | definicja punktów i testy perturbacyjne |
| H-BC-01 | warunki brzegowe określają dopuszczalne skręty i domknięcie węzła | HYPOTHESIS | macierz warunków i testy |
| H-TWIST-01 | węzeł trójhelikalny ma kilka nieredukowalnych miar skrętu | PLAUSIBLE / do formalizacji | definicje i pomiary niezależnych wielkości |

## 12. Następny krok

Przed implementacją nowej helisy należy odzyskać z istniejących źródeł TIMDR dokładną definicję:
- trajektorii trójkąta, która generuje sygnał;
- operatora redukcji;
- czterowęzła i trójwęzła, o których mówi autor;
- osi i punktów kardynalnych;
- warunków przejścia oraz znaczenia skrętów w węźle.

Jeżeli źródłowa definicja znajduje się tylko w notatkach / archiwalnych plikach, należy przenieść ją do GIA-TIMDR z linkiem do oryginału i nie zmieniać jej po cichu. Brak definicji należy zapisać jako lukę, nie uzupełniać domysłem.

## 13. Dziennik zmian

- **2026-11-09 / v0.1:** zapisano hipotezę genezy sygnału z trajektorii trójkąta; uwzględniono redukcję czterowęzła do trójwęzła jako otwarty problem; wydzielono oś, punkty kardynalne, trzy gałęzie, rodzaje skrętu i warunki brzegowe; zidentyfikowano archiwalne źródła TRM i ograniczenia ich statusu.
