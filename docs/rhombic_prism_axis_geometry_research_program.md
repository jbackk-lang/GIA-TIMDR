# Axis geometry research program — claims, proofs, tests, and open questions

Date: 2026-11-13. This consolidates the earlier discussion into a falsifiable research program. A mathematical result is not presented as a new physical effect.

## Four tasks

1. **Limit of rotation and screw axes.** For all even reduced reflection words up to depth n, construct the cumulative set of proper-isometry axes. Use unoriented Pluecker lines L=(a,m), ||a||=1, a·m=0, and identify L~-L. Compare cumulative finite sets using sign-invariant distances, and separately test boundedness of moment norms. Finite-depth stabilization is not proof of infinite-depth Hausdorff convergence.
2. **Invariants.** Verify ||a||=1, a·m=0, orthogonality of each linear part, det(R)=±1, and the rigid-displacement center identity ||g(O)-O||²=4ρ²sin²(θ/2)+h² for proper screw motions. These are classical identities, not newly discovered invariants of the prism family. Seek additional parameter-dependent relations and test them separately.
3. **Numerical artifacts.** Vary matrix deduplication precision (currently 10 or 12 decimals), axis-line deduplication precision (currently 7 decimals), small-angle cutoffs (0.5,1,2,5 degrees), and depth. Test sign discontinuities in canonical axis representatives, residuals of axis equations, and conditioning near the identity. Distinguish distinct reduced words, distinct affine maps, and distinct geometric axes.
4. **Theorem or equation for a limit.** First prove or disprove boundedness; then choose an appropriate compactification and derive a functional characterization that predicts independently computed geometric features. Defining an accumulation set as the zero set of a distance-to-tail function is legitimate but does not constitute a new closed analytic formula.

## Proven facts for the implemented reflection model

Let t=(u,v,w), w=sqrt(1-u²-v²)>0, and O=((1+u)/2,sqrt(3)/6+v/2,w/2).

- The reflections in z=0 and z=w generate T(x)=x+2we_z. Thus the group is infinite and the orbit of O contains O+2nw e_z for all integers n. It is unbounded.
- Compose reflection in z=0 with reflection in a side-face plane. The two planes intersect in a horizontal base-edge line, giving a nontrivial rotation about that line. Conjugating by T^n translates its axis vertically by 2nw. If a is its horizontal unit direction, its Pluecker moment is m_n=m_0+2nw(e_z×a), so ||m_n||→∞ as |n|→∞. Therefore the full axis set is unbounded in the usual affine Pluecker chart.
- For n→+∞, m_n/||m_n||→e_z×a; for n→-∞, the opposite limit holds. This is a limiting direction of one explicit family, not the entire limit set.
- An affine orthogonal isometry g(x)=Rx+b acts on Pluecker coordinates by a'=Ra and m'=det(R)Rm+b×Ra.
- For a proper screw displacement, the transverse squared displacement of O is W=4ρ²sin²(θ/2). The axial displacement h is orthogonal to the transverse part, giving ||g(O)-O||²=W+h².

## A correction to earlier discussion

The triangular prism is generally not centrally symmetric. O is its centroid for a homogeneous prism, not a center of inversion symmetry. The central line joining the base centroids is not necessarily an axis of rotational symmetry for a sheared prism. Also, discrete reflection words do not determine time, angular velocity, force, or centrifugal acceleration.

## Hypotheses and experimental priorities

- The high-symmetry configuration (u,v)=(0,0) may have much slower growth in distinct center positions than generic sheared configurations. Test at increasing depths and multiple deduplication tolerances.
- Search for robust features in center displacement, screw pitch, axis distance ρ, and angular spectrum that survive cutoff and precision changes.
- Compare the center orbit with the orbit of the base median and with the family of extracted screw axes; these are different geometric objects.
- Investigate compactified asymptotic directions for center positions and Pluecker moments, not an ordinary compact Hausdorff limit of unbounded sets.
- If proposing a zeta-like zero equation, specify the analytic function/operator, convergence domain, and why its zeros coincide with the desired geometry. This remains open.

## Relevant scripts

- experiments/rhombic_prism_axis_geometry_limit_audit.py
- experiments/rhombic_prism_axis_limit_study.py
- experiments/rhombic_prism_mobility_screw_coupling.py
- experiments/rhombic_prism_center_orbit_geometry.py

The first two already audit finite-depth Pluecker-axis sets. The center-orbit script is newly added and has not yet been independently validated by CI.
