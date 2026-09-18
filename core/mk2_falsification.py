"""TIMDR M/S<->K #2 — real-data falsification harness.

This is the preregistered analysis pipeline, not a validation result.
It never constructs a modal component to favour the hypothesis. All
omega_1 values are measured from supplied real-data windows.

Input format per domain: NPZ with keys
  signals: float array [n_windows, n_samples]
  time: optional float array [n_samples]
  positive: optional bool [n_windows]  (externally defined, preregistered)
  negative: optional bool [n_windows]  (externally defined, preregistered)
  artifact: optional bool [n_windows] (externally defined or locked rule)

A separate calibration NPZ contains `signals` used ONLY for A_ref.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class Prereg:
    # Frozen analysis choices; replace only before preregistration is frozen.
    fs: float = 100.0
    rel_amp_threshold: float = 0.05
    low_quantile: float = 0.25
    high_quantile: float = 0.75
    eps_fraction_of_aref: float = 0.01
    n_perm: int = 5000
    alpha: float = 0.05
    seed: int = 20260918


def load_npz(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def validate_windows(signals: np.ndarray) -> np.ndarray:
    x = np.asarray(signals, dtype=float)
    if x.ndim != 2:
        raise ValueError("signals must have shape [n_windows, n_samples]")
    if x.shape[0] < 2 or x.shape[1] < 8:
        raise ValueError("not enough windows/samples")
    if not np.isfinite(x).all():
        raise ValueError("signals contain non-finite values")
    return x


def compute_aref(calibration_signals: np.ndarray) -> float:
    """Robust amplitude reference: median RMS of preregistered background windows."""
    x = validate_windows(calibration_signals)
    rms = np.sqrt(np.mean(x * x, axis=1))
    aref = float(np.median(rms))
    if not np.isfinite(aref) or aref <= 0:
        raise ValueError("A_ref must be finite and positive")
    return aref


def x_tilde(x: np.ndarray, aref: float) -> np.ndarray:
    return np.abs(np.mean(x, axis=1)) / aref


def omega1_fft(window: np.ndarray, cfg: Prereg) -> float:
    """First non-DC FFT bin above a locked relative-amplitude threshold."""
    n = window.size
    freqs = np.fft.rfftfreq(n, d=1.0 / cfg.fs)
    amp = np.abs(np.fft.rfft(window))
    mask = freqs > 0.0
    if not np.any(mask):
        raise ValueError("no non-DC bins")
    max_amp = float(np.max(amp[mask]))
    if max_amp <= 0:
        raise ValueError("no non-DC spectral energy")
    candidates = mask & (amp >= cfg.rel_amp_threshold * max_amp)
    idx = np.flatnonzero(candidates)
    if idx.size == 0:
        raise ValueError("no omega_1 candidate passed filter")
    return float(freqs[idx[0]])


def omega1_all(signals: np.ndarray, cfg: Prereg) -> np.ndarray:
    return np.asarray([omega1_fft(row, cfg) for row in signals], dtype=float)


def phase_randomized_surrogate(signals: np.ndarray, seed: int) -> np.ndarray:
    """Preserve each window's DC and spectral magnitudes; randomize non-DC phases."""
    rng = np.random.default_rng(seed)
    out = np.empty_like(signals)
    for i, row in enumerate(signals):
        spec = np.fft.rfft(row)
        if spec.size <= 2:
            out[i] = row
            continue
        phase = rng.uniform(-np.pi, np.pi, spec.size - 2)
        mag = np.abs(spec)
        new_spec = spec.copy()
        new_spec[1:-1] = mag[1:-1] * np.exp(1j * phase)
        # Keep DC and Nyquist exactly; irfft returns real signal.
        out[i] = np.fft.irfft(new_spec, n=row.size)
    return out


