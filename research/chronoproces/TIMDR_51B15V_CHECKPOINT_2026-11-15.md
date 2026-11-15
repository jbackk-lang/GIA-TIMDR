# TIMDR 51B.15v — Dolne granice obserwowalności i koszt informacji dla bezpiecznego sterowania
Checkpoint 2026-11-15, continuation of 51B.15u.

## Model
Finite partial-observation safety game G=(X,A,Omega,T,O,D,I0), observations O(x), actions chosen after observation and before adversarial successor. Policy can use full history, no memory bound. Post_a(B)={x':exists x in B,(x,a,x') in T}. Assume enabled actions have nonempty successors for all relevant x or handle partial enablement explicitly.

## Immediate informational obstruction
Act_safe(B)={a:Post_a(B) nonempty and Post_a(B) subset D}, with a enabled across B. If Act_safe(B)=empty, no policy (even unbounded-memory) can guarantee safety from this belief at current decision: every action has some possible unsafe successor before new observation. This is local, not global from I0 if earlier safe diagnosis could avoid B.

Example X={p,q,bad}, D={p,q}, O(p)=O(q)=o, B0={p,q}, p--a-->p, p--b-->bad, q--a-->bad, q--b-->q. Neither action safe for both, so impossible from B0. Contrast 51B.15u alternating-actions example where initial p known and parity memory suffices despite constant observations.

## Global winning region
Let Z* be greatest fixed point of finite belief-game safety predecessor from 51B.15u. B0 not in Z* iff no observation-feedback winning policy exists, even with unbounded memory. Finite elimination rank yields finite-horizon spoiling strategy. Nonobservability alone not equivalent to unwinability: common safe action or safe active diagnosis may suffice.

## Safe diagnosis
An additional action d can map p to p' and q to q' safely with distinct next observations, enabling different safe continuation actions. Diagnosis must itself preserve safety for all possible current states. Information received only after transition cannot retroactively prevent a violation.

## One-step sensor symbol lower bound
Given known finite possible initial X0 subset D and deterministic current sensor O, for each state x define A_safe(x)={a:Post_a({x}) subset D}, requiring enabled actions. Each sensor fiber C_o={x in X0:O(x)=o} must satisfy intersection_{x in C_o} A_safe(x) nonempty. This is necessary and sufficient for a safe one-step observation-only policy. Define m* minimal number of partition classes of X0 whose members have nonempty common safe-action intersection; a designed deterministic sensor requires at least m* symbols, so fixed-length output bits >=ceil(log2 m*). This does not automatically bound channel capacity, time-average information or all-horizon observability.

## Conflict graph
Graph vertices X0, edge x--x' when A_safe(x) intersect A_safe(x') empty. A safe sensor fiber must be independent; thus m* >= chromatic number chi(G_conf), bits >=ceil(log2 chi). Pairwise compatibility is not sufficient for joint common-action intersection: 3+ states may be pairwise compatible but jointly incompatible.

## Noisy sensor
For y=g(x)+v with v in V, possible measurement set Y(x)=g(x)+V. If two states have disjoint safe action sets, their measurement sets must be disjoint for a one-step policy based only on current y. In scalar bounded noise |v|<=epsilon, closed intervals imply |g(x)-g(x')|>2 epsilon for such conflict pairs. This is necessary pairwise, not generally sufficient for many-state or future-horizon safety. Past information can refine current beliefs; bounds must be applied to actual information sets.

## TIMDR relevance and limits
Beliefs B subset S_Phi x Q encode uncertain relational and physical configurations. Distinguish reconstruction of exact state from enough information to choose a common relationally safe action. Guarantees conditional on disturbance/measurement model. Memory stores information, sensing supplies it, safe control may actively acquire it. Future 51B.15w: active observability, safe diagnosis, information acquisition within robust invariant regions.
