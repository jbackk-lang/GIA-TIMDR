# Operator G-Rezonans — Aksjomat G5 gałęzi geometrycznej

**Status:** zaimplementowany i przetestowany numerycznie (17/17 nowych
testów w `tests/test_geometric_resonance_operator.py`, plus 6/6
istniejących testów trójwęzła bez zmian w
`tests/test_trefoil_resonance_model.py`) dla dowolnej liczby węzłów
\(N\geq3\), z walidacją strukturalną (nie empiryczną) ogólności kodu.
**Nie jest** zwalidowany na realnej, zmierzonej krzywej 3D — patrz §4.

Ten dokument opisuje podniesienie prototypu z
[`TIMDR_Trefoil_ResonanceModel.md`](./TIMDR_Trefoil_ResonanceModel.md)
(zbudowanego i przetestowanego wyłącznie dla trójwęzła, N=3) do rangi
formalnego operatora gałęzi geometrycznej G —
**Aksjomat G5** w `docs/theory/Axioms_G_TIMDR_Geometry.md`, zastępujący
wcześniejszą wersję tego aksjomatu, która jawnie stwierdzała brak
takiego operatora. Zrobione na wyraźną prośbę użytkownika: "Dodać
G-Rezonans jako pełnoprawny operator, analogicznie do M-Rezonansu i
K-Rezonansu."

## 0. Dlaczego to w ogóle jest gałąź G, a nie K

Zanim jest matematyka: to samo pytanie, które ekosystem TIMDR zadaje
sobie przy każdym współdzieleniu słowa. \(\mathcal{R}_G\) operuje na
**krzywej z węzłami mechanicznymi** (masy, sprężyny, tłumienie) — układ
fizyczny drugiego rzędu w sensie równań różniczkowych. Rezonans modalny
K (`Axioms_K_TIMDR.md`, Aksjomat 5) operuje na **modułach fal**
\((f,\phi,A)\) na przestrzeni topologicznej \(T=(X,\tau)\) — wyrównanie
parametrów, nie układ dynamiczny drugiego rzędu. Domeny są rozłączne;
jedyne co łączy oba obiekty to potoczne słowo "częstość własna". Patrz
Aksjomat G6b (zaktualizowany razem z G5) za formalne stwierdzenie tego
rozróżnienia.

## 1. Definicja formalna (streszczenie Aksjomatu G5)

Pełny tekst: `docs/theory/Axioms_G_TIMDR_Geometry.md`, Aksjomat G5
(G5a-G5f). W skrócie:

