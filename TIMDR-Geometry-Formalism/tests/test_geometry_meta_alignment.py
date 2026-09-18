import numpy as np
import pytest

from timdr_geometry.geometry_meta_alignment import (
    surface_to_time_h_trace,
    assert_exact_meta_time_grid,
    geometry_lambda_on_meta_blocks,
)
from timdr_geometry.weingarten import make_plane_mesh


def test_exact_time_grid_accepts_identical_grid():
    t = np.array([0.0, 1.0, 2.0])
    assert_exact_meta_time_grid(t, t.copy())


def test_exact_time_grid_rejects_different_grid():
    t_g = np.array([0.0, 1.0, 2.0])
    t_m = np.array([0.0, 1.0, 2.1])
    with pytest.raises(ValueError, match="geometry_times != meta_times"):
        assert_exact_meta_time_grid(t_g, t_m)


def test_exact_time_grid_rejects_different_length():
    t_g = np.array([0.0, 1.0])
    t_m = np.array([0.0, 1.0, 2.0])
    with pytest.raises(ValueError, match="tego samego kształtu"):
        assert_exact_meta_time_grid(t_g, t_m)


def test_lambda_g_uses_same_disjoint_blocks():
    meshes = [make_plane_mesh(n=5, size=1.0) for _ in range(5)]
    t = np.arange(5, dtype=float)
    values, blocks = geometry_lambda_on_meta_blocks(
        geometry_times=t,
        meshes=meshes,
        meta_times=t.copy(),
        window_size=2,
        eps=1e-9,
    )
    assert blocks == [(0, 2), (2, 4), (4, 5)]
    assert values.shape == (3,)
    assert np.allclose(values, 0.0)


def test_surface_to_time_h_trace_uses_explicit_vertex_times_not_indices():
    times = np.array([2.0, 0.0, 1.0, 0.0])
    h = np.array([20.0, 1.0, 10.0, 3.0])
    grid = np.array([0.0, 1.0, 2.0])
    result = surface_to_time_h_trace(times, h, grid)
    assert np.allclose(result, np.array([2.0, 10.0, 20.0]))


def test_surface_to_time_h_trace_is_permutation_invariant():
    times = np.array([2.0, 0.0, 1.0, 0.0])
    h = np.array([20.0, 1.0, 10.0, 3.0])
    grid = np.array([0.0, 1.0, 2.0])
    perm = np.array([3, 1, 0, 2])
    result_a = surface_to_time_h_trace(times, h, grid)
    result_b = surface_to_time_h_trace(times[perm], h[perm], grid)
    assert np.allclose(result_a, result_b)


def test_surface_to_time_h_trace_missing_time_is_invalid_not_zero():
    with pytest.raises(ValueError, match="invalid, nie zero"):
        surface_to_time_h_trace(
            np.array([0.0, 0.0, 2.0]),
            np.array([1.0, np.nan, 3.0]),
            np.array([0.0, 1.0, 2.0]),
        )


def test_surface_to_time_h_trace_rejects_length_mismatch():
    with pytest.raises(ValueError):
        surface_to_time_h_trace(
            np.array([0.0, 1.0]),
            np.array([1.0]),
            np.array([0.0, 1.0]),
        )
