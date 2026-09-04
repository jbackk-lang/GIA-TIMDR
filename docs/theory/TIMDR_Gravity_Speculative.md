# Grawitacja z (P,Q,M) — dokument spekulacyjny, POZA głównymi aksjomatami

> **STATUS: SPEKULACYJNY / EKSPLORACYJNY. Ten dokument NIE jest częścią
> aksjomatów Axioms_S/Axioms_G/Axioms_K i CELOWO łamie "zasadę
> nadrzędną" z `TIMDR_Branch_Specification.md` (gałęzie M/S, G, K nie są
> rozszerzeniami/przypadkami siebie nawzajem; jedyny dozwolony most to
> wąski, udowodniony most Fouriera M/S↔K, §5 `TIMDR_Chronoprocess.md`).
> To złamanie jest tu ŚWIADOME i JAWNE — ten plik nie zmienia ani nie
> osłabia tamtej zasady dla reszty teorii, jest odizolowaną eksploracją
> "co by było, gdyby ją odłożyć na bok". Nic stąd nie jest cytowane jako
> "domknięte" ani "sprawdzone" gdziekolwiek indziej w repo. Poziom
> pewności: **analogia strukturalna**, nie wyprowadzona fizyka — patrz
> §5 za listę tego, czego brakuje, żeby to zmienić.**

## 0. Punkt wyjścia

Wiadomość użytkownika zaproponowała: mając parametr przestrzeni
\((P,Q)\) (Aksjomat G10, `Axioms_G_TIMDR_Geometry.md`) i "parametry
czasu \(k_{MS},k_G,k_K\)" (po jednym na gałąź), złożyć je w tensor
\(\Omega=(P,Q)\otimes(k_{MS},k_G,k_K)\) i wprowadzić masę \(M\) (albo
gęstość \(\rho(x)\)) przez analogię do potencjału Newtonowskiego,
\(g \sim M\cdot\Omega\).

**Uczciwie od razu:** \(k_{MS},k_G,k_K\) NIE istniały nigdzie w repo
przed tym dokumentem — sprawdziłem `Axioms_S_TIMDR_Signal.md`,
`Axioms_G_TIMDR_Geometry.md`, `Axioms_K_TIMDR.md`,
`TIMDR_Chronoprocess.md`. Poniżej proponuję dla nich konkretne
definicje, zbudowane z obiektów, które JUŻ istnieją w Chronoprocesie
\(\Xi=(T,x,\Gamma,\phi)\) — ale to są propozycje z tej sesji, nie
odtworzenie czegoś ustalonego.

---

## 1. Przypomnienie: \((P,Q)\) z Aksjomatu G10

\(P=L_0/L\), \(Q=L_k/L=1-P\) — udział prostoliniowej vs łukowej części
obwiedni zaokrąglonego trójkąta \(\partial_R(\Delta)\). Ciągły,
skalarny parametr na \([0,1]\) (jeden stopień swobody: \(Q=1-P\)).
Pełna definicja: `Axioms_G_TIMDR_Geometry.md`, Aksjomat G10.

## 2. Propozycja: \(k_{MS}, k_G, k_K\) — "krzywizna czasu" per gałąź

Każde z trzech poniżej próbuje odpowiedzieć: "jak bardzo tempo tej
gałęzi PRZYSPIESZA/ZWALNIA (nie: jakie jest), analogicznie do tego jak
\(Q\) mierzy odejście od zerowej krzywizny przestrzennej" — czyli
druga, nie pierwsza pochodna względem \(T\) z Chronoprocesu.

- **\(k_{MS}\) — z tempa/driftu (§2 Chronoprocesu).**
  \(\text{tempo}(t)=t[i{+}1]-t[i]\), \(\text{drift}(t)=\text{tempo}_{\text{zmierzone}}-\text{tempo}_{\text{nominalne}}\)
  już istnieją. Propozycja: \(k_{MS}(t) := \text{drift}(t{+}1)-\text{drift}(t)\)
  — dyskretna DRUGA różnica indeksu czasowego względem nominału, czyli
  "przyspieszenie zegara" gałęzi M/S. Zero nowych aksjomatów Axioms_S
  — czysta funkcja istniejącego \(x:T\to\mathbb{R}^d\) (Aksjomat 1
  tamtej gałęzi).

