"""LUMO: stosunki czestotliwosci (odniesienie z samej stali) w roznych porach roku + wykrycie uszkodzen stezen.
PREREG_LUMO_RATIOS_v0_1. Kotwice z rozwoju (dam6_111, zdrowe, X 2020): szczyty sredniego widma, prominencja >= 2,
odstep >= 8%. Samokorekta +-4% i interpolacja paraboliczna w kazdym bloku 10-min."""
import json, os
import numpy as np
from scipy.stats import spearmanr

LUMO = os.path.join(os.path.dirname(__file__), '..', '..', 'DATA', 'lumo')
ANCH = [2.82, 13.41, 16.33, 39.62, 71.42, 92.29, 101.01, 117.39]
DEV = 'exemplary_datasets_dam6_111'


def load():
    d = np.load(os.path.join(LUMO, 'lumo_spectra.npz'))
    case = np.array([k.split('/')[0].replace('exemplary_datasets_', '') for k in d['keys']])
    healthy = np.char.find(d['state'], 'Healthy') >= 0
    return d['f'], d['S'], d['temp'], case, healthy


def freqs(f, S):
    out = np.zeros((len(S), len(ANCH))); df = f[1] - f[0]
    for b in range(len(S)):
        s = np.log(S[b].mean(0))
        for k, a in enumerate(ANCH):
            m = np.where(np.abs(f - a) <= 0.04 * a)[0]; j = m[np.argmax(s[m])]
            y0, y1, y2 = s[j - 1:j + 2]; out[b, k] = f[j] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12) * df
    return out


def variants(F, T, ref_mask):
    ref = np.median(F[ref_mask], 0); raw = F / ref - 1
    s = np.median(F / ref, 1); norm = F / (s[:, None] * ref) - 1
    reg = np.zeros_like(raw)
    for k in range(F.shape[1]):
        p = np.polyfit(T[ref_mask], raw[ref_mask, k], 1); reg[:, k] = raw[:, k] - np.polyval(p, T)
    return {"surowe": raw, "stosunki": norm, "termometr": reg}, s


def final():
    import sys; sys.path.insert(0, os.path.dirname(__file__))
    from real_lanl_3story_bridge import novelty
    from radar_or_eval import auc
    f, S, T, case, h = load(); F = freqs(f, S); dev = case == 'dam6_111'
    X, s = variants(F, T, dev & h); test = ~dev
    res = {"prereg": "PREREG_LUMO_RATIOS_v0_1.md", "n_test_zdrowe": int((test & h).sum()), "n_test_uszk": int((test & ~h).sum()),
           "T_test_zakres": [float(T[test].min()), float(T[test].max())], "warianty": {}}
    for n, Y in X.items():
        tr = Y[dev & h]; sc = novelty(tr, Y)
        o = {"AUC_wszystkie": auc(sc[test & ~h], sc[test & h])}
        for c in sorted(set(case[test])):
            o[f"AUC_{c}"] = auc(sc[(case == c) & ~h], sc[test & h])
        o["falszywe_alarmy_p95"] = float(np.mean(sc[test & h] > np.percentile(novelty(tr, tr, loo=True), 95) * 1.0))
        res["warianty"][n] = o
    W = res["warianty"]; d = W["stosunki"]["AUC_wszystkie"] - W["surowe"]["AUC_wszystkie"]
    res["H1"] = {"dAUC_stosunki-surowe": d, "verdict": "SUPPORTED" if d > 0.02 else ("MIXED" if d > -0.02 else "NOT SUPPORTED")}
    small = ["dam3_010", "dam4_010", "dam6_010"]
    k = sum(W["stosunki"][f"AUC_{c}"] > W["surowe"][f"AUC_{c}"] for c in small)
    res["H2"] = {"pojedyncze_prety_stosunki>surowe": int(k), "verdict": "SUPPORTED" if k >= 2 else "NOT SUPPORTED"}
    res["opisowo_rho_s_T_test_zdrowe"] = float(spearmanr(T[test & h], s[test & h]).correlation)
    p = os.path.join(os.path.dirname(__file__), '..', 'docs', 'geometry', 'RESULT_LUMO_RATIOS_v0_1.json')
    json.dump(res, open(p, 'w'), indent=1, ensure_ascii=False)
    return res


if __name__ == '__main__':
    r = final(); print(json.dumps(r, indent=1, ensure_ascii=False))
