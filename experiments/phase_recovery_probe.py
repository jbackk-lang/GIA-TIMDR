"""Controlled probe separating frequency re-lock from phase recovery.

This probe deliberately does not call frequency re-lock "information repair".
It produces reproducible phase-step and temporary-detuning traces and reports
phase/frequency residuals separately. Requires numpy and scipy.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.signal import hilbert


def circular_error(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.angle(np.exp(1j * (a - b)))


def make_trace(fs: float = 4000.0, duration: float = 6.0,
               phase_step: float = np.pi / 2, detune: float = 0.03,
               detune_start: float = 2.0, detune_end: float = 4.0):
    t = np.arange(int(fs * duration)) / fs
    f0 = 80.0
    # Pure phase step: frequency is unchanged; only phase origin changes.
    phase_step_at = 2.0
    phi_step = 2 * np.pi * f0 * t + phase_step * (t >= phase_step_at)
    x_step = np.sin(phi_step)

    # Temporary frequency detuning: frequency returns, accumulated phase does not.
    inst_f = np.full_like(t, f0)
    mask = (t >= detune_start) & (t < detune_end)
    inst_f[mask] = f0 * (1.0 + detune)
    phi_detune = 2 * np.pi * np.cumsum(inst_f) / fs
    x_detune = np.sin(phi_detune)
    phi_nominal = 2 * np.pi * f0 * t
    return t, x_step, phi_step, x_detune, phi_detune, phi_nominal, inst_f


def estimate_phase(signal: np.ndarray) -> np.ndarray:
    return np.unwrap(np.angle(hilbert(signal)))


def summarize(t, signal, phase_truth, nominal_phase, true_frequency):
    phase_hat = estimate_phase(signal)
    phase_error = circular_error(phase_hat, phase_truth)
    # Derivative of unwrapped analytic phase estimates instantaneous frequency.
    freq_hat = np.gradient(phase_hat) * (len(t) / (t[-1] - t[0])) / (2 * np.pi)
    windows = {
        "before": (t >= 0.5) & (t < 1.8),
        "during": (t >= 2.2) & (t < 3.8),
        "after": (t >= 4.2) & (t < 5.8),
    }
    result = {}
    for name, mask in windows.items():
        result[name] = {
            "phase_error_rms_rad": round(float(np.sqrt(np.mean(phase_error[mask] ** 2))), 6),
            "frequency_error_rms_hz": round(float(np.sqrt(np.mean((freq_hat[mask] - true_frequency[mask]) ** 2))), 6),
            "phase_error_vs_nominal_rms_rad": round(float(np.sqrt(np.mean(circular_error(phase_hat[mask], nominal_phase[mask]) ** 2))), 6),
        }
    return result


def run():
    fs = 4000.0
    t, xs, ps, xd, pd, pn, fd = make_trace(fs=fs)
    # Independent payload sentinel: analysis must not mutate the stored payload.
    payload = bytes([0, 1, 1, 0, 1, 0, 0, 1] * 128)
    digest_before = hashlib.sha256(payload).hexdigest()
    # The estimator receives only signal arrays, never the payload.
    phase_case = summarize(t, xs, ps, pn, np.full_like(t, 80.0))
    detune_case = summarize(t, xd, pd, pn, fd)
    digest_after = hashlib.sha256(payload).hexdigest()
    return {
        "status": "controlled_signal_probe_not_information_recovery",
        "sample_rate_hz": fs,
        "phase_step_rad": round(float(np.pi / 2), 6),
        "temporary_detune_fraction": 0.03,
        "temporary_detune_seconds": 2.0,
        "pure_phase_step": phase_case,
        "temporary_detune_then_return": detune_case,
        "payload_digest_unchanged": digest_before == digest_after,
        "payload_digest": digest_before,
        "limitations": [
            "analytic-signal estimator is a measurement baseline, not a TIMDR phase repair algorithm",
            "no cryptographic or adversarial data recovery is tested",
            "frequency return does not imply phase-offset removal",
            "synthetic narrowband signals only",
        ],
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
