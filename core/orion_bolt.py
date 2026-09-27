"""ORION-AE (FEMTO-ST): luzowanie sruby w konstrukcji drgajacej (PREREG_ORION_BOLT_v0_1).

Wibrator 118,4 Hz (amplituda sterowana), 7 poziomow dokrecenia 60 -> 5 cNm. Kanaly: A, B, C = emisja akustyczna (5 MHz),
D = wibrometr laserowy. Kazdy plik (~0,9 s) dzielony na 4 odcinki.
TIMDR (droga wg reguly rezimow):
  fala  -> galaz K: kotwica = czestotliwosc wymuszenia (samokorekta, szczyt 20-500 Hz), linie H = log((P(2f)+P(3f))/P(f))
           (nieliniowosc kontaktu, jak zderzak LANL v0.3);
  czasteczka -> emisja akustyczna A: P (udzial 5% najsilniejszych probek energii obwiedni 100-900 kHz) i D (gestosc zdarzen).
Klasyczne: RMS emisji A, liczba przekroczen progu (3 sigma z pliku referencyjnego 60 cNm tej serii) na sekunde,
kurtoza predkosci.
"""
from __future__ import annotations
import io, json, re, sys, zipfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import decimate, welch
from scipy.stats import kurtosis, spearmanr
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.transition_params import event_density, band_envelope  # noqa: E402
from core.real_seu_multichannel_bridge import lda_fit, lda_predict, macro_f1  # noqa: E402

DATA = Path(__file__).resolve().parent.parent.parent / "DATA" / "orion_ae"
FS = 5e6
NSEG = 4
CACHE = DATA / "_features_v0_1.json"
RESULT = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_ORION_BOLT_v0_1.json"


def seg_features(a, v):
    vd = decimate(decimate(decimate(v, 10, ftype="fir"), 10, ftype="fir"), 10, ftype="fir"); fd = FS / 1000
    f, P = welch(vd - vd.mean(), fd, nperseg=min(1024, len(vd)))
    m = (f > 20) & (f < 500); f0 = f[m][np.argmax(P[m])]
    pw = lambda c: P[np.abs(f - c) <= 3 * (f[1] - f[0])].max()
    H = float(np.log((pw(2 * f0) + pw(3 * f0)) / pw(f0)))
    a = a - a.mean(); env = band_envelope(a, FS, 100e3, 900e3); e2 = env ** 2; k = int(0.05 * len(e2))
    d = event_density(env, FS)
    return {"f0": float(f0), "H": H, "P": float(np.sort(e2)[-k:].sum() / e2.sum()), "D": d["D"],
            "ae_rms": float(a.std()), "v_kurt": float(kurtosis(vd)), "a": a}


def extract(budget=165):
    import time
    t0 = time.time(); rows = json.loads(CACHE.read_text()) if CACHE.exists() else []
    done = {(r["file"], r["seg"]) for r in rows}
    for s in "BDE":
        z = zipfile.ZipFile(DATA / f"series_{s}.zip"); names = sorted(x for x in z.namelist() if x.endswith(".mat"))
        ref_sigma = None
        for fn in sorted(names, key=lambda x: ("60cNm" not in x, x)):     # najpierw 60 cNm: prog referencyjny serii
            if all((fn, i) in done for i in range(NSEG)) and ref_sigma is not None:
                continue
            m = loadmat(io.BytesIO(z.read(fn))); A, V = m["A"].ravel(), m["D"].ravel(); L = len(A) // NSEG
            for i in range(NSEG):
                f = seg_features(A[i * L:(i + 1) * L], V[i * L:(i + 1) * L]); a = f.pop("a")
                if ref_sigma is None:
                    ref_sigma = float(a.std())
                f["ae_count"] = float(np.sum((np.abs(a[1:]) > 3 * ref_sigma) & (np.abs(a[:-1]) <= 3 * ref_sigma)) / (len(a) / FS))
                if (fn, i) not in done:
                    rows.append({"series": s, "torque": int(re.search(r"_(\d\d)cNm_", fn).group(1)), "file": fn, "seg": i, **f})
            if time.time() - t0 > budget:
                CACHE.write_text(json.dumps(rows)); print("czesciowo", len(rows)); return
    CACHE.write_text(json.dumps(rows)); print("gotowe", len(rows))


SETS = {"T": ["H", "P", "D"], "KL": ["ae_rms", "ae_count", "v_kurt"]}


def final():
    R = json.loads(CACHE.read_text())
    def mat(s, cols):
        rr = [r for r in R if r["series"] == s]; X = np.array([[r[c] for c in cols] for r in rr])
        X = (X - X.mean(0)) / (X.std(0) + 1e-12)          # standaryzacja w obrebie serii (bez etykiet)
        return X, np.array([r["torque"] for r in rr])
    res = {"prereg": "PREREG_ORION_BOLT_v0_1.md", "n": {s: sum(r["series"] == s for r in R) for s in "BDE"}, "rho_H": {}, "f1": {}}
    for s in "DE":
        rr = [r for r in R if r["series"] == s]
        res["rho_H"][s] = float(spearmanr([r["torque"] for r in rr], [r["H"] for r in rr]).correlation)
    for k, cols in SETS.items():
        Xb, yb = mat("B", cols); mdl = lda_fit(Xb, yb); res["f1"][k] = {}
        for s in "DE":
            X, y = mat(s, cols); res["f1"][k][s] = macro_f1(y, lda_predict(mdl, X))
    Pmed = {s: {t: float(np.median([r["P"] for r in R if r["series"] == s and r["torque"] == t])) for t in (5, 10, 20, 30, 40, 50, 60)} for s in "DE"}
    res["P_median"] = Pmed
    res["H1"] = "SUPPORTED" if all(res["rho_H"][s] <= -0.6 for s in "DE") else "NOT SUPPORTED"
    mt = np.mean(list(res["f1"]["T"].values())); mk = np.mean(list(res["f1"]["KL"].values()))
    res["H2"] = {"T": float(mt), "KL": float(mk), "verdict": "SUPPORTED" if mt > mk else "NOT SUPPORTED"}
    res["H3"] = "SUPPORTED" if all(max(Pmed[s], key=Pmed[s].get) >= 10 for s in "DE") else "NOT SUPPORTED"
    RESULT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    print(json.dumps(final(), indent=1)) if sys.argv[1] == "final" else extract()
