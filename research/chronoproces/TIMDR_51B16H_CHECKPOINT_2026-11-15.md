# TIMDR 51B.16h — Dualny system certyfikatów i niezależny weryfikator
Checkpoint 2026-11-15.

## Trust boundary
Separate untrusted synthesizer (heuristics, LP/SMT/ML) from deterministic independent certificate checker. Both refer to a single canonical model M=(X,A,T,O_theta,K^gamma,I0,lambda,tau), with explicit time order observe->act->memory update->physical transition->next observe; distinguish current-mode diagnosis from origin-label diagnosis. Canonical content fingerprint recommended. Trusted computing base still includes parser, semantics, arithmetic and checker.

## Positive certificate
Cert+ = (alpha,eta,W,r) with deterministic controller alpha:M x Y->A, eta:M x Y->M, product invariant W over physical state, memory and exact or sound belief. Check initial coverage; every represented actual state is safe; all possible product successors are covered; for each non-target node rank r in N strictly decreases along every successor (or successor is target). Then safety holds inductively and no infinite non-diagnostic path exists. For finite W, maximum initial rank bounds diagnosis steps. For continuous dynamics, sound set inclusion obligations required.

## Negative certificate
Cert-=(L,sigma_E,R), where L is family of non-diagnostic beliefs and sigma_E is adversarial response with concrete realizability proof R. Check initial belief in L; for each B in L and every action a either there is a concrete unsafe successor (so action cannot guarantee safety) or a realizable observation y with exact Psi_a(B,y) in L. For finite games this proves no policy can guarantee safe finite-time diagnosis. For continuous models ensure coherent infinite realizability; local abstract-edge existence alone is not enough.

## Checker protocol
VALID_POSITIVE, VALID_NEGATIVE, INVALID_CERTIFICATE, UNVERIFIED. Invalid certificate does not imply theorem false. Unverified means proof obligation beyond checker's supported theory. Pseudocode positive checks model match, initial coverage, node safety, all successors, decreasing rank; negative checks model match, initial belief coverage, non-diagnostic trap, every action unsafe or legal response into trap. Helper functions need implementation; no working checker claimed.

## Reference negative test: continuous variant A
B0={(s1,0),(s2,0)}, u(a0)=0,u(a1)=1, |w|<=.15, gamma=.2, K1=[-2.8,.8], K2=[-.8,2.8], relational modes fixed. a1 from (s1,0) yields x' in [.85,1.15], violating K1. Under a0 environment can select w_t=0, maintaining x=0 for both modes indefinitely; both sensors yield same observations for equal sensor-noise choices. Thus no safe sure diagnosis, any memory. Witness is existential adversarial disturbance, not assertion that every a0 trajectory remains at zero.

## Continuous obligations
Linear polytope inclusions via rational arithmetic/LP dual certificates; ellipsoid inclusions via certified PSD matrix checks; nonlinear reachability via outward-rounded intervals and verified Taylor remainder. Negative proofs need realizability in addition to overapprox inclusion. Soundness distinct from completeness; no universal completeness for general nonlinear continuous systems. No executable checker yet implemented.
