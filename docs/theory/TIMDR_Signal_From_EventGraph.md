# Sygnał z grafu zdarzeń — Φ_M/S, konstrukcja v0.1

Stan: 23 września 2026 r. Definicja konstrukcyjna i testy syntetyczne.
Źródło: [graf TRM/GIA i mapa odwzorowań](TIMDR_EventGraph_Branch_Construction.md).
Kod: [`signal_projection`, `gaussian_signal`](../../core/trm_gia_projections.py).

## 1. Od miary zdarzeń do sygnału

Dla skończonego grafu po selekcji GIA, z energią e_i ≥ 0 i czasem t_i,
definiujemy miarę energii:

\[
\mu=\sum_{i\in V'}e_i\delta_{t_i}.
\]

Dirac jest miarą/dystrybucją; aby otrzymać ograniczoną funkcję numeryczną
w rozumieniu [S-1](Axioms_S_TIMDR_Signal.md), wybieramy operator pomiarowy.
Energia e_i jest tu wagą zdarzenia w zadanych jednostkach, np. J; jej fizyczne
znaczenie i kalibrację ustala źródło danych.

## 2. Binning i dokładne zachowanie energii

Wybieramy Δt > 0, b_k = T_min + kΔt, k=0,…,N, oraz rozłączne koszyki
B_k=[b_k,b_{k+1}). Wszystkie zdarzenia muszą należeć do [T_min,T_max),
gdzie T_max=b_N. Zdarzenie dokładnie w T_max wymaga rozszerzenia zakresu.
Środek koszyka to c_k=b_k+Δt/2. Definiujemy:

\[
K(u)=\mathbf1_{(-1/2,\,1/2]}(u),\qquad
x_k=\frac1{\Delta t}\sum_i e_i K\!\left(\frac{c_k-t_i}{\Delta t}\right)
=\frac{\mu(B_k)}{\Delta t}.
\]

Półotwarty przedział usuwa niejednoznaczność na granicy; każdy impuls trafia
dokładnie do jednego koszyka. Zapis z samym |c_k−t_i|<Δt/2 pomijałby
zdarzenia dokładnie na granicach, dlatego potrzebna jest ta konwencja.
**Dla idealnego, pełnego binningu całkowita energia jest zachowana dokładnie:**

\[
\sum_{k=0}^{N-1}x_k\Delta t=\sum_i e_i.
\]

Dowód: sumując po k, wskaźniki dla każdego t_i sumują się do 1.
x_k ma jednostkę energii/czas, np. W; sama suma w koszyku ma jednostkę energii.
Dla nierównych koszyków kod stosuje x_k=μ(B_k)/(b_{k+1}−b_k), z analogiczną
tożsamością ważoną szerokościami koszyków. Nie nadaje to nierównej siatce
automatycznej zgodności ze zwykłą FFT.

Wielokanałowość wymaga dodatkowo jawnych wag kanałowych a_ij. Wówczas
x_kj=Σ_i a_ij e_i 1_Bk(t_i)/Δt. Zachowanie energii po zsumowaniu kanałów
wymaga a_ij≥0 i Σ_j a_ij=1. Referencyjny kod v0.1 implementuje jeden kanał.

## 3. Przykład i skoki na granicach

Dla Δt=1 s i zdarzeń (t,e)=(0,1),(1,2),(2,3),(3,4) sygnał wynosi
[1,2,3,4] J/s, a energia całkowita 10 J.

| Impuls o energii 1 J | Koszyk [0,1) | Koszyk [1,2) |
|---|---:|---:|
| t=1−ε | 1 J/s | 0 J/s |
| t=1+ε | 0 J/s | 1 J/s |

**Na granicach koszyków występują skoki binningu; są artefaktem dyskretyzacji,
nie dynamiki zdarzenia.** Dla dowolnie małego ε>0 norma L1 różnicy powyższych
wektorów wynosi 2 J/s. Binning nie jest więc globalnie ciągły względem czasu
zdarzeń w tej normie. Jeśli odległość każdego t_i od granic przekracza η,
przesunięcia mniejsze niż η nie zmieniają przypisania. Zmiana przekraczająca
jedną granicę dotyka dwóch sąsiednich koszyków.

## 4. Jądro wygładzające i warunki normalizacji

Dla jądra K≥0, całki ∫K=1 i szerokości h>0:

\[
f_h(t)=\sum_i\frac{e_i}{h}K\!\left(\frac{t-t_i}{h}\right),
\qquad \int_{\mathbb R}f_h(t)\,dt=\sum_i e_i.
\]

Szerokość h i krok próbkowania Δt to dwa oddzielne parametry. Dla Gaussa
K(u)=exp(−u²/2)/√(2π) kod zwraca próbki f_h(t_k). **Suma próbek razy Δt
na skończonej siatce jest przybliżeniem całki**, ponieważ występują błąd
kwadratury i ucięcie ogonów. Sam czynnik 1/Δt nie zapewnia dokładnej sumy
dla dowolnego jądra i dowolnej siatki. **Dla jąder wygładzających (np. Gauss)
na skończonej siatce dokładne zachowanie Σ_k x_kΔt=Σ_i e_i wymaga dodatkowej
normalizacji jądra na siatce, osobno dla każdego zdarzenia.**

Jeżeli potrzebne jest dokładne zachowanie energii na zadanej skończonej
siatce, można zdefiniować w_ki=K((t_k−t_i)/h)/Σ_l K((t_l−t_i)/h), a potem
x_k=Σ_i e_i w_ki/Δt. Warunek: każdy mianownik jest dodatni. Ten wariant
przenosi całą energię na zakres obserwacji i zmienia zachowanie przy brzegu;
nie jest domyślną implementacją v0.1.

Dla K o ograniczonej pochodnej i stałym h, przy |t_i−t_i'|≤ε:

\[
\|f_h-f_h'\|_\infty\leq
\frac{\|K'\|_\infty}{h^2}\,\varepsilon\sum_i e_i.
\]

Wynika to z twierdzenia o wartości średniej. Dla Gaussa
||K'||∞=exp(−1/2)/√(2π). Gauss oddziałuje na wszystkie próbki, z malejącymi
ogonami; ścisłą lokalność daje jądro o zwartym nośniku. Wąskie h zwiększa
wrażliwość na przesunięcia czasowe.

## 5. W jakim sensie odzyskujemy impulsy

Nie ma granicy punktowej będącej zwykłą funkcją równą Diracowi. Zachodzi
**zbieżność słaba miar** f_h(t)dt → μ dla h→0: dla ciągłej funkcji testowej
o zwartym nośniku ψ, ∫ψ(t)f_h(t)dt → Σ_i e_i ψ(t_i).

Dla binningu tę samą własność ma funkcja stała x_k na każdym B_k, gdy
maksymalna szerokość koszyków dąży do zera. Różnica całek jest ograniczona
przez Σ_i e_i razy moduł ciągłości ψ na tej szerokości. Jeżeli całkę
wygładzonego sygnału przybliżamy próbkami, krok siatki musi dodatkowo
rozdzielać szerokość jądra (np. Δt/h→0, z kontrolą zakresu i ogonów).

## 6. Powiązanie z M/S

Φ_M/S dostarcza wejście x. Anomalia, defekt, skręt sygnałowy i rezonans M
pozostają istniejącymi operatorami działającymi na x, z ich własnymi
parametrami i procedurą kalibracji. Konstrukcja zapewnia ograniczoność
skończonego sygnału, liniowość względem energii przy zamrożonej selekcji,
niezmienniczość na zmianę kolejności rekordów i zachowanie energii binningu.
Skuteczność diagnostyczna ich złożenia wymaga osobnego eksperymentu.
