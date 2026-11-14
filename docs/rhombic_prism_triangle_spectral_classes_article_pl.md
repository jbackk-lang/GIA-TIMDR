# Dwie algebraiczne klasy spektralne komutatorów odbić graniastosłupa rombowego

**Artykuł matematyczny — wersja robocza z odtwarzalnymi certyfikatami obliczeń dokładnych**

## Streszczenie

Badamy trójkątny graniastosłup, którego trzy ściany boczne są rombami, oraz izometrie otrzymane przez porównanie iloczynu trzech obrotów z iloczynem o odwróconej kolejności. W otwartej rodzinie fizycznych kształtów klasyfikujemy konfiguracje, dla których komutator porządków pozostawia środek bryły nieruchomy. Certyfikowana eliminacja wielomianowa prowadzi do dziewięciu różnych konfiguracji, tworzących dwie orbity symetrii o licznościach trzy i sześć. Odpowiadają im dwie rozłączne algebraiczne klasy cosinusa kąta obrotu. Wyprowadzamy ponadto wielomian charakterystyczny dziewięciowymiarowej reprezentacji przez sprzężenie macierzy. Rozdzielamy twierdzenia czysto algebraiczne od etapów wymagających dostarczonych certyfikatów komputerowych.

## 1. Geometria i operatory

Niech
\[
A=(0,0,0),\quad B=(1,0,0),\quad C=(1/2,\sqrt3/2,0)
\]
oraz niech górna podstawa będzie przesunięta o
\[
t=(u,v,w),\qquad w=\sqrt{1-u^2-v^2}>0,\qquad u^2+v^2<1.
\]
Ponieważ \(\|t\|=1\), wszystkie krawędzie boczne mają długość 1, a ściany boczne są rombami. Środek bryły wynosi
\[
O=\left(\frac{1+u}{2},\frac{\sqrt3}{6}+\frac v2,\frac w2\right).
\]
Niech \(s_0\) będzie odbiciem w płaszczyźnie dolnej podstawy, a \(s_2,s_3,s_4\) odbiciami w płaszczyznach bocznych. Definiujemy trzy właściwe izometrie
\[
g_i=s_0s_{i+1}\quad (i=1,2,3).
\]
Dla permutacji \(\sigma=(i,j,k)\) oznaczmy
\[
P_\sigma=g_i g_j g_k,\quad Q_\sigma=g_k g_j g_i,\quad
\Delta_\sigma=P_\sigma Q_\sigma^{-1}.
\]
Przez \(R_\sigma\in SO(3)\) oznaczamy część liniową \(\Delta_\sigma\).
Warunkiem powrotu środka jest \(\Delta_\sigma(O)=O\).

## 2. Twierdzenie główne

**Twierdzenie 1 (klasyfikacja geometryczna i spektralna).**
Dla sześciu kolejności \(\sigma\in S_3\) zbiór fizycznych kształtów
\((u,v)\), dla których \(\Delta_\sigma(O)=O\) dla co najmniej jednej
kolejności, zawiera dokładnie dziewięć elementów. Przy naturalnym
działaniu symetrii trójkąta \(D_3\), obejmującym odpowiednią relabelizację
generatorów, rozkłada się on na orbity liczności 3 i 6.

Każdy z tych dziewięciu kształtów spełnia warunek powrotu dla dokładnie
dwóch kolejności, będących wzajemnymi odwróceniami. Ich macierze obrotu
mają jednakowy ślad. Na orbicie trzy-elementowej
\(\operatorname{tr}R=1+2c_3\), na sześcioelementowej
\(\operatorname{tr}R=1+2c_6\), gdzie
\[
\frac12<c_3<\frac35,\qquad
\frac14<c_6<\frac13.
\]
W szczególności wartości śladu są rozłączne:
\[
2<\operatorname{tr}R_3<\frac{11}{5},
\qquad
\frac32<\operatorname{tr}R_6<\frac53.
\]

**Twierdzenie 2 (widmo operatora sprzężenia).**
Dla dowolnej z powyższych konfiguracji niech
\(\mathcal T_R:M_3(\mathbb R)\to M_3(\mathbb R)\) będzie określony przez
\(\mathcal T_R(X)=RXR^\top\). Wtedy
\[
M_3(\mathbb R)=\mathbb RI\oplus\mathfrak{so}(3)
\oplus\operatorname{Sym}_0(3),\qquad 9=1+3+5,
\]
a przy \(c=(\operatorname{tr}R-1)/2=\cos\theta\)
\[
\boxed{\chi_{\mathcal T_R}(\lambda)=
(\lambda-1)^3(\lambda^2-2c\lambda+1)^2
(\lambda^2-(4c^2-2)\lambda+1).}
\]
W szczególności widmo zespolone to
\[
\{1^{(3)},e^{i\theta\,(2)},e^{-i\theta\,(2)},
e^{2i\theta},e^{-2i\theta}\}.
\]

