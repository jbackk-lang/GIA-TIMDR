# TIMDR 51B.15y — Minimalne eksperymenty rozróżniające i koszt bezpiecznej identyfikacji relacyjnej
Checkpoint 2026-11-15. Continuation of 51B.15x.

## Model and hard constraints
Finite partial-observation safety game G=(X,A,Omega,T,O,D,I0), relational label lambda:X->Lambda. Winning belief region Z*, identification target I_lambda={B in Z*: |lambda(B)|=1}, diagnostic reachability R_lambda*. Strategy pi maps observation-action histories to actions; tau_pi is first hitting time of I_lambda. Robust safety and eventual identification must hold for every admissible adversarial run. In finite games with sure reachability, there exists a uniformly bounded-time winning strategy.

## Cost
Nonnegative step costs c_E(B,a), c_T(B,a), c_M(B,a) (energy/time/measurement), weighted scalar c_w=sum_i w_i c_i with nonnegative weights. Worst-case total J_w(pi,B0)=sup_runs sum_{t<tau_pi} c_w(B_t,a_t). Optimize over safe proper strategies guaranteeing identification; value +infinity if none. Weights encode engineering preferences, not probabilities. Multiobjective robust vector (max energy, max time, max measurement count) admits Pareto analysis; componentwise maxima can come from different paths and must not be confused with a single realized trajectory.

## Safety clearance gamma
For continuous physical decoding regions D_s subset Q, eroded D_s^[gamma]={x in D_s:dist(x,Q\D_s)>=gamma}, gamma>0; D^[gamma]=union_s {s}xD_s^[gamma]. Require Pred_a(B) subset D^[gamma] for all disturbances before observation; also all possible posterior beliefs stay within winning region Z*^[gamma]. Actions A_gamma(B) must be enabled for all possible states and have nonempty successors. Stronger gamma shrinks admissible strategy set. This is a hard constraint, not a penalty; it remains conditional on disturbance/model bounds.

## Adaptive distinguishing sequences
An adaptive diagnostic experiment is an observation-branching policy tree: internal nodes carry beliefs and safe actions, outgoing edges cover all possible observations and their correct posterior beliefs, terminal leaves have a unique relational label. A strategy guaranteeing identification by n steps iff such a tree exists of depth <=n; proof by unrolling/folding policy histories.

## Minimax dynamic programming
Target I_lambda^[gamma]. V_gamma^(0)(B)=0 on target, +infinity elsewhere. For n>=0:
V_gamma^(n+1)(B)=min{V_gamma^(n)(B), min_{a in A_gamma(B)}[c(B,a)+max_{y possible}V_gamma^(n)(Psi_a(B,y))]}.
Induction shows V_gamma^(n) is optimal worst-case cost among safe policies reaching target by n. For finite game, nonnegative costs and proper sure-reaching strategies, one may choose a strategy without repeating a belief along a branch (remove nonnegative-cost loops), yielding finite depth bounded by number of reachable nonterminal beliefs; hence finite-horizon search suffices for global proper-policy optimum. Zero-cost cycles make naive unconstrained stationary Bellman equations potentially admit improper spurious solutions; use horizon/rank or proper-policy restriction.

## Example time-energy tradeoff
Three relational hypotheses. Safe full test d_full costs energy 10, time 1, distinguishes all. Adaptive d1 costs energy 2/time1, isolates lambda1 vs {lambda2,lambda3}; if latter, d2 energy2/time1 distinguishes lambda2/lambda3. Full test worst-case (E,T)=(10,1), adaptive strategy (4,2). Weighted J=E+beta T yields full 10+beta, adaptive 4+2beta; adaptive preferred beta<6, equal at 6, full preferred beta>6. Assumes tests are safe and deterministic as specified, do not change hypothesis labels.

## Margin monotonicity
For gamma1<=gamma2, D^[gamma2] subset D^[gamma1], hence feasible strategies at gamma2 subset those at gamma1, provided unchanged objective and target semantics; V_gamma1*(B)<=V_gamma2*(B). Define gamma_max(B)=sup{gamma:V_gamma*(B)<infinity}; supremum may not be attained. Piecewise jumps in optimal cost possible as actions lose feasibility.

## Sound computational certificate
Each policy-tree node records belief enclosure, universally enabled action, verified Pred_a(B) subset D^[gamma], exhaustive observation successors, sound posterior enclosure, termination rank, singleton relational label at leaves, worst-case cost bound. Interval arithmetic, adaptive cells, polyhedral/ellipsoidal enclosures from 51B.15p-q can produce conservative sound certificates. Simulation alone insufficient; overapproximate failure does not prove real impossibility.

## Scope
Exact finite-game results; continuous Chronoproces requires correct Markov state (augment history/resources if necessary) and sound abstraction. Worst-case costs are not expectations. Next 51B.15z: joint sensor, memory and diagnostic policy design.
