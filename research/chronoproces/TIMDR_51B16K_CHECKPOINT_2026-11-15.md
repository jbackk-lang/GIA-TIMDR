# TIMDR 51B.16k — Negatywne certyfikaty ograniczonej pamięci i kwantyzacja
Checkpoint 2026-11-15.

## Formal result
For finite state model with actions A, observations Y and memory k, deterministic total controller tables alpha,eta:M x Y->A,M (fixed m0=0) have count N_k=(|A|k)^(k|Y|). A negative architecture certificate enumerates all tables and provides for each a reachable unsafe prefix or an exact nonterminal epistemic lasso in product z=(m,B,y). Checker verifies every table is represented exactly once and all witness edges are legal. Theorem: accepted complete certificate proves no k-memory controller guarantees safety until diagnosis and finite-time current-label identification.

## Implemented code
Prototype archive: /mnt/data/timdr_51b16k_prototype.zip
Modules: base_checker.py, memory_checker.py, negative_checker.py, test_negative_checker.py, README.md. Untrusted generator find_refutation/synthesize_negative_certificate is separate from verify_memory_negative and check_witness. Checker returns VALID_NEGATIVE, INVALID_CERTIFICATE, UNVERIFIED (including excessive enumeration). Positive checker from 51B.16j included.

## Tests actually executed
cd /mnt/data/timdr_51b16k && python -m unittest -v
4 tests passed in ~0.20 s:
- identity ambiguous 2-state model: all k=1 controllers (2) and k=2 controllers (16) refuted, VALID_NEGATIVE.
- missing, duplicate, invalid cycle index rejected; enumeration limit UNVERIFIED.
- diagnostic probe model: generator cannot produce negative proof for k=1 or k=2.
- differential comparison of witness generator with independent reachable-product graph oracle on tiny games.
During development a cycle index bug was found by tests and fixed before final rerun.

## Quantization limits
Continuous Q cells do not become controller-visible sensor values. Forward overapprox supports positive safety but negative abstract lassos may be spurious. Negative transfer requires concrete realizability for every adversarial response or a verified alternating game relation. No continuous negative checker implemented.

## Limitations
Prototype not formally verified, shared Model semantics between generator and checker, limited tests, no serialized canonical format, no origin tags, no post-diagnosis infinite safety, exponential table enumeration, no general nonlinear continuous proof support.
