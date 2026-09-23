# TRM/GIA → gałęzie TIMDR — konstrukcja referencyjna v0.1

Data: 23 września 2026 r. Status: **jawna konstrukcja matematyczna z kodem
i kontrolami syntetycznymi**. Rozwija [szkic architektury](../../ARCHITEKTURA_TIMDR.md).
Cel: z jednego opisanego grafu zdarzeń zbudować wejścia czterech gałęzi,
z podaniem potrzebnych założeń i sprawdzalnych własności.

## 1. Graf źródłowy

\[
\mathcal G=(V,\mathcal E,w),\qquad w(v_i)=(e_i,t_i,p_i),
\quad e_i\geq0,\quad t_i\in\mathbb R,\quad p_i\in\mathbb R^3.
\]

V jest skończony; identyfikatory są unikalne; wszystkie wagi skończone.
Krawędzie skierowane łączą istniejące, różne węzły. Symbol e oznacza wagę
energii, a ℰ zbiór krawędzi. Jednostki energii, czasu i pozycji są jawne
w danych. Jest to przyjęty model wejściowy TRM dla tej konstrukcji;
nie zakładamy, że każdy historyczny moduł TRM już generuje ten format.

## 2. Zamrożony operator GIA

Z osobnych pozycji kalibracyjnych wyznaczamy środek c i główny kierunek
PCA u, ||u||=1. Wymagamy dodatniej największej wartości własnej oraz luki
λ_1−λ_2>γλ_1 (γ>0). Przy zdegenerowanym kierunku kod odmawia dopasowania.
Promień a≥0 ustalamy przed oceną nowych danych. Tor odniesienia:
L={c+su:s∈R}. Odległość i selekcja:

