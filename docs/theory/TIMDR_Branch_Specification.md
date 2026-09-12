# TIMDR Branch Specification — formalna specyfikacja trzech gałęzi TIMDR

**Status:** dokument-indeks, źródło prawdy dla podziału "co formalnie
znaczy TIMDR" w tym repo. Nie definiuje niczego nowego matematycznie —
zbiera w jednym miejscu to, co już istnieje w `Axioms_S_TIMDR_Signal.md`,
`Axioms_G_TIMDR_Geometry.md` i `Axioms_K_TIMDR.md`, i jawnie rozdziela
semantykę wspólnych słów ("skręt", "rezonans", "anomalia") między
trzema gałęziami. W razie sprzeczności między tym dokumentem a
aksjomatami źródłowymi, aksjomaty źródłowe wygrywają — ten dokument ma
być zawsze aktualizowany razem z nimi, nie odwrotnie.

**Zasada nadrzędna (obowiązuje wszystkie trzy gałęzie):** gałęzie NIE są
rozszerzeniami ani szczególnymi przypadkami siebie nawzajem. Wspólne
słowo nazywa różne obiekty matematyczne w różnych domenach — nie różne
poziomy jednej teorii. Ta zasada jest jawnie zakodowana w każdym
zestawie aksjomatów osobno (Axioms_S nagłówek, Axioms_G Aksjomat G6,
Axioms_K przez rozdzielność domen) — tutaj jest tylko zebrana w jedną
tabelę.

---

## Gałąź M/S — sygnałowa

- **Domena:** dyskretny szereg czasowy \(x: T \to \mathbb{R}^d\), \(x
  \in \ell^\infty(T,\mathbb{R}^d)\) (Aksjomat 1).
- **Obiekty podstawowe:** sygnał \(x\), próg \(\mu_i \pm 2\sigma_i\)
  kalibrowany na żywo, okno jako operator (\(W_k\) przesuwne vs. \(P_k\)
  partycja, Aksjomat 10), hipoteza \(H\) z odciskiem SHA-256
  (Aksjomat 6), przestrzeń metryk \(\mathcal{M}\), funkcjonał testowy
  \(T: \mathcal{M}\times\mathcal{P}(\mathcal{X})\times\mathcal{P}(\mathcal{X})\to\mathbb{T}\)
  (Aksjomat 13).
- **Operatory:**
  - `anomalia` \(\mathbb{A}_i(x_i)(t) = \mathbb{1}[|x_i(t)-\mu_i|>2\sigma_i]\) (Aksjomat 2)
  - `rezonans sygnałowy (M)` \(\mathcal{R}_{\text{sig}}(x)(t) = \mathbb{1}[\sum_i \mathbb{A}_i(x_i)(t) \geq K]\) — koincydencja progowa (Aksjomat 3)
  - `skręt sygnałowy` — odwrócenie znaku lokalnego nachylenia regresji, próg \(1.5\sigma_\beta\) (Aksjomat 4)
  - `efekt jako operator` \(E: (\text{próbki},\text{próbki}) \to \mathbb{R}\times[-1,1]\), \(e_0=(0,0)\) (Aksjomat 11)
  - generatory kontroli jako próbniki rozkładów \(D_{\text{pos}}, D_A, D_B\), moc kontroli policzalna Monte Carlo (Aksjomat 12)
- **Aksjomaty:** 13 — `Axioms_S_TIMDR_Signal.md` (numeracja 1-13,
  status: 1,2,3,5 dowiedzione formalnie i/lub zwalidowane empirycznie;
  6-13 to działający kod, nie propozycja).
- **Status empiryczny:** jedyna gałąź z realną walidacją na
  rzeczywistych danych — permutacyjny test rezonansu M na
  Krakow_Centrum, wynik honestly inconclusive (p=1.0 z powodu zerowej
  mocy, nie potwierdzonego braku efektu), kontrola pozytywna
  potwierdziła sprawność metodyki (p≈0.0002).