| | |
|---|---|
| **Domena** | Zamknięta krzywa \(C\subset\mathbb{R}^3\) z \(N\geq3\) węzłami sprzężenia \(p_0,\dots,p_{N-1}\) rozłożonymi cyklicznie; węzeł \(i\) niesie krzywiznę \(\kappa_i\), segment \(i\to(i{+}1)\bmod N\) niesie torsję \(\tau_i\). |
| **Przeciwdziedzina** | Widmo rezonansowe \(\Sigma=(\{\omega_k\},\{Q_k\},A(\omega))\). |
| **Definicja** | \(Mx''+\Gamma x'+Kx=F(t)\), \(K_{ii}=k_{\text{scale}}\kappa_i+kc_{\text{scale}}(\lvert\tau_{i-1}\rvert+\lvert\tau_i\rvert)\), \(K_{i,i+1}=-kc_{\text{scale}}\lvert\tau_i\rvert\); pobudzenie lokalne \(F(t)=F_0\cos(\omega t)e_j\); odpowiedź ustalona \(X(\omega)=(K-\omega^2M+i\omega\Gamma)^{-1}F\). |
| **Warunek stabilności** | \(M,K,\Gamma\) ściśle dodatnio określone \(\Rightarrow\) \(\det(K-\omega^2M+i\omega\Gamma)\neq0\) dla każdego rzeczywistego \(\omega\) \(\Rightarrow\) odpowiedź skończona dla każdego skończonego pobudzenia (brak "destrukcyjnego" nietłumionego rezonansu). |
| **Defekt** | Perturbacja \(D_i(\Delta\kappa_i,\Delta\tau_i)\) zmienia \(K\) i przez to \(\Sigma\) — jakościowo różny odcisk widmowy per typ defektu (§3). |

## 2. Implementacja

`core/geometric_resonance_operator.py` — operator ogólny:

- `build_ring_matrices(n_nodes, kappa, tau, m=None, gamma=0.08, k_scale=1.0, kc_scale=1.0)`
  — buduje `M, K, Γ` dla dowolnego \(N\geq3\). Odrzuca \(N<3\) (przy
  \(N=2\) "pierścień" degeneruje się do dwóch nierozróżnialnych
  sprzężeń między tą samą parą węzłów — jawnie wykluczone, nie cicho
  tolerowane).
- `natural_frequencies`, `steady_state_response`, `find_peaks`,
  `estimate_Q`, `default_omega_sweep` — identyczne API co w
  pierwotnym prototypie trójwęzła, ale N-niezależne (żadna z tych
  funkcji nigdy nie zakładała N=3 nawet w pierwotnej wersji — patrz
  §2.1).
- `is_stable(M, K, Gamma)` — **nowość**, formalny predykat Warunku
  Stabilności (G5d), zastępujący nieformalne porównanie Q z testów
  trójwęzła (`Q < 3*Q0`) jawnym, sprawdzalnym kryterium algebraicznym
  (dodatnia określoność trzech macierzy). Nigdy nie rzuca wyjątku.

`core/trefoil_resonance_model.py` — **cienka warstwa kompatybilności**
(N=3, stałe geometryczne idealnego trójwęzła \(\kappa=0{,}2062\),
\(\tau=0{,}3509\)): `build_matrices()` teraz woła
`build_ring_matrices(3, ...)` z `k_scale=kc_scale=1.0` (bo `k0`/`kc0` w
tej warstwie są już w jednostkach mechanicznych, nie surową
geometrią); pozostałe funkcje są **re-eksportem tych samych obiektów**
(`is` identyczność sprawdzona testem, nie tylko równość wyniku) — nie
ma dwóch równoległych implementacji do rozjechania się w przyszłości.

### 2.1 Dlaczego to było łatwe do uogólnienia

Cztery z sześciu funkcji pierwotnego prototypu (`natural_frequencies`,
`steady_state_response`, `find_peaks`, `estimate_Q`,
`default_omega_sweep`) nigdy nie odwoływały się do liczby węzłów wprost
— działały na macierzach o dowolnym wymiarze already. Jedyną funkcją
zakodowaną na sztywno dla N=3 była `build_matrices` (ręcznie wypisany
słownik trzech par sąsiadów). Uogólnienie sprowadziło się więc do
zastąpienia tego jednego miejsca pętlą po \(N\) węzłach
(`build_ring_matrices`) — nie przepisania całego modułu.

## 3. Wyniki testów

**Regresja (`TestBackwardCompatibilityZTrojweztem`, 2 testy):**
`trefoil_resonance_model.build_matrices()` daje macierze identyczne
bit-w-bit (`np.array_equal`, nie `allclose`) z rekonstrukcją przez
`build_ring_matrices()`, dla defektu zerowego i niezerowego
(`defect_r1`, `defect_tau1` w różnych kombinacjach). Funkcje
re-eksportowane są sprawdzone na tożsamość obiektu (`is`), nie tylko
równoważność wyniku.

**Ogólność (`TestOgolnoscDowolnegoN`, 5 testów):** dla pierścienia
SYMETRYCZNEGO (jednakowe \(\kappa,\tau\)) macierz \(K\) jest
cyrkulantowa — jej widmo ma znaną postać analityczną
\(\lambda_j=k_0+2k_c(1-\cos(2\pi j/N))\), niezależną od testowanego
kodu. Sprawdzone dla \(N\in\{3,4,5,6,8\}\) — zgodność do `1e-9`.
Dodatkowo: \(N=4\) ma jakościowo INNĄ strukturę degeneracji niż \(N=3\)
(singlet-dublet-singlet zamiast singlet-dublet) i test to explicite
sprawdza; defekt na jednym węźle pierścienia \(N=5\) łamie symetrię
tym samym mechanizmem co w trójwęźle; pełny potok (macierze → skan →
odpowiedź → piki) działa end-to-end dla \(N=6\).

**Warunek stabilności (`TestWarunekStabilnosciG5d`, 4 testy):**
`is_stable()` poprawnie zwraca `True` dla układu bazowego, `False` gdy
tłumienie jest zerowe na którymkolwiek węźle, `False` gdy sztywność
węzła jest na tyle ujemna, że psuje dodatnią określoność \(K\), i nigdy
nie rzuca wyjątku na niepoprawnym (niekwadratowym) wejściu.

**Walidacja wejścia (`TestWalidacjaWejscia`, 3 testy):** `N<3`,
niedopasowana długość `kappa`/`tau`/`m` — wszystkie jawnie odrzucane z
czytelnym `ValueError`, nie cichym błędem numerycznym dalej w potoku.

Razem: **17/17** nowych testów, **6/6** istniejących testów trójwęzła
bez regresji, pełny zestaw repo (poza jednym, wcześniej istniejącym,
niezwiązanym błędem importu w `tests/test_operators_wiring.py` —
patrz §5): **82/82**.

## 4. Status walidacji — czego NIE zrobiono

To jest ta sama dyscyplina, co w każdym innym dokumencie tej sesji
(`TIMDR_Trefoil_RealDataValidation.md`,
`TIMDR_Trefoil_MissingCoordinateSolver.md`): oddzielić "zbudowane i
poprawne na kontrolowanych przykładach" od "użyteczne w praktyce".

- **Zero walidacji empirycznej.** Operator nie był uruchomiony na
  ŻADNEJ realnej, zmierzonej krzywej 3D — tylko na geometrii idealnego
  trójwęzła (analityczny wzór) i na syntetycznych pierścieniach
  symetrycznych zbudowanych do testu teorii cyrkulantowej. Kontrast z
  gałęzią sygnałową M/S, gdzie realna walidacja już się odbyła.
- **Stałe modelowe nieskalibrowane.** `k_scale`, `kc_scale`, `gamma`
  (przejście geometria → mechanika) są wyborem modelowym — ten sam
  status co `min_curvature` w `the_geo_pro_4d.py` czy `K_SCALE`/
  `KC_SCALE` w pierwotnym prototypie trójwęzła. Nic w tej aktualizacji
  tego nie zmienia.
- **`Δz` (przesunięcie węzła wzdłuż krzywej) wciąż nie jest
  reprezentowane** w macierzach `M/K/Γ` — dziedziczone ograniczenie z
  prototypu trójwęzła, nie naprawione przy uogólnianiu.
  Uogólnienie na dowolne N NIE rozwiązało tego braku, bo dotyczy on
  reprezentacji defektu, nie liczby węzłów.
- **"Ogólność" tutaj znaczy "kod nie jest zahardkodowany na N=3"**, NIE
  "sprawdzone na innej realnej figurze geometrycznej". Testy §3 używają
  syntetycznych, idealnie symetrycznych pierścieni i porównania z
  czystą teorią cyrkulantową — mocny dowód poprawności KODU, żaden
  dowód przydatności PRAKTYCZNEJ na innej krzywej.
- **Próba praktycznego zastosowania figury trójwęzła (jako model
  sygnału, nie jako G-Rezonans) na realnych danych pogodowych już dała
  wynik negatywny** (`TIMDR_Trefoil_RealDataValidation.md`) — z innych,
  niezależnych przyczyn (artefakty progu na realnych szeregach
  czasowych). To NIE jest test tego operatora, ale przypomnienie, że w
  tym ekosystemie "matematycznie poprawne i przetestowane" i
  "praktycznie użyteczne na realnych danych" to systematycznie mylone,
  odrębne twierdzenia.

## 5. Znaleziona przy okazji, niezwiązana usterka

Podczas uruchamiania pełnego zestawu testów repo (`pytest` bez
filtrów) w trakcie tej pracy, `tests/test_operators_wiring.py` nie
przechodzi kolekcji: `ImportError: cannot import name 'RESONANCE_MAX_K'
from 'core.constants'`. Zweryfikowane jako PRZEDISTNIEJĄCE — plik
pochodzi z wcześniejszej, osobnej partii pracy (commit
`767c0bc`, dane z 31 sierpnia), niezwiązanej z operatorem G-Rezonans;
nie naprawione tutaj (poza zakresem tego zadania), odnotowane zamiast
przemilczane, zgodnie z konwencją tego repo.

## Źródła

- Kod: [`../../core/geometric_resonance_operator.py`](../../core/geometric_resonance_operator.py)
  (operator ogólny), [`../../core/trefoil_resonance_model.py`](../../core/trefoil_resonance_model.py)
  (warstwa N=3)
- Testy: [`../../tests/test_geometric_resonance_operator.py`](../../tests/test_geometric_resonance_operator.py),
  [`../../tests/test_trefoil_resonance_model.py`](../../tests/test_trefoil_resonance_model.py)
- Aksjomat: [`../theory/Axioms_G_TIMDR_Geometry.md`](../theory/Axioms_G_TIMDR_Geometry.md) (G5)
- Specyfikacja gałęzi: [`../theory/TIMDR_Branch_Specification.md`](../theory/TIMDR_Branch_Specification.md)
- Prototyp/geneza: [`TIMDR_Trefoil_ResonanceModel.md`](./TIMDR_Trefoil_ResonanceModel.md),
  [`TIMDR_Trefoil_FrenetTorsion.md`](./TIMDR_Trefoil_FrenetTorsion.md)
- Uczciwy wynik negatywny praktycznego zastosowania (inny obiekt, ta
  sama figura): [`TIMDR_Trefoil_RealDataValidation.md`](./TIMDR_Trefoil_RealDataValidation.md)
- Rozgraniczenie znaczeń "rezonans": [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md),
  [`../theory/Resonance_M_Operator_Empiryczny.md`](../theory/Resonance_M_Operator_Empiryczny.md) §0
