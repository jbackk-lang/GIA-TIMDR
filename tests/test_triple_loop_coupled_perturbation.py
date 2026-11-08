import numpy as np

from experiments.triple_loop_coupled_perturbation import (
    operator_j, run_case, spectral_radius,
)


def test_original_operator_has_no_contracting_lambda_sampled():
    for lam in (-1.0, -0.2, 0.0, 0.2, 1.0):
        assert spectral_radius(lam) >= 1.0 - 1e-12


def test_linear_operator_does_not_erase_perturbation_selectively():
    result = run_case(0.0, (0,), steps=8, stabilize=False)
    assert result["final_distance_from_unperturbed_trajectory"] > 0


def test_normalization_does_not_restore_original_state():
    raw = run_case(0.5, (0,), steps=8, stabilize=False)
    normalized = run_case(0.5, (0,), steps=8, stabilize=True)
    assert normalized["final_distance_from_unperturbed_trajectory"] > 0
    assert raw["initial_perturbation_norm"] == normalized["initial_perturbation_norm"]


def test_same_operator_acts_on_all_three_channels_as_one_state():
    lam = 0.4
    j = operator_j(lam)
    state = np.array([1.0, 0.7, -0.35])
    assert np.allclose(j @ state, np.array([0.7 + 0.35 * lam,
                                             1.0 * -lam - 0.35,
                                             1.0 - 0.7 * lam]))
