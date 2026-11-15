# TIMDR 51B.15w — Aktywna obserwowalność i bezpieczna diagnostyka
Checkpoint 2026-11-15; continuation of 51B.15v.

## Model
Finite partial-observation safety game G=(X,A,Omega,T,O,D,I0), belief B subset X. For action a, Post_a(B)={x': exists x in B with (x,a,x') in T}; Upd(B,a,o)=Post_a(B) intersect O^-1(o); possible observations Omega_a(B)={o:Upd nonempty}. Action must be enabled for every possible x, with nonempty successor. Safe diagnostic action has Post_a(B) subset D, *before* new observation. No future information can undo unsafe transition.

## Measuring information
Choose uncertainty functional U on nonempty beliefs; worst-case one-step U_worst(B,a)=max_{o in Omega_a(B)} U(Upd(B,a,o)). Strict decrease U_worst(B,a)<U(B) is one possible diagnostic criterion, not necessary for eventual diagnosis; raw belief cardinality may increase under dynamics even if information becomes more useful. Information objective must specify relational, physical, or decision-relevant uncertainty.

## Safety-preserving diagnosis in winning region
Let Z* be greatest winning belief region from 51B.15u. DiagAct(B)={a: Post_a(B) subset D and every possible posterior Upd(B,a,o) in Z*}, with enabled/nonempty successor requirements. For B in Z*, DiagAct(B) nonempty. Any policy selecting DiagAct(B) indefinitely is robustly safe by induction; minimizing U_worst among such actions is safe but does not guarantee uncertainty decreases or diagnosis terminates.

## Reachability of diagnostic target
Let T_diag subset Z* denote desired informative beliefs (e.g. unique relational label, or enough information for specific task). R0=T_diag; R_{n+1}=R_n union {B in Z*: exists enabled a with Post_a(B) subset D and all possible Upd(B,a,o) in R_n}. For finite belief game, B in R_n iff there exists a safe policy guaranteeing T_diag reached within <=n steps, by induction. R_infty union_n R_n stabilizes and characterizes bounded-time worst-case diagnostic reachability in finite game. B may be in Z* but outside R_infty: indefinitely safe without guaranteed identification.

## Worked example
Initial belief B0={p,q}, O(p)=O(q)=o. Safe diagnostic action d maps p->p', q->q' with distinct observations O(p')=o_p and O(q')=o_q; both successor states safe. Posterior after d is singleton {p'} or {q'}, hence diagnosis guaranteed in one step. Subsequent actions may be selected based on observed branch.

## Cost
With nonnegative costs c(B,a), robust shortest-diagnosis objective V(B)=0 for B in target; otherwise min over safe enabled a of c(B,a)+max_{possible o}V(Upd(B,a,o)), restricted to policies guaranteeing target reachability. Zero-cost cycles require proper-policy/rank constraints to avoid interpreting infinite looping as success. Safety is a hard constraint, not a soft cost.

## TIMDR continuous relation
Belief B subset S_Phi x Q. Constraining Pred_a(B) subset union_s ({s} x K_s^infty) is a strong sufficient condition for staying inside earlier all-action robust invariant regions; it can be conservative compared with joint controlled safety-diagnosis synthesis in belief space. All mathematical guarantees conditional on exact/sound transition and observation models and certified reachability.

## Next
51B.15x: safe relational identifiability, permanently indistinguishable relational states, active distinguishing strategies and decision relevance.
