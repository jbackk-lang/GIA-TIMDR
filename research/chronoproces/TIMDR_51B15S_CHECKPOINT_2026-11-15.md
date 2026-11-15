# TIMDR 51B.15s — Minimalna pamięć informacyjna dla odpornego sterowania
Checkpoint 2026-11-15. Continuation of 51B.15r.

## Scope and robustness caveat
Set-membership worst-case guarantees cover all modeled disturbances W_a and observation errors V, conditional on correct model, initial set containment, and information timing; they are not unconditional physical guarantees.

## History and belief sufficiency
Controller history h_t=(y0,a0,y1,...,a_{t-1},y_t). Exact belief B(h_t) subset S x Q updates recursively B(h a y)=Psi_a(B(h),y). For Markov physical/relational dynamics and the stated observation model, exact belief is a sufficient statistic for possible future pairs. It need not be minimal for safety.

## Safety language and online congruence
For a history h, L_safe(h) denotes all future observation-feedback policies that guarantee safety against all compatible future disturbances/observations. Equality of L_safe defines a decision-language equivalence, but by itself need not establish a right-congruence for online updating. For implementable quotient, require agreement of relevant safety outputs and admissible actions, agreement on possible next observations per action, and right-congruence h1~h2 implies h1 a y~h2 a y whenever the extension is possible. Then Z=H/~ supports update tau(z,a,y). If finite, N classes can be represented with ceil(log2 N) bits for state ID, excluding transition tables, numerical representation and computation. Given a safe policy on classes whose transitions remain within safe classes, inductively obtain infinite-horizon robust safety. Stronger equality of all safe policies vs existence of one safe policy are distinct minimization problems.

## Simple example
Single relational state s, Q=R, D=[-1,1], F_0(x)=0, F_1(x)=2, no process disturbance. Beliefs B1={-0.8,-0.3} and B2={0.2,0.9} differ, but only a=0 is safe for both; a=0 sends both to {0}. With observations that do not introduce safety-relevant distinctions, they can be compressed into one information state. This illustrates nonminimality of exact belief, not a universal characterization of minimal quotient.

## Non-equivalence warning
Same currently safe action does not imply equivalent future information. Histories can require different future decisions after a shared action/observation. Iterative partition refinement of finite informational abstractions may construct an update-stable congruence. Continuous observations/infinite beliefs need not admit a finite exact quotient. Certified finite approximations require separate soundness proof. State-memory bits are not physical continuous dimension.

## Next research
Formalize safety-language residuals and a Myhill-Nerode-like minimality theorem under explicit finite observation/action alphabets and admissibility semantics; derive lower bounds on controller memory and observation precision; distinguish all-safe-policy preservation from existence of some safe strategy.
