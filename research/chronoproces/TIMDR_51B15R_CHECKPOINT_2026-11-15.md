# TIMDR 51B.15r — synteza odporności przy częściowej obserwowalności
Checkpoint 2026-11-15; mathematical research, not empirical physical validation. Continues 51B.15q.

## Model and exact set-membership filtering
Finite relational states S, physical Q, decoder domains D_s. Physical x'=F_a(x)+w, w in W_a; observation y=g(x)+v, v in V. Action chosen after current observation and before next process noise and observation. Belief/information state B subset S x Q contains all relational/physical pairs consistent with observed history. Prediction Pred_a(B)={(delta_a(s),F_a(x)+w):(s,x) in B, w in W_a}. Observation compatibility O(y)={(s,x):y-g(x) in V}. Posterior Psi_a(B,y)=Pred_a(B) intersect O(y). If actual pair belongs to B and noise assumptions hold, actual successor belongs to Psi_a(B,y_next). Verified overapproximations Bhat containing exact B preserve sound estimation.

## Belief safety and control
Define safe belief family Dfrak={nonempty B subset union_s ({s} x D_s)}. If B is singleton relational slice {s} x X, safety iff X subset D_s. For exogenous actions, B subset union_s ({s} x K_s^infty) suffices for all-action robustness, but not necessary for controlled viability. For each B, Adm(B) actions enabled in every possible relational state. Obs_a(B)={g(x')+v:(s',x') in Pred_a(B),v in V}. Belief predecessor BPre(Cfrak) consists of B in Dfrak for which exists a in Adm(B) with Pred_a(B) in Dfrak and for every possible y in Obs_a(B), Psi_a(B,y) in Cfrak. Pred safety before measurement matters; a later measurement cannot undo unsafe transitions. A family Cfrak subset Dfrak with Cfrak subset BPre(Cfrak) gives a sound infinite-horizon safety controller depending on B: choose witness action at each belief, and induct. Witness action is shared for all physical states in B and chosen before disturbance. In infinite belief spaces naive intersection of finite-horizon winning sets need not automatically yield a witness action without additional conditions; finite action sets and nested witnesses can help. Greatest winning region can be defined semantically by existence of a policy.

## Separation caveat and counterexample
Sound set estimation plus a controller designed for a point estimate is not enough. If B={-1,+1} and actions a_minus/a_plus are each safe for only one of the two states, forall x exists a safe action but no common a safe for all x. Classical LQG separation principle does not automatically extend to adversarial set-membership safety. A robustly correct estimator-regulator composition must be verified jointly against all possible states, actions, disturbances, and future observations.

## Exact observation example
Q=R, single relational s, D=(-2,2), F_plus(x)=x+0.5, F_minus(x)=x-0.5, w in [-0.1,0.1]. From initial B=[-1,1], either first action remains safe. With exact y=x, policy choose minus if x>=0 else plus. For x>=0 in D, next x in ( -0.6,1.6); for x<0 next x in (-1.6,0.6); hence D robust invariant under observation-feedback policy. With noisy y=x+v, sign(y) policy does not automatically preserve guarantee; belief-based redesign needed.

## Numerical representation
Polyhedral, ellipsoidal, unions of adaptive cells, and hybrid per-relational-state families X_s can overapproximate belief. Maintain actual possible states within Bhat, but this alone does not certify safety; selected action must preserve safe belief family and all observation successors. Computational soundness distinct from completeness.

## Next
51B.15s minimal information states for safety, equivalence of observation histories under all future controls/measurements, lower bounds on memory and observability costs, finite abstraction conditions.
