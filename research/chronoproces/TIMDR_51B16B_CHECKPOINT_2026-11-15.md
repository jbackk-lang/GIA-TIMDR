# TIMDR 51B.16b — Relacyjny automat testowy i rzeczywista wymienność czujnika z pamięcią
Checkpoint 2026-11-15.

## Non-synchronizing relational automaton
S_Phi={s1,s2}. For both actions a0,a1 define delta_a(s1)=s2 and delta_a(s2)=s1. Every action swaps modes, hence any action word acts as a permutation and cannot synchronize distinct initial modes. Physical dynamics x'=x/2+u(a)+w, u(a0)=0,u(a1)=1. Safe gamma=.2 regions K1=[-2.8,.8], K2=[-.8,2.8]. Coarse sensor sign(x); fine sensor round(x,1)+v, |v|<=.05.

## Alternating phase cycle
Desired a1 from s1 to s2 and a0 from s2 to s1, nominal centers x1=2/3 and x2=4/3. Both positive so coarse always reports R. For symmetric robust phase intervals H1=[2/3-r,2/3+r], H2=[4/3-r,4/3+r], invariance requires r>=2nu. At original nu=.15, minimal r=.3; H1 upper 29/30=.9667 exceeds K1 upper .8. More generally if any nonempty compact intervals I1 subset K1 and I2 subset K2 satisfy robust a1(I1) subset I2 and a0(I2) subset I1, their upper endpoints obey U2>=U1/2+1+nu, U1>=U2/2+nu, hence U1>=2/3+2nu. Since U1<=.8, necessary nu<=1/15. Original nu=.15 violates. This is a no-go for the specified robust two-phase corridor, not all possible strategies.

## Explicit modified reference variant 16b-R
Reduce only disturbance bound to nu=.05 (not a claim about original nu=.15). Choose H1=[17/30,23/30] = [2/3-.1,2/3+.1], H2=[37/30,43/30] = [4/3-.1,4/3+.1]. H1 subset K1, H2 subset K2. Exact robust equalities a1(H1)+[-.05,.05]=H2 and a0(H2)+[-.05,.05]=H1. Operational requirement is infinite-horizon corridor H=({s1}xH1) union ({s2}xH2), stronger than original safe K. Assume initial phase s1 known and x0 in H1.

## Memory/sensor substitution theorem
Coarse sees R in both H1,H2. A 2-memory-state controller alternates a1 then a0, preserving H robustly. One-state coarse controller always sees R and so outputs a constant action; a1 required to move H1->H2, a0 required to move H2->H1; therefore k_min(coarse)=2 for this corridor task with known initial phase.
Fine output on H1 <=.85 and on H2 >=1.15 (rounding to nearest tenth with tie rule irrelevant at these extrema); memoryless threshold y<1 selects a1, else a0. Thus k_min(fine)=1. Full robustness for all disturbances and sensor noise as bounded.

## Epistemic caveat
This is phase tracking with initial calibration, not identification of initially unknown relational phase. If initial belief includes both ({s1}xH1) and ({s2}xH2), coarse cannot safely select the correct first corridor-preserving action; memory does not create absent initial information. Fine can identify phase directly via separated outputs. Do not mislabel coarse phase tracking as active diagnosis of unknown origin.

## Costs
Given sensor coarse=2, fine=8, memory k1=1,k2=3: certified coarse/k2 fixed cost 5; fine/k1 fixed cost 9; coarse/k1 fixed cost 3 but infeasible for corridor task; fine/k2 cost 11 but redundant. With same physical alternating actions and identical action cost, coarse/k2 cheaper by 4, excluding initial calibration cost.

## Next
51B.16c could add explicit initial calibration protocol, task-relevant relational identification, and certified optimization including calibration cost, or investigate impossibility with original nu=.15 under alternative automata.