\[
d_i=\|(I-uu^T)(p_i-c)\|,\qquad
V'=\{v_i:d_i\leq a\},\qquad
T_{c,u,a}(\mathcal G)=\mathcal G[V'].
\]

Wyjściem jest podgraf indukowany. Ten wariant formalizuje **geometryczny
warunek przynależności do toru**; nazwa „rezonansowy” z architektury nie
dodaje automatycznie warunku rezonansu fazowego K ani koincydencji M/S.

Własności przy zamrożonym c,u,a:

1. **Selekcja:** V'⊆V i ℰ'=ℰ∩(V'×V').
2. **Monotoniczność względem inkluzji grafów:** H⊆G ⇒ T(H)⊆T(G), gdy
   używamy tej samej referencji i tych samych wag wspólnych zdarzeń.
3. **Idempotencja:** T(T(G))=T(G), bo predykat dla każdego zachowanego
   punktu pozostaje ten sam. Iteracja osiąga punkt stały po jednym kroku.
4. **Stabilność z marginesem:** jeśli min_i|d_i−a|=m>0 i każda pozycja
   zmieni się o mniej niż m, zbiór identyfikatorów pozostaje ten sam.
   Dowód: odległość do ustalonej prostej jest 1-Lipschitz.
5. **Zgodność z ruchem sztywnym:** obrót/translacja danych i referencji
   razem zachowują odległości i decyzje. Znak osi u nie zmienia wyniku.

Na granicy d_i=a brak globalnej ciągłości twardej selekcji. Powyższe dowody
nie obejmują ponownego dopasowania PCA po każdej iteracji. PCA jest wrażliwe
na odstające punkty; ta referencja zakłada odpowiedni zbiór kalibracyjny.
Istniejący [odporny filtr GIA](../../filters/_vendor_senscore_gia_filter.py)
ma osobną implementację i testy; v0.1 go nie zastępuje.

## 3. Cztery odwzorowania

| Gałąź | Konstrukcja | Własność i dodatkowe założenie |
|---|---|---|
| M/S | Φ_M/S(G') = energia w koszykach / szerokość koszyka | Zachowuje całkowitą energię; pełny zakres obserwacji, rozłączne koszyki |
| G | Φ_G(G') = interpolowana krzywa przez pozycje | Zachowuje punkty; jedna trajektoria, ścisły porządek czasu; powierzchnia wymaga dodatkowej konstrukcji |
| K | Φ_K(G') = FFT(Φ_M/S(G')) | Dokładna dyskretna rekonstrukcja i Parseval; równy krok czasu, podana konwencja fazy |
| META | Φ_META(G') = (Λ,τ,ρ,J) per okno | Zakresy kanałów, odrębne źródła ρ/J, jawne parametry kalibracji |

Szczegóły: [sygnał z grafu](TIMDR_Signal_From_EventGraph.md),
[krzywa, wstęga i rura](TIMDR_Geometry_From_EventGraph.md).
Mapy zachowują wybrane informacje: Φ_M/S pomija pozycje i krawędzie,
Φ_G pomija energie, META agreguje. Nie są ogólnie odwracalne i nie
utożsamiają gałęzi ze sobą.

## 4. Modalność K

Dla N próbek x_n w równych odstępach Δt:

\[
X_m=\sum_{n=0}^{N-1}x_n e^{-2\pi i mn/N},\qquad f_m=\frac{m}{N\Delta t}.
\]

Dla rzeczywistego x używamy widma jednostronnego: A_m=2|X_m|/N dla
wewnętrznych koszyków; A_0=|X_0|/N, a dla parzystego N również
A_{N/2}=|X_{N/2}|/N. Faza arg(X_m) odnosi się do pierwszej próbki.
Dla zerowej amplitudy faza jest nieokreślona (NaN w kodzie). Konwencja
rekonstrukcji używa cos; dla konwencji sin w gałęzi K należy przesunąć
fazę o +π/2, z osobnym traktowaniem składowej stałej.

Dowody zgodności: odwrotna DFT odtwarza próbki i zachodzi
Σ_n|x_n|²=(1/N)Σ_m|X_m|² dla pełnego widma. Ta norma kwadratowa różni
się od całkowitej energii zdarzeń Σ_i e_i zachowanej przez binning.
Warunki rezonansu K można następnie oceniać na zdefiniowanych modach;
obecność widma sama nie jest dowodem rezonansu.

Przykład syntetyczny: x_n=2+cos(2π·2n/16), Δt=1 daje składową stałą 2
i mod f=0,125, A=1, faza=0. To dokładny przypadek koszykowy. Dla
częstotliwości poza siatką występuje przeciek widma; STFT, wybór okna
i śledzenie modów wymagałyby osobnej wersji adaptera.

## 5. Nowa instancja META dla grafu zdarzeń

Stosujemy rozłączne okna W_k=[b_k,b_{k+1}), co najmniej dwa zdarzenia
o różnych czasach w każdym oknie. Zamrażamy energię odniesienia e_ref,
próg odchylenia q≥0, próg zgodności kierunku c_0∈[0,1], referencję u
oraz ε>0 w jednostkach energii. Dla uporządkowanych zdarzeń w oknie:

\[
d_i=|e_i-e_{\mathrm{ref}}|,\quad
\Lambda_k=\frac{\sigma(e)}{\sigma(e)+|\bar e|+\varepsilon},\quad
\tau_k=\operatorname{mean}_i\frac{|d_{i+1}-d_i|}{t_{i+1}-t_i},\quad
\rho_k=\frac{\#\{i:d_i>q\}}{n_k}.
\]

J korzysta z krawędzi wewnątrz okna. Krawędź o wektorze
v_ij=p_j−p_i jest zgodna z torem, jeśli ||v_ij||>0 oraz
|v_ij·u|/||v_ij||≥c_0. Definiujemy J_k jako frakcję takich krawędzi.
Krawędzie zerowej długości nie są zgodne. Gdy nie ma krawędzi, przyjmujemy
J=0 i zwracamy także ich liczbę. Konwencja ma sens dla grafu z obserwowaną
topologią; brak zmierzonych krawędzi nie może być mylony z ich nieobecnością.

Z konstrukcji 0≤Λ<1, τ≥0 oraz ρ,J∈[0,1]. τ ma jednostkę energii/czas;
zmiana jednostek musi objąć też parametry odniesienia. J zależy od pozycji
i krawędzi, a ρ od energii — żadna z masek nie jest wymuszonym podzbiorem
drugiej. To rozdzielenie źródeł zgodne z META-5, **nie dowód statystycznej
niezależności**. Selekcja GIA może zawęzić zmienność J, co trzeba zmierzyć
w późniejszej kalibracji na danych domenowych.

Stan zapisujemy na początku okna b_k. Operator ewolucji to
M_k=(S_k−S_{k−1})/(b_k−b_{k−1}), a jego wielkość to norma L1, zgodnie
z META-6. Obliczenie wymaga zakończenia danego okna; czas etykiety b_k
nie oznacza dostępności stanu online już na początku okna.

To konkretna instancja kształtu z [Axioms META](Axioms_META_TIMDR.md),
z kontrolami zakresów i źródeł. Nie nadajemy jej automatycznie faz
„stabilna/krytyczna” ani przewagi predykcyjnej: pełne wymagania walidacji
META-8/9 pozostają zadaniem dla osobnego eksperymentu.

## 6. Przykład i odtwarzalność

Z katalogu głównego repo:

```powershell
python -m core.trm_gia_projections
python -m unittest discover -s tests -p test_trm_gia_projections.py -v
```

Wymagania: Python z NumPy; testy korzystają ze standardowego unittest.
Przykład tworzy 16 zdarzeń na prostej z e_i=2+cos(2π·2i/16), czasy i=0,…,15,
oraz jedno zdarzenie poza torem. Referencja jest dopasowana do osobnych
trzech punktów. Selekcja zachowuje 16 zdarzeń, binning daje energię 32,
FFT odzyskuje f=0,125 i A=1, interpolacja zachowuje końce (0,0,0) i (15,0,0).
META ma cztery okna; po trzy wewnętrzne krawędzie na okno i J=1.

17 testów referencyjnych przeszło 23 września 2026 r. Obejmują własności
wyżej, degenerację PCA, skok progu i binningu, normalizację Gaussa,
promień pomocniczej rury, rekonstrukcję FFT, Parsevala i rozdzielenie
źródeł ρ/J. Wynik oznaczono `SYNTHETIC_CONSTRUCTION_CHECK`.

**Osiągnięty krok:** jawna ścieżka od grafu TRM/GIA do reprezentacji
czterech gałęzi, z założeniami i działającym przykładem. Konstrukcja
wiąże ich pochodzenie z konkretnymi mapami; nie wyprowadza wszystkich
aksjomatów ani empirycznej skuteczności gałęzi z samej definicji grafu.
