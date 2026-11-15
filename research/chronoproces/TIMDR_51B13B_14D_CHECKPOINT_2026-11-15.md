# TIMDR 51B.13b–51B.14d — punkt kontrolny (2026-11-15)

## Status
Notatka badawcza. Oddziela twierdzenia w klasach modeli od hipotez ontologicznych TIMDR. Kontynuacja po 51B.13a.

## 51B.13b — potencjalność, realizacja, chronologia
- `Next_poss`: dopuszczalność przejścia; `Next_act`: bezpośrednie następstwo rzeczywistych wystąpień; `Prec`: ścisła chronologia wystąpień.
- **Twierdzenie:** w skończonej liniowej realizacji, jeśli `Next_act` jest relacją sąsiedztwa w porządku, `Prec = Next_act^+`. Dowód: każdy porządek dwóch różnych wystąpień jest realizowany ścieżką sąsiedztwa i odwrotnie.
- **Kontrprzykład:** identyczny graf możliwości A→B i A→C może współistnieć z realizacjami A≺B≺C i A≺C≺B, jeśli model dopuszcza obie kolejności. Sam `Next_poss` nie wyznacza `Prec`.
- Nie utożsamiać przejścia możliwego z następnikiem konkretnego wystąpienia. W modelach współbieżnych trzeba osobno zdefiniować chronologię.

## 51B.13c — minimalność w klasie abstrakcyjnej
Klasa C_fin: skończony zbiór wystąpień E; N=Next_act jest ścieżką Hamiltona; C=Contains jest ścisłą przechodnią relacją bez cykli; a:E→A ma dopuszczalne trójki MIN≤MAX, Δt>0; brak dodatkowych sprzężeń.
- Niezależność C: ten sam N,a, ale C=∅ lub C={(u,v)}.
- Niezależność a: ten sam N,C, ale różne wartości a w wyróżnionym początku ścieżki.
- Niezależność N: różne kolejności wystąpień o rozróżniających atrybutach, to samo C,a. Sama zmiana kolejności przy identycznych atrybutach NIE jest wystarczającym świadkiem nieizomorfizmu.
**Wniosek:** {Next_act,Contains,Attr} jest minimalne inkluzyjnie względem tej samej pełnej sygnatury w C_fin. Nie udowodniono minimalności dla całego TIMDR ani wystarczalności dla rozszerzonej sygnatury.

## 51B.14 — semantyka trójki
**Zasada:** semantyka (MIN,MAX,Δt) nie wynika z zapisu. Lokalna charakterystyka zdarzenia nie jest relacją między zdarzeniami.
Roboczo: a:E→V×V×T_{>0}, MIN(e)≤_V MAX(e), V uporządkowana przestrzeń wartości, T_{>0} dodatnia rozciągłość czasowa; V i T nie muszą być tym samym typem. Nie przyjmować Δt=MAX−MIN bez uzasadnienia wymiarowego.
- S1: tylko typy i nierówność.
- S2: aksjomaty zgodności Γ(a,N,C,P) ograniczają geometrię.
- S3: co najmniej jedna relacja jest wyznaczona przez atrybuty.
S3 może być szczególnym przypadkiem S2. Wariant hybrydowy S2 jest hipotezą roboczą, nie przyjętą ontologią TIMDR.

## Przestrzeń dopuszczalnych geometrii
Dla ustalonego E,a:
A_E(a)={(N,C,P): Γ(E,a,N,C,P)}; zakładać A_E(a)≠∅.
A_R(a)={R^G:G∈A_E(a)}.
- |A_R(a)|=1 oznacza wyznaczalność R na ustalonym oznaczonym E.
- |A_R(a)|>1 oznacza niewyznaczalność R przez samo a na oznaczonym E.
- |A_E(a)|>1 samo nie dowodzi niewyznaczalności konkretnej relacji.
- Dla minimalności rdzenia należy porównywać struktury z identycznymi pozostałymi relacjami i wykazać nieizomorfizm pełnych rozwinięć. Różność oznaczonych relacji nie zawsze oznacza nieizomorfizm.

## 51B.14d — kandydat H1
Interpretacja warunkowa: MIN,MAX wyznaczają przedział WARTOŚCI I_V(e)=[MIN(e),MAX(e)]_V, niekoniecznie czas.
K_C(a(x),a(y)) ⇔ MIN(x)≤MIN(y) ∧ MAX(y)≤MAX(x).
(H1) Contains(x,y) ⇒ K_C(a(x),a(y)).
Dla K_a={(x,y):x≠y i K_C(a(x),a(y))}, H1 daje C⊆K_a.
Przy dodatkowym wymaganiu ścisłego porządku częściowego, bez innych ograniczeń, dopuszczalne C to ścisłe porządki częściowe zawarte w K_a.
Przykład I(x)=[0,10], I(y)=[2,5], I(z)=[3,4]: dopuszczalne zarówno C1={(x,y),(y,z),(x,z)}, jak i C2={(x,y),(x,z)}; obie struktury mają te same atrybuty, różnią się hierarchią i liczbą par. H1 ogranicza, ale nie wyznacza C.
**Zastrzeżenie:** H1 nie wynika z samej interpretacji MIN/MAX jako ekstremów. Wymaga dodatkowej semantyki, że zakres kontenera obejmuje zakresy zawieranych zdarzeń.

## Δt i następny etap 51B.14e
H1 nie wykorzystuje Δt. Nie przyjmować Δt(y)≤Δt(x) dla Contains bez założenia zawierania czasowego. Można badać N(x,y)⇒K_N(a(x),a(y)), ale K_N musi mieć uzasadnienie semantyczne.
**Kluczowe:** sama długość trwania Δt nie określa położenia zdarzenia w czasie ani kolejności. Aby z niej wnioskować o następstwie, potrzebna jest informacja o umiejscowieniu lub dodatkowe aksjomaty.
Otwarte: ontologiczne znaczenie V, T, Δt; uzasadnienie H1; wybór K_N; minimalność rdzenia po aksjomatach TIMDR.

## Zasada metodologiczna
Atrybuty mogą określać przestrzeń geometrii dopuszczalnych, niekoniecznie geometrię rzeczywistą. Ograniczanie ≠ wyznaczanie. Nie mylić definicji roboczej, twierdzenia warunkowego i hipotezy ontologicznej.
