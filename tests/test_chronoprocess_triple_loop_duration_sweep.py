from experiments.chronoprocess_triple_loop_duration_sweep import run_sweep, simulate


def test_stronger_coupling_improves_recovery_for_matched_single_loop_pulse():
    weak = simulate(0.2, 1.0, disturbance="one")
    strong = simulate(0.8, 1.0, disturbance="one")
    assert strong["coherence_at_end"] > weak["coherence_at_end"]
    assert strong["relative_phase_rms_at_end_rad"] < weak["relative_phase_rms_at_end_rad"]


def test_common_mode_disturbance_preserves_relative_coherence_without_repair():
    result = simulate(0.0, 2.0, disturbance="all")
    assert result["coherence_min_during_pulse"] > 0.999999
    assert result["relative_phase_rms_at_end_rad"] < 1e-10


def test_no_coupling_does_not_recover_long_single_loop_pulse():
    result = simulate(0.0, 2.0, disturbance="one")
    assert result["status"] == "not_recovered_within_horizon"


def test_duration_sweep_covers_whole_three_loop_cases():
    rows = run_sweep()
    assert len(rows) == 90
    assert {r["disturbance"] for r in rows} == {"one", "two", "all"}
