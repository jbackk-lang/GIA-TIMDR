import numpy as np

from experiments.chronoprocess_triple_loop_time_history import run_probe


def test_shared_time_history_leaves_phase_memory_after_frequency_returns():
    result = run_probe()
    for case in result["cases"].values():
        assert case["three_loop_coherence_mean"]["before"] > 0.999
        assert case["three_loop_coherence_mean"]["after"] < 0.999
        assert case["phase_relation_rms_rad"]["after"] > 0.1


def test_more_disturbed_loop_clocks_change_whole_state_coherence():
    result = run_probe()
    one = result["cases"]["one_loop"]["three_loop_coherence_mean"]["after"]
    two = result["cases"]["two_loops"]["three_loop_coherence_mean"]["after"]
    all_three = result["cases"]["all_three_loops"]["three_loop_coherence_mean"]["after"]
    assert np.isfinite([one, two, all_three]).all()
    assert not np.isclose(one, two)
    assert not np.isclose(two, all_three)


def test_probe_does_not_claim_recovery():
    assert run_probe()["status"] == "chronoprocess_time_history_probe_not_self_repair"
