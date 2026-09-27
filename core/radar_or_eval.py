"""Ocena Open Radar v0.1: zestawy cech, LDA ze skurczem, UAV-vs-reszta AUC i 4 klasy macro-F1."""
import os, json, numpy as np
import radar_or_io as io
from real_seu_multichannel_bridge import lda_fit, macro_f1

SETS = {
    'A_klasyczne': ['dopp', 'jem', 'cvd'],
    'B_TIMDR': ['sieve', 'char'],
    'AB': ['dopp', 'jem', 'cvd', 'sieve', 'char'],
    'K_kinematyka': ['kin'],
}


def load(part, tag='v0_1'):
    d = os.path.join(io.DATA, f'feat_{tag}_{part}')
    return [json.load(open(os.path.join(d, f))) for f in sorted(os.listdir(d))]


def matrix(R, groups):
    X = np.array([sum((r[g] for g in groups), []) for r in R], float)
    y = np.array([r['cls'] for r in R])
    return X, y


def impute(Xtr, Xte):
    med = np.nanmedian(Xtr, 0)
    Xtr = np.where(np.isfinite(Xtr), Xtr, med); Xte = np.where(np.isfinite(Xte), Xte, med)
    return Xtr, Xte


def lda_scores(m, X):
    Z = (X - m['mu']) / m['sd']
    return Z @ m['Si'] @ m['means'].T - 0.5 * np.einsum('ij,jk,ik->i', m['means'], m['Si'], m['means'])


def auc(pos, neg):
    x = np.r_[pos, neg]; r = np.argsort(np.argsort(x)) + 1.0
    # remisy: srednie rangi
    from scipy.stats import rankdata
    r = rankdata(x)
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def fit_eval(Xtr, ytr, Xte, yte):
    Xtr, Xte = impute(Xtr, Xte)
    m4 = lda_fit(Xtr, ytr)
    yp = m4['ks'][np.argmax(lda_scores(m4, Xte), 1)]
    f1 = macro_f1(yte, yp)
    yb = np.where(ytr == 'uav', 'uav', 'rest')
    mb = lda_fit(Xtr, yb)
    sc = lda_scores(mb, Xte); s = sc[:, list(mb['ks']).index('uav')] - sc[:, list(mb['ks']).index('rest')]
    a = auc(s[yte == 'uav'], s[yte != 'uav'])
    return f1, a, s, yp


# ---------------- zamrozona ocena (jedno uruchomienie) ----------------
def bootstrap_delta(y, sA, sB, ypA, ypB, n=2000, seed=1):
    rng = np.random.default_rng(seed)
    idx = {c: np.where(y == c)[0] for c in io.CLASSES}
    dA, dF = [], []
    for _ in range(n):
        ii = np.concatenate([rng.choice(v, len(v)) for v in idx.values()])
        yy = y[ii]
        dA.append(auc(sB[ii][yy == 'uav'], sB[ii][yy != 'uav']) - auc(sA[ii][yy == 'uav'], sA[ii][yy != 'uav']))
        dF.append(macro_f1(yy, ypB[ii]) - macro_f1(yy, ypA[ii]))
    q = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    return {'dAUC_CI95': q(dA), 'dF1_CI95': q(dF)}


def auc_ci(y, s, n=2000, seed=2):
    rng = np.random.default_rng(seed)
    idx = {c: np.where(y == c)[0] for c in io.CLASSES}
    v = []
    for _ in range(n):
        ii = np.concatenate([rng.choice(w, len(w)) for w in idx.values()]); yy = y[ii]
        v.append(auc(s[ii][yy == 'uav'], s[ii][yy != 'uav']))
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


def final(tag='v0_1'):
    Rd, Re = load('dev', tag), load('eval', tag)
    ytr = np.array([r['cls'] for r in Rd]); yte = np.array([r['cls'] for r in Re])
    out = {'n_dev': len(Rd), 'n_eval': len(Re), 'sets': {}}
    keep = {}
    for sname, gr in SETS.items():
        Xtr, _ = matrix(Rd, gr); Xte, _ = matrix(Re, gr)
        f1, a, s, yp = fit_eval(Xtr, ytr, Xte, yte)
        keep[sname] = (s, yp)
        out['sets'][sname] = {'macroF1': f1, 'AUC_uav': a, 'AUC_uav_CI95': auc_ci(yte, s)}
        # podzbior jednej konfiguracji radaru (bw ~220 MHz, wszystkie klasy) -- kontrola sladu akwizycji
        m = np.array([abs(r['bw'] / 1e6 - 219.7) < 1 for r in Re])
        out['sets'][sname]['AUC_uav_bw220'] = auc(s[m & (yte == 'uav')], s[m & (yte != 'uav')])
    out['H1_AB_vs_A'] = bootstrap_delta(yte, keep['A_klasyczne'][0], keep['AB'][0], keep['A_klasyczne'][1], keep['AB'][1])
    # kontrola negatywna: permutacja etykiet dev (200x) -> AUC na eval zestawu AB
    rng = np.random.default_rng(3); Xtr, _ = matrix(Rd, SETS['AB']); Xte, _ = matrix(Re, SETS['AB'])
    perm = [fit_eval(Xtr, rng.permutation(ytr), Xte, yte)[1] for _ in range(200)]
    out['perm_AUC_AB'] = [float(np.percentile(perm, 50)), float(np.percentile(perm, 95))]
    # H4: dualnosc / rytm (przewidywania z rozwoju)
    ch = np.array([r['char'] for r in Re], float); sv = np.array([r['sieve'] for r in Re], float)
    out['H4'] = {
        'P_median': {c: float(np.nanmedian(ch[yte == c, 1])) for c in io.CLASSES},
        'P_AUC_uav_lower': 1 - auc(ch[yte == 'uav', 1][np.isfinite(ch[yte == 'uav', 1])], ch[yte != 'uav', 1][np.isfinite(ch[yte != 'uav', 1])]),
        'alpha_median': {c: float(np.nanmedian(sv[yte == c, 2])) for c in io.CLASSES},
    }
    return out


if __name__ == '__main__':
    import sys
    res = final()
    p = os.path.join(os.path.dirname(__file__), '..', 'docs', 'geometry', 'RESULT_OPEN_RADAR_MICRODOPPLER_v0_1.json')
    json.dump(res, open(p, 'w'), indent=1)
    print(json.dumps(res, indent=1))