## 3. Eliminacja algebraiczna i liczba kształtów

Podstawmy \(z=v/\sqrt3\). Dokładna baza Gröbnera układu powrotu
środka, po usunięciu czynnika niezerowego w otwartym dysku fizycznym,
zawiera równanie liniowe wyznaczające \(u=U(z)\) oraz eliminant
proporcjonalny do
\[
(z^2-1)F_5(z)F_8(z),
\]
gdzie
\[
F_5(z)=1152z^5+264z^4-132z^3-33z^2+4z+1,
\]
\[
\begin{split}
F_8(z)={}&12544z^8-448z^7-18432z^6-248z^5\\
&+6968z^4+1668z^3-945z^2-372z-27.
\end{split}
\]
Izolacja rzeczywistych pierwiastków przedziałami wymiernymi oraz
dokładne oszacowanie \(u(z)^2+3z^2\) dowodzą, że dla kolejności
\((1,2,3)\) występują dokładnie trzy pierwiastki w otwartym dysku.
Z symetrii cyklicznej uzyskuje się trzy rodziny po trzy kształty.
Dokładna arytmetyka przedziałowa wykazuje parami rozłączność wszystkich
dziewięciu prostokątów izolujących. Działanie \(D_3\) łączy pierwiastek
osiowy w orbitę trzy-elementową, a dwa pozostałe w orbitę
sześcioelementową.

