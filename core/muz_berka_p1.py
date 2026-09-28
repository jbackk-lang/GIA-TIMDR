"""MUZ P1 na danych publicznych (PKDD'99, Berka i Sochorova): drogowskazy TIMDR w budzecie domowym.
Czy zegar wyplaty + odniesienie do wlasnego dochodu (+ rezim zdarzen) lepiej wskazuja klopoty finansowe
(kredyt zly: status B/D) niz klasyczne cechy kalendarzowe w kwotach nominalnych?
PREREG_MUZ_P1_BERKA_v0_1. Tylko historia przed przyznaniem kredytu; tylko >= 10 miesiecy historii (regula wykonalnosci)."""
import os, sys, json
import numpy as np
import pandas as pd

_LOC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "DATA", "berka", "repo")
D = os.environ.get("BERKA", _LOC if os.path.isdir(_LOC) else "/mnt/user-data/uploads/Downloads/a/DATA/berka/repo")
MIN_M = 10


def load():
    L = pd.read_csv(os.path.join(D, "fin_loan.tsv"), sep="\t", header=None,
                    names=["loan", "acc", "date", "amount", "dur", "pay", "status"], parse_dates=["date"])
    L["bad"] = L.status.isin(["B", "D"]).astype(int)
    T = pd.read_csv(os.path.join(D, "fin_trans.tsv"), sep="\t", header=None,
                    names=["id", "acc", "date", "amt", "bal", "type", "op", "cat", "bank", "oacc"], parse_dates=["date"],
                    dtype={"op": str, "cat": str, "bank": str})
    T = T[T.acc.isin(L.acc)].copy(); T["op"] = T.op.fillna("").str.strip(); T["cat"] = T.cat.fillna("").str.strip()
    T["credit"] = T.type == "C"
    return L, T


def payday(h):
    """Kotwica: dzien wyplaty = dzien miesiaca najczestszego stalego wplywu z innego banku (COB); gdy brak --
    najwiekszego regularnego wplywu gotowkowego; gdy brak -- 1. dzien (kalendarz)."""
    c = h[h.credit & (h.cat != "IC")]
    for src in (c[c.op == "COB"], c):
        if len(src):
            months = src.date.dt.to_period("M").nunique(); tot = h.date.dt.to_period("M").nunique()
            if months >= 0.6 * tot:
                big = src.loc[src.groupby(src.date.dt.to_period("M")).amt.idxmax()]
                return int(big.date.dt.day.median()), ("COB" if src is not c else "wplyw")
    return 1, "kalendarz"


def cycles(h, day):
    """Granice cykli: kolejne daty 'dzien wyplaty' (z przycieciem do dlugosci miesiaca)."""
    start = h.date.min().to_period("M").to_timestamp(); end = h.date.max()
    b = []
    m = start
    while m <= end + pd.offsets.MonthBegin(1):
        dd = min(day, m.days_in_month); b.append(m + pd.Timedelta(days=dd - 1)); m = m + pd.offsets.MonthBegin(1)
    return pd.DatetimeIndex(b)


def eta_D(x):
    x = np.asarray(x, float)
    if x.sum() == 0:
        return 0.0
    eta = x.mean() ** 2 / (np.mean(x ** 2) + 1e-12); return float(eta / max(1 - eta, 1e-9))


def feats_cycles(h, bounds, ratio=True):
    """Cechy na cyklach [b_k, b_{k+1}): wydatki E, dochod I, E/I (lub E nominalnie), minimum salda przed kolejna
    wyplata wzgledem I (lub nominalnie), udzialy kategorii, rezim zdarzen (D dziennych wydatkow)."""
    rows = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        s = h[(h.date >= a) & (h.date < b)]
        if len(s) == 0:
            continue
        I = s[s.credit & (s.cat != "IC")].amt.sum(); E = s[~s.credit].amt.sum()
        days = pd.date_range(a, b - pd.Timedelta(days=1)); dcount = s[~s.credit].groupby(s.date).size().reindex(days, fill_value=0)
        ref = I if (ratio and I > 0) else (1.0 if not ratio else np.nan)
        rows.append({"r": E / ref, "minbal": s.bal.min() / ref, "hh": s[s.cat == "HH"].amt.sum() / ref,
                     "ins": s[s.cat == "IN"].amt.sum() / ref, "cash": s[s.op == "WIC"].amt.sum() / ref, "D": eta_D(dcount.values),
                     "neg": float((s.bal < 0).any())})
    R = pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan)
    if len(R) < 3:
        return None
    k = np.arange(len(R))
    tr = float(pd.Series(R.r.values).corr(pd.Series(k), method="spearman")) if R.r.notna().sum() > 3 else 0.0
    med = lambda v: float(np.nanmedian(v))
    return [med(R.r), float(np.nanmedian(np.abs(R.r - np.nanmedian(R.r)))), float(np.nanmean(R.r > (1 if ratio else np.nanmedian(R.r) * 1.2))),
            tr if np.isfinite(tr) else 0.0, float(np.nanmin(R.minbal)), med(R.minbal), med(R.hh), med(R.ins), med(R.cash), med(R.D),
            float(R.neg.mean())]


