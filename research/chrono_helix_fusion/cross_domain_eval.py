"""Cross-domain CHF benchmark on labeled signal recordings.

Manifest CSV columns: path,label,group,fs,domain
path: relative to manifest directory (or absolute); .npy or single-column .csv
group: independent recording/device/session; never split a group across train/test
fs: sample rate in Hz; domain: e.g. electrical, mechanical, plasma

Run: python research/chrono_helix_fusion/cross_domain_eval.py --manifest data/signals.csv
Requires numpy, scipy, scikit-learn. No automatic data download.
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from benchmark import extract
from bridges import vector

WINDOW = 2048
MODELS = {
    "fft_stats": (0,),
    "chrono": (0, 1),
    "unbridged_chf": (0, 1, 2, 3),
    "chf_trinode": (0, 1, 2, 3, 4),
}

def load_signal(path):
    if path.suffix.lower() == ".npy":
        x = np.load(path, allow_pickle=False)
    elif path.suffix.lower() == ".csv":
        x = np.loadtxt(path, delimiter=",", ndmin=1)
    else:
        raise ValueError(f"Unsupported signal format: {path}")
    x = np.asarray(x, float).reshape(-1)
    if not np.isfinite(x).all() or len(x) < WINDOW:
        raise ValueError(f"Invalid/short recording: {path}")
    return x

def load_manifest(manifest, max_windows=25, rms_normalize=False):
    rows = list(csv.DictReader(manifest.open(encoding="utf-8-sig", newline="")))
    if not rows:
        raise ValueError("Empty manifest")
    for col in ("path", "label", "group", "fs", "domain"):
        if col not in rows[0]:
            raise ValueError(f"Missing manifest column: {col}")
    features, labels, groups, domains = [], [], [], []
    for row in rows:
        p = Path(row["path"])
        if not p.is_absolute():
            p = manifest.parent / p
        fs = float(row["fs"])
        if fs <= 0:
            raise ValueError("fs must be positive")
        x = load_signal(p)
        for i in range(min(max_windows, len(x) // WINDOW)):
            w = x[i*WINDOW:(i+1)*WINDOW].copy()
            if rms_normalize:
                w -= w.mean()
                w /= max(np.sqrt(np.mean(w*w)), 1e-12)
            p5 = extract(w, fs=fs)
            b = vector(w, fs=fs, max_lag=12)
            features.append((p5, b))
            labels.append(row["label"])
            groups.append(row["group"])
            domains.append(row["domain"])
    return features, np.asarray(labels), np.asarray(groups), np.asarray(domains)

def evaluate(manifest, seed=42, rms_normalize=False):
    feats, y, groups, domains = load_manifest(manifest, rms_normalize=rms_normalize)
    report = {"manifest": str(manifest), "seed": seed, "window_samples": WINDOW,
              "rms_normalized": rms_normalize, "n_windows": len(y),
              "n_groups": len(set(groups)), "domains": {}}
    for domain in sorted(set(domains)):
        ix = np.flatnonzero(domains == domain)
        yy, gg = y[ix], groups[ix]
        if len(set(gg)) < 4 or len(set(yy)) < 2:
            report["domains"][domain] = {"status": "insufficient_groups_or_classes"}
            continue
        splitter = GroupShuffleSplit(n_splits=5, test_size=.25, random_state=seed)
        splits = list(splitter.split(ix, yy, gg))
        results = {}
        for name, indices in MODELS.items():
            X = np.asarray([[v for k in indices for v in feats[j][0][k]] for j in ix])
            if name == "unbridged_chf":
                pass
            fold_scores = []
            for tr, te in splits:
                if len(set(yy[tr])) < 2 or len(set(yy[te])) < 2:
                    continue
                clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=seed))
                clf.fit(X[tr], yy[tr])
                pred = clf.predict(X[te])
                score = {"accuracy": float(accuracy_score(yy[te], pred)),
                         "macro_f1": float(f1_score(yy[te], pred, average="macro"))}
                if len(set(yy)) == 2:
                    score["auroc"] = float(roc_auc_score(yy[te], clf.predict_proba(X[te])[:, 1]))
                fold_scores.append(score)
            results[name] = fold_scores
        X = np.asarray([[v for k in (0, 1, 2, 3) for v in feats[j][0][k]] + feats[j][1] for j in ix])
        bridge_scores = []
        for tr, te in splits:
            if len(set(yy[tr])) < 2 or len(set(yy[te])) < 2:
                continue
            clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=seed))
            clf.fit(X[tr], yy[tr])
            pred = clf.predict(X[te])
            score = {"accuracy": float(accuracy_score(yy[te], pred)),
                     "macro_f1": float(f1_score(yy[te], pred, average="macro"))}
            if len(set(yy)) == 2:
                score["auroc"] = float(roc_auc_score(yy[te], clf.predict_proba(X[te])[:, 1]))
            bridge_scores.append(score)
        results["chf_lagged_bridges"] = bridge_scores
        report["domains"][domain] = {"status": "exploratory", "n_groups": len(set(gg)),
                                      "n_windows": len(ix), "scores_by_split": results}
    report["limitations"] = [
        "Within-domain only; not a trained cross-domain transfer test.",
        "Five grouped random splits are correlated; do not treat as independent experiments.",
        "Labels and group independence must be verified against source provenance.",
        "No physical interpretation of bridge correlations is established.",
        "Sampling rates and fixed sample windows imply different physical durations."
    ]
    return report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=Path("cross_domain_results.json"))
    ap.add_argument("--rms-normalize", action="store_true")
    args = ap.parse_args()
    report = evaluate(args.manifest, rms_normalize=args.rms_normalize)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
