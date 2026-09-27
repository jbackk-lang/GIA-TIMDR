"""Antyrezonanse (zera funkcji przenoszenia) jako lokalny slad uszkodzenia -- Hell Bridge Test Arena.

Fizyka: rezonanse (bieguny FRF) sa globalne -- te same w kazdym punkcie; antyrezonanse (zera H_i = S_iA/S_AA) powstaja
z wygaszania sie modow i zaleza od miejsca pomiaru i wzbudzenia -> sa lokalne i przy lokalnym uszkodzeniu przesuwaja
sie mocniej niz bieguny. Galaz K od strony zer; cecha jak w przerwie ciaglosci: MAKSIMUM |z| przesuniecia po czujnikach.
Kotwice (bieguny) z rejestracji uczacej; zero_i,k = minimum |H_i| miedzy sasiednimi kotwicami k, k+1 (interpolacja
paraboliczna w log). Odniesienie: bieguny (przesuniecie kotwic, jak v0.1) na tych samych oknach.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from scipy.signal import csd, welch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.hbta_modal_anchor import H5  # noqa: E402

AL = [f"AL{i:02d}" for i in range(1, 41)]
FS = 100.0


def load(name):
    import h5py
    with h5py.File(H5, "r") as f:
        acc = f[name]["acceleration"]
        X = np.array([acc[n]["z"][:] for n in AL]); a = acc["AS"]["z"][:]
    return X, a


def frf(X, a, nperseg=2048):
    Xc = X - X.mean(1, keepdims=True); ac = a - a.mean()
    f, Paa = welch(ac, FS, nperseg=nperseg); _, Sxa = csd(Xc, ac[None, :], FS, nperseg=nperseg)
    return f, Sxa / (Paa[None, :] + 1e-30)


def _parab(y, j):
    if 0 < j < len(y) - 1:
        y0, y1, y2 = y[j - 1:j + 2]; return 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
    return 0.0


def poles_zeros(f, H, anchors, tol=0.04):
    """Bieguny: szczyt sumy |H|^2 po czujnikach w +-4% kotwicy. Zera: minimum log|H_i| miedzy kolejnymi biegunami
    (z marginesem 10% odstepu od biegunow). Zwraca (bieguny[K], zera[czujniki, K-1])."""
    S = (np.abs(H) ** 2).sum(0); df = f[1] - f[0]; P = []
    for a in anchors:
        m = np.where(np.abs(f - a) <= tol * a)[0]; j = m[np.argmax(S[m])]
        P.append(f[j] + _parab(np.log(S), j) * df)
    L = np.log(np.abs(H) + 1e-30); Z = np.zeros((H.shape[0], len(P) - 1))
    for k in range(len(P) - 1):
        g = 0.1 * (P[k + 1] - P[k]); m = np.where((f > P[k] + g) & (f < P[k + 1] - g))[0]
        if len(m) < 3:                                  # bieguny zbyt blisko: brak zera do wyznaczenia
            Z[:, k] = np.nan; continue
        for i in range(H.shape[0]):
            j = m[np.argmin(L[i, m])]; Z[i, k] = f[j] + _parab(-L[i], j) * df
    return np.array(P), Z


# ---------------- rejestracje sweep (SM): FRF z przemiatania sinusem, zamrozone w PREREG_HBTA_ANTIRESONANCE_v0_4 ----------------
DEPTH_MIN = 2.0          # zero wybrane, gdy log|H| w zerze jest >= 2 ponizej sredniej log|H| przy biegunach (oba sweepy ref)
NPER_SM = 4096           # 41 s, rozdzielczosc 0,024 Hz


def sweep_halves(name):
    """Rejestracja SM = przemiatanie w gore (2 -> ~48 Hz) i w dol. Zawrocenie = szczyt czestotliwosci chwilowej wibratora."""
    from scipy.signal import spectrogram
    X, a = load(name)
    fr, t, S = spectrogram(a, FS, nperseg=1000, noverlap=0); pk = fr[S.argmax(0)]
    cut = int(t[int(np.argmax(pk * (pk < 60)))] * FS); out = []
    for sl in (slice(1000, cut), slice(cut, X.shape[1])):
        f, H = frf(X[:, sl], a[sl], nperseg=NPER_SM); P, Z = poles_zeros(f, H, ANCHORS_SM); out.append((P, Z, f, H))
    return out


ANCHORS_SM = [6.86, 7.42, 17.26, 24.12, 30.08, 32.32]      # kotwice z reguly koherencji (PREREG_HBTA_MODAL_CURVATURE_v0_2)


def zero_depth(r):
    P, Z, f, H = r; L = np.log(np.abs(H) + 1e-30); D = np.full(Z.shape, np.nan)
    for k in range(len(P) - 1):
        for i in range(H.shape[0]):
            if np.isfinite(Z[i, k]):
                lp = 0.5 * (np.interp(P[k], f, L[i]) + np.interp(P[k + 1], f, L[i])); D[i, k] = lp - np.interp(Z[i, k], f, L[i])
    return D


def position_result(pos):
    """Dla pozycji wibratora: stosunek przesuniecia (DSk vs UDS_01) do przesuniecia (UDS_02 vs UDS_01), osobno dla zer
    (mediana wzglednego przesuniecia po wybranych zerach) i biegunow (mediana wzglednego przesuniecia biegunow)."""
    R = {"ref": sweep_halves(f"MVS_{pos}_UDS_SM_Z_01"), "nul": sweep_halves(f"MVS_{pos}_UDS_SM_Z_02")}
    for i in range(1, 9):
        R[f"DS{i}"] = sweep_halves(f"MVS_{pos}_DS{i}_SM_Z_01")
    Pm = {k: np.mean([r[0] for r in v], 0) for k, v in R.items()}; Zm = {k: np.mean([r[1] for r in v], 0) for k, v in R.items()}
    sel = np.minimum(zero_depth(R["ref"][0]), zero_depth(R["ref"][1])) >= DEPTH_MIN
    zs = lambda k: float(np.nanmedian(np.where(sel, np.abs(Zm[k] - Zm["ref"]) / Zm["ref"], np.nan)))
    ps = lambda k: float(np.median(np.abs(Pm[k] - Pm["ref"]) / Pm["ref"]))
    out = {"n_zer": int(sel.sum()), "zer_razem": int(sel.size), "null": {"zera": zs("nul"), "bieguny": ps("nul")}, "DS": {}}
    for i in range(1, 9):
        k = f"DS{i}"; d = np.where(sel, np.abs(Zm[k] - Zm["ref"]) / Zm["ref"], 0)
        c, j = np.unravel_index(int(np.argmax(d)), d.shape)
        out["DS"][k] = {"zera_do_null": zs(k) / zs("nul"), "bieguny_do_null": ps(k) / ps("nul"),
                        "max_zero": {"czujnik": AL[c], "odcinek_Hz": [ANCHORS_SM[j], ANCHORS_SM[j + 1]], "przesuniecie_wzgl": float(d[c, j])}}
    return out


def final():
    import json
    res = {"prereg": "PREREG_HBTA_ANTIRESONANCE_v0_4.md", "P2_rozwoj": position_result("P2"), "P1_test": position_result("P1")}
    T = res["P1_test"]["DS"]; ds = list(T)
    nz = sum(T[k]["zera_do_null"] > 1 for k in ds); nb = sum(T[k]["zera_do_null"] > T[k]["bieguny_do_null"] for k in ds)
    nbr = sum(T[k]["zera_do_null"] > 1 for k in ("DS5", "DS6", "DS7"))
    res["H1"] = {"zera>null": nz, "verdict": "SUPPORTED" if nz >= 7 else ("MIXED" if nz >= 5 else "NOT SUPPORTED")}
    res["H2"] = {"zera>bieguny": nb, "verdict": "SUPPORTED" if nb >= 7 else ("MIXED" if nb >= 5 else "NOT SUPPORTED")}
    res["H3"] = {"stezenia_zera>null": nbr, "verdict": "SUPPORTED" if nbr >= 2 else "NOT SUPPORTED"}
    p = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_HBTA_ANTIRESONANCE_v0_4.json"
    p.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    import json
    r = final(); print(json.dumps({k: r[k] for k in ("H1", "H2", "H3")}, indent=1, ensure_ascii=False))
    for pos in ("P2_rozwoj", "P1_test"):
        print(pos, "null", r[pos]["null"], "zera", r[pos]["n_zer"])
        for k, v in r[pos]["DS"].items():
            print(" ", k, round(v["zera_do_null"], 2), round(v["bieguny_do_null"], 2), v["max_zero"]["czujnik"], v["max_zero"]["odcinek_Hz"])
