# Axioms G — TIMDR-Geometry: aksjomaty gałęzi geometrycznej

**EN:** Formal axioms for the geometric branch of TIMDR — the triangle
model, surfaces, normals, and surface-twist. Distinct from the
signal-domain branch (`Axioms_S_TIMDR_Signal.md`) and the modal branch
(`Axioms_K_TIMDR.md`) — shared words ("skręt", "rezonans") name
different objects across the three, not different levels of one
theory.
**PL:** Gałąź G opisuje wyłącznie model geometryczny trójkąta,
powierzchni i skrętu powierzchniowego. Nie dotyczy sygnałów czasowych
(M, S) ani rezonansu modalnego (K) — wspólne słowa ("skręt",
"rezonans") oznaczają różne obiekty w trzech gałęziach, nie różne
poziomy jednej teorii.

Status: koncepcyjna (patrz Aksjomat G7). G1-G3 mają jasno określone
obiekty i wzory już używane gdzie indziej w repo (skręt powierzchniowy:
`Resonance_M_Operator_Empiryczny.md` §6). G4 wyznacza kierunek
(związek skrętu z krzywizną przez operator Weingartena); G8-G9 (dodane
później) domykają ten kierunek analitycznie — formalny operator \(T_S\)
z domeną/przeciwdziedziną/ciągłością (G8) i jawna postać \(F\) przez
dyskretny/różniczkowy operator Weingartena (G9) — ale wyłącznie jako
wyprowadzenie matematyczne (tożsamość różniczkowo-geometryczna w
granicy \(\Delta p \to 0\)), nie jako przetestowaną implementację na
siatce 3D ani walidację empiryczną: patrz zastrzeżenia pod G9 i status
w G7. G10 (dodany później, ta sama sesja co niniejsza aktualizacja)
formalizuje INNY obiekt — krzywiznę krzywej (obwiedni trójkąta), nie
powierzchni — jako parametr redukcji/rozwinięcia \((P,Q)\); status
identyczny jak G8-G9 (wyprowadzenie ręczne, niezaimplementowane), patrz
zastrzeżenie pod G10.

---

## Aksjomat G1 — Przestrzeń i obiekty podstawowe

Istnieje trójwymiarowa przestrzeń euklidesowa \(\mathbb{R}^3\) oraz
klasa dopuszczalnych powierzchni \(S \subset \mathbb{R}^3\), takich że:

- **(G1a)** Każda powierzchnia \(S\) jest lokalnie homeomorficzna z
  dyskiem (dwuwymiarowa, bez osobliwości topologicznych w lokalnej
  skali).
- **(G1b)** Na każdej powierzchni \(S\) istnieje dobrze określone pole
  normalnych \(n: S \to \mathbb{S}^2\) prawie wszędzie (z wyjątkiem
  zbioru miary zero).

---

## Aksjomat G2 — Trójkąt jako minimalna jednostka asymetrii

Istnieje wyróżniony obiekt \( \Delta = (A,B,C) \), trójkąt w
\(\mathbb{R}^3\), taki że:

- **(G2a)** Trójkąt równoboczny \(\Delta_{\text{eq}}\) reprezentuje
  stan idealnej symetrii: \(|AB| = |BC| = |CA|\).
- **(G2b)** Każde odejście od równoboczności (różnoboczność lub
  równoramienność) definiuje **asymetrię geometryczną** jako pierwotne
  źródło różnicy w gałęzi G.
- **(G2c)** Asymetria trójkąta jest minimalnym, nieredukowalnym
  źródłem skrętu w gałęzi geometrycznej.

---

## Aksjomat G3 — Skręt powierzchniowy jako lokalna zmiana orientacji

Dla powierzchni \(S\) z polem normalnych \(n(p)\) definiujemy
**lokalny skręt powierzchniowy** w punkcie \(p\) jako:

\[
T_S(p) = \|n(p+\Delta p) - n(p)\|
\]

