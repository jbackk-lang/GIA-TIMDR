# TIMDR — helisa i fraktal jako główne reprezentacje struktury nadrzędnej (v0.1)

**Data:** 2026-11-09
**Status:** formalizacja kierunku wskazanego przez autora, zgodna z wcześniejszym rozdzieleniem gałęzi TIMDR. Nie jest nowym aksjomatem ani dowodem fizycznym.

## 1. Korekta hierarchii

Autor przypomina, że podczas wcześniejszych formalizmów doszliśmy do wniosku, iż helisa jest jednym z rzutów/reprezentacji struktury TIMDR, a znacząca część pozostałej reprezentacji ma charakter fraktalny.

Nie wolno zatem traktować helisy jako całej struktury źródłowej ani fraktala jako ozdobnego dodatku do helisy. Oba są kandydatami na odrębne, powiązane reprezentacje tego samego procesu/obiektu nadrzędnego. Tożsamość źródłowa i mapa przejścia między reprezentacjami wymagają jawnego określenia.

Robocza hierarchia:

1. **Struktura nadrzędna TIMDR** — stan, relacje, reguły przejścia, historia i warunki brzegowe.
2. **Rodzina reprezentacji/rzutów** — co najmniej reprezentacja helikalna i fraktalna; inne reprezentacje pozostają otwarte.
3. **Operatory przejścia** — projekcja, lift 2D→3D, obrót/transport ramy, redukcja, zmiana skali, sklejenie i transformacja fazowa.
4. **Obserwable** — geometria, faza, chiralność, wymiar/skalowanie, widmo, topologia, odpowiedź na sygnał.

## 2. Minimalny zapis matematyczny

Niech \(\mathcal X\) oznacza przestrzeń stanów struktury nadrzędnej. Niech \(\Pi_H\) i \(\Pi_F\) oznaczają mapy reprezentacji helikalnej i fraktalnej:

\[ H=\Pi_H(X), \qquad F=\Pi_F(X), \qquad X\in\mathcal X. \]

Nie zakładamy, że mapy są odwracalne ani że reprezentacje są równoważne. Pytamy, które informacje każda zachowuje, a które gubi. Jeśli istnieje operator przejścia między reprezentacjami, zapisujemy go jako:

\[ H\xrightarrow{\;T_{H\to F}\;}F, \qquad F\xrightarrow{\;T_{F\to H}\;}H. \]

Nie należy z góry zakładać, że \(T_{F\to H}\) jest odwrotnością \(T_{H\to F}\). Redukcja może być nieodwracalna albo wymagać dodatkowej historii/stanu.

## 3. Co może znaczyć reprezentacja fraktalna

Termin „fraktalna” trzeba rozbić na mierzalne własności, zamiast używać go jako synonimu złożoności:

- samopodobieństwo dokładne lub statystyczne;
- prawo skalowania w określonym przedziale skal;
- wymiar fraktalny (np. Hausdorffa, pudełkowy lub korelacyjny — nie są automatycznie równoważne);
- rekurencyjna/regułowa konstrukcja;
- niezmienniczość lub kowariancja względem zmiany skali;
- rozkład defektów, osobliwości i granic między skalami.

Nie przypisywać jednej wartości wymiaru fraktalnego bez określenia obiektu, metody estymacji, zakresu skal i błędu. Wymiar zależny od skali może być bardziej informacyjny niż pojedynczy wykładnik.

## 4. Relacja helisa–fraktal: hipotezy rozłączne

**H1 — wspólne źródło:** helikalna i fraktalna reprezentacja są dwoma rzutami tego samego stanu nadrzędnego.

**H2 — helisa jako lokalny/wybrany przekrój:** helisa jest reprezentacją lokalną lub projekcją ograniczoną do wybranego kierunku/osi, podczas gdy fraktal opisuje organizację wieloskalową.

**H3 — sprzężenie rekurencyjne:** reguła generująca strukturę helikalną powtarza się na kolejnych skalach, a helisa jest jednym z poziomów samopodobnej hierarchii.

**H4 — reprezentacje komplementarne:** helisa koduje orientację, fazę i transport; fraktal koduje rozkład, rekurencję i skalowanie. Dopiero wspólny stan pozwala odtworzyć strukturę nadrzędną.

Te hipotezy mogą być częściowo zgodne, ale należy je testować osobno. Sam fakt występowania helis i fraktali w przyrodzie nie rozstrzyga żadnej z nich.

