# Triangle-order centroid-return zeros: refined numerical evidence

Date: 2026-11-13. This is a numerical result, **not** a proof of completeness or a quantum anomaly.

Let r_i be the proper rotation obtained by composing bottom-plane reflection with the i-th side-plane reflection. Put P=r_1 r_2 r_3, Q=r_3 r_2 r_1, and Delta=P Q^{-1}. Let O be the centroid of the prism. We solve the three-component equation f(u,v)=Delta(O)-O=0 on u²+v²<1, and inspect A_R=||R_Delta-I||_F².

Numerical least-squares refinement of three previously reported candidates (double precision):

| u | v | ||f|| | singular values of 3x2 Jacobian Df |
|---|---|---|---|
| -0.58610596 | -0.33838843 | 6.14e-16 | 2.50098, 0.14352 |
| -0.68589188 | -0.17579820 | 8.90e-16 | 3.91409, 0.24942 |
| -0.49519165 | -0.50610070 | 5.39e-16 | 3.91409, 0.24942 |

The two nonzero Jacobian singular values at each candidate show full column rank of the numerical Jacobian. Thus these are locally well-conditioned isolated solutions *if* they are exact zeros. Numerical precision alone does not prove that the overdetermined three-equation/two-unknown system has exact zeros. A rigorous interval or symbolic existence proof is still needed.

The last two points have matching Jacobian singular values and matching rotational asymmetry A_R≈2.86611; this suggests symmetry or an algebraic relation but does **not** establish a D3 orbit. The first has A_R≈1.90193.

**Important group-theoretic correction:** Delta(O)=O for Delta=P Q^-1 is equivalent to P^-1(O)=Q^-1(O), **not** generally to P(O)=Q(O). Comparing P(O) and Q(O) is a distinct experiment.

At (u,v)=(0,0), R_Delta≈I but Delta is a pure translation of length 3, so A_O=9 and A_R≈0. These quantities measure classical noncommuting rigid motions, not a quantum triangle anomaly.

Next tasks:
1. Derive exact rational/algebraic expressions using s=sqrt(3), w²=1-u²-v², clear denominators only where they are strictly positive.
2. Use resultants or Gröbner bases to isolate exact solutions and certify that f vanishes.
3. Apply interval Newton/Krawczyk bounds to certify isolated solutions in parameter boxes.
4. Determine whether the candidates are related by D3 actions on (u,v), with correct induced permutation of ordered side-face generators.
5. Compare robust dimensionless rotational measures with molecular attitude dynamics; any particle-physics anomaly comparison requires quantum field-theoretic structure not present here.
