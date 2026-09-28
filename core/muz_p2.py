"""MUZ P2 (PKDD'99): odniesienie do zobowiazania (raty) zamiast do dochodu.
Lekcja P1: wzorzec ma znosic zakłócenie, nie cel. Pytanie o wyplacalnosc = czy starczy na rate, wiec
wzorcem jest rata z tego samego medium (kwota znana w chwili przyznania kredytu). Zegar od wyplaty: dołek salda
przed kolejna wyplata. PREREG_MUZ_P2_BERKA_v0_1."""
import sys, json
import numpy as np, pandas as pd
import muz_berka_p1 as p1


def feats_R(h, bounds, pay):
    rows = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        s = h[(h.date >= a) & (h.date < b)]
        if len(s) == 0:
            continue
        I = s[s.credit & (s.cat != "IC")].amt.sum(); E = s[~s.credit].amt.sum()
        days = pd.date_range(a, b - pd.Timedelta(days=1)); dc = s[~s.credit].groupby(s.date).size().reindex(days, fill_value=0)
        rows.append({"low": s.bal.min() / pay, "I": I / pay, "net": (I - E) / pay, "D": p1.eta_D(dc.values),
                     "short": float(s.bal.min() < pay)})
    R = pd.DataFrame(rows)
    if len(R) < 3:
        return None
    return [float(R.low.min()), float(R.low.median()), float(np.percentile(R.low, 25)), float(R.I.median()),
            float(R.net.median()), float(R.short.mean()), float(R.D.median())]


def build():
    L, T = p1.load(); out = []
    for _, l in L.iterrows():
        h = T[(T.acc == l.acc) & (T.date < l.date)].sort_values("date")
        if len(h) == 0 or (l.date - h.date.min()).days / 30.4 < p1.MIN_M:
            continue
        day, src = p1.payday(h)
        fR = feats_R(h, p1.cycles(h, day), l.pay); fRc = feats_R(h, p1.cycles(h, 1), l.pay)
        fT = p1.feats_cycles(h, p1.cycles(h, day), True)
        if fR is None or fRc is None or fT is None:
            continue
        out.append({"loan": int(l.loan), "acc": int(l.acc), "bad": int(l.bad), "C": p1.classic(h), "R": fR, "R_cal": fRc, "T": fT})
    return out


p1.SETS.clear(); p1.SETS.update({"C": "C", "R": "R", "R_cal": "R_cal", "T": "T", "C+R": ("C", "R")})
HYP = {"H1_dodaje": ("C+R", "C"), "H2_rata_vs_dochod": ("R", "T"), "H3_zegar": ("R", "R_cal"), "H4_R_vs_C": ("R", "C")}


def evaluate(rows, n_boot=2000, seed=7):
    S = {n: p1.cv_scores(rows, k) for n, k in p1.SETS.items()}; y = S["C"][1]
    res = {"n": len(y), "n_bad": int(y.sum()), "AUC": {n: p1.auc(s, y) for n, (s, _) in S.items()}}
    rng = np.random.default_rng(seed); i1 = np.where(y == 1)[0]; i0 = np.where(y == 0)[0]
    B = [np.concatenate([rng.choice(i1, len(i1)), rng.choice(i0, len(i0))]) for _ in range(n_boot)]
    for h, (a, b) in HYP.items():
        v = [p1.auc(S[a][0][ii], y[ii]) - p1.auc(S[b][0][ii], y[ii]) for ii in B]
        d = res["AUC"][a] - res["AUC"][b]; c = [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
        res[h] = {"porownanie": f"{a} - {b}", "dAUC": d, "CI95": c,
                  "verdict": "SUPPORTED" if c[0] > 0 else ("MIXED" if d > 0 else "NOT SUPPORTED")}
    return res


if __name__ == "__main__":
    rows = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else build()
    if len(sys.argv) <= 2:
        json.dump(rows, open("rows_p2.json", "w"))
    dev, test = p1.split(rows)
    print(json.dumps(evaluate(dev if sys.argv[1] == "dev" else test), indent=1, ensure_ascii=False))