gdzie \(\Delta p\) jest dopuszczalnym, lokalnym przesunięciem wzdłuż
powierzchni.

- **(G3a)** Skręt \(T_S(p)\) jest dobrze określony prawie wszędzie na
  \(S\).
- **(G3b)** \(T_S(p) = 0\) oznacza lokalny brak zmiany orientacji
  (brak skrętu).
- **(G3c)** Dodatnie wartości \(T_S(p) > 0\) oznaczają lokalną zmianę
  orientacji powierzchni (skręt).
- **(G3d)** Skręt powierzchniowy jest własnością pola normalnych, nie
  torsji krzywej — gałąź G nie utożsamia \(T_S\) z \(\tau\) krzywej 1D.

---

## Aksjomat G4 — Krzywizna i operator kształtu (Weingarten)

Istnieje dyskretny odpowiednik operatora kształtu (Weingarten) \(W_S\)
dla powierzchni \(S\), taki że:

- **(G4a)** \(W_S\) działa na polu normalnych \(n(p)\) i opisuje
  lokalną krzywiznę powierzchni.
- **(G4b)** Skręt powierzchniowy \(T_S(p)\) jest funkcją lokalnej
  krzywizny: istnieje funkcja \(F\) taka, że \(T_S(p) = F(W_S(p))\).
- **(G4c)** W gałęzi G krzywizna (poprzez \(W_S\)) jest pierwotna
  względem skrętu — skręt jest pochodną miarą zmiany orientacji, nie
  niezależnym obiektem.

*(Ten aksjomat wyznacza kierunek: implementacja \(W_S\) i \(F\) jest
otwarta, ale musi być zgodna z tym związkiem. To jest dokładnie luka,
którą `Axioms_S_TIMDR_Signal.md` — sekcja "Pozostałe braki formalne" —
zostawiła jako niesformalizowaną; G4 nie ją domyka, tylko nazywa i
zobowiązuje przyszłą implementację do zgodności z nią. **Aktualizacja:**
Aksjomaty G8-G9 poniżej podają jawną, analitycznie wyprowadzoną postać
\(F\) — patrz zastrzeżenia tam co do zakresu tego domknięcia.)*

---

## Aksjomat G8 — \(T_S\) jako formalny operator: domena, przeciwdziedzina, ciągłość, stabilność

Aksjomat G3 podaje wzór na \(T_S(p)\); ten aksjomat formalizuje go jako
właściwy operator matematyczny, nie tylko wyrażenie.

- **(G8a) Domena.** \(T_S\) jest funkcją częściową
  \(T_S: S \times \mathbb{R}^3 \rightharpoonup \mathbb{R}_{\geq 0}\),
  określoną w punktach \((p, \Delta p)\) takich że \(p \in S\),
  \(p + \Delta p \in S\), oraz \(n\) jest określone w obu punktach (co,
  z G1b, wyklucza jedynie zbiór miary zero) — zgodnie z G3a.
- **(G8b) Przeciwdziedzina jest ograniczona.** Ponieważ
  \(n(p), n(p+\Delta p) \in \mathbb{S}^2\) (wektory jednostkowe), z
  nierówności trójkąta na sferze jednostkowej wynika
  \(T_S(p) \in [0, 2]\) dla każdego dopuszczalnego \((p,\Delta p)\) —
  \(T_S\) nie tylko jest nieujemny (G3c), ale ma jawnie skończony,
  uniwersalny (niezależny od \(S\)) zakres.
- **(G8c) Ciągłość w granicy \(\Delta p \to 0\).** Jeśli \(n\) jest
  różniczkowalne w \(p\) (co zachodzi prawie wszędzie, G1b), to
  \(\lim_{\Delta p \to 0} T_S(p, \Delta p) = 0\) — zgodnie z G3b (brak
  przesunięcia = brak skrętu). Mocniej: dla małych \(\Delta p\),
  \(T_S\) jest różniczkowalny w \(\Delta p\) i jego rozwinięcie do
  pierwszego rzędu jest dane przez Aksjomat G9 poniżej.
