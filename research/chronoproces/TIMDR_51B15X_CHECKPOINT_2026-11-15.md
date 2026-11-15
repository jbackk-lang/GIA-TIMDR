# TIMDR 51B.15x — Bezpieczna identyfikowalność relacyjna i nierozróżnialność trwała
Checkpoint 2026-11-15; continuation of 51B.15w.

## Model and target
Finite partial-observation safety game with X subset S_Phi x Q (or a sound finite abstraction), transition T, observation O, safe D, initial belief B0. Relational label lambda:X->Lambda (finite). Current relational label uniquely known at belief B iff |Lambda(B)|=1, where Lambda(B)={lambda(x):x in B}. Distinguish identifying current label from identifying initial label: if dynamics merge classes, augment state with immutable origin tag lambda(x0) to diagnose origin.

## Safe diagnostic reachability
Z* is winning belief region. Target I_lambda={B in Z*: |Lambda(B)|=1}. Define R0=I_lambda and R_{n+1}=R_n union {B in Z*: exists action a enabled for all x in B, Post_a(B) nonempty and subset D, and all nonempty observation successors Upd(B,a,o) in R_n}. Finite iteration stabilizes at R_lambda*. B in R_n iff a policy keeps safety and guarantees current-label identification in <=n steps against all environment choices. In finite belief games B in R_lambda* iff some uniformly finite worst-case identification time exists. Rank r_lambda(B)=min{n:B in R_n}, infinity outside; Bellman minimax rank r(B)=1+min_{safe winning actions a} max_o r(Upd(B,a,o)), with rank 0 at target.

## Permanent inability to guarantee diagnosis
N_lambda=Z* minus R_lambda* denotes beliefs from which safety is possible indefinitely but no policy can guarantee eventual identification. For finite adversarial safety/reachability games, environment can choose a path avoiding the target indefinitely against any proposed safe strategy. This does NOT assert that no particular outcome ever yields information or that an individual physical pair remains identical at all times.

## Strong observational indistinguishability
One can study whether two different relational-origin hypotheses admit overlapping observation histories for all safe experimental policies. This is stronger semantic analysis and requires explicit quantifier order, safe admissibility, origin tags, and nondeterministic trace semantics. Do not automatically equate this with bisimulation: bisimulation may give sufficient certificates but is not generally necessary.

## Pairwise distinction insufficient
Three initial relational hypotheses x1,x2,x3. For each pair i,j there is a safe distinguishing test d_ij for that pair, but it is unsafe for the third hypothesis. A universally safe holding action c yields no new information and preserves the full triple. Thus initial belief {x1,x2,x3} is winning for safety (repeat c) but not in R_lambda*, even though each pair is separately distinguishable under its own restricted belief. Shows need for common safe action at current belief and adaptive policy-tree quantifiers.

## Continuous TIMDR and sound abstraction
Relational label can encode isomorphism class of event geometry (E,N,C,a). Full archival history not required if label and predictive dynamics are preserved; otherwise augment Markov state with sufficient history. For continuous noisy dynamics, verified overapproximation of reachability and observations can certify safe strategies under correct refinement, but failure of conservative abstract diagnosis does not prove intrinsic nonidentifiability of original continuous system. All guarantees conditional on modeled uncertainty and timing.

## Next
51B.15y minimal distinguishing experiments, robust worst-case diagnosis time, energy, observations, tradeoffs and certificates.
