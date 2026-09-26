"""POST-HOC (po jednorazowej ocenie): bootstrap po pomiarach testowych dla sredniego zysku BT-B w obrebie warunku.
Nie zmienia werdyktu."""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_paderborn_vibration_complement import FEAT, CONDS, SEED, _REPO
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1
recs = [json.loads((FEAT / f"{k:03d}.json").read_text()) for k in range(192)]
rows = [(r["cond"], r["split"], r["cls"], i, f) for i, r in enumerate(recs) for f in r["features"]]
names = list(rows[0][4]); B = [n for n in names if n.startswith("B_")]; BT = names
cond = np.array([r[0] for r in rows]); spl = np.array([r[1] for r in rows]); y = np.array([r[2] for r in rows]); mid = np.array([r[3] for r in rows])
def Xn(cols):
    X = np.array([[r[4][n] for n in cols] for r in rows], float)
    for c in CONDS:
        m = cond == c; X[m] = (X[m] - X[m].mean(0)) / (X[m].std(0) + 1e-12)
    return X
XB, XBT = Xn(B), Xn(BT); pred = {}
for c in CONDS:
    tr = (cond == c) & (spl == "train"); te = np.where((cond == c) & (spl == "calibration"))[0]
    pred[c] = (te, lda_predict(lda_fit(XB[tr], y[tr]), XB[te]), lda_predict(lda_fit(XBT[tr], y[tr]), XBT[te]))
rng = np.random.default_rng(SEED); boots = []
for _ in range(2000):
    g = []
    for c in CONDS:
        te, pb, pbt = pred[c]; ms = np.unique(mid[te]); pick = rng.choice(ms, len(ms), replace=True)
        idx = np.concatenate([np.where(mid[te] == m)[0] for m in pick])
        g.append(macro_f1(y[te][idx], pbt[idx]) - macro_f1(y[te][idx], pb[idx]))
    boots.append(np.mean(g))
lo, hi = np.percentile(boots, [2.5, 97.5])
out = {"bootstrap_mean_gain_ci95": [float(lo), float(hi)], "p_gain_le_0": float(np.mean(np.array(boots) <= 0)),
       "n_test_measurements": int(len(np.unique(mid[spl == "calibration"])))}
(_REPO / "docs/geometry/POSTHOC_PADERBORN_VIBRATION_COMPLEMENT_v0.1.json").write_text(json.dumps(out, indent=1))
print(out)
