"""Reproducible CHF ablation pilot: synthetic signals or public SciPy ECG.

Usage:
  python research/chrono_helix_fusion/benchmark.py --source synthetic
  python research/chrono_helix_fusion/benchmark.py --source ecg
Dependencies: numpy scipy scikit-learn
Results are exploratory; synthetic labels do NOT establish real-world superiority.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy import datasets, signal, stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupShuffleSplit

FS = 360
N = 720


def synthetic(seed=42, n_groups=60, windows_per_group=8):
    rng = np.random.default_rng(seed)
    xs, ys, groups = [], [], []
    for g in range(n_groups):
        freq = rng.uniform(4, 12)
        for j in range(windows_per_group):
            t = np.arange(N) / FS
            x = np.sin(2 * np.pi * freq * t + rng.uniform(0, 2*np.pi))
            x += rng.normal(0, 0.30, N)
            y = int(j % 2 == 1)
            if y:
                # Phase reset / transient: time structure differs, often with modest spectral change
                cut = rng.integers(N // 3, 2*N // 3)
                x[cut:] = np.sin(2*np.pi*freq*t[cut:] + rng.uniform(0, 2*np.pi)) + rng.normal(0, 0.30, N-cut)
            xs.append(x)
            ys.append(y)
            groups.append(g)
    return np.asarray(xs), np.asarray(ys), np.asarray(groups)


def ecg_windows():
    try:
        x = datasets.electrocardiogram()
    except Exception as exc:
        raise RuntimeError("ECG download unavailable. Use --source synthetic, or enable internet access.") from exc
    # No validated anomaly labels for this particular segmentation.
    # Thus ECG is feature-extraction only; do not invent diagnostic labels.
    return [x[i:i+N] for i in range(0, len(x)-N+1, N)]


def extract(x, fs=FS):
    x = np.asarray(x, dtype=float)
    x = x - np.median(x)
    a = signal.hilbert(x)
    amp = np.abs(a)
    phase = np.unwrap(np.angle(a))
    f = np.diff(phase)*fs/(2*np.pi)
    z = np.column_stack([a.real, a.imag, np.arange(len(x))/fs])
    v = np.gradient(z, 1/fs, axis=0)
    acc = np.gradient(v, 1/FS, axis=0)
    curvature = np.linalg.norm(np.cross(v, acc), axis=1)/(np.linalg.norm(v, axis=1)**3+1e-8)
    spectrum = np.abs(np.fft.rfft(x))**2
    spectrum /= spectrum.sum()+1e-12
    bins = np.array_split(spectrum, 8)
    base = [float(np.sqrt(np.mean(x*x))), float(stats.kurtosis(x, fisher=True)),
            *[float(b.sum()) for b in bins]]
    chrono = [float(np.mean(np.abs(np.diff(x)))), float(np.std(np.diff(x))),
              float(np.mean(np.abs(np.diff(x, n=2))))]
    helix = [float(np.median(curvature)), float(np.quantile(curvature, .9))]
    branches = [float(np.mean(amp)), float(np.std(amp)),
                float(np.median(f)), float(np.std(np.clip(f, -fs/2, fs/2)))]
    # Tri-node proxies: coupling between temporal variation of amplitude,
    # curvature and phase speed, without claiming causal interactions.
    da = np.diff(amp)
    dc = np.diff(np.clip(curvature, 0, np.quantile(curvature, .99)))
    df = np.diff(np.clip(f, -fs/2, fs/2))
    m = min(len(da),len(dc),len(df))
    def corr(a,b):
        if np.std(a[:m]) < 1e-9 or np.std(b[:m]) < 1e-9:
            return 0.
        return float(np.corrcoef(a[:m],b[:m])[0,1])
    tri = [corr(da,dc),corr(dc,df),corr(df,da)]
    return base, chrono, helix, branches, tri


def run_synthetic():
    xs, y, groups = synthetic()
    parts = [extract(x) for x in xs]
    feature_sets = {
        "baseline_fft_stats": [0],
        "baseline_plus_chrono": [0,1],
        "baseline_chrono_helix": [0,1,2],
        "baseline_chrono_helix_branches": [0,1,2,3],
        "baseline_chrono_helix_branches_trinode": [0,1,2,3,4],
    }
    splitter = GroupShuffleSplit(n_splits=1, test_size=.25, random_state=42)
    train, test = next(splitter.split(xs, y, groups))
    report = {"source":"synthetic", "seed":42, "n_windows":len(xs),
              "n_groups":len(np.unique(groups)), "train_groups":len(np.unique(groups[train])),
              "test_groups":len(np.unique(groups[test])), "results":{}}
    for name, indices in feature_sets.items():
        X = np.asarray([[v for k in indices for v in p[k]] for p in parts])
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
        clf.fit(X[train], y[train])
        prob = clf.predict_proba(X[test])[:,1]
        report["results"][name] = {"auroc":round(float(roc_auc_score(y[test],prob)),4),
                                    "auprc":round(float(average_precision_score(y[test],prob)),4)}
    report["caveat"] = "One synthetic split; no independent real-world validation, no Möbius test."
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",choices=["synthetic","ecg"],default="synthetic")
    args=parser.parse_args()
    if args.source=="synthetic":
        report=run_synthetic()
    else:
        windows=ecg_windows()
        feats=[extract(x) for x in windows]
        report={"source":"scipy_ecg","n_windows":len(feats),
                "mean_features_by_branch":[np.mean([p[k] for p in feats],axis=0).tolist() for k in range(5)],
                "caveat":"Unlabeled ECG; descriptive features only, no diagnostic performance."}
    output=Path(__file__).with_name("benchmark_"+args.source+".json")
    output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