## 5. Kandydat na wspólny stan i niezmienniki

Rozszerzamy stan roboczy z programu anomaly-first:

\[ X=(G,C,F_r,\phi,b,h,\sigma), \]

gdzie \(G\) — graf/geometria, \(C\) — relacje środków, \(F_r\) — rama orientacji (nie mylić z reprezentacją fraktalną), \(\phi\) — faza i winding, \(b\) — warunki brzegowe, \(h\) — historia, a \(\sigma\) — skala lub poziom hierarchii.

Przy przejściu między reprezentacjami należy sprawdzać zachowanie, transformację lub utratę:

- ciągłości i sąsiedztwa;
- orientacji/chiralności i znaku skrętu;
- fazy oraz historii fazowej;
- relacji osi i punktów kardynalnych;
- warunków brzegowych i topologii;
- praw skalowania oraz relacji między poziomami;
- informacji o anomaliach, defektach i osobliwościach.

Nie wszystkie wielkości muszą być niezmiennikami. Celem jest ustalenie ich praw transformacji.

## 6. Program testów — mały, rozstrzygający, bez budowania kolejnej teorii na wyrost

### T1 — identyfikacja wcześniejszego formalizmu fraktalnego
Zlokalizować istniejące repozytorium/plik, z którego pochodzi wcześniejszy wniosek o fraktalnej reprezentacji. Przenieść do GIA-TIMDR wyłącznie odnośnik, definicje i status dowodowy; nie przepisywać niezależnego formalizmu bez potrzeby.

### T2 — charakterystyka fraktalna
Na jednym jawnie zdefiniowanym obiekcie wyznaczyć wymiar metodą box-counting w zamrożonym zakresie skal, sprawdzić stabilność nachylenia, zakres liniowości, efekt rozdzielczości i porównać z kontrolą niefraktalną o podobnej geometrii.

### T3 — charakterystyka helikalna
Na tej samej konstrukcji mierzyć oś, promień, skok, fazę, podpisany skręt/torsję, holonomię i warunki brzegowe. Nie redukować orientacji do modułu.

### T4 — test wspólnego źródła
Sprawdzić, czy parametry struktury nadrzędnej pozwalają przewidzieć jednocześnie miary helikalne i fraktalne na danych niewykorzystanych do dopasowania. Porównać z dwoma niezależnymi modelami reprezentacji.

### T5 — test wieloskalowy
Zbadać, czy po zmianie skali reguła generująca helikalną reprezentację zachowuje postać, zmienia parametry według prawa skalowania, czy całkowicie się zmienia. Zmierzyć również, czy anomalie i punkty przejścia pojawiają się w odpowiadających sobie skalach.

### T6 — test informacji utraconej
Zrekonstruować wspólny stan z każdej reprezentacji osobno i z ich połączenia. Porównać, czy połączenie H+F odtwarza więcej informacji (w szczególności fazę, chiralność, historię i strukturę brzegową) niż każda reprezentacja oddzielnie.

## 7. Audyt aktualnego GIA-TIMDR

W drzewie głównego repozytorium widoczne są formalizmy geometrii powierzchni/Weingartena, kongruencji Chronoprocesu, obwiedni trójkąta, projekcji grafu zdarzeń oraz operator liftu fazorowego 2D→3D. Są one przydatne jako elementy geometrii i projekcji.

Nie odnaleziono w aktualnym drzewie `main` dedykowanego modułu ani formalnego dokumentu fraktalnej reprezentacji TIMDR. To nie dowodzi, że wcześniejszy formalizm nie istnieje — może znajdować się w innym repozytorium lub w niepodłączonej części ekosystemu. Nie należy zastępować go nową, wymyśloną definicją. Do pełnej integracji potrzebny jest wskazany wcześniejszy artefakt/repo.

## 8. Decyzja architektoniczna

Od tej chwili dokumentacja helisy powinna opisywać ją jako **reprezentację helikalną**, nie jako całość TIMDR. Badania fraktalne prowadzić jako równoległą reprezentację, po czym testować wspólne źródło i mapy przejścia. Nie podporządkowywać fraktala helisie ani helisy fraktalowi przed wynikiem testu.

**Wniosek:** właściwym przedmiotem poszukiwania jest struktura nadrzędna oraz rodzina jej reprezentacji. Helisa i fraktal są głównymi kandydatami na dwa komplementarne rzuty; ich wspólna reguła generująca pozostaje pytaniem badawczym.