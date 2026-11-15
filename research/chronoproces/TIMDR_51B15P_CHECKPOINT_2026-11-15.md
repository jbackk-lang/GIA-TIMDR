# TIMDR 51B.15p — obliczalna synteza i certyfikacja obszarów odpornych
Checkpoint 2026-11-15. Continuation of TIMDR 51B.15o.

## Sound inner and outer approximations
For relational automaton A, correct decoding regions D_s, post-update dynamics x'=F_a(x)+w, w in W_a, maximal robust invariant family K^infty from 51B.15o. Certified inner sets L_s must satisfy L_s subset D_s and F_a(L_s)+W_a subset L_delta_a(s) for all admissible (s,a). Then L_s subset K^infty_s by maximality. Outer approximations can be finite predecessor iterates K^(n) from D; K^infty subset K^(n). Numerical candidate alone is not a certificate.

## Polyhedral verification
For affine F_a(x)=A_a x+b_a, source K_s={x:H_s x<=h_s}, target K_t={x:H_t x<=h_t}, compact polyhedral W_a, exact inclusion F_a(K_s)+W_a subset K_t iff for every row i of H_t:
sup_{x in K_s} (H_t)_i A_a x + (H_t)_i b_a + sup_{w in W_a}(H_t)_i w <= (h_t)_i.
With fixed polyhedra these are linear programs (if nonempty and bounded where appropriate). Simultaneous synthesis of unknown facet normals, centers, and dynamics is generally nonconvex; exactness of LP verification does not imply tractability of all synthesis tasks.

## Ellipsoidal verification
For K_s={x:(x-c_s)^T P_s (x-c_s)<=1}, P_s positive definite, target t=delta_a(s), centered affine transition A_a c_s+b_a=c_t and Euclidean noise ||w||<=nu, sufficient:
||P_t^(1/2) A_a P_s^(-1/2)||_2 + nu ||P_t^(1/2)||_2 <=1.
Not necessary; optimization over P_s and other variables is not always a convex LMI problem.

## Certified grid algorithm
Partition bounded Q into finitely many cells C_i. Start with cells wholly contained in D_s. For each cell C and action a, compute guaranteed outer reachability R_a(C) satisfying F_a(C)+W_a subset R_a(C). Iteratively remove any cell for which an admissible action has R_a(C) not contained in union of currently retained target-state cells. Iterate to fixed point. Returned unions L_s satisfy robust invariance and are sound inner approximations, provided cell membership and reachability tests are mathematically rigorous. Finite grid ensures finite termination (only deletions), but the result is maximal only relative to this conservative finite-cell test, not necessarily maximal in continuous Q. Sampled simulations without rigorous reachability bounds do not certify safety. In controlled variant retain cell if exists an action whose reachable set lies in safe target union; output a state/cell feedback policy. In exogenous variant require every admissible action. Observation uncertainty and ability to select a before disturbance require explicit modeling.

## Complexity and completeness
With r cells per coordinate in dimension d, r^d cells. Polyhedra may have facet explosion; ellipsoids may be conservative; grids suffer curse of dimensionality. Inner soundness does not imply convergence to maximal invariant set as grid size tends to zero. Empty-interior safe sets, zero-margin boundaries, nonregular dynamics can defeat conservative grid completeness. Numerical outward rounding/interval arithmetic or exact rational arithmetic may be necessary for formal certification.

## Main distinction
Correctly decoded region D_s need not equal robust viable region K^infty_s. Candidate synthesis + rigorous outer reachability + independently checked invariance gives a sound safety certificate. This is conditional mathematical assurance, not proof of physical reliability outside the modeled disturbances and observation assumptions.
