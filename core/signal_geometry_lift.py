"""Explicit 2D phasor-to-3D geometric lift.

This is a representation operator, not a physical signal-to-helix law.
A complex/phasor signal q1 + i*q2 supplies transverse coordinates;
z supplies the third coordinate; an SO(3) frame defines orientation.
"""
from __future__ import annotations

from typing import Sequence
import numpy as np


def lift_phasor_to_3d(q1: Sequence[float], q2: Sequence[float], z: Sequence[float],
                      frame: np.ndarray, origin: Sequence[float] = (0.0, 0.0, 0.0),
                      *, atol: float = 1e-9) -> np.ndarray:
    """Embed a 2D phasor sequence into R^3 using an oriented frame.

    frame is one 3x3 SO(3) matrix or an (N,3,3) sequence. Frame
    vectors are columns e1=frame[:,0], e2=frame[:,1], e3=frame[:,2].
    Returns X[n] = origin + q1[n]*e1[n] + q2[n]*e2[n] + z[n]*e3[n].
    This operator does not infer dynamics, forces, or physical coupling.
    """
    a = np.asarray(q1, dtype=float)
    b = np.asarray(q2, dtype=float)
    axial = np.asarray(z, dtype=float)
    c = np.asarray(origin, dtype=float)
    F = np.asarray(frame, dtype=float)
    if a.ndim != 1 or b.shape != a.shape or axial.shape != a.shape:
        raise ValueError("q1, q2 and z must be 1D arrays with identical shape")
    if c.shape != (3,):
        raise ValueError("origin must be a 3-vector")
    if F.shape == (3, 3):
        F = np.broadcast_to(F, (len(a), 3, 3))
    if F.shape != (len(a), 3, 3):
        raise ValueError("frame must have shape (3,3) or (N,3,3)")
    if not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))
            and np.all(np.isfinite(axial)) and np.all(np.isfinite(c))
            and np.all(np.isfinite(F))):
        raise ValueError("all inputs must be finite")
    gram = np.swapaxes(F, 1, 2) @ F
    identity = np.broadcast_to(np.eye(3), gram.shape)
    determinants = np.linalg.det(F)
    if not np.allclose(gram, identity, atol=atol, rtol=0.0):
        raise ValueError("each frame must be orthonormal")
    if not np.allclose(determinants, 1.0, atol=atol, rtol=0.0):
        raise ValueError("each frame must be right-handed with det=+1")
    return (c[None, :] + a[:, None] * F[:, :, 0]
            + b[:, None] * F[:, :, 1] + axial[:, None] * F[:, :, 2])


def recover_phasor_coordinates(points: np.ndarray, frame: np.ndarray,
                                origin: Sequence[float] = (0.0, 0.0, 0.0)
                                ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Recover (q1,q2,z) by projection onto the same orthonormal frame."""
    X = np.asarray(points, dtype=float)
    c = np.asarray(origin, dtype=float)
    F = np.asarray(frame, dtype=float)
    if X.ndim != 2 or X.shape[1] != 3 or c.shape != (3,):
        raise ValueError("points must be (N,3) and origin a 3-vector")
    if F.shape == (3, 3):
        F = np.broadcast_to(F, (len(X), 3, 3))
    if F.shape != (len(X), 3, 3):
        raise ValueError("frame must have shape (3,3) or (N,3,3)")
    local = np.einsum("nij,ni->nj", np.swapaxes(F, 1, 2), X - c)
    return local[:, 0], local[:, 1], local[:, 2]
