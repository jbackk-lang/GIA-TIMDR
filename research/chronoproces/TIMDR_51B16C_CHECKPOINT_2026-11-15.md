# TIMDR 51B.16c — Naprawa odpornego cyklu Chronoprocesu przy pierwotnym poziomie zakłóceń
Checkpoint 2026-11-15.

## Fixed original model
Two relational modes s1,s2, alternating automaton delta_a(s1)=s2, delta_a(s2)=s1 for both actions. Gamma=.2 yields K1=[-2.8,.8], K2=[-.8,2.8]. Dynamics x'=x/2+u(a)+w, |w|<=nu=.15. Sensors: coarse sign(x), fine round(x,1)+v, |v|<=.05.

## General robust two-phase cycle
For action offsets u0,u1, cycle nominal centers c2=c1/2+u1 and c1=c2/2+u0, hence c1=(2u1+4u0)/3 and c2=(4u1+2u0)/3. Symmetric corridor H_i=[c_i-r,c_i+r] robustly invariant under a1 from H1 to H2 and a0 from H2 to H1 iff r/2+nu<=r, i.e. r>=2nu=.3. To fit K1,K2 with r=.3, require -2.5<=c1<=.5 and -.5<=c2<=2.5.

## First repair: u0=0,u1=.6
Centers c1=.4,c2=.8, corridors H1=[.1,.7], H2=[.5,1.1]. Exact robust equalities F_a1(H1)+W=H2 and F_a0(H2)+W=H1, both inside corresponding K. Hence robust gamma=.2 infinite-horizon safety at original nu=.15. BUT H1 and H2 overlap [.5,.7], so neither physical sensor can distinguish the relational phase at overlapping x; fine cannot be proven memoryless by phase observation. Coarse remains R on both and 2-state memory can track known initial phase.

## Full repair preserving sensor-memory tradeoff: u0=-.3,u1=1.2
Centers c1=.4,c2=1.4; H1=[.1,.7] subset K1, H2=[1.1,1.7] subset K2. Exact images:
F_a1(H1)+[-.15,.15]=[1.1,1.7]=H2;
F_a0(H2)+[-.15,.15]=[.1,.7]=H1.
Both positive, so coarse reports R in both phases. With initial phase s1 known and x0 in H1, coarse requires and suffices 2-state memory alternating a1,a0. A 1-state coarse controller always chooses same action under R and cannot preserve alternating corridor. Fine sensor round(x,1)+v with |v|<=.05 has y<=.75 on H1, y>=1.05 on H2; threshold y=.9 supports memoryless controller choosing a1 for y<.9 and a0 for y>=.9. Thus k_min(coarse)=2, k_min(fine)=1 for specified corridor-maintenance task, at original nu=.15 and gamma=.2. This is phase tracking with known initial calibration, not initial-mode diagnosis from unknown phase.

## Repair by altering margin or decoding region
Original u0=0,u1=1 and nu=.15 requires r=.3 and H1=[11/30,29/30], H2=[31/30,49/30]. With D_s1=[-3,1], fitting H1 into D_s1^[gamma] requires gamma<=1/30=.033333..., weaker than original .2. To retain gamma=.2, need expand D_s1 upper endpoint to >=29/30+.2=7/6, requiring independent semantic/physical justification. Neither should be silently called equivalent to original hard safety requirements.

## Longer or asymmetric cycle
For phases with interval H_i=[l_i,r_i] and action a_i, robust successor inclusion requires l_{i+1}<=l_i/2+u(a_i)-nu, r_{i+1}>=r_i/2+u(a_i)+nu, H_i subset K_{s_i}, cyclic indexing. These are linear inequalities for fixed action words and offsets, so feasibility can be checked by linear programming. Longer cycle is not guaranteed to exist or improve feasibility.

## Conclusions
Changing both action offsets to -.3 and 1.2 repairs original-noise robust safety AND maintains sensor-memory substitution. Simply shrinking positive amplitude to .6 repairs safety but not sensor phase separation. Do not confuse calibrated phase tracking with acquisition of unknown initial relational information.
