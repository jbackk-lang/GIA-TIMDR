# Eksperyment NRG-01: graf redukcji nuklidów a geometria TIMDR

**Status:** protokół prerejestracyjny; eksperyment jeszcze niewykonany  
**Wersja:** 0.1 · 2026-11-09  
**Repozytorium nadrzędne:** GIA-TIMDR  
**Powiązane źródła:** `TIMDR-Concept-Archive/Topological-Reduction-Model-TRM/physics/element-stability.md`, `decay-series.md`, `math/reduction-equations.md`  
**Powiązane badania:** `HELIX_TIMDR_RESEARCH_PROGRAM.md`, `TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md`

## 0. Pytanie badawcze

Czy rzeczywiste szeregi przemian jądrowych można opisać jako skierowane grafy stanów, których redukcje (kontrakcje, ilorazy lub projekcje) mają mierzalne cechy porównywalne z postulowaną redukcją TIMDR 4→3?

Nie testujemy tezy, że rozpad jądrowy i geometria helisy są tym samym zjawiskiem. Testujemy, czy graf nuklidów dostarcza niezależnego, empirycznie zakotwiczonego modelu przejść, rozgałęzień, stanów końcowych i redukcji liczby stopni swobody.

## 1. Hipotezy i kryteria falsyfikacji

- **NRG-H1:** szeregi rozpadu dają się przedstawić jako skierowane grafy stanów nuklidów ((Z,N)). Status: fakt definicyjny modelowania; poprawność grafu zależy od danych wejściowych.
- **NRG-H2:** dla wybranych fragmentów grafu istnieją naturalne klasy równoważności, których iloraz upraszcza opis bez utraty wybranych obserwabli. Status: otwarta.
- **NRG-H3:** niektóre lokalne struktury rozgałęzień mogą mieć trzy kanały / trzy klasy skutków, ale nie ma założenia, że wszystkie czterostanowe konfiguracje redukują się do trzech. Status: otwarta.
- **NRG-H4:** miara `τ_nuc` z archiwum TRM wnosi predykcyjną wartość ponad proste cechy ((Z,N)), parzystość i odległość od doliny stabilności. Status: spekulatywna.

Falsification:
- H2/H3 odpadają dla badanego przypadku, jeśli żadna jawna, niearbitralna relacja równoważności nie zachowuje wskazanych obserwabli.
- H4 odpada, jeśli na danych odłożonych `τ_nuc` nie poprawia predykcji względem baseline'ów albo wymaga niestabilnego strojenia.
- Nie wolno wybierać tylko tych szeregów, które pasują do oczekiwanego wyniku 4→3.

## 2. Dane i pochodzenie

Źródłem danych muszą być ocenione dane nuklidowe, nie ręcznie przepisywana lista z materiału koncepcyjnego. Preferowane źródła:
- ENSDF / NNDC dla ocenionych poziomów i danych rozpadu;
- IAEA Live Chart of Nuclides jako dostępna prezentacja danych;
- AME dla mas atomowych i energii związanych z bilansem.

Każdy pobrany plik należy zachować w katalogu eksperymentu wraz z adresem źródła, datą pobrania, wersją/edycją, sumą SHA-256 i opisem licencji/warunków użycia. Jeżeli źródło nie dostarcza informacji o niepewności lub rozgałęzieniu, oznaczyć pole jako brakujące; nie uzupełniać domysłem.

Minimalne pola:
- nuklid: (Z,N,A), symbol;
- status stabilności;
- kanał rozpadu;
- produkt(y) rozpadu;
- prawdopodobieństwo rozgałęzienia / intensywność, jeśli dostępna;
- okres półtrwania i niepewność;
- energia Q i niepewność, jeśli dostępna;
- referencja oceny.

## 3. Definicja grafu

Graf skierowany (G=(V,E)):
- każdy wierzchołek (v\in V) to nuklid ((Z,N));
- krawędź (e=(v_i,v_j,c)) oznacza kanał rozpadu (c);
- krawędzie równoległe są dozwolone, jeśli dwa kanały prowadzą do tego samego produktu;
- krawędź ma atrybuty: kanał, branching ratio, Q, half-life rodzica, niepewności i źródło.

Podstawowe reguły bilansu do walidacji danych:
- (alpha: (Z,N)\to(Z-2,N-2));
- (eta^-: (Z,N)\to(Z+1,N-1));
- (eta^+ / EC: (Z,N)\to(Z-1,N+1));
- (gamma): zmiana stanu wzbudzenia, bez zmiany (Z,N); modelować jako przejście poziomów tego samego nuklidu tylko wtedy, gdy dane zawierają poziomy energetyczne.

Nie traktować wszystkich przejść jako tego samego typu. Fisja, emisja neutronu/protonu, wychwyt i kanały egzotyczne wymagają osobnych reguł.

## 4. Co mierzymy w grafie

Dla każdego szeregu / komponentu:
- liczba wierzchołków i krawędzi;
- stopnie wejściowe i wyjściowe;
- liczba rozgałęzień i ich arność;
- liczba stanów końcowych stabilnych;
- długości ścieżek do stanów końcowych;
- cykle (jeśli występują; nie zakładać DAG bez sprawdzenia danych);
- osiągalność i komponenty;
- rozkład kanałów;
- niepewność i kompletność danych.

Wielkości te są analogami strukturalnymi grafu, nie geometrycznym skrętem helisy.

## 5. Test redukcji i przypadek 4→3

Dla każdego kandydującego podgrafu o czterech wyróżnionych stanach lub rolach należy zdefiniować redukcję przed obliczeniem wyniku. Co najmniej trzy odrębne warianty:

