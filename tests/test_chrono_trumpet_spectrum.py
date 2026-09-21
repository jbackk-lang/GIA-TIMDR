# tests/test_chrono_trumpet_spectrum.py
"""Testy jednostkowe dla core/chrono_trumpet_spectrum.py -- patrz
docs/geometry/PREREG_CHRONO_TRUMPET_SPECTRUM_v0.1.md. Sprawdzaja
WYLACZNIE poprawnosc konstrukcji (katy, promienie, wierzcholki,
triangulacja, wzor testu serii Walda-Wolfowitza na znanych
przykladach) -- NIE powtarzaja analizy realnych danych CWRU (ta jest
uruchamiana jako skrypt, wyniki w RESULT_..._v0.1.md).
"""
import os
import sys

import numpy as np
import pytest

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from core.chrono_trumpet_spectrum import (  # noqa: E402
    radii_from_eigs,
    trumpet_angles,
    build_trumpet_vertices,
    build_trumpet_faces,
    build_trumpet_mesh,
    compute_curvature_grid,
    wald_wolfowitz_runs_test,
    curvature_sign_test_per_i,
    spectrum_trace,
)


# ---------------------------------------------------------------------
# Katy i promienie
# ---------------------------------------------------------------------


def test_trumpet_angles_n3():
    angles = trumpet_angles(3)
    assert angles.shape == (3,)
    np.testing.assert_allclose(angles, [0.0, 2 * np.pi / 3, 4 * np.pi / 3])


def test_trumpet_angles_n2():
    angles = trumpet_angles(2)
    np.testing.assert_allclose(angles, [0.0, np.pi])


def test_radii_from_eigs_normalized_rows_sum_to_one():
    eig_matrix = np.array([[2.0, 0.0], [1.0, 1.0], [3.0, 1.0]])
    radii = radii_from_eigs(eig_matrix)
    row_sums = np.nansum(radii, axis=1)
    np.testing.assert_allclose(row_sums, [1.0, 1.0, 1.0])
    np.testing.assert_allclose(radii[0], [1.0, 0.0])
    np.testing.assert_allclose(radii[1], [0.5, 0.5])


def test_radii_from_eigs_degenerate_row_is_nan():
    eig_matrix = np.array([[0.0, 0.0], [1.0, 1.0]])
    radii = radii_from_eigs(eig_matrix)
    assert np.all(np.isnan(radii[0]))
    np.testing.assert_allclose(radii[1], [0.5, 0.5])


# ---------------------------------------------------------------------
# Wierzcholki i triangulacja
# ---------------------------------------------------------------------


def test_build_trumpet_vertices_known_values():
    radii = np.array([[1.0, 0.5], [0.5, 1.0]])   # T=2, N=2
    times = np.array([0.0, 1.0])
    angles = trumpet_angles(2)  # [0, pi]
    verts = build_trumpet_vertices(radii, times, angles)
    assert verts.shape == (4, 3)
    # t_idx=0, i_idx=0: r=1, theta=0 -> (1,0,0)
    np.testing.assert_allclose(verts[0], [1.0, 0.0, 0.0], atol=1e-10)
    # t_idx=0, i_idx=1: r=0.5, theta=pi -> (-0.5, ~0, 0)
    np.testing.assert_allclose(verts[1], [-0.5, 0.0, 0.0], atol=1e-10)
    # t_idx=1, i_idx=0: r=0.5, theta=0 -> (0.5,0,1)
    np.testing.assert_allclose(verts[2], [0.5, 0.0, 1.0], atol=1e-10)
    # t_idx=1, i_idx=1: r=1.0, theta=pi -> (-1,0,1)
    np.testing.assert_allclose(verts[3], [-1.0, 0.0, 1.0], atol=1e-10)


def test_build_trumpet_faces_count_and_wrap():
    n_t, n_channels = 3, 3
    faces = build_trumpet_faces(n_t, n_channels)
    assert faces.shape == (2 * (n_t - 1) * n_channels, 3)
    # ostatni "slice" po i=2 (n_channels-1) musi zawijac sie do i=0
    wraps = [f for f in faces if 2 in f[:1] or True]
    # sprawdz wprost, ze krawedz i=2 -> (i+1)%3=0 wystepuje (zawiniecie)
    found_wrap = any(
        (f[0] % n_channels == 2 and f[1] % n_channels == 0) for f in faces
    )
    assert found_wrap


def test_build_trumpet_mesh_shape():
    radii = np.tile([0.5, 0.3, 0.2], (5, 1))
    times = np.arange(5, dtype=float)
    angles = trumpet_angles(3)
    mesh = build_trumpet_mesh(radii, times, angles)
    assert mesh.vertices.shape == (15, 3)
    assert mesh.faces.shape == (2 * 4 * 3, 3)


# ---------------------------------------------------------------------
# Krzywizna na syntetycznej siatce N=3 (nie powinna sie wywalic, i
# wewnetrzne wierzcholki powinny dostac wartosc, brzegowe NaN)
# ---------------------------------------------------------------------


