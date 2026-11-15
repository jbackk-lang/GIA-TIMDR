# TIMDR 51B.16e — Adaptacyjne dzielenie przestrzeni stanów i certyfikowana kontrola konserwatyzmu abstrakcji
Checkpoint 2026-11-15.

## Tri-valued semantics
For concrete Post_a(H)=P subset sound overapprox Phat: SAFE if Phat subset target H' and inductive cycle closes; UNSAFE only if an actual realizable admissible successor/trajectory outside H' is certified; UNKNOWN if abstraction violates inclusion without concrete witness. UNKNOWN is not physical unsafety. Infinite-horizon SAFE needs invariant/inductive closure.

## Quantifying conservatism
One-sided Hausdorff error eps_abs(P,Phat)=sup_{z in Phat}dist(z,P), usually not directly computable. For target polytope H'={z:Gz<=h}, facet residual rho_j(Phat)=sup_{z in Phat}(g_j^T z-h_j). All rho_j<=0 certify inclusion; positive residual localizes obstruction but not necessarily real violation.

## Example: nonlinear dependency loss
F(x,q)=(x,x^2), x in [-1,1]; concrete reachable parabola P={(x,x^2)} is safe for target H'={(z1,z2):z2>=z1^2}. Coordinate box Phat=[-1,1]x[0,1] contains spurious (1,0), hence only UNKNOWN, not UNSAFE.

## Sound adaptive subdivision
If H covered by union H_i, each Post(H_i) subset Phat_i, then Post(H) subset union_i Phat_i. Preserve union rather than collapse to one box. To ensure monotonic tightening define Phat^(n+1)=Phat^n intersect (union_i Phat_i^(n+1)); both contain concrete P so inclusion preserved and new overapprox subset old.

## Certified parabola refinement with positive margin
Target H'_mu={(z1,z2):z2>=z1^2-mu}, mu>0. For cell I=[l,r], width h, center c, exact x^2=c^2+2c(x-c)+(x-c)^2, remainder in [0,h^2/4]. Correlated enclosure Phat_I={(z1,z2):z1 in I,z2=c^2+2c(z1-c)+rI,0<=rI<=h^2/4}. Then z2-z1^2>=-h^2/4. So h<=2sqrt(mu) sufficient for sound inclusion. At mu=.01, width <=.2; ten equal cells partition [-1,1]. At mu=0 this particular enclosure has no finite subdivision guarantee despite concrete safety; choose exact relational representation instead.

## CEGAR-TIMDR
Iterate sound image computation, verify corridor inclusions, certify SAFE if inductive, certify UNSAFE only via concrete witness, else select blocking facets and refine local cells or representation. Return UNKNOWN on exhausted budget. Soundness of each positive/negative certificate does not imply completeness or termination.

## Observation semantics
For set-valued sensor O_theta(x), Y_theta(H)=union_{x in H}O_theta(x). Robust one-step distinguishability requires Y_theta(H_i) intersect Y_theta(H_j)=empty. Disjoint sound overapproximations suffice; overlapping overapproximations do not prove true ambiguity. Original 2D corridors H1=[.1,.7]x[-.1,.1], H2=[1.1,1.7]x[-.1,.1]: fine round(x,1)+v, |v|<=.05 yields y<=.75 in H1, y>=1.05 in H2; coarse sign(x) always R in both. Refinement cannot create sensor information absent physically.

## Conditional finite certification theorem
If concrete P compact and strictly inside target H' with positive clearance d, abstraction family converges uniformly in Hausdorff as max cell diameter->0, and refinement schedule makes relevant cell diameters->0, then finite refinement level yields Phat subset H'. Boundary-touching cases may fail forever. Heuristic selection by predicted violation reduction per cost does not affect soundness but no global optimality is claimed.

## Research next
51B.16f could integrate adaptive geometric abstraction with epistemic belief refinement and controller-memory synthesis, and prove refinement preservation under observation nondeterminism. Also measure real computational complexity, not claim dimension curse solved.
