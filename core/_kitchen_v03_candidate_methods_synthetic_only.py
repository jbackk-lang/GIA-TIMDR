"""Candidate-method comparison for B4-Kitchen v0.3 -- SYNTHETIC DATA ONLY.

This script NEVER touches the real Kitchen geometry/audio data or the
frozen lambda_g/lambda_meta series. It exists purely to compare, on the
exact same synthetic positive/negative controls used by v0.1 and v0.2
(identical generators and seeds), which candidate null-distribution
method for the Spearman test best resolves the known false-positive
problem (full permutation, then block permutation L=12, both already
failed/partially-failed the AR(1) negative control in v0.1/v0.2).

Candidates compared:
  1. block permutation L=12 (v0.2, for reference)
  2. block permutation L=20
  3. block permutation L=25
  4. block permutation L=40
  5. HAC-adjusted Spearman z-test (Newey-West style variance of the mean
     cross-product of centered ranks, Bartlett kernel, bandwidth = L-1)
  6. AR(1) effective-sample-size adjusted Spearman t-test (Bartlett-style
     n_eff = n * (1 - r1x*r1y) / (1 + r1x*r1y), using lag-1 autocorrelation
     of the RANKS of each series)

This is exploratory method-selection work, explicitly allowed to look at
results on synthetic data (the same controls already frozen in the v0.1/
v0.2 PREREGs) -- selecting a method here does NOT touch the frozen real
Kitchen result and does NOT retroactively change v0.1 or v0.2.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b4_kitchen_run_v0_2 as mod  # noqa: E402  (reuse _rank, _ar1, N_PERMUTATIONS, SEED)

N = 1645
ALPHA = 0.05


def _spearman_rho(rx: np.ndarray, ry: np.ndarray) -> float:
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    denom = float(np.linalg.norm(rx) * np.linalg.norm(ry))
    if denom == 0.0:
        raise ValueError("constant series")
    return float(np.dot(rx, ry) / denom)


def block_permutation(x: np.ndarray, y: np.ndarray, seed: int, block_length: int) -> dict:
    rx = mod._rank(x)
    ry_full = mod._rank(y)
    rx_c = rx - rx.mean()
    denom_x = float(np.linalg.norm(rx_c))
    n = rx.size

    def rho_for(ry_arr):
        ry_c = ry_arr - ry_arr.mean()
        denom = denom_x * float(np.linalg.norm(ry_c))
        return float(np.dot(rx_c, ry_c) / denom)

    observed = rho_for(ry_full)
    rng = np.random.default_rng(seed)
    n_blocks = math.ceil(n / block_length)
    exceed = 0
    for _ in range(mod.N_PERMUTATIONS):
        offset = int(rng.integers(0, n))
        y_shift = np.concatenate((ry_full[offset:], ry_full[:offset]))
        order = rng.permutation(n_blocks)
        pieces = [y_shift[b * block_length : (b + 1) * block_length] for b in order]
        y_perm = np.concatenate(pieces)[:n]
        if abs(rho_for(y_perm)) >= abs(observed):
            exceed += 1
    return {"rho": observed, "pvalue": (1 + exceed) / (mod.N_PERMUTATIONS + 1), "exceed": exceed}


def hac_adjusted_spearman(x: np.ndarray, y: np.ndarray, bandwidth: int) -> dict:
    """Newey-West / Bartlett-kernel HAC variance for mean(rx_c * ry_c),
    used to z-test whether the observed Spearman rho differs from 0 under
    autocorrelated ranks. Standard HAC construction applied to the
    product series u_t = rx_c[t] * ry_c[t] (mean(u) is proportional to
    the numerator of rho); se_hac estimates the long-run variance of that
    mean using a Bartlett kernel out to `bandwidth` lags.
    """
    rx = mod._rank(x)
    ry = mod._rank(y)
    rx_c = rx - rx.mean()
    ry_c = ry - ry.mean()
    n = rx.size
    denom = float(np.linalg.norm(rx_c) * np.linalg.norm(ry_c))
    rho = float(np.dot(rx_c, ry_c) / denom)

    u = rx_c * ry_c
    u_c = u - u.mean()
    gamma0 = float(np.dot(u_c, u_c) / n)
    var_lr = gamma0
    for lag in range(1, bandwidth + 1):
        w = 1.0 - lag / (bandwidth + 1)  # Bartlett kernel
        gamma_lag = float(np.dot(u_c[lag:], u_c[:-lag]) / n)
        var_lr += 2.0 * w * gamma_lag
    var_lr = max(var_lr, 1e-12)
    se_mean_u = math.sqrt(var_lr / n)
    # scale factor relating d(mean u)/d(rho) at the observed point:
    # rho = sum(rx_c*ry_c) / (||rx_c||*||ry_c||) = mean(u) * n / denom
    se_rho = se_mean_u * n / denom
    z = rho / se_rho if se_rho > 0 else float("inf")
    # two-sided normal p-value via erfc (no scipy dependency)
    pvalue = math.erfc(abs(z) / math.sqrt(2.0))
    return {"rho": rho, "z": z, "pvalue": pvalue, "bandwidth": bandwidth}


def ar1_effective_n_spearman(x: np.ndarray, y: np.ndarray) -> dict:
    """Bartlett-style effective sample size for correlating two
    autocorrelated series: n_eff = n * (1 - r1x*r1y) / (1 + r1x*r1y),
    using lag-1 autocorrelation of each series' RANKS. Then a standard
    t-approximation for Spearman significance with n_eff replacing n.
    """
    rx = mod._rank(x)
    ry = mod._rank(y)
    rx_c = rx - rx.mean()
    ry_c = ry - ry.mean()
    n = rx.size
    denom = float(np.linalg.norm(rx_c) * np.linalg.norm(ry_c))
    rho = float(np.dot(rx_c, ry_c) / denom)

    def lag1_autocorr(v_c):
        num = float(np.dot(v_c[1:], v_c[:-1]))
        den = float(np.dot(v_c, v_c))
        return num / den if den > 0 else 0.0

    r1x = lag1_autocorr(rx_c)
    r1y = lag1_autocorr(ry_c)
    denom_eff = 1.0 + r1x * r1y
    n_eff = n * (1.0 - r1x * r1y) / denom_eff if denom_eff > 0 else n
    n_eff = max(n_eff, 3.0)
    # t statistic for Spearman rho with n_eff
    t_stat = rho * math.sqrt((n_eff - 2) / max(1e-12, 1 - rho ** 2))
    # two-sided p-value via incomplete beta is unavailable without scipy;
    # use large-df normal approximation to the t-distribution (n_eff will
    # typically still be in the hundreds, where t approx normal is fine).
    pvalue = math.erfc(abs(t_stat) / math.sqrt(2.0))
    return {"rho": rho, "r1x": r1x, "r1y": r1y, "n_eff": n_eff, "t": t_stat, "pvalue": pvalue}


def make_controls():
    positive = np.arange(N, dtype=float)
    neg_x = mod._ar1(N, 0.8, 20_260_917)
    neg_y = mod._ar1(N, 0.8, 20_260_918)
    return positive, neg_x, neg_y


def main():
    positive, neg_x, neg_y = make_controls()
    seed = mod.SEED

    print(f"{'method':45s} {'pos p':>12s} {'pos pass':>9s} {'neg p':>12s} {'neg pass':>9s} {'BOTH':>6s}")
    results = {}

    for L in (12, 20, 25, 40):
        pos = block_permutation(positive, positive, seed, L)
        neg = block_permutation(neg_x, neg_y, seed, L)
        pos_pass = pos["pvalue"] < ALPHA
        neg_pass = neg["pvalue"] >= ALPHA
        name = f"block_permutation L={L}"
        results[name] = {"positive": pos, "negative": neg, "both_pass": pos_pass and neg_pass}
        print(f"{name:45s} {pos['pvalue']:>12.5f} {str(pos_pass):>9s} {neg['pvalue']:>12.5f} {str(neg_pass):>9s} {str(pos_pass and neg_pass):>6s}")

    for bw in (12, 20, 25, 40, 60):
        pos = hac_adjusted_spearman(positive, positive, bw)
        neg = hac_adjusted_spearman(neg_x, neg_y, bw)
        pos_pass = pos["pvalue"] < ALPHA
        neg_pass = neg["pvalue"] >= ALPHA
        name = f"HAC-adjusted Spearman bw={bw}"
        results[name] = {"positive": pos, "negative": neg, "both_pass": pos_pass and neg_pass}
        print(f"{name:45s} {pos['pvalue']:>12.5f} {str(pos_pass):>9s} {neg['pvalue']:>12.5f} {str(neg_pass):>9s} {str(pos_pass and neg_pass):>6s}")

    pos = ar1_effective_n_spearman(positive, positive)
    neg = ar1_effective_n_spearman(neg_x, neg_y)
    pos_pass = pos["pvalue"] < ALPHA
    neg_pass = neg["pvalue"] >= ALPHA
    name = "AR(1) n_eff-adjusted Spearman"
    results[name] = {"positive": pos, "negative": neg, "both_pass": pos_pass and neg_pass}
    print(f"{name:45s} {pos['pvalue']:>12.5f} {str(pos_pass):>9s} {neg['pvalue']:>12.5f} {str(neg_pass):>9s} {str(pos_pass and neg_pass):>6s}")
    print()
    print("neg control diagnostics (AR(1) n_eff method):", {k: neg[k] for k in ("r1x", "r1y", "n_eff")})

    import json
    out = Path("/sessions/blissful-focused-lamport/mnt/a/GIA-TIMDR/core/_kitchen_v03_candidate_results.json")
    out.write_text(json.dumps(results, indent=2, default=str))
    print(f"\nsaved: {out}")


if __name__ == "__main__":
    main()