- **Pliki źródłowe:** `Axioms_S_TIMDR_Signal.md`,
  `TIMDR-Math-Formalism/timdr_formalism/pipeline.py`,
  `TIMDR-Math-Formalism/docs/PROTOCOL.md`,
  `TIMDR-Math-Formalism/docs/REAL_DATA_VALIDATION.md`,
  `Resonance_M_Operator_Empiryczny.md`, `timdr-signal-framework` (skill,
  §1-§3 wersji zawężonej do GIA-TIMDR). Osobno, w tym samym repo:
  `timdr_formalism/{gs_matrix,theta_bifurcation,signal_class,signal_meta_bridge}.py`
  + `docs/SG_COUPLING_PHASE_DIAGRAM.md` + `docs/theory/Signal_Classes.md`
  — pipeline sygnałowy SG-Coupling/Θ_bif/klasy I-II-III (od 2026-09-12
  zamknięty w `MetaState`/faza systemu przez `signal_meta_bridge.py` —
  patrz sekcja "Gałąź META-DYNAMICS" niżej, siódma domena), ARCHITEKTONICZNIE
  ODRĘBNY od `pipeline.py`/`PROTOCOL.md` powyżej (ten pierwszy pyta "w
  jakim reżimie pracuje sygnał", ten drugi "czy hipoteza o nim jest
  matematycznie sensowna") — patrz sekcja "Warstwa meta" niżej po pełne
  rozróżnienie.
- **Czym NIE jest:** rozszerzeniem gałęzi K (rezonans modalny to inny
  operator — wyrównanie częstotliwości/fazy, nie koincydencja progowa)
  ani gałęzi G (skręt sygnałowy to odwrócenie trendu w czasie, nie
  zmiana normalnej powierzchni).

---

## Gałąź G — geometryczna

- **Domena:** trójwymiarowa przestrzeń euklidesowa \(\mathbb{R}^3\) i
  klasa dopuszczalnych powierzchni \(S \subset \mathbb{R}^3\), lokalnie
  homeomorficznych z dyskiem, z polem normalnych \(n:S\to\mathbb{S}^2\)
  określonym p.w. (Aksjomat G1).
- **Obiekty podstawowe:** trójkąt \(\Delta=(A,B,C)\) jako minimalna
  jednostka asymetrii (Aksjomat G2), pole normalnych \(n(p)\), operator
  kształtu (Weingarten) \(S_p: T_pS \to T_pS\), \(S_p(v)=-D_vn(p)\)
  (Aksjomat G9a) z jego dyskretną aproksymacją różnicą skończoną
  (Aksjomat G9b).
- **Operatory:**
  - `skręt powierzchniowy` \(T_S(p) = \|n(p+\Delta p)-n(p)\|\), operator
    częściowy \(T_S: S\times\mathbb{R}^3 \rightharpoonup [0,2]\)
    (Aksjomaty G3, G8)
  - związek z krzywizną: \(T_S(p) = F(W_S)(p,\Delta p) =
    \|\Delta p\|\cdot\|S_p(\widehat{\Delta p})\| + O(\|\Delta p\|^2)\)
    (Aksjomaty G4, G9c) — domknięty analitycznie, nie numerycznie
  - `G-Rezonans` \(\mathcal{R}_G\): widmo rezonansowe
    \((\{\omega_k\},\{Q_k\},A(\omega))\) zamkniętej krzywej z \(N\geq3\)
    węzłami sprzężenia, jako odpowiedź układu \(N\) tłumionych
    oscylatorów harmonicznych (macierze \(M,K,\Gamma\) z lokalnej
    krzywizny/torsji) na pobudzenie lokalne (Aksjomat G5) — domknięty
    numerycznie DLA \(N=3\) (trójwęzeł), nie zwalidowany empirycznie
  - **`Λ_G` — dyspersja krzywizny (dodane 2026-09-10)**:
    \(\Lambda_G(S) = \sigma_H/(\sigma_H+|\bar H|+\epsilon)\), gdzie
    \(H(p)\) to krzywizna średnia z operatora kształtu (G9b) po
    wszystkich wierzchołkach z pełnym 1-ringiem. Zbudowane w
    odpowiedzi na propozycję traktowania Λ z META-DYNAMICS jako rodziny
    operatorów per gałąź — pierwotny pomysł (parametr porządku pola
    KIERUNKÓW głównych krzywizny, analogia nematyczna do
    `circular_dispersion`) ODRZUCONY: kierunki główne żyją w LOKALNYCH
    bazach stycznych różnych dla każdego wierzchołka, więc uśrednianie
    kątów między nimi wymagałoby transportu równoległego (osobny,
    niezrobiony projekt) — zamiast tego użyto już istniejącej,
    koordynatowo-niezależnej wielkości skalarnej \(H(p)\). 0 = krzywizna
    stała (sfera/płaszczyzna/walec), →1 = silnie niejednorodna.
    Zwalidowane na syntetykach: sfera/walec ≈0, płaszczyzna z losowym
    szumem wysokości wyraźnie wyższe (6/6 testów, `timdr_geometry/
    weingarten.py::mean_curvature_dispersion`,
    `tests/test_curvature_dispersion.py`).
- **Aksjomaty:** 10 — `Axioms_G_TIMDR_Geometry.md` (G1-G10; G1-G3
  mają wzory już używane gdzie indziej w repo, G4 nazywa związek z
  Weingartenem, G5 definiuje operator G-Rezonans (zaktualizowane —
  wcześniej jawnie stwierdzał brak), G6 rozdziela od M/K, G7 ustala
  status, G8-G9 domykają analitycznie związek skrętu z krzywizną, G10
  formalizuje parametr redukcji/rozwinięcia obwiedni trójkąta).
- **Status empiryczny:** koncepcyjna (Aksjomat G7) — brak
  zaimplementowanej numerycznie wersji \(W_S\) na rzeczywistej siatce
  3D i brak walidacji empirycznej dla żadnego operatora gałęzi
  (włącznie z \(\mathcal{R}_G\), mimo że TEN jest już zaimplementowany
  i przetestowany numerycznie dla \(N=3\) — patrz G5f); wymagania do
  pełnej teorii matematycznej wypisane wprost w G7c.
- **Pliki źródłowe:** `Axioms_G_TIMDR_Geometry.md`,
  `Resonance_M_Operator_Empiryczny.md` §6, `TIMDR_Twists.md` (definicja
  skrętu powierzchniowego wśród pięciu), główny `README.md` sekcje
  o modelu trójkąta / Möbius / tetroidzie, `core/geometric_resonance_operator.py`
  + `core/trefoil_resonance_model.py` + `TIMDR_GResonance_Operator.md`
  (operator G-Rezonans, G5), osobne repo `TIMDR-Geometry-Formalism`
  (`timdr_geometry/weingarten.py` — numeryczna implementacja G8-G9:
  dyskretny operator kształtu, testy na płaszczyźnie/sferze/walcu/
  zbieżności siatki; nieuruchomione w sesji, w której powstały; ten sam
  plik zawiera też `Λ_G`/`mean_curvature_dispersion`, dodane
  2026-09-10, 6/6 testów potwierdzonych w sandboxie).
- **Czym NIE jest:** rozszerzeniem gałęzi M/S (obiekty G nie są
  elementami przestrzeni sygnałów \(x:T\to\mathbb{R}^d\) — Aksjomat
  G6a) ani gałęzi K — \(\mathcal{R}_G\) (G5) nie jest szczególnym
  przypadkiem rezonansu modalnego (inna domena: krzywa z węzłami
  mechanicznymi, nie moduły falowe na przestrzeni topologicznej,
  Aksjomat G6b).

---

## Gałąź K — modalna

- **Domena:** przestrzeń topologiczna \(T=(X,\tau)\) (Aksjomat 1);
  konfiguracje informacyjne \(I: T \to \mathcal{I}\) generujące
  modalności falowe.
- **Obiekty podstawowe:** modalności \(M = \mathcal{M}(I) =
  \{(f_i,\phi_i,A_i)\}\) — trójki częstotliwość/faza/amplituda
  (Aksjomat 3); superpozycja interferencyjna \(I(t) = \sum_i A_i
  \sin(2\pi f_i t + \phi_i)\) (Aksjomat 4); hierarchia warstw
  rezonansowych \(R_1 \subseteq R_2 \subseteq \dots \subseteq R_n\)
  (Aksjomat 8).
- **Operatory:**
  - `rezonans modalny` — wyrównanie parametrów modalnych:
    \(|f_i-f_j|<\varepsilon_f \land |\phi_i-\phi_j|<\varepsilon_\phi\)
    (Aksjomat 5)
  - `R = 𝓡(I(t))` — rezonans jako operator na sygnale interferencyjnym,
    tworzy stabilne struktury (Aksjomat 6)
  - `E = 𝓔(R,T)` — właściwości emergentne z konfiguracji rezonansowych
    (Aksjomat 7)
  - przejście między warstwami \(R_{k+1}=F(R_k)\), spójność całości
    \(\bigcap_k R_k \neq \varnothing\) (Aksjomaty 9-10)
  - **`Λ_K`, `τ_K` — dyspersja fazowa i jej tempo (dodane 2026-09-10)**:
    \(\Lambda_K(t) = 1-\lvert\text{mean}_i(e^{i\theta_i(t)})\rvert\),
    gdzie \(\theta_i(t)\) to faza chwilowa modalności \(i\) (Aksjomat 4).
    W przeciwieństwie do próby w gałęzi G (odrzuconej z powodu braku
    wspólnego układu odniesienia), TUTAJ wszystkie modalności dzielą
    JEDEN globalny okrąg fazowy — więc to jest DOSŁOWNIE ten sam obiekt
    matematyczny co `circular_dispersion` w Quantum-Lattice i
    `wind_direction_coherence` w Synoptyk-v3, nie tylko analogia.
    \(\tau_K(t,\Delta t) = \lvert\Lambda_K(t+\Delta t)-\Lambda_K(t)\rvert/\Delta t\).
    Nietrywialna dynamika: mimo że modalności są monochromatyczne
    (Aksjomat 3, stałe f/φ), \(\Lambda_K(t)\) OSCYLUJE w czasie dla
    układów wielu częstości (dudnienie) — zerowe TYLKO analitycznie, gdy
    wszystkie \(f_i\) są równe. Zwalidowane: 8/8 testów, w tym kontrola
    analityczna \(\tau_K\equiv0\) dla równych częstości
    (`timdr_modal/phase_sync.py::modal_phase_dispersion`,
    `modal_phase_tempo`, `tests/test_phase_dispersion.py`).
- **Aksjomaty:** 10 — `Axioms_K_TIMDR.md` (numeracja 1-10).
- **Status empiryczny:** brak realnej walidacji empirycznej udokumentowanej
  w tym repo (w odróżnieniu od gałęzi M/S) — status nieokreślony wprost
  w samym pliku źródłowym; traktować jako co najmniej tak samo
  koncepcyjny jak gałąź G, dopóki nie powstanie odpowiednik
  `REAL_DATA_VALIDATION.md` dla K.
- **Pliki źródłowe:** `Axioms_K_TIMDR.md`, `Operators_N_TIMDR.md`
  (operatory dla domeny modalnej, w tym skręt topologiczny τ),
  `TIMDR-Modal-Formalism/timdr_modal/phase_sync.py` (`Λ_K`/`τ_K`
  dodane 2026-09-10, `modal_phase_dispersion`/`modal_phase_tempo`, 8/8
  testów potwierdzonych w sandboxie, w tym kontrola analityczna).
- **Czym NIE jest:** rozszerzeniem gałęzi M/S (rezonans modalny to
  wyrównanie częstotliwości/fazy, nie koincydencja progowa amplitud w
  czasie — jawnie rozróżnione w Axioms_S Aksjomat 3) ani gałęzi G
  (moduły \((f,\phi,A)\) nie są punktami powierzchni ani polem
  normalnych).

---

## Gałąź META-DYNAMICS — agregatowa (Λ-τ-ρ-J)

**Dodane 2026-09-10** — ta gałąź istniała już od dawna jako działający
kod uruchomiony w sześciu niezależnych domenach, ale nigdy nie była
formalnie opisana obok M/S, G, K w tym dokumencie ani w
`TIMDR_Twists.md`/`GLOSSARY_EN_PL.md`. Dodana w odpowiedzi na
propozycję użytkownika, żeby traktować Λ/τ/ρ/J (i pochodne od nich
sygnały) jako **rodzinę operatorów agregatowych**, dokładnie tak jak
`TIMDR-Geometry-Formalism` potraktował krzywiznę: nie jedną wielkość,
tylko rodzinę operatorów, z których każdy działa w swojej domenie, ale
dzieli wspólną strukturę matematyczną (stan 4-wymiarowy + operator
ewolucji `M=dS/dt` + klasyfikacja fazy na podstawie `magnitude(M)`).

- **Domena:** dowolny system, dla którego można w każdym kroku czasowym
  policzyć CZTERY zagregowane liczby (nie surowy szereg 1D jak w M/S,
  nie punkt/siatkę 3D jak w G, nie moduły falowe jak w K) — jeden
  `MetaState(Λ,τ,ρ,J) ∈ ℝ⁴` per krok.
- **Obiekty podstawowe:**
  - `MetaState(Λ,τ,ρ,J)` — stan pola na poziomie meta (`core_meta/meta_state.py`,
    `TIMDR-META-DYNAMICS`): Λ = **struktura**, τ = **transformacja**, ρ =
    **anomalia**, J = **operator punktowy**. Tych czterech nazw NIE należy
    mylić z żadnym innym Λ/τ/ρ/J użytym gdzie indziej w tym ekosystemie —
    to jest niezależna, samodzielna definicja tej gałęzi (patrz
    rozgraniczenie τ poniżej).
  - Operator ewolucji `M = d/dt(Λ,τ,ρ,J)` (`core_meta/meta_operator_M.py`,
    klasa `MetaOperatorM`), `magnitude(M) = Σ|składowa|`,
    `classify_phase(M) ∈ {"stabilna","przejściowa","krytyczna"}` z
    progami 0.1/1.0 — jawnie oznaczonymi jako **arbitralne/nieskalibrowane**
    na żadnej konkretnej domenie (patrz status empiryczny niżej).
- **Operatory (rodzina konkretnych instancji, jedna per domena — wzorem
  rodziny operatorów krzywizny w Geometry Formalism):** każda z sześciu
  domen mapuje własny stan na `MetaState` przez własny `meta_adapter.py`,
  z WŁASNYMI, udokumentowanymi w danym repo definicjami Λ/τ/ρ/J —
  ta gałąź NIE narzuca jednego wzoru, tylko wspólny KSZTAŁT (4 liczby +
  operator ewolucji). Przykład w pełni udokumentowany (najświeższy,
  `TIMDR-Quantum-Lattice/meta_adapter.py`):
  - Λ = **dyspersja fazowa** = `1 - |mean(exp(i·faza))|` po całej
    siatce (0 = kolaps/porządek, ~1 = fazy losowe) — ten sam wzór, co
    już używany gdzie indziej w tym repo do diagnozowania kolapsu.
  - τ = **tempo zmiany defektu** = średnie `|D(t)-D(t-1)|` po całej
    siatce, znormalizowane globalnym progiem (mediana+k·MAD z okna
    kalibracyjnego).
  - ρ = **hotspoty** = frakcja komórek z `D > próg_anomalii`.
  - J = **kanał rezonansu** = frakcja komórek z `|R| > próg_rezonansu`
    — ŚWIADOMIE nieaddytywny z ρ (dodanie wprost, `Ω=D+|R|`, zostało
    przetestowane w innym miejscu tego repo i ODRZUCONE jako niszczące
    sygnał lokalizacji hotspotów; J wchodzi do wspólnego wyniku
    WYŁĄCZNIE przez `magnitude(M)` na pochodnych, nigdy przez sumę
    surowych poziomów).
  - Pozostałe pięć domen (chronologicznie): finansowa
    (`analizator-gieldowy-v3/meta_dynamics_module.py`), pogodowa
    (`Synoptyk-v3/membrane/meta_adapter.py`), sejsmiczna
    (`TIMDR-Earthquake-Core/meta_adapter.py`), wibracje łożysk
    (`TIMDR-Industrial-Predict/bearing_meta_adapter.py`), starzenie
    sieci energetycznej (`TIMDR-Grid-Monitor/meta_adapter.py`) — każda
    z własnym, jawnie udokumentowanym mapowaniem Λ/τ/ρ/J na wielkości
    fizyczne tej domeny, nieidentycznym ze wzorami Quantum-Lattice
    powyżej.
  - **Siódma domena (2026-09-12), pierwsza z tego repo/gałęzi M/S**:
    `TIMDR-Math-Formalism/timdr_formalism/signal_meta_bridge.py` —
    domyka łańcuch `sygnał → SG-Coupling → Θ_bif → klasa I/II/III →
    MetaState → faza systemu`, zlecony wprost przez użytkownika. W
    odróżnieniu od pozostałych sześciu domen (agregacja PO PRZESTRZENI,
    np. po komórkach siatki), tu nie ma przestrzeni — agregacja jest PO
    OKNIE CZASOWYM (partycja rozłączna). `ρ` = frakcja kroków w oknie
    sklasyfikowanych jako Klasa III (zależne od `β`), `J` = średnia
    względna wielkość `N(t)=S_down·S_up` znormalizowana do własnego
    maksimum w oknie (zależne od `N`, CELOWO inna wielkość źródłowa niż
    `ρ`, żeby korelacja między kanałami była wynikiem empirycznym, nie
    tautologią z konstrukcji). Wynik, ten sam wzorzec co w pozostałych
    sześciu domenach: **mechanizm działa** (mean(ρ) i mean(J) wyraźnie
    wyższe w trybie twardym niż miękkim, kierunek zgodny z intuicją),
    ale **próg "krytyczna" (`magnitude(M)≥1.0`) nie rozdziela reżimów**
    (identyczna liczba okien w obu trybach) — progi 0.1/1.0 pozostają
    nieskalibrowane na tej skali, dokładnie jak w Quantum-Lattice. Pełne
    liczby: `TIMDR-Math-Formalism/docs/theory/Signal_Classes.md`, sekcja
    "Integracja z MetaState".
  - Warstwa walidacji NIEZALEŻNA od pojedynczej domeny:
    `TIMDR-Math-Formalism/timdr_formalism/meta_validator.py` — pięć
    obszarów sprawdzeń (kształt/zakres, izolacja kanałów przez
    korelację Spearmana, diagnostyka progów fazy, porównanie reżimów
    Manna-Whitneya+Kołmogorowa-Smirnowa, stabilność fazy, spójność
    między przebiegami) działających na SUROWYCH liczbach `MetaSeriesData`,
    bez zależności od żadnej konkretnej domeny — analogicznie do tego,
    jak `pipeline.py` służy całej gałęzi M/S, nie jednemu repo.
- **Aksjomaty:** BRAK sformalizowanego zestawu aksjomatów (w
  odróżnieniu od M/S=13, G=10, K=10) — ta gałąź istnieje jako
  DZIAŁAJĄCY KOD w sześciu repo plus jeden uniwersalny walidator, nie
  jako spisany zestaw aksjomatów. To jest jawna, uczciwie nazwana luka,
  nie przeoczenie — analogicznie do tego, jak Aksjomat G7 jawnie
  nazywał brak implementacji numerycznej gałęzi G, zanim
  `TIMDR-Geometry-Formalism` ją dostarczył.
- **Status empiryczny:** mieszany, per domena, ZAWSZE z uczciwie
  zgłoszonym wynikiem negatywnym gdzie wystąpił. Przykład najpełniej
  udokumentowany (Quantum-Lattice): kontrola pozytywna (kolaps
  `helix_mode="original"`) wykazała statystycznie istotną różnicę
  `magnitude(M)` między aktywną a osiadłą fazą (Mann-Whitney,
  p=7.3e-136) — mechanizm DZIAŁA — ale progi `classify_phase()`
  (0.1/1.0, przeniesione bez zmian z oryginalnego szkicu) nigdy się nie
  odpaliły na tej skali danych (max zaobserwowane magnitude ~0.03) —
  **mechanizm działa, progi nie są skalibrowane** — to rozróżnienie
  jest odtąd formalnym wymogiem tej gałęzi, nie tylko zaleceniem.
  Druga, niezależna weryfikacja tego samego wyniku:
  `meta_validator.py` zastosowany do tych samych danych Quantum-Lattice
  potwierdził rozdzielenie faz i ujawnił nowe, uczciwie zaraportowane
  zastrzeżenie (korelacja Λ-τ podczas aktywnego kolapsu, prawdopodobnie
  wspólny trend monotoniczny, nie błąd zduplikowanego sygnału).
- **Pliki źródłowe:** `TIMDR-META-DYNAMICS/core_meta/meta_state.py`,
  `core_meta/meta_operator_M.py`, sześć `*meta_adapter.py`/
  `meta_dynamics_module.py` w domenowych repo wymienionych wyżej,
  `TIMDR-Math-Formalism/timdr_formalism/meta_validator.py` (i jego
  testy), `jbackk-lang.github.io/KATEGORIE.md` (zbiorcza tabela
  wszystkich integracji tej gałęzi).
- **Czym NIE jest:** rozszerzeniem żadnej z pozostałych trzech gałęzi —
  `MetaState` nie jest elementem przestrzeni sygnałów `x:T→ℝᵈ` (M/S),
  nie żyje na powierzchni/siatce 3D (G), nie jest modułem
  częstotliwość/faza/amplituda (K); to CZWARTY, niezależny kształt
  obiektu matematycznego (wektor 4D + operator ewolucji), współdzielący
  z pozostałymi gałęziami wyłącznie OGÓLNY protokół numerologii/
  formalizmu (§2 skilla), nie żaden konkretny wzór.
- **Domenowe instancje NIE są osobnymi gałęziami.** Jawna odpowiedź na
  propozycję "Quantum-Lattice jako pełnoprawna gałąź": sześć repo
  wymienionych wyżej dzielą JEDEN kształt obiektu matematycznego
  (`MetaState` + `MetaOperatorM`) i jeden protokół walidacji
  (`meta_validator.py`) — różnią się TYLKO tym, jak fizyczne wielkości
  danej domeny są zmapowane na Λ/τ/ρ/J, dokładnie tak jak
  Krakow_Centrum i inne miasta są różnymi INSTANCJAMI gałęzi M/S, nie
  osobnymi gałęziami. Nowa gałąź byłaby uzasadniona tylko wtedy, gdyby
  jakaś domena wymagała INNEGO kształtu obiektu matematycznego (jak G
  różni się od M/S kształtem domeny: powierzchnia 3D zamiast szeregu
  1D) — żadna z sześciu instancji tego nie robi.
- **Sygnał pokrewny, ale formalnie OSOBNY (nie część tej gałęzi):**
  zespolony parametr porządku `Z(t) = mean(exp(i·faza))` (parametr
  porządku Kuramoto), użyty w `TIMDR-Quantum-Lattice` (dynamika faz
  siatki) i w `Synoptyk-v3/membrane/spectrum.py`
  (`wind_direction_coherence`, spójność kierunku wiatru) — to NIE jest
  kanał Λ/τ/ρ/J (choć w Quantum-Lattice `Λ` jest z niego wyprowadzone
  przez `1-|Z|`, `Z` samo w sobie niesie WIĘCEJ informacji: `arg(Z)`,
  czyli średnią fazę/kierunek, którego żaden z czterech kanałów
  META-DYNAMICS nie przenosi). Tematycznie bliższy duchowi gałęzi K
  (synchronizacja faz wielu oscylatorów/kierunków), ale sformalizowany
  innym wzorem niż wyrównanie częstotliwość/faza z Aksjomatu K5 — nie
  utożsamiany z rezonansem modalnym. Nie ma jeszcze własnego wpisu
  aksjomatycznego ani w `Axioms_K_TIMDR.md`, ani nigdzie indziej — jawnie
  odnotowane tutaj jako otwarty punkt, żeby nie stał się kolejnym cichym
  kolizyjnym użyciem tego samego wzoru w trzeciej domenie.

**Runda 2 (2026-09-10, ten sam dzień): rodzina Λ (i częściowo τ)
rozszerzona na G i K.** Użytkownik zapytał "a gdyby" Λ/τ/ρ/J nie były
własnością jednej gałęzi, tylko RODZINĄ CZTERECH PYTAŃ (dyspersja/tempo/
gęstość/sprzężenie) realizowaną osobno w KAŻDEJ gałęzi TIMDR — dokładnie
tak, jak ta gałąź sama jest realizowana osobno w sześciu domenach.
Audyt przed obietnicą pokazał, że z 16 możliwych komórek (4 pytania ×
4 gałęzie) tylko ok. 6-7 miało już realny kod — reszta była czystą
analogią słowną. Użytkownik wybrał zbudowanie brakujących operatorów
(nie tylko nazwanie luki) dla dwóch najbardziej obiecujących komórek:
- **`Λ_G`** (dyspersja krzywizny średniej) w `TIMDR-Geometry-Formalism`
  — patrz sekcja "Gałąź G" wyżej.
- **`Λ_K`/`τ_K`** (dyspersja fazowa i jej tempo) w
  `TIMDR-Modal-Formalism` — patrz sekcja "Gałąź K" wyżej. Nie ODRZUCONE
  jak próba w G, bo modalności dzielą jeden globalny okrąg fazowy —
  formuła jest tu DOSŁOWNIE tym samym obiektem co `circular_dispersion`,
  nie tylko analogią.

Pozostałe komórki (ρ/J-podobne sygnały w G/K, cała kolumna TRM,
dyspersja/tempo w M/S poza istniejącym skrętem sygnałowym) pozostają
NIEZBUDOWANE — jawnie nienazwane jako "zrobione", żeby nie sugerować
kompletności, której nie ma.

---

## Warstwa meta: TIMDR-Math-Formalism jako meta-detektor hipotez (nie piąta gałąź)

**Dodane 2026-09-12**, w odpowiedzi na pytanie użytkownika "gdzie
wstawiłeś klasy sygnałów I/II/III?" i wyjaśnienie, że mieszają się tu
dwa różne poziomy. `TIMDR-Math-Formalism` NIE jest piątą gałęzią obok
M/S, G, K, META-DYNAMICS — samo repo mówi to wprost we własnym
`docs/PROTOCOL.md`: "nie jest detektorem sygnału czasowego — jest
detektorem **matematycznej sensowności**". Odpowiada na inne pytanie
niż którakolwiek z czterech gałęzi: nie "jaki kształt ma ten obiekt
matematyczny" (pytanie gałęzi), tylko "czy ta struktura / ten wzór /
ten »rezonans« to w ogóle realna matematyka, czy tylko ładnie
wyglądający pattern bez dowodu (numerologia)". To WARSTWA PRZEKROJOWA
(meta-poziom): sześciokrokowy protokół (pre-rejestracja, kontrola +/-,
Mann-Whitney, effect size, korekta Bonferroniego, uczciwy wynik
negatywny) nie zależy od tego, czy testowana hipoteza dotyczy sygnału
1D (M/S), powierzchni 3D (G), modułów falowych (K) czy `MetaState` 4D
(META-DYNAMICS) — stosuje się do hipotez z KAŻDEJ gałęzi naraz.

To samo repo zawiera DRUGĄ, architektonicznie odrębną rzecz, łatwą do
pomylenia z powyższym, bo mieszka w tych samych plikach: pipeline
SG-Coupling + operator bifurkacji Θ_bif + **klasy sygnału I/II/III**
(`timdr_formalism/{gs_matrix,theta_bifurcation,signal_class}.py`,
`docs/SG_COUPLING_PHASE_DIAGRAM.md`, `docs/theory/Signal_Classes.md`).
To NIE jest część meta-detektora — to zastosowana implementacja gałęzi
M/S (sygnał + próg `Q` + reakcja `β`), rozszerzona o `MetaState` z
META-DYNAMICS jako dodatkowy kanał diagnostyczny (`N(t)` w
`Signal_Classes.md`). Odpowiada na pytanie "w jakim reżimie aktualnie
pracuje TEN KONKRETNY sygnał" (klasa I: zachowawczy, II: modulujący,
III: anomalia strukturalna) — zupełnie inny poziom niż "czy hipoteza o
tym sygnale jest matematycznie sensowna". Oba mechanizmy żyją w jednym
repo z powodów praktycznych/historycznych (rozwijane w tej samej
sesji), NIE dlatego, że są tym samym mechanizmem:

