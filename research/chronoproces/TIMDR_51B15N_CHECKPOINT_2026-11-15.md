# TIMDR 51B.15n — certyfikaty nieskończonego horyzontu (2026-11-15)

Research checkpoint, conditional mathematical results, not physical empirical validation. Follows TIMDR_51B15L_15M_CHECKPOINT_2026-11-15.md.

## Setup and robust invariant-region theorem
Finite relational automaton A, admissible event maps delta_a, physical Q and disjoint decoding regions U_s. Post-update disturbance model x_{t+1}=F_{a_t}(x_t)+w_t, w_t in W_{a_t}. If F_a(U_s) + W_a subset U_{delta_a(s)} for all admissible (s,a), then every finite or infinite admissible event/disturbance sequence starting in x_0 in U_{s_0} satisfies x_t in U_{s_t} for all t>=0. Proof by induction. Distinguish pre-update noise F_a(U_s+B_nu) from post-update F_a(U_s)+B_nu.

## Uniform contraction
Ideal z_{t+1}=F_a(z_t), perturbed x_{t+1}=F_a(x_t)+w_t. For common Lipschitz K<1 and ||w_t||<=nu, e_n<=K^n e0+nu(1-K^n)/(1-K), limsup e_n<=nu/(1-K), and sup_n e_n<=max(e0,nu/(1-K)). If ideal trajectories have uniform distance to incorrect decoding region strictly above this bound, decoding remains correct. For K=1 the bound e0+n nu does not prove actual divergence; for K>1 the exponential upper bound similarly need not be tight. Invariance may hold without global contraction.

## Ellipsoidal error invariant set
For e'=A_a e+w, ||w||_2<=nu, common E_P={e:e^T P e<=1}, P positive definite. Sufficient condition ||P^{1/2} A_a P^{-1/2}||_2 + nu ||P^{1/2}||_2 <=1 for all a. Follows from triangle inequality. State-dependent P_s and region-dependent conditions are also possible.

## Volume-preserving obstruction
If U is nonempty bounded measurable subset R^d with positive finite Lebesgue measure, F linear invertible with |det F|=1, and W contains a full-dimensional ball of positive radius, F(U)+W cannot be subset U: volume(F(U))=volume(U), whereas Brunn–Minkowski implies volume(F(U)+W)>volume(U). The statement assumes full-dimensional additive post-update disturbance and bounded region, and is not a universal prohibition of reversible physical dynamics. Compactness not needed; finite positive volume and appropriate measurability suffice.

## Worked example
Q=R, F(x)=x/4 (bijective on R, not volume preserving), automaton A={0,1}, delta(0)=delta(1)=0, U0=(-2,2), U1=(3,5), post-update w in [-nu,nu]. For transition 0->0, image range (-0.5-nu,0.5+nu), clearance 1.5-nu. For 1->0, image (0.75-nu,1.25+nu), clearance 0.75-nu. Uniform positive clearance gamma*=0.75-nu for 0<=nu<0.75. For nu=0.5, gamma*=0.25, guaranteeing correct relational decoding for every admissible sequence. This is a mathematical construction, not an experiment. Note strict margin at boundaries and distinction between open U and closed W.

## Research next
TIMDR 51B.15o: necessary versus sufficient criteria for invariant-region existence; constrained switching, joint spectral radius, nonnormal transient amplification, anisotropic disturbances, reachable sets, and computation of maximal robust controlled-invariant relational regions. Do not claim Lyapunov contraction necessary.
