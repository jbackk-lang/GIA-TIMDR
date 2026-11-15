# TIMDR 51B.15u — Gry bezpieczeństwa z częściową obserwacją i minimalna pamięć sterownika
Checkpoint 2026-11-15. Continuation of 51B.15t.

## Finite partial-observation safety game
G=(X,A,Omega,T,O,X_safe,I0), finite X,A,Omega; transition relation T subset X x A x X encodes adversarial nondeterminism; deterministic observation O:X->Omega; I0 initial uncertainty. Controller sees current observation, chooses action, environment chooses successor, controller observes new state. Assume total transitions for admissible actions or explicitly reject actions with empty Post; terminal behavior separate.

Belief update Post_a(B)={x':exists x in B,(x,a,x') in T}; Upd(B,a,o)=Post_a(B) intersect O^{-1}(o), nonempty only for possible o. Safe beliefs B_safe={nonempty B subset X_safe}. Controllable predecessor F(Z) consists of safe beliefs B with some action a such that Post_a(B) nonempty and subset X_safe and every nonempty observation successor Upd(B,a,o) in Z. Iterate Z0=B_safe, Z_{n+1}=F(Z_n); monotone descending, finite stabilization at greatest fixed point Z*. B in Z* iff exists deterministic observation-based infinite-horizon winning strategy, under standard perfect-recall and adversarial transition semantics. Construct policy by choosing winning witness action per belief; outside Z* environment can force finite safety violation (finite-rank induction).

## Memory bound and minimization
A belief-memory controller can store current nonempty subset B subset X, at most 2^|X|-1 possibilities. If initial belief is winning, finite memory suffices; this is a worst-case upper bound for the belief-state implementation, not the minimum. Controller K=(M,m0,alpha,eta) with action alpha(m,o), memory update eta(m,o) and explicit observation timing. Minimize |M| among winning controllers for initial I0. For fixed k, finite enumeration of action/update tables and product reachability verification is decidable, though may be costly.

## Two-state-memory necessity example
X={p,q,bad}, safe={p,q}, O(p)=O(q)=o, initial known p. Actions a,b. Transitions p --a--> q, p --b--> bad; q --b--> p, q --a--> bad. With constant observation o, winning action sequence must alternate a,b,a,b,... . A two-memory-state controller tracks parity and wins; one memory state forces a constant action and loses (a loses second step, b immediately). Thus N_ctrl=2, one bit under this model. Include bad sink transitions as needed for totality.

## Strategic indistinguishability and lower bounds
Different beliefs need not require different controller memory. To prove lower bound k, show every winning implementation must distinguish k reachable histories with same current observation because merging leads to incompatible future safety requirements. Reachability and policy dependence make this subtler than Myhill-Nerode minimal exact monitor. Distinguish winning strategy existence, controller state minimization, and monitor minimality. In continuous Chronoproces, finite abstraction must be sound for original dynamics and observation uncertainty; abstract win does not transfer automatically without a correct refinement relation.

## Caveats
Set-membership worst-case guarantees conditional on assumed disturbance bounds and observation model. No probabilistic assumptions. Observation-based memoryless in belief space is not necessarily memoryless in observation space. Partial observation of state and relational labels may be represented jointly in X=S x Q or finite abstractions thereof.
