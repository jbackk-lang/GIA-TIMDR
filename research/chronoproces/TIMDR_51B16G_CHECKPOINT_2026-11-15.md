# TIMDR 51B.16g — Certyfikaty niemożliwości identyfikacji
Checkpoint 2026-11-15.

## Formal problem
Finite partial-observation hybrid game G=(X,A,T,O_theta,K,I0,lambda), nonempty T(x,a), set-valued O_theta(x). Belief update Psi_a(B,y)=Post_a(B) intersect O_theta^{-1}(y). Target I_lambda={nonempty B:|lambda(B)|=1}. Need policy pi such that for every admissible run, all physical states in K and some finite-time belief in I_lambda. Negation: for every pi, some run either violates safety or never reaches knowledge target. Initial observations partition I0 into B0(y0); analyze each nonempty initial observation belief. For origin-label identification use immutable origin tag.

## Finite-game winning fixpoints
Safety winning beliefs Z_* greatest fixpoint of beliefs B subset K with some action whose all possible nonempty successor beliefs lie in Z_*; equivalent to all actual successors safe. Reachability rank R0=Z_* intersect I_lambda; R_{n+1}=R_n union {B in Z_*: exists robust safe action a such that for every realizable next observation y, Psi_a(B,y) in R_n}. Finite stabilization. B0 in R_* iff an observation-history strategy can enforce safe finite-time identification; rank decreases uniformly, so winning strategy has bounded worst-case diagnosis time. For all initial observations require each B0(y0) winning.

## Negative epistemic trap
Nonempty L disjoint from target; for every B in L and every a either Post_a(B) not subset K (unsafe action), or exists realizable observation y with Psi_a(B,y) in L. This locally checkable dual certificate defeats any controller strategy: unsafe action admits a violating run; otherwise environment keeps beliefs in L. For finite-state systems consistent infinite path exists (König lemma). A pure information barrier additionally requires that controller can maintain safety indefinitely but environment can keep ambiguity; otherwise failure may be mixed safety/information.

## Finite example
X={p,q}, labels distinct, both actions identity transitions, both states safe, O(p)=O(q)={R}, initial belief {p,q}. Trap L={% raw %}{{p,q}}{% endraw %} closed for both actions, so safe survival feasible but no diagnosis with any memory.

## Concrete continuous variant A witness
Original x'=x/2+u(a)+w, u(a0)=0,u(a1)=1, |w|<=.15, relational modes fixed. K1=[-2.8,.8], K2=[-.8,2.8], B0={(s1,0),(s2,0)}. Action a1 from possible (s1,0) has successor [.85,1.15] outside K1, so no robust safe strategy can choose a1 on common ambiguous history. Under a0 and environment disturbance w=0, x=0 remains for both modes forever; sensors coarse sign and fine round(x,1)+v yield same outputs for same x and equal chosen sensor-noise sequence. Thus no safe sure diagnosis for either sensor and any controller memory, though safe survival possible with a0. Concrete realizable infinite witness avoids abstraction artifacts.

## Bounded controller memory
For finite action alphabet A, observation alphabet Y, memory size k, fixed initial memory, deterministic controller tables alpha,eta:M x Y -> A,M number (|A|k)^(k|Y|). Enumerate and independently verify each candidate's physical safety and epistemic diagnosis; exclusion of all proves impossibility within finite class. If initial memory state selectable, account for k initializations. For continuous observation alphabet (fine sensor), finite enumeration requires proven finite observation partition or restricted controller class. A failed individual controller does not prove architecture infeasibility.

## Negative abstraction transfer
Sound overapprox B subset Bhat supports positive singleton knowledge but abstract ambiguous beliefs can be spurious. Abstract trap alone is NOT proof of real impossibility. Need actual realizable adversarial strategy or a verified alternating/simulation relation that transfers each adversarial response to a concrete admissible run, preserving observation and label ambiguity. A mere forward overapprox Post(H) subset widehatPost(H) does not guarantee abstract edges are realizable.

## Certificate artifacts and statuses
Machine-checkable negative proof obligations: model dynamics, initial belief, hard safety, action coverage, realizable adversarial observations/transitions, invariant ambiguity; example structured YAML is illustrative schema, not executable verifier. Distinguish CERTIFIED_FEASIBLE, INFORMATION_IMPOSSIBLE, SAFETY_IMPOSSIBLE, MEMORY_INSUFFICIENT (with bounded impossibility plus wider-class feasibility), UNKNOWN. Universal completeness for nonlinear continuous dynamics not claimed.
