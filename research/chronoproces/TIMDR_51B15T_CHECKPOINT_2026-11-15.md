# TIMDR 51B.15t — Twierdzenie o minimalności automatu bezpieczeństwa
Checkpoint 2026-11-15. Continuation of 51B.15s.

## Finite-alphabet informational histories
Let A and Y be finite action/observation alphabets, H a prefix-closed set of admissible histories (encoded as alternating action-observation pairs, with initial observation convention). Exact belief B(h) subset S x Q. Define sigma(h)=1 iff B(h) is contained in the prescribed safe relational-physical decoding domain, else 0. Extensions h u must preserve admissibility, including impossible observation sequences.

## Safety Myhill-Nerode equivalence
h1 equiv_MN h2 iff for every finite future word u in (A x Y)*, h1u admissible iff h2u admissible, and when admissible sigma(h1u)=sigma(h2u). This is a right-congruence. Quotient H/equiv_MN supports deterministic online transition tau([h],a,y)=[hay], exact safety output, and exact extension-domain recognition. Minimal deterministic exact monitor has precisely |H/equiv_MN| states, possibly infinite. Proof: quotient construction establishes upper bound; any exact deterministic monitor merging histories must yield identical future outputs and admissibility and hence histories belong to same equivalence class. Finite monitor state ID requires ceil(log2 N) bits, excluding transition/output tables and numeric representation.

## Crucial distinction from controller minimization
A safety controller need only implement one safe observation-feedback policy, not preserve outcomes for all possible actions. Thus minimal exact monitor may have more states than a safe controller. Example two safe states p,q, actions a,b, one observation symbol; a keeps both safe (p->p, q->q), b keeps p safe but sends q to unsafe sink. Exact monitor must distinguish p,q because action b separates safety futures, but constant-action controller always choosing a needs only one memory state. Note physical states must be distinguished by initial information histories for the monitor lower-bound comparison; this is an abstract deterministic transition-system example.

## Finite-memory controller
Controller K=(M,m0,alpha,eta), action alpha(m,y), memory update eta(m,y), with explicit observation timing. Minimize |M| subject to robust safety for all reachable observation/disturbance histories. No general equality between controller memory minimum and |H/equiv_MN|. Pairwise policy-relevant histories that cannot be merged under any safe realization give lower bounds k states and ceil(log2 k) bits, but this requires careful reachability and strategy quantifiers. Distinguish minimal sufficient belief state, minimal exact monitor, and minimal safety controller.

## Limitations
Myhill-Nerode result applies to exact deterministic monitors of a specified safety output and extension-domain language. It does not by itself prove minimality of robust controller or guarantee finite quotient in continuous observations. Safety of the underlying physical system remains conditional on modeled W,V, initial beliefs and observability. Future work: memory lower bounds for strategy synthesis, finite-state safety games, observation equivalence, decidability and complexity.
