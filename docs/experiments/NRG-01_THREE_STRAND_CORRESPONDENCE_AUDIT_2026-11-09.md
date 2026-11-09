# NRG-01 / audyt odpowiedniości trzech komponentów do trzech gałęzi helisy

**Data:** 2026-11-09  
**Status:** audyt wykonany na artefakcie NRG-01 z GitHub Actions  
**Wejście:** `nrg01-parallel-tracks-capped.zip`, artifact ID `13650530264`  
**Kod audytu:** `experiments/nuclear_reduction/NRG-01/src/audit_three_strand_correspondence.py`  
**Zakres:** porównanie struktury grafu nuklidów z istniejącą geometrią trefoil / postulatem trzech gałęzi. Nie zakładamy z góry mapowania.

## 1. Wynik w skrócie

**Nie da się obecnie wyznaczyć jednoznacznego mapowania trzech komponentów nuklidowych na trzy gałęzie helisy.** Trzy komponenty grafu są rzeczywiste w pobranym zbiorze, ale ich liczba wynika z trzech niezależnych jąder startowych i rozłącznych rodzin rozpadu. Dane nuklidowe nie zawierają współrzędnych 3D, fazy helisy, podpisanej torsji geometrycznej ani etykiet punktów kardynalnych.

Można utworzyć sześć bijekcji (3!) pomiędzy komponentami a trzema nazwanymi gałęziami. Wszystkie są równoważne względem dostępnych danych — brak kryterium, które wyróżniałoby jedną z nich. To nie jest jeszcze odkryta korespondencja.

## 2. Rzeczywista struktura komponentów

| Komponent / źródło | Węzły | Krawędzie | Rozgałęzienia | Ścieżki od źródła do końca | Najdłuższa ścieżka |
|---|---:|---:|---:|---:|---:|
| Np-237 | 16 | 18 | 3 | 4 | 12 krawędzi |
| U-238 | 20 | 24 | 5 | 15 | 14 krawędzi |
| Th-232 | 12 | 12 | 1 | 2 | 10 krawędzi |

Wszystkie trzy składowe są skierowanymi acyklicznymi grafami w rozpoznanym podzbiorze danych (DAG). Każda ma jeden korzeń odpowiadający wybranemu nuklidowi startowemu i jeden terminalny węzeł w tym częściowym grafie:
- Np-237 → Tl-205;
- U-238 → Pb-206;
- Th-232 → Pb-208.

Terminalny węzeł oznacza tu brak rozpoznanej krawędzi wychodzącej w pobranym podzbiorze, a nie automatycznie potwierdzoną stabilność.

### 2.1. Rozgałęzienia według komponentu

- Np-237: Fr-221, At-217, Bi-213.
- U-238: Po-218, At-218, Bi-214, Pb-210, Bi-210.
- Th-232: Bi-212.

Arność wszystkich rozpoznanych rozgałęzień wynosi 2. Żaden komponent nie zawiera rozpoznanego rozgałęzienia trójkanałowego. W każdym komponencie pozostają też kanały nierozstrzygnięte: odpowiednio 4, 6 i 2. Wniosek o braku rozgałęzień trójkanałowych dotyczy więc wyłącznie krawędzi rozpoznanych.

## 3. Test odpowiedniości do trzech gałęzi

### 3.1. Test liczby komponentów

Liczba komponentów wynosi 3, ale eksperyment rozpoczął się od dokładnie trzech wybranych jąder: U-238, Th-232 i Np-237. Otrzymanie trzech komponentów jest zatem zgodne z konstrukcją wejścia. Nie stanowi niezależnego dowodu na trzy fundamentalne gałęzie geometrii.

### 3.2. Test zachowania struktury

Profile komponentów nie są równoważne:
- liczby węzłów: 16 / 20 / 12;
- liczby rozgałęzień: 3 / 5 / 1;
- liczby ścieżek: 4 / 15 / 2;
- długości najdłuższych ścieżek: 12 / 14 / 10.

Nie ma podstaw, aby uznać te komponenty za trzy symetryczne kopie jednej gałęzi. Możliwe jest mapowanie trzech różnych grafów do trzech różnych obiektów geometrycznych, ale wymaga ono jawnego operatora i kryterium zachowania obserwabli. Takiego operatora jeszcze nie zdefiniowano.

### 3.3. Test sześciu przypisań

Dla trzech komponentów i trzech nazwanych gałęzi istnieje (3!=6) przypisań. Ponieważ graf nie zawiera danych geometrycznych ani fazowych, wszystkie sześć przypisań ma identyczny status. Mapowanie jest **nieidentyfikowalne** z obecnych danych.

## 4. Porównanie z geometrią istniejącą w GIA-TIMDR

