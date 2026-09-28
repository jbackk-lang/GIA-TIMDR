"""Krzywe uczenia: czy TIMDR jako warstwa porzadkujaca zmniejsza liczbe przykladow potrzebnych do nauki?
PREREG_PADERBORN_LEARNING_CURVES_v0_1. Ta sama mala siec z uwaga (1 warstwa transformera, 2 glowy, d = 32) na:
  raw   -- surowy przebieg 2 s / 32 kHz pociety na 125 tokenow po 512 probek,
  spec  -- klasyczna obrobka ML: log-spektrogram (STFT 512 probek, skok 512, Hann) -> 125 tokenow (ramki czasu) x 257 binow,
  timdr -- pole TIMDR: 15 pasm nosnych (tokeny) x widmo obwiedni wzgledem tla, w rzedach obrotu (230 binow),
oraz trzecia kolumna: cechy sita TIMDR (12) + LDA ze skurczem 0,1.
Lozyska rozlaczne (5 foldow: po jednym zdrowym, zewn., wewn. w tescie). Krzywa: N przykladow na klase."""
import json, os, sys, time
import numpy as np
import torch
import torch.nn as nn

D = os.environ.get("LC_DATA", "/mnt/user-data/uploads/Downloads/a/DATA/paderborn_lc_v0_1")
BEAR = {0: ["K002", "K003", "K004", "K005", "K006"], 1: ["KA04", "KA15", "KA16", "KA22", "KA30"],
        2: ["KI04", "KI14", "KI16", "KI18", "KI21"]}
NS = [4, 8, 16, 32, 64, 128, 160]
REPS, STEPS, BATCH, LR, WD = 3, 300, 32, 1e-3, 1e-2
FEATS = ['G_curv_BPFI', 'G_curv_BPFO', 'G_ext_BPFI', 'G_ext_BPFO', 'Q_BPFI', 'Q_BPFO', 'Q_went_BPFI', 'Q_went_BPFO',
         'R_BPFI', 'R_BPFO', 'R_BSF', 'R_w_entropy']
torch.set_num_threads(2)


def load(meas_range):
    rs = {j["member"]: j["f"] for j in json.load(open(os.path.join(D, "rs_feats_all.json")))}
    out = {}
    for c, bs in BEAR.items():
        for b in bs:
            z = np.load(os.path.join(D, f"{b}.npz")); m = np.isin(z["meas"], list(meas_range))
            raw = z["raw"][m]; raw = raw / (raw.std(1, keepdims=True) + 1e-9)
            f = np.array([[rs[f"{b}/{cd}_{b}_{n}.mat"][k] for k in FEATS] for cd, n in zip(z["cond"][m], z["meas"][m])])
            seg = raw.reshape(len(raw), 125, 512) * np.hanning(512)[None, None, :]
            spec = np.log(np.abs(np.fft.rfft(seg, axis=2)) ** 2 + 1e-8).astype(np.float32)
            out[b] = {"raw": raw.reshape(len(raw), 125, 512).astype(np.float32), "spec": spec, "timdr": z["tok"][m].astype(np.float32),
                      "lda": f, "y": np.full(m.sum(), c)}
    return out


class Net(nn.Module):
    def __init__(self, ntok, din, d=32, heads=2, ncls=3):
        super().__init__()
        self.emb = nn.Linear(din, d); self.pos = nn.Parameter(torch.zeros(1, ntok, d))
        self.enc = nn.TransformerEncoderLayer(d, heads, dim_feedforward=64, dropout=0.1, batch_first=True)
        self.out = nn.Linear(d, ncls)

    def forward(self, x):
        return self.out(self.enc(self.emb(x) + self.pos).mean(1))


def macro_f1(y, p):
    s = []
    for k in np.unique(y):
        tp = np.sum((p == k) & (y == k)); fp = np.sum((p == k) & (y != k)); fn = np.sum((p != k) & (y == k))
        s.append(0.0 if tp == 0 else 2 * tp / (2 * tp + fp + fn))
    return float(np.mean(s))


def train_net(Xtr, ytr, Xte, seed):
    torch.manual_seed(seed); rng = np.random.default_rng(seed)
    mu = Xtr.mean(0, keepdims=True); sd = Xtr.std(0, keepdims=True) + 1e-6      # standaryzacja z uczacych
    Xtr = torch.tensor((Xtr - mu) / sd); Xte = torch.tensor((Xte - mu) / sd); ytr_t = torch.tensor(ytr)
    net = Net(Xtr.shape[1], Xtr.shape[2]); opt = torch.optim.AdamW(net.parameters(), lr=LR, weight_decay=WD)
    lossf = nn.CrossEntropyLoss(); net.train()
    for _ in range(STEPS):
        i = rng.integers(0, len(ytr), min(BATCH, len(ytr))); opt.zero_grad()
        l = lossf(net(Xtr[i]), ytr_t[i]); l.backward(); opt.step()
    net.eval()
    with torch.no_grad():
        return net(Xte).argmax(1).numpy(), float(l)


