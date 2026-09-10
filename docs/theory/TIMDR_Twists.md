# TIMDR_Twists — skonsolidowana formalna specyfikacja sześciu znaczeń "skrętu"

**Status:** dokument referencyjny (T1 + T2), nie nowy zestaw aksjomatów.
Nie definiuje niczego nowego matematycznie — zbiera w jednym miejscu
formalne definicje "skrętu", które już istnieją rozproszone po
`Axioms_S_TIMDR_Signal.md`, `Axioms_G_TIMDR_Geometry.md`,
`Operators_N_TIMDR.md` i `MAGE-IN-IMAGE-DECODER`, i jawnie rozdziela ich
domeny. Źródłem prawdy dla każdej definicji pozostaje plik źródłowy
wskazany w kolumnie "Źródło" — ten dokument jest indeksem/mapą, nie
zamiennikiem.

**Dlaczego ten dokument istnieje:** "skręt"/"twist" jest w ekosystemie
TIMDR słowem przeciążonym — używanym w co najmniej sześciu,
matematycznie niezwiązanych znaczeniach. `GLOSSARY_EN_PL.md` już
zawiera krótkie wpisy dla każdego; ten dokument idzie krok dalej i
podaje pełną domenę/przeciwdziedzinę/definicję dla każdego, jedno pod
drugim, żeby rozdzielenie było niepodważalne przy pierwszym spojrzeniu.

**Uwaga o symbolu τ poza tym dokumentem:** ten plik indeksuje znaczenia
słowa "skręt"/"twist", nie każde użycie samego symbolu τ w ekosystemie.
Gałąź META-DYNAMICS (`TIMDR_Branch_Specification.md`, sekcja "Gałąź
META-DYNAMICS") ma WŁASNE τ ("transformacja", tempo zmiany defektu w
Λ-τ-ρ-J) — nigdy nie nazywane "skrętem" w kodzie źródłowym, więc formalnie
poza zakresem tego dokumentu, ale współdzielące symbol z punktami 2 i 6
poniżej. Czytelnik szukający WSZYSTKICH kolizji symbolu τ (nie tylko
słowa "skręt") powinien sprawdzić oba dokumenty.

---

## T1 — Formalne definicje pięciu skrętów

### 1. Skręt sygnałowy (gałąź M/S — sygnałowa)

- **Domena:** szereg czasowy \(x: T \to \mathbb{R}^d\), \(T \subset
  \mathbb{R}\) (dyskretne próbki w czasie).
- **Definicja:** odwrócenie trendu — zmiana znaku lokalnego nachylenia
  regresji między dwoma kolejnymi oknami, o wielkości przekraczającej
  próg \(1.5\sigma\):
  \[
  \text{skręt}(t) \iff \operatorname{sign}(\text{slope}(x, W_{t-1})) \neq
  \operatorname{sign}(\text{slope}(x, W_t)) \;\land\;
  |\Delta\text{slope}| > 1.5\sigma
  \]
- **Przeciwdziedzina:** boolowska (skręt wykryty / nie wykryty) w danym
  punkcie czasowym \(t\).
- **Nie jest:** bifurkacją w sensie teorii układów dynamicznych (brak
  jawnego modelu \(f(x;\lambda)\)) — patrz `Resonance_M_Operator_Empiryczny.md`
  §5.
- **Wcześniejszy, mniej rygorystyczny wariant:** \(T(t) =
  [\operatorname{sign}(S'(t)) \neq \operatorname{sign}(S'(t-\Delta t))]\)
  z sekcji "📘 TIMDR — Pełny Model..." w głównym README — ten sam
  koncept (odwrócenie kierunku), ale bez progu wielkości (samo
  przejście przez zero). Traktowany jako poprzednik, nie osobne, piąte
  znaczenie.
- **Źródło:** `Axioms_S_TIMDR_Signal.md` (Aksjomat 4).

### 2. Skręt topologiczny (τ) (gałąź G — geometryczna, dynamika deformacji)

- **Domena:** rodzina powierzchni \(S_\lambda \subset \mathbb{R}^3\)
  parametryzowana stopniem deformacji \(\lambda\) (nie pojedynczy punkt
  ani szereg czasowy).
- **Definicja:** deformacja powierzchni zmieniająca orientowalność —
  przejście torus → wstęga Möbiusa → tetroida, wzdłuż ciągłej ścieżki
  deformacji \(\lambda \mapsto S_\lambda\); τ opisuje stopień/moment
  tej zmiany.
- **Przeciwdziedzina:** zależna od konkretnej parametryzacji w
  `Operators_N_TIMDR.md` (osobliwość τ jest zdarzeniem na ścieżce
  deformacji, nie liczbą per punkt powierzchni).