- **\(k_G\) — z kongruencji \(\Gamma(t,s)\) (§3 Chronoprocesu).**
  §3 Chronoprocesu **jawnie mówi**, że rozkład ekspansji/ścinania/skrętu
  \(\theta/\sigma/\omega\) (Raychaudhuri) "NIE jest zaimplementowany ani
  wyprowadzony — to była wskazana analogia". Zamiast go tu implementować
  (co byłoby nieuczciwe — dokładnie ten sam błąd, przed którym ostrzega
  ten fragment), proponuję słabszy, ale już dostępny proxy: średnia
  krzywizna \(H(p)=(\kappa_1(p)+\kappa_2(p))/2\) powierzchni
  \(S=\Gamma(T\times I)\) (z operatora Weingartena, Aksjomat G9a) ZMIENIA
  SIĘ wzdłuż \(T\) — \(k_G(t) := \partial H/\partial t\) wzdłuż \(\Gamma\).
  To NIE jest ekspansja Raychaudhuriego (inny obiekt), tylko coś, co da
  się faktycznie policzyć z tego, co G8-G9 już definiują — jeśli i kiedy
  ktoś doda \(\theta\), to będzie osobna, lepsza kandydatka.

- **\(k_K\) — z mapy synchronizacji fazy \(f\) (§4 Chronoprocesu).**
  \(t_{\text{lokalne}}=f(\tau_{\text{globalne}})\) jest, pod Aksjomatami
  K3/K4 (oscylator o STAŁYCH parametrach), funkcją **afiniczną** w
  \(\tau_{\text{globalne}}\) — §4 Chronoprocesu mówi to wprost
  ("Granica zakresu: ta mapa jest AFINICZNA"). Naturalna propozycja
  \(k_K := d^2f/d\tau^2\) jest wtedy **tożsamościowo zero** pod
  obecnymi aksjomatami K. To nie jest luka w tym dokumencie — to
  poprawny, uczciwy wniosek z tego, co K3/K4 już zakładają: dopóki K nie
  zostanie rozszerzone o dynamikę sprzężenia (§4 Chronoprocesu: "wymagałoby
  rozszerzenia Axioms_K_TIMDR.md o dynamikę sprzężenia — jawnie NIE
  zrobione tutaj"), \(k_K\equiv 0\).

*(Status: wszystkie trzy są propozycjami z tej sesji, żadna nie jest
zaimplementowana ani przetestowana numerycznie. \(k_K\equiv0\) jest
wyprowadzonym faktem pod obecnymi aksjomatami K, nie założeniem.)*

## 3. Tensor \(\Omega\) — jawna postać

\((P,Q)\) jest 2-wektorem, \((k_{MS},k_G,k_K)\) 3-wektorem — ich
iloczyn tensorowy jest jednoznacznie macierzą \(2\times3\), nie
wektorem:
\[
\Omega = (P,Q)\otimes(k_{MS},k_G,k_K) =
\begin{pmatrix} P\,k_{MS} & P\,k_G & P\,k_K \\ Q\,k_{MS} & Q\,k_G & Q\,k_K \end{pmatrix}
\]
Z §2, kolumna \(k_K\) jest obecnie tożsamościowo zerowa (pod K3/K4) —
\(\Omega\) ma efektywnie 4, nie 6, niezależnych składowych dzisiaj.

**Problem, który trzeba nazwać wprost:** prawdziwe pole grawitacyjne
\(g(x)\) jest 3-wektorem (albo w OTW: tensorem o określonej walencji w
4D). \(\Omega\) powyżej jest macierzą \(2\times3\) — inny kształt.
\(g\sim M\cdot\Omega\) NIE ma zgodnych wymiarów/rzędu tensora tak, jak
jest napisane; potrzebna byłaby jawna mapa kontrakcji
\(\pi:\mathbb{R}^{2\times3}\to\mathbb{R}^3\) (np. suma po wierszach,
albo wybrany rzut), której wyboru ten dokument NIE rozstrzyga — to
otwarta decyzja modelowa, nie szczegół techniczny do pominięcia.

## 3a. Przykład liczbowy (syntetyczny)

Cel: policzyć \(\Omega\) i \(g\sim M\cdot\Omega\) na konkretnych,
zmyślonych liczbach — pokazać, że wzór daje się w ogóle policzyć i że
"reaguje" na \(M\), a jednocześnie pokazać wprost, czego taki rachunek
NIE dowodzi. Wszystkie liczby poniżej są syntetyczne (zmyślone do tego
przykładu), nie pochodzą z żadnego pomiaru.

**Krok 1 — \((P,Q)\) z konkretnego trójkąta (Aksjomat G10).** Trójkąt
3-4-5 (boki \(a{=}3,b{=}4,c{=}5\), kąt prosty przy wierzchołku
naprzeciw boku \(c\)) — jawnie asymetryczny (G2b), obwód
\(P_0{=}12\), \(c(\Delta){=}\sum\cot(\theta_i/2)=3.0{+}2.0{+}1.0=6.0\)
(policzone z \(\cot(\theta/2)=(1{+}\cos\theta)/\sin\theta\) dla każdego
kąta), pole \(=6\), półobwód \(s{=}6\), więc
\(r_{\text{in}}=6/6=1.0=R_{\max}(\Delta)\) (Aksjomat G10e, poprawiona
wersja — patrz `Axioms_G_TIMDR_Geometry.md`). Biorę \(R{=}0.4\)
(dowolny punkt wewnątrz \([0,R_{\max})\), nie brzeg):
\[
L_0(0.4)=12-2(0.4)(6)=7.2,\quad L_k(0.4)=2\pi(0.4)=2.5133,\quad L=9.7133
\]
\[
P = 7.2/9.7133 = 0.7412, \qquad Q = 2.5133/9.7133 = 0.2588
\]

**Krok 2 — \((k_{MS},k_G,k_K)\) syntetyczne (§2 powyżej).**
\(k_{MS}{=}0.10\) (zmyślona wartość drugiej różnicy driftu, jednostka
1/krok²), \(k_G{=}0.03\) (zmyślona wartość \(\partial H/\partial t\),
jednostka 1/długość/krok), \(k_K{=}0\) (NIE zmyślone — wyprowadzone w
§2, tożsamościowo zero pod K3/K4).

**Krok 3 — \(\Omega\) (macierz \(2\times3\), §3):**
\[
\Omega = \begin{pmatrix} 0.7412{\times}0.10 & 0.7412{\times}0.03 & 0 \\ 0.2588{\times}0.10 & 0.2588{\times}0.03 & 0 \end{pmatrix}
= \begin{pmatrix} 0.07412 & 0.02224 & 0 \\ 0.02588 & 0.00776 & 0 \end{pmatrix}
\]

**Krok 4 — dlaczego "najprostsza" kontrakcja jest zwodnicza.** Naiwna
próba: zsumować WSZYSTKIE 6 wpisów \(\Omega\), żeby dostać jedną liczbę.
\[
\textstyle\sum_{ij}\Omega_{ij} = (P{+}Q)(k_{MS}{+}k_G{+}k_K) = 1\times(0.10{+}0.03{+}0) = 0.13
\]
— **bo \(P+Q\equiv1\) zawsze** (G10b), ta suma NIE ZALEŻY od \(P,Q\) w
ogóle — wyszłoby dokładnie to samo \(0.13\) dla DOWOLNEGO trójkąta,
dowolnego \(R\). Ta "najprostsza" kontrakcja kasuje dokładnie tę
informację geometryczną, po którą sięgnięto po \((P,Q)\) w pierwszej
kolejności. To nie jest szczegół techniczny — to konkretny dowód, że
wybór mapy kontrakcji \(\pi\) (§3) realnie zmienia, czy \(\Omega\) w
ogóle coś niesie, więc nie da się go pominąć milczeniem.

**Krok 5 — jedna, jawnie ARBITRALNA kontrakcja, tylko do tej
ilustracji.** Biorę tylko wiersz \(Q\) (część "rozwiniętą/zakrzywioną"
— wybór uzasadniony wyłącznie tym, że \(Q\) jest w tej narracji bliżej
"krzywizny", nie żadnym wyprowadzeniem):
\[
v = Q\cdot(k_{MS},k_G,k_K) = (0.02588,\ 0.00776,\ 0)
\]

**Krok 6 — \(g\sim M\cdot\Omega\) (tu: \(M\cdot v\)) dla dwóch mas:**

| \(M\) | \(g\) (3 składowe) | \(\lVert g\rVert\) |
|---|---|---|
| 1 | \((0.02588,\ 0.00776,\ 0)\) | 0.0270 |
| 10 | \((0.2588,\ 0.0776,\ 0)\) | 0.2702 |

\(\lVert g\rVert\) rośnie dokładnie 10-krotnie przy \(M\times10\) —
**ale to jest trywialne**: \(g=M\cdot v\) jest z definicji liniowe w
\(M\), bo tak to zapisano, nie dlatego że coś zostało wyprowadzone czy
zaobserwowane. Dowolna funkcja postaci "stała razy \(M\)" ma tę samą
własność.

**Krok 7 — co ten przykład POKAZUJE, a czego nie.** Pokazuje: (a)
\(\Omega\) i \(g\sim M\cdot\Omega\) dają się policzyć na konkretnych
liczbach, bez sprzeczności wewnętrznej; (b) wybór kontrakcji \(\pi\)
naprawdę ma znaczenie (Krok 4) — nie jest to pomijalny szczegół
techniczny z §3, tylko coś, co przy złym wyborze niszczy sens całej
konstrukcji. NIE pokazuje: (i) że \(g\) zależy od ODLEGŁOŚCI od masy —
w przeciwieństwie do \(g(x)\) Newtona, powyższy wzór nie zawiera
ŻADNEJ współrzędnej przestrzennej \(x\) ani \(x'\) (\(\Omega\) zależy
tylko od trójkąta \(\Delta\), promienia \(R\) i lokalnych
\(k_{MS},k_G,k_K\) w jednym wybranym punkcie procesu) — brak
mechanizmu odpowiadającego \(1/\lVert x-x'\rVert\) jest konkretnym,
znalezionym w tym ćwiczeniu brakiem, nie tylko abstrakcyjną uwagą; (ii)
superpozycji wielu mas (\(\int\rho(x')\,d^3x'\) w całce Newtona sumuje
WKŁADY z różnych miejsc — tu nie ma dla tego odpowiednika); (iii)
żadnych jednostek fizycznych łączących \(k_{MS},k_G,k_K,M\) z realnym
przyspieszeniem grawitacyjnym [m/s²]. Liniowość w \(M\) w Kroku 6 jest
więc najsłabszym możliwym testem — potwierdza tylko, że mnożenie
działa tak, jak zapisano.

## 4. Analogia grawitacyjna — co to jest, a czego NIE jest

Klasyczna grawitacja Newtonowska:
\[
\Phi(x) = -G\!\int\!\frac{\rho(x')}{\|x-x'\|}\,d^3x', \qquad g(x)=-\nabla\Phi(x)
\]
wynika z konkretnego prawa (odwrotność kwadratu odległości), które z
kolei wynika z równania Poissona \(\nabla^2\Phi=4\pi G\rho\) — pochodzącego
z liniowej granicy równań pola Einsteina. Propozycja \(g\sim M\cdot\Omega\)
**nie wynika z żadnego z powyższych** — jest to zapisanie "coś
proporcjonalnego do masy razy nasz tensor" PO WZORZE strukturalnym
Newtona, nie wyprowadzenie z zasady wariacyjnej, równania pola, ani
z jakiejkolwiek dynamiki. To jest uczciwa różnica między "wygląda jak"
a "jest".

**Czego brakuje, żeby to były prawdziwe równania pola (nie tylko
zapis), zgodnie z tym, jak ten projekt już testuje takie hipotezy
(patrz skill `timdr-signal-framework`, protokół numerologii/formalizmu):**

1. **Jednostki/wymiary.** \(P,Q\) są bezwymiarowe (stosunek długości);
   \(k_{MS},k_G,k_K\) mają wymiary zależne od propozycji w §2 (np.
   \(k_{MS}\) — [czas]\(^{-1}\) w dyskretnych krokach, \(k_G\) —
   [długość]\(^{-1}\)[czas]\(^{-1}\)) — nie zgadzają się ze sobą ani z
   przyspieszeniem grawitacyjnym [długość][czas]\(^{-2}\) bez
   dodatkowej stałej wymiarowej (odpowiednika \(G\)), której tu nie ma.
2. **Zasada wariacyjna albo równanie pola.** Prawdziwa teoria
   grawitacji potrzebuje albo działania \(S[\cdot]\), z którego \(g\)
   wypada przez zasadę najmniejszego działania, albo bezpośredniego
   równania różniczkowego wiążącego \(\Omega\) ze źródłem \(\rho\) —
   \(g\sim M\cdot\Omega\) jest ani jednym, ani drugim, jest tylko
   przypisaniem wartości.
3. **Co najmniej jedna odróżniająca predykcja.** Musiałoby istnieć
   COŚ, co ta konstrukcja przewiduje INACZEJ niż Newton/OTW — inaczej
   nie da się jej odróżnić od zwykłej grawitacji nawet w zasadzie, a
   "nieodróżnialne od istniejącej teorii" nie jest fałszywe, ale też
   nic nie tłumaczy ponad to, co Newton już tłumaczy.
4. **Kontrola negatywna/pozytywna na sztucznych danych**, dokładnie w
   duchu protokołu numerologii z `timdr-signal-framework` (§13/§15 tego
   skilla) — zanim jakiekolwiek twierdzenie "\(\Omega\) koreluje z
   czymkolwiek fizycznym" zostanie potraktowane poważnie, powinno przejść
   te same testy (pre-rejestracja, kontrola pozytywna/negatywna,
   niezależna baza), które ten projekt stosuje już w gałęzi M/S
   (`REAL_DATA_VALIDATION.md`).

## 5. Relacja do zasady nieredukowalności gałęzi

`TIMDR_Branch_Specification.md`, "Zasada nadrzędna": gałęzie M/S, G, K
nie są rozszerzeniami/przypadkami siebie nawzajem; jedyny wyjątek to
most Fouriera M/S↔K (`TIMDR_Chronoprocess.md` §5), uzasadniony
KONKRETNĄ, znaną tożsamością matematyczną (zasada nieoznaczoności
Gabora = Heisenberga), nie ogólną analogią strukturalną.

\(\Omega\) w tym dokumencie łączy WSZYSTKIE TRZY gałęzie naraz przez
iloczyn tensorowy — to jest dokładnie ten typ konstrukcji, przed którą
zasada nadrzędna ostrzega, i nie ma tu odpowiednika mostu Fouriera
(żadnej znanej tożsamości matematycznej uzasadniającej *dlaczego* akurat
iloczyn tensorowy \((P,Q)\otimes(k_{MS},k_G,k_K)\), a nie inna
kombinacja). **Ten dokument istnieje mimo to, jawnie oznaczony jako
poza aksjomatami** — nie modyfikuje `TIMDR_Branch_Specification.md` ani
żadnego pliku `Axioms_*`, i żaden z nich nie powinien go cytować jako
uzasadnienie złamania zasady nieredukowalności.

---

Powiązane: [`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md)
(Aksjomat G10, źródło \((P,Q)\)), [`TIMDR_Chronoprocess.md`](./TIMDR_Chronoprocess.md)
(§2-§4, źródło obiektów użytych do zdefiniowania \(k_{MS},k_G,k_K\)),
[`TIMDR_Branch_Specification.md`](./TIMDR_Branch_Specification.md)
(zasada nadrzędna, którą ten dokument świadomie i jawnie łamie), skill
`timdr-signal-framework` §13/§15 (protokół testowania, czy wzorzec
numerologiczny/strukturalny jest realną matematyką czy artefaktem —
zalecany następny krok przed dalszym rozwijaniem tego pomysłu).
