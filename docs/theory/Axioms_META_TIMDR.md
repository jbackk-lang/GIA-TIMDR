# Axioms META — Aksjomaty gałęzi META-DYNAMICS TIMDR

**To NIE jest rozszerzenie [`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md),
[`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md) ani
[`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md).** To czwarty, równoległy zestaw
aksjomatów — dla gałęzi **META-DYNAMICS** (`TIMDR-META-DYNAMICS`,
`core_meta/meta_state.py`, `core_meta/meta_operator_M.py`,
`TIMDR-Math-Formalism/timdr_formalism/meta_validator.py`). Inny obiekt niż
pozostałe trzy gałęzie: nie pojedynczy sygnał, nie powierzchnia/krzywa, nie
moduły falowe, tylko **stan zagregowany** \(S_{\text{meta}}=(\Lambda,\tau,\rho,J)\)
opisujący jedną domenę (sygnał, siatkę, pole) jako punkt w \(\mathbb{R}^4\)
per okno czasowe, plus operator ewolucji \(M=dS_{\text{meta}}/dt\) między
kolejnymi oknami.

**Dlaczego ten dokument powstaje teraz, mimo że kod istnieje od dawna.**
Gałąź META-DYNAMICS miała, przed tym dokumentem, działający kod
(`MetaState`, `MetaOperatorM`), działający walidator
(`meta_validator.py`, 537 linii, 5 obszarów sprawdzeń), co najmniej
cztery zweryfikowane w tej sesji, niezależne instancje domenowe
(`TIMDR-Earthquake-Core`, `TIMDR-Grid-Monitor`, `Synoptyk-v3`,
`TIMDR-Math-Formalism/signal_meta_bridge.py`) i testy — ale **zero
aksjomatów**. To był największy jawny brak formalny w całym ekosystemie
TIMDR (`TIMDR_Branch_Specification.md`, sekcja "Gałąź META-DYNAMICS",
wiersz "Aksjomaty: BRAK"). Kolejność w tym dokumencie jest **celowa, na
wyraźną prośbę użytkownika (2026-09-18)**: najpierw \(\Lambda\)
(dyspersja) i \(\tau\) (tempo zmiany defektu) — dwa kanały, dla których
audyt czterech realnych instancji dał najbogatszy, najbardziej
rozbieżny materiał źródłowy — dopiero potem \(\rho\) (gęstość) i \(J\)
(sprzężenie).

**Metoda.** Zgodnie z regułą ekosystemu "audytuj istniejące znaczenia
PRZED napisaniem aksjomatów" (`timdr-signal-framework`, wniosek
wielokrotnego użytku #1 z §3), każdy aksjomat niżej jest wyprowadzony z
**przeczytanego w tej sesji kodu źródłowego** czterech instancji
domenowych, nie z opisu w README/skillu. Tam, gdzie dokumentacja
ekosystemu cytuje wynik empiryczny, którego generującego kodu nie udało
się zlokalizować w tym repo, jest to jawnie oznaczone jako niezweryfikowane
— patrz sekcja "Status empiryczny per domena" niżej.

Status: Aksjomaty META-1, META-2, META-6, META-7 mają pełne pokrycie
kodem i testami w ≥4 niezależnych instancjach. Aksjomat META-3
dokumentuje **brak** jednorodności między instancjami jako ustalony fakt
empiryczny, nie hipotezę do potwierdzenia. Aksjomaty META-4, META-5 mają
pełne pokrycie kodem, ale nigdy nie były testowane statystycznie
(Mann-Whitney) na żadnej z czterech instancji — tylko sprawdzane wizualnie/
opisowo per przebieg. Aksjomat META-8/META-9 opisują istniejący,
działający walidator (`meta_validator.py`), nie propozycję.

---

# Aksjomat META-1 — META-state jest rodziną instancji jednego kształtu, nie jednym wzorem
**EN:** A MetaState is a 4-tuple \((\Lambda,\tau,\rho,J)\in\mathbb{R}^4\)
per time window; each domain supplies its own map from raw physical
quantities to this tuple, sharing the shape but not the formula.
**PL:** MetaState to czwórka \((\Lambda,\tau,\rho,J)\in\mathbb{R}^4\) per
okno czasowe; każda domena dostarcza własne odwzorowanie z surowych
wielkości fizycznych na tę czwórkę, dzieląc kształt, nie wzór.

\[
S_{\text{meta}} : T \rightarrow \mathbb{R}^4, \quad
S_{\text{meta}}(t) = \big(\Lambda(t), \tau(t), \rho(t), J(t)\big)
\]

\[
\varphi_D : (\text{surowe wielkości domeny } D)\big|_{\text{okno}} \longrightarrow S_{\text{meta}} \in \mathbb{R}^4
\]

`T` to zbiór **początków okien** wynikających z partycji (bloki
rozłączne, nie okno przesuwne — ta sama zasada `P_k` co w gałęzi M/S,
`Axioms_S_TIMDR_Signal.md`, "Operator okna"), NIE indeks pojedynczej
próbki. `MetaState` (`core_meta/meta_state.py`) jest **jedyną kanoniczną
definicją tej czwórki w ekosystemie** — wcześniej duplikowana w
`timdr_meta_dynamics/__init__.py`, teraz ten plik tylko reeksportuje.
Cztery niezależnie przeczytane w tej sesji instancje \(\varphi_D\)
(sejsmika — `TIMDR-Earthquake-Core/core/meta_adapter.py`; sieć
energetyczna — `TIMDR-Grid-Monitor/meta_adapter.py`, reużywa sejsmicznego
okienkowania wprost; pogoda — `Synoptyk-v3/membrane/meta_adapter.py`;
pipeline sygnałowy SG-Coupling — `TIMDR-Math-Formalism/timdr_formalism/signal_meta_bridge.py`)
potwierdzają: żadna z nich nie współdzieli ani jednej linii wzoru z
pozostałymi — każda liczy \(\Lambda,\tau,\rho,J\) z zupełnie innych
wielkości źródłowych domeny. Wspólny jest wyłącznie **kształt**
(4 liczby, jeden `MetaState` per okno, jeden operator ewolucji `M`
działający identycznie na każdej instancji — Aksjomat META-6). To
dokładnie ten sam wzorzec co krzywizna w gałęzi G ("rodzina instancji
dzieląca kształt, nie jeden wzór", `TIMDR_Branch_Specification.md`).

Status: **ustalony, pełne pokrycie kodem** — cztery niezależne, przeczytane
w tej sesji instancje, każda z własnym plikiem `meta_adapter.py`.

---

# Aksjomat META-2 — Λ (dyspersja) jest ograniczoną [0,1) miarą rozrzutu własnej skali, samo-znormalizowaną
**EN:** Λ is a self-normalized dispersion measure, bounded in [0,1) by
construction, computed entirely from quantities internal to the window
— never from an externally calibrated threshold.
**PL:** Λ to samo-znormalizowana miara rozrzutu, ograniczona do [0,1) z
konstrukcji, liczona wyłącznie z wielkości wewnętrznych dla okna —
nigdy z zewnętrznie kalibrowanego progu.

W przeczytanych instancjach Λ przyjmuje jedną z dwóch, algebraicznie
różnych, ale obie samo-znormalizowanych postaci:

\[
\Lambda_{\text{widmowa}} = \frac{P_{\text{wysokie}}}{P_{\text{wysokie}} + P_{\text{niskie}}} \in [0,1]
\qquad\text{(ułamek energii widma FFT okna w górnej połowie pasm)}
\]

\[
\Lambda_{\text{dyspersja}} = \frac{\sigma(Q)}{\sigma(Q) + |\mu(Q)| + \varepsilon} \in [0,1)
\qquad\text{(rozrzut własny wielkości } Q \text{ względem własnej skali)}
\]

Pierwsza postać (`_high_freq_fraction`) występuje wprost w
`TIMDR-Earthquake-Core/core/meta_adapter.py` (reużyte bez zmian w
`TIMDR-Grid-Monitor/meta_adapter.py`) i jako średnia dwóch takich
ułamków (temperatura+ciśnienie) w `Synoptyk-v3/membrane/meta_adapter.py`.
Druga postać występuje w `signal_meta_bridge.py`
(`aggregate_window_to_meta_state`), której własny docstring **jawnie
przyznaje**, że to "ten sam kształt wzoru co Λ_G (dyspersja krzywizny,
σ/(σ+|mean|+eps))" z gałęzi G — patrz zastrzeżenie o kolizji symboli
niżej. Obie postaci są bounded **z czystej algebry** (mianownik ≥
licznik z konstrukcji), nie z żadnego dowodu statystycznego — to
odróżnia Λ od τ (Aksjomat META-3), gdzie taka gwarancja nie istnieje.
`meta_validator.py::validate_shape_and_ranges` sprawdza Λ∈[0,1] jako
oczekiwaną konwencję we WSZYSTKICH dotąd zaadaptowanych domenach.

Status: **ustalony strukturalnie** (ograniczenie to tożsamość algebraiczna,
nie wynik empiryczny) w 4/4 przeczytanych instancjach.

---

# Aksjomat META-3 — τ (tempo zmiany defektu) jest nieograniczonym tempem zmiany i NIE jest jednym wzorem między domenami
**EN:** τ measures the rate of change of a domain-specific "defect"
quantity per unit time. Unlike Λ, ρ, J, it has no shared codomain bound
across domains — this is documented as an empirical fact about the
branch, not an oversight.
**PL:** τ mierzy tempo zmiany domenowej wielkości "defektu" na jednostkę
czasu. W odróżnieniu od Λ, ρ, J nie ma wspólnego ograniczenia
przeciwdziedziny między domenami — to udokumentowany fakt empiryczny o
gałęzi, nie przeoczenie.

\[
\tau : (\text{okno}) \longrightarrow \mathbb{R}_{\geq 0}, \qquad
\text{JEDYNA gwarantowana własność: } \tau \geq 0
\]

Audyt czterech instancji ujawnia **dwie strukturalnie różne rodziny**:

**(a) Stosunek do progu odpornego (robust threshold), liczonego GLOBALNIE
lub PER-ZRZUT, nigdy per-okno:**

\[
\tau_{\text{próg}} = \frac{\text{mean}(|\Delta q|)_{\text{okno}}}{\text{próg}}, \qquad
\text{próg} = \text{med} + k\cdot\text{MAD}
\]

`TIMDR-Earthquake-Core/core/meta_adapter.py` liczy próg **raz na całym
śladzie** (`compute_global_thresholds`, z jawnie udokumentowanym wariantem
przyczynowym `rolling_history_seconds`); `Synoptyk-v3/membrane/meta_adapter.py`
liczy próg **niezależnie per dzień** (`defects_t.threshold`). Obie
formy są bounded do rzędu jedności *empirycznie*, nie z konstrukcji —
Synoptyk-v3 jawnie odnotowuje (V2, zastrzeżenie #3), że τ po tej
normalizacji jest *systematycznie* \(\ll 1\), bo próg z definicji leży w
ogonie rozkładu.

**Dlaczego NIE per-okno:** `TIMDR-Earthquake-Core` udokumentował i
**udowodnił algebraicznie** (nie zgadywaniem), że wersja V1, w której
każde okno jest normalizowane WZGLĘDEM SAMEGO SIEBIE
(`mean(okno)/próg(tego samego okna)`), jest niezmiennicza na jednorodne
przeskalowanie całego okna — mnożąc każdą wartość okna przez stałą `c`,
zarówno mediana, jak i MAD (a więc i próg) rosną `c`-krotnie, więc
stosunek zostaje bez zmian. V1 mierzył więc *kształt* rozkładu wewnątrz
okna, nie *poziom aktywności* względem reszty śladu — dało to zerową moc
dyskryminującą na realnym śladzie Ridgecrest 2019 (wszystkie 71 kroków
"stabilna", |M| w wąskim paśmie 0.005–0.07). To realny, udokumentowany
błąd konstrukcyjny, nie hipotetyczny — patrz `meta_adapter.py`,
nagłówek "WERSJA 1 (PORZUCONA)".

**(b) Surowe tempo zmiany podzielone przez krok czasowy symulacji, BEZ
żadnego progu:**

\[
\tau_{\text{tempo}} = \frac{\text{mean}(|\Delta\beta|)_{\text{okno}}}{dt_{\text{krok}}}
\]

`signal_meta_bridge.py` (`aggregate_window_to_meta_state`) liczy τ w ten
sposób i **sam siebie jawnie ostrzega** w pre-rejestracji (punkt 4): skala
tej postaci τ zależy całkowicie od `dt_krok` (domyślnie 0.01), więc może
łatwo przekroczyć próg klasyfikacji `1.0` nawet dla niewielkich zmian —
i jest to skala "całkowicie inna niż w pozostałych sześciu domenach [z
dokumentacji ekosystemu]".

**Wniosek (ustalony empirycznie, nie założenie):** w odróżnieniu od Λ, ρ,
J (Aksjomaty META-2, META-4, META-5), które są ograniczone do [0,1] w
KAŻDEJ z czterech przeczytanych instancji, τ NIE ma wspólnego
ograniczenia przeciwdziedziny między domenami — to jest właśnie powód,
dla którego `meta_validator.py::validate_shape_and_ranges` **celowo NIE
wymaga** τ∈[0,1], w przeciwieństwie do pozostałych trzech kanałów.

**Rozdzielenie od innych znaczeń "τ" w ekosystemie (WYMAGANE, patrz
zasada audytu):** τ w tym aksjomacie (tempo zmiany defektu) jest
**innym obiektem** niż:
1. **τ (skręt topologiczny)** z `Operators_N_TIMDR.md` — stopień
   deformacji powierzchni torus→Möbius→tetroida wzdłuż ścieżki
   \(\lambda\mapsto S_\lambda\); zupełnie inna dziedzina (rodzina
   powierzchni, nie okno czasowe) i przeciwdziedzina.
2. **τ_i (torsja Freneta–Serreta)** z Aksjomatu G5a/G5c
   (`Axioms_G_TIMDR_Geometry.md`) — geometryczna torsja krzywej w węźle
   \(i\) wchodząca do macierzy sztywności \(K_{ii}\) modelu
   G-Rezonans; zupełnie inny obiekt (własność lokalna krzywej 3D, nie
   tempo zmiany szeregu czasowego).

`TIMDR_Twists.md` katalogował dotąd cztery znaczenia "skrętu"/τ
(sygnałowy, topologiczny, powierzchniowy, blokowy) — **to jest piąte,
jeszcze nie wpisane do tego indeksu** (patrz "Pozostałe braki formalne"
niżej).

Status: **ustalony jako fakt o niejednorodności branży** — nie hipoteza
do potwierdzenia w przyszłości, tylko odczyt z 4/4 przeczytanych instancji.

---

# Aksjomat META-4 — ρ (gęstość/anomalia) jest ograniczonym [0,1] ułamkiem próbek/komórek kwalifikujących się w oknie
**EN:** ρ is the fraction of samples/cells in a window meeting a
domain-specific anomaly/class criterion, bounded [0,1] by construction
in every read instance.
**PL:** ρ to ułamek próbek/komórek w oknie spełniających domenowe
kryterium anomalii/klasy, ograniczony [0,1] z konstrukcji we WSZYSTKICH
przeczytanych instancjach.

\[
\rho = \frac{n_{\text{kwalifikujące się}}}{n_{\text{całkowite}}} \in [0,1]
\]

Najbardziej jednorodny kanał z czterech — każda przeczytana instancja
używa dosłownie tego kształtu: `TIMDR-Earthquake-Core` — ułamek próbek w
oknie, gdzie \(|s-\text{trm}(s)|\) przekracza globalny próg odporny;
`TIMDR-Grid-Monitor` — to samo, per kanał (voltage/frequency/harmonics/
load), niezależnie; `Synoptyk-v3` — suma komórek-defektów po 4 kanałach
podzielona przez `4×n_komórek` (mianownik ×4, bo licznik sumuje po 4
NIEZALEŻNYCH kanałach — jedna komórka może być defektem w więcej niż
jednym kanale naraz, więc dzielenie tylko przez `n_komórek` mogłoby dać
wartość >1); `signal_meta_bridge.py` — ułamek kroków w oknie
sklasyfikowanych jako Klasa III (najgłębsza anomalia pipeline'u
sygnałowego).

Status: **ustalony strukturalnie**, 4/4 instancji. Nigdy nie testowany
statystycznie (Mann-Whitney) między reżimem spokojnym a anomalnym w
żadnej z czterech instancji — tylko porównywany opisowo (liczba okien w
danej fazie), patrz Aksjomat META-9 dla tego, czego brakuje.

---

# Aksjomat META-5 — J (sprzężenie) jest ograniczonym [0,1] operatorem punktowym, celowo niezależnym strukturalnie od ρ
**EN:** J is bounded [0,1] like ρ, but its source quantity is
deliberately chosen to be a DIFFERENT physical quantity than ρ's, in
every read instance — never a quantity that is a subset/superset of ρ's
by construction.
**PL:** J jest ograniczone [0,1] jak ρ, ale jego wielkość źródłowa jest
celowo dobrana jako INNA wielkość fizyczna niż źródło ρ w KAŻDEJ
przeczytanej instancji — nigdy wielkość będąca z konstrukcji
podzbiorem/nadzbiorem ρ.

\[
J = \frac{n_{\text{koincydencja/nakładanie}}}{n_{\text{całkowite}}} \in [0,1]
\]

`signal_meta_bridge.py` formułuje to jako jawny wymóg projektowy
(pre-rejestracja, punkt 2): J bazuje na \(N(t)=S_{\downarrow}\cdot S_{\uparrow}\)
(nakładanie kanałów), **nie** na klasie/anomalii wprost — gdyby J było
np. "ułamek kroków z `cutoff=True`", byłoby to z KONSTRUKCJI nadzbiorem ρ
(Klasa III wymaga `cutoff=True`), czyli gwarantowaną korelacją z
definicji, nie wynikiem empirycznym do sprawdzenia. To samo rozróżnienie
źródeł obowiązuje w pozostałych trzech instancjach: `TIMDR-Earthquake-Core`/
`TIMDR-Grid-Monitor` liczą J z \(|d(\text{flow\_grad})/dt|\) (tempo zmiany
gradientu przepływu) względem globalnego progu, podczas gdy ρ liczone
jest z odchyłki od trendu \(|s-\text{trm}(s)|\) — inna wielkość źródłowa.
`Synoptyk-v3` liczy J z liczby komórek rezonansowych (koincydencja ≥k=3
kanałów, `analyze.RESONANCE_K`) względem `n_komórek` (bez czynnika ×4,
bo rezonans to JEDNA maska, nie suma 4 kanałów) — również odrębne od
sumy defektów użytej w ρ.

**Formalny, testowalny odpowiednik tego wymogu projektowego** to
`meta_validator.py::validate_channel_isolation` (korelacja Spearmana
między parami kanałów, ze szczególnym naciskiem na niezależność J) —
cytuje dwa realne, udokumentowane naruszenia tego wymogu jako uzasadnienie:
dominację surowych ρ/J w Synoptyk-v3 V1 (patrz Aksjomat META-2/META-4 wyżej,
ten sam incydent) oraz odrzucony wzór \(\Omega=D+|R|\) w Quantum-Lattice
(cytowane w `meta_validator.py`, **niezweryfikowane w tej sesji z
brakującego pliku źródłowego** — patrz "Status empiryczny per domena"
niżej).

Status: **ustalony strukturalnie** jako wymóg projektowy (4/4 instancji
świadomie dobiera odrębne źródło dla J), **częściowo ustalony** jako
wymóg testowalny (walidator istnieje i działa, ale nie był uruchomiony w
tej sesji na żadnej z czterech instancji z realnymi danymi — patrz
Aksjomat META-8/META-9).

---

# Aksjomat META-6 — Operator ewolucji M jest różnicą skończoną stanu, wielkość jest normą L1
**EN:** The evolution operator M is the finite difference of consecutive
MetaStates divided by dt; magnitude is the L1 norm of its four
components — this operator is IDENTICAL across all four read domain
instances, the one fully branch-uniform piece of the formalism.
**PL:** Operator ewolucji M to różnica skończona kolejnych MetaState
podzielona przez dt; wielkość to norma L1 czterech składowych — ten
operator jest IDENTYCZNY we wszystkich czterech przeczytanych instancjach
domenowych, jedyny w pełni jednorodny element formalizmu.

\[
M = \mathcal{M}(S_{\text{prev}}, S_{\text{next}}, dt) =
\frac{1}{dt}\big(\Delta\Lambda, \Delta\tau, \Delta\rho, \Delta J\big),
\qquad dt \neq 0
\]

\[
\|M\| = |\Delta\Lambda/dt| + |\Delta\tau/dt| + |\Delta\rho/dt| + |\Delta J/dt|
\]

Implementacja: `MetaOperatorM.compute`/`.magnitude`
(`core_meta/meta_operator_M.py`, `ValueError` przy `dt=0`). W
odróżnieniu od \(\varphi_D\) (Aksjomat META-1), który różni się wzorem
między domenami, `M` jest **wywoływane bez zmian** w każdej z czterech
przeczytanych instancji — jedyny element formalizmu, o którym można
powiedzieć "ta sama matematyka we wszystkich domenach" bez zastrzeżeń.

Status: **ustalony, pełne pokrycie kodem i testami**, 4/4 instancji,
zero wariacji międzydomenowej.

---

# Aksjomat META-7 — Klasyfikacja fazy jest stałym progiem na wielkości M, jawnie nieskalibrowanym
**EN:** Phase classification is a fixed three-way threshold on
\(\|M\|\); the thresholds (0.1/1.0) are explicitly documented as
arbitrary in the original code and independently re-confirmed as
non-discriminating on first attempt in EVERY read domain instance.
**PL:** Klasyfikacja fazy to stały, trójwartościowy próg na \(\|M\|\);
progi (0.1/1.0) są jawnie udokumentowane jako arbitralne w oryginalnym
kodzie i niezależnie ponownie potwierdzone jako niedyskryminujące przy
pierwszej próbie w KAŻDEJ przeczytanej instancji domenowej.

\[
\text{faza}(M) = \begin{cases}
\text{stabilna} & \|M\| < 0.1 \\
\text{przejściowa} & 0.1 \leq \|M\| < 1.0 \\
\text{krytyczna} & \|M\| \geq 1.0
\end{cases}
\]

`classify_phase()` (`core_meta/meta_operator_M.py`) ma **w swoim
własnym docstringu** zastrzeżenie, że progi są arbitralne/nieskalibrowane
per domena, analogicznie do `AdaptiveThresholds` w Synoptyk-v3. To NIE
jest zastrzeżenie teoretyczne — każda z czterech przeczytanych instancji
niezależnie natknęła się na to empirycznie:

- `Synoptyk-v3` V1: WSZYSTKIE kroki (spokojne i frontowe) wyszły
  "krytyczna" (surowe ρ/J zdominowały sumę) — zero mocy dyskryminującej.
- `TIMDR-Earthquake-Core` V1 τ: WSZYSTKIE 71 kroków wyszło "stabilna"
  (odwrotny błąd, patrz Aksjomat META-3) — zero mocy dyskryminującej w
  drugą stronę.
- `TIMDR-Grid-Monitor` PRÓBA 1 (`WINDOW_SECONDS=0.5s`): kontrola
  negatywna (scenariusz `normalny`, zero wstrzykniętych zdarzeń) dała
  ≥95% okien "przejściowa"/"krytyczna" na wszystkich czterech kanałach —
  odrzucone, PRÓBA 2 (2.0s) naprawiła to na 3/4 kanałach.
- `signal_meta_bridge.py`: jawnie NIE zakłada z góry, czy progi
  cokolwiek rozróżnią na trybie miękkim/twardym SG-Coupling — traktuje
  to jako pytanie otwarte do zbadania w `test_signal_meta_bridge.py`.

**Wniosek:** zero z czterech przeczytanych instancji ma skalibrowane
progi `classify_phase()`. Tam, gdzie mechanizm w końcu zadziałał
(Grid-Monitor PRÓBA 2, Earthquake-Core V2/V3 z globalnymi progami), było
to wynikiem naprawy WEJŚCIA (skali Λ/τ/ρ/J), nie zmiany progów
0.1/1.0 samych w sobie.

Status: **ustalony jako fakt o gałęzi** — progi klasyfikacji fazy są
uniwersalnie nieskalibrowane w każdej dotąd przeczytanej instancji, nie
w jednej wybranej.

---

# Aksjomat META-8 — Izolacja kanałów jest wymogiem testowalnym, weryfikowanym korelacją Spearmana
**EN:** No channel may be a near-deterministic function of another by
construction; this is enforced as a testable statistical requirement
(`meta_validator.py::validate_channel_isolation`), not merely assumed.
**PL:** Żaden kanał nie może być z konstrukcji niemal deterministyczną
funkcją innego; ten wymóg jest egzekwowany jako testowalny wymóg
statystyczny (`meta_validator.py::validate_channel_isolation`), nie
tylko zakładany.

Implementacja liczy korelację Spearmana między każdą parą kanałów
\((\Lambda,\tau,\rho,J)\) na serii `MetaState`, z osobnym naciskiem na
niezależność J (Aksjomat META-5). Dwa realne, udokumentowane naruszenia
tego wymogu w historii ekosystemu — Synoptyk-v3 V1 (ρ/J zdominowały sumę
przez brak normalizacji, Aksjomat META-4/META-7) i odrzucony wzór
Quantum-Lattice \(\Omega=D+|R|\) (cytowany przez `meta_validator.py`,
status niezweryfikowany w tej sesji — patrz niżej) — są **motywacją
konstrukcyjną** tego aksjomatu, nie tylko przykładami post factum.

Status: **ustalony jako działający kod** (`meta_validator.py`, 537
linii). Nie uruchomiony w tej sesji na żadnej z czterech przeczytanych
instancji z realnymi danymi — otwarty punkt, patrz "Pozostałe braki
formalne".

---

# Aksjomat META-9 — Walidacja statystyczna wymaga porównania reżimów, nie tylko opisu jednego przebiegu
**EN:** Establishing that phase classification discriminates a real
regime requires a two-sample statistical comparison (Mann-Whitney +
independent Kolmogorov-Smirnov) between labeled regimes, a
phase-stability diagnostic against window-too-short noise, and a
cross-run consistency check — the same discipline as the M/S branch's
protocol (`Axioms_S_TIMDR_Signal.md`, Aksjomaty 6-9), reapplied here.
**PL:** Ustalenie, że klasyfikacja fazy rozróżnia realny reżim, wymaga
statystycznego porównania dwóch prób (Mann-Whitney + niezależny
Kołmogorow-Smirnow) między oznaczonymi reżimami, diagnostyki stabilności
fazowej przeciw szumowi zbyt krótkiego okna, i sprawdzenia spójności
międzyseryjnej — ta sama dyscyplina co protokół gałęzi M/S
(`Axioms_S_TIMDR_Signal.md`, Aksjomaty 6-9), zastosowana tu ponownie.

Trzy komponenty, wszystkie zaimplementowane w `meta_validator.py`:

1. `compare_regimes` — Mann-Whitney U + niezależny test
   Kołmogorowa-Smirnowa (dwa różne testy dwupróbkowe, nie jeden
   powtórzony) między serią `MetaState` reżimu A i B.
2. `phase_stability_diagnostic` — oznacza jako szum (nie sygnał) sytuację,
   w której >50% kolejnych kroków zmienia fazę — ten sam wzorzec co
   incydent PRÓBA 1 w TIMDR-Grid-Monitor (Aksjomat META-7), tu
   sformalizowany jako automatyczna diagnostyka, cytujący jako
   precedens PRÓBĘ 1 z `TIMDR-Grid-Monitor` PRZED formalizacją.
3. `cross_run_consistency` — współczynnik zmienności (CV) między
   niezależnymi przebiegami/ziarnami losowości, flaguje CV>1.0.

**Status empiryczny: ŻADNA z czterech przeczytanych instancji domenowych
nie przeszła jeszcze przez `compare_regimes`/`phase_stability_diagnostic`/
`cross_run_consistency` na realnych danych w tej sesji** — Grid-Monitor,
Earthquake-Core i Synoptyk-v3 porównują reżimy WYŁĄCZNIE opisowo (liczba
okien w danej fazie, np. "7/23 okien przejściowa"), nie testem
istotności z rozmiarem efektu, w przeciwieństwie do analogicznego
protokołu już wdrożonego i uruchomionego na realnych danych w gałęzi M/S
(`Axioms_S_TIMDR_Signal.md`, wynik Krakow_Centrum). To jest jawna,
nienaprawiona w tej sesji luka między tym, co branża META-DYNAMICS MA
(walidator), a tym, co branża FAKTYCZNIE zrobiła (opisowe zliczanie faz).

Status: **walidator ustalony jako działający kod, protokół NIE
zastosowany** na żadnej z czterech przeczytanych instancji.

---

## Status empiryczny per domena (co faktycznie zweryfikowano w tej sesji, 2026-09-18)

Cztery instancje **przeczytane w pełni w tej sesji**, kod zweryfikowany
bezpośrednio (nie z opisu w README/skillu):

- **Sejsmika** — `TIMDR-Earthquake-Core/core/meta_adapter.py`. Trzy
  warianty kalibracji progu (`calibration_end=None`/`calibration_end`/
  `rolling_history_seconds`), przetestowane end-to-end na realnym śladzie
  Ridgecrest 2019 (stacja CLC, 360s). Jeden realny przykład, nie
  kalibracja — jawnie tak oznaczone we własnym pliku.
- **Sieć energetyczna** — `TIMDR-Grid-Monitor/meta_adapter.py`. Reużywa
  całej warstwy okienkowania sejsmicznej wprost (sibling-import przez
  `importlib`). Czwarte, piąte pole w kolejności realnych integracji wg
  własnego nagłówka pliku (finansowa, pogodowa, sejsmiczna, łożyskowa,
  sieciowa).
- **Pogoda** — `Synoptyk-v3/membrane/meta_adapter.py`. Druga integracja
  w ekosystemie wg własnego nagłówka. V1→V2 (naprawa skalowania, nie
  progów) udokumentowana na realnych 10 dniach danych siatki 3×3 wokół
  Warszawy.
- **Pipeline sygnałowy SG-Coupling** — `TIMDR-Math-Formalism/timdr_formalism/signal_meta_bridge.py`.
  Siódma instancja wg numeracji w nagłówku pliku, pierwsza z gałęzi M/S —
  **NIE jest most międzygałęziowy** w sensie `MC_{K↔G}`/`MC_{M/S↔G}`
  eksplorowanych w `Axioms_G_TIMDR_Geometry.md`/`Axioms_K_TIMDR.md` —
  to instancja META-DYNAMICS działająca na obiektach WEWNĄTRZ gałęzi M/S
  (klasy I/II/III z `signal_class.py`, nie na obiekcie innej gałęzi).

**Cztery instancje wymienione w dokumentacji ekosystemu (skill, README,
`TIMDR_Branch_Specification.md`, `GLOSSARY_EN_PL.md`, `KATEGORIE.md`),
ale NIE zweryfikowane w tej sesji:**

- **Finanse** (`analizator-gieldowy-v3`, pierwsza integracja wg
  dokumentacji) — repozytorium nieobecne w tym workspace, kod nie
  przeczytany.
- **Łożyska/wibracje** (`TIMDR-Industrial-Predict/bearing_meta_adapter.py`,
  czwarta wg dokumentacji) — repozytorium nieobecne w tym workspace, kod
  nie przeczytany.
- **Quantum-Lattice** — dokumentacja ekosystemu (skill
  `timdr-signal-framework`, `TIMDR_Branch_Specification.md`, README,
  `GLOSSARY_EN_PL.md`, `KATEGORIE.md`) cytuje ją wielokrotnie jako
  "pierwszego klienta"/najpełniej udokumentowaną instancję, z konkretnym
  wynikiem empirycznym: test Manna-Whitneya `p=7.3e-136` rozdzielający
  fazę aktywnego kolapsu od fazy osiadłej przez `magnitude(M)`.
  **Ten wynik NIE jest cytowany w niniejszym dokumencie jako
  zweryfikowany fakt**, ponieważ generujący go kod nie został
  zlokalizowany w tym repo mimo dokładnego przeszukania: `Glob` po
  `meta_adapter*.py` i po dowolnym `*.py` w całym `TIMDR-Quantum-Lattice`
  (8 plików, żaden nie zawiera integracji META), `Glob` po
  `*quantum*meta*.py` w całym workspace (0 wyników), `Grep` po
  `circular_dispersion` (termin specyficzny dla wzoru Λ tej domeny wg
  dokumentacji) w całym workspace — znaleziony wyłącznie w plikach
  dokumentacji oraz w `TIMDR-Quantum-Lattice/sweep_dynamics.py`/
  `sweep_variants.py`, z których `Grep` po
  `MetaState|Lambda|magnitude|classify_phase` **nie zwrócił ani
  jednego dopasowania** — te pliki zawierają termin `circular_dispersion`,
  ale nie integrację META-DYNAMICS. `Grep` po `7.3e-136|p=7\.3e|Quantum-Lattice`
  w całym `GIA-TIMDR` — 10 plików, wszystkie albo czysto dokumentacyjne,
  albo należące do INNEJ (siódmej, M/S) instancji `signal_meta_bridge.py`
  opisanej wyżej. **Wniosek: cytowany wynik pozostaje niezweryfikowanym
  twierdzeniem dokumentacji ekosystemu w tej sesji** — albo plik
  źródłowy istnieje poza tym workspace, albo dokumentacja opisuje wynik
  bez zachowanego, odtwarzalnego kodu. Zgodnie ze stałą zasadą tej sesji
  (twierdzenia techniczne muszą być ugruntowane w rzeczywistym kodzie,
  nie w pamięci/streszczeniu dokumentacji), ten aksjomat świadomie NIE
  powtarza `p=7.3e-136` jako potwierdzonego faktu.

---

## Rozdzielenie symboli Λ/τ/ρ/J od innych użyć w ekosystemie (dopisek)

Poza rozdzieleniem τ opisanym w Aksjomacie META-3, audyt tej sesji
ujawnił dodatkową, **nierozstrzygniętą** niejasność: Aksjomat G6b
(`Axioms_G_TIMDR_Geometry.md`) wymienia dosłownie "Λ, τ, ρ, J, \(T_S\),
\(W_S\), \(\mathcal{R}_G\)" jako operatory gałęzi G, przypisane do
Aksjomatu G5. Jednak treść G5a-G5e (przeczytana w tej sesji w pełni)
definiuje w rzeczywistości \(\kappa_i\) (krzywizna węzła), \(\tau_i\)
(torsja Freneta-Serreta — patrz Aksjomat META-3 punkt 2), macierze
\(M,K,\Gamma\) modelu mechanicznego, \(\Delta\kappa_i,\Delta\tau_i\)
(parametry defektu) oraz \(\omega_k,Q_k\) (częstości własne/dobroć) — nie
literalnie cztery symbole "Λ, ρ, J" gdziekolwiek w przeczytanej treści
G5. To może być: (a) niespójność dokumentacyjna w G6b, (b) odniesienie
do części gałęzi G nieprzeczytanej w tej sesji (G1-G4). **Nie zostało to
rozstrzygnięte w tym zadaniu** — flagowane tu jako otwarty punkt do
sprawdzenia (patrz "Pozostałe braki formalne"), nie po cichu pominięte
ani po cichu rozstrzygnięte bez weryfikacji. Niezależnie od źródła tej
niejasności: \(\Lambda,\tau,\rho,J\) zdefiniowane w niniejszym pliku
(`core_meta/meta_state.py`) są odrębnym, w pełni określonym obiektem —
zerowa identyfikacja z gałęzią G obowiązuje tu tak samo, jak wszędzie
indziej w ekosystemie (Aksjomat G6a-c), z tym zastrzeżeniem, że sama
etykieta G6b wymaga osobnego sprawdzenia, czym dokładnie jest, zanim
ktokolwiek uzna ją za ustalone starcie nazw z META-DYNAMICS.

---

## Pozostałe braki formalne

1. **Asymetria Λ/ρ/J (ograniczone [0,1]) vs τ (nieograniczone,
   Aksjomat META-3)** nie ma jeszcze głębszego uzasadnienia
   teoretycznego w tym dokumencie — jest to odczyt empiryczny z 4
   instancji, nie wyprowadzona konsekwencja jakiejś ogólniejszej zasady
   podziału gałęzi META na "kanały strukturalne" (Λ,ρ,J) i "kanał
   tempa" (τ). Możliwe przyszłe zadanie: czy istnieje formalny powód,
   dla którego DOKŁADNIE kanał tempa zmiany jest tym, który opiera się
   ograniczeniu — nie podjęte tutaj.
2. **Zero kalibracji progów `classify_phase()` (0.1/1.0) w
   jakiejkolwiek z czterech przeczytanych instancji** (Aksjomat META-7)
   — to jest fakt ustalony, nie luka do zamknięcia przez sam ten
   dokument, ale pozostaje otwartym zadaniem inżynierskim dla
   przyszłej sesji: żadna domena nie przeszła jeszcze przez pełny
   protokół Aksjomatu META-9 (kontrola pozytywna+negatywna, Mann-Whitney,
   rozmiar efektu) na progach fazy.
3. **Agregacja między-kanałowa/między-domenowa wewnątrz jednej gałęzi
   META nie jest jeszcze zaaksjomatyzowana.** `TIMDR-Grid-Monitor`
   jawnie NIE agreguje swoich czterech niezależnych kanałów
   (voltage/frequency/harmonics/load) w jeden zagregowany stan "energii
   E(t)" ani nie używa koincydencji między kanałami do połączenia ich w
   jeden wynik — świadomy wybór zakresu, udokumentowany w kodzie jako
   otwarty wątek. Gałąź M/S ma już formalny operator koincydencji
   wielokanałowej (rezonans sygnałowy, `Axioms_S_TIMDR_Signal.md`,
   Aksjomat 3) — czy analogiczny operator powinien istnieć dla
   wielokanałowych instancji META, pozostaje otwarte, świadomie
   nie poruszone w tym dokumencie (użytkownik poprosił o Λ/τ najpierw,
   ρ/J potem — agregacja międzykanałowa jest kolejnym krokiem, nie
   podjętym tu bez wyraźnej prośby).
4. **Kod źródłowy integracji Quantum-Lattice (cytowany wynik
   `p=7.3e-136`) nie został zlokalizowany w tym workspace** — patrz
   "Status empiryczny per domena" wyżej. Wymaga albo odnalezienia pliku,
   albo jawnej korekty dokumentacji ekosystemu, która obecnie cytuje ten
   wynik jako ustalony fakt w kilku miejscach (skill, README,
   `TIMDR_Branch_Specification.md`, `GLOSSARY_EN_PL.md`, `KATEGORIE.md`).
5. **Domeny finansowa (`analizator-gieldowy-v3`) i łożyskowa
   (`TIMDR-Industrial-Predict`)** — repozytoria nieobecne w tym
   workspace, ich konkretne wzory Λ/τ/ρ/J nie zostały włączone do
   Aksjomatów META-2/META-3/META-4/META-5 powyżej z tego samego powodu
   (brak dostępu do kodu źródłowego w tej sesji), nie dlatego, że są
   nieistotne.
6. **Niejasność etykiety G6b** ("Λ, τ, ρ, J" jako rzekome operatory
   gałęzi G) — patrz sekcja "Rozdzielenie symboli" wyżej, nie
   rozstrzygnięta w tym zadaniu.
7. **Piąte znaczenie τ nie zostało jeszcze wpisane do `TIMDR_Twists.md`**
   — ten dokument katalogował dotąd cztery znaczenia "skrętu" (sygnałowy,
   topologiczny, powierzchniowy, blokowy); τ_meta (Aksjomat META-3,
   "tempo zmiany defektu") jest piątym, odrębnym znaczeniem litery τ w
   ekosystemie, jeszcze nie skrzyżowo odniesionym w tamtym indeksie.

---

## Mapowanie aksjomatów META na kod/repo

- **META-1** (domena/rodzina instancji) — `core_meta/meta_state.py`
  (`MetaState`); cztery pliki `meta_adapter.py` (Earthquake-Core,
  Grid-Monitor, Synoptyk-v3) i `signal_meta_bridge.py`
  (`TIMDR-Math-Formalism`).
- **META-2** (Λ) — `_high_freq_fraction` w
  `TIMDR-Earthquake-Core/core/meta_adapter.py` (reużyte w Grid-Monitor);
  `radial_power_spectrum`-analog w `Synoptyk-v3/membrane/meta_adapter.py`;
  wzór dyspersji w `signal_meta_bridge.py::aggregate_window_to_meta_state`.
- **META-3** (τ) — `compute_global_thresholds`/`window_to_meta_state` w
  `TIMDR-Earthquake-Core/core/meta_adapter.py`; `tau` w
  `Synoptyk-v3/membrane/meta_adapter.py::membrane_result_to_meta_state`;
  `tau` w `signal_meta_bridge.py::aggregate_window_to_meta_state`.
- **META-4/META-5** (ρ, J) — te same trzy pliki, sekcje `rho`/`J`.
- **META-6** (operator M) — `core_meta/meta_operator_M.py`
  (`MetaOperatorM.compute`/`.magnitude`).
- **META-7** (klasyfikacja fazy) — `core_meta/meta_operator_M.py`
  (`MetaOperatorM.classify_phase`).
- **META-8/META-9** (walidacja) —
  `TIMDR-Math-Formalism/timdr_formalism/meta_validator.py` (pełne 537
  linii, funkcje `validate_shape_and_ranges`, `validate_channel_isolation`,
  `diagnose_phase_thresholds`, `compare_regimes`,
  `phase_stability_diagnostic`, `cross_run_consistency`,
  `validate_meta_series`).

---

## Powiązane

[`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md) (protokół
pre-rejestracji/kontroli pozytywnej-negatywnej, wzorowany tu w Aksjomacie
META-9), [`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md)
(Aksjomat G6b — źródło nierozstrzygniętej niejasności symboli Λ/τ/ρ/J,
patrz wyżej), [`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md),
[`TIMDR_Twists.md`](./TIMDR_Twists.md) (cztery dotychczasowe znaczenia
τ/skrętu — piąte, τ_meta, jeszcze nie dopisane, patrz "Pozostałe braki
formalne"), [`TIMDR_Branch_Specification.md`](./TIMDR_Branch_Specification.md)
(sekcja "Gałąź META-DYNAMICS" — wymaga aktualizacji wiersza "Aksjomaty:
BRAK" po tym dokumencie, nie zrobione w tym zadaniu bez wyraźnej prośby),
[`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md).