- **Nie jest:** torsją krzywej Freneta-Serreta \(\tau(t) = [(\dot r
  \times \ddot r)\cdot \dddot r]/\|\dot r \times \ddot r\|^2\)
  (sprawdzone i odrzucone jako tożsame — `timdr-signal-framework` §20,
  §12 macierzystego skilla) ani skrętem powierzchniowym poniżej (inna
  domena: rodzina powierzchni, nie ustalona siatka 3D).
- **Źródło:** `Operators_N_TIMDR.md` ("Skręt τ i jego osobliwość").

### 3. Skręt powierzchniowy (gałąź G — geometryczna, statyczna siatka)

- **Domena:** ustalona dopuszczalna powierzchnia \(S \subset
  \mathbb{R}^3\) (Aksjomat G1) z polem normalnych \(n: S \to
  \mathbb{S}^2\) określonym p.w.; operator \(T_S: S \times \mathbb{R}^3
  \rightharpoonup \mathbb{R}_{\geq 0}\) jest funkcją częściową punktu
  \(p\) i dopuszczalnego lokalnego przesunięcia \(\Delta p\) (Aksjomat
  G8a).
- **Definicja:**
  \[
  T_S(p) = \|n(p+\Delta p) - n(p)\|
  \]
  z jawną postacią przez dyskretny/różniczkowy operator Weingartena:
  \(T_S(p) = \|\Delta p\|\cdot\|S_p(\widehat{\Delta p})\| +
  O(\|\Delta p\|^2)\) (Aksjomat G9c).
- **Przeciwdziedzina:** \(T_S(p) \in [0,2]\) (ograniczone, bo \(n\) są
  wektorami jednostkowymi — Aksjomat G8b).
- **Nie jest:** torsją krzywej 1D (Aksjomat G3d) ani skrętem
  topologicznym τ powyżej (inna domena: ustalona siatka, nie rodzina
  powierzchni).
- **Źródło:** `Axioms_G_TIMDR_Geometry.md` (Aksjomaty G3, G8, G9),
  pierwsze wprowadzenie w `Resonance_M_Operator_Empiryczny.md` §6.

### 4. Twist blokowy (poza gałęziami TIMDR — MAGE-IN-IMAGE-DECODER)

- **Domena:** bloki obrazu w pipeline'ie dekodowania obrazu-w-obrazie
  (siatka 2D bloków pikseli, nie powierzchnia 3D ani szereg czasowy).
- **Definicja:** własna implementacja `TwistDetector` — nie jest
  instancją żadnej z trzech gałęzi TIMDR (M/S, G, K); nazwa współdzielona
  wyłącznie leksykalnie.
- **Przeciwdziedzina:** zależna od implementacji `TwistDetector`.
- **Nie jest:** częścią formalizmu TIMDR w żadnym sensie — wymieniony
  tu wyłącznie dla kompletności rozgraniczenia nazwy "skręt/twist" w
  szerszym ekosystemie repo.
- **Źródło:** `MAGE-IN-IMAGE-DECODER` repo, własny pipeline.

### 5. Torsja Freneta-Serreta trójwęzła (skręt osiowy) (gałąź G — geometryczna, krzywa 3D)

- **Domena:** pojedyncza przestrzenna krzywa \(\gamma: T \to
  \mathbb{R}^3\) sparametryzowana czasem/parametrem \(t\) (tu:
  klasyczny trójwęzeł/trefoil knot, ale definicja nie jest ograniczona
  do tej jednej krzywej) — **nie** rodzina powierzchni (jak τ
  topologiczne) ani ustalona siatka (jak skręt powierzchniowy).
- **Definicja:** torsja Freneta-Serreta liczona z prędkości/
  przyspieszenia/szarpnięcia (\(v,a,j\)) wyznaczonych różnicami
  skończonymi z 4 kolejnych próbek krzywej:
  \[
  \kappa(t) = \frac{\|v \times a\|}{\|v\|^3}, \qquad
  \tau(t) = \frac{\det(v,a,j)}{\|v \times a\|^2}
  \]
  z bramkowaniem szumu identycznym jak przy skręcie powierzchniowym:
  \(\kappa(t) < \kappa_{min} \Rightarrow \tau(t) = 0\) (dzielenie przez
  \(\|v\times a\|^2\) wzmacnia szum przy niemal-prostoliniowym odcinku
  krzywej — ten sam wzorzec błędu, co przy `cross_norm==0` opisanym w
  `the_geo_pro_4d.py`).