- **(G8d) Stabilność (ograniczenie Lipschitza).** W punktach, gdzie
  krzywizna główna powierzchni jest ograniczona przez
  \(\kappa_{\max}(p) = \max(|\kappa_1(p)|, |\kappa_2(p)|)\) (G9),
  zachodzi \(T_S(p,\Delta p) \leq \kappa_{\max}(p)\cdot\|\Delta p\| +
  O(\|\Delta p\|^2)\) — \(T_S\) jest lokalnie Lipschitzowski w
  \(\Delta p\) ze stałą daną przez lokalną krzywiznę, nie dowolnie
  wrażliwy na wybór kroku dyskretyzacji. To czyni \(T_S\) właściwym
  kandydatem na operator numeryczny (na siatce), pod warunkiem że krok
  siatki jest mały względem \(1/\kappa_{\max}\) — warunek jawnie
  sprawdzalny, nie założony milcząco.

*(G8b-G8d są twierdzeniami wynikającymi z G1 + G3 + G9, nie nowymi
założeniami — dowody: G8b z nierówności trójkąta na \(\mathbb{S}^2\)
(elementarne); G8c-G8d z rozwinięcia Taylora pola normalnych, patrz
G9.)*

---

## Aksjomat G9 — Dyskretny operator Weingartena i jawna postać \(F\)

Ten aksjomat podaje jawną definicję \(W_S\) i funkcji \(F\) z G4b —
domykając kierunek wyznaczony przez G4, w zakresie opisanym w
zastrzeżeniu na końcu.

- **(G9a) Operator kształtu (Weingarten) w wersji różniczkowej.** Dla
  \(p \in S\) z płaszczyzną styczną \(T_pS\), klasyczny operator
  kształtu \(S_p: T_pS \to T_pS\) jest zdefiniowany jako
  \(S_p(v) = -D_v n(p)\) — ujemna pochodna kierunkowa pola normalnych
  wzdłuż \(v\). To jest standardowy obiekt geometrii różniczkowej
  (mapa Weingartena), nie nowa konstrukcja TIMDR: jego wartości własne
  są krzywiznami głównymi \(\kappa_1(p), \kappa_2(p)\), ślad daje
  krzywiznę średnią \(H=(\kappa_1+\kappa_2)/2\), wyznacznik daje
  krzywiznę Gaussa \(K=\kappa_1\kappa_2\).
- **(G9b) Dyskretna aproksymacja na siatce.** Dla powierzchni
  reprezentowanej jako siatka (wierzchołki/krawędzie/normalne
  wierzchołkowe lub facetowe), dyskretny operator kształtu w punkcie
  \(p\) wzdłuż krawędzi \(\Delta p\) jest aproksymowany różnicą
  skończoną, rzutowaną na płaszczyznę styczną:
  \[
  S_p^{\text{dysk}}(\Delta p) \approx
  \Pi_{T_pS}\!\left[\frac{n(p+\Delta p) - n(p)}{\|\Delta p\|}\right]
  \]
  gdzie \(\Pi_{T_pS}\) jest rzutem ortogonalnym na płaszczyznę styczną
  w \(p\). To jest standardowa konstrukcja różnic skończonych dla
  operatora Weingartena na siatkach (por. dyskretne operatory geometrii
  różniczkowej), nie coś specyficznego dla TIMDR — TIMDR jedynie
  wskazuje, że to jest wymagana definicja \(W_S\) z G4a.
- **(G9c) Jawna postać \(F\) domykająca G4b.** Z rozwinięcia Taylora
  pola normalnych do pierwszego rzędu:
  \[
  T_S(p) = \|n(p+\Delta p) - n(p)\| =
  \|\Delta p\| \cdot \|S_p(\widehat{\Delta p})\| + O(\|\Delta p\|^2)
  \]
  gdzie \(\widehat{\Delta p} = \Delta p / \|\Delta p\|\). To definiuje
  \(F\) z G4b jawnie:
  \[
  F(W_S)(p,\Delta p) := \|\Delta p\| \cdot \|S_p(\widehat{\Delta p})\|
  \]
  z \(T_S(p) = F(W_S)(p,\Delta p) + O(\|\Delta p\|^2)\).
