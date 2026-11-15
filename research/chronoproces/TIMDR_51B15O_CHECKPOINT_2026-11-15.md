# TIMDR 51B.15o — Maksymalne odporne obszary niezmiennicze Chronoprocesu
Checkpoint 2026-11-15; mathematical research notes, not empirical validation. Continuation of 51B.15n.

## Setup
Finite relational automaton A with admissible event set Adm(s) and deterministic transition delta_a(s). Physical state Q, prescribed correct decoding domains D_s subset Q. Post-update bounded adversarial noise x'=F_a(x)+w, w in W_a. We seek maximal family K_s subset D_s such that F_a(K_s)+W_a subset K_{delta_a(s)} for all admissible (s,a). For no admissible outgoing events, empty intersection is Q (termination semantics; change if different termination model).

## Robust predecessor and fixed point
Pre_a(Y)={x in Q: F_a(x)+W_a subset Y}=F_a^{-1}(Y minus W_a), where minus denotes Pontryagin difference and inverse is set preimage. Family operator (V K)_s=D_s intersect intersection_{a in Adm(s)} Pre_a(K_{delta_a(s)}). Start K^(0)=D, K^(n+1)=V K^(n). Monotonicity gives descending K^(0) superset K^(1) superset ... . Let K^infty_s=intersection_{n>=0} K^(n)_s. Because universal preimage commutes with arbitrary intersections, K^infty is a fixed point and robust invariant. Any other robust invariant J subset D lies in each K^(n) by induction, hence J subset K^infty. Thus K^infty is greatest robust invariant family. No compactness or finite convergence required for this set-theoretic proof.

## Scalar worked example
Q=R, F(x)=x/4, W=[-0.5,0.5], A={0,1}, delta(0)=delta(1)=0. D0=(-1,1), D1=(1,3). F(D0)+W=(-0.75,0.75) subset D0, so K0^infty=D0. Pre(K0^infty)=(-2,2) (strict inequalities for open target and closed noise); K1^infty=D1 intersect (-2,2)=(1,2). Points x in [2,3) are correctly decoded as 1 now but unsafe for next step. For x=2 the upper disturbed image is 1, excluded from D0. Thus K1 is open at 2.

## Computation
Finite automaton does not imply finite stabilization of set iteration in continuous Q. Exact stabilization if K^(N+1)=K^(N); otherwise descending intersection. Numerical inner approximations certified invariant provide safe sufficient sets; outer approximations alone do not certify safety. Geometric and computational representations may need interval arithmetic, polyhedra, ellipsoids, symbolic sets, reachability or SMT, and explicit verification.

## Controlled variant and quantifiers
If event a is selectable before disturbance, controlled predecessor uses union over actions:
(V_ctrl K)_s=D_s intersect union_{a in Adm(s)} Pre_a(K_{delta_a(s)}).
It corresponds to exists action for all disturbances, whereas adversarial/exogenous event version corresponds to all actions for all disturbances. For feedback policies and nonanticipativity the information available to controller must be specified. A maximum controlled invariant set can be computed as greatest fixed point under appropriate strategy semantics. Avoid conflating safety for all events with existence of a safe controller.

## Caveats
D_s are given decoder regions; if decoder itself is to be optimized, joint synthesis is a distinct, potentially nonconvex task. The 'maximal' region is maximal relative to fixed D_s, F_a, W_a, event semantics and Q. Empty K_s means no robust guarantee from that decoded state. If only some histories are reachable, one may restrict initial state set or admissible event sequences; do not silently assume all automaton states reachable. The proof handles post-update noise; pre-update noise needs Pre_a(Y)={x:F_a(x+B_nu) subset Y}.
