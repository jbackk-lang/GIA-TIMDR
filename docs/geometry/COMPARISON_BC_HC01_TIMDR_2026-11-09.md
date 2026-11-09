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


## 10. Istniejący test chiralności w repozytorium siostrzanym Helix-Lock

Dodatkowo sprawdzono rzeczywisty kod źródłowy, a nie tylko opis archiwalny:
- `jbackk-lang/Helix-Lock/experiments/helical_tunnel_chirality.py`
- `jbackk-lang/Helix-Lock/tests/test_helical_tunnel_chirality.py`
- `jbackk-lang/Helix-Lock/docs/HELIX_LOOP_PARAMETER_BOUNDS.md`

To już istniejący eksperyment syntetyczny, który tworzy helisę prawą i jej lustrzane odbicie, sprawdza równość krzywizny i przeciwny znak torsji, układa poprzeczny wektor sygnału w lokalnej ramie Freneta, porównuje konwencję fazy zgodną z chiralnością z naiwną stałą konwencją fazy oraz pokazuje, że obecny G5 ma identyczną macierz sztywności i widmo dla obu znaków torsji przez abs(tau).

**Rzeczywiste logi CI Helix-Lock, run 42559444225:**
- Python 3.11: 148 testów zaliczonych;
- Python 3.12: 148 testów zaliczonych;
- średni błąd lustrzany sygnału przy konwencji chiralnej: 0.0;
- średni błąd przy naiwnej stałej konwencji fazy: 1.255915117488;
- maksymalny błąd przy konwencji chiralnej: 0.0;
- maksymalny błąd przy konwencji naiwnej: 1.996053456857;
- torsja prawej/lewej helisy: +0.311804008909 / -0.311804008909;
- macierze G5 i widma pod odbiciem: identyczne.

To jest już przetestowany baseline chiralności; nie należy kopiować go ponownie do GIA-TIMDR. Trzeba go traktować jako wynik syntetyczny i konwencję kandydującą, nie jako wyprowadzenie oryginalnego prawa TIMDR ani dowód odzyskiwania dowolnego payloadu.

**Konsekwencja dla następnej pracy:** nie powtarzać testu „czy znak torsji znika w G5” ani testu kowariancji tej samej idealnej helisy — one już istnieją. Nowe pytanie ma być inne: czy źródłowa reguła modułu TIMDR (po jej jednoznacznym zdefiniowaniu) indukuje tę samą regułę transportu ramy/fazy, czy wymaga innej. W razie potrzeby należy rozszerzyć istniejący test o geometrię wyprowadzoną z modułu, a nie tworzyć drugi eksperyment dla standardowej helisy.


## 11. Dodatkowa różnica: asymetria lokalna a skręt globalny modułów

Każda ściana czworościanu BC jest trójkątem równobocznym; kolejne tetraedry są przystające, a reguła doklejania zachowuje wszystkie krawędzie. Mimo braku asymetrii pojedynczego trójkąta, cała sekwencja ma niezerowy obrót śrubowy. W BC skręt globalny wynika z trójwymiarowej reguły odbicia i sklejenia modułów, nie z deformacji lokalnej ściany trójkątnej.

To nie obala G2 TIMDR: G2 mówi o asymetrii trójkąta jako źródle skrętu w gałęzi geometrycznej G, natomiast BC jest konstrukcją łańcucha brył z globalnym transportem orientacji. Pokazuje jednak, że musimy rozdzielić dwa mechanizmy: (a) lokalną asymetrię pojedynczego modułu/pola normalnych oraz (b) globalny obrót/holonomię wynikającą z reguły sklejenia modułów. Nie można zakładać, że jeden z nich automatycznie implikuje drugi.

**Nowy test dla przyszłego operatora TIMDR:** porównać wariant modułu symetrycznego i asymetrycznego przy tej samej regule sklejenia, a osobno zmienić regułę sklejenia przy stałym module. Zmierzyć przyrost fazy/ramy na krok. To rozdzieli, czy źródłem helikalności jest kształt modułu, czy globalna operacja jego transportu. Test ma sens dopiero po formalnym zdefiniowaniu obu wariantów; nie kodować z góry oczekiwanego wyniku.


## 12. Kontrola źródeł archiwalnych i repozytoriów siostrzanych

Sprawdzono bezpośrednio wskazane źródła, a nie tylko ich streszczenie w GIA:

- `TIMDR-Concept-Archive/TRM-Geometry-Core/docs/triangle.md` i `src/triangle.py`: trójkąt równoboczny jest opisany przez bok (a=r√3), trzy stany/fazy; kod zwraca jedynie długość boku. Brak 3D współrzędnych modułu, reguły odbicia, płaszczyzny sklejenia lub macierzy przejścia.
- `TRM-Geometry-Core/docs/core.md` i `docs/transitions.md`: operatorami są relacje skali (√3), (√π), (2/√3); dokument deklaruje zachowanie informacji, ale nie definiuje bijekcji ani operatora generującego helisę.
- `Topological-Reduction-Model-TRM/core/topological-wave.md` i `core/twist-reduction-law.md`: τ jest skalarnym polem/parametrem w równaniu fali i progu redukcji; nie jest tam geometrią krzywej, torsją Freneta ani regułą modułowego odbicia.
- `TIMDR-Geometry-Formalism/timdr_geometry/weingarten.py`: istnieje implementacja operatora kształtu na trójkątnej siatce powierzchni; nie generuje ona łańcucha modułów ani osi helisy.
- `THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py`: liczy krzywiznę i torsję z próbek ogólnej trajektorii 3D; nie konstruuje trajektorii z trójkąta.
- `TIMDR-META-DYNAMICS/models/evolution_helix.py` klasyfikuje stany po wejściowym `MetaState.tau`; jego własny docstring określa progi jako arbitralne. `analysis/meta_torsion.py` liczy oddzielną torsję Freneta trajektorii ((Λ,τ,ρ)). To odrębne wielkości, nie generator helisy.

**Wniosek po kontroli źródeł:** w tych wskazanych repozytoriach i plikach nie znaleziono brakującego (S_{TIMDR}). Zapis „trójkąt → helisa” jest kierunkiem/hipotezą, nie gotowym algorytmem. Nie należy konstruować go przez sklejanie samych współczynników (√3), (√2), τ lub przez zmianę etykiet. Potrzebne są jawne współrzędne, operator odbicia, interfejs sklejenia i orientacja.


## 10. Uzupełnienie: ogólny czworościan ma operator śrubowy co cztery kroki

Późniejszy dowód w `GENERAL_TETRAHEDRON_FOUR_STEP_SCREW_THEOREM_v0.1.md` doprecyzowuje wcześniejszą lukę z §6–7. Dla dowolnego niekoplanarnego czworościanu nie musi istnieć izometria przenosząca uporządkowane okno o jeden krok, ale istnieje stała właściwa izometria `T` przenosząca je o cztery kroki: `T(v_n)=v_{n+4}`. Wynika to z czterookresowej permutacji sześciu uporządkowanych kwadratów krawędzi oraz ekwiwariantności odbicia względem izometrii.

Zatem ogólny łańcuch BC nie jest na ogół jedną próbkowaną helisą jednokrokową. Jest sumą czterech przeplatanych orbit tej samej izometrii; w przypadku niezerowego obrotu i postępu osiowego są to cztery dyskretne helisy o wspólnej osi. To nie dowodzi fraktalności i nadal nie ustanawia równoważności BC z TIMDR.
