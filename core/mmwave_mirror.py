"""mmWave 77 GHz (chod: utykanie / machanie rekami / ukryta butelka) -- lustro i cien, v0.4 radaru.

Ten sam most K<->G co Open Radar v0.3 (lustrzane polowki +-d wokol linii ciala, S = czesc wspolna, A = cien), teraz na
danych spelniajacych regule wykonalnosci: klatki ciagle co 40 ms, 16 s (N_cyk kroku ~ 30), kat obserwacji staly
(chod wprost od radaru i z powrotem). Wejscie: P[400 klatek, 128 binow Dopplera] z mmwave_extract.py.
Odniesienie klasyczne: CVD (szczyt kadencji i jego sila) + rozrzut Dopplera, na tych samych klatkach.
"""
import glob, json, os
import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import csd, welch

PROC = os.path.join(os.path.dirname(__file__), '..', '..', 'DATA', 'mmwave', 'proc')
FSM, NB, ZERO = 25.0, 128, 64
BANDS = [(1 + 4 * k, 5 + 4 * k) for k in range(10)]        # |d| w binach Dopplera: 1-40
NEAR, FAR = range(0, 3), range(3, 10)
ALPHA = (0.5, 5.0); NPER = 128


def body_line(P):
    Pm = P.copy(); Pm[:, ZERO - 1:ZERO + 2] = 0                  # linia zerowa (resztki tla)
    return np.argmax(Pm, 1)


def halves(P):
    b = body_line(P); L = np.log(P + 1e-12)
    Ep, Em = [], []
    for lo, hi in BANDS:
        ip = np.clip(b[:, None] + np.arange(lo, hi)[None, :], 0, NB - 1); im = np.clip(b[:, None] - np.arange(lo, hi)[None, :], 0, NB - 1)
        Ep.append(np.log(np.exp(np.take_along_axis(L, ip, 1)).sum(1))); Em.append(np.log(np.exp(np.take_along_axis(L, im, 1)).sum(1)))
    d = lambda x: x - np.polyval(np.polyfit(np.arange(len(x)), x, 1), np.arange(len(x)))
    return np.array([d(x) for x in Ep]), np.array([d(x) for x in Em]), b


def mirror_feats(P):
    Ep, Em, b = halves(P)
    f, Ppp = welch(Ep, FSM, nperseg=NPER); _, Pmm = welch(Em, FSM, nperseg=NPER); _, Ppm = csd(Ep, Em, FSM, nperseg=NPER)
    _, PS = welch((Ep + Em) / 2, FSM, nperseg=NPER); _, PA = welch((Ep - Em) / 2, FSM, nperseg=NPER)
    sel = np.where((f >= ALPHA[0]) & (f <= ALPHA[1]))[0]
    norm = lambda X: X / (median_filter(X, size=(1, 9), mode='nearest') + 1e-30)
    sc = (norm(Ppp) + norm(Pmm)).sum(0)
    j2 = np.array([np.argmin(np.abs(f - 2 * f[j])) for j in sel])
    tot = sc[sel] + sc[j2]; j = sel[np.argmax(tot)]
    out = {'alpha': float(f[j]), 'Q': float(np.log(tot.max() / (2 * len(BANDS))))}
    for name, grp in (('near', NEAR), ('far', FAR)):
        g = list(grp); w = Ppp[g, j] + Pmm[g, j]; w = w / (w.sum() + 1e-30)
        out[f'coh_{name}'] = float((w * np.abs(Ppm[g, j]) ** 2 / (Ppp[g, j] * Pmm[g, j] + 1e-30)).sum())
        out[f'cos_{name}'] = float((w * np.real(Ppm[g, j]) / (np.abs(Ppm[g, j]) + 1e-30)).sum())
        out[f'R_{name}'] = float((w * PA[g, j] / (PA[g, j] + PS[g, j] + 1e-30)).sum())
    out['R_all'] = float(PA[:, sel].sum() / (PA[:, sel].sum() + PS[:, sel].sum() + 1e-30))
    return [out[k] for k in ('coh_near', 'cos_near', 'R_near', 'coh_far', 'cos_far', 'R_far', 'R_all', 'Q', 'alpha')], out


def classic(P):
    """CVD: FFT po klatkach log-mocy kazdego binu (lokalne tlo), szczyt kadencji i sila; rozrzut Dopplera wokol ciala."""
    b = body_line(P); L = np.log(P + 1e-12)
    rel = np.clip(b[:, None] + np.arange(-40, 41)[None, :], 0, NB - 1); Lr = np.take_along_axis(L, rel, 1)
    Lr = Lr - np.polyval(np.polyfit(np.arange(len(Lr)), Lr, 1), np.arange(len(Lr))[:, None]) if False else Lr - Lr.mean(0)
    f, C = welch(Lr.T, FSM, nperseg=NPER); C = C / (median_filter(C, size=(1, 9), mode='nearest') + 1e-30)
    sel = (f >= ALPHA[0]) & (f <= ALPHA[1]); c = C[:, sel].sum(0)
    Pl = np.exp(Lr); p = Pl / Pl.sum(1, keepdims=True); d = np.arange(-40, 41)
    sd = np.sqrt((p * d ** 2).sum(1)); ent = -(p * np.log(p + 1e-30)).sum(1) / np.log(81)
    return [float(f[sel][np.argmax(c)]), float(np.log(c.max() / (np.median(c) + 1e-30))), float(np.median(sd)), float(np.median(ent))]


