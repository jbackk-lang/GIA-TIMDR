# TIMDR Glossary (EN/PL)

---

## Topology / Topologia

### Torus  
**EN:** A surface with two independent cyclic directions (u, v).  
**PL:** Powierzchnia z dwoma niezależnymi cyklami (u, v).  
**Meaning / Znaczenie:** Stabilna cyrkulacja informacji.

### Möbius Band  
**EN:** A non‑orientable surface with a half‑twist.  
**PL:** Nieorientowalna powierzchnia z półobrotem.  
**Meaning / Znaczenie:** Odwrócenie fazy, zmiana modalności.

### Transition Region  
**EN:** Boundary zone between topological modes.  
**PL:** Strefa przejściowa między modalnościami.  
**Meaning / Znaczenie:** Bifurkacja, wzmacnianie rezonansu.

---

## Information / Informacja

### Informational Gradient  
**EN:** Change in configuration across the structure.  
**PL:** Zmiana konfiguracji wzdłuż struktury.  
**Meaning:** Zapala nową modalność.

### Informational Cycle  
**EN:** A stable repeating pattern.  
**PL:** Stabilny powtarzalny wzorzec.  
**Meaning:** Pamięć strukturalna.

### Informational Flow  
**EN:** Propagation of influence through topology.  
**PL:** Propagacja wpływu przez topologię.  
**Meaning:** Dynamika układu.

---

## Modal Dynamics / Dynamika Modalna

### Frequency (f)  
**EN:** Rate of periodic repetition.  
**PL:** Tempo powtarzania cyklu.  
**Meaning:** Energia modalna.

### Phase (φ)  
**EN:** Alignment between modes.  
**PL:** Wyrównanie między modalnościami.  
**Meaning:** Koherencja.

### Amplitude (A)  
**EN:** Intensity of the mode.  
**PL:** Intensywność modalności.  
**Meaning:** Siła oddziaływania.

### Coupling  
**EN:** Strength of interaction between modes.  
**PL:** Siła sprzężenia między modalnościami.  
**Meaning:** Stabilność układu.

---

## Interference / Interferencja

### Interference Pattern  
**EN:** Result of overlapping waves.  
**PL:** Wynik nakładania fal.  
**Meaning:** Struktura stabilna/niestabilna.

### Node  
**EN:** Point of destructive interference.  
**PL:** Punkt interferencji destruktywnej.  
**Meaning:** Niestabilność.

### Antinode  
**EN:** Point of constructive interference.  
**PL:** Punkt interferencji konstruktywnej.  
**Meaning:** Stabilność.

---

## Rezonans / Resonance — nazwy kanoniczne

**UWAGA:** tak jak skręt, "rezonans" ma w tym ekosystemie CZTERY
niezwiązane ze sobą znaczenia. Pełne rozgraniczenie modalnego i
sygnałowego: [`theory/Resonance_M_Operator_Empiryczny.md`](theory/Resonance_M_Operator_Empiryczny.md)
sekcja 0.

### Rezonans modalny
**EN:** Alignment of frequency and phase parameters between
modalities — `|f_i−f_j|<ε_f ∧ |φ_i−φ_j|<ε_φ`.
**PL:** Wyrównanie parametrów częstotliwości i fazy między
modalnościami — `|f_i−f_j|<ε_f ∧ |φ_i−φ_j|<ε_φ`.
**Meaning:** Powstaje struktura trwała ("cząstka").
**Źródło:** `theory/Axioms_K_TIMDR.md` (Aksjomat 5),
`theory/Operators_N_TIMDR.md` (operator ℛ). Operator na falach
(częstotliwość/faza), nie na progach amplitudy w czasie.

### Rezonans sygnałowy (M)
**EN:** Boolean coincidence-counting operator — `K` of `n` parameters
simultaneously anomalous, with a binomial independence baseline,
empirically validated on real weather data (Krakow_Centrum).
**PL:** Boolowski operator zliczający koincydencję — `K` z `n`
parametrów jednocześnie anomalnych, z bazą niezależności dwumianową,
zwalidowany empirycznie na realnych danych pogodowych (Krakow_Centrum).
**Źródło:** `timdr-signal-framework` §1, `theory/Axioms_S_TIMDR_Signal.md`
(Aksjomat 3), `theory/Resonance_M_Operator_Empiryczny.md`.

