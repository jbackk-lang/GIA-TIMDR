# core/chrono_trumpet_spectrum.py
"""
chrono_trumpet_spectrum.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_CHRONO_TRUMPET_SPECTRUM_v0.1.md) konstrukcji
"chrono_trumpet_spectrum": widmo macierzy korelacji (jak w
core/chrono_membrane_bridge.py, funkcje reuzyte bez zmian) zwiniete w
"trabke" -- indeks widma i=1..N rozlozony po obwodzie okregu (kat
stale), znormalizowana wartosc wlasna jako promien (zalezny od czasu),
czas jako os pionowa. To PIERWSZA konstrukcja w rodzinie chrono_cone/
chrono_membrane, ktora daje PRAWDZIWA siatke 2D (indeks x czas), wiec
pierwsza, do ktorej mozna zastosowac dyskretny operator Weingartena
(TIMDR-Geometry-Formalism/timdr_geometry/weingarten.py, G8-G9) -- ten
modul NIE przepisuje operatora, tylko buduje siatke (Mesh) w formacie,
jakiego on wymaga (wierzcholki+trojkatne faces), wzorem
make_cylinder_mesh z tego samego pliku.

WAZNE ODROZNIENIE od B4_BEARING_DATA_FREEZE.md: ta konstrukcja NIE
uzywa fizycznych wspolrzednych czujnikow DE/FE/BA jako wierzcholkow
siatki (freeze na to pozostaje w mocy) -- wierzcholkami sa punkty
SKONSTRUOWANE z WARTOSCI WIDMA w sztucznie zdefiniowanym ukladzie
kat+promien+czas, z jawna, gesta, prerejestrowana triangulacja
regularnej siatki. Inny obiekt matematyczny niz to, czego zakazuje
freeze.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow na
realnych danych CWRU.
"""
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
from scipy.stats import norm

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_GEOMETRY_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Geometry-Formalism")
_SIBLING_ROOT = os.path.dirname(_REPO_ROOT)
for _p in (_REPO_ROOT, _GEOMETRY_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_geometry.weingarten import (  # noqa: E402
    Mesh,
    vertex_normals,
    one_ring,
    discrete_shape_operator,
    gaussian_curvature,
)
from core.chrono_membrane_bridge import (  # noqa: E402
    channel_correlation_matrix,
    spectrum_from_correlation,
)

WINDOW_SIZE = 256  # PREREG SS4.3 -- zamrozone, srodkowe z WINDOW_SIZES chrono_membrane_bridge


# ---------------------------------------------------------------------
# PREREG SS2. Widmo w kolejnych (nieprzecinajacych sie) oknach --
# konstrukcja z chrono_membrane_bridge, reuzyta bez zmian
# ---------------------------------------------------------------------


def spectrum_trace(
    signals: Dict[str, np.ndarray],
    channels: List[str],
    window_size: int = WINDOW_SIZE,
    sample_rate_hz: float = 12_000.0,
) -> "tuple[np.ndarray, np.ndarray]":
    """Zwraca (times, eig_matrix). times: (T,) czas [s] poczatku
    kazdego okna. eig_matrix: (T,N) lambda_1>=...>=lambda_N>=0 na
    kazdym oknie (spectrum_from_correlation, BEZ ZMIAN)."""
    n = len(signals[channels[0]])
    n_avail = n // window_size
    if n_avail < 3:
        raise ValueError(
            f"za malo oknien ({n_avail}) do zbudowania trajektorii czasowej trabki"
        )
    times = np.empty(n_avail, dtype=float)
    eig_matrix = np.empty((n_avail, len(channels)), dtype=float)
    for k in range(n_avail):
        seg = [signals[ch][k * window_size:(k + 1) * window_size] for ch in channels]
        C = channel_correlation_matrix(seg)
        eig_matrix[k] = spectrum_from_correlation(C)
        times[k] = (k * window_size) / sample_rate_hz
    return times, eig_matrix


def radii_from_eigs(eig_matrix: np.ndarray) -> np.ndarray:
    """PREREG SS2 -- r_i(t) = lambda_i(t) / sum_j lambda_j(t).
    Normalizacja potrzebna, zeby porownywac KSZTALT powierzchni
    niezaleznie od amplitudy sygnalu (surowe lambda_i zaleza od skali
    kanalu/pliku)."""
    sums = eig_matrix.sum(axis=1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        radii = eig_matrix / sums
    degenerate = (sums[:, 0] < 1e-12)
    radii[degenerate, :] = np.nan
    return radii


def trumpet_angles(n_channels: int) -> np.ndarray:
    """PREREG SS2 -- theta_i = 2*pi*(i-1)/N dla i=1..N (0-indeksowane
    tutaj: theta[k] = 2*pi*k/N dla k=0..N-1, rownowazne)."""
    return np.array([2.0 * np.pi * k / n_channels for k in range(n_channels)])


# ---------------------------------------------------------------------
# PREREG SS3. Adaptacja do formatu Mesh weingarten.py (wzorzec
# make_cylinder_mesh, NIE przepisanie operatora)
# ---------------------------------------------------------------------


def build_trumpet_vertices(radii: np.ndarray, times: np.ndarray, angles: np.ndarray) -> np.ndarray:
    """(i,t) -> (r_i(t)*cos(theta_i), r_i(t)*sin(theta_i), t). Porzadek
    wierzcholkow v = t_idx*N + i_idx (PREREG SS3.2, jak w
    make_cylinder_mesh: t zewnetrzna petla, i wewnetrzna zawinieta)."""
    T, N = radii.shape
    assert len(times) == T
    assert len(angles) == N
    verts = np.empty((T * N, 3), dtype=float)
    cos_a = np.cos(angles)
    sin_a = np.sin(angles)
    for t_idx in range(T):
        r_row = radii[t_idx]
        verts[t_idx * N:(t_idx + 1) * N, 0] = r_row * cos_a
        verts[t_idx * N:(t_idx + 1) * N, 1] = r_row * sin_a
        verts[t_idx * N:(t_idx + 1) * N, 2] = times[t_idx]
    return verts


def build_trumpet_faces(n_t: int, n_channels: int) -> np.ndarray:
    """PREREG SS3.3 -- dokladnie regula make_cylinder_mesh: i zawiniete
    modulo N (obwod), t NIE zawiniete (czas ma poczatek i koniec)."""
    faces = []
    for j in range(n_t - 1):
        for i in range(n_channels):
            a = j * n_channels + i
            b = j * n_channels + (i + 1) % n_channels
            c = (j + 1) * n_channels + i
            d = (j + 1) * n_channels + (i + 1) % n_channels
            faces.append([a, b, d])
            faces.append([a, d, c])
    return np.array(faces, dtype=int)


def build_trumpet_mesh(radii: np.ndarray, times: np.ndarray, angles: np.ndarray) -> Mesh:
    verts = build_trumpet_vertices(radii, times, angles)
    T, N = radii.shape
    faces = build_trumpet_faces(T, N)
    return Mesh(verts, faces)


# ---------------------------------------------------------------------
# PREREG SS4.1. Krzywizna Gaussa per wierzcholek wewnetrzny (t_idx in
# [1, T-2], i_idx dowolne -- zawsze pelny 1-ring katowy)
# ---------------------------------------------------------------------


def compute_curvature_grid(mesh: Mesh, n_t: int, n_channels: int) -> "tuple[np.ndarray, np.ndarray]":
    """Zwraca (K, valid): K (T,N) NaN poza wewnetrznymi wierzcholkami
    lub gdy discrete_shape_operator rzuci ValueError (zdegenerowany
    rzad/za malo sasiadow -- PREREG SS3.4). valid (T,N) bool."""
    normals = vertex_normals(mesh)
    rings = one_ring(mesh)
    K = np.full((n_t, n_channels), np.nan, dtype=float)
    valid = np.zeros((n_t, n_channels), dtype=bool)
    if not np.all(np.isfinite(mesh.vertices)):
        finite_mask = np.all(np.isfinite(mesh.vertices), axis=1)
    else:
        finite_mask = None
    for t_idx in range(1, n_t - 1):
        for i_idx in range(n_channels):
            v = t_idx * n_channels + i_idx
            if finite_mask is not None and not finite_mask[v]:
                continue  # NaN promien (zdegenerowane okno) -- pomin
            try:
                op = discrete_shape_operator(mesh, normals, v, rings=rings)
            except ValueError:
                continue
            K[t_idx, i_idx] = gaussian_curvature(op)
            valid[t_idx, i_idx] = True
    return K, valid


# ---------------------------------------------------------------------
# PREREG SS4.2. Test serii Walda-Wolfowitza na sekwencji znakow K(i,t)
# ---------------------------------------------------------------------


@dataclass
class RunsTestResult:
    n1: int
    n2: int
    n: int
    n_zero: int
    n_nan: int
    R: Optional[int]
    mean_R: Optional[float]
    var_R: Optional[float]
    z: Optional[float]
    p: Optional[float]
    degenerate: bool


def wald_wolfowitz_runs_test(signs: np.ndarray) -> RunsTestResult:
    """PREREG SS4.2 -- signs: 1D array zawierajacy TYLKO +1/-1 (zera i
    NaN musza byc odfiltrowane PRZED wywolaniem, zliczone osobno przez
    wywolujacego). Standardowy wzor testu serii Walda-Wolfowitza."""
    signs = np.asarray(signs, dtype=float)
    if np.any(signs == 0) or np.any(~np.isfinite(signs)):
        raise ValueError("signs musi zawierac WYLACZNIE +1/-1 (bez zer/NaN) -- odfiltruj przed wywolaniem")

    n1 = int(np.sum(signs > 0))
    n2 = int(np.sum(signs < 0))
    n = n1 + n2

    if n == 0:
        return RunsTestResult(0, 0, 0, 0, 0, None, None, None, None, None, True)
    if n1 == 0 or n2 == 0:
        return RunsTestResult(n1, n2, n, 0, 0, 1, None, None, None, None, True)

    R = 1 + int(np.sum(signs[1:] != signs[:-1]))
    mean_R = 2.0 * n1 * n2 / n + 1.0
    var_R = (2.0 * n1 * n2 * (2.0 * n1 * n2 - n)) / (n ** 2 * (n - 1))
    if var_R <= 0:
        return RunsTestResult(n1, n2, n, 0, 0, R, mean_R, var_R, None, None, True)

    z = (R - mean_R) / np.sqrt(var_R)
    p = 2.0 * (1.0 - norm.cdf(abs(z)))
    return RunsTestResult(n1, n2, n, 0, 0, R, mean_R, var_R, float(z), float(p), False)


def curvature_sign_test_per_i(K: np.ndarray, valid: np.ndarray) -> List[RunsTestResult]:
    """Dla kazdej kolumny i (indeks widma), test serii na sekwencji
    znakow K(i,:) (kolejnosc czasowa), po odfiltrowaniu NaN/zer."""
    n_t, n_channels = K.shape
    results = []
    for i_idx in range(n_channels):
        col_K = K[:, i_idx]
        col_valid = valid[:, i_idx]
        vals = col_K[col_valid]
        n_nan = int(np.sum(~col_valid))
        n_zero = int(np.sum(vals == 0.0))
        nonzero = vals[vals != 0.0]
        signs = np.sign(nonzero)
        res = wald_wolfowitz_runs_test(signs)
        res.n_zero = n_zero
        res.n_nan = n_nan
        results.append(res)
    return results


# ---------------------------------------------------------------------
# Pelny pipeline diagnostyczny dla jednego pliku CWRU
# ---------------------------------------------------------------------


@dataclass
class TrumpetDiagnostic:
    n_t: int
    n_channels: int
    n_valid_vertices: int
    n_interior_vertices: int
    per_i: List[RunsTestResult]


def trumpet_diagnostic(
    signals: Dict[str, np.ndarray],
    channels: List[str],
    window_size: int = WINDOW_SIZE,
    sample_rate_hz: float = 12_000.0,
) -> TrumpetDiagnostic:
    times, eig_matrix = spectrum_trace(signals, channels, window_size, sample_rate_hz)
    radii = radii_from_eigs(eig_matrix)
    angles = trumpet_angles(len(channels))
    mesh = build_trumpet_mesh(radii, times, angles)
    n_t, n_channels = radii.shape
    K, valid = compute_curvature_grid(mesh, n_t, n_channels)
    per_i = curvature_sign_test_per_i(K, valid)
    n_interior = (n_t - 2) * n_channels if n_t >= 2 else 0
    return TrumpetDiagnostic(
        n_t=n_t,
        n_channels=n_channels,
        n_valid_vertices=int(valid.sum()),
        n_interior_vertices=n_interior,
        per_i=per_i,
    )


def format_diagnostic(name: str, diag: TrumpetDiagnostic) -> str:
    lines = [
        f"### {name} (N={diag.n_channels}, T={diag.n_t} okien, "
        f"wierzcholki_wewnetrzne={diag.n_interior_vertices}, "
        f"wazne(nie-degenerate)={diag.n_valid_vertices})"
    ]
    for i_idx, res in enumerate(diag.per_i):
        if res.degenerate:
            lines.append(
                f"  i={i_idx}: n1={res.n1} n2={res.n2} n_zero={res.n_zero} "
                f"n_nan={res.n_nan} -- DEGENERATE (jedna klasa pusta lub n=0), test serii niezdefiniowany"
            )
        else:
            lines.append(
                f"  i={i_idx}: n1={res.n1} n2={res.n2} n={res.n} n_zero={res.n_zero} "
                f"n_nan={res.n_nan} R={res.R} E[R]={res.mean_R:.3f} "
                f"z={res.z:+.3f} p={res.p:.4g}"
            )
    return "\n".join(lines)


if __name__ == "__main__":
    from timdr_geometry.b4_bearing_data_gate import load_synchronous_cwru_channels

    _BEARING_DIR = os.path.join(
        _SIBLING_ROOT, "TIMDR-Industrial-Predict", "data", "cwru_bearing",
        "b4_raw", "source_mirror", "Data", "1797 RPM",
    )
    NORMAL_FILE = os.path.join(_BEARING_DIR, "1797_Normal.npz")
    IR_FILE = os.path.join(_BEARING_DIR, "1797_IR_21_DE12.npz")
    OR6_FILE = os.path.join(_BEARING_DIR, "1797_OR@6_21_DE12.npz")

    t0 = time.time()
    normal = load_synchronous_cwru_channels(NORMAL_FILE, required_channels=("DE", "FE"))
    ir = load_synchronous_cwru_channels(IR_FILE, required_channels=("DE", "FE", "BA"))
    or6 = load_synchronous_cwru_channels(OR6_FILE, required_channels=("DE", "FE", "BA"))

    diag_normal = trumpet_diagnostic(normal.signals, ["DE", "FE"])
    diag_ir = trumpet_diagnostic(ir.signals, ["DE", "FE", "BA"])
    diag_or6 = trumpet_diagnostic(or6.signals, ["DE", "FE", "BA"])
    dt = time.time() - t0

    print("=== chrono_trumpet_spectrum -- diagnostyka krzywizny (EKSPLORACYJNE, patrz PREREG SS5) ===\n")
    print(format_diagnostic("Normal", diag_normal))
    print()
    print(format_diagnostic("IR_21", diag_ir))
    print()
    print(format_diagnostic("OR6_21", diag_or6))
    print(f"\nCzas: {dt:.1f}s")
