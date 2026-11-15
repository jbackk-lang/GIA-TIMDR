# TIMDR 51B.16j — Certyfikacja regulatorów o ograniczonej pamięci
Checkpoint 2026-11-15.

## Exact memory product
Node z=(m,B,y) with controller memory m before processing current observation y, exact posterior belief B, and current observation y. Action a=alpha(m,y), next memory m'=eta(m,y), next node z'=(m',Psi_a(B,y'),y') for each feasible observation y'. Controller is not permitted to inspect hidden physical state or belief B. Initial nodes are (m0,I0 intersect O^{-1}(y0),y0).

## Positive certificate obligations
Finite Model from 51B.16i, MemoryCertificate(k,alpha,eta,nodes,rank,initial_memory). Verify k>=1, m0 in [0,k), complete typed alpha,eta on M x Y; node typing, nonempty safe posterior beliefs consistent with observation; initial-node coverage; for every non-target node exact post subset K; all feasible observation branches covered; natural rank >=1 strictly decreases for all non-target successors. Terminal target means diagnosis task stops; no infinite-horizon safety after stopping claimed. Theorem: finite-memory controller with valid certificate guarantees safety until termination and finite-time current-label identification.

## Implemented
/mnt/data/timdr_51b16j/base_checker.py (copied 51B.16i finite model)
/mnt/data/timdr_51b16j/memory_checker.py (explicit memory certificate checker)
/mnt/data/timdr_51b16j/test_memory_checker.py (unittest)
/mnt/data/timdr_51b16j/README.md
/mnt/data/timdr_51b16j_prototype.zip

Local command: cd /mnt/data/timdr_51b16j && python -m unittest -v
Observed 4 test methods passed. Tests: one valid k=1 diagnostic probe controller, six mutated certificates rejected, exhaustive enumeration of all k=1,2 controller tables on small indistinguishable identity game (all impossible), independent graph cycle oracle comparing reference good/bad controllers.

## Scope and limitations
This tests the explicit memory implementation but is not a formally verified kernel. No bounded-memory negative certificate checker; enumeration test covers only a small toy game. No model/certificate serialization, origin tags, continuous dynamics, verified arithmetic, or post-diagnosis infinite safety. Full implementation and broader property-based differential tests remain open.