### Rezonans kierunkowy
**EN:** Mean sign-agreement of derivatives across multiple signals —
`R(t) = (1/n)·Σ sign(S_i'(t))` — directional coherence. NOT threshold
coincidence (rezonans M) and NOT frequency/phase alignment (rezonans
modalny).
**PL:** Średnia zgodność znaku pochodnych wielu sygnałów —
`R(t) = (1/n)·Σ sign(S_i'(t))` — koherencja kierunkowa. NIE koincydencja
progowa (rezonans M) i NIE wyrównanie częstotliwość/faza (rezonans
modalny).
**Źródło:** sekcja "📘 TIMDR — Pełny Model Operatora Topologicznej
Zmiany Sygnału" w głównym `README.md` GIA-TIMDR. To wcześniejszy,
mniej sformalizowany szkic — częściowo pokrywa się z gałęzią sygnałową
(M) w duchu (oba działają na progach/pochodnych szeregu czasowego), ale
używa **innego wzoru** (średnia zgodność kierunku, nie zliczanie
przekroczeń progu 2σ) — nie traktuj go jako tożsamego z rezonansem M.

### Rezonans dynamiczny trójwęzła / G-Rezonans (Aksjomat G5)
**EN:** True mechanical/physical resonance — a ring of N≥3 damped
coupled harmonic oscillators on nodes of a closed curve (coupled
through the curve as a "waveguide"), driven harmonically at one node;
response amplitude peaks at the system's natural frequencies. A node
defect splits the ring's degenerate frequency doublet (Δτ) or shifts
its singlet (Δr) — qualitatively different spectral fingerprints per
defect type. Formalized as **Aksjomat G5** of the geometric branch
(`Axioms_G_TIMDR_Geometry.md`) — general operator for any N≥3 in
`core/geometric_resonance_operator.py`; the original N=3 trefoil
prototype (`core/trefoil_resonance_model.py`) is now a thin wrapper
over it.
**PL:** Prawdziwy fizyczny/mechaniczny rezonans — pierścień N≥3
tłumionych, sprzężonych oscylatorów harmonicznych na węzłach zamkniętej
krzywej (sprzężone przez krzywą jako "falowód"), pobudzany harmonicznie
w jednym węźle; amplituda odpowiedzi ma piki przy częstościach własnych
układu. Defekt węzła rozszczepia zdegenerowany dublet częstości układu
(Δτ) albo przesuwa jego singlet (Δr) — jakościowo różny odcisk widmowy
per typ defektu. Sformalizowany jako **Aksjomat G5** gałęzi
geometrycznej (`Axioms_G_TIMDR_Geometry.md`) — operator ogólny dla
dowolnego N≥3 w `core/geometric_resonance_operator.py`; pierwotny
prototyp dla N=3 (trójwęzeł, `core/trefoil_resonance_model.py`) jest
teraz cienką warstwą nad nim.
**Źródło:** `docs/theory/Axioms_G_TIMDR_Geometry.md` (Aksjomat G5),
`core/geometric_resonance_operator.py`,
`core/trefoil_resonance_model.py`,
[`geometry/TIMDR_GResonance_Operator.md`](geometry/TIMDR_GResonance_Operator.md),
[`geometry/TIMDR_Trefoil_ResonanceModel.md`](geometry/TIMDR_Trefoil_ResonanceModel.md)
(pierwotny prototyp, przed podniesieniem do G5).
**Nie** jest rezonansem M (licznik koincydencji, operator boolowski),
rezonansem sygnałowym z `core/trefoil_frenet_torsion.py` (tam:
koincydencja ≥K z N kanałów anomalnych na TEJ SAMEJ figurze — różne
obiekty współdzielące figurę, nie tylko nazwę), ani rezonansem modalnym
K (wyrównanie częstotliwość/faza modułów na przestrzeni topologicznej —
Aksjomat G6b) — mimo współdzielenia pojęcia "częstości własnej", jest
osobnym obiektem matematycznym o innej domenie.

---

