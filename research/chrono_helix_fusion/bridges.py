"""Explicit experimental bridges M/S<->G, G<->K, K<->M/S.

Correlations are descriptive coupling proxies, NOT causal or topological proofs.
"""
import numpy as np
from scipy.signal import hilbert


def _corr(x, y):
    if len(x) < 4 or np.std(x) < 1e-10 or np.std(y) < 1e-10:
        return 0.0
    return float(np.clip(np.corrcoef(x, y)[0, 1], -1, 1))


def lagged_bridge(x, y, max_lag=12):
    """Return signed maximum-absolute Pearson correlation and its lag.

    Positive lag means y is shifted forward relative to x.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.shape != y.shape or x.ndim != 1 or len(x) < 2*max_lag+8:
        raise ValueError("Signals must be equal-length vectors longer than 2*max_lag+8")
    x, y = x-np.mean(x), y-np.mean(y)
    candidates = []
    for lag in range(-max_lag, max_lag+1):
        if lag < 0:
            a, b = x[-lag:], y[:lag]
        elif lag > 0:
            a, b = x[:-lag], y[lag:]
        else:
            a, b = x, y
        candidates.append((lag, _corr(a, b)))
    lag, corr = max(candidates, key=lambda p: abs(p[1]))
    return {"lag_samples":int(lag), "correlation":float(corr)}


def bridge_features(x, fs=360., max_lag=12):
    """Derive time-aligned proxies for M/S, G and K then three pairwise bridges."""
    x = np.asarray(x, float)
    if x.ndim != 1 or len(x) < 2*max_lag+12 or not np.isfinite(x).all():
        raise ValueError("Invalid signal")
    analytic = hilbert(x-np.median(x))
    amplitude = np.abs(analytic)
    phase = np.unwrap(np.angle(analytic))
    z = np.column_stack([analytic.real, analytic.imag, np.arange(len(x))/fs])
    v = np.gradient(z, 1/fs, axis=0)
    acc = np.gradient(v, 1/fs, axis=0)
    curvature = np.linalg.norm(np.cross(v, acc), axis=1)/(np.linalg.norm(v, axis=1)**3+1e-8)
    curvature = np.clip(curvature, 0, np.quantile(curvature, .99))
    # All series aligned to length N-2, avoiding artificial padding.
    ms = np.abs(np.diff(amplitude))[1:]
    g = np.abs(np.diff(curvature))[1:]
    k = np.abs(np.diff(phase, n=2))
    return {
        "MS_G":lagged_bridge(ms,g,max_lag),
        "G_K":lagged_bridge(g,k,max_lag),
        "K_MS":lagged_bridge(k,ms,max_lag),
    }


def vector(x, fs=360., max_lag=12):
    b = bridge_features(x, fs=fs, max_lag=max_lag)
    return [v for name in ("MS_G","G_K","K_MS")
            for v in (b[name]["correlation"], b[name]["lag_samples"]/float(max_lag))]
