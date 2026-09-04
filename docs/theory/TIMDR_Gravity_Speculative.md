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
  zrobione tutaj"), \(k_K\equiv 0\). \(k_K\equiv0\) nie jest brakiem
  teorii, lecz konsekwencją aksjomatów K3/K4 — modalność TIMDR jest z
  definicji afiniczna. Nie "brakuje" tu modalnej krzywizny czasu — ona
  po prostu nie istnieje w tej teorii, dopóki K3/K4 się nie zmienią.

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
\(k_{MS}{=}0.10\) (zmyślona wartość drugiej różnicy driftu; jednostka
**poprawiona w §4a poniżej** — to [czas]/[krok]², NIE 1/krok² jak
błędnie napisano tu wcześniej, bo drift sam niesie jednostkę czasu),
\(k_G{=}0.03\) (zmyślona wartość \(\partial H/\partial t\), jednostka
1/długość/krok), \(k_K{=}0\) (NIE zmyślone — wyprowadzone w §2,
tożsamościowo zero pod K3/K4).

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
działa tak, jak zapisano. Brak zależności od odległości
(\(1/\lVert x-x'\rVert\)) jest fundamentalny — bez niego konstrukcja
nie może być grawitacją w sensie Newtona ani OTW, niezależnie od tego,
jak zostanie ostatecznie rozwiązana kwestia kontrakcji z §3.

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
   \(k_{MS},k_G,k_K\) mają wymiary zależne od propozycji w §2, i nie
   zgadzają się ze sobą ani z przyspieszeniem grawitacyjnym
   [długość][czas]\(^{-2}\) bez dodatkowej stałej wymiarowej
   (odpowiednika \(G\)), której tu nie ma — pełne rozwinięcie, ze
   stałymi skalującymi \(\alpha_T,\alpha_L,\alpha_E\), jest w **§4a
   poniżej** (dodane po propozycji użytkownika, żeby to nie było już
   tylko jednym zdaniem).
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

## 4a. Jednostki i skalowanie (Units and scaling)

**Stan obecny, wprost:** wszystkie liczby w §3a (\(P,Q,k_{MS},k_G,k_K,
g,\lVert g\rVert\)) są **bezwymiarowe / w jednostkach modelowych**.
Żadna z nich nie jest metrem, sekundą ani dżulem. To nie jest
przeoczenie odkryte teraz — §4 punkt 1 mówił to już wcześniej jednym
zdaniem; ta sekcja rozwija to zdanie w konkretny, używalny aparat, wg
propozycji użytkownika.

**Trzy stałe skalujące — odpowiedniki \(c,h,G\) dla tego dokumentu.**
Chronoprocess \(\Xi=(T,x,\Gamma,\phi)\) liczy w krokach i jednostkach
modelowych, nie w SI. Żeby przejść z modelu do fizyki, potrzebne są
trzy niezależne stałe (żadna nie wynika z dotychczasowych aksjomatów —
każda musiałaby zostać wybrana lub skalibrowana):

| stała | jednostka | definiuje |
|---|---|---|
| \(\alpha_T\) | [s/krok] | \(T_{\text{fiz}} = \alpha_T\cdot T\) |
| \(\alpha_L\) | [m/jednostka\_modelowa] | \(x_{\text{fiz}} = \alpha_L\cdot x\) |
| \(\alpha_E\) | [J·m] | \(E_{\text{fiz}} = \alpha_E\cdot|\tau|\) (dla wielkości typu skręt/energia) |

**Zastosowanie do wielkości z §2-§3a, jedna po drugiej:**

- **\(T\) (indeks Chronoprocesu).** Wprost \(T_{\text{fiz}}=\alpha_T
  \cdot T\). Bez tego \(T\) jest liczbą kroków, nie czasem.

- **\((P,Q)\).** Już bezwymiarowe (stosunek dwóch długości obwiedni,
  §1) — **nie potrzebują żadnej stałej skalującej**, i to jest jedyna
  wielkość w \(\Omega\), która zostaje niezmieniona przy przejściu do
  fizyki. Warto to podkreślić dla kontrastu: \((P,Q)\) są "bezpieczne"
  wymiarowo, \((k_{MS},k_G,k_K)\) nie są.

- **\(k_{MS}\).** Zbudowane z \(\text{tempo}(t)=t[i{+}1]-t[i]\) i
  \(\text{drift}=\text{tempo}_{\text{zmierzone}}-\text{tempo}_{\text{nominalne}}\)
  (§2), gdzie \(\Delta(\text{krok})\equiv1\) z definicji. Skalowanie
  \(t\to\alpha_T\cdot t\) przenosi się liniowo:
  \(\text{tempo}_{\text{fiz}}=\alpha_T\cdot\text{tempo}_{\text{model}}\),
  \(\text{drift}_{\text{fiz}}=\alpha_T\cdot\text{drift}_{\text{model}}\),
  i \(k_{MS}\) jako DRUGA różnica driftu po kroku:
  \[
  k_{MS,\text{fiz}} = \alpha_T\cdot k_{MS,\text{model}}, \qquad
  [k_{MS,\text{fiz}}] = \text{s}/\text{krok}^2
  \]
  — to poprawia jednostkę zapisaną (błędnie) w §3a Krok 2 jako
  "1/krok²"; poprawna jednostka to [czas]/[krok]², dokładnie jak
  zauważył użytkownik.

- **\(k_G\).** Zbudowane z \(H=(\kappa_1+\kappa_2)/2\) (krzywizna
  średnia, [1/długość]) i \(\partial H/\partial t\) (§2). Skalowanie
  długości \(x\to\alpha_L\cdot x\) daje \(H_{\text{fiz}}=H_{\text{model}}
  /\alpha_L\) (krzywizna to odwrotność długości — skaluje się
  odwrotnie), a skalowanie czasu jak wyżej:
  \[
  k_{G,\text{fiz}} = \frac{k_{G,\text{model}}}{\alpha_L\cdot\alpha_T},
  \qquad [k_{G,\text{fiz}}] = \frac{1}{\text{m}\cdot\text{s}}
  \]

- **\(k_K\equiv0\).** Skalowanie nie zmienia zera — pozostaje
  tożsamościowo zero niezależnie od \(\alpha_T,\alpha_L,\alpha_E\)
  (konsekwencja K3/K4, §2, nie skalowania).

- **\(g\sim M\cdot\Omega\) (Krok 6, §3a).** Wartości \(\lVert g\rVert=
  0.0270\) / \(0.2702\) w tabeli §3a są **modelowe**, nie [m/s²]. Żeby
  je zinterpretować fizycznie, trzeba by najpierw ustalić, którą z
  \(\alpha_T,\alpha_L,\alpha_E\) (albo jaką ich kombinację) przypisać
  masie \(M\) i kontrakcji \(\pi\) z §3 — to NIE jest zrobione tutaj;
  bez tego kroku \(g_{\text{fiz}}\) nie jest zdefiniowane, tylko
  \(g_{\text{model}}\) jest.

**Dlaczego \(\alpha_T\) źle dobrane daje \(10^{31}\) Hz — nie bug, wybór
skali.** Jeśli częstotliwość liczy się jako \(f\sim1/\Delta T\) z
niezeskalowanym krokiem modelowym, a potem próbuje się ją
zinterpretować fizycznie przez \(f_{\text{fiz}}=1/(\alpha_T\cdot\Delta
T)\) z bardzo małym \(\alpha_T\) (np. \(10^{-35}\) s/krok — rząd czasu
Plancka, wybrany bez uzasadnienia), wynik rzędu \(10^{31}\) Hz jest
ARYTMETYCZNIE POPRAWNY, tylko \(\alpha_T\) było nieskalibrowane. To
dokładnie ta sama sytuacja, co \(\sim10^{31}\) Hz w
`genertor-fotonow/foton.py` (patrz
`genertor-fotonow/theory/dimensional-analysis.md` §4) — dwa niezależne
dokumenty, ten sam mechanizm: brak skalowania czasu, nie błąd w kodzie
czy w tym dokumencie.

**Dlaczego wielkość typu "\(|τ|\cdot0.001\)" nie jest energią.** Analogicznie:
dopóki nie wprowadzi się \(\alpha_E\) [J·m] i nie napisze
\(E_{\text{fiz}}=\alpha_E\cdot|\tau|\), wyrażenie \(|\tau|\cdot0.001\)
(gdziekolwiek by się pojawiło — w tym dokumencie żadna taka wielkość
jeszcze nie jest liczona, ale mechanizm dotyczy każdej przyszłej próby
zapisania czegoś jako "energię" z \(k_{MS},k_G,k_K\) czy z \(g\)) ma co
najwyżej wymiar tego, z czego jest zbudowane (np. [1/m] jeśli \(\tau\)
jest krzywizną/skrętem) razy liczba bezwymiarowa — czyli **gęstość
krzywizny, nie energię**, dopóki \(\alpha_E\) nie zostanie jawnie
podane.

**Zastrzeżenie uczciwości (wzorem reszty dokumentu).** Wprowadzenie
\(\alpha_T,\alpha_L,\alpha_E\) czyni model **wymiarowo poprawnym**, ale
**nie czyni go fizycznie prawdziwym**. Same stałe nie są tu
skalibrowane do niczego — dopóki nie ma niezależnego pomiaru
wiążącego \(T,x,\Omega\) z rzeczywistą obserwacją, wartości
\(\alpha_T,\alpha_L,\alpha_E\) można dobrać tak, by \(f_{\text{fiz}}\)
czy \(E_{\text{fiz}}\) wyszły w dowolnym z góry upatrzonym zakresie —
to jest dokładnie ryzyko numerologii, przed którym ostrzega protokół w
skillu `timdr-signal-framework` (§2: "freeze parameters before seeing
the result"). Wprowadzenie stałych bez kalibracji jest więc
warunkiem KONIECZNYM do fizycznej interpretacji, ale nie
WYSTARCZAJĄCYM.

**Decyzja (2026-09-04): wybór (b) — realna interpretacja fizyczna.**
Użytkownik wybrał: \(\alpha_T,\alpha_L,\alpha_E\) dostają konkretne
wartości, nie zostają symbolami.

**Wybrane kotwice — WYBRANE, nie zmierzone.** Żeby uniknąć
patologicznego wyniku z przykładu wyżej (np. \(\alpha_T{=}10^{-35}\)
s/krok → \(10^{31}\) Hz), wybieram najprostszą możliwą kotwicę, bez
ukrytego rzędu wielkości:
\[
\alpha_T = 1\ \text{s/krok}, \qquad \alpha_L = 1\ \text{m/jednostka\_modelowa}
\]
"1 krok = 1 sekunda, 1 jednostka modelowa = 1 metr" — to świadomie
NEUTRALNY wybór (mnożnik 1, nie ukrywa żadnej decyzji o skali), zrobiony
PO to, żeby liczby wylądowały w ludzkim zakresie, a nie dlatego że ktoś
to zmierzył. Epistemicznie to dokładnie ten sam typ kroku co
\(\kappa_{\text{twist}}\) w `genertor-fotonow` (§5 tamtego dokumentu):
jawnie oznaczona konwencja, zero potwierdzenia eksperymentalnego.

\(\alpha_E\) **nie dostaje wartości** — w tym dokumencie nie istnieje
żadna wielkość typu \(|\tau|\) (energia/skręt), do której miałaby się
przyłożyć (w przeciwieństwie do `genertor-fotonow`, gdzie
`energia_pola()` istnieje). Wymuszenie jakiejś wartości \(\alpha_E\)
bez punktu zaczepienia byłoby dokładnie ryzykiem numerologii
opisanym wyżej — więc zostaje nieprzypisana, do rewizji, jeśli/gdy
\(\Omega\) dostanie kiedyś jawną wielkość energetyczną.

**Przeliczenie §3a Kroki 2-6 na te kotwice:**

| wielkość (model) | wzór przeliczenia | wartość fizyczna |
|---|---|---|
| \(T\) | \(T_{\text{fiz}}=\alpha_T\cdot T\) | 1:1, w sekundach |
| \(k_{MS}=0.10\) | \(\alpha_T\cdot k_{MS}\) | \(0.10\ \text{s}^{-1}\) |
| \(k_G=0.03\) | \(k_G/(\alpha_L\alpha_T)\) | \(0.03\ \text{m}^{-1}\text{s}^{-1}\) |
| \(g\) (\(M{=}1\)) | \((\alpha_L/\alpha_T^2)\cdot g_{\text{model}}\) | \(\lVert g\rVert=0.0270\ \text{m/s}^2\) |
| \(g\) (\(M{=}10\)) | \((\alpha_L/\alpha_T^2)\cdot g_{\text{model}}\) | \(\lVert g\rVert=0.2702\ \text{m/s}^2\) |

Interpretując \(g\) jako analog przyspieszenia grawitacyjnego
(§4, wzorem Newtona), \(0.027\)-\(0.27\ \text{m/s}^2\) to rząd wielkości
mniejszy niż \(g_{\text{Ziemia}}=9.8\ \text{m/s}^2\) o czynnik
\(\sim\!36$-$360\) — liczba w rozsądnym, nie-absurdalnym zakresie
(porównywalna np. do przyspieszeń pływowych albo czułości dobrego
akcelerometru), ale **to jest artefakt wyboru \(\alpha_T{=}\alpha_L{=}1\),
nie predykcja** — przy innej (równie niezmierzonej) kotwicy wyszłaby
inna liczba, tak samo "rozsądna" albo nie.

**Co ta decyzja ZMIENIA, a czego NIE.** Zmienia: liczby w §3a mają
teraz jednostki SI, nie są gołymi floatami. Nie zmienia: \(\alpha_T,
\alpha_L\) same są niekalibrowane (żaden pomiar ich nie ustalił);
\(g\sim M\cdot\Omega\) dalej nie ma równania pola ani zasady
wariacyjnej (§4 pkt 2); dalej nie ma odróżniającej predykcji od
Newtona/OTW (§4 pkt 3); dalej nie przeszło żadnej kontroli
pozytywnej/negatywnej (§4 pkt 4). Status z nagłówka dokumentu
("analogia strukturalna, nie wyprowadzona fizyka") **pozostaje
prawdziwy** — wybór (b) czyni model wymiarowo mówiącym, nie
zweryfikowanym; to dokładnie rozróżnienie z akapitu
"Zastrzeżenie uczciwości" wyżej, teraz zastosowane, nie tylko
zapowiedziane.

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
kombinacja). Iloczyn tensorowy \((P,Q)\otimes(k_{MS},k_G,k_K)\) nie ma
odpowiednika w znanej tożsamości matematycznej, dlatego nie może pełnić
roli "mostu" analogicznego do Fouriera — most Fouriera jest most
DWÓCH gałęzi uzasadniony jedną konkretną, sprawdzoną tożsamością
(Gabor=Heisenberg); \(\Omega\) jest złożeniem TRZECH gałęzi bez żadnej
takiej tożsamości za sobą. To zamyka temat zasady nadrzędnej: \(\Omega\)
nie jest i nie może być traktowany jako drugi sankcjonowany most.

**Ten dokument istnieje mimo to, jawnie oznaczony jako
poza aksjomatami** — nie modyfikuje `TIMDR_Branch_Specification.md` ani
żadnego pliku `Axioms_*`, i żaden z nich nie powinien go cytować jako
uzasadnienie złamania zasady nieredukowalności.

## 6. Dlaczego to jest tylko analogia

TIMDR-Gravity (\(g\sim M\cdot\Omega\), §3-§4 powyżej) jest modelem
strukturalnym, nie teorią fizyczną — nie posiada równania pola,
jednostek ani dynamiki. Wszystko, co ten dokument dodaje ponad to
zdanie (§3a, §4), jest rozwinięciem TEGO ograniczenia na konkretnych
liczbach i konkretnej liście braków, nie próbą jego obejścia.

---

Powiązane: [`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md)
(Aksjomat G10, źródło \((P,Q)\)), [`TIMDR_Chronoprocess.md`](./TIMDR_Chronoprocess.md)
(§2-§4, źródło obiektów użytych do zdefiniowania \(k_{MS},k_G,k_K\)),
[`TIMDR_Branch_Specification.md`](./TIMDR_Branch_Specification.md)
(zasada nadrzędna, którą ten dokument świadomie i jawnie łamie), skill
`timdr-signal-framework` §13/§15 (protokół testowania, czy wzorzec
numerologiczny/strukturalny jest realną matematyką czy artefaktem —
zalecany następny krok przed dalszym rozwijaniem tego pomysłu).