## Skręt / Twist — nazwy kanoniczne

**UWAGA:** "skręt"/"twist" ma w tym ekosystemie SZEŚĆ niezwiązanych ze
sobą znaczeń. Każde nowe użycie tego słowa powinno od razu użyć
jednej z poniższych rozszerzonych nazw — samo "skręt" bez przymiotnika
jest niejednoznaczne. Pełne uzasadnienie i rozgraniczenie:
[`theory/Resonance_M_Operator_Empiryczny.md`](theory/Resonance_M_Operator_Empiryczny.md)
sekcja 0. Pełna, skonsolidowana formalna specyfikacja wszystkich
sześciu (domena, przeciwdziedzina, definicja, per znaczenie, jedno pod
drugim): [`theory/TIMDR_Twists.md`](theory/TIMDR_Twists.md). Osobno,
gałąź META-DYNAMICS ma WŁASNE τ ("transformacja") nigdy nie nazywane
"skrętem" — patrz sekcja "Λ-τ-ρ-J" niżej i
[`theory/TIMDR_Branch_Specification.md`](theory/TIMDR_Branch_Specification.md).

### Skręt sygnałowy
**EN:** Trend-reversal detection — sign flip of local regression slope
in a single time series, magnitude > 1.5σ.
**PL:** Wykrywanie odwrócenia trendu — zmiana znaku lokalnego
nachylenia regresji w pojedynczym szeregu czasowym, wielkość > 1.5σ.
**Źródło:** `timdr-signal-framework` §1. **Nie** jest bifurkacją w sensie
teorii układów dynamicznych (brak jawnego modelu `f(x;λ)`) — patrz
Resonance_M sekcja 5.

*Wcześniejszy, uproszczony wariant:* `T(t) = [sign(S'(t)) ≠
sign(S'(t−Δt))]` z sekcji "📘 TIMDR — Pełny Model..." w głównym
`README.md` GIA-TIMDR to ten sam koncept (odwrócenie kierunku), ale bez
progu wielkości (1.5σ) — samo przejście przez zero, nie tylko
odwrócenie o zauważalnej skali. Traktuj `T(t)` jako mniej rygorystycznego
poprzednika tej definicji, nie jako osobne, piąte znaczenie skrętu.

### Skręt topologiczny (τ)
**EN:** Surface deformation changing orientability (torus → Möbius →
tetroida).
**PL:** Deformacja powierzchni zmieniająca orientowalność (torus →
Möbius → tetroida).
**Źródło:** [`theory/Operators_N_TIMDR.md`](theory/Operators_N_TIMDR.md)
("Skręt τ i jego osobliwość"). Działa na rodzinie powierzchni
parametryzowanej stopniem deformacji, nie na pojedynczym punkcie ani
szeregu czasowym.

### Skręt powierzchniowy
**EN:** Local surface-normal difference, `‖n(p+Δp) − n(p)‖`, on a fixed
3D mesh — now a formal operator with domain/codomain/continuity (G8)
and an explicit curvature relation via a discrete Weingarten operator
(G9), analytically derived, not yet numerically implemented/validated.
**PL:** Lokalna różnica normalnej powierzchni, `‖n(p+Δp) − n(p)‖`, na
ustalonej siatce 3D — teraz formalny operator z domeną/przeciwdziedziną/
ciągłością (G8) i jawnym związkiem z krzywizną przez dyskretny operator
Weingartena (G9), wyprowadzonym analitycznie, jeszcze nie
zaimplementowanym numerycznie ani zwalidowanym.
**Źródło:** `theory/Resonance_M_Operator_Empiryczny.md` sekcja 6
(pierwsze wprowadzenie); formalna definicja jako aksjomat: `theory/Axioms_G_TIMDR_Geometry.md`
Aksjomaty G3 (`T_S`), G8 (operator: domena/przeciwdziedzina/ciągłość/
stabilność), G9 (dyskretny operator Weingartena, jawna postać `F`
domykająca G4b). Pełna, skonsolidowana specyfikacja wszystkich czterech
znaczeń skrętu: `theory/TIMDR_Twists.md`. Punktowy,
dyskretny — odrębny od torsji krzywej i od skrętu topologicznego τ
powyżej (inna domena: mesh 2D, nie rodzina powierzchni ani krzywa).

