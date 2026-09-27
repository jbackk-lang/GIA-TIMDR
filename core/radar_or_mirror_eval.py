"""Ocena Open Radar v0.3 (lustro / cien) -- zamrozona w PREREG_OPEN_RADAR_MIRROR_v0_3.md. Jedno uruchomienie:
python radar_or_mirror.py eval && python radar_or_mirror_eval.py"""
import json, os
import numpy as np
from scipy.stats import mannwhitneyu
from radar_or_eval import lda_fit, lda_scores, impute, auc, macro_f1

DATA = os.path.join(os.path.dirname(__file__), '..', '..', 'DATA', 'open_radar')
CL = ['person', 'bicycle', 'uav', 'vehicle']
MN = ['coh_near', 'cos_near', 'R_near', 'coh_far', 'cos_far', 'R_far', 'R_all', 'Q', 'alpha']
TARGETS = ['person', 'bicycle', 'uav']


def sets(part):
    R = json.load(open(os.path.join(DATA, f'feat_mirror_v0_3_{part}.json')))
    A = []
    for r in R:
        j = json.load(open(os.path.join(DATA, f'feat_v0_1_{part}', r['track'] + '.json'))); A.append(j['dopp'] + j['jem'] + j['cvd'])
    S = {'A_v01': np.array(A, float), 'C_full': np.array([r['C'] for r in R], float), 'M': np.array([r['M'] for r in R], float)}
    S['C+M'] = np.hstack([S['C_full'], S['M']]); S['A+C'] = np.hstack([S['A_v01'], S['C_full']])
    S['A+C+M'] = np.hstack([S['A+C'], S['M']])
    return R, np.array([r['cls'] for r in R]), S


def fit_eval(Xtr, ytr, Xte):
    Xtr, Xte = impute(Xtr, Xte)
    m = lda_fit(Xtr, ytr); yp = m['ks'][np.argmax(lda_scores(m, Xte), 1)]
    sc = {}
    for c in TARGETS:
        mb = lda_fit(Xtr, np.where(ytr == c, c, 'rest')); s = lda_scores(mb, Xte); ks = list(mb['ks'])
        sc[c] = s[:, ks.index(c)] - s[:, ks.index('rest')]
    return yp, sc


def boot(y, fn, n=2000, seed=1):
    rng = np.random.default_rng(seed); idx = [np.where(y == c)[0] for c in CL]; v = []
    for _ in range(n):
        ii = np.concatenate([rng.choice(w, len(w)) for w in idx]); v.append(fn(ii))
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


def verdict(ci, point):
    return 'SUPPORTED' if ci[0] > 0 else ('MIXED' if point > 0 else 'NOT SUPPORTED')


def final():
    Rd, yd, Sd = sets('dev'); Re, ye, Se = sets('eval')
    out = {'n_dev': len(yd), 'n_eval': len(ye), 'eval_counts': {c: int((ye == c).sum()) for c in CL}, 'sets': {}}
    keep = {}
    bw220 = np.array([abs(r['bw'] / 1e6 - 219.7) < 1 for r in Re])
    for nm in Sd:
        yp, sc = fit_eval(Sd[nm], yd, Se[nm]); keep[nm] = (yp, sc)
        o = {'macroF1': macro_f1(ye, yp)}
        for c in TARGETS:
            o[f'AUC_{c}'] = auc(sc[c][ye == c], sc[c][ye != c])
            m = bw220
            o[f'AUC_{c}_bw220'] = auc(sc[c][m & (ye == c)], sc[c][m & (ye != c)]) if (m & (ye == c)).any() else None
        out['sets'][nm] = o
    # H1: A+C+M vs A+C, macro-F1
    f = lambda ii: macro_f1(ye[ii], keep['A+C+M'][0][ii]) - macro_f1(ye[ii], keep['A+C'][0][ii])
    d = out['sets']['A+C+M']['macroF1'] - out['sets']['A+C']['macroF1']; ci = boot(ye, f)
    out['H1'] = {'dF1': d, 'CI95': ci, 'verdict': verdict(ci, d)}
    # H2: rower vs reszta, M vs A_v01 (AUC)
    def fa(a, b, c):
        return lambda ii: (auc(keep[b][1][c][ii][ye[ii] == c], keep[b][1][c][ii][ye[ii] != c])
                           - auc(keep[a][1][c][ii][ye[ii] == c], keep[a][1][c][ii][ye[ii] != c]))
    d = out['sets']['M']['AUC_bicycle'] - out['sets']['A_v01']['AUC_bicycle']; ci = boot(ye, fa('A_v01', 'M', 'bicycle'))
    out['H2'] = {'dAUC_bicycle_M_vs_A': d, 'CI95': ci, 'verdict': verdict(ci, d),
                 'M_vs_C_full_bicycle': out['sets']['M']['AUC_bicycle'] - out['sets']['C_full']['AUC_bicycle']}
    # H3: stereoskopia -- kierunki z rozwoju, Mann-Whitney jednostronny
    M = Se['M']; col = {n: i for i, n in enumerate(MN)}
    def mw(v, pos, greater):
        a = v[ye == pos]; b = v[ye != pos]; a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
        p = mannwhitneyu(a, b, alternative='greater' if greater else 'less').pvalue
        return {'median_pos': float(np.median(a)), 'median_rest': float(np.median(b)), 'p': float(p)}
    h3 = {'person_cos_far_wiekszy': mw(M[:, col['cos_far']], 'person', True),
          'person_R_far_mniejszy': mw(M[:, col['R_far']], 'person', False),
          'bicycle_R_all_wiekszy': mw(M[:, col['R_all']], 'bicycle', True)}
    k = sum(v['p'] < 0.05 for v in h3.values())
    h3['verdict'] = 'SUPPORTED' if k == 3 else ('MIXED' if k > 0 else 'NOT SUPPORTED'); out['H3'] = h3
    # H4: wykonalnosc -- dron poza zasiegiem (przewidywana porazka M: AUC_uav < 0,70)
    a = out['sets']['M']['AUC_uav']
    out['H4'] = {'AUC_uav_M': a, 'przewidywanie_potwierdzone': bool(a < 0.70),
                 'N_cyk>=10': {c: float(np.mean([r['info'].get('N_cyk', 0) >= 10 for r, yy in zip(Re, ye) if yy == c])) for c in CL}}
    # kontrola negatywna: permutacja etykiet dev (200x), A+C+M
    rng = np.random.default_rng(3)
    out['perm_macroF1_ACM'] = [float(np.percentile(v, q)) for v in
                               [[macro_f1(ye, fit_eval(Sd['A+C+M'], rng.permutation(yd), Se['A+C+M'])[0]) for _ in range(200)]] for q in (50, 95)]
    out['mediany_eval'] = {n: {c: float(np.nanmedian(M[ye == c, i])) for c in CL} for n, i in col.items()}
    return out


if __name__ == '__main__':
    res = final()
    p = os.path.join(os.path.dirname(__file__), '..', 'docs', 'geometry', 'RESULT_OPEN_RADAR_MIRROR_v0_3.json')
    json.dump(res, open(p, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
