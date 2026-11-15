# TIMDR / Chronoproces — 51B.13: ontologia i minimalna sygnatura geometrii

Data: 2026-11-15
Status: notatka badawcza. Twierdzenia dla jawnie określonych rodzin oddzielono od hipotez o całej teorii TIMDR.
Kontynuacja: 51B.10–51B.12 (geometria operacyjna, archiwalna, identyfikowalność).

## 1. Zmiana pytania badawczego

Wielkości ~H, ~Phi, eta, kappa i kappa_iso zależą od wybranego języka relacji i od definicji zachowywanej struktury. Zanim przypiszemy im interpretację ontologiczną, należy ustalić, co oznacza „ta sama geometria Chronoprocesu”.

Rozróżniamy:
- równoważność prognostyczną: jednakowe prawa wszystkich przyszłych obserwacji;
- równoważność archiwalną oznaczoną: identyczne odpowiedzi na wszystkie wymagane pytania o wystąpienia;
- izomorfizm geometryczny: zgodność struktury przy dopuszczalnej zmianie identyfikatorów.

Te relacje nie muszą być identyczne.

## 2. Twierdzenie 51B.13a — chronologia istotna informacyjnie

Rodzina C_n: n rozłącznych kontenerów w sekwencji Open_i -> X_i -> Close_i, gdzie X_i ma typ A lub B. Ciąg typów b należy do {0,1}^n.

Sygnatura R_A: zawieranie + predykaty typu A/B, bez porządku między kontenerami.
Sygnatura R_B: R_A + ścisły porządek liniowy kontenerów odpowiadający chronologii.
Sygnatura R_C: R_B + indywidualne identyfikatory kontenerów.

Izomorfizmy zachowują wszystkie predykaty danej sygnatury. Dla R_A mogą permutować kontenery; dla R_B muszą zachować ich kolejność.

Wynik:
|C_n / ≅_{R_A}| = n+1,
|C_n / ≅_{R_B}| = 2^n,
|C_n / ≅_{R_C}| = 2^n.

Dowód: w R_A izomorfizm zależy tylko od liczby kontenerów typu A, czyli jednej z n+1 wartości. W R_B skończony porządek liniowy ma jedyny automorfizm identycznościowy, więc każde położenie zachowuje typ A/B, a wszystkie 2^n ciągów są różne. Identyfikatory w R_C nie rozdzielają dalszych klas w tej konkretnej rodzinie.

Uwaga: „tylko zawieranie” bez zachowania typów A/B nie wystarcza do uzyskania n+1 klas; przy identycznych typach dzieci wszystkie takie struktury są izomorficzne. Ponadto chronologia nie zawsze podnosi liczbę klas: twierdzenie dotyczy zdefiniowanej rodziny i sygnatur.

Wniosek dowiedziony: dodanie chronologii zwiększa moc rozróżniającą w tej rodzinie z n+1 do 2^n klas izomorfizmu.
Nie wynika z tego jeszcze, że chronologia jest relacją pierwotną TIMDR.

## 3. Definicja rdzenia sygnatury

Niech R_full będzie ustaloną pełną sygnaturą relacji/atrybutów na klasie dopuszczalnych Chronoprocesów C. Podsygnatura R_core ⊆ R_full jest wystarczająca izomorficznie, gdy dla każdych C1,C2 z C:

C1 ≅_{R_core} C2  iff  C1 ≅_{R_full} C2.

Jest minimalna inkluzyjnie, gdy żaden jej właściwy podzbiór nie zachowuje tej własności.

Uwaga logiczna: minimalny inkluzyjnie rdzeń nie musi być jedyny i nie musi mieć minimalnej możliwej liczby symboli. Należy odróżnić minimalność inkluzyjną od minimalnej liczności.

## 4. Test niezbędności relacji (51B.13b)

Dla R ∈ R_core poszukujemy świadków C1,C2:
C1 ≅_{R_core \ {R}} C2,
ale
C1 nie ≅_{R_core} C2.