- **(G9d) Ograniczenie przez krzywizny główne.** Ponieważ
  \(\|S_p(v)\| \leq \kappa_{\max}(p)\) dla jednostkowego \(v\) (z
  definicji wartości własnych), zachodzi
  \(T_S(p) \leq \kappa_{\max}(p)\cdot\|\Delta p\| + O(\|\Delta p\|^2)\)
  — dokładnie ograniczenie użyte w G8d.

*(**Zastrzeżenie o zakresie domknięcia.** G9a-G9d są wyprowadzeniem
analitycznym (tożsamość różniczkowo-geometryczna, prawdziwa w granicy
\(\Delta p \to 0\), oraz jej standardowa dyskretna aproksymacja różnicą
skończoną) — NIE są zaimplementowanym, przetestowanym kodem na
rzeczywistej siatce 3D, ani nie są zwalidowane empirycznie na
rzeczywistych danych geometrycznych. To domyka G4b **analitycznie**
(jawna postać \(F\) istnieje i jest standardowym obiektem geometrii
różniczkowej), ale G7's status "koncepcyjna" oraz wymagania G7c
(2)-(4) — formalna przestrzeń powierzchni, testy empiryczne, niezależna
walidacja — pozostają otwarte: patrz zaktualizowany Aksjomat G7.)*

---

## Aksjomat G10 — Parametr redukcji/rozwinięcia obwiedni \((P,Q)\)

Ten aksjomat formalizuje inny obiekt niż G3-G9: nie krzywiznę
**powierzchni** \(S\) (operator Weingartena \(W_S\), wartości własne
\(\kappa_1,\kappa_2\)), tylko krzywiznę **krzywej** — obwiedni
zbudowanej na trójkącie \(\Delta=(A,B,C)\) z G2. To rozróżnienie jest
takiej samej natury, co G3d/G6c (to samo słowo "krzywizna", inny obiekt
matematyczny) i musi być utrzymane: \(\kappa\) tutaj jest skalarną
krzywizną krzywej 1D, nie wartością własną \(W_S\).

- **(G10a) Konstrukcja: obwiednia zaokrąglona \(\partial_R(\Delta)\).**
  Dla trójkąta \(\Delta=(A,B,C)\) o kątach wewnętrznych
  \(\theta_1,\theta_2,\theta_3\) (\(\theta_1+\theta_2+\theta_3=\pi\)) i
  promieniu zaokrąglenia \(R \geq 0\), \(\partial_R(\Delta)\) jest
  standardową konstrukcją zaokrąglonego wielokąta (jak w CAD/geometrii
  obliczeniowej, nie nowość TIMDR): każdy wierzchołek zastąpiony łukiem
  stycznym do obu sąsiednich boków, promienia \(R\), boki skrócone o
  odcinki styczne \(t_i = R\cot(\theta_i/2)\) na każdym końcu.
  Konstrukcja jest dobrze określona (łuki się nie przecinają) dla
  \(R \in [0, R_{\max}(\Delta))\), gdzie
  \(R_{\max}(\Delta) = \min_{\{i,j\}} \dfrac{a_{ij}}{\cot(\theta_i/2)+\cot(\theta_j/2)}\)
  (minimum po trzech bokach \(a_{ij}\) — bok nie może zostać skrócony
  do długości ujemnej).

