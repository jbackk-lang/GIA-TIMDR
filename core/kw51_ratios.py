"""KW51: stosunki czestotliwosci jako odniesienie z samej stali (PREREG_KW51_RATIOS_v0_2).

Temperatura zmienia modul E prawie rowno w calej konstrukcji -> wszystkie czestotliwosci skaluja sie jednym czynnikiem.
Czynnik skali s(t) = mediana po modach f_k(t) / f_k,ref (ref = mediana okresu bazowego); f~_k = f_k / s. Odniesienie
bez termometru, z tej samej stali (ta sama bezwladnosc cieplna co most). Warunek fizyczny: tylko rowne skalowanie --
ponizej 0 C podsypka i grunt zamarzaja, sztywnosc zmienia sie nierowno. Odniesienie klasyczne (z termometrem): regresja
kazdego modu na temperature powierzchni mostu, osobne nachylenia powyzej/ponizej 0 C, dopasowana na okresie bazowym.
"""
from __future__ import annotations
import datetime as dt, json, sys
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_lanl_3story_bridge import novelty  # noqa: E402

MAT = Path(__file__).resolve().parent.parent.parent / "DATA" / "kw51" / "trackedmodes" / "trackedmodes.mat"
MODES = [2, 4, 5, 8, 11, 12]            # 1,89 / 2,57 / 2,93 / 4,10 / 5,34 / 6,34 Hz: braki < 35% w calym zapisie
BASE = ("2018-12-01", "2019-03-01"); PRZED = ("2019-03-01", "2019-05-15"); PO = ("2019-09-28", "2020-01-16")


def load():
    import scipy.io as sio
    m = sio.loadmat(MAT, squeeze_me=True, struct_as_record=False)["modes"]
    t = np.array([np.datetime64(dt.datetime.fromordinal(int(s)) + dt.timedelta(days=s % 1) - dt.timedelta(days=366), "m") for s in m.sdn])
    return t, m.f[:, MODES], m.env[:, 0]


def mask(t, per):
    return (t >= np.datetime64(per[0])) & (t < np.datetime64(per[1]))


def features(t, F, Ts, base):
    ref = np.nanmedian(F[base], 0)
    s = np.nanmedian(F / ref, 1)                         # wspolny czynnik skali
    raw = F / ref - 1; norm = F / (s[:, None] * ref) - 1
    ok = np.isfinite(Ts) & base
    def fit(y):                                           # regresja z termometrem: osobno T > 0 i T <= 0
        out = np.full_like(y, np.nan)
        for sel in (Ts > 0, Ts <= 0):
            b = ok & sel & np.isfinite(y)
            if b.sum() > 20:
                p = np.polyfit(Ts[b], y[b], 1); m = sel & np.isfinite(Ts); out[m] = y[m] - np.polyval(p, Ts[m])
        return out
    reg = np.stack([fit(raw[:, k]) for k in range(raw.shape[1])], 1)
    return {"surowe": raw, "stosunki": norm, "termometr": reg}, s


def _mad(y):
    y = y[np.isfinite(y)]; return float(1.4826 * np.median(np.abs(y - np.median(y))))


def final():
    t, F, Ts = load(); b, pr, po = mask(t, BASE), mask(t, PRZED), mask(t, PO)
    X, s = features(t, F, Ts, b); res = {"prereg": "PREREG_KW51_RATIOS_v0_2.md", "okresy": {"baza": BASE, "przed": PRZED, "po": PO}}
    # H1: temperatura znika (okres PRZED, nieogladany; caly powyzej 0 C)
    st = {}
    for n, Y in X.items():
        st[n] = {"MAD_promil": [1000 * _mad(Y[pr, k]) for k in range(Y.shape[1])],
                 "rho_T": [float(abs(spearmanr(Ts[pr], Y[pr, k], nan_policy="omit").correlation)) for k in range(Y.shape[1])]}
    ratio = np.array(st["stosunki"]["MAD_promil"]) / np.array(st["surowe"]["MAD_promil"])
    beat_T = int(sum(a < c for a, c in zip(st["stosunki"]["MAD_promil"], st["termometr"]["MAD_promil"])))
    c1 = float(np.median(ratio)) < 0.8; c2 = np.median(st["stosunki"]["rho_T"]) < np.median(st["surowe"]["rho_T"])
    res["H1"] = {"MAD_stosunki/surowe_mediana": float(np.median(ratio)), "rho_T_mediana": {n: float(np.median(v["rho_T"])) for n, v in st.items()},
                 "verdict": "SUPPORTED" if c1 and c2 else ("MIXED" if c1 or c2 else "NOT SUPPORTED")}
    res["H1b"] = {"stosunki<termometr_MAD_modow": beat_T, "verdict": "SUPPORTED" if beat_T >= 4 else "NOT SUPPORTED"}
    res["statystyki_przed"] = st
    # H3: wykrycie wzmocnienia bez falszywych alarmow (kNN, k = 3; prog = p99 nowosci LOO na bazie)
    det = {}
    for n, Y in X.items():
        c = np.isfinite(Y).all(1); tr = Y[b & c][::3]
        thr = float(np.percentile(novelty(tr, tr, loo=True), 99))
        det[n] = {"prog": thr, "falszywe_alarmy_przed": float(np.mean(novelty(tr, Y[pr & c]) > thr)),
                  "trafienia_po": float(np.mean(novelty(tr, Y[po & c]) > thr)), "n_przed": int((pr & c).sum()), "n_po": int((po & c).sum())}
    d = det["stosunki"]; e = det["surowe"]
    res["H3"] = {"detekcja": det, "verdict": "SUPPORTED" if d["falszywe_alarmy_przed"] < e["falszywe_alarmy_przed"] and d["trafienia_po"] >= 0.9
                 else ("MIXED" if d["falszywe_alarmy_przed"] < e["falszywe_alarmy_przed"] or d["trafienia_po"] >= 0.9 else "NOT SUPPORTED")}
    # opisowo: skala s jako "termometr ze stali" (korelacja z temperatura powierzchni w okresie PRZED)
    ok = pr & np.isfinite(Ts) & np.isfinite(s)
    res["skala_vs_T_przed_rho"] = float(spearmanr(Ts[ok], s[ok]).correlation)
    p = Path(__file__).resolve().parent.parent / "docs" / "geometry" / "RESULT_KW51_RATIOS_v0_2.json"
    p.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


if __name__ == "__main__":
    import warnings; warnings.filterwarnings("ignore")
    r = final(); print(json.dumps({k: r[k] for k in ("H1", "H1b", "H3", "skala_vs_T_przed_rho")}, indent=1, ensure_ascii=False))
    for n, v in r["statystyki_przed"].items():
        print(n, "MAD", np.round(v["MAD_promil"], 2), "rho", np.round(v["rho_T"], 2))
