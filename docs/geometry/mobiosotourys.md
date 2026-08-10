# Mobiosotourys — torus ze skrętem Möbiusa

Mobiosotourys jest uogólnieniem taśmy Möbiusa i torusa.  
Powstaje przez nałożenie skrętu topologicznego τ na klasyczną parametryzację torusa.  
W granicy \( r \to 0 \) mobiosotourys przechodzi w tetroidę — osobliwość skrętu τ.

---

## 1. Parametryzacja torusa

Klasyczny torus opisujemy równaniami:



\[
\begin{aligned}
x(u,v) &= (R + r \cos v)\cos u, \\
y(u,v) &= (R + r \cos v)\sin u, \\
z(u,v) &= r \sin v,
\end{aligned}
\]



gdzie:
- \(u \in [0,2\pi)\) — parametr główny,
- \(v \in [0,2\pi)\) — parametr przekroju,
- \(R\) — promień główny,
- \(r\) — promień przekroju.

---

## 2. Wprowadzenie skrętu Möbiusa

Skręt Möbiusa wprowadzamy przez przesunięcie fazy:



\[
v \;\rightarrow\; v + \frac{n}{2}u,
\]



gdzie:
- \(n = 1\) — pojedynczy skręt Möbiusa,
- \(n\) nieparzyste → topologia Möbiusa,
- \(n\) parzyste → topologia torusa.

Powierzchnia mobiosotourysa:



\[
\begin{aligned}
x(u,v) &= (R + r \cos (v + \tfrac{n}{2}u))\cos u, \\
y(u,v) &= (R + r \cos (v + \tfrac{n}{2}u))\sin u, \\
z(u,v) &= r \sin (v + \tfrac{n}{2}u).
\end{aligned}
\]



---

## 3. Granica tetroidy

Tetroida jest granicą mobiosotourysa przy:



\[
r \to 0, \qquad n = 1, \qquad \tau = \tau_{\max}.
\]



Formalnie:



\[
T = \lim_{r \to 0} S(u,v; R, r, n=1),
\]



gdzie \(S\) jest powierzchnią mobiosotourysa.

Interpretacja:
- \(r > 0\) → torus ze skrętem Möbiusa,
- \(r \to 0\) → powierzchnia zapada się w tetroidę,
- tetroida jest osobliwością skrętu τ.

---

## 4. Znaczenie w TIMDR

Mobiosotourys opisuje:
- przejście topologiczne torus → Möbius → tetroida,
- koncentrację skrętu τ,
- redukcję złożoności ρ przy \(r \to 0\),
- naturalny ciąg przejść TIMDR:



\[
\text{torus} \;\xrightarrow{n=1}\; \text{mobiosotourys} \;\xrightarrow{r\to 0}\; \text{tetroida}.
\]



Jest to geometryczna realizacja operatora przejścia topologicznego:



\[
\mathbb{T}_p(T_1 \rightarrow T_2) = \Delta \tau.
\]