Istnienie takich świadków dowodzi, że R jest niezbędna w danym rdzeniu względem klasy C. Dla skończonej sygnatury i rdzenia wystarczającego takie świadectwa dla każdego symbolu są warunkiem minimalności inkluzyjnej.

Trzeba odróżnić:
(a) „R niezbędna w tym wybranym rdzeniu”,
(b) „R należy do każdego możliwego rdzenia”,
(c) „R jest pierwotna ontologicznie”.
(a) nie implikuje automatycznie (b) ani (c).

## 5. Kandydat na relacje pierwotne

R_candidate = {Next(a,b), Contains(a,b), Attr(a)=(MIN(a),MAX(a),Delta t(a))}.

- Next: bezpośrednie następstwo (należy określić, czy oznacza następstwo chronologiczne w jednym śladzie, czy dopuszczalną krawędź grafu przejść).
- Contains: relacja strukturalna/hierarchiczna, wraz z ustaleniem, czy jest bezpośrednia czy przechodnia.
- Attr: wartości MIN, MAX, Delta t, z ograniczeniami MIN ≤ MAX i Delta t > 0; nie zakładamy Delta t = MAX−MIN bez dodatkowego aksjomatu.

Pełna chronologia może być relacją pochodną od Next, ale nie musi.

## 6. Kluczowy test: czy Chronology jest definiowalna z Next?

Przypadek pozytywny (twierdzenie warunkowe):
Jeżeli każdy dopuszczalny Chronoproces jest skończonym liniowym śladem, a Next oznacza bezpośrednie następstwo jego wystąpień, to porządek ścisły Before(a,b) jest wyznaczony przez dodatnie domknięcie przechodnie Next:
Before(a,b) iff istnieje k≥1 i ścieżka Next długości k od a do b.
Wówczas zachowanie Next automatycznie zachowuje Before; osobny symbol Before jest redundantny dla izomorfizmu tej klasy.

Uwaga formalna: domknięcie przechodnie jest konstrukcją grafową / definicją w logice z domknięciem przechodnim; w ogólności nie musi być definiowalne pojedynczą formułą pierwszego rzędu na dowolnych skończonych strukturach. „Odtwarzalne” nie jest synonimem „definiowalne w FO”.

Przypadek negatywny (kontrprzykład do nieograniczonej tezy):
Niech Next oznacza graf dopuszczalnych przejść, nie rzeczywiste następstwo wystąpień. Dwa Chronoprocesy mogą mieć identyczny graf Next, Contains i Attr, lecz różną chronologię realizacji. Na przykład graf z niezależnymi zdarzeniami x,y nie narzuca, czy x nastąpiło przed y, czy y przed x. Zatem Before nie musi być odtwarzalne z Next w takiej semantyce.

Także w modelu współbieżności trzeba ustalić, czy chronologia to całkowity porządek realizacji, częściowy porządek przyczynowy czy relacja czasowa oparta na atrybutach.

## 7. Program badań 51B.13c

1. Zamrozić klasę modeli C i interpretację Next, Contains, Attr.
2. Ustalić pełną sygnaturę R_full, w tym typy zdarzeń, relacje czasowe i zasady izomorfizmu.
3. Dla każdej relacji sprawdzić odtwarzalność z pozostałych (nie tylko intuicyjną zależność).
4. Budować pary świadków niezbędności dla kandydatów do rdzenia.
5. Oddzielić redundancję semantyczną, izomorficzną i definiowalność w wybranym języku logicznym.
6. Dopiero potem ustalić eta_{R_core}, kappa_{n,R_core} i kappa_{n,R_core}^{iso}.

## 8. Status

DOWIEDZIONE W RODZINIE SYNTETYCZNEJ: |G_RA/≅|=n+1 i |G_RB/≅|=2^n.
DOWIEDZIONE WARUNKOWO: dla skończonych śladów liniowych chronologia jest odzyskiwalna z Next jako bezpośredniego następstwa.
OTWARTE: czy Next, Contains i Attr tworzą wystarczającą, minimalną sygnaturę geometrii TIMDR w wybranej pełnej klasie Chronoprocesów; czy chronologia jest pierwotna czy pochodna przy docelowej semantyce.
