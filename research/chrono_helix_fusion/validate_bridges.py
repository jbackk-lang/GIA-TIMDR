"""Repeated grouped holdout for CHF feature ablations. No external data needed.

Run: python research/chrono_helix_fusion/validate_bridges.py
Dependencies: numpy scipy scikit-learn
"""
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from benchmark import synthetic, extract
from bridges import vector


def main():
    xs, y, groups = synthetic(seed=42)
    parts = [extract(x) for x in xs]
    bridge = np.asarray([vector(x) for x in xs])
    base = np.asarray([p[0] for p in parts])
    chrono = np.asarray([p[1] for p in parts])
    helix = np.asarray([p[2] for p in parts])
    branches = np.asarray([p[3] for p in parts])
    original_tri = np.asarray([p[4] for p in parts])
    # Stronger control: all unbridged features vs same features + bridges.
    models = {
        "fft_stats":base,
        "unbridged_fusion":np.column_stack([base,chrono,helix,branches]),
        "original_trinode":np.column_stack([base,chrono,helix,branches,original_tri]),
        "lagged_bridges":np.column_stack([base,chrono,helix,branches,bridge]),
    }
    splits=GroupShuffleSplit(n_splits=20,test_size=.25,random_state=2026)
    scores={name:[] for name in models}
    split_groups=[]
    for train,test in splits.split(base,y,groups):
        assert not set(groups[train]) & set(groups[test])
        split_groups.append({"train":int(len(set(groups[train]))),
                             "test":int(len(set(groups[test])))})
        for name,X in models.items():
            model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1500,random_state=42))
            model.fit(X[train],y[train])
            pred=model.predict_proba(X[test])[:,1]
            scores[name].append({"auroc":float(roc_auc_score(y[test],pred)),
                                 "auprc":float(average_precision_score(y[test],pred))})
    summary={}
    for name, rows in scores.items():
        summary[name]={metric:{"mean":float(np.mean([r[metric] for r in rows])),
                               "sd":float(np.std([r[metric] for r in rows],ddof=1))}
                       for metric in ("auroc","auprc")}
    delta=np.array([a["auroc"]-b["auroc"] for a,b in zip(scores["lagged_bridges"],scores["unbridged_fusion"])])
    report={"status":"exploratory_synthetic","splits":20,"grouped":True,
            "model_summary":summary,
            "lagged_bridge_minus_unbridged_auroc":{"mean":float(delta.mean()),
                                                   "sd":float(delta.std(ddof=1)),
                                                   "positive_splits":int((delta>0).sum())},
            "caveats":["Repeated holdouts overlap and are not independent experimental replications.",
                       "Bridge lag selection uses within-window data; no causal inference.",
                       "Synthetic labels only; no real-world performance claims.",
                       "No Mobius topology test or correction for multiple comparisons."]}
    output=Path(__file__).with_name("validation_bridges.json")
    output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
