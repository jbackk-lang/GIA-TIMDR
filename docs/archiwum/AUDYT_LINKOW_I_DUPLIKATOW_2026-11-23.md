# Audyt odnośników i identycznych plików — 2026-11-23

## Zakres

Kontrola została wykonana na drzewie gałęzi `main` repozytorium GIA-TIMDR z 2026-11-23, przed dodaniem tego raportu do katalogu. Objęła sześć istniejących wówczas plików Markdown w `docs/archiwum/` (indeks, pięć plików z wejściowego CSV oraz raport inwentaryzacji) oraz wszystkie obiekty typu blob widoczne w rekurencyjnym drzewie repozytorium (1 120 plików). Po zapisaniu niniejszego raportu katalog zawiera siedem plików. Liczby 6 i 94 opisują więc zakres historycznego przebiegu kontroli, a nie liczbę dokumentów po utworzeniu raportu.

## Odnośniki w archiwum

Sprawdzono 94 względne odnośniki Markdown w sześciu dokumentach archiwum. Każdy cel wskazuje istniejący plik albo katalog w repozytorium.

- Odnośniki sprawdzone: **94**
- Cele istniejące: **94**
- Potwierdzone uszkodzone odnośniki: **0**

Kontrola obejmuje cele względne zapisane jako zwykłe odnośniki Markdown. Nie obejmuje poprawności zewnętrznych serwisów HTTP(S), kotwic wewnątrz dokumentów ani renderowania wszystkich formatów przez GitHub.

## Identyczne pliki w całym repozytorium

Porównanie identyfikatorów Git blob wykazało **6 grup identycznej zawartości**. Identyczny blob oznacza identyczne bajty pliku; samo powtórzenie nie dowodzi jednak, że kopie są zbędne.

| Grupa | Liczba ścieżek | Ścieżki |
|---|---:|---|
| Licencje | 4 | `LICENSE`, `TIMDR-Geometry-Formalism/LICENSE.txt`, `TIMDR-Math-Formalism/LICENSE`, `TIMDR-Modal-Formalism/LICENSE.txt` |
| Pliki ignorowania Git | 4 | `TIMDR-Geometry-Formalism/.gitignore`, `TIMDR-Math-Formalism/.gitignore`, `TIMDR-Modal-Formalism/.gitignore`, `TIMDR-Time-Formalism/.gitignore` |
| Zależności | 2 | `TIMDR-Geometry-Formalism/requirements.txt`, `TIMDR-Modal-Formalism/requirements.txt` |
| Puste pliki | 2 | `docs/research/info_geometry/selective_clock_distractors.py`, `filters/__init__.py` |
| Launchery kompatybilności eksperymentów | 52 | `experiments/bc_opposite_chirality_pair.py`, `experiments/bc_opposite_direction_pair.py`, `experiments/chronoprocess_coupled_phase_recovery.py`, `experiments/chronoprocess_triple_loop_duration_sweep.py`, `experiments/chronoprocess_triple_loop_time_history.py`, `experiments/pentachoron_facet_reflections.py`, `experiments/phase_recovery_probe.py`, `experiments/reflection_branch_tree.py`, `experiments/reflection_transition_bc_bridge.py`, `experiments/reflection_word_family.py`, `experiments/rhombic_prism_angle_spectrum_grid.py`, `experiments/rhombic_prism_angle_spectrum_parameter_sweep.py`, `experiments/rhombic_prism_angular_spectrum_depth_convergence.py`, `experiments/rhombic_prism_angular_spectrum_symmetry_check.py`, `experiments/rhombic_prism_axis_conditioning_sensitivity.py`, `experiments/rhombic_prism_axis_geometry_limit_audit.py`, `experiments/rhombic_prism_axis_limit_study.py`, `experiments/rhombic_prism_center_commutator.py`, `experiments/rhombic_prism_center_orbit_geometry.py`, `experiments/rhombic_prism_central_screw_unfolding.py`, `experiments/rhombic_prism_d3_degeneracy_diagnostic.py`, `experiments/rhombic_prism_ellipse_braid_relation.py`, `experiments/rhombic_prism_exceptional_affine_relations.py`, `experiments/rhombic_prism_helix_commutator_audit.py`, `experiments/rhombic_prism_locus_intersections.py`, `experiments/rhombic_prism_mobility_domain.py`, `experiments/rhombic_prism_mobility_screw_coupling.py`, `experiments/rhombic_prism_screw_axis_spatial_organization.py`, `experiments/rhombic_prism_screw_unfolding_multidegree.py`, `experiments/rhombic_prism_triangle_certified_disk.py`, `experiments/rhombic_prism_triangle_d3_equivariance.py`, `experiments/rhombic_prism_triangle_exact_cosine.py`, `experiments/rhombic_prism_triangle_exact_order_trace.py`, `experiments/rhombic_prism_triangle_exact_symmetry.py`, `experiments/rhombic_prism_triangle_groebner_roots.py`, `experiments/rhombic_prism_triangle_nine_exact_certificate.py`, `experiments/rhombic_prism_triangle_nine_shapes.py`, `experiments/rhombic_prism_triangle_nine_spectral_orbits.py`, `experiments/rhombic_prism_triangle_nine_spectrum.py`, `experiments/rhombic_prism_triangle_nine_symbolic_spectrum.py`, `experiments/rhombic_prism_triangle_nine_trace_moments.py`, `experiments/rhombic_prism_triangle_order_anomaly.py`, `experiments/rhombic_prism_triangle_polynomial_system.py`, `experiments/rhombic_prism_triangle_reduced_equations.py`, `experiments/rhombic_prism_triangle_reflection_symmetry.py`, `experiments/rhombic_prism_triangle_six_orders.py`, `experiments/rhombic_prism_triangle_spectral_separation.py`, `experiments/rhombic_triangular_prism_two_angles.py`, `experiments/triangular_prism_reflections.py`, `experiments/triple_loop_coupled_perturbation.py`, `experiments/triple_loop_transition_probe.py`, `experiments/truncated_tetrahedron_reflections.py` |
| README eksperymentów | 3 | `experiments/chronoprocess/README.md`, `experiments/reflections/README.md`, `experiments/rhombic_prism/README.md` |

## Decyzje

1. **Nie usunięto żadnego pliku.** Kopie licencji i `.gitignore` mogą być potrzebne w niezależnych podprojektach.
2. Powtarzające się `requirements.txt` pozostają lokalne dla podprojektów do czasu potwierdzenia, że ich cykle instalacji są wspólne.
3. 52 identyczne pliki w `experiments/` są launcherami kompatybilności: wybierają katalog tematyczny i uruchamiają właściwy moduł przez `runpy`. To świadomy mechanizm zgodności ścieżek, nie puste placeholdery; należy je zachować.
4. Dwa pozostałe identyczne pliki (`docs/research/info_geometry/selective_clock_distractors.py` i `filters/__init__.py`) są puste. Przed ewentualnym usunięciem trzeba sprawdzić historię Git i odwołania/importy.
5. Powtarzające się README mogą pełnić rolę lokalnych stron wejściowych; pozostają bez zmian.
6. Raport nie zmienia treści historycznych wyników, prerejestracji ani kodu eksperymentów.

## Ograniczenia

Drzewo Git obejmuje 1 200 wpisów, w tym 1 120 blobów. Audyt duplikatów porównuje identyczność bajtową, nie podobieństwo semantyczne. Nie rozstrzyga, czy różne wersje dokumentów opisują ten sam temat. Przenosiny lub kasowanie wymagają osobnej kontroli zależności i historii.
