# TIMDR_Twists — skonsolidowana formalna specyfikacja czterech znaczeń "skrętu"

**Status:** dokument referencyjny (T1 + T2), nie nowy zestaw aksjomatów.
Nie definiuje niczego nowego matematycznie — zbiera w jednym miejscu
formalne definicje "skrętu", które już istnieją rozproszone po
`Axioms_S_TIMDR_Signal.md`, `Axioms_G_TIMDR_Geometry.md`,
`Operators_N_TIMDR.md` i `MAGE-IN-IMAGE-DECODER`, i jawnie rozdziela ich
domeny. Źródłem prawdy dla każdej definicji pozostaje plik źródłowy
wskazany w kolumnie "Źródło" — ten dokument jest indeksem/mapą, nie
zamiennikiem.

**Dlaczego ten dokument istnieje:** "skręt"/"twist" jest w ekosystemie
TIMDR słowem przeciążonym — używanym w co najmniej czterech,
matematycznie niezwiązanych znaczeniach. `GLOSSARY_EN_PL.md` już
zawiera krótkie wpisy dla każdego; ten dokument idzie krok dalej i
podaje pełną domenę/przeciwdziedzinę/definicję dla każdego, jedno pod
drugim, żeby rozdzielenie było niepodważalne przy pierwszym spojrzeniu.

---

## T1 — Formalne definicje czterech skrętów

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

---

## T2 — Jawne rozdzielenie domen

| Znaczenie | Gałąź TIMDR | Domena obiektu | Przeciwdziedzina | Relacja do pozostałych trzech |
|---|---|---|---|---|
| Skręt sygnałowy | M/S (sygnałowa) | szereg czasowy \(x:T\to\mathbb{R}^d\) | boolowska (wykryty/nie) | niezależny; dzieli słowo, nie obiekt |
| Skręt topologiczny (τ) | G (geometryczna) | rodzina powierzchni \(S_\lambda\) | zależna od parametryzacji | niezależny od skrętu powierzchniowego (inna domena: rodzina vs. ustalona siatka) |
| Skręt powierzchniowy | G (geometryczna) | ustalona siatka \(S\subset\mathbb{R}^3\) | \([0,2]\subset\mathbb{R}_{\geq0}\) | niezależny od τ; związany z krzywizną przez G9, nie z τ |
| Twist blokowy | poza TIMDR | bloki obrazu 2D | zależna od implementacji | całkowicie niezależny, tylko leksykalne podobieństwo nazwy |

**Zasada nadrzędna (zgodna z Aksjomatem G6 i analogicznym rozdziałem w
`Axioms_S_TIMDR_Signal.md`):** żadne z czterech znaczeń nie jest
rozszerzeniem ani szczególnym przypadkiem żadnego innego. Wspólne słowo
nazywa różne obiekty matematyczne w różnych domenach — nie różne
poziomy jednej teorii. Każde nowe użycie słowa "skręt"/"twist" w tym
ekosystemie powinno od razu wskazywać, o które z czterech (lub o nowe,
piąte) znaczenie chodzi.

---

Powiązane: [`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md)
(Aksjomat 4 — skręt sygnałowy), [`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md)
(Aksjomaty G3, G8, G9 — skręt powierzchniowy), [`Operators_N_TIMDR.md`](./Operators_N_TIMDR.md)
(skręt topologiczny τ), [`TIMDR_Branch_Specification.md`](./TIMDR_Branch_Specification.md)
(formalna specyfikacja trzech gałęzi TIMDR, w tym rozdzielenie
"skrętu" per gałąź), [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md)
(krótkie, dwujęzyczne wpisy — ten dokument jest ich rozwinięciem).