def load_all():
    rows = []
    for p in sorted(glob.glob(os.path.join(PROC, '*.npz'))):
        name = os.path.basename(p)[:-4]; cls, idx = name.rsplit('_', 1)
        P = np.load(p)['P'].astype(float); v, o = mirror_feats(P)
        rows.append({'cls': cls, 'idx': int(idx), 'M': v, 'C': classic(P), 'info': o})
    return rows


# ---------------- zamrozone: PREREG_MMWAVE_MIRROR_v0_4 ----------------
CLS = ['HidingBottle', 'Limping', 'SlowWalk_SwingingHands']
MN = ['coh_near', 'cos_near', 'R_near', 'coh_far', 'cos_far', 'R_far', 'R_all', 'Q', 'alpha']


def final():
    import sys; sys.path.insert(0, os.path.dirname(__file__))
    from scipy.stats import mannwhitneyu
    from radar_or_eval import lda_fit, lda_scores, auc, macro_f1
    A = load_all(); dev = [r for r in A if r['idx'] <= 11]; te = [r for r in A if r['idx'] >= 12]
    yd = np.array([r['cls'] for r in dev]); yt = np.array([r['cls'] for r in te])
    Sd = {'C': np.array([r['C'] for r in dev]), 'M': np.array([r['M'] for r in dev])}; Sd['C+M'] = np.hstack([Sd['C'], Sd['M']])
    St = {'C': np.array([r['C'] for r in te]), 'M': np.array([r['M'] for r in te])}; St['C+M'] = np.hstack([St['C'], St['M']])
    res = {'prereg': 'PREREG_MMWAVE_MIRROR_v0_4.md', 'n_dev': {c: int((yd == c).sum()) for c in CLS}, 'n_test': {c: int((yt == c).sum()) for c in CLS}, 'zestawy': {}}
    keep = {}
    for n in Sd:
        m = lda_fit(Sd[n], yd); yp = m['ks'][np.argmax(lda_scores(m, St[n]), 1)]; sc = {}
        for c in CLS:
            mb = lda_fit(Sd[n], np.where(yd == c, 'T', 'R')); s = lda_scores(mb, St[n]); ks = list(mb['ks']); sc[c] = s[:, ks.index('T')] - s[:, ks.index('R')]
        keep[n] = (yp, sc)
        res['zestawy'][n] = {'macroF1': macro_f1(yt, yp), **{f'AUC_{c}': auc(sc[c][yt == c], sc[c][yt != c]) for c in CLS}}
    rng = np.random.default_rng(1); idx = [np.where(yt == c)[0] for c in CLS]
    def boot(fn):
        v = [fn(np.concatenate([rng.choice(w, len(w)) for w in idx])) for _ in range(2000)]
        return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    ver = lambda ci, d: 'SUPPORTED' if ci[0] > 0 else ('MIXED' if d > 0 else 'NOT SUPPORTED')
    d = res['zestawy']['C+M']['macroF1'] - res['zestawy']['C']['macroF1']
    ci = boot(lambda ii: macro_f1(yt[ii], keep['C+M'][0][ii]) - macro_f1(yt[ii], keep['C'][0][ii]))
    res['H1'] = {'dF1_(C+M)-C': d, 'CI95': ci, 'verdict': ver(ci, d)}
    h = 'HidingBottle'; d = res['zestawy']['M'][f'AUC_{h}'] - res['zestawy']['C'][f'AUC_{h}']
    ci = boot(lambda ii: auc(keep['M'][1][h][ii][yt[ii] == h], keep['M'][1][h][ii][yt[ii] != h]) - auc(keep['C'][1][h][ii][yt[ii] == h], keep['C'][1][h][ii][yt[ii] != h]))
    res['H2'] = {'dAUC_ukryta_butelka_M-C': d, 'CI95': ci, 'verdict': ver(ci, d)}
    M = St['M']; col = {n: i for i, n in enumerate(MN)}
    def mw(a, b, greater):
        return {'med_a': float(np.median(a)), 'med_b': float(np.median(b)), 'p': float(mannwhitneyu(a, b, alternative='greater' if greater else 'less').pvalue)}
    h3 = {'R_all_butelka>reszta': mw(M[yt == h, col['R_all']], M[yt != h, col['R_all']], True),
          'cos_far_butelka<machanie': mw(M[yt == h, col['cos_far']], M[yt == 'SlowWalk_SwingingHands', col['cos_far']], False),
          'coh_near_machanie<reszta': mw(M[yt == 'SlowWalk_SwingingHands', col['coh_near']], M[yt != 'SlowWalk_SwingingHands', col['coh_near']], False)}
    k = sum(v['p'] < 0.05 for v in h3.values()); h3['verdict'] = 'SUPPORTED' if k == 3 else ('MIXED' if k else 'NOT SUPPORTED'); res['H3'] = h3
    a = M[:, col['alpha']]; lim = yt == 'Limping'
    n1, n2 = int((a[lim] < 1.2).sum()), int((a[~lim] > 1.2).sum())
    res['H4'] = {'utykanie_alfa<1,2Hz': n1, 'pozostale_alfa>1,2Hz': n2, 'verdict': 'SUPPORTED' if n1 >= 7 and n2 >= 14 else 'NOT SUPPORTED'}
    res['mediany_test'] = {n: {c: float(np.median(M[yt == c, i])) for c in CLS} for n, i in col.items()}
    p = os.path.join(os.path.dirname(__file__), '..', 'docs', 'geometry', 'RESULT_MMWAVE_MIRROR_v0_4.json')
    json.dump(res, open(p, 'w'), indent=1, ensure_ascii=False)
    return res


if __name__ == '__main__':
    r = final(); print(json.dumps({k: r[k] for k in ('zestawy', 'H1', 'H2', 'H3', 'H4')}, indent=1, ensure_ascii=False))
