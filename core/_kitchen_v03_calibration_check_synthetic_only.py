"""Calibration check across MANY independent AR(1) draws -- SYNTHETIC ONLY.

Motivation: the single-seed-pair negative control (seeds 20260917/20260918)
gave p in [0.012, 0.023] for every candidate method tried in
_kitchen_v03_candidate_methods_synthetic_only.py (block permutation L in
{12,20,25,40}, HAC-adjusted Spearman, AR(1) n_eff-adjusted Spearman) --
none cleared alpha=0.05 on THAT ONE draw. But a single p-value from a
single draw can never distinguish "this method is miscalibrated" from
"this method is fine and this particular draw happened to land in its
(correctly sized) 5% rejection region" -- a valid alpha=0.05 test rejects
a true null 5% of the time BY CONSTRUCTION. The only way to tell these
apart is to look at the empirical false-positive rate across MANY
independent draws.

This script does exactly that for the two closed-form (fast) candidates
-- HAC-adjusted Spearman and AR(1) n_eff-adjusted Spearman -- across many
independent AR(1) draws (phi=0.8, length 1645, same as the frozen
negative-control generator). Block permutation is excluded here purely
for compute-budget reasons (10,000 permutations x many draws does not fit
this session's per-call time budget) -- noted as an open item, not
silently dropped.

Never touches real Kitchen data.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b4_kitchen_run_v0_2 as mod  # noqa: E402
from _kitchen_v03_candidate_methods_synthetic_only import hac_adjusted_spearman, ar1_effective_n_spearman  # noqa: E402

N = 1645
ALPHA = 0.05
N_DRAWS = 300


def main():
    rng_master = np.random.default_rng(42)
    seed_pairs = [(int(a), int(b)) for a, b in rng_master.integers(1, 10_000_000, size=(N_DRAWS, 2))]

    hac_rejects = 0
    aref_rejects = 0
    for sx, sy in seed_pairs:
        x = mod._ar1(N, 0.8, sx)
        y = mod._ar1(N, 0.8, sy)
        if hac_adjusted_spearman(x, y, bandwidth=25)["pvalue"] < ALPHA:
            hac_rejects += 1
        if ar1_effective_n_spearman(x, y)["pvalue"] < ALPHA:
            aref_rejects += 1

    def wilson_ci(k, n, z=1.96):
        p = k / n
        denom = 1 + z**2 / n
        centre = p + z**2 / (2 * n)
        adj = z * ((p * (1 - p) / n + z**2 / (4 * n**2)) ** 0.5)
        return ((centre - adj) / denom, (centre + adj) / denom)

    hac_rate = hac_rejects / N_DRAWS
    aref_rate = aref_rejects / N_DRAWS
    hac_ci = wilson_ci(hac_rejects, N_DRAWS)
    aref_ci = wilson_ci(aref_rejects, N_DRAWS)

    print(f"N_DRAWS={N_DRAWS}, nominal alpha={ALPHA}")
    print(f"HAC-adjusted Spearman (bw=25):     false-positive rate = {hac_rate:.4f} ({hac_rejects}/{N_DRAWS}), 95% CI [{hac_ci[0]:.4f}, {hac_ci[1]:.4f}]")
    print(f"AR(1) n_eff-adjusted Spearman:      false-positive rate = {aref_rate:.4f} ({aref_rejects}/{N_DRAWS}), 95% CI [{aref_ci[0]:.4f}, {aref_ci[1]:.4f}]")
    print()
    print("Interpretation: if 0.05 falls INSIDE the 95% CI, the method's rejection")
    print("rate is statistically consistent with correct calibration at this alpha")
    print("-- the single frozen negative-control draw (p in [0.012,0.023] for all")
    print("methods tried) would then be an unlucky draw, not proof of miscalibration.")

    import json
    out = Path("/sessions/blissful-focused-lamport/mnt/a/GIA-TIMDR/core/_kitchen_v03_calibration_results.json")
    out.write_text(json.dumps({
        "n_draws": N_DRAWS,
        "alpha": ALPHA,
        "hac_bw25": {"rejects": hac_rejects, "rate": hac_rate, "ci95": hac_ci},
        "ar1_neff": {"rejects": aref_rejects, "rate": aref_rate, "ci95": aref_ci},
    }, indent=2))
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