**Zakres certyfikacji.** Izolacja, liczba pierwiastków i rozłączność
dziewięciu przedziałów są wykonywane dokładnie w skrypcie
\`rhombic_prism_triangle_nine_exact_certificate.py\`. Przeniesienie
wyników między kolejnościami korzysta z wcześniej sprawdzonej
kowariancji symetrii trójkąta; nie jest wnioskiem z samego liczenia
pierwiastków.

## 4. Ścisły lemat o odwróceniu kolejności

**Lemat 3.** Dla dowolnych trzech odwracalnych izometrii \(g_i,g_j,g_k\),
bez jakichkolwiek założeń geometrycznych,
\[
\Delta_{(k,j,i)}=\Delta_{(i,j,k)}^{-1}.
\]

**Dowód.** Dla \(\sigma=(i,j,k)\) mamy \(P_\sigma=g_i g_j g_k\)
i \(Q_\sigma=g_k g_j g_i\). Dla kolejności odwróconej
\(P_{\sigma^{\rm rev}}=Q_\sigma\) oraz
\(Q_{\sigma^{\rm rev}}=P_\sigma\). Zatem
\[
\Delta_{\sigma^{\rm rev}}=
Q_\sigma P_\sigma^{-1}
=(P_\sigma Q_\sigma^{-1})^{-1}=\Delta_\sigma^{-1}.
\]
Ponadto \(\Delta_\sigma(O)=O\) wtedy i tylko wtedy, gdy
\(\Delta_\sigma^{-1}(O)=O\). Dla części liniowej,
\(R_{\sigma^{\rm rev}}=R_\sigma^{-1}=R_\sigma^\top\), a więc
\[
\operatorname{tr}R_{\sigma^{\rm rev}}
=\operatorname{tr}R_\sigma.
\]
\(\square\)

**Wniosek 4.** Trzy pary kolejności
\[
(123,321),\qquad(231,132),\qquad(312,213)
\]
mają parami identyczne zbiory kształtów powrotu środka.
Certyfikowana rozłączność trzech rodzin cyklicznych dowodzi, że żaden
kształt nie należy do dwóch różnych par. Wobec tego każdy z dziewięciu
kształtów ma dokładnie dwie dopuszczalne kolejności, o tym samym śladzie.

**Uwaga.** Ten argument nie mówi, że wszystkie sześć kolejności ma ten
sam ślad przy ustalonym kształcie. Równość dotyczy wyłącznie dwóch
kolejności, dla których środek rzeczywiście powraca.

## 5. Dokładne wielomiany obu klas

Eliminacja parametru \(z\) z warunku powrotu oraz
\(c=(\operatorname{tr}R-1)/2\) prowadzi do wielomianów
\[
\begin{split}
H_3(c)={}&3439853568c^5-174103840768c^4\\
&+3145786042786c^3-590528708979c^2\\
&+2034692645632c-1345672319791,
\end{split}
\]
\[
\begin{split}
H_6(c)={}&411102815929c^4-22711964978020c^3\\
&+103536116470230c^2-164124750044260c\\
&+38719737491257.
\end{split}
\]
Oba są nierozkładalne nad \(\mathbb Q\), a
\(\gcd(H_3,H_6)=1\). Metoda Sturma daje dokładnie jeden
pierwiastek \(H_3\) w \((1/2,3/5)\) i dokładnie jeden
pierwiastek \(H_6\) w \((1/4,1/3)\). Wybór pierwiastków
odpowiadających fizycznym orbitom wynika z połączenia eliminacji
z certyfikatem lokalizacji rozwiązań geometrycznych.

Dla \(F_5\) resultant ma czynnik \(H_3\) z krotnością 1,
natomiast dla \(F_8\) pojawia się \(H_6^2\).
Stopnie algebraiczne cosinusów wynoszą zatem odpowiednio 5 i 4.

## 6. Dowód twierdzenia spektralnego

Niech \(R\in SO(3)\) ma kąt \(\theta\in[0,\pi]\). Jego wartości
własne nad \(\mathbb C\) to \(1,e^{i\theta},e^{-i\theta}\).
Działanie \(X\mapsto RXR^\top\) na \(M_3(\mathbb C)\)
jest równoważne działaniu tensorowemu \(R\otimes R\);
jego wartości własne są wszystkimi dziewięcioma iloczynami
par wartości własnych \(R\). Zliczenie krotności daje
\(1\) trzykrotnie, \(e^{\pm i\theta}\) po dwa razy i
\(e^{\pm2i\theta}\) po jednym razie. Ponieważ
\(2\cos2\theta=4c^2-2\), otrzymujemy wzór z Twierdzenia 2.

Rozkład na macierze skalarne, antysymetryczne i symetryczne
bezśladowe jest ortogonalny względem iloczynu Frobeniusa
i zachowany przez sprzężenie ortogonalne. Wymiary wynoszą
odpowiednio \(1,3,5\). To kończy dowód. \(\square\)

Dla obu rozważanych kątów, bez degeneracji wartości własnych,
wielomian minimalny \(\mathcal T_R\) **nad \(\mathbb Q(c)\)**
ma postać
\[
(\lambda-1)(\lambda^2-2c\lambda+1)
(\lambda^2-(4c^2-2)\lambda+1).
\]
Nie należy utożsamiać go z wielomianem minimalnym nad
\(\mathbb Q\) ani utożsamiać dziewięciu kształtów z wymiarem
dziewięciowym przestrzeni macierzy: są to dwa odrębne znaczenia
liczby dziewięć.

## 7. Odtwarzalność i ograniczenia

Wszystkie wskazane skrypty znajdują się w katalogu
\`experiments/\`:

- \`rhombic_prism_triangle_reduced_equations.py\` — równania powrotu;
- \`rhombic_prism_triangle_nine_exact_certificate.py\` — izolacja
  wymierna i dziewięć rozłącznych kształtów;
- \`rhombic_prism_triangle_exact_cosine.py\` — resultants i
  nierozkładalność wielomianów cosinusów;
- \`rhombic_prism_triangle_spectral_separation.py\` — metoda Sturma
  i rozdzielenie śladów;
- \`rhombic_prism_triangle_exact_order_trace.py\` — dokładna
  tożsamość odwrócenia i certyfikat jednoznaczności pary;
- \`rhombic_prism_triangle_nine_symbolic_spectrum.py\` —
  dziewięciowymiarowy wielomian charakterystyczny;
- \`rhombic_prism_triangle_nine_spectral_orbits.py\` —
  niezależny test numeryczny dziewięciu kształtów i kolejności.

Pełny argument ma charakter **dowodu wspomaganego obliczeniami
symbolicznymi i certyfikatami przedziałowymi**, a nie krótkiego
ręcznego wyprowadzenia wszystkich współczynników wielomianów.
Testy numeryczne pełnią rolę kontroli niezależnej; nie zastępują
dokładnej izolacji ani tożsamości grupowych. Artykuł nie zawiera
twierdzeń o dowolnych graniastosłupach ani roszczeń do nowości
samego rozkładu reprezentacji \(1+3+5\).

## 8. Konkluzja

Warunek powrotu środka dla porządkowo zależnego komutatora odbić
wyróżnia dziewięć fizycznych kształtów w badanej rodzinie.
Symetria trójkąta organizuje je w orbity \(3+6\), a ślad obrotu
rozdziela te orbity za pomocą dwóch dokładnie określonych liczb
algebraicznych. Indukowany operator na macierzach \(3\times3\)
ma uniwersalny rozkład \(1+3+5\) i jawny wielomian
charakterystyczny, co daje pełną charakterystykę spektralną
obu klas.
