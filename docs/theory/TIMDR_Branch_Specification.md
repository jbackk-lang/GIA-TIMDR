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
  §1-§3 wersji zawężonej do GIA-TIMDR).
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
- **Aksjomaty:** 9 — `Axioms_G_TIMDR_Geometry.md` (G1-G9; G1-G3
  mają wzory już używane gdzie indziej w repo, G4 nazywa związek z
  Weingartenem, G8-G9 domykają go analitycznie, G5 jawnie stwierdza
  brak operatora rezonansu geometrycznego, G6 rozdziela od M/K, G7
  ustala status).
- **Status empiryczny:** koncepcyjna (Aksjomat G7) — brak
  zaimplementowanej numerycznie wersji na rzeczywistej siatce 3D i
  brak walidacji empirycznej; wymagania do pełnej teorii matematycznej
  wypisane wprost w G7c.
- **Pliki źródłowe:** `Axioms_G_TIMDR_Geometry.md`,
  `Resonance_M_Operator_Empiryczny.md` §6, `TIMDR_Twists.md` (definicja
  skrętu powierzchniowego wśród czterech), główny `README.md` sekcje
  o modelu trójkąta / Möbius / tetroidzie.
- **Czym NIE jest:** rozszerzeniem gałęzi M/S (obiekty G nie są
  elementami przestrzeni sygnałów \(x:T\to\mathbb{R}^d\) — Aksjomat
  G6a) ani gałęzi K (brak operatora rezonansu — Aksjomat G5); nie ma
  własnego "rezonansu geometrycznego" w tym wydaniu.

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
- **Aksjomaty:** 10 — `Axioms_K_TIMDR.md` (numeracja 1-10).
- **Status empiryczny:** brak realnej walidacji empirycznej udokumentowanej
  w tym repo (w odróżnieniu od gałęzi M/S) — status nieokreślony wprost
  w samym pliku źródłowym; traktować jako co najmniej tak samo
  koncepcyjny jak gałąź G, dopóki nie powstanie odpowiednik
  `REAL_DATA_VALIDATION.md` dla K.
- **Pliki źródłowe:** `Axioms_K_TIMDR.md`, `Operators_N_TIMDR.md`
  (operatory dla domeny modalnej, w tym skręt topologiczny τ).
- **Czym NIE jest:** rozszerzeniem gałęzi M/S (rezonans modalny to
  wyrównanie częstotliwości/fazy, nie koincydencja progowa amplitud w
  czasie — jawnie rozróżnione w Axioms_S Aksjomat 3) ani gałęzi G
  (moduły \((f,\phi,A)\) nie są punktami powierzchni ani polem
  normalnych).

---

## Tabela porównawcza (jedna strona, cały ekosystem)

| | **M/S — sygnałowa** | **G — geometryczna** | **K — modalna** |
|---|---|---|---|
| Domena | \(x:T\to\mathbb{R}^d\) (szereg czasowy) | \(S\subset\mathbb{R}^3\) (powierzchnia/siatka) | \(T=(X,\tau)\), moduły \((f,\phi,A)\) |
| "Rezonans" | koincydencja progowa \(\geq K\) parametrów naraz | **brak operatora** (Aksjomat G5) | wyrównanie częstotliwość/faza |
| "Skręt" | odwrócenie trendu (regresja) | zmiana normalnej \(T_S\), związana z krzywizną (G8-G9) | *(nieużywane w tej gałęzi)* |
| "Anomalia" | \(\mathbb{1}[\lvert x_i-\mu_i\rvert>2\sigma_i]\) | *(nieużywane w tej gałęzi)* | *(nieużywane w tej gałęzi)* |
| Liczba aksjomatów | 13 | 9 | 10 |
| Status | częściowo zwalidowana empirycznie (realne dane, honest negative/inconclusive) | koncepcyjna, związek z krzywizną domknięty analitycznie | koncepcyjna, brak udokumentowanej walidacji |
| Plik źródłowy | `Axioms_S_TIMDR_Signal.md` | `Axioms_G_TIMDR_Geometry.md` | `Axioms_K_TIMDR.md` |

**Puste komórki są zamierzone**, nie przeoczeniem: brak operatora
rezonansu w G (Aksjomat G5) i brak użycia "skrętu"/"anomalii" w K są
jawnymi stwierdzeniami o zakresie każdej gałęzi, nie lukami do
wypełnienia.

---

Powiązane: [`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md),
[`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md),
[`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md), [`TIMDR_Twists.md`](./TIMDR_Twists.md)
(rozwinięcie wiersza "Skręt" powyżej na cztery znaczenia z pełnymi
definicjami), [`Resonance_M_Operator_Empiryczny.md`](./Resonance_M_Operator_Empiryczny.md),
[`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md) (krótkie, dwujęzyczne
wpisy — ten dokument jest ich strukturalnym rozwinięciem na poziomie
całych gałęzi, nie pojedynczych słów).
