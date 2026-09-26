# Rura analityczna — zwinięcie sygnału i pola w rurę (most M/S ↔ G)

Status: **konstrukcja z testami syntetycznymi** (2026-09-26). Kod: `core/analytic_tube.py`, testy:
`tests/test_analytic_tube.py` (6/6). Nie jest jeszcze wynikiem na danych rzeczywistych.

## 1. Idea (J. Kielich)

Zwinięcie pola to przekształcenie na sygnał w rurze. Formuła istnieje i jest ścisła — to sygnał analityczny (Gabor, 1946).

## 2. Jeden sygnał

Dla rzeczywistego x(t), z transformatą Hilberta H:

\[
z(t) = x(t) + i\,H[x](t) = A(t)\,e^{i\varphi(t)}, \qquad
\Gamma(t) = \big(v t,\; A(t)\cos\varphi(t),\; A(t)\sin\varphi(t)\big).
\]

Krzywa Γ leży na powierzchni obrotowej (rurze) T(t, θ) = (v t, A(t) cos θ, A(t) sin θ) wokół osi czasu:

| Rura | Sygnał |
|---|---|
| promień A(t) | obwiednia (amplituda chwilowa) |
| kąt na obwodzie φ(t) | faza chwilowa |
| tempo skrętu φ′(t) = ω(t) | częstotliwość chwilowa |
| liczba okrążeń (φ(T) − φ(0)) / 2π | `phase_winding_fn` TIMDR (ta sama definicja — test) |
| „oddychanie” rury: widmo A(t) | widmo obwiedni — to czyta sito rezonansowe |

Powrót jest dokładny: x(t) = A(t) cos φ(t). Parametr v (prędkość wzdłuż osi) jest jawnym parametrem konstrukcji,
tak jak promień r₀ rury w `TIMDR_Geometry_From_EventGraph.md` — ale tu promień przestaje być parametrem: jest daną.

## 3. Geometria rury i spirali (operatory gałęzi G)

Rura jako powierzchnia obrotowa o profilu r(u) = A, u = v t, r′ = dr/du (normalna do wnętrza):

\[
\kappa_{\text{merid}} = -\frac{r''}{(1+r'^2)^{3/2}},\quad
\kappa_{\text{równ}} = \frac{1}{r\sqrt{1+r'^2}},\quad
H = \tfrac12(\kappa_{\text{merid}}+\kappa_{\text{równ}}),\quad K = \kappa_{\text{merid}}\kappa_{\text{równ}}.
\]

Walec (stała obwiednia): H = 1/(2A), K = 0 (znak H zależy od orientacji normalnej; w
`TIMDR_Geometry_From_EventGraph.md` przyjęto normalną zewnętrzną, stąd tam −1/(2r₀)).

Spirala (Frenet): κ = |Γ′×Γ″| / |Γ′|³, τ = (Γ′×Γ″)·Γ‴ / |Γ′×Γ″|². Dla tonu (A, ω stałe) — klasyczna helisa:
κ = Aω² / (v² + A²ω²), τ = vω / (v² + A²ω²) (sprawdzone testem).

## 4. Pole → wiązka rur

Pole czas × pasmo (membrana): dla każdego pasma nośnego b sygnał analityczny pasma z_b = A_b e^{iφ_b} (maska widma).
Każde pasmo to własna rura; pole zwinięte to **wiązka rur**. Sito rezonansowe (`bearing_resonance_sieve.py`,
`core/real_paderborn_resonance_sieve.py`) w tym języku: mierzy, jak rury oddychają z częstotliwością uszkodzenia, a oczka
sita ważą rury według siły tego oddychania. Uszkodzenie łożyska = okresowe „pulsowanie” promienia wybranych rur.

## 5. Co daje, a czego jeszcze nie

- Daje ścisły, odwracalny most sygnał ↔ geometria: obwiednia, faza i częstotliwość chwilowa stają się promieniem,
  kątem i skrętem krzywej na powierzchni, więc operatory G (κ, τ, H, K) mają sens fizyczny.
- Porządkuje dotychczasowe wyniki: `phase_winding` = liczba okrążeń rury; sito = widmo oddychania rur.
- **Nie** jest jeszcze sprawdzone, czy nowe wielkości geometryczne rury (np. rozkład κ, τ, H w czasie) dodają informację
  ponad samo widmo oddychania. Test wymaga pre-rejestracji; rezerwa: Paderborn, pomiary 16–20.
- Znane ograniczenia: efekty brzegowe transformaty Hilberta (w testach pomijane 10% brzegów), niejednoznaczność
  częstotliwości chwilowej dla sygnałów wieloskładnikowych (dlatego wiązka rur pasmami, a nie jedna rura).
