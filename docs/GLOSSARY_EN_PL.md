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

**UWAGA:** tak jak skręt, "rezonans" ma w tym ekosystemie TRZY
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

---

## Skręt / Twist — nazwy kanoniczne

**UWAGA:** "skręt"/"twist" ma w tym ekosystemie CZTERY niezwiązane ze
sobą znaczenia. Każde nowe użycie tego słowa powinno od razu użyć
jednej z poniższych rozszerzonych nazw — samo "skręt" bez przymiotnika
jest niejednoznaczne. Pełne uzasadnienie i rozgraniczenie:
[`theory/Resonance_M_Operator_Empiryczny.md`](theory/Resonance_M_Operator_Empiryczny.md)
sekcja 0.

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
3D mesh.
**PL:** Lokalna różnica normalnej powierzchni, `‖n(p+Δp) − n(p)‖`, na
ustalonej siatce 3D.
**Źródło:** `theory/Resonance_M_Operator_Empiryczny.md` sekcja 6.
Punktowy, dyskretny — odrębny od torsji krzywej i od skrętu
topologicznego τ powyżej (inna domena: mesh 2D, nie rodzina powierzchni
ani krzywa).

### Twist blokowy
**EN:** What `TwistDetector` computes in the image-in-image decoding
pipeline — operates on image blocks, own implementation, own purpose.
**PL:** To, co liczy `TwistDetector` w pipeline'ie dekodowania obrazu-w-
obrazie — działa na blokach obrazu, własna implementacja, własny cel.
**Źródło:** `MAGE-IN-IMAGE-DECODER`.

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