| | Meta-detektor hipotez | Pipeline sygnałowy (M/S) |
|---|---|---|
| Pytanie | "czy to w ogóle jest prawdziwa matematyka?" | "w jakim reżimie pracuje ten sygnał?" |
| Wejście | hipoteza (opis struktury + twierdzenie) | szereg czasowy sygnału `x(t)` |
| Pliki | `pipeline.py`, `calibration.py`, `meta_validator.py`, `chronosignal.py`, `docs/PROTOCOL.md`, `docs/REAL_DATA_VALIDATION.md` | `gs_matrix.py`, `theta_bifurcation.py`, `signal_class.py`, `docs/SG_COUPLING_PHASE_DIAGRAM.md`, `docs/theory/Signal_Classes.md` |
| Wynik | werdykt: efekt istotny / nie / niejednoznaczny | klasa I, II lub III w danym kroku czasowym |

Dokumentacja obu powinna być czytana i aktualizowana OSOBNO — nie
wolno traktować werdyktu jednego mechanizmu jako potwierdzenia albo
zaprzeczenia drugiego.

---

## Tabela porównawcza (jedna strona, cały ekosystem)

| | **M/S — sygnałowa** | **G — geometryczna** | **K — modalna** | **META-DYNAMICS — agregatowa** |
|---|---|---|---|---|
| Domena | \(x:T\to\mathbb{R}^d\) (szereg czasowy) | \(S\subset\mathbb{R}^3\) (powierzchnia/siatka) LUB krzywa \(C\subset\mathbb{R}^3\) z węzłami (G5) | \(T=(X,\tau)\), moduły \((f,\phi,A)\) | dowolny system, per krok jeden \(MetaState(\Lambda,\tau,\rho,J)\in\mathbb{R}^4\) |
| "Rezonans" | koincydencja progowa \(\geq K\) parametrów naraz | widmo \((\omega_k,Q_k,A(\omega))\) układu N oscylatorów na węzłach krzywej (Aksjomat G5) — zaimplementowane i przetestowane dla N=3, nie zwalidowane empirycznie | wyrównanie częstotliwość/faza | kanał J — frakcja komórek/elementów z \(\lvert R\rvert\) ponad próg, NIEaddytywny z ρ |
| "Skręt" | odwrócenie trendu (regresja) | zmiana normalnej \(T_S\), związana z krzywizną (G8-G9) | *(nieużywane w tej gałęzi)* | τ = tempo zmiany defektu/anomalii w czasie (transformacja) — INNY obiekt niż τ topologiczne G ani τ TRM, mimo wspólnego symbolu |
| "Anomalia" | \(\mathbb{1}[\lvert x_i-\mu_i\rvert>2\sigma_i]\) | *(nieużywane w tej gałęzi)* | *(nieużywane w tej gałęzi)* | ρ — frakcja komórek/elementów ponad próg anomalii (mediana+k·MAD) |
| Liczba aksjomatów | 13 | 10 | 10 | 0 (działający kod w 6 domenach + 1 uniwersalny walidator, brak spisanych aksjomatów — jawna luka) |
| Status | częściowo zwalidowana empirycznie (realne dane, honest negative/inconclusive) | koncepcyjna, związek skrętu z krzywizną domknięty analitycznie, operator G-Rezonans domknięty numerycznie (N=3) | koncepcyjna, brak udokumentowanej walidacji | mechanizm potwierdzony (Mann-Whitney, p=7.3e-136 w Quantum-Lattice), progi klasyfikacji fazy nieskalibrowane w żadnej z 6 domen |
| Plik źródłowy | `Axioms_S_TIMDR_Signal.md` | `Axioms_G_TIMDR_Geometry.md` | `Axioms_K_TIMDR.md` | `TIMDR-META-DYNAMICS/core_meta/meta_state.py` + `meta_operator_M.py` |

