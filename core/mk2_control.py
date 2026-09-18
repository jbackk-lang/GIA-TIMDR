"""TIMDR M/S<->K #2 — preregistered synthetic control harness.

This script validates the implementation of the candidate operator.
It is NOT a validation of the bridge on real data.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class Prereg:
    fs: float = 100.0
    n: int = 1000
    f0: float = 5.0
    noise_sd: float = 0.02
    a_ref: float = 1.0
    eps: float = 0.01
    n_rep: int = 30
    min_rel_amp: float = 0.05


def mc_ms_k(zero_mode: float, omega_1: float, eps: float) -> float:
    """Candidate M/S <-> K #2 operator."""
    if zero_mode < 0:
        raise ValueError("zero_mode must be non-negative")
    if omega_1 < 0:
        raise ValueError("omega_1 must be non-negative")
    if eps <= 0:
        raise ValueError("eps must be strictly positive")
    return omega_1 / (zero_mode + eps)


def omega1_fft(x: np.ndarray, cfg: Prereg) -> float:
    """First non-DC spectral candidate above a preregistered relative amplitude."""
    freqs = np.fft.rfftfreq(x.size, d=1.0 / cfg.fs)
    amp = np.abs(np.fft.rfft(x))
    positive = freqs > 0.0
    if not np.any(positive):
        raise ValueError("No non-DC spectral bins")
    max_non_dc = amp[positive].max()
    candidates = positive & (amp >= cfg.min_rel_amp * max_non_dc)
    candidates &= positive
    idx = np.flatnonzero(candidates)
    if idx.size == 0:
        raise ValueError("No modal candidate passed the preregistered filter")
    return float(freqs[idx].min())


def make_signal(baseline: float, seed: int, cfg: Prereg) -> np.ndarray:
    rng = np.random.default_rng(seed)
    t = np.arange(cfg.n) / cfg.fs
    return (
        baseline
        + np.sin(2.0 * np.pi * cfg.f0 * t)
        + cfg.noise_sd * rng.standard_normal(cfg.n)
    )


def summarize(values: np.ndarray) -> tuple[float, float]:
    return float(np.median(values)), float(np.std(values, ddof=1))


def main() -> None:
    cfg = Prereg()
    positive = []
    negative = []

    for i in range(cfg.n_rep):
        x_pos = make_signal(0.05, 100 + i, cfg)  # suppressed mean
        x_neg = make_signal(1.00, 200 + i, cfg)  # preserved mean

        for x, out in ((x_pos, positive), (x_neg, negative)):
            zero_mode = abs(float(np.mean(x))) / cfg.a_ref
            omega_1 = omega1_fft(x, cfg)
            out.append(mc_ms_k(zero_mode, omega_1, cfg.eps))

    positive = np.asarray(positive)
    negative = np.asarray(negative)
    u = stats.mannwhitneyu(positive, negative, alternative="greater")

    n1, n2 = positive.size, negative.size
    mu = n1 * n2 / 2.0
    sd = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12.0)
    z = (u.statistic - mu - 0.5) / sd
    r = z / math.sqrt(n1 + n2)

    pos_med, pos_sd = summarize(positive)
    neg_med, neg_sd = summarize(negative)

    print("MK-2 synthetic control report")
    print(f"N per group: {cfg.n_rep}")
    print(f"positive median/std: {pos_med:.6g} / {pos_sd:.6g}")
    print(f"negative median/std: {neg_med:.6g} / {neg_sd:.6g}")
    print(f"Mann-Whitney U: {u.statistic:.6g}")
    print(f"p (one-sided, greater): {u.pvalue:.6g}")
    print(f"effect r (normal approximation): {r:.6g}")
    print("NOTE: this is an implementation/control test, not empirical bridge validation.")


if __name__ == "__main__":
    main()