- **(G10b) Rozkład L0/Lk i parametr \((P,Q)\).** Obwiednia
  \(\partial_R(\Delta)\) rozkłada się jednoznacznie na część prostą
  (krzywizna \(\kappa=0\)) o łącznej długości \(L_0(R)\) i część
  łukową (krzywizna stała \(\kappa=1/R\)) o łącznej długości
  \(L_k(R)\), \(L(R)=L_0(R)+L_k(R)\). Definiujemy
  \[
  P(R) = \frac{L_0(R)}{L(R)}, \qquad Q(R) = \frac{L_k(R)}{L(R)} = 1-P(R).
  \]
  \(P\) mierzy udział części zredukowanej (rozwijalnej, płaskiej —
  "2D-jak"), \(Q\) udział części rozwiniętej (krzywoliniowej — o
  nieznikającej krzywiźnie).

- **(G10c) Jawna postać liniowa.** Z twierdzenia o sumie kątów
  zewnętrznych dowolnego wypukłego wielokąta (\(=2\pi\), fakt
  standardowy) wynika \(L_k(R) = 2\pi R\) **dokładnie**, niezależnie od
  kształtu \(\Delta\). Z G10a, \(L_0(R) = P_0 - 2Rc(\Delta)\), gdzie
  \(P_0\) jest obwodem \(\Delta\) i \(c(\Delta)=\sum_{i=1}^3\cot(\theta_i/2)\).
  Obie funkcje są więc afiniczne w \(R\); w szczególności
  \(L(R) = P_0 + 2R(\pi - c(\Delta))\).