def lda(Xtr, ytr, Xte, shrink=0.1):
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-12; Z = (Xtr - mu) / sd; ks = np.unique(ytr)
    M = np.stack([Z[ytr == k].mean(0) for k in ks]); R = np.concatenate([Z[ytr == k] - M[i] for i, k in enumerate(ks)])
    S = R.T @ R / max(len(R) - len(ks), 1); p = S.shape[0]; S = (1 - shrink) * S + shrink * np.trace(S) / p * np.eye(p)
    Si = np.linalg.inv(S); T = (Xte - mu) / sd
    sc = T @ Si @ M.T - 0.5 * np.einsum("ij,jk,ik->i", M, Si, M)
    return ks[np.argmax(sc, 1)]


def run(meas_range, ns=NS, reps=REPS, folds=range(5), arms=("raw", "spec", "timdr", "lda"), log=None):
    data = load(meas_range); res = []
    for fo in folds:
        te = [BEAR[c][fo] for c in range(3)]; tr = [b for c in range(3) for b in BEAR[c] if b not in te]
        cat = lambda bs, k: np.concatenate([data[b][k] for b in bs])
        yte = cat(te, "y"); ytr_all = cat(tr, "y")
        for n in ns:
            for r in range(reps):
                rng = np.random.default_rng(1000 * fo + 10 * n + r)
                idx = np.concatenate([rng.choice(np.where(ytr_all == c)[0], min(n, (ytr_all == c).sum()), replace=False) for c in range(3)])
                row = {"fold": fo, "n": n, "rep": r}
                for a in arms:
                    Xtr = cat(tr, a)[idx]; Xte = cat(te, a); t0 = time.time()
                    if a == "lda":
                        p = lda(Xtr, ytr_all[idx], Xte); row[a] = macro_f1(yte, p)
                    else:
                        p, l = train_net(Xtr, ytr_all[idx], Xte, seed=1000 * fo + 10 * n + r)
                        row[a] = macro_f1(yte, p); row[a + "_loss"] = l
                    row[a + "_s"] = round(time.time() - t0, 1)
                res.append(row)
                if log:
                    print(json.dumps(row), file=log, flush=True)
    return res


def summarize(res, arms=("raw", "spec", "timdr", "lda")):
    ns = sorted(set(r["n"] for r in res))
    return {a: {n: float(np.mean([r[a] for r in res if r["n"] == n])) for n in ns} for a in arms}


def hypotheses(res):
    S = summarize(res); ns = sorted(S["timdr"])
    def first(a, target):
        for n in ns:
            if S[a][n] >= target:
                return n
        return None
    out = {"krzywe": S}
    for comp, key in (("spec", "H1"), ("raw", "H1b")):
        target = S[comp][ns[-1]]; nc = first(comp, target); nt = first("timdr", target)
        ratio = (nc / nt) if (nc and nt) else None
        v = "NOT SUPPORTED" if ratio is None or ratio < 1.5 else ("SUPPORTED" if ratio >= 3 else "MIXED")
        out[key] = {"porownanie": comp, "cel_F1": target, "N_" + comp: nc, "N_timdr": nt, "stosunek": ratio, "verdict": v}
    pairs = [r for r in res if r["n"] <= 32]; k = sum(r["timdr"] > r["spec"] for r in pairs)
    out["H2"] = {"timdr>spec_przy_N<=32": f"{k}/{len(pairs)}", "verdict": "SUPPORTED" if k >= 0.8 * len(pairs) else "NOT SUPPORTED"}
    d = S["lda"][ns[-1]] - S["timdr"][ns[-1]]
    out["H3"] = {"lda-timdr_przy_N_max": d, "verdict": "SUPPORTED" if d >= -0.02 else "NOT SUPPORTED"}
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "dev":
        res = run(range(1, 11), ns=[8, 32, 80], reps=1, folds=[0, 1], arms=("spec",), log=sys.stdout)
        print(json.dumps(summarize(res, arms=("spec",)), indent=1))
        sys.exit()
    if mode == "final":
        log = open(sys.argv[2] + ".log", "w")
        res = run(range(11, 21), log=log)
        out = {"prereg": "PREREG_PADERBORN_LEARNING_CURVES_v0_1.md", "wiersze": res, **hypotheses(res)}
        json.dump(out, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
        print(json.dumps({k: v for k, v in out.items() if k != "wiersze"}, indent=1, ensure_ascii=False))
