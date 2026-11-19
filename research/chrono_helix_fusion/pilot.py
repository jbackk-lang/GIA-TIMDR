"""CHF pilot: public ECG signal, basic helix features; NOT a clinical detector."""
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import datasets, signal

FS = 360.0


def features(x, fs=FS):
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or len(x) < 20 or not np.isfinite(x).all():
        raise ValueError("Expected finite one-dimensional signal of length >=20")
    x = x - np.median(x)
    analytic = signal.hilbert(x)
    amplitude = np.abs(analytic)
    phase = np.unwrap(np.angle(analytic))
    t = np.arange(len(x)) / fs
    # Time scale chosen only for visualization/prototyping, not fitted on test labels.
    helix = np.column_stack((amplitude * np.cos(phase),
                             amplitude * np.sin(phase), t))
    velocity = np.gradient(helix, 1 / fs, axis=0)
    acceleration = np.gradient(velocity, 1 / fs, axis=0)
    curvature = np.linalg.norm(np.cross(velocity, acceleration), axis=1) / (
        np.linalg.norm(velocity, axis=1) ** 3 + 1e-9)
    freq = np.diff(phase) * fs / (2 * np.pi)
    return {
        "rms": float(np.sqrt(np.mean(x*x))),
        "mean_envelope": float(np.mean(amplitude)),
        "median_helix_curvature": float(np.median(curvature)),
        "median_instantaneous_frequency_hz": float(np.median(freq)),
    }


def main():
    x = datasets.electrocardiogram()  # downloads/caches public sample on first use
    segment = np.asarray(x[10000:13600], dtype=np.float64)
    report = {
        "project": "GIA-TIMDR / CHRONO-HELIX-FUSION",
        "status": "exploratory_features_only",
        "dataset": "SciPy electrocardiogram sample (public ECG record)",
        "sampling_rate_hz": FS,
        "sample_count": int(segment.size),
        "sha256_segment_float64": hashlib.sha256(segment.tobytes()).hexdigest(),
        "features": features(segment),
        "caveat": "No labels, held-out evaluation, Möbius topology proof or superiority claim.",
    }
    out = Path(__file__).with_name("pilot_results.json")
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
