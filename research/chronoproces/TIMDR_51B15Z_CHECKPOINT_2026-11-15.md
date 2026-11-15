# TIMDR 51B.15z — Wspólna synteza czujników, pamięci i eksperymentów diagnostycznych
Checkpoint 2026-11-15. Continuation of 51B.15y.

## Co-design
Finite physical-relational game G0=(X,A,T,D,I0,lambda), finite sensor designs Theta. Sensor theta has set-valued observation O_theta:X->2^{Y_theta}\{empty}, representing uncertainty. Finite-memory controller K=(M,m0,alpha,eta), alpha:M x Y_theta->A, eta:M x Y_theta->M. Timing: observe y_t, choose a_t=alpha(m_t,y_t), update memory m_{t+1}=eta(m_t,y_t), then environment transitions and emits y_{t+1}. Diagnostic strategy must be implementable by K, not treated as free extra infinite memory.

## Cost and safety
Total cost C_total=C_sensor(theta)+C_memory(|M|)+C_logic(K)+J_diag(theta,K), using consistent economic units/horizon. Hard requirements: all real runs x_t in D^[gamma], guaranteed finite-time identification of relational label lambda, memory budget |M|<=k_max. Pareto alternative for hardware, memory bits ceil(log2|M|), worst-case energy, time, logic. Cost of state-ID bits excludes control tables and numeric implementation.

## Belief update with noisy sensors
Y_theta(B)=union_{x in B} O_theta(x). Psi_{theta,a}(B,y)=Post_a(B) intersect {x': y in O_theta(x')}. For each theta, calculate safety winning region Z_theta^gamma as greatest fixed point over nonempty beliefs B subset D^[gamma] with common enabled action a, nonempty Post_a(B) subset D^[gamma], and all possible nonempty observation posteriors again in region. Diagnostic target consists of winning beliefs with singleton lambda-label, and safe diagnostic reachability follows earlier least-fixed-point iteration.

## More informative sensors
If deterministic mapping f:Y_theta2->Y_theta1 satisfies O_theta1(x)=f(O_theta2(x)) as sets for every x, theta2 can emulate theta1 by preprocessing observation through f. At identical dynamics and no extra memory cost for f, better information cannot reduce existence of winning safety or diagnosis policy; it can still be economically worse due to hardware cost. More observation symbols alone is not a valid information ordering.

## Minimum memory
k_min(theta,gamma,lambda)=minimum number of memory states of finite-state controllers guaranteeing both safety and eventual relational identification, infinity if impossible. k_min^safe(theta,gamma)<=k_min(theta,gamma,lambda). Under sensor simulation with free stateless preprocessing, richer sensor cannot increase minimum memory required for same task. Example from 51B.15u: p--a-->q, q--b-->p, wrong actions unsafe, initial p known. Constant observation needs 2 memory states to alternate a,b; sensor distinguishing p,q permits one-state memoryless observation-based controller.

## Verification
For fixed theta,K, finite product X x M x Y_theta with consistent y in O_theta(x), transitions (x,m,y)->(x',eta(m,y),y') where a=alpha(m,y), (x,a,x') in T, y' in O_theta(x'). Safety iff no reachable product vertex has x outside D^[gamma]. Identification is epistemic: cannot check solely via actual x. Add a belief monitor or certify possible physical states for each reachable controller information state; then guaranteed termination iff no reachable cycle avoiding the informational goal in finite product/monitor. Exact initial observation and initial memory convention must be fixed.

## Decidability
For finite Theta,X,A,Y_theta and bounded k<=k_max, finitely many action/update tables; enumerate and verify via finite product and belief monitor. Existence of a safe diagnostic co-design decidable, and optimal selection within this finite candidate class possible with computable costs; no efficiency claim. Complexity grows rapidly.

## Continuous Chronoproces
Sensor y=g_theta(x)+v, v in V_theta; dynamics x'=F_a(x)+w, w in W_a. Sound finite overapproximate abstraction can certify implementation under correct refinement; abstract optimality is not necessarily continuous optimality, and abstract infeasibility may be conservative. Resource/history-dependent dynamics require augmented Markov state.

## Scope
Co-design may make individually minimal sensor, memory and diagnostic policy globally suboptimal or infeasible. Hard safety margin gamma remains nonnegotiable. Joint design closes 51B.15r–z series.