- **Przeciwdziedzina:** \(\tau(t) \in \mathbb{R}\) (nieograniczona, w
  przeciwieństwie do skrętu powierzchniowego \([0,2]\)).
- **Nie jest:** skrętem topologicznym τ powyżej (inna domena:
  pojedyncza krzywa 3D, nie rodzina powierzchni \(S_\lambda\)) — mimo
  współdzielonego symbolu τ w obu miejscach, celowo NIEidentyfikowane.
  Formalnie ten sam matematyczny obiekt co torsja Freneta-Serreta,
  którą `Operators_N_TIMDR.md` explicite sprawdza i **odrzuca** jako
  tożsamą ze skrętem topologicznym — więc tu jest nazwana wprost jako
  odrębne, piąte znaczenie, zamiast milcząco pożyczać nazwę "skręt
  topologiczny".
- **Status:** empirycznie przetestowane na syntetycznym trójwęźle z
  kontrolą pozytywną (deformacja węzła wykrywalna, zlokalizowana z
  dokładnością ≤6 próbek/300) i negatywną (czysty trójwęzeł — zero
  fałszywych alarmów) — patrz `TIMDR_Trefoil_FrenetTorsion.md`. Różni
  się statusem od τ topologicznego (koncepcyjne, bez implementacji) i
  od skrętu powierzchniowego (analityczne G8-G9, numeryczna
  implementacja nieuruchomiona w sesji, w której powstała) — to jedyne
  z trzech znaczeń gałęzi G, które ma **uruchomione i potwierdzone
  testy** na tym etapie.
- **Źródło:** `core/trefoil_frenet_torsion.py`,
  `docs/geometry/TIMDR_Trefoil_FrenetTorsion.md`. Matematyka
  identyczna z `THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py` (tam
  zwalidowana: błąd <0,001% względem analitycznej helisy).

### 6. τ TRM (Model Topologicznej Redukcji, gałąź poza formalną klasyfikacją M/S/G/K)

- **Domena:** ciągły proces redukcji informacji \(I(t)\) — nie rodzina
  powierzchni (jak τ topologiczne), nie ustalona siatka (jak skręt
  powierzchniowy), nie pojedyncza krzywa 3D (jak torsja trójwęzła) —
  skalarna wielkość dynamiczna z własną drabinką dyskretną
  \(\tau_{i+1}=\lambda\tau_i \to \phi\).
- **Definicja:** prawo redukcji \(R(\tau)=k\cdot\tau^n\),
  \(dI/dt=-R(\tau)\), z rozwiązaniem analitycznym dla \(n\neq1\)
  (autonomiczna postać \(\tau=aI\) daje \(dI/dt=-C\cdot I^n\)). Stan
  graniczny \(\phi\) opisany jako "czysta rotacja" (minimalna informacja).
- **Przeciwdziedzina:** \(\tau(t) \in \mathbb{R}_{\geq0}\) (ciągła
  wielkość skalarna z własną dynamiką różniczkową, nie zdarzenie
  boolowskie ani miara chwilowa punktu/siatki).
- **Nie jest (ROZSTRZYGNIĘTE):** torsją Freneta-Serreta trójwęzła
  (punkt 5) — inna domena, inna dynamika.
