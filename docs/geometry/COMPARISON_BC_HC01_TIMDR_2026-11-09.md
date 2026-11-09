# Porównanie: Boerdijk–Coxeter, HC-01 i konstrukcja TIMDR

**Data:** 2026-11-09  
**Status:** porównanie formalne istniejących definicji; nie jest dowodem równoważności obiektów.  
**Powiązane źródła:** `timdr-signal-framework-SKILL.md` §12, `BOERDIJK_COXETER_EXACT_REFERENCE_2026-11-09.md`, `HELIX_CHARACTERIZATION_PROTOCOL_HC01_v0.1.md`, `TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md`, `Axioms_G_TIMDR_Geometry.md`, `HELIX_SOURCE_PROPERTIES_DRIFT_AUDIT_2026-11-09.md`.

## 1. Wynik porównania w skrócie

**BC i HC-01 są geometrycznie zgodne na poziomie położenia wierzchołków:** dokładna konstrukcja odbić czworościanów generuje dyskretny zbiór punktów leżących na jednej helisie kołowej. Można zatem wyznaczyć odpowiadającą jej ciągłą helisę HC-01 z dokładnych parametrów śrubowych.

**TIMDR nie ma jeszcze jawnego operatora generującego helisę z trójkąta.** W G2 trójkąt i jego asymetria są pierwotnym obiektem; G3/G9 opisują zmianę pola normalnych powierzchni i operator Weingartena. Nie podano jednak reguły, która z trójkątnego modułu, jego odbicia i sklejenia tworzy kolejne punkty osi lub kolejne moduły przestrzenne. Nie można więc obecnie wyprowadzić (S_{TIMDR}) ani uczciwie stwierdzić równoważności z BC.

## 2. Porównanie obiektów

| Cecha | Boerdijk–Coxeter (BC) | HC-01 | TIMDR – stan źródeł |
|---|---|---|---|
| Obiekt bazowy | regularny czworościan foremny | ciągła krzywa kołowa | trójkąt Δ=(A,B,C), asymetria jako kandydat źródła różnicy |
| Reguła generowania | odbicie najstarszego z 4 wierzchołków przez płaszczyznę pozostałych 3 | jawna parametryzacja (r(t)=(acos t,asin t,ht)) | brak jednoznacznej reguły odbicia modułu i sklejenia |
| Wymiar | dyskretne wierzchołki + tetraedry | ciągła krzywa 1D | trójkąt/powierzchnia i pole normalnych; oś helisy jako pierwotna hipoteza, bez parametryzacji |
| Oś | wyprowadzona z transformacji śrubowej | dana jako oś z | postulowana jako pierwotna, ale nie wyprowadzona z operatora |
| Skręt | kąt dwuścienny, kąt obrotu śrubowego i ciągła τ_FS to różne miary | τ_FS ma wzór analityczny | (T_S) jest zmianą pola normalnych; nie jest τ_FS |
| Domknięcie | łańcuch otwarty/nieskończony | helisa otwarta | zależne od wariantu; G5 wymaga zamkniętej krzywej |
| Status | dokładnie skonstruowane i przetestowane | analityczny baseline i pilot numeryczny | mechanizm trójkąt→helisa pozostaje hipotezą |

## 3. BC jako szczególny przypadek HC-01

Dla BC, w konwencji współrzędnych z raportu:
[
a=\frac{3\sqrt6}{5},\qquad
\Delta z=-\frac{2}{\sqrt5},\qquad
\Delta\phi=\arccos(-2/3).
]
Odpowiadający ciągły skok HC-01 na jednostkę kąta:
[
h=\frac{\Delta z}{\Delta\phi}
=\frac{-2/\sqrt5}{\arccos(-2/3)}.
]
Wyniki numeryczne:
- promień (a\approx1.4696938457);
- (h\approx-0.3887928131);
- κ ≈ 0.6359118106;
- podpisana τ_FS ≈ -0.1682241117;
- τ_FS/κ ≈ -0.2645400022;
- skok na pełny obrót (2\pi h\approx-2.443) (wartość zaokrąglona).

Kontrola: odległość kolejnych wierzchołków wynosi dokładnie (2\sqrt2); odpowiadająca jej długość cięciwy spełnia:
[
2a^2(1-\cos\Delta\phi)+(h\Delta\phi)^2=8.
]
To dowodzi zgodności dyskretnych punktów BC z próbkami ciągłej helisy kołowej. Nie dowodzi, że tetraedry jako bryły są równoważne krzywej HC-01 ani że HC-01 zawiera regułę generowania BC.

## 4. Korekta terminologiczna: trzy kąty, nie jedna „torsja”

