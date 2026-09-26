"""POST-HOC (po jednorazowej ocenie v0.1) -- nie zmienia werdyktu, tylko sprawdza, czym jest wynik.
python core/real_seu_multichannel_posthoc.py"""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_seu_multichannel_bridge import FEAT_DIR, CLASSES, CONDS, lda_fit, lda_predict, macro_f1, _REPO

data = {(c, d): json.loads((FEAT_DIR / f"{c}_{d}.json").read_text(encoding="utf-8"))["features"] for c in CLASSES for d in CONDS}
names = list(data[("health", "20_0")][0])

def mat(cond, cols):
    X = np.asarray([[f[n] for n in cols] for c in CLASSES for f in data[(c, cond)]], float)
    return X, np.repeat(np.arange(5), 100)

def run(cols, per_cond_std=False):
    out = {}
    for a, b in (("20_0", "30_2"), ("30_2", "20_0")):
        Xa, ya = mat(a, cols); Xb, yb = mat(b, cols)
        if per_cond_std:  # kazdy warunek standaryzowany wlasnymi statystykami (bez etykiet)
            Xa = (Xa - Xa.mean(0)) / (Xa.std(0) + 1e-12); Xb = (Xb - Xb.mean(0)) / (Xb.std(0) + 1e-12)
        m = lda_fit(Xa, ya); yp = lda_predict(m, Xb)
        cm = np.zeros((5, 5), int)
        for t, p in zip(yb, yp): cm[t, p] += 1
        out[f"{a}->{b}"] = {"f1": round(macro_f1(yb, yp), 3), "confusion": cm.tolist()}
    return out

B = [n for n in names if n.startswith("B_")]; T = [n for n in names if n.startswith("T_")]
res = {
 "B_bez_std": run([n for n in B if not n.startswith("B_std")]),
 "B_std_per_warunek": run(B, True),
 "T_std_per_warunek": run(T, True),
 "BT_std_per_warunek": run(B + T, True),
 "tylko_T_conc": run(["T_conc"]),
 "tylko_srednie_abs_r": run(["X_mean_abs_r"]),
 "T_bez_conc": run([n for n in T if n != "T_conc"]),
 "T_confusion": run(T),
}
(_REPO / "docs/geometry/POSTHOC_SEU_MULTICHANNEL_v0.1.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
for k, v in res.items():
    print(k, {d: x["f1"] for d, x in v.items()})
print("T confusion (wiersze prawdziwe", CLASSES, ")")
for d, x in res["T_confusion"].items(): print(d, x["confusion"])
for d, x in res["tylko_T_conc"].items(): print("conc", d, x["confusion"])
