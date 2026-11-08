import numpy as np
import pytest

from experiments.chronoprocess_coupled_phase_recovery import simulate


def test_uncoupled_differential_disturbance_does_not_recover():
    result = simulate(0.0, (0,), total_duration=8.0, sample_rate=250.0)
    assert result["post_disturbance_mean_order_parameter"] < 0.95
    assert result["time_to_order_parameter_0_99_seconds"] is None


def test_positive_coupling_recovers_relative_phase_after_one_loop_detuning():
    result = simulate(1.6, (0,), total_duration=8.0, sample_rate=250.0)
    assert result["post_disturbance_mean_order_parameter"] > 0.99
    assert result["time_to_order_parameter_0_99_seconds"] is not None


def test_common_mode_detuning_preserves_relative_coherence_without_repair():
    result = simulate(0.0, (0, 1, 2), total_duration=8.0, sample_rate=250.0)
    assert result["post_disturbance_mean_order_parameter"] > 0.999999
    assert result["post_disturbance_mean_abs_relative_phase_rad"] < 1e-10


def test_stronger_coupling_shortens_recovery_time():
    weak = simulate(0.8, (0,), total_duration=10.0, sample_rate=250.0)
    strong = simulate(1.6, (0,), total_duration=10.0, sample_rate=250.0)
    assert weak["time_to_order_parameter_0_99_seconds"] is not None
    assert strong["time_to_order_parameter_0_99_seconds"] is not None
    assert strong["time_to_order_parameter_0_99_seconds"] < weak["time_to_order_parameter_0_99_seconds"]


def test_invalid_coupling_rejected():
    with pytest.raises(ValueError):
        simulate(-0.1, (0,))