1. **Quotient / identyfikacja stanów:** relacja równoważności (\sim) scala stany tylko wtedy, gdy spełniają jawne kryterium obserwacyjne (np. nierozróżnialność dla ustalonego zestawu obserwabli). Sprawdzić, czy relacja jest zwrotna, symetryczna i przechodnia.
2. **Kontrakcja grafu:** scalenie wybranych sąsiednich wierzchołków; jawnie raportować zmianę stopni, krawędzi, cykli i osiągalności.
3. **Projekcja obserwacyjna:** mapowanie pełnego grafu do mniejszego alfabetu stanów / klas; nie interpretować ukrytego stanu jako fizycznie usuniętego.

Dla każdej redukcji porównać przed i po:
- zachowanie osiągalności stanów końcowych;
- zachowanie rozkładu prawdopodobieństwa dojścia (jeśli dane na to pozwalają);
- zachowanie kanałów rozpadu lub jawnie wskazaną utratę kanału;
- zachowanie czasu przejścia / rozkładu czasu;
- zachowanie liczby niezależnych cykli i rozgałęzień;
- informację utraconą przez mapę.

**Ważne:** cztery wierzchołki grafu nie są automatycznie czterowęzłem topologicznym. Graf przejść nuklidów i węzeł osadzony w przestrzeni to różne obiekty matematyczne. Wynik 4→3 w grafie nie dowodzi redukcji topologicznej w helisie.

## 6. Test modelu `τ_nuc` z TRM

Wersja archiwalna:
[
\tau_{nuc}=\alpha|N-Z|+\beta Z
]

Przed dopasowaniem:
- sprawdzić jednostki i skalowanie;
- zdefiniować, czy `τ_nuc` jest cechą stanu czy krawędzi;
- ustalić osobne modele dla kanałów rozpadu;
- nie utożsamiać `τ_nuc` z torsją Freneta-Serreta.

Modele do porównania:
- B0: tylko (Z,N,A);
- B1: odległość od empirycznej doliny stabilności i parzystość;
- B2: prosta regresja / model klasyfikacyjny z cechami jądrowymi;
- T1: cechy B0 + `τ_nuc`;
- T2: cechy B1 + `τ_nuc`.

Podział danych ma być grupowany po łańcuchu / rodzinie, by uniknąć przecieku sąsiednich izotopów do treningu i testu. Raportować metryki na zbiorze odłożonym, przedziały niepewności i kalibrację. Nie stroić `α,β,k,n,m` na zbiorze testowym.

Samo dopasowanie korelacji nie jest dowodem mechanizmu fizycznego. `τ_nuc∝1/(B/A)` i `λ=λ_0τ^m` traktować jako osobne hipotezy do falsyfikacji.

## 7. Most do geometrii TIMDR — bez utożsamiania obiektów

Dopiero po walidacji grafu można porównywać jego abstrakcyjną strukturę z modelem trajektorii trójkąta:
- trzy wyróżnione klasy / kanały mogą być kandydatem do porównania z trzema gałęziami;
- oś grafu (uporządkowanie etapów / główna ścieżka) nie jest automatycznie osią geometryczną helisy;
- węzły rozgałęzień mogą być porównane z punktami kardynalnymi jako zdarzenia, nie jako identyczne obiekty;
- warunki brzegowe grafu (stany początkowe/końcowe) można porównać z warunkami zamknięcia/otwarcia trajektorii;
- miary skrętu geometrycznego muszą pozostać oddzielne od `τ_nuc`.

Mapowanie ma jawnie określać: dziedzinę, przeciwdziedzinę, zachowane obserwable, utracone informacje i kryterium falsyfikacji.

## 8. Minimalny plan wykonania

1. Pozyskać ocenione dane dla U-238, Th-232 i Np-237 wraz z rozgałęzieniami i niepewnościami.
2. Zbudować i zwalidować grafy; wykryć brakujące dane i niespójności bilansu.
3. Wybrać przypadki do testów na podstawie prerejestracji, nie oczekiwanego wyniku.
4. Zmierzyć metryki grafowe i zidentyfikować kandydatów na redukcje 4→3.
5. Wykonać redukcje quotient, kontrakcję i projekcję oddzielnie.
6. Porównać model `τ_nuc` z baseline'ami na danych odłożonych.
7. Opublikować surowe dane, manifest, kod, wersje bibliotek, seed, wyniki i raport negatywny.

## 9. Artefakty wymagane do reprodukcji

Katalog wynikowy:
`experiments/nuclear_reduction/NRG-01/`

Wymagane pliki:
- `README.md` — instrukcja uruchomienia;
- `manifest.json` — źródła, wersje, commity, daty, SHA-256;
- `raw/` — oryginalne dane (z zachowaniem warunków licencji);
- `processed/nuclides.csv`, `processed/transitions.csv`;
- `graphs/` — grafy i metryki;
- `models/` — konfiguracje baseline i TRM;
- `results/` — wyniki surowe, wykresy, metryki i niepewności;
- `report.md` — interpretacja, ograniczenia i wyniki negatywne.

## 10. Kryterium przejścia do porównania z helisą

Porównanie z trójhelikalną geometrią może się rozpocząć dopiero, gdy:
- graf jest zwalidowany z ocenionymi danymi;
- każda reguła przejścia ma bilans i źródło;
- redukcja 4→3 ma jawne kryterium, a nie jest wybrana wizualnie;
- wiadomo, które obserwable zachowuje mapa;
- wykazano, że wniosek nie wynika wyłącznie z arbitralnego grupowania.

Do tego czasu eksperyment jest protokołem, a nie wynikiem.

## 11. Dziennik zmian

- **2026-11-09 / v0.1:** prerejestracja eksperymentu grafu nuklidów; rozdzielenie grafu przejść od węzła topologicznego; zapis testów redukcji i modelu `τ_nuc`; ustalenie kryteriów porównania z geometrią TIMDR.
