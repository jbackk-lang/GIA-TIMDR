"""Hell Bridge: regula kierunku + stosunki czestotliwosci (PREREG_HBTA_LATERAL_RATIOS_v0_5).

Kierunek: stezenia wiatrowe (DS5-7) przenosza obciazenia poprzeczne -> wzbudzenie poprzeczne (sweep Y) i czujniki
poprzeczne na pasach dzwigarow (AG, os y, 17 kanalow). Stosunki: temperatura zmienia modul E prawie rowno w calej
stali -> kazda czestotliwosc skaluje sie tym samym czynnikiem sqrt(E(T)/E0); po podzieleniu przez srednia geometryczna
(mediana stosunkow biegunow do referencji) czynnik sie skraca (stereoskopia czestotliwosci), a lokalne uszkodzenie zmienia mody nierowno.
Warianty: bieguny surowe / znormalizowane, zera surowe / znormalizowane (zero / srednia geometryczna biegunow).
Statystyka jak v0.4: mediana wzglednego przesuniecia (DSk vs UDS_01) / to samo dla UDS_02 vs UDS_01.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.signal import coherence, csd, spectrogram, welch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.hbta_modal_anchor import H5  # noqa: E402
from core.hbta_antiresonance import poles_zeros, DEPTH_MIN  # noqa: E402

FS, NPER = 100.0, 4096
AG_Y = [f"AG{i:02d}" for i in range(1, 19) if i != 9]            # AG09 bez osi y
AL_Z = [f"AL{i:02d}" for i in range(1, 41)]
COH_MIN, SEP = 0.8, 0.08
VARIANTS = ("bieguny", "bieguny_norm", "zera", "zera_norm")


def load(name, direction):
    import h5py
    with h5py.File(H5, "r") as f:
        acc = f[name]["acceleration"]
        if direction == "Y":
            X = np.array([acc[n]["y"][:] for n in AG_Y]); a = acc["AS"]["y"][:]
        else:
            X = np.array([acc[n]["z"][:] for n in AL_Z]); a = acc["AS"]["z"][:]
    return X, a


def frf(X, a):
    Xc = X - X.mean(1, keepdims=True); ac = a - a.mean()
    f, Paa = welch(ac, FS, nperseg=NPER); _, Sxa = csd(Xc, ac[None, :], FS, nperseg=NPER)
    return f, Sxa / (Paa[None, :] + 1e-30)


def halves(X, a):
    fr, t, S = spectrogram(a, FS, nperseg=1000, noverlap=0); pk = fr[S.argmax(0)]
    cut = int(t[int(np.argmax(pk * (pk < 60)))] * FS)
    return [(X[:, sl], a[sl]) for sl in (slice(1000, cut), slice(cut, X.shape[1]))]


def select_anchors(name, direction, fmin=2.0, fmax=45.0):
    """Kotwice z rejestracji uczacej: szczyty sum |H|^2 (prominencja 1 w log), koherencja kanalow z wibratorem
    mediana i p10 >= 0,8, zachlannie od najsilniejszego z odstepem >= 8% (miejsce na zero miedzy biegunami)."""
    from scipy.signal import find_peaks
    X, a = load(name, direction); f, H = frf(X, a); S = np.log((np.abs(H) ** 2).sum(0))
    _, C = coherence(X - X.mean(1, keepdims=True), (a - a.mean())[None, :], FS, nperseg=NPER)
    m = np.where((f > fmin) & (f < fmax))[0]; pk, _ = find_peaks(S[m], prominence=1.0); idx = m[pk]
    ok = [j for j in idx if np.median(C[:, j]) >= COH_MIN and np.percentile(C[:, j], 10) >= COH_MIN]
    acc = []
    for j in sorted(ok, key=lambda j: -S[j]):
        if all(abs(f[j] - f[k]) > SEP * min(f[j], f[k]) for k in acc):
            acc.append(j)
    return sorted(float(f[j]) for j in acc)


def depth(P, Z, f, H):
    L = np.log(np.abs(H) + 1e-30); D = np.full(Z.shape, np.nan)
    for k in range(len(P) - 1):
        for i in range(H.shape[0]):
            if np.isfinite(Z[i, k]):
                D[i, k] = 0.5 * (np.interp(P[k], f, L[i]) + np.interp(P[k + 1], f, L[i])) - np.interp(Z[i, k], f, L[i])
    return D


def record(name, direction, anchors):
    out = []
    for Xh, ah in halves(*load(name, direction)):
        f, H = frf(Xh, ah); P, Z = poles_zeros(f, H, anchors); out.append((P, Z, depth(P, Z, f, H)))
    return out


def position(pos, direction, anchors):
    R = {"ref": record(f"MVS_{pos}_UDS_SM_{direction}_01", direction, anchors),
         "nul": record(f"MVS_{pos}_UDS_SM_{direction}_02", direction, anchors)}
    for i in range(1, 9):
        R[f"DS{i}"] = record(f"MVS_{pos}_DS{i}_SM_{direction}_01", direction, anchors)
    P = {k: np.mean([r[0] for r in v], 0) for k, v in R.items()}; Z = {k: np.mean([r[1] for r in v], 0) for k, v in R.items()}
    sel = np.minimum(R["ref"][0][2], R["ref"][1][2]) >= DEPTH_MIN
    # wspolny czynnik skali wzgledem referencji = mediana stosunkow biegunow (odporna na przeskok jednego modu)
    g = {k: float(np.median(P[k] / P["ref"])) for k in P}
    q = {"bieguny": lambda k: P[k], "bieguny_norm": lambda k: P[k] / g[k],
         "zera": lambda k: np.where(sel, Z[k], np.nan), "zera_norm": lambda k: np.where(sel, Z[k] / g[k], np.nan)}
    shift = {v: (lambda k, v=v: float(np.nanmedian(np.abs(q[v](k) - q[v]("ref")) / np.abs(q[v]("ref"))))) for v in VARIANTS}
    out = {"n_zer": int(sel.sum()), "null": {v: shift[v]("nul") for v in VARIANTS}, "DS": {}}
    for i in range(1, 9):
        k = f"DS{i}"; out["DS"][k] = {v: shift[v](k) / shift[v]("nul") for v in VARIANTS}
    return out


# ---------------- zamrozone (PREREG_HBTA_LATERAL_RATIOS_v0_5) ----------------
ANCHORS_Y = [7.23, 8.59, 11.33, 12.52, 14.94, 16.19, 18.63, 20.97, 23.41, 26.22, 29.57, 32.57, 38.4]   # z P2 UDS_01 Y
ANCHORS_Z = [6.86, 7.42, 17.26, 24.12, 30.08, 32.32]


def final():
    res = {"prereg": "PREREG_HBTA_LATERAL_RATIOS_v0_5.md",
           "P1_Y": position("P1", "Y", ANCHORS_Y), "P1_Z": position("P1", "Z", ANCHORS_Z)}
    Y, Z = res["P1_Y"]["DS"], res["P1_Z"]["DS"]; br = ("DS5", "DS6", "DS7"); vt = ("DS1", "DS2")
    mY = float(np.mean([Y[k]["bieguny"] for k in br])); mZ = float(np.mean([Z[k]["bieguny"] for k in br]))
    n = sum(Y[k]["bieguny"] > 1 for k in br); c1, c2 = n >= 2, mY > mZ
    res["H1"] = {"stezenia_Y>null": int(n), "sr_Y": mY, "sr_Z": mZ,
                 "verdict": "SUPPORTED" if c1 and c2 else ("MIXED" if c1 or c2 else "NOT SUPPORTED")}
    vY = float(np.mean([Y[k]["bieguny"] for k in vt])); vZ = float(np.mean([Z[k]["bieguny"] for k in vt]))
    res["H1b"] = {"pionowe_sr_Y": vY, "pionowe_sr_Z": vZ, "verdict": "SUPPORTED" if vY < vZ else "NOT SUPPORTED"}
    cells = {f"{d}_{q}": res[f"P1_{d}"]["null"][f"{q}_norm"] < res[f"P1_{d}"]["null"][q] for d in ("Y", "Z") for q in ("bieguny", "zera")}
    k = sum(cells.values())
    res["H2"] = {"null_norm<null_surowy": cells, "verdict": "SUPPORTED" if k >= 3 else ("MIXED" if k == 2 else "NOT SUPPORTED")}
    p = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_HBTA_LATERAL_RATIOS_v0_5.json"
    p.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = final(); print(json.dumps({k: r[k] for k in ("H1", "H1b", "H2")}, indent=1, ensure_ascii=False))
    for d in ("P1_Y", "P1_Z"):
        print(d, "null", {k: round(v, 4) for k, v in r[d]["null"].items()}, "zer", r[d]["n_zer"])
        for k, v in r[d]["DS"].items():
            print(" ", k, {kk: round(vv, 2) for kk, vv in v.items()})
