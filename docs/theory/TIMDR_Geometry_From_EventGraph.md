# Geometria z grafu zdarzeń — Φ_G, konstrukcja v0.1

Stan: 23 września 2026 r. Definicje, przykłady analityczne i testy syntetyczne.
Źródło: [graf TRM/GIA i mapa odwzorowań](TIMDR_EventGraph_Branch_Construction.md).
Kod: [`curve_projection`, `tube_from_frames`](../../core/trm_gia_projections.py).

## 1. Krzywa z uporządkowanych zdarzeń

Zakładamy jedną trajektorię oraz ściśle rosnące czasy t_0<…<t_n i pozycje
p_i∈R³ po selekcji GIA. Dla t∈[t_i,t_{i+1}] definiujemy łamaną:

\[
C(t)=(1-\alpha)p_i+\alpha p_{i+1},\qquad
\alpha=\frac{t-t_i}{t_{i+1}-t_i}.
\]

Mapa Φ_G daje krzywą C⊂R³ wraz z parametryzacją. Zachowuje węzły,
jest zgodna z obrotami i translacjami. Przy stałych czasach i perturbacjach
pozycji ||p_i−p_i'||≤ε interpolacja daje ||C(t)−C'(t)||≤ε, ponieważ
wagi są nieujemne i sumują się do 1.

Jednoczesne zdarzenia w różnych miejscach wymagają identyfikatorów torów
lub innego jawnego porządku. Kod odrzuca powtórzone czasy, zamiast zgadywać
połączenia. Porządek czasowy nie gwarantuje ścieżki po krawędziach grafu:
jeśli wymagana jest zgodność z krawędziami, trzeba dostarczyć i sprawdzić
odpowiednią ścieżkę. Odcinki zerowej długości są odrzucane.

## 2. Krzywizna krzywej

Łamana jest ciągła i odcinkami liniowa; w jej narożnikach klasyczna
krzywizna różniczkowa nie jest określona. Można zastosować osobno określoną
krzywiznę dyskretną albo interpolant C klasy C² o ||C'||>0:

\[
\kappa(t)=\frac{\|C'(t)\times C''(t)\|}{\|C'(t)\|^3}.
\]

Wybór interpolantu i jego wygładzenia jest częścią adaptera. Normalna
Freneta wymaga κ>0; na odcinkach prostych potrzebna jest inna ramka,
np. ramka Bishopa z podaną normalną początkową. Sama normalna do krzywej
nie jest jeszcze polem normalnych powierzchni.

## 3. Wstęga jako minimalna powierzchnia pomocnicza

Dla gładkiej krzywej C(s), najlepiej parametryzowanej długością łuku,
oraz gładkiego jednostkowego pola n(s) prostopadłego do C'(s):

\[
S_{\mathrm{wstęga}}(s,r)=C(s)+r\,n(s),\qquad r\in(-a,a).
\]

To powierzchnia o dwóch parametrach (s,r). Warunek regularności:
(C'(s)+r n'(s))×n(s)≠0. W pobliżu r=0 zachodzi lokalnie dzięki
prostopadłości n i C'; szerokość a musi być dobrana do konkretnej krzywej.
Dla C(s)=(s,0,0), n=(0,1,0) otrzymujemy płaską wstęgę (s,r,0), której
obie krzywizny główne wynoszą zero.

## 4. Rura i rola promienia

Dla ortonormalnej ramki normalnej n_1(s), n_2(s) oraz **ustalonego** r_0>0:

\[
S_{r_0}(s,\theta)=C(s)+r_0\left(\cos\theta\,n_1(s)
+\sin\theta\,n_2(s)\right),\quad \theta\in[0,2\pi).
\]

Można zapisać rodzinę S(s,r,θ), ale powierzchnią rury jest przekrój
r=r_0. Swobodne trzy parametry opisują obszar przestrzenny. Lokalnie
wystarczy r_0 κ(s)<1 dla regularnej gładkiej krzywej z ramką normalną;
brak globalnych samoprzecięć wymaga dodatkowo kontroli odległości
między oddalonymi fragmentami krzywej.

`tube_from_frames` próbkuje ten wzór z dostarczonych ramek. Sprawdza
ortogonalność i normy n_1,n_2. Gładkość ramki, jej prostopadłość do stycznej,
regularność powierzchni i samoprzecięcia pozostają warunkami wejściowymi;
funkcja nie rekonstruuje ich z samej listy punktów.

## 5. Operator Weingartena i interpretacja

Dla regularnej powierzchni S klasy C² definiujemy
N=(S_u×S_v)/||S_u×S_v|| oraz W=−dN działające na płaszczyźnie stycznej.
Po próbkowaniu potrzebna jest również jawna triangulacja, spójna orientacja
i obsługa brzegów, zgodnie z implementacją
[Geometry-Formalism](../../TIMDR-Geometry-Formalism/).

**Wstęga i rura są konstrukcjami pomocniczymi do użycia operatora
Weingartena.** Ich geometria zależy od krzywej, ale też od ramki,
szerokości/promienia i sposobu rekonstrukcji. Interpretacja wraca do
krzywej przez te jawne parametry; nie jest bezpośrednim pomiarem fizycznej
powierzchni ani automatycznym wynikiem B4 na zmierzonej geometrii.

Przykład: dla C(s)=(s,0,0), n_1=(0,1,0), n_2=(0,0,1) powstaje walec.
Przy W=−dN i normalnej skierowanej na zewnątrz krzywizny główne wynoszą
0 i −1/r_0; H=−1/(2r_0), a krzywizna Gaussa 0. Krzywa środkowa ma κ=0.
Zatem niezerowa średnia krzywizna rury pochodzi tutaj z promienia, a nie
z zakrzywienia toru. Zmiana r_0 zmienia wynik bez zmiany danych zdarzeń.

## 6. Status konstrukcji

Φ_G dostarcza krzywą z grafu; wstęga/rura rozszerza ją o jawne dane
konstrukcyjne do powierzchni. To konkretne powiązanie TRM/GIA z obiektami
gałęzi G. Stabilność pozycji interpolowanej krzywej nie daje automatycznie
stabilności jej drugich pochodnych lub estymatora Weingartena — te własności
wymagają warunków gładkości, rozdzielczości i osobnych testów.