### Twist blokowy
**EN:** What `TwistDetector` computes in the image-in-image decoding
pipeline — operates on image blocks, own implementation, own purpose.
**PL:** To, co liczy `TwistDetector` w pipeline'ie dekodowania obrazu-w-
obrazie — działa na blokach obrazu, własna implementacja, własny cel.
**Źródło:** `MAGE-IN-IMAGE-DECODER`.

### Torsja Freneta-Serreta trójwęzła (skręt osiowy)
**EN:** Frenet-Serret torsion along a trefoil-knot curve's own axis —
`τ(t) = det(v,a,j)/‖v×a‖²` from finite-difference velocity/
acceleration/jerk, identical formula to `the_geo_pro_4d.py`
(`THE_TIMDR_Hyperflow_Engine`), curvature-gated (`κ<min_curvature ⇒
τ=0`, same noise-amplification fix as G8-G9 for surface twist).
**PL:** Torsja Freneta-Serreta wzdłuż osi krzywej trójwęzła (trefoil
knot) — `τ(t) = det(v,a,j)/‖v×a‖²` z prędkości/przyspieszenia/
szarpnięcia liczonych różnicami skończonymi, wzór identyczny z
`the_geo_pro_4d.py` (`THE_TIMDR_Hyperflow_Engine`), bramkowany
krzywizną (`κ<min_curvature ⇒ τ=0`, ta sama poprawka na wzmacnianie
szumu co G8-G9 dla skrętu powierzchniowego).
**Źródło:** `core/trefoil_frenet_torsion.py`,
[`geometry/TIMDR_Trefoil_FrenetTorsion.md`](geometry/TIMDR_Trefoil_FrenetTorsion.md).
Zainspirowane koncepcją "trójwęzła helikalnego" z
`geometry/tourosomobius.md` (tam czysto notacyjną, bez dziedziny/
przeciwdziedziny/kodu/testów) — tu domknięte jako osobny, empirycznie
przetestowany obiekt. **Nie** jest skrętem topologicznym τ powyżej
(inna domena: pojedyncza krzywa 3D sparametryzowana czasem, nie rodzina
powierzchni) — mimo współdzielonego symbolu τ w obu miejscach, celowo
NIEidentyfikowane (patrz `theory/TIMDR_Branch_Specification.md`,
zasada nadrzędna).

### τ TRM (Model Topologicznej Redukcji)
**EN:** Scalar reduction-law quantity with its own discrete ladder
`τᵢ₊₁=λτᵢ→φ`, driving `dI/dt=-R(τ)=-k·τⁿ` — relation to topological
twist τ above is explicitly UNRESOLVED (open question, not
independence, not identity). The concrete reduction law was tested
empirically (AIC, pre-registered ΔAIC=2 threshold) on two independent
real decay curves (Quantum-Lattice collapse dispersion, NASA battery
capacity fade) and **rejected both times** — does not invalidate
`TRM_biology.md` as a whole, only this specific functional form.
**PL:** Skalarna wielkość prawa redukcji z własną dyskretną drabinką
`τᵢ₊₁=λτᵢ→φ`, napędzająca `dI/dt=-R(τ)=-k·τⁿ` — związek ze skrętem
topologicznym τ powyżej jest jawnie NIEROZSTRZYGNIĘTY (otwarte pytanie,
nie niezależność, nie tożsamość). Konkretne prawo redukcji przetestowane
empirycznie (AIC, pre-rejestrowany próg ΔAIC=2) na dwóch niezależnych
realnych krzywych zaniku (dyspersja kolapsu Quantum-Lattice, zanik
pojemności baterii NASA) i **odrzucone dwukrotnie** — nie obala całości
`TRM_biology.md`, tylko tę konkretną formę funkcyjną.
**Źródło:** `theory/TRM_biology.md`, `theory/TIMDR_Twists.md` (punkt 6),
`timdr-signal-framework` §13 (pełne liczby testów AIC).

---

## Λ-τ-ρ-J / META-DYNAMICS — nazwy kanoniczne

