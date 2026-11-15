# TIMDR 51B.15l–m — checkpoint 2026-11-15

Research notes; mathematical models and conditional proofs, not empirical physical validation. Continues TIMDR_51B15E_15K_CHECKPOINT_2026-11-15.md.

## 51B.15l — robust realization of minimal relational automaton
Finite minimal relational automaton A=H/equiv_Z with transitions delta_a. Physical state space Q, disjoint nonempty decoding regions U_s, maps F_a. For pre-update disturbance B_nu, robust invariant-region condition F_a(U_s+B_nu) subset U_{delta_a(s)}. It implies correct decoding for every finite admissible sequence by induction if initial state in appropriate U_s. A single-point injective realization F_a(rho(s))=rho(delta_a(s)) requires delta_a injective. However injective F_a can map two distinct physical regions into disjoint subsets of the same decoded target region; thus microscopic reversibility and relational noninjectivity coexist. Example Q=R, F(x)=x/4, U_0=(-2,2), U_1=(3,5), delta(0)=delta(1)=0. F(U_0)=(-0.5,0.5) subset U_0 and F(U_1)=(0.75,1.25) subset U_0. For a finite disjoint partition of all Q into nonempty U_s, bijective F with F(U_s) subset U_delta(s) forces delta surjective (and for finite A bijective), since F(Q)=Q. Compactness not needed for this proof. For Q=[0,L]^d sup norm and disjoint closed eps-balls around m codes, packing bound m<=k^d, k=max(1,ceil(L/(2eps))). If eps-balls are closed and decoding regions are disjoint, separation must be strictly >2eps. The static packing bound is not sufficient for dynamical realization.

## 51B.15m — quantitative safety margin certificates
Q=R^d, target region U_t, V_{s,a}=F_a(U_s+B_nu). Signed distance sd_U(x)=dist(x,Q\U) for x in U and -dist(x,U) otherwise. Define gamma_{s,a}=inf_{x in V} sd_{U_t}(x), gamma_*=min over admissible (s,a). gamma_*>0 certifies V subset U_target with uniform positive clearance and hence all finite updates correct. gamma=0 is inconclusive, and gamma<0 means some image lies outside closure of U_target (subject to distance convention).

Ball certificate: U_s=open ball(c_s,R_s) in norm, F_a Lipschitz K_a on perturbed source, t=delta_a(s), gammahat_{s,a}=R_t-||F_a(c_s)-c_t||-K_a(R_s+nu). gammahat>0 suffices and lower bounds clearance. Example F(x)=x/4, U_0=(-2,2), U_1=(3,5), delta(0)=delta(1)=0. gammahat_0=1.5-nu/4, gammahat_1=0.75-nu/4; for nu=1, uniform margin >=0.5.

Ellipsoid certificate: U_s={x:(x-c_s)^T P_s(x-c_s)<1}, P_s positive definite. For x'=A_a x+w with ||w||_2<=nu, and A_a c_s=c_t, sufficient condition ||P_t^{1/2} A_a P_s^{-1/2}||_2 + nu ||P_t^{1/2}||_2 < 1. This ensures perturbed images of closed input ellipsoid lie in open target ellipsoid. It is sufficient, not necessary; nonlinear maps need remainder/reachability bounds. Anisotropic ellipsoids may outperform balls for directionally expanding/contracting maps, but are not universally optimal. For A=diag(2,1/4), a round ball maps to ellipse; no implication of long-term robust invariance.

Optimization: maximize minimum gamma subject to disjoint regions, inclusion in bounded Q, dynamical class, and appropriate size/shape constraints; otherwise objective may be ill-posed or unbounded. For fixed linear maps, some ellipsoidal certificate problems admit matrix inequalities; joint optimization over maps/regions/centers may be nonconvex.

Cautions and errata:
- Calling the F(x)=x/4 example 'empirical' is inaccurate: it is mathematical.
- 'Bistability' is not equivalent to bijectivity or bi-Lipschitzness.
- For 51B.15g on infinite H, Delta=inf pairwise distance >2eps is sufficient but not necessary for pairwise separation >2eps (inf can equal 2eps); finite H yields equivalence.
- Robustness is relative to a specified disturbance order: pre-update F(U+B_nu) versus post-update F(U)+B_nu.
- Finite-state relational automaton does not automatically admit smooth reversible physical realization.