**Pozostałe puste komórki są zamierzone**, nie przeoczeniem: brak
użycia "skrętu"/"anomalii" w K jest jawnym stwierdzeniem o zakresie tej
gałęzi, nie luką do wypełnienia. Komórka "Rezonans" dla gałęzi G była
wcześniej pusta (Aksjomat G5 jawnie stwierdzał brak operatora) — od
tej aktualizacji jest wypełniona operatorem G-Rezonans, patrz
`TIMDR_GResonance_Operator.md` po pełny opis i uczciwy stan walidacji.
Kolumna META-DYNAMICS dodana 2026-09-10 — patrz sekcja "Gałąź
META-DYNAMICS" powyżej po pełne uzasadnienie i sześć domenowych
instancji.

---

Powiązane: [`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md),
[`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md),
[`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md), [`TIMDR_Twists.md`](./TIMDR_Twists.md)
(rozwinięcie wiersza "Skręt" powyżej na sześć znaczeń z pełnymi
definicjami, w tym τ META-DYNAMICS z tej strony), [`Resonance_M_Operator_Empiryczny.md`](./Resonance_M_Operator_Empiryczny.md),
[`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md) (krótkie, dwujęzyczne
wpisy — ten dokument jest ich strukturalnym rozwinięciem na poziomie
całych gałęzi, nie pojedynczych słów), `TRM_biology.md` (τ TRM — osobny,
NIErozstrzygnięty związek ze skrętem topologicznym gałęzi G, patrz
`timdr-signal-framework` §13).