**UWAGA:** czwarta gałąź TIMDR (obok M/S, G, K), dodana do
`theory/TIMDR_Branch_Specification.md` 2026-09-10 jako formalny opis
kodu działającego od dawna w sześciu niezależnych domenach. Λ, τ, ρ, J
tutaj są NIEZALEŻNE od wszystkich innych znaczeń tych symboli w tym
dokumencie (zwłaszcza τ — patrz sekcja "Skręt" powyżej, ten symbol ma
już cztery inne, wzajemnie rozdzielone znaczenia).

### Λ (Lambda) — struktura
**EN:** Aggregate structural state of the system at one time step
(domain-specific — e.g. phase dispersion `1-|mean(exp(i·phase))|` on a
lattice).
**PL:** Zagregowany stan strukturalny systemu w jednym kroku czasowym
(zależny od domeny — np. dyspersja fazowa `1-|mean(exp(i·faza))|` na
siatce).

### τ (tau) — transformacja
**EN:** Rate of change of the system's defect/anomaly level (domain
example: mean `|D(t)-D(t-1)|` across a lattice, normalized by a
rolling median+k·MAD threshold). **Independent object** from
topological twist τ (branch G) and from τ TRM — shares only the Greek
letter, not the mathematical object; relation to τ TRM specifically
untested (different domains, no formal comparison attempted).
**PL:** Tempo zmiany poziomu defektu/anomalii systemu (przykład
domenowy: średnie `|D(t)-D(t-1)|` po całej siatce, znormalizowane
progiem rolling mediana+k·MAD). **Niezależny obiekt** od skrętu
topologicznego τ (gałąź G) i od τ TRM — dzieli tylko literę grecką, nie
obiekt matematyczny; związek z τ TRM konkretnie niezbadany (różne
domeny, brak formalnego porównania).

### ρ (rho) — anomalia
**EN:** Fraction of elements/cells currently above a domain-calibrated
anomaly threshold ("hotspots").
**PL:** Frakcja elementów/komórek aktualnie ponad skalibrowany domenowo
próg anomalii ("hotspoty").

### J — operator punktowy (kanał rezonansu)
**EN:** Fraction of elements/cells currently above a resonance
threshold — deliberately NOT summed with ρ at the raw-value level
(tested and rejected as `Ω=D+|R|` in `TIMDR-Quantum-Lattice`); enters
the combined result only through `magnitude(M)` on derivatives.
**PL:** Frakcja elementów/komórek aktualnie ponad próg rezonansu —
świadomie NIEsumowana z ρ na poziomie surowych wartości (przetestowane
i odrzucone jako `Ω=D+|R|` w `TIMDR-Quantum-Lattice`); wchodzi do
wspólnego wyniku wyłącznie przez `magnitude(M)` na pochodnych.
**Źródło (całej rodziny Λ-τ-ρ-J):**
`TIMDR-META-DYNAMICS/core_meta/meta_state.py`,
`core_meta/meta_operator_M.py`, sześć domenowych `meta_adapter.py`
(finanse, pogoda, sejsmika, łożyska, sieć energetyczna, siatka
kwantowa — pełna lista w `theory/TIMDR_Branch_Specification.md`),
`TIMDR-Math-Formalism/timdr_formalism/meta_validator.py` (uniwersalna
warstwa walidacji, niezależna od domeny).
**Nie jest:** rozszerzeniem M/S, G ani K — czwarty, niezależny kształt
obiektu matematycznego (wektor 4D + operator ewolucji `M=dS/dt`), patrz
`theory/TIMDR_Branch_Specification.md` sekcja "Czym NIE jest".

---

## Emergence / Emergencja

### Emergent Field  
**EN:** Coherent distribution created by resonance.  
**PL:** Koherentny rozkład powstały z rezonansu.  
**Meaning:** Pole fizyczne.

### Structural Stability  
**EN:** Persistence of a resonant configuration.  
**PL:** Trwałość konfiguracji rezonansowej.  
**Meaning:** Stabilna forma.

### Energy Distribution  
**EN:** Modal amplitude and density pattern.  
**PL:** Wzorzec amplitudy i gęstości modalnej.  
**Meaning:** Energia jako wynik struktury.
