# Axioms S — Aksjomaty sygnałowego TIMDR-Math-Formalism

**To NIE jest rozszerzenie [`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md).**
To równoległy, niezależny zestaw aksjomatów dla **sygnałowej** gałęzi
TIMDR (`timdr-signal-framework`, `TIMDR-Math-Formalism`) — inny operator
rezonansu (koincydencja progów w czasie, nie wyrównanie częstotliwość/
faza/amplituda), inna domena (dyskretne szeregi czasowe i statystyczne
testy hipotez, nie topologia/modalności falowe). Tam, gdzie oba zestawy
używają tego samego słowa ("rezonans", "skręt"), oznaczają **różne
obiekty matematyczne** — patrz
[`Resonance_M_Operator_Empiryczny.md`](./Resonance_M_Operator_Empiryczny.md)
sekcja 0 i [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md) po pełne
rozgraniczenie.

Status: aksjomaty 1, 2, 3, 5 poniżej mają formalny dowód (ciągłość p.w.)
i/lub realną walidację empiryczną, spisane w Resonance_M. Aksjomaty
6-13 opisują protokół testowy `TIMDR-Math-Formalism` — działający kod,
nie propozycja (`timdr_formalism/pipeline.py`, `docs/PROTOCOL.md`).
Aksjomaty 11-13 formalizują to, co wcześniej było tylko opisane
nieformalnie w PROTOCOL.md (efekt jako operator, moc kontroli, protokół
jako złożenie) — patrz też sekcja "Pozostałe braki formalne" niżej dla
tego, co świadomie NIE zostało jeszcze sformalizowane.

---

# Aksjomat 1 — Sygnał jest funkcją ograniczoną w czasie
**EN:** A TIMDR signal is a bounded function from a time index set to
ℝᵈ.
**PL:** Sygnał TIMDR to ograniczona funkcja ze zbioru indeksów czasu do ℝᵈ.

\[
x : T \rightarrow \mathbb{R}^d, \quad x \in \ell^\infty(T, \mathbb{R}^d)
\]

`T` dyskretny (np. dni, próbki); ograniczoność jest założeniem
fizycznym (realne pomiary są zawsze skończone), nie dodatkowym
warunkiem technicznym.

---

# Aksjomat 2 — Próg definiuje operator anomalii
**EN:** A threshold, calibrated live from the same window, defines the
per-parameter anomaly operator.
**PL:** Próg, kalibrowany na żywo z tego samego okna, definiuje operator
anomalii dla pojedynczego parametru.

\[
\mathbb{A}_i(x_i)(t) = \mathbb{1}\left[\, |x_i(t) - \mu_i| > 2\sigma_i \,\right],
\quad \mu_i = \text{mean}(x_i),\ \sigma_i = \text{std}(x_i)
\]

Próg NIE jest stałą uniwersalną — jest liczony z danych, zgodnie z
zasadą "kalibracja live, stała tylko jako ostateczność" (patrz
`analyzer/adaptive_thresholds.py` w ekosystemie).

---

# Aksjomat 3 — Rezonans sygnałowy jest koincydencją progową, nie falą
**EN:** Signal-domain resonance is a boolean coincidence-counting
operator over threshold crossings, not a wave-interference phenomenon.
**PL:** Rezonans sygnałowy to boolowski operator zliczający koincydencję
przekroczeń progu, nie zjawisko interferencji fal.

\[
\mathcal{R}_{\text{sig}}(x_1, \dots, x_n)(t) = \mathbb{1}\left[\, \sum_{i=1}^{n} \mathbb{A}_i(x_i)(t) \geq K \,\right]
\]

To jest operator **inny** niż ℛ w `Axioms_K_TIMDR.md` (Aksjomat 5:
`|f_i - f_j| < ε_f ∧ |φ_i - φ_j| < ε_φ`) — działa na progach amplitudy w
czasie, nie na dopasowaniu częstotliwości i fazy.

---

# Aksjomat 4 — Skręt sygnałowy jest wykrywaniem odwrócenia trendu, nie bifurkacją
**EN:** Signal-domain "skręt" is trend-reversal detection on a single
observed trajectory — not a bifurcation of a parametrized dynamical
system, absent an explicit `f(x;λ)` and a shown qualitative change.
**PL:** Skręt sygnałowy to wykrywanie odwrócenia znaku lokalnego
nachylenia w jednej obserwowanej trajektorii — nie bifurkacja
sparametryzowanego układu dynamicznego, dopóki nie wskazano jawnego
`f(x;λ)` i nie pokazano zmiany jakościowej.

\[
\text{skręt}_{\text{sig}}(x)(t) = \mathbb{1}\left[\, \text{sign}(\hat{\beta}(t^-)) \neq \text{sign}(\hat{\beta}(t^+)) \ \land\ |\hat{\beta}(t^+) - \hat{\beta}(t^-)| > 1.5\sigma_\beta \,\right]
\]

gdzie `β̂` to lokalne nachylenie regresji. Uzasadnienie krytyki "skręt =
bifurkacja": `Resonance_M_Operator_Empiryczny.md` sekcja 5.

---

# Aksjomat 5 — Operator rezonansu sygnałowego jest ciągły prawie wszędzie
**EN:** `𝓡_sig` is continuous everywhere except on a measure-zero set of
threshold-boundary points.
**PL:** `𝓡_sig` jest ciągły wszędzie poza zbiorem miary zero — punktami
leżącymi dokładnie na granicy progu.

\[
\text{Disc}(\mathcal{R}_{\text{sig}}) \subseteq \bigcup_{i=1}^{n} \{x_i : x_i = \mu_i \pm 2\sigma_i\}, \quad \mu\left(\bigcup_i \{\cdot\}\right) = 0
\]

Dowód: `𝔸_i` to funkcja wskaźnikowa zbioru domkniętego o brzegu miary
zero (dla ciągłego rozkładu `x_i`); suma skończenie wielu takich
operatorów i próg `≥K` mają zbiór nieciągłości będący skończoną sumą
zbiorów miary zero. Pełny wywód: `Resonance_M_Operator_Empiryczny.md`
sekcja 1.1. Ten wynik mówi o **stabilności klasyfikacji** wobec
drobnego szumu pomiarowego — nie mówi nic o tym, czy `𝓡_sig` wykrywa
cokolwiek ponad przypadek (to Aksjomat 8-9 poniżej, kwestia empiryczna).

---

# Aksjomat 6 — Hipoteza musi być zamrożona przed dotknięciem danych
**EN:** A hypothesis (structure + measurable effect) must be
preregistered — fingerprinted — before any data is touched; a change
after seeing results is data-snooping, detected by fingerprint mismatch.
**PL:** Hipoteza (struktura + mierzalny efekt) musi być zamrożona —
z odciskiem palca — przed dotknięciem jakichkolwiek danych; zmiana po
zobaczeniu wyniku to data-snooping, wykrywany przez niezgodność odcisku.

\[
\text{fingerprint} = \text{SHA-256}\big(\text{JSON}(\text{Hypothesis}, \text{params})\big)
\]

Implementacja: `Hypothesis`, `Preregistration.create/verify_unchanged`
w `timdr_formalism/pipeline.py`.

---

# Aksjomat 7 — Test musi przejść bramkę kontroli pozytywnej i negatywnej
**EN:** No hypothesis test may run on real/main data unless a positive
control (known effect, must detect) and a negative control (no effect,
must not false-alarm) both pass first.
**PL:** Żaden test na danych realnych/głównych nie może zostać
uruchomiony, dopóki kontrola pozytywna (znany efekt, musi wykryć) i
kontrola negatywna (brak efektu, nie może dać fałszywego alarmu) nie
przejdą obie.

\[
\text{passed} = \mathbb{1}[p_{\text{pos}} < \alpha] \land \mathbb{1}[p_{\text{neg}} \geq \alpha]
\]

Implementacja: `run_controls` w `timdr_formalism/pipeline.py`.

---

# Aksjomat 8 — Istotność i rozmiar efektu są niezależnymi osiami
**EN:** Statistical significance (p-value) and effect size are
orthogonal — a small, practically irrelevant difference can be
significant at large n, and vice versa.
**PL:** Istotność statystyczna (p-wartość) i rozmiar efektu to
niezależne osie — mała, praktycznie nieistotna różnica może być istotna
statystycznie przy dużym n, i odwrotnie.

\[
r = \frac{2U}{n_{\text{test}} \cdot n_{\text{background}}} - 1, \quad r \in [-1, 1]
\]

Implementacja: `rank_biserial_effect_size`, `TestResult.effect_size_r`
w `timdr_formalism/pipeline.py`. Pełne uzasadnienie i skrajne
przypadki: `docs/PROTOCOL.md` sekcja 4a w `TIMDR-Math-Formalism`.

---

# Aksjomat 9 — Wynik nieistotny wymaga sprawdzenia mocy przed interpretacją jako "brak efektu"
**EN:** `p ≥ α` is a complete, valid answer ONLY if the test had power
to detect the effect had it existed — otherwise it reports absence of
data, not absence of effect. Retrospective/post-hoc power must not be
computed (it is a deterministic function of p, adding no information);
power must be assessed prospectively, by simulation.
**PL:** `p ≥ α` jest pełną, ważną odpowiedzią TYLKO jeśli test miał moc
do wykrycia efektu, gdyby istniał — inaczej raportuje brak danych, nie
brak efektu. Mocy retrospektywnej/post-hoc nie wolno liczyć (jest
zdeterminowaną funkcją p, nic nie wnosi); moc trzeba oceniać
prospektywnie, symulacją.

Ten aksjomat ma bezpośrednie, realne potwierdzenie: walidacja
`𝓡_sig` na danych Krakow_Centrum dała `p=1.0` dla obu testowanych `K`,
NIE dlatego że rezonans nie przekracza przypadku, ale dlatego że w
24-dniowym oknie było zero zdarzeń współbieżnych w obu grupach — test
strukturalnie nie miał mocy. Kontrola pozytywna (wymuszona
współbieżność) wykazała `p≈0.0002`, potwierdzając sprawność metodyki.
Pełne dane: `TIMDR-Math-Formalism/docs/REAL_DATA_VALIDATION.md`,
`Resonance_M_Operator_Empiryczny.md` sekcja 3.

---

# Aksjomat 10 — Okno jest operatorem, nie tylko parametrem liczbowym
**EN:** Window-based aggregation is formally an operator on the signal
space — either a sliding window (overlapping) or a partition
(non-overlapping) — and the choice between them is a modeling decision
with consequences (i.i.d. assumption of downstream tests), not an
implementation detail.
**PL:** Agregacja okienkowa jest formalnie operatorem na przestrzeni
sygnału — przesuwanym oknem (nachodzącym) albo partycją (rozłączną) — a
wybór między nimi to decyzja modelowa z konsekwencjami (założenie i.i.d.
testów statystycznych stosowanych dalej), nie szczegół implementacyjny.

\[
W_k(x)(t) = (x(t-k), \dots, x(t+k)) \in \mathbb{R}^{2k+1}
\qquad\text{vs.}\qquad
P_k(x) = (W'_1, \dots, W'_m),\ W'_i \text{ rozłączne}
\]

`TIMDR-Math-Formalism` używa `P_k` (partycji), nie `W_k` (przesuwanego
okna) — bo Mann-Whitney U wymaga niezależnych obserwacji, a nachodzące
okna dałyby skorelowane próbki. Pełne uzasadnienie:
`docs/PROTOCOL.md` sekcja 4e.

---

# Aksjomat 11 — Efekt jest operatorem odrębnym od istotności
**EN:** Effect is an operator `E: (samples, samples) → ℝ×[-1,1]` —
direction and scale-free magnitude of a difference — orthogonal to the
significance test that judges whether that difference is distinguishable
from chance.
**PL:** Efekt jest operatorem `E: (próbki, próbki) → ℝ×[-1,1]` —
kierunek i bezskalowa wielkość różnicy — niezależnym od testu
istotności, który ocenia, czy ta różnica jest odróżnialna od
przypadku.

\[
E(x_{\text{test}}, x_{\text{bg}}) = \big(\text{median}(x_{\text{test}}) - \text{median}(x_{\text{bg}}),\ r(x_{\text{test}}, x_{\text{bg}})\big) \in \mathcal{E} = \mathbb{R} \times [-1,1]
\]

z wyróżnionym elementem `e₀=(0,0)` ("brak efektu"). Implementacja: pola
`TestResult.median_test`, `.median_background`, `.effect_size_r`.
Uzasadnienie: `docs/PROTOCOL.md` §4c w `TIMDR-Math-Formalism`.

---

# Aksjomat 12 — Generatory kontroli są próbnikami rozkładów, moc kontroli jest policzalna
**EN:** `positive_injector`/`negative_generator_*` are samplers of
distributions `D_pos, D_A, D_B` known by construction — unlike real-data
power (Aksjomat 9), control power is exactly computable by Monte Carlo,
because the ground truth is defined by the caller, not estimated from
data.
**PL:** Generatory kontroli to próbniki rozkładów `D_pos, D_A, D_B`
znanych z konstrukcji — w odróżnieniu od mocy na danych realnych
(Aksjomat 9), moc kontroli jest dokładnie policzalna metodą Monte
Carlo, bo prawda gruntowa jest zdefiniowana przez wywołującego, nie
szacowana z danych.

\[
\text{power}_{\text{pos}}(n_{\text{windows}}) \approx \frac{1}{R}\sum_{i=1}^{R} \mathbb{1}\!\left[p_{\text{pos}}^{(i)} < \alpha\right]
\]

Implikacja praktyczna: kontrola pozytywna, która regularnie nie
przechodzi, ma dwie różne możliwe przyczyny (za słaby wstrzyknięty
efekt — naprawialne zwiększeniem `n_windows`; albo metryka strukturalnie
nieczuła — nienaprawialne zwiększeniem `n_windows`) i tylko symulacja
Monte Carlo je rozróżnia. Uzasadnienie: `docs/PROTOCOL.md` §4d.

---

# Aksjomat 13 — Protokół jest złożeniem operatorów na wspólnej przestrzeni
**EN:** The six-step protocol is a composition of operators over a
shared hypothesis space `H`, metric space `M`, and test functional `T`
— not six independent techniques.
**PL:** Sześciokrokowy protokół jest złożeniem operatorów nad wspólną
przestrzenią hipotez `H`, przestrzenią metryk `M` i funkcjonałem
testowym `T` — nie sześcioma niezależnymi technikami.

\[
\text{Report} = \text{format\_report} \circ \langle \text{Gate}, T \rangle \circ \text{Generate} \circ \text{Preregister}
\]

gdzie `T: M × 𝒫(𝒳) × 𝒫(𝒳) → 𝕋` (test na danych głównych) jest **funkcją
częściową**, zdefiniowaną tylko gdy `Gate(...).passed = 1` — bramka
kontrolna (Aksjomat 7) nie jest krokiem opcjonalnym, jest warunkiem
istnienia dla `T` na danych głównych w tym złożeniu. Uzasadnienie:
`docs/PROTOCOL.md` sekcja "Formalna przestrzeń TIMDR-Math".

---

## Podsumowanie — mapowanie na kod

| Aksjomat | Operator/pojęcie | Implementacja |
|---|---|---|
| 1 | Sygnał `x: T→ℝᵈ` | wejście `metric_fn`, `positive_injector` w `pipeline.py` |
| 2 | `𝔸_i` (anomalia) | `analyzer/adaptive_thresholds.py` (ekosystem sygnałowy) |
| 3 | `𝓡_sig` (rezonans) | `TIMDRAnalyzer.analyze` (ekosystem sygnałowy) |
| 4 | skręt sygnałowy | `timdr-signal-framework` §1 |
| 5 | ciągłość p.w. `𝓡_sig` | dowód w Resonance_M §1.1 |
| 6 | pre-rejestracja | `Hypothesis`, `Preregistration` |
| 7 | bramka kontroli +/- | `run_controls` |
| 8 | effect size `r` | `rank_biserial_effect_size` |
| 9 | moc testu | `docs/PROTOCOL.md` §4b (dyscyplina, nie pojedyncza funkcja) |
| 10 | okno jako operator | `docs/PROTOCOL.md` §4e |
| 11 | efekt jako operator `E` | `docs/PROTOCOL.md` §4c |
| 12 | moc kontroli (Monte Carlo) | `docs/PROTOCOL.md` §4d |
| 13 | protokół jako złożenie operatorów | `docs/PROTOCOL.md` "Formalna przestrzeń TIMDR-Math" |

## Pozostałe braki formalne (świadomie niesformalizowane)

Żeby ten dokument nie sugerował więcej, niż faktycznie zawiera:

- **Skręt powierzchniowy jako operator geometryczny.** Formuła
  `‖n(p+Δp)−n(p)‖` (Resonance_M §6) nie jest tu powiązana z operatorem
  kształtu (Weingarten) ani formalnie zdefiniowaną krzywizną dyskretną
  — to wymaga nowej teorii geometrycznej, nie tylko zapisu, i nie jest
  częścią tego zestawu aksjomatów.
- **Dynamika/bifurkacje.** Aksjomat 4 (wyżej) krytykuje "skręt =
  bifurkacja", ale nie proponuje modelu `ẋ=f(x;λ(t))` ani dowodu
  korelacji skrętu z przejściem przez punkt krytyczny — to jedyny punkt
  w całym ekosystemie TIMDR wymagający nowych badań empirycznych, nie
  formalizacji istniejącego kodu (patrz Resonance_M §5).

Powiązane: [`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md) (równoległy zestaw,
domena modalna), [`Operators_N_TIMDR.md`](./Operators_N_TIMDR.md)
(operatory dla domeny modalnej), [`Resonance_M_Operator_Empiryczny.md`](./Resonance_M_Operator_Empiryczny.md)
(dowody i walidacja empiryczna cytowane powyżej), [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md)
(kanoniczne nazwy, rozgraniczenie "rezonans"/"skręt").