def classic(h):
    """Klasyka: miesiace kalendarzowe, kwoty nominalne (cechy z literatury PKDD'99)."""
    m = h.date.dt.to_period("M")
    inc = h[h.credit].groupby(m).amt.sum(); exp = h[~h.credit].groupby(m).amt.sum()
    n = len(exp); g = (exp.iloc[-3:].mean() - exp.iloc[:3].mean()) / (abs(exp.iloc[:3].mean()) + 1e-9) if n >= 6 else 0.0
    return [h.bal.mean(), h.bal.min(), h.bal.std(), float((h.bal < 0).sum()), inc.mean(), exp.mean(), exp.std(), g,
            float(len(h[~h.credit]) / max(n, 1))]


def build():
    L, T = load(); out = []
    for _, l in L.iterrows():
        h = T[(T.acc == l.acc) & (T.date < l.date)].sort_values("date")
        if len(h) == 0 or (l.date - h.date.min()).days / 30.4 < MIN_M:
            continue
        day, src = payday(h); bp = cycles(h, day); bc = cycles(h, 1)
        fT = feats_cycles(h, bp, True); fTc = feats_cycles(h, bc, True); fTn = feats_cycles(h, bp, False)
        if fT is None or fTc is None or fTn is None:
            continue
        out.append({"loan": int(l.loan), "acc": int(l.acc), "bad": int(l.bad), "payday": day, "src": src,
                    "C": classic(h), "T": fT, "T_cal": fTc, "T_nom": fTn})
    return out


def split(rows, seed=20260928):
    """Podzial po rachunkach, warstwowo wg bad: 1/3 rozwoj, 2/3 test (ustalony przed cechami)."""
    rng = np.random.default_rng(seed); dev = set()
    for b in (0, 1):
        ids = sorted({r["acc"] for r in rows if r["bad"] == b}); rng.shuffle(ids); dev |= set(ids[: len(ids) // 3])
    return [r for r in rows if r["acc"] in dev], [r for r in rows if r["acc"] not in dev]


def lda_score(Xtr, ytr, Xte, shrink=0.1):
    mu, sd = np.nanmean(Xtr, 0), np.nanstd(Xtr, 0) + 1e-12
    Xtr = np.where(np.isfinite(Xtr), Xtr, mu); Xte = np.where(np.isfinite(Xte), Xte, mu)
    Z = (Xtr - mu) / sd; T_ = (Xte - mu) / sd; M = np.stack([Z[ytr == k].mean(0) for k in (0, 1)])
    R = np.concatenate([Z[ytr == k] - M[k] for k in (0, 1)]); S = R.T @ R / (len(R) - 2); p = S.shape[0]
    S = (1 - shrink) * S + shrink * np.trace(S) / p * np.eye(p); w = np.linalg.solve(S, M[1] - M[0])
    return T_ @ w


def auc(s, y):
    from scipy.stats import rankdata
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def cv_scores(rows, key, reps=10, k=5, seed=1):
    """Powtarzana warstwowa k-krotna CV: sredni wynik out-of-fold dla kazdego kredytu."""
    X = np.array([r[key] if isinstance(key, str) else sum((r[q] for q in key), []) for r in rows], float)
    y = np.array([r["bad"] for r in rows]); acc = np.zeros(len(y)); rng = np.random.default_rng(seed)
    for _ in range(reps):
        fold = np.zeros(len(y), int)
        for b in (0, 1):
            ii = np.where(y == b)[0]; rng.shuffle(ii); fold[ii] = np.arange(len(ii)) % k
        s = np.zeros(len(y))
        for f in range(k):
            te = fold == f; s[te] = lda_score(X[~te], y[~te], X[te])
        acc += (s - s.mean()) / (s.std() + 1e-12)
    return acc / reps, y


SETS = {"C": "C", "T": "T", "T_cal": "T_cal", "T_nom": "T_nom", "C+T": ("C", "T")}


def evaluate(rows, n_boot=2000, seed=7):
    S = {n: cv_scores(rows, k) for n, k in SETS.items()}; y = S["C"][1]
    res = {"n": len(y), "n_bad": int(y.sum()), "AUC": {n: auc(s, y) for n, (s, _) in S.items()}}
    rng = np.random.default_rng(seed); i1 = np.where(y == 1)[0]; i0 = np.where(y == 0)[0]
    def ci(a, b):
        v = []
        for _ in range(n_boot):
            ii = np.concatenate([rng.choice(i1, len(i1)), rng.choice(i0, len(i0))])
            v.append(auc(S[a][0][ii], y[ii]) - auc(S[b][0][ii], y[ii]))
        return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    ver = lambda d, c: "SUPPORTED" if c[0] > 0 else ("MIXED" if d > 0 else "NOT SUPPORTED")
    for h, (a, b) in {"H1": ("T", "C"), "H2_zegar": ("T", "T_cal"), "H3_odniesienie": ("T", "T_nom"), "H4_dodaje": ("C+T", "C")}.items():
        d = res["AUC"][a] - res["AUC"][b]; c = ci(a, b); res[h] = {"porownanie": f"{a} - {b}", "dAUC": d, "CI95": c, "verdict": ver(d, c)}
    return res


if __name__ == "__main__":
    rows = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else build()
    dev, test = split(rows)
    part = dev if sys.argv[1] == "dev" else test
    print(json.dumps(evaluate(part), indent=1, ensure_ascii=False))
