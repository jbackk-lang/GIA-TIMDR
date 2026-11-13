# Two spectral classes of the triangular rhombic prism: a certified theorem

## Setup

Let the bottom triangle have vertices
\(A=(0,0,0)\), \(B=(1,0,0)\), \(C=(1/2,\sqrt3/2,0)\).
Translate its upper copy by \(t=(u,v,w)\), where
\(u^2+v^2<1\) and \(w=\sqrt{1-u^2-v^2}>0\).
The three lateral faces are unit-edge rhombi.

Write \(s_0\) for reflection in the bottom plane and \(s_2,s_3,s_4\)
for reflections in the three affine lateral planes. Set
\(g_i=s_0s_{i+1}\), \(i=1,2,3\). For an order \(\sigma\in S_3\), put
\[
P_\sigma=g_{\sigma(1)}g_{\sigma(2)}g_{\sigma(3)},\qquad
Q_\sigma=g_{\sigma(3)}g_{\sigma(2)}g_{\sigma(1)},\qquad
\Delta_\sigma=P_\sigma Q_\sigma^{-1}.
\]
The prism center is
\(O=((1+u)/2,\sqrt3/6+v/2,w/2)\).

## Theorem (nine configurations and two spectral classes)

Across all six generator orders, the physical solutions of
\(\Delta_\sigma(O)=O\) consist of exactly nine distinct shape
parameters \((u,v)\). Under the natural \(D_3\) action that simultaneously
transforms the shape and relabels the side generators, these form two
orbits of cardinalities 3 and 6.

For every shape, all orders satisfying the center-return condition have
the same rotation trace. Consequently, there are exactly two trace
values, \(1+2c_3\) and \(1+2c_6\), respectively, with
\[
\tfrac12<c_3<\tfrac35,\qquad \tfrac14<c_6<\tfrac13.
\]
The corresponding rotation angles are distinct and satisfy
\(\theta_3<\pi/3<\arccos(1/3)<\theta_6\).

The induced conjugation operator on \(M_3(\mathbb R)\),
\(\mathcal T_R(X)=RXR^\top\), has invariant orthogonal splitting
\[
M_3(\mathbb R)=\mathbb RI\oplus\mathfrak{so}(3)
\oplus\operatorname{Sym}_0(3),\qquad 9=1+3+5,
\]
and, for \(c=(\operatorname{tr}R-1)/2\), characteristic polynomial
\[
\chi_{\mathcal T_R}(\lambda)
=(\lambda-1)^3(\lambda^2-2c\lambda+1)^2
(\lambda^2-(4c^2-2)\lambda+1).
\]

## Exact algebraic certificates

The two cosine values satisfy the irreducible polynomials
\[
\begin{aligned}
P_3(c)={}&3439853568c^5-174103840768c^4
+3145786042786c^3\\
&-590528708979c^2+2034692645632c-1345672319791,\\
P_6(c)={}&411102815929c^4-22711964978020c^3
+103536116470230c^2\\
&-164124750044260c+38719737491257.
\end{aligned}
\]
Here \(c_3\) is the unique root of \(P_3\) in \((1/2,3/5)\)
and \(c_6\) the unique root of \(P_6\) in \((1/4,1/3)\).
These are minimal polynomials of the *cosine parameters*, not
minimal polynomials of the 9D operator over \(\mathbb Q\).

## Proof outline and reproducible certificates

1. The affine reflection equations reduce to three polynomials in
   \((u,v)\). Gröbner elimination with \(z=v/\sqrt3\) produces a
   degree-15 eliminant, factoring into \((z-1)(z+1)P_5(z)P_8(z)\).
   Exact rational root isolation certifies precisely three solutions
   in the open physical disk for a fixed order.
2. Cyclic spatial conjugacy, order reversal, and exact rational-box
   separation establish nine distinct physical configurations and
   their \(D_3\) orbit decomposition \(3+6\).
3. The trace of the rotation part of \(\Delta\) is rational in the
   reduced shape parameters. Algebraic elimination yields the
   irreducible cosine polynomials above. Sturm counts certify the
   disjoint rational intervals.
4. A separate all-orders numerical regression checks that the
   return-order traces coincide at each of the nine shapes. This
   consistency is also explained by conjugacy and inversion of
   the relevant rotation commutators; the regression is not, by
   itself, an exact algebraic certificate for arbitrary orders.
5. For any \(R\in SO(3)\), complex eigenvalues are
   \(1,e^{i\theta},e^{-i\theta}\). Their pairwise products give the
   displayed characteristic polynomial. The decomposition into
   scalar, skew, and traceless symmetric matrices is invariant
   under conjugation. For the two nonexceptional angle classes,
   the operator's minimal polynomial over \(\mathbb Q(c)\) is
   \((\lambda-1)(\lambda^2-2c\lambda+1)
   (\lambda^2-(4c^2-2)\lambda+1)\).

## Verification scripts

- `experiments/rhombic_prism_triangle_certified_disk.py`
- `experiments/rhombic_prism_triangle_nine_exact_certificate.py`
- `experiments/rhombic_prism_triangle_exact_cosine.py`
- `experiments/rhombic_prism_triangle_spectral_separation.py`
- `experiments/rhombic_prism_triangle_nine_symbolic_spectrum.py`
- `experiments/rhombic_prism_triangle_nine_spectral_orbits.py`

The equality of spectral traces across the return orders is currently
supported by the all-orders numerical regression and symmetry argument;
a fully symbolic order-by-order trace identity is a natural further
strengthening. The theorem concerns this specific rhombic prism family,
not arbitrary prisms.
