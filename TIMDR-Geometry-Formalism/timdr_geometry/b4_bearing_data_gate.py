"""Readiness gate for the preregistered B4-Bearing data path.

The CWRU recordings provide synchronous accelerometer channels, but an
accelerometer triplet is not automatically a surface.  This module makes that
boundary executable: it validates the common sample-time grid and refuses to
construct curvature unless a separately measured, sufficiently sampled sensor
mesh is supplied.  It never invents coordinates, triangulation, or samples.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np


CHANNEL_ORDER = ("DE", "FE", "BA")


@dataclass(frozen=True)
class BearingChannels:
    """Synchronous CWRU channels and their explicit relative time axis."""

    time: np.ndarray
    signals: dict[str, np.ndarray]
    sample_rate_hz: float


@dataclass(frozen=True)
class BearingGeometryReadiness:
    """Result of checking whether curvature may be calculated honestly."""

    ready: bool
    reasons: tuple[str, ...]


def _as_signal_vector(value: np.ndarray, channel: str) -> np.ndarray:
    value = np.asarray(value, dtype=float)
    if value.ndim == 2 and value.shape[1] == 1:
        value = value[:, 0]
    if value.ndim != 1 or value.size == 0:
        raise ValueError(f"kanał {channel} musi być niepustym wektorem 1D")
    if not np.all(np.isfinite(value)):
        raise ValueError(f"kanał {channel} zawiera NaN/inf")
    return value


def load_synchronous_cwru_channels(
    path: str | Path,
    *,
    sample_rate_hz: float = 12_000.0,
    required_channels: Sequence[str] = CHANNEL_ORDER,
) -> BearingChannels:
    """Load same-recording CWRU channels on ``t_i = i / sample_rate_hz``.

    The time axis is an acquisition-relative axis, not an inferred UTC clock.
    Every accepted channel comes from the same NPZ recording and has exactly
    the same number of samples.  Cross-recording alignment is intentionally
    not implemented.
    """
    if not np.isfinite(sample_rate_hz) or sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz musi być skończone i > 0")

    path = Path(path)
    with np.load(path, allow_pickle=False) as archive:
        missing = [channel for channel in required_channels if channel not in archive]
        if missing:
            raise ValueError(f"brak wymaganych kanałów: {', '.join(missing)}")
        signals = {
            channel: _as_signal_vector(archive[channel], channel)
            for channel in required_channels
        }

    lengths = {values.size for values in signals.values()}
    if len(lengths) != 1:
        raise ValueError("kanały nie mają identycznej liczby próbek; brak wspólnej osi czasu")

    n_samples = lengths.pop()
    time = np.arange(n_samples, dtype=float) / float(sample_rate_hz)
    return BearingChannels(time=time, signals=signals, sample_rate_hz=float(sample_rate_hz))


def assess_measured_sensor_mesh(
    sensor_coordinates: np.ndarray | None,
    faces: np.ndarray | None,
    *,
    n_signal_channels: int,
) -> BearingGeometryReadiness:
    """Require an independently measured closed mesh before using ``H``.

    Three channels can form at most one triangle.  A single triangle has no
    vertex with a full two-dimensional one-ring and cannot support the
    discrete Weingarten fit used by this repository.  Interpolating extra
    vertices from those channels would be a new proxy model, not measured
    geometry, and is deliberately outside this B4 gate.
    """
    reasons: list[str] = []
    if sensor_coordinates is None:
        reasons.append("brak mierzonych współrzędnych czujników")
    else:
        sensor_coordinates = np.asarray(sensor_coordinates, dtype=float)
        if sensor_coordinates.ndim != 2 or sensor_coordinates.shape[1] != 3:
            reasons.append("współrzędne czujników muszą mieć kształt (N, 3)")
        elif not np.all(np.isfinite(sensor_coordinates)):
            reasons.append("współrzędne czujników zawierają NaN/inf")
        elif sensor_coordinates.shape[0] < 4:
            reasons.append("siatka geometrii wymaga co najmniej 4 mierzonych węzłów")
        elif sensor_coordinates.shape[0] != n_signal_channels:
            reasons.append("liczba współrzędnych nie zgadza się z liczbą kanałów")

    if faces is None:
        reasons.append("brak prerejestrowanej triangulacji mierzonych węzłów")
    else:
        faces = np.asarray(faces, dtype=int)
        if faces.ndim != 2 or faces.shape[1] != 3 or faces.shape[0] < 4:
            reasons.append("triangulacja musi mieć co najmniej 4 trójkątne ściany")

    return BearingGeometryReadiness(ready=not reasons, reasons=tuple(reasons))
