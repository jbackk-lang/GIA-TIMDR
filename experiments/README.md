# Indeks eksperymentów GIA-TIMDR

Ten katalog jest indeksem eksperymentów pogrupowanych według obszaru badawczego. Nie zmienia lokalizacji istniejących skryptów ani ich importów — dzięki temu sam indeks nie narusza ścieżek używanych przez workflow, testy i dokumentację. Serie zgrupowane katalogowo pozostają w swoich dotychczasowych miejscach.

## Serie uporządkowane katalogowo

| Obszar | Lokalizacja | Zakres |
|---|---|---|
| 54A | [54A/](54A/README.md) | eksperymenty 54A: kod, raporty i wyniki |
| Charakterystyka helis | [helix_characterization/](helix_characterization/) | geometria helis, rurki i testy |
| Redukcja helis | [helix_reduction/](helix_reduction/) | redukcje powierzchni, audyty płatów i testy |
| Odpowiedź sygnałowa helisy | [helix_signal_response/](helix_signal_response/) | minimalne sprzężenie i testy |
| Historia fazy MAGE | [mage_temporal_phase_history/](mage_temporal_phase_history/) | testy historii fazowej |
| Redukcja jądrowa | [nuclear_reduction/NRG-01/](nuclear_reduction/NRG-01/README.md) | NRG-01: źródła, audyty i testy |
| Zachowanie pola fazowego | [phase_field_preservation/](phase_field_preservation/) | model zachowania pola fazowego i test |
 
## Eksperymenty w katalogu głównym

Poniższe skrypty pozostają na dotychczasowych ścieżkach do czasu sprawdzenia wszystkich odwołań w workflow, testach i dokumentacji.

### Chronoproces i pętle sprzężone
- `chronoprocess_coupled_phase_recovery.py`
- `chronoprocess_triple_loop_duration_sweep.py`
- `chronoprocess_triple_loop_time_history.py`
- `triple_loop_coupled_perturbation.py`
- `triple_loop_transition_probe.py`
- `phase_recovery_probe.py`

### Rhombic prism — geometria, osie i widma
- `rhombic_prism_angle_spectrum_grid.py`
- `rhombic_prism_angle_spectrum_parameter_sweep.py`
- `rhombic_prism_angular_spectrum_depth_convergence.py`
- `rhombic_prism_angular_spectrum_symmetry_check.py`
- `rhombic_prism_axis_conditioning_sensitivity.py`
- `rhombic_prism_axis_geometry_limit_audit.py`
- `rhombic_prism_axis_limit_study.py`
- `rhombic_prism_center_commutator.py`
- `rhombic_prism_center_orbit_geometry.py`
- `rhombic_prism_central_screw_unfolding.py`
- `rhombic_prism_d3_degeneracy_diagnostic.py`
- `rhombic_prism_ellipse_braid_relation.py`
- `rhombic_prism_exceptional_affine_relations.py`
- `rhombic_prism_helix_commutator_audit.py`
- `rhombic_prism_locus_intersections.py`
- `rhombic_prism_mobility_domain.py`
- `rhombic_prism_mobility_screw_coupling.py`
- `rhombic_prism_screw_axis_spatial_organization.py`
- `rhombic_prism_screw_unfolding_multidegree.py`
- pozostałe `rhombic_prism_triangle_*.py` — certyfikaty, symetrie, widma i układy wielomianowe

### Odbicia i geometrie wielościenne
- `bc_opposite_chirality_pair.py`
- `bc_opposite_direction_pair.py`
- `pentachoron_facet_reflections.py`
- `reflection_branch_tree.py`
- `reflection_transition_bc_bridge.py`
- `reflection_word_family.py`
- `rhombic_triangular_prism_two_angles.py`
- `triangular_prism_reflections.py`
- `truncated_tetrahedron_reflections.py`

## Zasada dalszego porządkowania

Przenoszenie plików z katalogu głównego do podkatalogów tematycznych należy wykonać dopiero po audycie odwołań tekstowych i automatyzacji CI. Przy przenosinach trzeba równolegle aktualizować workflow, instrukcje uruchamiania, importy i linki w dokumentacji. Nie należy przenosić kodu rdzenia (`core/`), aplikacji (`applications/`) ani testów integracyjnych (`tests/`) do archiwum eksperymentów.
