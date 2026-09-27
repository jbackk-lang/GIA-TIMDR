"""Most kolejowy KW51 (Leuven): kotwica modalna K z surowych drgan vs wzmocnienie (PREREG_KW51_MODAL_ANCHOR_v0_1).

Kotwica stala z modelu modalnego (galaz K): 5 modow pionowych z trackedmodes (mediana przed wzmocnieniem, pazdziernik 2018).
W kazdym rekordzie (300 s, kanaly pionowe pomostu aBD11Az, aBD17Az, decymacja do 25,8 Hz) kotwica samokoryguje sie:
szczyt usrednionego widma w +-4% (interpolacja paraboliczna). Cechy TIMDR: 5 czestotliwosci.
Odniesienia: (a) AR(5) na obu kanalach; (b) czestotliwosci SSI autorow (trackedmodes, najblizsza godzina).
Detektor kNN (k = 3) jak LANL/HBTA. Uczenie: pierwsza polowa pazdziernika 2018; test 'przed': druga polowa pazdziernika;
test 'po': styczen 2020.
"""
from __future__ import annotations
import io, json, sys, zipfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import welch, decimate
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_lanl_3story_bridge import novelty, auc  # noqa: E402

DATA = Path(__file__).resolve().parent.parent.parent / "DATA" / "kw51"
CH = (0, 2)                     # aBD11Az, aBD17Az
VMODES = [4, 5, 9, 11, 12]      # indeksy (0-based) modow pionowych w trackedmodes
CACHE = DATA / "_features_v0_1.json"
RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_KW51_MODAL_ANCHOR_v0_1.json"


def tracked():
    M = loadmat(str(DATA / "trackedmodes" / "trackedmodes.mat"), squeeze_me=True, struct_as_record=False)["modes"]
    return M.sdn, M.f[:, VMODES], M.env[:, 0]


def anchors():
    sdn, f, _ = tracked()
    m = sdn < 737364.0            # przed 2018-11-01 (datenum)
    return np.nanmedian(f[m], 0)


def rec_features(x, fs, anch):
    y = np.stack([decimate(decimate(x[:, c], 8, ftype="fir", zero_phase=True), 4, ftype="fir", zero_phase=True) for c in CH])
    fd = fs / 32
    f, P = welch(y - y.mean(1, keepdims=True), fd, nperseg=1024)
    S = (P / np.median(P, 1, keepdims=True)).mean(0)
    out = []
    for a in anch:
        m = np.where(np.abs(f - a) <= 0.04 * a)[0]; j = m[np.argmax(S[m])]
        y0, y1, y2 = np.log(S[j - 1:j + 2]); d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
        out.append(float(f[j] + d * (f[1] - f[0])))
    ar = []
    for c in y:
        c = (c - c.mean()) / c.std(); A = np.stack([c[5 - i - 1:len(c) - i - 1] for i in range(5)], 1)
        ar += np.linalg.lstsq(A, c[5:], rcond=None)[0].tolist()
    return out, ar


def extract(budget=165):
    import time
    t0 = time.time(); anch = anchors()
    rows = json.loads(CACHE.read_text()) if CACHE.exists() else []
    done = {r["name"] for r in rows}
    for z in ("ambient_201810.zip", "ambient_202001.zip"):
        zz = zipfile.ZipFile(DATA / z)
        for n in sorted(i.filename for i in zz.infolist() if not i.is_dir()):
            if n in done:
                continue
            p = loadmat(io.BytesIO(zz.read(n)), squeeze_me=True, struct_as_record=False)["predat_a"]
            f, ar = rec_features(np.asarray(p.tdata, float), float(p.fs), anch)
            rows.append({"name": n, "sdn": float(np.asarray(p.sdn).ravel()[0]), "f": f, "ar": ar})
            if time.time() - t0 > budget:
                CACHE.write_text(json.dumps(rows)); print("czesciowo", len(rows)); return
    CACHE.write_text(json.dumps(rows)); print("gotowe", len(rows))


def final():
    rows = sorted(json.loads(CACHE.read_text()), key=lambda r: r["sdn"])
    sdn_t, f_t, T_t = tracked(); anch = anchors()
    before = [r for r in rows if "201810" in r["name"]]; after = [r for r in rows if "202001" in r["name"]]
    k = len(before) // 2; tr, te_b = before[:k], before[k:]
    def ssi(r):
        j = int(np.argmin(np.abs(sdn_t - r["sdn"])))
        return f_t[j] if abs(sdn_t[j] - r["sdn"]) < 1 / 48 else np.full(len(VMODES), np.nan)
    F = lambda R: np.array([r["f"] for r in R]); A = lambda R: np.array([r["ar"] for r in R])
    S = lambda R: np.array([ssi(r) for r in R])
    Str = S(tr); med = np.nanmedian(Str, 0)
    fill = lambda X: np.where(np.isfinite(X), X, med)
    sets = {"T": (F(tr), F(te_b), F(after)), "AR": (A(tr), A(te_b), A(after)), "SSI": (fill(Str), fill(S(te_b)), fill(S(after)))}
    res = {"prereg": "PREREG_KW51_MODAL_ANCHOR_v0_1.md", "n": {"train": len(tr), "before_test": len(te_b), "after": len(after)},
           "anchors_hz": anch.tolist(), "auc": {}}
    for kx, (a, b, c) in sets.items():
        res["auc"][kx] = auc(novelty(a, b), novelty(a, c))
    # H1: zgodnosc z SSI (wszystkie rekordy z dopasowana godzina)
    allr = before + after; Fa, Sa = F(allr), S(allr)
    rel = np.abs(Fa - Sa) / Sa
    res["median_rel_err_vs_SSI"] = [float(np.nanmedian(rel[:, i])) for i in range(len(VMODES))]
    res["n_matched"] = [int(np.isfinite(rel[:, i]).sum()) for i in range(len(VMODES))]
    res["shift_after_minus_before_hz"] = {"T": (np.median(F(after), 0) - np.median(F(before), 0)).tolist(),
                                          "SSI": (np.nanmedian(S(after), 0) - np.nanmedian(S(before), 0)).tolist()}
    res["temp_Ts_after_median"] = float(np.nanmedian([T_t[int(np.argmin(np.abs(sdn_t - r["sdn"])))] for r in after]))
    ok = sum(e <= 0.01 for e in res["median_rel_err_vs_SSI"])
    res["H1"] = {"n_ok": ok, "verdict": "SUPPORTED" if ok >= 4 else "NOT SUPPORTED"}
    res["H2"] = "SUPPORTED" if res["auc"]["T"] >= 0.9 else "NOT SUPPORTED"
    res["H3"] = "SUPPORTED" if res["auc"]["T"] >= res["auc"]["AR"] - 0.02 else "NOT SUPPORTED"
    res["H4"] = "SUPPORTED" if res["auc"]["T"] >= res["auc"]["SSI"] - 0.05 else "NOT SUPPORTED"
    RESULT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "extract":
        extract()
    else:
        print(json.dumps(final(), indent=1))
