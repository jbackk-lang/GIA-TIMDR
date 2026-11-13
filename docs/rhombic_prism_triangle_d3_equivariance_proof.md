# Triangle D3 equivariance versus fixed-word symmetry

## Exact geometric theorem (rotation)

Let A=(0,0,0), B=(1,0,0), C=(1/2,sqrt(3)/2,0), c=(1/2,sqrt(3)/6,0). Let K(x)=Q(x-c)+c where Q is the +120-degree rotation around the vertical axis. Write t=(u,v,w), w=sqrt(1-u²-v²)>0, and t'=Qt. Let s_0 be reflection in z=0 and s_i(t) be reflection in the side plane spanned by edge i and t, i=1,2,3. Define g_i=s_0 s_i.

Since K sends A to B, B to C, and C to A, it maps each base edge and its side plane to the next side plane for t'. It also preserves z=0. Therefore

K s_0 K^-1=s_0,  K s_i(t) K^-1=s_(i+1)(t'),
K g_i(t) K^-1=g_(i+1)(t').

For any ordered triple I=(i,j,k), put P_I=g_i g_j g_k, Q_I=g_k g_j g_i and Delta_I=P_I Q_I^-1. By multiplicativity of conjugation,

**K Delta_I(t) K^-1 = Delta_(i+1,j+1,k+1)(t').**

The centroid satisfies O(t')=K O(t), hence ||Delta_I(t)O(t)-O(t)||² and ||R_Delta_I(t)-I||_F² are preserved under the **combined** transformation (t,I)->(Qt,cyclic(I)). This is an exact proof, independent of floating-point checks.

## What it does not say

The fixed ordered word (1,2,3) need not be invariant under parameter rotation t->Qt alone. The transformed word is (2,3,1). Thus a fixed-word locus with three roots need not form a full threefold rotation orbit. To discuss D3, include the full family of six orderings (or identify equivalent orderings carefully).

The reflection component of D3 can be treated similarly by conjugating side-plane reflections with a vertical spatial mirror and permuting edge labels; the conjugation argument does not depend on orientation preservation. For a given fixed ordering, additional word reversal and inversion identities need separate checking.

No statement about a quantum triangle anomaly follows from this classical rigid-motion equivariance.

## Reproducibility

Numerical regression: `experiments/rhombic_prism_triangle_d3_equivariance.py`.
