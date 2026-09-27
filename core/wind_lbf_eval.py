"""wind_lbf_eval.py -- ocena wg PREREG_WIND_LBF_ORDER_SIEVE_v0.1.
  python core/wind_lbf_eval.py extract <od> <do>   (lista plikow ewaluacyjnych: Healthy, OuterRace, InnerRace, RollerElement)
  python core/wind_lbf_eval.py evaluate"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.stats import mannwhitneyu
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.wind_lbf_io import split, DATA  # noqa: E402
from core.wind_lbf_sieve import segment_rows  # noqa: E402

OUT = DATA / "_eval_v0_1"; RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_WIND_LBF_ORDER_SIEVE_v0.1.json"
EVAL_CLASSES = ("Healthy", "OuterRace", "InnerRace", "RollerElement")


def jobs():
    return [(c, n) for c in EVAL_CLASSES for n in split(c)[1]]


def extract(lo, hi):
    OUT.mkdir(exist_ok=True)
    for i, (c, n) in enumerate(jobs()[lo:hi], start=lo):
        (OUT / f"{i:03d}.json").write_text(json.dumps(segment_rows(c, n)))
        print("ok", i, c, n.split("/")[-1], flush=True)


def auc(pos, neg):
    return float(mannwhitneyu(pos, neg, alternative="two-sided").statistic / (len(pos) * len(neg)))


def evaluate():
    rows = [r for i in range(len(jobs())) for r in json.loads((OUT / f"{i:03d}.json").read_text())]
    g = lambda c, k: [r[k] for r in rows if r["cls"] == c]
    non_or = lambda k: [r[k] for r in rows if r["cls"] != "OuterRace"]
    res = {"prereg": "PREREG_WIND_LBF_ORDER_SIEVE_v0.1.md", "n_segments": {c: len(g(c, "QO_BPFO")) for c in EVAL_CLASSES}}
    a_qo = auc(g("OuterRace", "QO_BPFO"), g("Healthy", "QO_BPFO"))
    sw_qo = auc(g("OuterRace", "QO_BPFO"), non_or("QO_BPFO")); sw_qh = auc(g("OuterRace", "QH_BPFO"), non_or("QH_BPFO"))
    ctrl = auc(g("OuterRace", "QO_BPFI"), g("Healthy", "QO_BPFI"))
    res["H1"] = {"AUC_QO_BPFO_OR_vs_H": a_qo, "verdict": "SUPPORTED" if a_qo >= 0.90 else "NOT SUPPORTED",
                 "day_control_AUC_QO_BPFI": ctrl, "day_control_ok": 0.25 <= ctrl <= 0.75}
    res["H2"] = {"AUC_sw_QO": sw_qo, "AUC_sw_QH": sw_qh, "diff": sw_qo - sw_qh,
                 "verdict": "SUPPORTED" if sw_qo - sw_qh >= 0.10 else "NOT SUPPORTED"}
    res["descriptive"] = {
        "AUC_QH_BPFO_OR_vs_H": auc(g("OuterRace", "QH_BPFO"), g("Healthy", "QH_BPFO")),
        "AUC_QO_BPFI_IR_vs_H": auc(g("InnerRace", "QO_BPFI"), g("Healthy", "QO_BPFI")),
        "AUC_QO_BSF2_RE_vs_H": auc(g("RollerElement", "QO_BSF2"), g("Healthy", "QO_BSF2")),
        "AUC_KURT_OR_vs_H": auc(g("OuterRace", "KURT"), g("Healthy", "KURT")), "AUC_sw_KURT": auc(g("OuterRace", "KURT"), non_or("KURT")),
        "AUC_RMS_OR_vs_H": auc(g("OuterRace", "RMS"), g("Healthy", "RMS")), "AUC_sw_RMS": auc(g("OuterRace", "RMS"), non_or("RMS")),
        "median_QO_BPFO_minus_BPFI_OR": float(np.median(np.array(g("OuterRace", "QO_BPFO")) - np.array(g("OuterRace", "QO_BPFI")))),
        "median_QO_BPFO_minus_BPFI_H": float(np.median(np.array(g("Healthy", "QO_BPFO")) - np.array(g("Healthy", "QO_BPFI"))))}
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print(json.dumps(evaluate(), indent=1))
