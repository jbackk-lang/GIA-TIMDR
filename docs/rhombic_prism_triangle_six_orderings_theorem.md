# Six orderings: reversal pairing and D3 covariance

Let g1,g2,g3 be the three proper rotations formed from bottom-face and side-face reflections. For each permutation I=(i,j,k), set P_I=g_i g_j g_k, Q_I=g_k g_j g_i, and Delta_I=P_I Q_I^-1.

## Theorem 1: reversal

For reversed order I^rev=(k,j,i), P_(I^rev)=Q_I and Q_(I^rev)=P_I. Therefore

Delta_(I^rev)=Q_I P_I^-1=Delta_I^-1.

For an isometry D(x)=Rx+b, the fixed points of D and D^-1 coincide. Moreover ||D(O)-O||=||D^-1(O)-O|| (apply R^-1 to the displacement), and ||R-I||_F=||R^-1-I||_F. Thus the three reversal pairs (123,321), (231,132), (312,213) have identical centroid-return sets and identical A_O and A_R at every shape parameter.

## Theorem 2: cyclic equivariance

Let K be the +120 degree spatial rotation around the base centroid, and let C act on the horizontal displacement (u,v). As established in docs/rhombic_prism_triangle_d3_equivariance_proof.md,

K Delta_(ijk)(u,v) K^-1 = Delta_(i+1,j+1,k+1)(C(u,v)).

The centroid transforms covariantly. Hence the zero locus for ordering (231) is the 120-degree rotated zero locus for (123), and the zero locus for (312) is the 240-degree rotated zero locus for (123), subject to the convention for the direction of C. The other three orderings have the same loci by reversal.

**Consequences conditional on the earlier exact three-root classification:** if (123) has exactly three centroid-return shapes in the open unit disk, then every ordering has exactly three, and the union across all orderings contains at most nine shapes (potential overlaps require separate examination). Counting a union of nine distinct points without checking overlaps would be premature.

## Scope

This is a theorem about the entire **family of ordered words**. A single fixed ordering need not be invariant under 120-degree parameter rotation. The tests in experiments/rhombic_prism_triangle_six_orders.py check the identities numerically for several shapes; the algebraic proof above does not depend on their execution.

No quantum anomaly or parity-violating field-theory conclusion follows.