- **Nie jest (NIEROZSTRZYGNIĘTE, jawnie zostawione otwarte na prośbę
  użytkownika):** czy τ TRM to rozszerzenie skrętu topologicznego τ
  (punkt 2) czy odrębny obiekt pod tym samym symbolem — język
  `TRM_biology.md` ("τ_krit", "skręt τ rośnie aż do wartości
  krytycznej") silnie przypomina `Operators_N_TIMDR.md`, ale związek
  nie został zbadany matematycznie. Traktuj jako otwarte pytanie, nie
  jako ustalone rozróżnienie ani utożsamienie.
- **Status empiryczny:** rdzeń matematyczny (rozwiązanie analityczne)
  sprawdzony algebraicznie jako poprawny. Prawo redukcji \(R(\tau)=k\tau^n\)
  przetestowane empirycznie metodą AIC (próg pre-rejestrowany ΔAIC=2)
  na dwóch niezależnych realnych krzywych zaniku (dyspersja kolapsu
  TIMDR-Quantum-Lattice: ΔAIC=+7.96; zanik pojemności baterii NASA
  B0047: ΔAIC=+38.02) — **ODRZUCONE dwukrotnie** (dodatkowy parametr
  \(n\) nie jest uzasadniony na żadnej z dwóch realnych krzywych
  testowanych dotąd). To NIE obala `TRM_biology.md` jako całości
  (jakościowe twierdzenia teorii pozostają nietestowane tą metodą) —
  tylko konkretne, dosłowne prawo redukcji w tej formie funkcyjnej.
- **Źródło:** `TRM_biology.md`, `timdr-signal-framework` §13 (pełne
  liczby obu testów AIC), `TIMDR_Branch_Specification.md` (odnośnik do
  tej sekcji z punktu widzenia gałęzi META-DYNAMICS, z którą τ TRM NIE
  jest tożsame mimo pokrewnego ducha "tempa zmiany").

---

## T2 — Jawne rozdzielenie domen

| Znaczenie | Gałąź TIMDR | Domena obiektu | Przeciwdziedzina | Relacja do pozostałych |
|---|---|---|---|---|
| Skręt sygnałowy | M/S (sygnałowa) | szereg czasowy \(x:T\to\mathbb{R}^d\) | boolowska (wykryty/nie) | niezależny; dzieli słowo, nie obiekt |
| Skręt topologiczny (τ) | G (geometryczna) | rodzina powierzchni \(S_\lambda\) | zależna od parametryzacji | niezależny od skrętu powierzchniowego i od torsji trójwęzła (inna domena); relacja z τ TRM NIEROZSTRZYGNIĘTA |
| Skręt powierzchniowy | G (geometryczna) | ustalona siatka \(S\subset\mathbb{R}^3\) | \([0,2]\subset\mathbb{R}_{\geq0}\) | niezależny od τ i od torsji trójwęzła; związany z krzywizną przez G9, nie z τ |
| Twist blokowy | poza TIMDR | bloki obrazu 2D | zależna od implementacji | całkowicie niezależny, tylko leksykalne podobieństwo nazwy |
| Torsja Freneta-Serreta trójwęzła | G (geometryczna) | pojedyncza krzywa 3D \(\gamma:T\to\mathbb{R}^3\) | \(\mathbb{R}\) (nieograniczona) | niezależna od τ topologicznego mimo współdzielonego symbolu τ; jedyne znaczenie gałęzi G z uruchomionymi testami |
| τ TRM | poza formalną klasyfikacją M/S/G/K | skalarny proces redukcji \(I(t)\) z drabinką \(\tau_{i+1}=\lambda\tau_i\to\phi\) | \(\mathbb{R}_{\geq0}\) | relacja z τ topologicznym NIEROZSTRZYGNIĘTA; prawo redukcji ODRZUCONE empirycznie (AIC) dwukrotnie, nie obala całości TRM_biology.md |

**Zasada nadrzędna (zgodna z Aksjomatem G6 i analogicznym rozdziałem w
`Axioms_S_TIMDR_Signal.md`):** żadne z sześciu znaczeń nie jest
rozszerzeniem ani szczególnym przypadkiem żadnego innego (z jednym
jawnie oznaczonym wyjątkiem: relacja skręt topologiczny ↔ τ TRM jest
NIEROZSTRZYGNIĘTA, nie ustalona jako niezależna). Wspólne słowo/symbol
nazywa różne obiekty matematyczne w różnych domenach — nie różne
poziomy jednej teorii. Każde nowe użycie słowa "skręt"/"twist" (lub
symbolu τ) w tym ekosystemie powinno od razu wskazywać, o które z
sześciu (lub o nowe, siódme) znaczenie chodzi — patrz też τ
META-DYNAMICS w `TIMDR_Branch_Specification.md`, które współdzieli
symbol, ale nigdy nie jest nazywane "skrętem".

---

Powiązane: [`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md)
(Aksjomat 4 — skręt sygnałowy), [`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md)
(Aksjomaty G3, G8, G9 — skręt powierzchniowy), [`Operators_N_TIMDR.md`](./Operators_N_TIMDR.md)
(skręt topologiczny τ), [`TIMDR_Branch_Specification.md`](./TIMDR_Branch_Specification.md)
(formalna specyfikacja czterech gałęzi TIMDR — M/S, G, K, META-DYNAMICS
— w tym rozdzielenie "skrętu"/τ per gałąź), [`TRM_biology.md`](./TRM_biology.md)
(punkt 6 — τ TRM, model topologicznej redukcji, prawo redukcji odrzucone
empirycznie), [`../geometry/tourosomobius.md`](../geometry/tourosomobius.md)
(pojęciowy szkic "trójwęzła helikalnego", inspiracja punktu 5 — czysto
notacyjny, bez formalizacji), [`TIMDR_Trefoil_FrenetTorsion.md`](../geometry/TIMDR_Trefoil_FrenetTorsion.md)
(punkt 5 — torsja Freneta-Serreta trójwęzła, pełny opis eksperymentu i
kodu), [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md)
(krótkie, dwujęzyczne wpisy — ten dokument jest ich rozwinięciem).