- **(G10d) Monotoniczność i odwracalność (kierunek "i odwrotnie").**
  Ponieważ \(\cot(x/2)\) jest wypukła na \((0,\pi)\), z nierówności
  Jensena \(c(\Delta) \geq 3\sqrt3 > \pi\) dla każdego trójkąta (równość
  tylko dla \(\Delta_{\text{eq}}\), G2a) — więc \(L(R)\) jest ściśle
  malejąca. Bezpośredni rachunek (regułą ilorazu) daje
  \(dP/dR = -2(c(\Delta)L_k(R)+\pi L_0(R))/L(R)^2 < 0\) na całej
  dziedzinie \([0,R_{\max}(\Delta))\) poza punktem zerowym — \(P(R)\)
  jest więc **ściśle monotoniczna**, zatem odwracalna. To daje DWA
  kierunki przekształcenia, oba jawnie zdefiniowane na tej rodzinie:
  - **redukcja** (pomiar, "3D→2D" w sensie tego aksjomatu): krzywa
    \(\mapsto (P,Q)\), z G10b — ekstrakcja parametru z danej obwiedni;
  - **rozwinięcie** (konstrukcja, odwrotny kierunek — **"i
    odwrotnie"**): zadany \(P\in(P_{\min}(\Delta),1]\)
    \(\mapsto R=P^{-1}(P) \mapsto \partial_R(\Delta)\) — jednoznaczne
    odtworzenie obwiedni o zadanym stopniu "spłaszczenia", bo \(P(R)\)
    jest bijekcją na swojej dziedzinie (G10d); po poprawce G10e
    \(Q_{\max}(\Delta)=1\) dla KAŻDEGO \(\Delta\) (granica
    \(R\to R_{\max}\)), więc \(P_{\min}(\Delta)=0\) dla każdego
    trójkąta — patrz G10e za poprawną treścią.
  *(Zastrzeżenie o zakresie: ta odwracalność jest udowodniona dla TEJ
  KONKRETNEJ jednoparametrowej rodziny \(\{\partial_R(\Delta)\}_R\) przy
  ustalonym \(\Delta\), nie dla dowolnej krzywej o zadanym \(P\) — wiele
  różnych krzywych może mieć to samo \(P\), więc "odwrotność" poza tą
  rodziną wymaga dodatkowego wyboru/regularyzacji, nie jest tu
  twierdzona.)*

- **(G10e) \(R_{\max}(\Delta)=r_{\text{in}}(\Delta)\) dla KAŻDEGO
  trójkąta — poprawka wcześniejszej wersji tego punktu.** *(Ta wersja
  G10e zastępuje wcześniejszą z tej samej sesji, która twierdziła, że
  złamanie symetrii ścinało \(R_{\max}\) poniżej \(r_{\text{in}}\) —
  błąd znaleziony i naprawiony przy pisaniu przykładu liczbowego do
  `TIMDR_Gravity_Speculative.md`; szczegóły w dopisku na końcu tego
  punktu.)* Ze standardowej tożsamości stycznej-do-okręgu-wpisanego,
  \(\cot(\theta_i/2) = (s-a_i)/r_{\text{in}}\) (\(a_i\) = bok
  PRZECIWLEGŁY wierzchołkowi \(i\), \(s\) = półobwód), oraz z tożsamości
  \(a_{ij}=(s-a_i)+(s-a_j)\) (bok między wierzchołkami \(i,j\) jako suma
  dwóch stycznych z incentera) wynika dla KAŻDEGO boku:
  \[
  \frac{a_{ij}}{\cot(\theta_i/2)+\cot(\theta_j/2)}
  = \frac{a_{ij}\cdot r_{\text{in}}}{(s-a_i)+(s-a_j)}
  = \frac{a_{ij}\cdot r_{\text{in}}}{a_{ij}} = r_{\text{in}}(\Delta),
  \]
  identycznie dla wszystkich trzech boków — więc
  \(R_{\max}(\Delta)=\min\{r_{\text{in}},r_{\text{in}},r_{\text{in}}\}=r_{\text{in}}(\Delta)\)
  **dokładnie, dla dowolnego trójkąta**, nie tylko \(\Delta_{\text{eq}}\).
  Sumując te trzy tożsamości dodatkowo dostajemy
  \(c(\Delta)=\sum\cot(\theta_i/2)=s/r_{\text{in}}(\Delta)\) dokładnie,
  skąd \(L_0(R_{\max}) = P_0-2r_{\text{in}}c(\Delta) = 2s-2r_{\text{in}}\cdot(s/r_{\text{in}})=0\)
  — obwiednia degeneruje się DOKŁADNIE do okręgu wpisanego (\(P\to0\),
  \(Q\to1\) osiągalne w granicy \(R\to R_{\max}\)) **dla każdego
  trójkąta**, symetrycznego czy nie. Złamanie symetrii (G2b) NIE
  ogranicza więc osiągalny zakres \(Q\) tą drogą — to twierdzenie z
  wcześniejszej wersji tego punktu było błędne.

  Co POZOSTAJE prawdą i wynika wprost z G10d (nierówność Jensena,
  \(c(\Delta)\geq3\sqrt3\), równość tylko dla \(\Delta_{\text{eq}}\)):
  z \(c(\Delta)=s/r_{\text{in}}(\Delta)\) dostajemy
  \(r_{\text{in}}(\Delta)\leq s/(3\sqrt3)\), równość tylko dla
  \(\Delta_{\text{eq}}\) — czyli **przy ustalonym obwodzie \(P_0=2s\)**,
  trójkąt równoboczny ma NAJWIĘKSZY promień wpisany, więc NAJWIĘKSZY
  \(R_{\max}\) spośród wszystkich trójkątów o tym samym obwodzie.
  Złamanie symetrii nie blokuje więc Q=1 (osiągalne zawsze), tylko
  zmniejsza BEZWZGLĘDNY promień \(R\), przy którym to następuje, dla
  ustalonego obwodu — inna, słabsza, ale poprawna wersja "asymetria ma
  koszt".

  *(Dopisek o znalezieniu błędu: poprzednia wersja tego punktu twierdziła
  matematycznie fałszywy fakt, sprawdzony i naprawiony w tej samej
  sesji, w której dopisano `TIMDR_Gravity_Speculative.md` — przy próbie
  policzenia konkretnego przykładu liczbowego (trójkąt 3-4-5) okazało
  się, że \(R_{\max}=r_{\text{in}}=1\) i \(L_0(R_{\max})=0\) mimo że
  trójkąt jest ostro asymetryczny, co jest sprzeczne z wcześniejszym
  tekstem — stąd ręczne wyprowadzenie ogólnej tożsamości powyżej.
  Zachowane tu jawnie, zgodnie z konwencją tego repo ujawniania
  znalezionych błędów zamiast ich cichego poprawiania.)*

*(**Zastrzeżenie o statusie i o analogii z topologią.** (1) G10c-G10e
są rachunkiem wykonanym ręcznie w tej sesji (sumy kątów zewnętrznych,
wzór na długość odcinka stycznego, nierówność Jensena, zbieżność
środków łuków w incenterze) — sprawdzonym krok po kroku, ale NIE
zaimplementowanym ani przetestowanym numerycznie (ten sam status co
G8-G9, patrz zastrzeżenie tam i G7). (2) \(P,Q\) są parametrem
CIĄGŁYM (modułem geometrycznym, \(P\in[0,1]\)) — to inny TYP obiektu
niż rodzaj/genus (odróżniający torus od wstęgi Möbiusa) czy wymiar
sympleksu (odróżniający trójkąt-jako-2-sympleks od czworościanu-jako-
3-sympleksu), które są niezmiennikami DYSKRETNYMI, stałymi pod
homeomorfizmem — zaokrąglony trójkąt i ostry trójkąt są homeomorficzne
(oba to okrąg topologicznie), mimo różnego \(P\). Intuicja, która
zainspirowała ten aksjomat (jeden typ parametru rządzący przejściem
między jakościowo różnymi reżimami — tu: wielokątnym i gładkim) jest
tym, co G10 formalizuje; dosłowne utożsamienie z rodzajem/wymiarem
sympleksu byłoby nadinterpretacją i nie jest tu twierdzone. Jedyny
ścisły punkt styku z opisem sympleksowym: granica \(R\to0\) (\(P\to1\))
odtwarza dokładnie brzeg gołego 2-sympleksu (sam trójkąt, zero
krzywizny) — to jest właściwy, ograniczony sens, w jakim \(P\)
"dotyka" opisu kombinatorycznego.)*

---

## Aksjomat G5 — Brak operatora rezonansu geometrycznego (na tym etapie)

Gałąź geometryczna G **nie definiuje** własnego operatora rezonansu na
powierzchniach:

- **(G5a)** Nie istnieje w tym wydaniu formalny operator "rezonansu
  geometrycznego" analogiczny do rezonansu M w gałęzi sygnałowej.
- **(G5b)** Wszelkie użycie słowa "rezonans" w kontekście gałęzi G ma
  charakter metaforyczny lub koncepcyjny, nie formalny.
- **(G5c)** Próby zdefiniowania rezonansu geometrycznego muszą być
  jawnie oznaczone jako osobne rozszerzenie, nie część tego zestawu
  aksjomatów.

---

## Aksjomat G6 — Rozdział gałęzi G od M i K

- **(G6a)** Obiekty gałęzi G (trójkąt, powierzchnia, normalne, skręt
  powierzchniowy) nie są elementami przestrzeni sygnałów
  \(x:T\to\mathbb{R}^d\) ani modułów \((f,\phi,A)\).
- **(G6b)** Operatory gałęzi G (Λ, τ, ρ, J, \(T_S\), \(W_S\)) nie są
  rozszerzeniami ani szczególnymi przypadkami operatorów gałęzi M
  (anomalia, defekt, skręt sygnałowy, rezonans M) ani gałęzi K
  (rezonans modalny).
- **(G6c)** Wspólne słowa ("skręt", "rezonans") oznaczają różne
  obiekty w gałęziach G, M i K — nie różne poziomy tej samej teorii.

---

## Aksjomat G7 — Status gałęzi geometrycznej

- **(G7a)** Gałąź geometryczna G jest na tym etapie **koncepcyjna**:
  posiada obiekty, wzory i kierunki, ale nie pełną formalną teorię ani
  walidację empiryczną.
- **(G7b)** Wszelkie twierdzenia o fizycznej rzeczywistości,
  kosmologii, polach, czasie globalnym itp. w gałęzi G mają status
  **metafory strukturalnej**, nie teorii naukowej.
- **(G7c)** Rozszerzenie gałęzi G do pełnej teorii matematycznej
  wymaga: (1) pełnej definicji \(W_S\) — **domknięte analitycznie przez
  G8-G9 i zaimplementowane numerycznie w osobnym repo,
  `TIMDR-Geometry-Formalism`** (moduł `timdr_geometry/weingarten.py`:
  normalne wierzchołkowe, dyskretny operator kształtu metodą MNK na
  1-ringu, testy na płaszczyźnie/sferze/walcu/zbieżności siatki) — testy
  tego repo NIE były uruchomione w sesji, w której powstały (patrz
  zastrzeżenie w jego README), więc status pozostaje
  "zaimplementowane, nie potwierdzone wykonaniem", (2) formalnej przestrzeni powierzchni — otwarte, (3) testów
  empirycznych — otwarte (żaden z powyższych wzorów nie był
  uruchomiony na rzeczywistych danych geometrycznych; kontrast z
  gałęzią sygnałową M, gdzie realna walidacja już się odbyła —
  `TIMDR-Math-Formalism/docs/REAL_DATA_VALIDATION.md`), (4)
  niezależnej walidacji — otwarte.

---

## Mapowanie aksjomatów G na README / repo

| Aksjomat | Odniesienie |
|---|---|
| G1-G2 | Sekcja 1 głównego `README.md` GIA-TIMDR (model trójkąta, asymetria, impuls) |
| G3-G4 | Skręt powierzchniowy w `Resonance_M_Operator_Empiryczny.md` §6, plus sekcje o Mobiosotourys/Tetroidzie (README sekcja 6) |
| G5 | Wiersz "Operator rezonansu: brak" dla gałęzi G w tabeli "Trzy gałęzie TIMDR" (README) |
| G6 | Sekcja "🌿 Trzy gałęzie TIMDR — mapa terenu" w README |
| G7 | Ostrzeżenie na początku README ("model koncepcyjny / narzędzie do myślenia, nie teoria naukowa") |
| G8-G9 | Domykają analitycznie związek \(T_S = F(W_S)\) nazwany w G4 — patrz też `TIMDR_Branch_Specification.md` (gałąź G, sekcja operatorów) |
| G10 | Parametr redukcji/rozwinięcia \((P,Q)\) obwiedni trójkąta — nowy obiekt (krzywizna krzywej, nie powierzchni), powiązany z G2 (trójkąt; \(Q_{\max}=1\) dla KAŻDEGO trójkąta, poprawka G10e — symetria wpływa na bezwzględny \(R_{\max}=r_{\text{in}}\) przy ustalonym obwodzie, nie na osiągalność \(Q=1\)) i z rzutem G Chronoprocesu (`TIMDR_Chronoprocess.md` §3 — jeden generator \(\gamma_s\) rodziny \(\Gamma\) jako obwiednia) |

Powiązane: [`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md) (gałąź modalna),
[`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md) (gałąź
sygnałowa — sekcja "Pozostałe braki formalne" tam odnosi się wprost do
G4/G8/G9 powyżej), [`Resonance_M_Operator_Empiryczny.md`](./Resonance_M_Operator_Empiryczny.md)
§6 (pierwsze wprowadzenie \(T_S\), przed formalizacją jako G3, G8, G9),
[`TIMDR_Twists.md`](./TIMDR_Twists.md) (skonsolidowane formalne
definicje wszystkich czterech znaczeń "skrętu" w ekosystemie, w tym
skrętu powierzchniowego z G3/G8/G9), [`TIMDR_Branch_Specification.md`](./TIMDR_Branch_Specification.md)
(formalna specyfikacja trzech gałęzi TIMDR — źródło prawdy dla
podziału M/S, G, K), [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md) (kanoniczne nazwy
"skręt powierzchniowy" i rozgraniczenie od pozostałych trzech znaczeń
skrętu).