def random_pairing(xv: np.ndarray, ov: np.ndarray, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Data-derived null: break x~-omega1 pairing without changing marginals."""
    rng = np.random.default_rng(seed)
    return xv[rng.permutation(xv.size)], ov.copy()


def split_low_high(xv: np.ndarray, ov: np.ndarray, qlo: float, qhi: float) -> tuple[np.ndarray, np.ndarray]:
    lo = np.quantile(xv, qlo)
    hi = np.quantile(xv, qhi)
    low = ov[xv <= lo]
    high = ov[xv >= hi]
    if low.size < 5 or high.size < 5:
        raise ValueError("low/high groups too small; no inference")
    return low, high


def mw_effect(low: np.ndarray, high: np.ndarray) -> dict[str, float]:
    """Tests H1: omega1 is larger in low-x~ windows than high-x~ windows."""
    res = stats.mannwhitneyu(low, high, alternative="greater")
    n1, n2 = low.size, high.size
    mu = n1 * n2 / 2.0
    sd = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12.0)
    if sd == 0:
        r = np.nan
    else:
        z = (res.statistic - mu - 0.5) / sd
        r = z / np.sqrt(n1 + n2)
    return {
        "n_low": int(n1),
        "n_high": int(n2),
        "median_low": float(np.median(low)),
        "median_high": float(np.median(high)),
        "delta_median": float(np.median(low) - np.median(high)),
        "U": float(res.statistic),
        "p_one_sided": float(res.pvalue),
        "r": float(r),
    }


def spearman_strength(xv: np.ndarray, ov: np.ndarray) -> dict[str, float]:
    rho, p = stats.spearmanr(xv, ov)
    return {"rho": float(rho), "p_two_sided": float(p)}


def permutation_strength(xv: np.ndarray, ov: np.ndarray, cfg: Prereg) -> dict[str, float]:
    """Permutation null for the observed Spearman association."""
    observed = abs(float(stats.spearmanr(xv, ov).statistic))
    rng = np.random.default_rng(cfg.seed)
    ge = 0
    for _ in range(cfg.n_perm):
        rho = abs(float(stats.spearmanr(xv[rng.permutation(xv.size)], ov).statistic))
        ge += rho >= observed
    return {"abs_rho_observed": observed, "perm_p": (ge + 1) / (cfg.n_perm + 1)}


def control_report(signals: np.ndarray, cfg: Prereg, aref: float) -> dict:
    xv = x_tilde(signals, aref)
    ov = omega1_all(signals, cfg)
    low, high = split_low_high(xv, ov, cfg.low_quantile, cfg.high_quantile)
    result = {
        "n": int(signals.shape[0]),
        "x_tilde_summary": {
            "median": float(np.median(xv)),
            "q25": float(np.quantile(xv, 0.25)),
            "q75": float(np.quantile(xv, 0.75)),
        },
        "omega1_summary_hz": {
            "median": float(np.median(ov)),
            "q25": float(np.quantile(ov, 0.25)),
            "q75": float(np.quantile(ov, 0.75)),
        },
        "primary_mw": mw_effect(low, high),
        "association": spearman_strength(xv, ov),
        "association_permutation": permutation_strength(xv, ov, cfg),
    }
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", required=True, type=Path)
    ap.add_argument("--domain", action="append", nargs=2, metavar=("NAME", "NPZ"), required=True)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    cfg = Prereg()
    cal = load_npz(args.calibration)
    aref = compute_aref(cal["signals"])
    eps = cfg.eps_fraction_of_aref

    report: dict = {
        "status": "analysis_harness_only_no_result_until_real_data_supplied",
        "prereg": asdict(cfg),
        "A_ref": aref,
        "epsilon": eps,
        "domains": {},
    }

    for name, path_s in args.domain:
        data = load_npz(Path(path_s))
        x = validate_windows(data["signals"])
        base = control_report(x, cfg, aref)

        # Baseline 1: random pairing of observed x~ with observed omega_1.
        xv = x_tilde(x, aref)
        ov = omega1_all(x, cfg)
        xv_perm, _ = random_pairing(xv, ov, cfg.seed)
        base["random_pairing_baseline"] = {
            "association": spearman_strength(xv_perm, ov),
            "permutation_strength": permutation_strength(xv_perm, ov, cfg),
        }

        # Baseline 2: preserve each window's modal spectrum but destroy phase.
        x_phase = phase_randomized_surrogate(x, cfg.seed)
        base["phase_randomized_modality_preserved"] = control_report(x_phase, cfg, aref)

        # Baseline 3: naturally flagged artifact windows, never injected here.
        if "artifact" in data:
            artifact = np.asarray(data["artifact"], dtype=bool)
            if artifact.shape != (x.shape[0],):
                raise ValueError(f"{name}: artifact mask has wrong shape")
            if artifact.sum() >= 5 and (~artifact).sum() >= 5:
                art = control_report(x[artifact], cfg, aref)
                clean = control_report(x[~artifact], cfg, aref)
                base["artifact_vs_clean"] = {"artifact": art, "clean": clean}
            else:
                base["artifact_vs_clean"] = {"status": "insufficient_flagged_windows"}
        else:
            base["artifact_vs_clean"] = {"status": "no_external_artifact_mask_supplied"}

        # Baseline 4: DC leakage audit — omega_1 must not depend on whether DC is removed.
        x_demeaned = x - np.mean(x, axis=1, keepdims=True)
        ov_dc = omega1_all(x, cfg)
        ov_demean = omega1_all(x_demeaned, cfg)
        base["dc_leakage_audit"] = {
            "fraction_same_omega1": float(np.mean(ov_dc == ov_demean)),
            "median_abs_delta_hz": float(np.median(np.abs(ov_dc - ov_demean))),
        }

        # Explicit controls must be externally defined before analysis.
        for key in ("positive", "negative"):
            if key in data:
                mask = np.asarray(data[key], dtype=bool)
                if mask.shape != (x.shape[0],):
                    raise ValueError(f"{name}: {key} mask has wrong shape")
                if mask.sum() >= 5:
                    base[key + "_control"] = control_report(x[mask], cfg, aref)
                else:
                    base[key + "_control"] = {"status": "insufficient_windows"}
            else:
                base[key + "_control"] = {"status": "missing_preregistered_external_mask"}

        report["domains"][name] = base

    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
