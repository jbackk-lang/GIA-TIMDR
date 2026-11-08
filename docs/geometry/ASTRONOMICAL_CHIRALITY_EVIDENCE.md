# Astronomical handedness: observational check (2026-11-08)

## Claim under examination
"Cosmic helices are usually left-handed when followed outward from their center."

## Findings
**Not supported as a universal statement.** Chirality is defined only after specifying the object, oriented axis, observation direction and physical handedness observable. Projected clockwise/counterclockwise spiral arms are not interchangeable with 3D torsion or magnetic helicity.

1. **Solar magnetic structures:** Northern solar hemisphere preferentially exhibits negative/left-handed magnetic helicity; southern hemisphere preferentially positive/right-handed. This is a statistical hemispheric rule, not an absolute one. A sample of 571 erupting solar filaments found 94.8% negative helicity in the northern hemisphere and 87.4% positive in the southern hemisphere. Source: https://doi.org/10.3847/1538-4357/835/1/94
2. **Spiral galaxies:** Galaxy Zoo analysis of about 37,000 spiral galaxies, after bias correction, found winding-sense distribution consistent with statistical isotropy and no significant preferred global handedness. Source: https://doi.org/10.1111/j.1365-2966.2008.13490.x
3. **Observational and semantic trap:** Galaxy arm winding measured outward from center and apparent rotation on the sky are different conventions; the apparent clockwise direction reverses with viewpoint. Source: https://academic.oup.com/mnras/article/388/4/1686/981637
4. **Helicity is not necessarily geometrical torsion:** Solar magnetic helicity sign and the Frenet torsion of a 3D space curve require different definitions and data.

## TSI consequences and falsifiable protocol
Do not set a universal `left-handed` prior based on astronomy. Model handedness priors as conditional on physical context, hemisphere, axis orientation and measurement type. Test mirror-equivariant inference with both signs; include hemisphere-dependent synthetic priors as an optional *hypothesis* and compare against balanced priors on out-of-distribution controls. Do not use solar hemispheric statistics to claim properties of galaxies or an engineered TSI core.

## Repo research state
Helix-Lock phase-history inference CI https://github.com/jbackk-lang/Helix-Lock/actions/runs/42506276081 passed 183 tests on Python 3.11 and 3.12; these are synthetic tests, not astronomical validation.
