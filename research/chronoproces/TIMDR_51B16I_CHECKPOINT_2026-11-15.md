# TIMDR 51B.16i — Minimalne jądro dowodowe: prototyp i testy
Checkpoint 2026-11-15.

## Implemented local prototype
Created files in local runtime:
- timdr_51b16i/checker.py: exact finite-game checker in Python, no external dependencies
- timdr_51b16i/test_checker.py: four unittest methods with valid and intentionally corrupted positive and negative certificates, initial observation branches, unsupported model
- timdr_51b16i/README.md: usage, precise scope and limitations
- timdr_51b16i_prototype.zip: downloadable archive.

Local command: cd timdr_51b16i && python -m unittest -v
Result: 4 tests passed (4/4).

## Exact semantics
Finite Model stores states, actions, observations, total nonempty transitions T(s,a), nonempty observation possibilities O(s), safe K, initial I0 and current-state labels. Initial observation partitions I0 into nonempty initial beliefs. Belief update Psi_a(B,y)=Post_a(B) intersect O^{-1}(y).

verify_positive checks initial belief coverage, safe nonempty nodes, action for each nontarget belief, exact post safety, all feasible observation successor beliefs covered, and strictly decreasing natural rank for each nontarget successor. Terminal singleton-label beliefs stop the task. It checks belief-based strategy, NOT a bounded k-state controller implementation.

verify_negative checks initial belief coverage, all trap beliefs safe and ambiguous, and for every trap belief and action either an exact unsafe successor exists or some feasible observation has exact successor belief in trap. Sound for finite model and all observation-history policies.

Statuses VALID_POSITIVE, VALID_NEGATIVE, INVALID_CERTIFICATE, UNVERIFIED (non-Model input).

## Honest limitations
This is a tested prototype, not a formally verified checker. No bounded-memory alpha/eta validation, no continuous systems, no certified arithmetic, no canonical serialization/fingerprint, no immutable-origin label semantics, no safety guarantee after diagnosis stops. Four passing tests cannot prove code correctness or reliability against all malicious certificates.

## Next tasks
Add explicit k-state controller product, immutable origin labels, independent serialized certificate schema, property-based exhaustive cross-check on tiny games, and continuous proof obligations.
