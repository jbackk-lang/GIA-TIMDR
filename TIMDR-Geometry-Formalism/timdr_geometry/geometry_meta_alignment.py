"""Strict geometry -> META time-alignment adapter for TIMDR B2.

This module defines the missing pipeline layer between the existing geometric
Weingarten operator and the META window partition. It does not alter either
operator and does not interpolate or otherwise reshape data after the fact.

Pipeline:
    ordered mesh snapshots + timestamps
        -> one mean-curvature summary H(t_i) per snapshot
        -> exact timestamp/grid validation against META time samples
        -> exact disjoint block partition supplied by META window_size
        -> Lambda_G per the same block slices as Lambda_META,disp

This is an adapter specification, not empirical validation of the bridge.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np

from .weingarten import Mesh, mean_curvature, mean_curvature_dispersion_blocks
from .weingarten import discrete_shape_operator, vertex_normals, one_ring


def mesh_snapshot_to_mean_curvature(mesh: Mesh) -> float:
    """Return one scalar H for one mesh snapshot.

    The scalar is the arithmetic mean of vertex mean-curvature values over all
    vertices for which the discrete shape operator is defined (>=2 useful,
    non-degenerate tangent-neighbour rows).

    No interpolation, smoothing, clipping, or weighting is introduced here.
    Invalid vertices are skipped only when the existing Weingarten operator
    explicitly rejects them; if no valid vertex remains, the snapshot is
    invalid rather than silently mapped to zero.
    """
    normals = vertex_normals(mesh)
    rings = one_ring(mesh)
    H_values: list[float] = []

    for point_idx in range(mesh.n_vertices):
        try:
            op = discrete_shape_operator(mesh, normals, point_idx, rings=rings)
        except ValueError:
            continue
        H_values.append(mean_curvature(op))

    if not H_values:
        raise ValueError("snapshot geometrii nie ma ani jednego poprawnie wyznaczalnego H")

    return float(np.mean(np.asarray(H_values, dtype=float)))


def surface_to_time_h_trace(
    vertex_times: np.ndarray,
    vertex_h_values: np.ndarray,
    time_grid: np.ndarray,
) -> np.ndarray:
    """Reduce vertex-wise H(t_i, s_j) to one H_i per explicit time t_i.

    ``vertex_times[j]`` is the actual timestamp attached to vertex/value
    ``vertex_h_values[j]``. The reduction never infers time from vertex index
    ordering and never interpolates between timestamps. For each requested
    ``time_grid[i]`` it takes the arithmetic mean of all finite H values whose
    explicit timestamp equals that grid value. A time with no valid H values
    is invalid and raises ``ValueError`` rather than becoming zero.

    This function is the explicit H(t_i, s_j) -> H_i layer required by B2.
    The caller is responsible for constructing ``vertex_times`` from the
    actual geometry/time association (for example from Gamma(T, s)); this
    adapter does not assume any particular vertex-index layout.
    """
    vertex_times = np.asarray(vertex_times, dtype=float)
    vertex_h_values = np.asarray(vertex_h_values, dtype=float)
    time_grid = np.asarray(time_grid, dtype=float)

    if vertex_times.ndim != 1 or vertex_h_values.ndim != 1:
        raise ValueError("vertex_times i vertex_h_values muszą być 1D")
    if vertex_times.size != vertex_h_values.size:
        raise ValueError("vertex_times i vertex_h_values muszą mieć tę samą długość")
    if time_grid.ndim != 1 or time_grid.size == 0:
        raise ValueError("time_grid musi być niepustą tablicą 1D")
    if not np.all(np.isfinite(vertex_times)) or not np.all(np.isfinite(time_grid)):
        raise ValueError("czasy zawierają NaN/inf")
    if np.any(np.diff(time_grid) <= 0):
        raise ValueError("time_grid musi być ściśle rosnąca")

    h_trace = np.empty(time_grid.size, dtype=float)
    for i, t_i in enumerate(time_grid):
        mask = np.isclose(vertex_times, t_i, rtol=0.0, atol=0.0)
        h_i = vertex_h_values[mask]
        valid = h_i[np.isfinite(h_i)]
        if valid.size == 0:
            raise ValueError(
                f"brak poprawnych H dla czasu t={t_i}; wynik jest invalid, nie zero"
            )
        h_trace[i] = float(np.mean(valid))

    return h_trace


def geometry_snapshots_to_h_trace(
    geometry_times: np.ndarray,
    meshes: Sequence[Mesh],
) -> np.ndarray:
    """Build H_trace with exactly one H sample per ordered mesh timestamp."""
    geometry_times = np.asarray(geometry_times, dtype=float)
    if geometry_times.ndim != 1:
        raise ValueError("geometry_times musi mieć kształt 1D")
    if len(geometry_times) != len(meshes):
        raise ValueError("geometry_times i meshes muszą mieć tę samą długość")
    if len(geometry_times) == 0:
        raise ValueError("brak snapshotów geometrii")
    if not np.all(np.isfinite(geometry_times)):
        raise ValueError("geometry_times zawiera NaN/inf")
    if len(geometry_times) >= 2 and not np.all(np.diff(geometry_times) > 0):
        raise ValueError("geometry_times muszą być ściśle rosnące")

    return np.asarray([mesh_snapshot_to_mean_curvature(m) for m in meshes], dtype=float)


def assert_exact_meta_time_grid(
    geometry_times: np.ndarray,
    meta_times: np.ndarray,
) -> None:
    """Require geometry and META samples to share the exact time grid.

    No nearest-neighbour matching and no interpolation is allowed in this
    adapter. The caller must construct the two traces on the same sample grid.
    """
    geometry_times = np.asarray(geometry_times, dtype=float)
    meta_times = np.asarray(meta_times, dtype=float)
    if geometry_times.shape != meta_times.shape:
        raise ValueError(
            "geometria i META nie mają tego samego kształtu czasu; "
            "bez jawnej, prerejestrowanej transformacji nie wolno ich wyrównywać"
        )
    if not np.all(np.isfinite(geometry_times)) or not np.all(np.isfinite(meta_times)):
        raise ValueError("siatka czasu zawiera NaN/inf")
    if not np.array_equal(geometry_times, meta_times):
        raise ValueError(
            "geometry_times != meta_times; B2 wymaga identycznej osi czasu, "
            "bez interpolacji ani nearest-neighbour"
        )


def geometry_lambda_on_meta_blocks(
    geometry_times: np.ndarray,
    meshes: Sequence[Mesh],
    meta_times: np.ndarray,
    window_size: int,
    eps: float,
) -> tuple[np.ndarray, list[tuple[int, int]]]:
    """Compute Lambda_G on the exact disjoint META blocks.

    The only allowed path is:
        meshes -> H_trace -> exact time-grid check -> META block slices
        -> mean_curvature_dispersion_blocks.
    """
    geometry_times = np.asarray(geometry_times, dtype=float)
    meta_times = np.asarray(meta_times, dtype=float)
    assert_exact_meta_time_grid(geometry_times, meta_times)
    if window_size <= 0:
        raise ValueError("window_size musi być > 0")

    H_trace = geometry_snapshots_to_h_trace(geometry_times, meshes)
    block_slices = [
        (start, min(start + window_size, len(H_trace)))
        for start in range(0, len(H_trace), window_size)
    ]
    lambda_g = mean_curvature_dispersion_blocks(H_trace, block_slices, eps=eps)
    return lambda_g, block_slices
