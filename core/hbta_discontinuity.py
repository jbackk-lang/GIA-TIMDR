"""Lokalne uszkodzenie = przerwanie ciaglosci (PREREG_HBTA_DISCONTINUITY_v0_3). Sciezka K -> G -> M/S:
K: kotwica + faza wzgledem wibratora -> G: ksztalt modu na siatce 4 podluznic x 10 punktow -> M/S: 'defekt = skok' w przestrzeni.
(a) wzdluz linii: odchylka punktu od gladkiej kubicznej interpolacji z sasiadow i+-1, i+-2 (gapped smoothing, Ratcliffe);
(b) w poprzek: roznica ksztaltu miedzy sasiednimi podluznicami w tym samym x (zerwana wspolbieznosc).
Cecha = MAKSIMUM (nie suma) z-score zmiany wzgledem uczenia po polozeniach, dla kazdej kotwicy -- osobliwosc, nie srednia.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_lanl_3story_bridge import novelty, auc  # noqa: E402
from core.hbta_modal_anchor import TRAIN, UND_TEST, DAMAGED  # noqa: E402
from core.hbta_modal_curvature import ANCH, record, grid_order  # noqa: E402

RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_HBTA_DISCONTINUITY_v0_3.json"


def along(G):
    """Odchylka od kubicznej interpolacji z sasiadow (rowny rozstaw): psi_i - (-p[i-2] + 4p[i-1] + 4p[i+1] - p[i+2]) / 6."""
    return G[:, 2:-2] - (-G[:, :-4] + 4 * G[:, 1:-3] + 4 * G[:, 3:-1] - G[:, 4:]) / 6


def across(G):
    return G[1:, :] - G[:-1, :]


def final():
    tr, pos = record(TRAIN); grid, h = grid_order(pos)
    ref = np.mean([r["shape"] for r in tr], 0)
    def align(sh):
        s = sh.copy()
        for k in range(len(ANCH)):
            if np.dot(s[k], ref[k]) < 0:
                s[k] = -s[k]
        return s
    def maps(rows):                       # (okna, kotwice, ...)
        A, C = [], []
        for r in rows:
            sh = align(r["shape"]); A.append([along(sh[k][grid]) for k in range(len(ANCH))]); C.append([across(sh[k][grid]) for k in range(len(ANCH))])
        return np.array(A), np.array(C)
    Atr, Ctr = maps(tr)
    stats = {}
    for key, M in (("a", Atr), ("c", Ctr)):
        med = np.median(M, 0); mad = 1.4826 * np.median(np.abs(M - med), 0) + 1e-9; stats[key] = (med, mad)
    def feats(A, C):
        za = np.abs((A - stats["a"][0]) / stats["a"][1]); zc = np.abs((C - stats["c"][0]) / stats["c"][1])
        fa = za.reshape(len(A), len(ANCH), -1).max(2); fc = zc.reshape(len(C), len(ANCH), -1).max(2)
        return fa, fc, za, zc
    fa_tr, fc_tr, _, _ = feats(Atr, Ctr)
    und, _ = record(UND_TEST); fa_u, fc_u, _, _ = feats(*maps(und))
    sets_tr = {"ALONG": fa_tr, "ACROSS": fc_tr, "DISC": np.hstack([fa_tr, fc_tr])}
    sets_u = {"ALONG": fa_u, "ACROSS": fc_u, "DISC": np.hstack([fa_u, fc_u])}
    res = {"prereg": "PREREG_HBTA_DISCONTINUITY_v0_3.md", "auc": {}, "loc": {}}
    xs = np.sort(np.unique(np.round(pos[:, 0], 2)))
    for name in DAMAGED:
        R, _ = record(name); A, C = maps(R); fa, fc, za, zc = feats(A, C); ds = name.split("_")[2]
        s = {"ALONG": fa, "ACROSS": fc, "DISC": np.hstack([fa, fc])}
        res["auc"][ds] = {k: auc(novelty(sets_tr[k], sets_u[k]), novelty(sets_tr[k], s[k])) for k in s}
        mc = zc.mean((0, 1))                              # (pary linii, x)
        i, j = np.unravel_index(int(np.argmax(mc)), mc.shape)
        res["loc"][ds] = {"para_linii": int(i), "x_m": float(xs[j]), "z": float(mc[i, j])}
    allds = [f"DS{i}" for i in range(1, 9)]; mean = lambda k, ds: float(np.mean([res["auc"][d][k] for d in ds]))
    res["mean_auc"] = {k: mean(k, allds) for k in ("ALONG", "ACROSS", "DISC")}
    ref_v02 = {"AR": 0.8016666666666666, "SHAPE_DS12": (0.8088888888888889 + 0.9333333333333333) / 2}
    res["ref_v0_2"] = ref_v02
    res["H1"] = "SUPPORTED" if res["mean_auc"]["DISC"] > ref_v02["AR"] else "NOT SUPPORTED"
    res["H2"] = {"DISC_DS12": mean("DISC", ["DS1", "DS2"]), "SHAPE_DS12": ref_v02["SHAPE_DS12"],
                 "verdict": "SUPPORTED" if mean("DISC", ["DS1", "DS2"]) > ref_v02["SHAPE_DS12"] else "NOT SUPPORTED"}
    res["H3"] = "SUPPORTED" if res["mean_auc"]["ACROSS"] > res["mean_auc"]["ALONG"] else "NOT SUPPORTED"
    RESULT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = final(); print(json.dumps({k: r[k] for k in ("auc", "mean_auc", "H1", "H2", "H3", "loc")}, indent=1))
