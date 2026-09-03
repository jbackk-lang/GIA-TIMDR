# Resonance M — Operator rezonansu: formalizacja, stabilność, walidacja empiryczna

**EN:** Formal treatment of the signal-domain resonance operator (as
used across TIMDR's engineering repos), its stability, an honest
real-data validation of its independence-baseline claim, and a
disambiguation of "resonance" and "skręt/twist" across the ecosystem.
**PL:** Formalne ujęcie operatora rezonansu w sensie sygnałowym (jak
używany w repozytoriach inżynierskich TIMDR), jego stabilność, uczciwa
walidacja na realnych danych oraz rozgraniczenie znaczeń "rezonansu" i
"skrętu/twistu" w ekosystemie.

Status: część treści poniżej (aksjomaty sygnałowe, operator rezonansu,
wynik empiryczny) była **realnie przetestowana** przed spisaniem —
patrz sekcja 4. Część (krytyka "skręt = bifurkacja", formuła
geometryczna) jest analizą pojęciową, nie numerycznym testem — oznaczone
osobno.

---

## 0. Dlaczego ten dokument zaczyna się od disambiguacji

Zanim cokolwiek sformalizujemy: słowa "rezonans" i "skręt" mają w tym
ekosystemie **więcej niż jedno, niezwiązane ze sobą znaczenie**. To nie
jest pedanteria — pomylenie tych znaczeń jest dokładnie tym błędem,
przed którym ostrzega `timdr-signal-framework` §7 i §15 (żargon formalny
bez spełnionych aksjomatów).

**"Rezonans" — dwa niezwiązane znaczenia:**

1. **Rezonans sygnałowy** (`timdr-signal-framework` §1,
   `TIMDRAnalyzer.analyze`, `run_controls` w TIMDR-Math-Formalism): licznik
   koincydencji — `R(t) = 1[liczba jednocześnie anomalnych parametrów >= K]`.
   To operator boolowski na wielu niezależnych szeregach czasowych, **nie
   fizyczny oscylator**.
2. **Rezonans modalny** (`Axioms_K_TIMDR.md` Aksjomat 5,
   `Operators_N_TIMDR.md` operator ℛ): wyrównanie parametrów falowych
   `(f, φ, A)` między modalnościami — `|f_i - f_j| < ε_f ∧ |φ_i - φ_j| < ε_φ`.
   To operator na falach/modalnościach, w duchu bliższy fizycznemu
   rezonansowi (dudnienie, sprzężenie fazowe).

Te dwa operatory **nie są tym samym obiektem matematycznym** — jeden
działa na progach amplitudy w czasie, drugi na dopasowaniu częstotliwości
i fazy. Ten dokument dotyczy **wyłącznie rezonansu sygnałowego (1)** —
to on ma testowalną, statystyczną treść (baza niezależności, test
permutacyjny), którą da się realnie zwalidować na danych. Rezonans
modalny (2) pozostaje poza zakresem tego dokumentu.

**"Skręt/twist" — teraz cztery niezwiązane znaczenia:**

1. **Skręt sygnałowy** (`timdr-signal-framework` §1): odwrócenie trendu —
   zmiana znaku lokalnego nachylenia regresji, o wielkości > 1.5σ. Działa
   na pojedynczym szeregu czasowym.
2. **Skręt topologiczny τ** (`Operators_N_TIMDR.md`, sekcja "Skręt τ i
   jego osobliwość"): deformacja powierzchni zmieniająca orientowalność
   (torus → Möbius → tetroida). Działa na rodzinie powierzchni
   parametryzowanych stopniem deformacji.
3. **Skręt geometryczny** (propozycja z tej sesji, sekcja 6 poniżej):
   różnica lokalnej normalnej powierzchni w punkcie —
   `skręt(p) = ‖n(p+Δp) − n(p)‖`. Działa punktowo na jednej, ustalonej
   powierzchni 3D.
4. **`TwistDetector`** (`MAGE-IN-IMAGE-DECODER`): detektor w pipeline'ie
   dekodowania obrazu-w-obrazie, osobna implementacja o osobnym celu.

Rekomendacja (jak w §7 skilla dla "rezonansu"): każde nowe użycie słowa
"skręt"/"twist" powinno od razu doprecyzować, o które z czterech znaczeń
chodzi — najlepiej przez rozszerzoną nazwę: **"skręt sygnałowy"**,
**"skręt topologiczny"**, **"skręt powierzchniowy"**, **"twist
blokowy"**. Ten dokument używa tych rozszerzonych nazw wszędzie tam,
gdzie mogłoby dojść do pomyłki. Lista kanoniczna (jedno miejsce, nie
duplikować gdzie indziej): [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md)
sekcja "Skręt / Twist — nazwy kanoniczne".

---

## 1. Przestrzeń sygnału i operatory progowe

Niech `T` będzie zbiorem indeksów czasu (dyskretnym, np. dniami) i
`x: T → ℝᵈ` sygnałem wielowymiarowym (`d` parametrów obserwowanych
jednocześnie), `x ∈ ℓ^∞(T, ℝᵈ)` (ograniczony — realne pomiary fizyczne
zawsze są ograniczone).

**Operator anomalii** `𝔸_i` dla parametru `i`, liczony **adaptacyjnie z
tego samego okna** (nie z ustalonej stałej — zgodnie z
`analyzer/adaptive_thresholds.py`):

```
𝔸_i(x_i)(t) = 1[ |x_i(t) − μ_i| > 2·σ_i ],   μ_i = mean(x_i), σ_i = std(x_i)
```

**Operator rezonansu sygnałowego** dla `n` parametrów, próg `K`:

```
ℛ_sig(x_1, ..., x_n)(t) = 1[ Σ_i 𝔸_i(x_i)(t) ≥ K ]
```

(dokumentowany system engineering używa `n=5`, `K=3`).

### 1.1 Ciągłość operatora rezonansu (p.w.)

`𝔸_i` jest funkcją wskaźnikową zbioru `{x_i : |x_i − μ_i| > 2σ_i}` — jej
jedyne punkty nieciągłości leżą na brzegu tego zbioru,
`{x_i = μ_i ± 2σ_i}`, który ma miarę Lebesgue'a zero dla dowolnego
ciągłego rozkładu `x_i`. Złożenie skończenie wielu takich operatorów
(sumowanie i próg `≥K`) ma zbiór nieciągłości będący skończoną sumą
zbiorów miary zero — więc `ℛ_sig` jest **ciągły prawie wszędzie**
(wszędzie poza mierzalnym zbiorem miary zero threshold-boundary).

To słaby, ale prawdziwy wynik: mówi, że drobne zaburzenie danych
(szum pomiarowy) niemal nigdy nie zmieni klasyfikacji rezonans/nie-rezonans
— poza rzadkimi przypadkami "na granicy progu". Nie mówi nic o tym, czy
rezonans **cokolwiek wykrywa** ponad przypadek — to pytanie empiryczne,
sekcja 3-4.

---

## 2. Baza niezależności — oszacowanie teoretyczne

Jeśli `n` parametrów jest **niezależnych** i każdy ma rozkład w
przybliżeniu normalny, to `P(𝔸_i=1) ≈ P(|Z|>2) ≈ 0.0455` dla standardowego
`Z`. Prawdopodobieństwo, że **co najmniej K z n** będzie anomalnych
jednocześnie **czysto przez przypadek**, to ogon rozkładu dwumianowego:

```
P(Binomial(n, 0.0455) ≥ K)
```

Dla udokumentowanego systemu (`n=5, K=3`): **≈ 0.09%**. To liczba
**czysto teoretyczna** — zależy od dwóch założeń (niezależność,
normalność), które w realnych danych pogodowych generalnie **nie
zachodzą** (parametry pogodowe są ze sobą skorelowane; rozkłady nie są
idealnie gaussowskie). Traktowanie 0.09% jako gotowego faktu o realnym
systemie byłoby dokładnie błędem, przed którym ostrzega §13 skilla —
formuła bez przepuszczenia przez dane.

---

## 3. Walidacja empiryczna — realne dane, nie założenie

Zamiast opierać się na oszacowaniu z sekcji 2, przetestowano operator
rezonansu **na realnych danych pogodowych**, permutacyjnie — bez
zakładania niezależności ani normalności, tylko z realnych marginalnych
rozkładów każdego parametru.

**Dane:** stacja Krakow_Centrum, `synoptyk-v2.0-main/krakow_forecast_snapshots.csv`,
tylko wiersze realnych obserwacji (nie prognoz), 2026-08-09 .. 2026-09-02,
24 dni. **Ograniczenie danych:** kolumna wilgotności nie istnieje w tym
pliku w ogóle, a pokrycie opadu jest niepełne — użyto n=3 parametrów
(temperatura maks., ciśnienie, wiatr), nie udokumentowanych n=5. To
zawężony analog systemu, nie pełna replikacja.

**Metoda:** progi 2σ liczone live z tego okna; `ℛ_sig` dla K=2 i K=3;
model null przez permutację — każdy parametr tasowany niezależnie
(zrywa wyrównanie czasowe między parametrami, zachowuje realny rozkład
anomalii każdego z osobna), 5000 powtórzeń, p-wartość permutacyjna.
Pełny opis i kod: `TIMDR-Math-Formalism/docs/REAL_DATA_VALIDATION.md`
i `TIMDR-Math-Formalism/examples/real_weather_resonance_validation.py`.

**Realny wynik:**

| Parametr | anomalne dni / 24 |
|---|---|
| temperatura | 2 |
| ciśnienie | 0 |
| wiatr | 1 |

| K | realna stopa rezonansu | p (permutacja) |
|---|---|---|
| 2 | 0/24 | 1.0 |
| 3 | 0/24 | 1.0 |

Kontrola pozytywna (sztucznie wymuszona pełna współbieżność w 3 dniach,
sprawdzająca, czy sama metodyka działa): stopa 3/24, **p ≈ 0.0002** —
wykryte poprawnie.

**Uczciwy werdykt:** to **nie jest** dowód, że rezonans sygnałowy nie
przekracza przypadku. Ciśnienie w tym oknie nigdy nie przekroczyło progu
2σ (realna stopa anomalii per parametr: 8.3% / 0% / 4.2%, znacząco
poniżej teoretycznych ~4.55% z sekcji 2), więc przy obu wartościach K
liczba zdarzeń współbieżnych wyniosła zero zarówno w danych realnych,
jak i w rozkładzie null — test **nie miał mocy statystycznej w żadną
stronę**. Kontrola pozytywna potwierdza, że mechanika testu jest
sprawna (wykrywa realną współbieżność, gdy występuje) — więc to wynik
ograniczenia danych (za krótkie, za spokojne pogodowo okno), nie wada
operatora ani testu.

**Co by było potrzebne, żeby faktycznie rozstrzygnąć tę hipotezę:**
dłuższe okno obejmujące więcej dni ekstremalnej pogody (żeby każdy
parametr miał realistyczną własną liczbę anomalii) i/lub dane z
wilgotnością, żeby dojść do udokumentowanych n=5 parametrów.

Ten wynik zastępuje w praktycznym zastosowaniu teoretyczne 0.09% z
sekcji 2 — nie dlatego, że 0.09% jest błędne jako rachunek, ale dlatego,
że **żadna z dwóch liczb (0.09% teoretyczne, p=1.0 empiryczne z tego
okna) nie jest jeszcze ostatecznym stwierdzeniem o tym, czy rezonans
sygnałowy realnie przekracza przypadek** — pierwsza bo opiera się na
niesprawdzonych założeniach, druga bo test nie miał mocy w tym
konkretnym oknie. Uczciwy stan wiedzy: **otwarte pytanie, wymagające
dłuższego okna danych**, nie ustalony fakt w żadną stronę.

---

## 4. Metoda dokumentowania (dla przejrzystości)

Sekcje 1-3 powyżej zostały **realnie policzone**, nie tylko opisane:
operator rezonansu i test permutacyjny zaimplementowano i wykonano
(niezależna reimplementacja JavaScript uruchomiona w przeglądarce, bo
Python/bash były w tej sesji niedostępne — ten sam kompromis, inny RNG,
udokumentowany w `TIMDR-Math-Formalism`), na realnych 24 dniach danych z
`krakow_forecast_snapshots.csv`. Liczby w tabelach w sekcji 3 to
bezpośredni output tego wykonania, nie ilustracja.

---

## 5. Skręt sygnałowy vs bifurkacja — krytyka pojęciowa

*(Poniższa sekcja jest analizą pojęciową, nie testem numerycznym.)*

Propozycja "skręt = bifurkacja" utożsamia skręt sygnałowy (odwrócenie
znaku lokalnego nachylenia w pojedynczym szeregu czasowym, > 1.5σ) z
bifurkacją w teorii układów dynamicznych (`ẋ = f(x; λ)`, jakościowa
zmiana zachowania **rodziny** układów sparametryzowanej `λ`, przy
przejściu `λ` przez wartość krytyczną).

To dwa różne obiekty:

- Skręt sygnałowy działa na **jednej, obserwowanej trajektorii w
  czasie** — nie wymaga (i nie ma) żadnego jawnego modelu dynamicznego
  `f`, ani parametru `λ`, którego zmiana miałaby być przyczyną.
- Bifurkacja to własność **rodziny** układów — wymaga wskazania, co
  jest `λ` i jaki jest `f`, oraz wykazania jakościowej zmiany
  portretu fazowego (liczby/stabilności punktów stałych, cykli itd.),
  nie tylko zmiany znaku pochodnej jednej obserwowanej trajektorii.

Odwrócenie trendu w szeregu czasowym **może** być objawem przejścia
przez bifurkację w leżącym u podstaw układzie dynamicznym — ale samo
wykrycie odwrócenia trendu tego nie stwierdza, dopóki nie ma
wyspecyfikowanego modelu `f(x; λ)` i pokazanej zmiany jakościowej, nie
tylko ilościowej.

**Rekomendacja:** nazywać skręt sygnałowy tym, czym realnie jest —
**wykrywaniem odwrócenia trendu** ("trend-reversal detection") —  a
termin "bifurkacja" rezerwować dla przypadków, gdzie faktycznie
wyspecyfikowano `f(x; λ)` i pokazano jakościową zmianę zachowania przy
zmianie `λ`. To dokładnie dyscyplina z §15 skilla: żargon formalny bez
spełnionych aksjomatów tej formalnej teorii nie czyni czegoś tą teorią.

---

## 6. Skręt geometryczny — formuła powierzchniowa

*(Analiza pojęciowa; poprawna geometrycznie, nie testowana numerycznie
w tej sesji na konkretnych danych 3D.)*

Zaproponowana formuła dla powierzchni (nie krzywej):

```
skręt(p) = ‖n(p + Δp) − n(p)‖,   próg: > k · median(‖n(q+Δq) − n(q)‖ dla q w sąsiedztwie)
```

gdzie `n(p)` to lokalna normalna powierzchni w punkcie `p` (np. z
operatora kształtu / macierzy Weingartena). To **dyskretna aproksymacja
lokalnej zmiany kierunku normalnej** — sensowny, samodzielny konstrukt
geometryczny, dobrze określony na siatce/mesh 3D.

**Ważne rozgraniczenie od torsji krzywej.** Torsja krzywej
`τ = (ṙ, r̈, r⃛) / ‖ṙ × r̈‖²` (iloczyn mieszany pierwszej, drugiej i
trzeciej pochodnej, znormalizowany) mierzy, jak bardzo krzywa **wychodzi
z płaszczyzny oskulacyjnej** — to własność **jednej krzywej 1D w
przestrzeni**, ciągła, globalnie zdefiniowana wzdłuż parametryzacji.

Skręt geometryczny powyżej działa inaczej: jest **dyskretny, lokalny, i
zdefiniowany na powierzchni 2D (mesh), nie na krzywej** — mierzy zmianę
normalnej między sąsiednimi punktami powierzchni, nie odchylenie
trajektorii od płaszczyzny. To nie jest "torsja dla powierzchni" ani jej
uogólnienie — to **inny obiekt geometryczny, mierzący inną rzecz**,
skonstruowany analogicznie (różnica lokalnego kierunku), ale bez
formalnego związku z definicją torsji.

Wniosek: formuła jest geometrycznie poprawna i użyteczna jako własny,
nazwany konstrukt — pod warunkiem używania rozszerzonej nazwy **"skręt
powierzchniowy"** (żeby odróżnić od skrętu sygnałowego, skrętu
topologicznego τ z `Operators_N_TIMDR.md`, i `TwistDetector` z
MAGE-IN-IMAGE-DECODER — patrz sekcja 0).

---

## 7. Podsumowanie

| Twierdzenie | Status |
|---|---|
| Operator rezonansu sygnałowego jest ciągły p.w. | Dowiedzione formalnie (sekcja 1.1) |
| Teoretyczna baza niezależności (n=5, K=3) ≈ 0.09% | Rachunek poprawny, ale oparty na niesprawdzonych założeniach (niezależność, normalność) |
| Realny rezonans sygnałowy przekracza przypadek | **Otwarte** — test na 24-dniowym oknie realnych danych nie miał mocy statystycznej (za mało anomalii/parametr); metodyka testu zweryfikowana jako sprawna kontrolą pozytywną (sekcja 3) |
| "Skręt = bifurkacja" | Nieuzasadnione bez wyspecyfikowanego modelu dynamicznego; rekomendowana etykieta: "wykrywanie odwrócenia trendu" (sekcja 5) |
| Skręt powierzchniowy (`‖n(p+Δp)−n(p)‖`) | Geometrycznie poprawny, odrębny od torsji krzywej i od pozostałych 3 znaczeń "skrętu" w ekosystemie — wymaga rozszerzonej nazwy (sekcja 6) |

Powiązane dokumenty: [`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md) (rezonans
modalny — inny operator niż tu opisany), [`Operators_N_TIMDR.md`](./Operators_N_TIMDR.md)
(skręt topologiczny τ — inny obiekt niż tu opisany),
[`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md) (aksjomaty dla
domeny sygnałowej opisanej tutaj), [`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md)
(formalna aksjomatyzacja skrętu powierzchniowego z sekcji 6 — Aksjomat
G3, z powiązaniem do Weingartena w G4), [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md)
(kanoniczna lista nazw skrętu), `TIMDR-Math-Formalism/docs/REAL_DATA_VALIDATION.md`
(pełne dane i kod walidacji z sekcji 3), `TIMDR-Math-Formalism/docs/PROTOCOL.md`
(effect size, moc testu, operator okna — formalizacja kroków 4/5 protokołu).