W regularnym czworościanie wewnętrzny kąt dwuścienny ma (cos\alpha=1/3), (alpha\approx70.5288^\circ). Transformacja śrubowa BC ma kąt obrotu na krok (cos\theta=-2/3), (	heta\approx131.8103^\circ). Ciągła helisa HC-01 ma ponadto torsję Freneta–Serreta τ_FS w jednostkach odwrotności długości.

W skillu Claude §12 wyrażenie „torsion angle” z (cos\tau=1/3) jest terminologicznie niejednoznaczne. W tym porównaniu wartość (1/3) przypisujemy wewnętrznemu kątowi dwuściennemu czworościanu, a kąt śrubowy wyprowadzamy niezależnie z macierzy (R). Nie utożsamiamy żadnego z tych kątów z τ_FS.

## 5. Dlaczego nie wolno jeszcze podać BC do G-Rezonansu

Obecny G5 / `build_ring_matrices` zakłada zamkniętą krzywą z cyklicznym pierścieniem (N\ge3) węzłów. Łańcuch BC jest otwarty i nieskończony (albo skończony z końcami), więc bez jawnego domknięcia lub warunków brzegowych nie spełnia domeny G5. Sztuczne połączenie końców zmieniłoby problem fizyczny i widmo.

Ponadto G5 używa (|\tau_i|) w sprzężeniu. Znak torsji zostaje utracony. Nie jest to „błąd” w sensie algebraicznym obecnego modelu skalarnego, ale oznacza, że G5 w tej postaci nie jest testem chiralności. Dodanie znaku do skalarnej sprężyny nie jest automatycznie poprawnym modelem fizycznym. Chiralne sprzężenie wymagałoby jawnego, zorientowanego stopnia swobody (np. wektorowego przekroju i macierzy transportu ramy) oraz jednostek/definicji kąta obrotu na segmencie. Taki operator byłby osobną hipotezą modelową.

## 6. Najważniejsza luka TIMDR

Zestawienie G2–G4/G9 i `TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md` daje:
- trójkąt jako obiekt źródłowy;
- asymetrię jako kandydat źródła różnicy;
- pole normalnych i zmianę orientacji powierzchni;
- operator Weingartena / krzywizny powierzchni.

Nie daje natomiast:
1. jednoznacznej definicji modułu, który jest odbijany;
2. operatora odbicia/obrotu kolejnych modułów;
3. reguły sklejenia na szwie;
4. macierzy przejścia (S_{TIMDR});
5. mapy z modułów do osi (A(s)) i gałęzi helikalnych;
6. dowodu domknięcia pozycji, stycznej, ramy i fazy.

Z tego powodu hipoteza „obrót trójkątnych modułów generuje helisę” pozostaje **HYPOTHESIS**, zgodnie z audytem driftu źródłowego. BC jest użytecznym wzorcem porównawczym: pokazuje, jak wygląda kompletny operator, ale nie uzupełnia brakującej reguły TIMDR.

## 7. Następny eksperyment – bez dopowiadania mechanizmu

Przywrócić kolejność z audytu źródłowego:
1. ustalić, co dokładnie jest odbijane: trójkąt jako bryła/moduł, jego wierzchołki, orientacja czy stan;
2. jawnie określić płaszczyznę odbicia i regułę wyboru strony;
3. określić, jak kolejny moduł jest sklejany z poprzednim (wspólny wierzchołek, krawędź, ściana lub inny interfejs);
4. dopiero z tych danych wyprowadzić operator przejścia i sprawdzić, czy jest stały;
5. wyznaczyć oś z konstrukcji, nie zakładać jej parametryzacji;
6. porównać przewidywania na kolejnych modułach niewykorzystanych do wyznaczenia operatora;
7. wykonać odbicie lustrzane i sprawdzić, które wielkości zmieniają znak.

Nie rozwijać teraz hipotezy 5→6, kuli/jaja ani punktów kardynalnych. Nie ma jeszcze operatora bazowego, który miałby być przez nie ograniczany.

## 8. Decyzja

- BC: **EXACTLY VERIFIED** jako modułowa tetrahelisa.
- BC vertex locus ↔ HC-01: **EXACT GEOMETRIC EQUIVALENCE** po sztywnym ustawieniu osi i odpowiednim próbkowaniu.
- BC ↔ TIMDR: **NO EQUIVALENCE ESTABLISHED**.
- Trójkąt TIMDR → helisa: **HYPOTHESIS / OPERATOR MISSING**.
- BC → G5 response: **NOT DIRECTLY APPLICABLE** bez jawnych warunków końcowych/domknięcia i modelu znaku skrętu.

**Reguła anty-zapętlenia:** następną pracą nie jest kolejny sweep promienia, torsji ani progu. Jest nią formalne odzyskanie źródłowego operatora trójkąt→moduł następny. BC pozostaje referencją do testowania kompletności takiego operatora.
