# Physical analogies and falsifiable comparisons for GIA-TIMDR

Date: 2026-11-13. Scope: comparisons with particle motion, molecular dynamics, and observed astrophysical motions. These are analogies and proposed tests, **not** assertions that a reflection group models physical forces.

## Mathematical-to-physical dictionary

| GIA-TIMDR quantity | Physical counterpart | Required additional assumptions |
| --- | --- | --- |
| Proper screw isometry (axis a, angle θ, pitch h) | Helical trajectory of charged particle in a uniform magnetic field | A physical time step Δt and Lorentz equation m dv/dt=q v×B; ω_c=|q|B/m, ρ=v_perp/ω_c, pitch per turn=2πv_parallel/ω_c |
| Center displacement relative to screw axis | Orbital motion of a point about a fixed axis | Continuous trajectory and angular velocity; geometry alone does not imply centripetal force |
| Noncommuting rotations R1R2≠R2R1 | Molecular rotations, rigid-body attitude, precession | Dynamics, inertia tensor, torques, and angular momentum |
| Changes of axis under repeated compositions | Precession and nutation | A physical evolution law, not arbitrary reflection words |
| Distribution of directions in long words | Particle scattering / transport | A stochastic or deterministic sampling law and time parameter |
| Closed/near-closed orbits and angular ratios | Resonances in orbital dynamics | Equations of motion and perturbations, not visual resemblance |
| Expanding or helical orbit geometry | Astrophysical jets / magnetized plasmas | MHD or relativistic plasma physics and observed kinematic scales |

## Exact geometric control identity

For a proper screw isometry g and the prism centroid O, if ρ is distance from O to the screw axis, θ is rotation angle and h axial translation, then

||g(O)-O||² = 4ρ² sin²(θ/2) + h².

This is a *finite displacement identity*. It must not be identified with an acceleration or energy without specifying time and dynamics.

## Research tests

1. **Helix test:** Select a one-parameter sequence g^n for a fixed proper screw isometry and compare center positions with a mathematical helix. Then compare with cyclotron trajectories only after introducing Δt, q, m, and B. Distinguish g^n from the entire reflection-group orbit.
2. **Noncommutativity test:** Measure ||(g1g2)(O)-(g2g1)(O)|| and relative rotation angle for selected proper isometries. Test parameter dependence. This measures order sensitivity, not a new force.
3. **Precession test:** Track screw-axis direction under sequences of proper isometries; compare angular drift with rigid-body precession models. Beware axis sign identification a~-a.
4. **Transport test:** Measure mean squared displacement vs number of steps for *specified* word-selection distributions. Do not infer diffusion from counting all reduced words.
5. **Astrophysics test:** Compare dimensionless geometric ratios (pitch/radius, angular drift per step) with models of orbital resonances or magnetized plasma structures. Never fit arbitrary physical units to force a match.
6. **Robustness:** Repeat for symmetric (u=v=0), near-symmetric, and generic sheared prisms; vary depth, floating-point precision, axis thresholds, and choice of word sampling.

## Disconfirmation criteria

- If a supposed vortex disappears when changing word order or selection rule, it is not an intrinsic invariant of the geometry.
- If a pattern depends strongly on rounding or axis cutoffs, it may be a numerical artifact.
- If no consistent time evolution or physical equations reproduce the motion, describe it as geometric resemblance only.
- If the model cannot predict independently measured quantities without fitted free parameters, no physical explanatory claim is warranted.

## Existing related notes and scripts

- docs/rhombic_prism_center_orbit_and_rotational_coupling.md
- docs/rhombic_prism_axis_geometry_research_program.md
- experiments/rhombic_prism_center_orbit_geometry.py
- experiments/rhombic_prism_axis_geometry_limit_audit.py

Next: implement numerical commutator and helix diagnostics, and validate in CI.