def test_compute_curvature_grid_interior_valid_boundary_nan():
    rng = np.random.default_rng(0)
    T, N = 8, 3
    # promien lekko oscylujacy w czasie, zeby uniknac zdegenerowanej plaskiej siatki
    base = 0.4 + 0.05 * np.sin(np.linspace(0, 4 * np.pi, T))
    radii = np.tile(base[:, None], (1, N)) + rng.normal(0, 0.01, (T, N))
    radii = np.abs(radii)
    times = np.arange(T, dtype=float) * 0.5
    angles = trumpet_angles(N)
    mesh = build_trumpet_mesh(radii, times, angles)
    K, valid = compute_curvature_grid(mesh, T, N)
    assert K.shape == (T, N)
    # brzegi czasowe (t_idx=0 i t_idx=T-1) nigdy nie sa wazne
    assert not np.any(valid[0, :])
    assert not np.any(valid[T - 1, :])
    # co najmniej jakis wewnetrzny wierzcholek powinien byc policzalny dla N=3
    assert np.any(valid[1:T - 1, :])


# ---------------------------------------------------------------------
# Test serii Walda-Wolfowitza -- wzor na znanych przykladach
# ---------------------------------------------------------------------


def test_runs_test_alternating_sequence_has_max_runs():
    signs = np.array([1.0, -1.0, 1.0, -1.0, 1.0, -1.0])
    res = wald_wolfowitz_runs_test(signs)
    assert res.degenerate is False
    assert res.n1 == 3
    assert res.n2 == 3
    assert res.R == 6  # maksymalna mozliwa liczba serii dla n=6
    assert res.mean_R == pytest.approx(4.0)
    assert res.z > 0  # wiecej serii niz losowo oczekiwane -> naprzemiennosc


def test_runs_test_two_blocks_has_minimum_runs():
    signs = np.array([1.0] * 5 + [-1.0] * 5)
    res = wald_wolfowitz_runs_test(signs)
    assert res.R == 2  # jeden blok +, jeden blok -
    assert res.z < 0  # mniej serii niz losowo oczekiwane -> sklejanie


def test_runs_test_all_same_sign_is_degenerate():
    signs = np.array([1.0, 1.0, 1.0, 1.0])
    res = wald_wolfowitz_runs_test(signs)
    assert res.degenerate is True
    assert res.p is None
    assert res.R == 1


def test_runs_test_rejects_zero_or_nan():
    with pytest.raises(ValueError):
        wald_wolfowitz_runs_test(np.array([1.0, 0.0, -1.0]))
    with pytest.raises(ValueError):
        wald_wolfowitz_runs_test(np.array([1.0, np.nan, -1.0]))


def test_curvature_sign_test_per_i_filters_nan_and_zero():
    K = np.array([
        [np.nan, np.nan],
        [1.0, 0.0],
        [-1.0, 2.0],
        [1.0, -3.0],
        [np.nan, np.nan],
    ])
    valid = np.array([
        [False, False],
        [True, True],
        [True, True],
        [True, True],
        [False, False],
    ])
    results = curvature_sign_test_per_i(K, valid)
    assert len(results) == 2
    # kolumna 0: wartosci [1,-1,1] -> n1=2,n2=1,n=3, n_nan=2, n_zero=0
    assert results[0].n1 == 2
    assert results[0].n2 == 1
    assert results[0].n_nan == 2
    assert results[0].n_zero == 0
    # kolumna 1: wartosci [0,2,-3] -> n_zero=1 (odfiltrowane), n1=1,n2=1
    assert results[1].n_zero == 1
    assert results[1].n1 == 1
    assert results[1].n2 == 1


# ---------------------------------------------------------------------
# spectrum_trace -- integracja z chrono_membrane_bridge (mala synteyka)
# ---------------------------------------------------------------------


def test_spectrum_trace_shapes_and_descending_order():
    rng = np.random.default_rng(1)
    n = 2000
    signals = {
        "DE": rng.normal(0, 1, n),
        "FE": rng.normal(0, 1, n),
        "BA": rng.normal(0, 1, n),
    }
    times, eig_matrix = spectrum_trace(signals, ["DE", "FE", "BA"], window_size=200, sample_rate_hz=1000.0)
    assert times.shape[0] == n // 200
    assert eig_matrix.shape == (n // 200, 3)
    # malejaco w kazdym wierszu
    assert np.all(np.diff(eig_matrix, axis=1) <= 1e-9)
    # czas rosnie
    assert np.all(np.diff(times) > 0)


def test_spectrum_trace_raises_when_too_few_windows():
    signals = {"DE": np.zeros(10), "FE": np.zeros(10)}
    with pytest.raises(ValueError):
        spectrum_trace(signals, ["DE", "FE"], window_size=5, sample_rate_hz=1000.0)