Repozytorium zawiera klasyczną krzywą trefoil w `core/trefoil_frenet_torsion.py` i opis w `docs/geometry/TIMDR_Trefoil_FrenetTorsion.md`.

To jeden zamknięty obiekt krzywej 3D z trzema lobami (wyróżnionymi obszarami parametru), a nie trzy niezależne, zmierzone helikalne krzywe. Trzy loby trefoila nie są tym samym co trzy składowe grafu nuklidów. Samo przypisanie komponentu do loba byłoby arbitralne, dopóki nie zdefiniujemy relacji zachowującej kolejność, orientację, fazę i strukturę przejść.

Repozytorium ma również konstrukcję `Φ_G` z grafu zdarzeń do krzywej (`docs/theory/TIMDR_Geometry_From_EventGraph.md`). Wymaga ona pozycji (p_i\in\mathbb R^3), czasów (t_i) i jawnej ścieżki / porządku zdarzeń. Graf nuklidów NRG-01 zawiera (Z,N), kanały rozpadu i wybrane dane jądrowe, ale nie zawiera współrzędnych przestrzennych, które pozwoliłyby zastosować `Φ_G` bez sztucznego konstruowania embeddingu.

## 5. Test osi, punktów kardynalnych i ręczności

| Właściwość | Graf nuklidów | Geometria helisy | Można porównać teraz? |
|---|---|---|---|
| Kolejność | DAG / relacje przejść | parametr krzywej | Częściowo, po zdefiniowaniu mapy |
| Rozgałęzienia | Tak, arność 2 | Wymagają jawnych węzłów/junctions | Tylko abstrakcyjnie |
| Oś geometryczna | Brak | Tak, po definicji | Nie |
| Punkty kardynalne | Brak etykiet | Definicja nadal otwarta | Nie |
| Podpisana torsja | Brak | Możliwa do obliczenia | Nie |
| Faza helisy | Brak | Możliwa do zdefiniowania | Nie |
| Lewo-/prawoskrętność | Brak orientowanego osadzenia | Zachowana przez znak torsji/skoku | Nie |

W konsekwencji graf nuklidów nie może obecnie potwierdzić, czy redukcja zachowuje lewo- lub prawoskrętność. To nie jest wynik negatywny dla samej geometrii helisy; to brak wymaganej informacji po stronie nuklidowej.

## 6. Rozstrzygnięcie

1. **Trzy komponenty:** potwierdzone w danych, ale warunkowe względem trzech wybranych jąder startowych.
2. **Trzy równoważne gałęzie:** niepotwierdzone; profile komponentów istotnie się różnią.
3. **Jednoznaczne mapowanie komponent → gałąź:** nieidentyfikowalne; wszystkie 6 przypisań pozostaje równoważnych.
4. **Punkty kardynalne:** nie można ich wyprowadzić z samych rozgałęzień jądrowych bez jawnego operatora mapującego.
5. **Zachowanie ręczności:** nie można przetestować między domenami, ponieważ graf nuklidów nie ma geometrycznej orientacji.
6. **Redukcja 4→3:** nie została wykazana.

To jest konkretna odpowiedź na pytanie o korespondencję: **obecne dane nie uzasadniają utożsamienia trzech łańcuchów z trzema gałęziami helisy**. Nie należy dopasowywać ich po fakcie.

## 7. Co jest potrzebne do rozstrzygającego testu

Należy wykonać dwa niezależne kroki:

A. Dla geometrii TIMDR dostarczyć trzy jawne krzywe (H_i(s)), wspólną oś (A(s)), parametryzację, fazy, podpisane torsje/skoki, punkty kardynalne i warunki brzegowe. Jeżeli istnieje tylko jedna krzywa trefoil, nie nazywać jej trzema niezależnymi helisami.

B. Dla grafu nuklidów zdefiniować z góry operator mapowania zdarzeń na cechy krzywych. Nie wolno wymyślać współrzędnych 3D nuklidów po obejrzeniu wyników. Najpierw trzeba wskazać, które wielkości fizyczne miałyby generować pozycję, fazę i orientację, a następnie sprawdzić, czy mapa zachowuje DAG, rozgałęzienia i obserwable.

Dopiero wtedy można testować:
- zgodność osi i kolejności punktów kardynalnych;
- zachowanie znaku torsji i skoku;
- stabilność mapowania przy perturbacji danych;
- czy redukcja zachowuje rozgałęzienia i liczbę ścieżek;
- czy istnieje niearbitralna, falsyfikowalna relacja 3-komponenty ↔ 3-gałęzie.

**Wniosek końcowy:** audyt nie wykazał odpowiedniości 3→3. Wykazał dokładnie, dlaczego obecny zbiór danych jej nie identyfikuje i jakie dane oraz definicje są konieczne, aby ją uczciwie sprawdzić.
