import numpy as np
import pytest

from experiments.triple_loop_transition_probe import (
    I3, MINUS_I3, P, apply_full_loop, run_probe,
)


def test_full_three_loop_cycle_closes_as_P_cubed_identity():
    assert np.allclose(np.linalg.matrix_power(P, 3), I3)


def test_disturbance_to_one_loop_is_not_erased_by_cycle_closure():
    initial = np.array([1.0 + 0j, 0.7 * np.exp(0.4j), 0.45 * np.exp(-0.8j)])
    disturbed = initial.copy()
    disturbed[0] *= 0.25 * np.exp(1.1j)
    returned = np.linalg.matrix_power(P, 3) @ disturbed
    assert np.allclose(returned, disturbed)
    assert not np.allclose(returned, initial)


def test_one_two_and_three_full_loops_are_not_conflated():
    state = np.array([1.0 + 0j, 0.7 + 0.2j, 0.4 - 0.1j])
    after_one = np.linalg.matrix_power(P, 1) @ state
    after_two = np.linalg.matrix_power(P, 2) @ state
    after_three = np.linalg.matrix_power(P, 3) @ state
    assert not np.allclose(after_one, state)
    assert not np.allclose(after_two, state)
    assert np.allclose(after_three, state)


def test_global_inversion_has_two_loop_period_not_three():
    state = np.array([1.0 + 0j, 0.7 + 0.2j, 0.4 - 0.1j])
    assert np.allclose(np.linalg.matrix_power(MINUS_I3, 2) @ state, state)
    assert not np.allclose(MINUS_I3 @ state, state)


def test_invalid_state_shape_rejected():
    with pytest.raises(ValueError):
        apply_full_loop(np.array([1.0, 2.0]), P)


def test_probe_labels_its_scope_honestly():
    result = run_probe()
    assert result["status"] == "algebraic_triple_loop_probe_not_self_repair_validation"
    assert result["P_cubed_identity_error"] < 1e-12
    assert result["residual_disturbance_after_three_full_loops"] > 0
