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
(związek skrętu z krzywizną przez operator Weingartena) bez podania
implementacji — to zamierzone, nie przeoczenie: patrz zastrzeżenie pod
G4.

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
zobowiązuje przyszłą implementację do zgodności z nią.)*

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
  wymaga: (1) pełnej definicji \(W_S\), (2) formalnej przestrzeni
  powierzchni, (3) testów empirycznych, (4) niezależnej walidacji.

---

## Mapowanie aksjomatów G na README / repo

| Aksjomat | Odniesienie |
|---|---|
| G1-G2 | Sekcja 1 głównego `README.md` GIA-TIMDR (model trójkąta, asymetria, impuls) |
| G3-G4 | Skręt powierzchniowy w `Resonance_M_Operator_Empiryczny.md` §6, plus sekcje o Mobiosotourys/Tetroidzie (README sekcja 6) |
| G5 | Wiersz "Operator rezonansu: brak" dla gałęzi G w tabeli "Trzy gałęzie TIMDR" (README) |
| G6 | Sekcja "🌿 Trzy gałęzie TIMDR — mapa terenu" w README |
| G7 | Ostrzeżenie na początku README ("model koncepcyjny / narzędzie do myślenia, nie teoria naukowa") |

Powiązane: [`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md) (gałąź modalna),
[`Axioms_S_TIMDR_Signal.md`](./Axioms_S_TIMDR_Signal.md) (gałąź
sygnałowa — sekcja "Pozostałe braki formalne" tam odnosi się wprost do
G4 powyżej), [`Resonance_M_Operator_Empiryczny.md`](./Resonance_M_Operator_Empiryczny.md)
§6 (pierwsze wprowadzenie \(T_S\), przed formalizacją jako G3),
[`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md) (kanoniczne nazwy
"skręt powierzchniowy" i rozgraniczenie od pozostałych trzech znaczeń
skrętu).
