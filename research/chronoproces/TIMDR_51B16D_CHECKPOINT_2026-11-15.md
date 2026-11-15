# TIMDR 51B.16d — Skalowanie certyfikowanej syntezy na układy wielowymiarowe i nieliniowe
Checkpoint 2026-11-15.

## General hybrid model
X=S_Phi x Q, Q subset R^n. s'=delta_a(s), x'=f_{s,a}(x,w), w in W_{s,a}. Mode-specific hard safe K_s^gamma={x in D_s:dist(x,R^n\D_s)>=gamma} (or relative Q complement, if explicitly selected). Joint safe K^gamma=union_s {s}xK_s^gamma. Reachable set Post_{s,a}(H)={f_{s,a}(x,w):x in H,w in W}. Sound overapproximation Post(H) subset widehatPost(H). If corridors H_i subset K_{s_i}^gamma, delta_{a_i}(s_i)=s_{i+1}, and widehatPost_{s_i,a_i}(H_i) subset H_{i+1} cyclically, induction proves infinite-horizon robust safety for all disturbances. Failure of an overapprox inclusion need not imply concrete infeasibility.

## Polyhedral certificate
Affine x'=A_{s,a}x+b_{s,a}+E_{s,a}w. H_i={x:G_i x<=h_i}. For each target facet g^T x<=h, robust inclusion is max_{x in H_i}g^T A x + g^T b + max_{w in W}g^T E w <=h. For compact polytopes and fixed matrices, evaluate via linear programs. Joint synthesis of shape and feedback may be nonconvex.

## Ellipsoidal certificate
E(c,P)={x:(x-c)^T P^{-1}(x-c)<=1}, P positive definite. For disturbance ellipsoid E(0,R), affine image centered at c'=Ac+b is enclosed by E(c',Pbar), with Pbar=(1+epsilon) A P A^T+(1+1/epsilon) E R E^T, epsilon>0, Pbar positive definite. Inclusion in target E(c',P') follows from Pbar <= P' (PSD ordering). Sufficient, not necessary; shifted target centers require additional handling.

## Nonlinear remainder
For x'=f(x)+Ew, Taylor expansion f(x)=f(c)+J(c)(x-c)+r(x). If r(H) subset certified R(H), then Post(H) subset f(c)+J(c)(H-c) plus R(H) plus E W (Minkowski sums). If second derivative norm uniformly <=L on convex corridor, norm remainder <= L/2 norm(x-c)^2. Sampled numerical bounds alone do not certify global inclusion.

## Explicit two-dimensional reference example
Let z=(x,q), x'=x/2+u(a)+w_x, q'=q/4+w_q, |w_x|<=.15, |w_q|<=.05, u(a0)=-.3,u(a1)=1.2. Relational automaton swaps s1,s2 after each action. Corridors H1=[.1,.7]x[-.1,.1], H2=[1.1,1.7]x[-.1,.1]. Exact x images under a1(H1) and a0(H2) match next x intervals. q image [-.075,.075] subset [-.1,.1]. Thus robust inclusions H1--a1-->H2--a0-->H1.
Extend decoding sets to Dtilde_s1=[-3,1]x[-1,1], Dtilde_s2=[-1,3]x[-1,1]; with Euclidean gamma=.2, eroded Ktilde_s1=[-2.8,.8]x[-.8,.8], Ktilde_s2=[-.8,2.8]x[-.8,.8]. Corridors contained in respective eroded sets, giving infinite-horizon gamma safety for all disturbances.

## Sensor-memory tradeoff in 2D
Coarse O_c(x,q)=sign(x) gives R throughout both corridors, so with known initial phase s1, 2 memory states are necessary/sufficient to alternate a1,a0. Fine O_f(x,q)=round(x,1)+v, |v|<=.05 yields y<=.75 in H1 and y>=1.05 in H2; one-state controller threshold y<.9 ->a1 else a0 works. k_min(coarse)=2, k_min(fine)=1 for corridor maintenance with known initial phase. Does NOT imply coarse can identify unknown initial mode.

## Co-design
Optimize sensor cost, controller memory and logic, worst-case diagnostic cost, over safe corridors and sound overapproximations, with relational automaton consistency and explicit epistemic goal. Nonlinear joint synthesis often nonconvex; distinguish candidate discovery from independent sound certification. Global optimum for general nonlinear Chronoprocess not established.
