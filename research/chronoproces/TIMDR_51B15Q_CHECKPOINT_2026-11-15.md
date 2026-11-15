# TIMDR 51B.15q — Hierarchiczna i wieloskalowa synteza certyfikatów odporności relacyjnej
Checkpoint 2026-11-15. Continuation of 51B.15p.

## Correct control quantifiers
Define Safe_a(s,C,K) iff guaranteed outer reachability R_a(C) subset K_{delta_a(s)}. Exogenous actions: retain cell iff forall admissible a Safe_a; remove iff exists a not Safe_a. Controlled action chosen before disturbance: retain iff exists a Safe_a; remove iff forall a not Safe_a. Safe-action table pi_safe(s,C)={a: R_a(C) subset K_delta(s)}. The user's formula forall a R_a(C) not subset target is the removal criterion for controlled case, not retention. An action may depend on s and observed C, but not future w.

## Adaptive hierarchy
Represent bounded physical Q by tree of cells, refine only uncertain cells. Candidate labels: certified safe, proven excluded, unresolved. Failure of sufficient test alone does not prove unsafety. Given decoder domains D_s, finite leaf families L_s, let L_s^union = union_{C in L_s} C. If each retained cell C subset D_s and for every admissible (s,a) an outer reachability set Rhat_a(C) obeys F_a(C)+W_a subset Rhat_a(C) subset L_delta(s)^union, then the family of unions is robust invariant and hence subset of maximal K^infty from 51B.15o. Proof pointwise on each leaf and maximality. This soundness is independent of cell shapes, hierarchy and representation of outer reachability.

## Local ellipsoidal reachability
For each cell C choose enclosing ellipsoid E_C with C subset E_C; if F_a(E_C)+W_a subset Rhat_a(E_C), then F_a(C)+W_a subset Rhat_a(E_C). For nonlinear smooth F_a on C, use Taylor F_a(x)=F_a(c_C)+J_a(c_C)(x-c_C)+r_a(x), with rigorously certified remainder r_a(C) subset R_{a,C}. Then reachability is bounded by F_a(c_C)+J_a(c_C)(C-c_C)+R_{a,C}+W_a. Interval arithmetic, Lipschitz bounds or verified Taylor models can supply remainder.

## Algorithm
Initialize cells wholly inside decoder regions; compute sound reachability bounds; eliminate cells violating current candidate target unions; refine unresolved cells adaptively by boundary intersection, reachability overapproximation width, or decision ambiguity; iterate within resource budget. Independently recheck all invariance inclusions against final retained family, since deleting targets may invalidate earlier tests. If failure, delete and repeat. For controlled case certify at least one common safe action per retained cell; store pi_safe(s,C). Finite budget/finite hierarchy ensures termination of implementation but may yield empty inner set; that is not proof no viable states exist.

## Quantifier issue on adaptive cells
forall x in C exists a Safe(x,a) does not imply exists a forall x in C Safe(x,a). Refinement can enable cell-dependent policies, provided controller knows the cell. Observation uncertainty changes the information pattern and requires belief-set synthesis.

## Limitations
Adaptive refinement can reduce practical work but does not eliminate curse of dimensionality in worst case; full h-resolution in d dimensions may need O(h^-d) cells. Soundness does not imply numerical completeness or polynomial runtime. Certified safe versus proven excluded must be distinguished from merely unresolved. Local elliptical bounds may be conservative. All results conditional on modeled disturbances and exact/verified enclosure computations.

## Next
51B.15r: partial observation, belief-state robust viability, quantifier order, observation noise, finite-state abstraction and sound safety policies.
