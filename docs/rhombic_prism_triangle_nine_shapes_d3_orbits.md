# Nine candidate configurations and D3 orbit decomposition

Date: 2026-11-13.

Assuming the previously reported exact algebraic root classification for the fixed ordering (123), its three interior roots are approximately

A=(-0.49519165,-0.50610070),
B=(-0.58610596,-0.33838843),
C=(-0.68589188,-0.17579820).

Let R denote rotation by +120 degrees in parameter space, and H reflection across u=sqrt(3)v:

R=[[-1/2,-sqrt(3)/2],[sqrt(3)/2,-1/2]],
H=[[1/2,sqrt(3)/2],[sqrt(3)/2,-1/2]].

Then H(A)=C, H(B)=B, H(C)=A (within numerical precision). R^3=H²=I and HRH=R^-1 exactly. Thus the D3 orbit of B has 3 elements and the D3 orbit of A has 6 elements, provided the numerical candidates are exact and distinct.

The union of roots for all six orderings (grouped in three reversal pairs) is represented by

| ordering pair | root 1 (u,v) | root 2 (u,v) | root 3 (u,v) |
|---|---|---|---|
| 123/321 | (-0.495192,-0.506101) | (-0.586106,-0.338388) | (-0.685892,-0.175798) |
| 231/132 | (+0.685892,-0.175798) | (+0.586106,-0.338388) | (+0.495192,-0.506101) |
| 312/213 | (-0.190700,+0.681899) | (0,+0.676777) | (+0.190700,+0.681899) |

All nine approximations are pairwise separated; the minimum separation is about 0.190769. Since the approximations are accurate far beyond the separation, this is strong numerical evidence that the nine points are distinct. The numerical enumeration is reproducible with experiments/rhombic_prism_triangle_nine_shapes.py.

**Conditional completeness:** the assertion that there are *exactly* nine physical solutions across the six orderings depends on a valid exact certification of the three-root count for the (123) ordering. To make this unconditional, isolate the algebraic roots with rational intervals, evaluate the rational formula for u with interval bounds, and certify u²+v²<1 or >1 for every real root. This document does not claim that such interval certificates have already been produced.

The D3 orbit decomposition (3+6) is a statement about parameter geometry and generator-order covariance. It is not evidence of a quantum triangle anomaly.
