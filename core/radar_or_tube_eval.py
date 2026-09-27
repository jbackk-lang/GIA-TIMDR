"""Ocena v0.2: radar jako rura (PREREG_OPEN_RADAR_TUBE_v0_2). Jedno uruchomienie."""
import os, json, numpy as np
import radar_or_io as io, radar_or_eval as ev

SETS = {'A': ['dopp', 'jem', 'cvd'], 'T': ['tube'], 'A+T': ['dopp', 'jem', 'cvd', 'tube'], 'B+T': ['sieve', 'char', 'tube']}
PART_IDX = 6 + 1   # T_particle_p90 w wektorze tube (6 median + 6 p90)


def load(part):
    R = ev.load(part, 'v0_1'); d = os.path.join(io.DATA, f'feat_tube_v0_1_{part}')
    for r, f in zip(R, sorted(os.listdir(d))):
        t = json.load(open(os.path.join(d, f))); assert t['cls'] == r['cls']; r['tube'] = t['tube']
    return R


def boot(y, s1, s2, n=2000, seed=1):
    rng = np.random.default_rng(seed); idx = {c: np.where(y == c)[0] for c in io.CLASSES}; v = []
    for _ in range(n):
        ii = np.concatenate([rng.choice(w, len(w)) for w in idx.values()]); yy = y[ii]
        v.append(ev.auc(s2[ii][yy == 'uav'], s2[ii][yy != 'uav']) - ev.auc(s1[ii][yy == 'uav'], s1[ii][yy != 'uav']))
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


def final():
    Rd, Re = load('dev'), load('eval')
    ytr = np.array([r['cls'] for r in Rd]); yte = np.array([r['cls'] for r in Re])
    out = {'sets': {}}; S = {}
    for k, g in SETS.items():
        Xtr, _ = ev.matrix(Rd, g); Xte, _ = ev.matrix(Re, g)
        f1, a, s, yp = ev.fit_eval(Xtr, ytr, Xte, yte); S[k] = s
        out['sets'][k] = {'macroF1': f1, 'AUC_uav': a, 'AUC_uav_CI95': ev.auc_ci(yte, s)}
    d1 = out['sets']['A+T']['AUC_uav'] - out['sets']['A']['AUC_uav']; c1 = boot(yte, S['A'], S['A+T'])
    out['H1_AT_vs_A'] = {'dAUC': d1, 'CI95': c1, 'verdict': 'SUPPORTED' if c1[0] > 0 else ('NOT SUPPORTED' if d1 <= 0 else 'MIXED')}
    d2 = out['sets']['B+T']['AUC_uav'] - out['sets']['A']['AUC_uav']; c2 = boot(yte, S['A'], S['B+T'], seed=2)
    out['H2_BT_vs_A'] = {'dAUC': d2, 'CI95': c2,
                         'verdict': 'SUPPORTED (nie gorszy)' if c2[0] > -0.05 else ('NOT SUPPORTED' if c2[1] < 0 else 'MIXED')}
    p = np.array([r['tube'][PART_IDX] for r in Re]); a3 = ev.auc(p[yte == 'uav'], p[yte != 'uav'])
    ci3 = ev.auc_ci(yte, p)
    out['H3_particle_uav'] = {'AUC': a3, 'CI95': ci3, 'verdict': 'SUPPORTED' if ci3[0] > 0.5 else 'NOT SUPPORTED',
                              'median': {c: float(np.median(p[yte == c])) for c in io.CLASSES}}
    return out


if __name__ == '__main__':
    r = final()
    json.dump(r, open(os.path.join(os.path.dirname(__file__), '..', 'docs', 'geometry', 'RESULT_OPEN_RADAR_TUBE_v0_2.json'), 'w'), indent=1)
    print(json.dumps(r, indent=1))
