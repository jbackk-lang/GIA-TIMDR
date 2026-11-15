# TIMDR 51B.16a — Minimalny Chronoproces Referencyjny i integralny certyfikat bezpieczeństwa
Checkpoint 2026-11-15.

## User-given physical model
S_Phi={s1,s2}, Q=[-4,4]. Decoding domains D_s1=[-3,1], D_s2=[-1,3]; gamma=.2 gives K1=[-2.8,.8], K2=[-.8,2.8]. Joint safe K=({s1}xK1) union ({s2}xK2); physical union alone is insufficient. Dynamics x'=x/2+u(a)+w, u(a0)=0,u(a1)=1, |w|<=.15. Exact interval images:
a0(K1)=[-1.55,.55]; a1(K1)=[-.55,1.55]; a0(K2)=[-.55,1.55]; a1(K2)=[.45,2.55].
a0(K1) subset K1, a1(K2) subset K2, but a1(K1) not subset K1 and a0(K2) not subset K2.
Sensor coarse sign(x), fine round(x,1)+v with |v|<=.05. Both depend on x only, cannot distinguish (s1,x) from (s2,x) by instantaneous observation at shared x in [-.8,.8]. Fine output remains continuum due to additive noise; finite-game methods need sound observation partition unless controller ignores observation.

## Crucial underspecification
Relational automaton delta_a, initial belief I0, identification target (current vs initial mode), step diagnostic costs were unspecified. Do not claim a unique certificate without choices. Two explicit completions show opposite outcomes.

## Variant A: identity relational automaton
delta_a(s)=s for both actions. Initial belief B0={(s1,0),(s2,0)}. At x=0, action a1 has physical successor [.85,1.15], exceeding K1 upper .8, hence not robustly safe for s1. Action a0 preserves x=0 if adversary chooses w=0, both modes give same sensor outputs and remain distinct. Therefore no safe policy can guarantee identification of current or initial relational mode from B0. Safety is feasible: H=[-.3,.3] robust invariant under a0 because .5H+[-.15,.15]=H, and H subset K1 intersect K2. Thus B0 winning safety but not sure diagnostic reachability.

## Variant B: reset-to-action relational automaton
delta_a0(s)=s1 and delta_a1(s)=s2 for all s. Set I0=K, lambda(s,x)=s. Constant action a1 maps K1 to [-.55,1.55] subset K2 and K2 to [.45,2.55] subset K2; every successor mode s2. Repeating a1 keeps K robustly invariant for all disturbances and identifies CURRENT mode after exactly 1 step by known action effect, not by observing it. Does not identify INITIAL mode, because distinct initial modes are merged. One-state controller M={m}, alpha(m,y)=a1, eta(m,y)=m works for either sensor (no measurement required). Certificate: correct relational mode after action, infinite-horizon gamma=.2 safety, one-step current-mode identification, k=1.

## Costs and optimum
Given C_sensor(coarse)=2, C_sensor(fine)=8, C_memory(1)=1, C_memory(2)=3. Candidate fixed overheads coarse/k1=3, coarse/k2=5, fine/k1=9, fine/k2=11. With unit cost per diagnostic action, every policy starting at I0=K requires at least 1 action to identify current mode; constant a1 attains 1 step, so coarse/k1 is globally optimal among four architectures with total 4; others running same action total 6,10,12. With arbitrary nonnegative diagnostic costs, optimality needs assumptions on action costs, so do not overclaim. The user's anticipated coarse/k2 vs fine/k1 tradeoff is NOT supported by this particular model: reset-to-known-mode removes need for sensor and memory.

## Next
To exhibit a genuine sensor-memory tradeoff, specify a relational automaton with nontrivial hidden modes and a target that cannot be solved by simply resetting to a known mode, potentially identify immutable initial mode; use sound finite abstraction and exact initial belief. Distinguish empirical model testing from proof.
