import numpy as np
import pytest

from timdr_geometry.weingarten import (
    EPS_GEOMETRY,
    mean_curvature_dispersion,
    mean_curvature_dispersion_blocks,
)


def test_constant_h_is_zero_dispersion():
    assert mean_curvature_dispersion(np.array([2.0, 2.0, 2.0])) == 0.0


def test_formula_matches_np_std_and_mean():
    h = np.array([-1.0, 0.0, 1.0, 2.0])
    s = np.std(h)
    m = abs(np.mean(h))
    expected = s / (s + m + EPS_GEOMETRY)
    assert mean_curvature_dispersion(h) == pytest.approx(expected)


def test_nan_is_not_silently_filtered():
    result = mean_curvature_dispersion(np.array([1.0, np.nan, 2.0]))
    assert np.isnan(result)


def test_empty_input_is_explicitly_invalid():
    with pytest.raises(ValueError):
        mean_curvature_dispersion(np.array([]))


def test_eps_must_be_positive_and_finite():
    with pytest.raises(ValueError):
        mean_curvature_dispersion(np.array([1.0, 2.0]), eps=0.0)
    with pytest.raises(ValueError):
        mean_curvature_dispersion(np.array([1.0, 2.0]), eps=np.nan)


def test_same_supplied_blocks_are_used_without_repartitioning():
    h = np.array([1.0, 1.0, 2.0, 2.0, 3.0])
    blocks = [(0, 2), (2, 5)]
    result = mean_curvature_dispersion_blocks(h, blocks)
    expected = np.array([
        mean_curvature_dispersion(h[0:2]),
        mean_curvature_dispersion(h[2:5]),
    ])
    assert np.allclose(result, expected, equal_nan=True)


def test_invalid_block_bounds_are_rejected():
    with pytest.raises(ValueError):
        mean_curvature_dispersion_blocks(np.array([1.0, 2.0]), [(0, 3)])
