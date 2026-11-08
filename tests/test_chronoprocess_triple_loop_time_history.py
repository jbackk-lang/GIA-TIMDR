import numpy as np

from experiments.chronoprocess_triple_loop_time_history import run_probe


def test_shared_time_history_leaves_phase_memory_after_frequency_returns():
    result = run_probe()
    for case in result["cases"].values():
        assert case["three_loop_coherence_mean"]["before"] > 0.999
        if case["disturbed_loop_indices_1_based"] == [1, 2, 3]:
            # A common-mode time shift moves all three phases together:
            # relative coherence survives even though absolute phase moved.
            assert case["three_loop_coherence_mean"]["after"] > 0.999
        else:
            assert case["three_loop_coherence_mean"]["after"] < 0.999
            assert case["phase_relation_rms_rad"]["after"] > 0.1


def test_more_disturbed_loop_clocks_change_whole_state_coherence():
    result = run_probe()
    one = result["cases"]["one_loop"]["three_loop_coherence_mean"]["after"]
    two = result["cases"]["two_loops"]["three_loop_coherence_mean"]["after"]
    all_three = result["cases"]["all_three_loops"]["three_loop_coherence_mean"]["after"]
    assert np.isfinite([one, two, all_three]).all()
    assert np.isclose(one, two)
    assert all_three > 0.999
    one_phase = result["cases"]["one_loop"]["final_relative_phase_rad"]
    two_phase = result["cases"]["two_loops"]["final_relative_phase_rad"]
    assert not np.allclose(one_phase, two_phase)


def test_probe_does_not_claim_recovery():
    assert run_probe()["status"] == "chronoprocess_time_history_probe_not_self_repair"
