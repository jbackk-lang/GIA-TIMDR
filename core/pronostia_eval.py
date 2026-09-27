"""Ocena PRONOSTIA v0.1 (PREREG_PRONOSTIA_REGIME_PATH_v0_1): trajektoria rezimu wzdluz zycia lozyska."""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
from scipy.ndimage import median_filter
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import pronostia_io as pio  # noqa: E402

KEYS = ["rms", "kurt", "P", "D", "Q", "K"]
RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_PRONOSTIA_REGIME_PATH_v0_1.json"


def bearing_stats(b, ch="h"):
    R = json.loads((pio.DATA / "_features_v0_1" / f"{b}.json").read_text()); n = len(R); t = np.arange(n)
    rho = {k: float(spearmanr(t, median_filter(np.array([r[ch][k] for r in R]), 15)).correlation) for k in KEYS}
    D = median_filter(np.array([r[ch]["D"] for r in R]), 15); e = max(3, int(0.03 * n))
    return {"n": n, "rho": rho, "D_end_over_min": float(D[-e:].mean() / D.min())}


def evaluate(bearings):
    S = {b: bearing_stats(b) for b in bearings}
    med = lambda k: float(np.median([S[b]["rho"][k] for b in bearings]))
    negD = float(np.median([-S[b]["rho"]["D"] for b in bearings]))
    out = {"per_bearing": S, "median_rho": {k: med(k) for k in KEYS}, "median_minus_rho_D": negD}
    n1 = sum(S[b]["rho"]["D"] <= -0.3 for b in bearings)
    n3 = sum(S[b]["D_end_over_min"] >= 1.2 for b in bearings)
    out["H1"] = {"n_ok": int(n1), "n": len(bearings), "verdict": "SUPPORTED" if n1 >= 8 else "NOT SUPPORTED"}
    out["H2"] = {"minus_rho_D": negD, "rho_RMS": med("rms"), "verdict": "SUPPORTED" if negD > med("rms") else "NOT SUPPORTED",
                 "vs_kurt": {"rho_kurt": med("kurt"), "tie_pred_abs_diff_lt_0.1": abs(negD - med("kurt")) < 0.1}}
    out["H3"] = {"n_ok": int(n3), "n": len(bearings), "verdict": "SUPPORTED" if n3 >= 6 else "NOT SUPPORTED"}
    out["H4"] = {"rho_Q": med("Q"), "minus_rho_D": negD, "verdict": "SUPPORTED" if med("Q") < negD else "NOT SUPPORTED"}
    return out


if __name__ == "__main__":
    which = sys.argv[1]
    r = evaluate(pio.DEV if which == "dev" else pio.EVAL)
    if which == "eval":
        r["prereg"] = "PREREG_PRONOSTIA_REGIME_PATH_v0_1.md"; RESULT.write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: r[k] for k in ("median_rho", "H1", "H2", "H3", "H4")}, indent=1, ensure_ascii=False))
