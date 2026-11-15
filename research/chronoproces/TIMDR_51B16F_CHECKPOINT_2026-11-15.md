# TIMDR 51B.16f — Wspólne uszczelnianie abstrakcji geometrycznej i epistemicznej
Checkpoint 2026-11-15.

## Exact physical-epistemic model
X=S_Phi x Q, finite relational modes, continuous compact Q subset R^n, hybrid dynamics s'=delta_a(s), x'=f_{s,a}(x,w), admissible w. Set-valued observation O_theta(s,x) subset Y_theta. Exact belief B_t subset X after observation history, updated B_{t+1}=Post_a(B_t) intersect O_theta^{-1}(y_{t+1}) with timing observe->act->memory update->physical transition->next observe. Current relational labels Lambda(B)={s:exists x (s,x) in B}; I_cur={nonempty B:|Lambda(B)|=1}. Initial-origin diagnosis requires immutable tag Bhat subset S_origin x S_current x Q to avoid mistaking merging for identification.

## Sound abstract beliefs
Finite geometry cells C and symbolic belief Bhat with B subset Bhat. If Bhat nonempty singleton label then exact B nonempty singleton label; converse fails. Abstraction can create spurious ambiguity but never certify false positive identification when sound.

## Spurious ambiguity example
Physical phase corridors H1=[.1,.7], H2=[1.1,1.7]; fine sensor y=round(x,1)+v, |v|<=.05. Sound measurement ranges within [.05,.75] and [1.05,1.75], disjoint. Coarse monitor ranges [0,1.2] and [.8,2] overlap spuriously; refinement to tight ranges certifies one-step identification without changing hardware. Coarse sign(x) yields R in both phases, a genuine one-step ambiguity. One-step overlap alone does NOT establish impossibility of all future active diagnosis.

## Real impossibility witnesses
For fixed policy pi, two admissible infinite runs with distinct target labels and identical action-observation histories disprove sure identification by pi. To disprove existence of ANY safe identifying strategy, need adversarial strategy maintaining ambiguity against all controller choices (game/viability certificate), not merely one failed controller.

## Geometry-epistemic product
Verification product physical X x controller memory M x belief monitor family B, with consistency true state in monitored belief. For finite-state verification need finite symbolic beliefs and sound transitions. Verify physical transitions, observation-conditioned alpha, memory update eta, belief updates and time ordering. For continuous Q product need abstraction.

## CEGAR-GE procedure
Start coarse geometric and observation/belief abstraction, construct product, check robust safety, sure identification and memory k. Outcomes CERTIFIED; CONTROLLER_REJECTED (concrete counterexample for specific controller); ARCHITECTURE_INFEASIBLE (complete impossibility proof for all allowed controllers); UNKNOWN. Spurious counterexamples guide refinement geometry, observation, belief; insufficient controller search must not be mislabeled architecture impossibility. Sound simulation condition B subset Bhat implies Psi_a(B,y) subset PsiHat_a(Bhat,y) for realizable y. Tightening sound abstractions preserves local safe-set inclusion and singleton-label certification for nonempty beliefs, though graph structure/global controller certificate may require recheck.

## Certified global cost optimum
For finite design class D and fixed exact costs, if candidate d* certified feasible at cost C* and every design with strictly lower cost has certified infeasibility, then d* globally minimizes cost in D. UNKNOWN cheaper designs prevent global optimality claim. For strategy-dependent diagnostic costs enumerate strategies or certify lower bounds.

## Certificate artifacts
Geometric: corridors, disturbance bounds, sound images, hard gamma inclusions.
Epistemic: possible observations, belief updates, diagnosis or persistent indistinguishability proof.
Architectural: controller alpha,eta, memory count, cost, closed-loop product. All must use same dynamics, noise, sensor, timing. No universal completeness of CEGAR-GE is claimed.
