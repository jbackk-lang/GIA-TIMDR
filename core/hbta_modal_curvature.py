"""Most K<->G: ksztalt modu z faza + krzywizna (PREREG_HBTA_MODAL_CURVATURE_v0_2).

K: kotwica f_k (samokorekta +-4%) i widmo wzajemne kazdego kanalu z sila/przyspieszeniem wibratora (AS) -> H_i = S_iA / S_AA.
Przejscie K->G: faza H_i daje znak -> rzeczywisty ksztalt psi_k = Re(H e^{-i theta}), theta maksymalizuje czesc rzeczywista.
G: siatka 4 podluznic x 10 punktow (AL01-AL40, rozstaw 3,5 m) -> krzywizna kappa = druga roznica wzdluz podluznicy / h^2.
Cechy: CDI_k = sum|kappa_k - kappa0_k| / sum|kappa0_k| (kappa0 = srednia uczenia) dla kotwic z koherencja >= 0,8.
Odniesienia w tym samym przebiegu: AR(5) jak v0.1; ksztalt z faza bez krzywizny (1 - MAC).
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.signal import csd, welch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_lanl_3story_bridge import novelty, auc  # noqa: E402
from core.hbta_modal_anchor import H5, FS, WIN, TRAIN, UND_TEST, DAMAGED, ar_coefs  # noqa: E402

ANCH_ALL = [6.86, 7.42, 9.40, 12.79, 17.26, 24.12, 30.08, 32.32]
ANCH = [6.86, 7.42, 17.26, 24.12, 30.08, 32.32]      # koherencja AL-AS >= 0,8 (mediana i p10) na UDS_01 -- regula wykonalnosci
AL = [f"AL{i:02d}" for i in range(1, 41)]
RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_HBTA_MODAL_CURVATURE_v0_2.json"


def load(name):
    import h5py
    with h5py.File(H5, "r") as f:
        acc = f[name]["acceleration"]
        pos = np.array([np.asarray(acc[n].attrs["position"]).ravel() for n in AL])
        X = np.array([acc[n]["z"][:] for n in AL]); a = acc["AS"]["z"][:]
    return X, a, pos


def grid_order(pos):
    """Indeksy kanalow ulozone w siatke [linia podluznicy (y), x rosnaco]."""
    ys = sorted(set(np.round(pos[:, 1], 2))); out = []
    for y in ys:
        idx = np.where(np.round(pos[:, 1], 2) == y)[0]; out.append(idx[np.argsort(pos[idx, 0])])
    return np.array(out), float(np.median(np.diff(np.sort(np.unique(np.round(pos[:, 0], 2))))))


def window_shapes(Xw, aw):
    f, Paa = welch(aw - aw.mean(), FS, nperseg=2048)
    _, P = welch(Xw - Xw.mean(1, keepdims=True), FS, nperseg=2048)
    S = (P / np.median(P, 1, keepdims=True)).mean(0)
    _, Sxa = csd(Xw - Xw.mean(1, keepdims=True), (aw - aw.mean())[None, :], FS, nperseg=2048)
    shapes, freqs = [], []
    for a in ANCH:
        m = np.where(np.abs(f - a) <= 0.04 * a)[0]; j = m[np.argmax(S[m])]
        H = Sxa[:, j] / (Paa[j] + 1e-30)
        th = 0.5 * np.angle(np.sum(H ** 2)); psi = np.real(H * np.exp(-1j * th))
        shapes.append(psi / (np.linalg.norm(psi) + 1e-30)); freqs.append(f[j])
    return np.array(shapes), np.array(freqs)


def record(name):
    X, a, pos = load(name); rows = []
    for s in range(0, X.shape[1] - WIN + 1, WIN):
        sh, fr = window_shapes(X[:, s:s + WIN], a[s:s + WIN])
        rows.append({"shape": sh, "f": fr, "ar": np.concatenate([ar_coefs(c) for c in X[:, s:s + WIN]])})
    return rows, pos


def curvature(sh, grid, h):
    G = sh[grid]                                   # (linie, x)
    return (G[:, 2:] - 2 * G[:, 1:-1] + G[:, :-2]) / h ** 2


def final():
    tr, pos = record(TRAIN); grid, h = grid_order(pos)
    ref = np.mean([r["shape"] for r in tr], 0)
    def align(sh):                                  # znak ksztaltu wzgledem sredniej uczenia
        s = sh.copy()
        for k in range(len(ANCH)):
            if np.dot(s[k], ref[k]) < 0:
                s[k] = -s[k]
        return s
    for r in tr:
        r["shape"] = align(r["shape"])
    ref = np.mean([r["shape"] for r in tr], 0); ref = ref / np.linalg.norm(ref, axis=1, keepdims=True)
    k0 = np.array([curvature(ref[k], grid, h) for k in range(len(ANCH))])
    def feats(rows):
        C, M = [], []
        for r in rows:
            sh = align(r["shape"])
            C.append([np.abs(curvature(sh[k], grid, h) - k0[k]).sum() / np.abs(k0[k]).sum() for k in range(len(ANCH))])
            M.append([1 - np.dot(sh[k], ref[k]) ** 2 for k in range(len(ANCH))])
        return np.array(C), np.array(M)
    Ctr, Mtr = feats(tr)
    Atr = np.array([r["ar"] for r in tr]); mu = Atr.mean(0); _, _, Vt = np.linalg.svd(Atr - mu, full_matrices=False); V = Vt[:10].T
    ar = lambda R: (np.array([r["ar"] for r in R]) - mu) @ V
    und, _ = record(UND_TEST); Cu, Mu = feats(und)
    res = {"prereg": "PREREG_HBTA_MODAL_CURVATURE_v0_2.md", "anchors": ANCH, "grid": grid.tolist(), "h_m": h, "auc": {}, "loc_x_max_dkappa": {}}
    xs = np.sort(np.unique(np.round(pos[:, 0], 2)))[1:-1]
    for name in DAMAGED:
        R, _ = record(name); C, M = feats(R); ds = name.split("_")[2]
        res["auc"][ds] = {"CURV": auc(novelty(Ctr, Cu), novelty(Ctr, C)), "SHAPE": auc(novelty(Mtr, Mu), novelty(Mtr, M)),
                          "AR": auc(novelty(ar(tr), ar(und)), novelty(ar(tr), ar(R)))}
        dk = np.mean([np.abs(curvature(align(r["shape"])[k], grid, h) - k0[k]) for r in R for k in range(len(ANCH))], 0)  # (linie, x)
        res["loc_x_max_dkappa"][ds] = float(xs[int(np.argmax(dk.sum(0)))])
    allds = [f"DS{i}" for i in range(1, 9)]; mean = lambda key, ds: float(np.mean([res["auc"][d][key] for d in ds]))
    res["mean_auc"] = {k: mean(k, allds) for k in ("CURV", "SHAPE", "AR")}
    res["H1"] = "SUPPORTED" if res["mean_auc"]["CURV"] > res["mean_auc"]["AR"] else "NOT SUPPORTED"
    res["H2"] = "SUPPORTED" if res["mean_auc"]["CURV"] >= 0.65 + 0.10 else "NOT SUPPORTED"
    vert, brace = ["DS1", "DS2", "DS3", "DS4", "DS8"], ["DS5", "DS6", "DS7"]
    res["H3"] = {"vertical": mean("CURV", vert), "bracing": mean("CURV", brace),
                 "verdict": "SUPPORTED" if mean("CURV", vert) > mean("CURV", brace) else "NOT SUPPORTED"}
    RESULT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = final(); print(json.dumps({k: r[k] for k in ("auc", "mean_auc", "H1", "H2", "H3", "loc_x_max_dkappa")}, indent=1))
