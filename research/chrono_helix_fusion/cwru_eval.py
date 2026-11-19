"""CWRU 12 kHz drive-end pilot, leave-one-load-out evaluation.

Download files from official CWRU website and put them under --data-dir.
No implicit remote downloads; provenance remains under researcher control.
Usage: python research/chrono_helix_fusion/cwru_eval.py --data-dir data/cwru
Dependencies: numpy scipy scikit-learn
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.io import loadmat
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from benchmark import extract
from bridges import vector

# 0/1/2/3 HP load; normal vs three fault types, 0.007 inch defects.
RECORDS = {
    "normal":[97,98,99,100],
    "inner":[105,106,107,108],
    "ball":[118,119,120,121],
    "outer":[130,131,132,133],
}
FS = 12000
WINDOW = 2048


def read_drive_end(path, record):
    mat = loadmat(path)
    # Some MAT files contain extraneous channels; insist on the matching record ID.
    key = f"X{record:03d}_DE_time"
    if key not in mat:
        raise ValueError(f"{path}: missing expected channel {key}")
    x = np.asarray(mat[key], dtype=float).reshape(-1)
    if not np.isfinite(x).all():
        raise ValueError(f"{path}: non-finite data")
    return x


def dataset(folder, max_windows=25):
    xs, labels, loads, provenance = [], [], [], []
    for condition, records in RECORDS.items():
        for load, record in enumerate(records):
            path = folder / f"{record}.mat"
            if not path.is_file():
                raise FileNotFoundError(f"Download {record}.mat from official CWRU portal into {folder}")
            raw = path.read_bytes()
            x = read_drive_end(path, record)
            count = min(max_windows, len(x)//WINDOW)
            if count < 2:
                raise ValueError(f"{path}: too short")
            for i in range(count):
                xs.append(x[i*WINDOW:(i+1)*WINDOW])
                labels.append(int(condition != "normal"))
                loads.append(load)
            provenance.append({"record":record,"condition":condition,"load_hp":load,
                               "sha256":hashlib.sha256(raw).hexdigest(),"windows":count})
    return xs, np.array(labels), np.array(loads), provenance


def evaluate(folder):
    xs,y,loads,provenance = dataset(folder)
    # Preserve original 12 kHz sampling and full available bandwidth.
    feats=[extract(x, fs=FS) for x in xs]
    b=np.asarray([vector(x, fs=FS, max_lag=12) for x in xs])
    base=np.asarray([p[0] for p in feats])
    chrono=np.asarray([p[1] for p in feats])
    helix=np.asarray([p[2] for p in feats])
    branches=np.asarray([p[3] for p in feats])
    models={
        "fft_stats":base,
        "unbridged":np.column_stack([base,chrono,helix,branches]),
        "lagged_bridges":np.column_stack([base,chrono,helix,branches,b]),
    }
    scores={}
    for name,X in models.items():
        rows=[]
        for held_load in range(4):
            train=np.where(loads!=held_load)[0]
            test=np.where(loads==held_load)[0]
            assert not set(loads[train]) & set(loads[test])
            model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,random_state=42))
            model.fit(X[train],y[train])
            prob=model.predict_proba(X[test])[:,1]
            rows.append({"held_out_load_hp":held_load,
                         "auroc":float(roc_auc_score(y[test],prob)),
                         "auprc":float(average_precision_score(y[test],prob))})
        scores[name]=rows
    return {"status":"exploratory_real_data","dataset":"CWRU 12k DE, 0.007-inch defects",
            "sample_rate_original":FS,"sample_rate_processed":FS,
            "n_windows":len(xs),"files":provenance,"scores":scores,
            "limitations":["Full-band 12 kHz signal retained; Hilbert features may still need bandpass preprocessing.",
                           "Same physical fault construction may recur across loads; load holdout is not bearing holdout.",
                           "Non-overlapping windows from same recording are correlated.",
                           "No confidence intervals or external replication."]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    args=parser.parse_args()
    report=evaluate(args.data_dir)
    out=Path(__file__).with_name("cwru_results.json")
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"scores":report["scores"]},indent=2))


if __name__=="__main__":
    main()
