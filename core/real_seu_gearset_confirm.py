"""real_seu_gearset_confirm.py -- PREREG_SEU_GEARSET_CONFIRM_v0.2.
  python core/real_seu_gearset_confirm.py extract <Plik bez .csv>
  python core/real_seu_gearset_confirm.py evaluate"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import core.real_seu_multichannel_bridge as v1  # noqa: E402

v1.DATA = Path(os.environ.get("SEU_GEAR_DATA", v1._REPO.parent / "DATA" / "seu_gearset"))
FEAT = v1.DATA / "_features_v0_2"
RESULT = v1._REPO / "docs" / "geometry" / "RESULT_SEU_GEARSET_CONFIRM_v0.2.json"
CLASSES = ("Health", "Chipped", "Miss", "Root", "Surface")
CONDS = ("20_0", "30_2")


def extract(name):
    X = v1.load(name)
    starts = np.round(np.linspace(0, len(X) - v1.W, v1.N_WIN)).astype(int)
    feats = [v1.window_features(X[s:s + v1.W][:, v1.CHANNELS]) for s in starts]
    FEAT.mkdir(exist_ok=True)
    (FEAT / f"{name}.json").write_text(json.dumps({"sha256": v1.sha256(v1.DATA / f"{name}.csv"), "n_rows": int(len(X)),
                                                    "features": feats}), encoding="utf-8")
    print(name, len(X))


def evaluate():
    data = {(c, d): json.loads((FEAT / f"{c}_{d}.json").read_text(encoding="utf-8")) for c in CLASSES for d in CONDS}
    names = list(data[("Health", "20_0")]["features"][0])
    B = [n for n in names if n.startswith("B_")]; T = [n for n in names if n.startswith("T_")]
    sets = {"B": B, "T": T, "BT": B + T, "B+topo": B + [n for n in T if n != "T_conc"]}

    def mat(cond, cols, idx=slice(None), percond=True):
        X = np.array([[f[n] for n in cols] for c in CLASSES for f in data[(c, cond)]["features"][idx]], float)
        y = np.repeat(np.arange(5), len(data[("Health", cond)]["features"][idx]))
        if percond:
            X = (X - X.mean(0)) / (X.std(0) + 1e-12)
        return X, y
    res = {"prereg": "PREREG_SEU_GEARSET_CONFIRM_v0.2.md",
           "files": {f"{c}_{d}": {"sha256": v["sha256"], "n_rows": v["n_rows"]} for (c, d), v in data.items()},
           "gate_synthetic": v1.gate()}
    rng = np.random.default_rng(v1.PERM_SEED); f1 = {}; neg = {}
    for a, b in (("20_0", "30_2"), ("30_2", "20_0")):
        k = f"{a}->{b}"; f1[k] = {}
        for s, cols in sets.items():
            Xa, ya = mat(a, cols); Xb, yb = mat(b, cols)
            f1[k][s] = v1.macro_f1(yb, v1.lda_predict(v1.lda_fit(Xa, ya), Xb))
        Xa, ya = mat(a, sets["BT"]); Xb, yb = mat(b, sets["BT"])
        neg[k] = v1.macro_f1(yb, v1.lda_predict(v1.lda_fit(Xa, rng.permutation(ya)), Xb))
    g = [f1[k]["BT"] - f1[k]["B"] for k in f1]
    if all(f1[k]["B"] >= 0.97 for k in f1):
        verdict = "INCONCLUSIVE (sufit)"
    elif np.mean(g) >= 0.05 and all(x > 0 for x in g):
        verdict = "SUPPORTED"
    elif np.mean(g) <= 0:
        verdict = "NOT SUPPORTED"
    else:
        verdict = "MIESZANY"
    res["negative_control"] = {"f1": neg, "passed": all(v <= 0.35 for v in neg.values())}
    res["f1"] = f1; res["gain_BT_minus_B"] = g; res["mean_gain"] = float(np.mean(g))
    res["within_condition"] = {c: {s: v1.macro_f1(*(lambda tr, te: (te[1], v1.lda_predict(v1.lda_fit(*tr), te[0])))(
        mat(c, cols, slice(0, 50)), mat(c, cols, slice(50, 100)))) for s, cols in sets.items()} for c in CONDS}
    ok = res["gate_synthetic"]["passed"] and res["negative_control"]["passed"]
    res["verdict"] = verdict if ok else "INCONCLUSIVE (kontrole)"
    RESULT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract(sys.argv[2])
    else:
        r = evaluate(); print(json.dumps({k: r[k] for k in ("negative_control", "f1", "gain_BT_minus_B", "mean_gain", "within_condition", "verdict")}, indent=1))
