"""Unsupervised CHF event-discovery pilot: impulses, dropouts, relation changes.

No claim of novelty: compare against raw-energy and phase-locking controls.
Run: python research/chrono_helix_fusion/event_discovery.py --source synthetic
     python research/chrono_helix_fusion/event_discovery.py --source ecg
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy import datasets, signal

def make_synthetic(seed=71, fs=360, duration=120):
    rng=np.random.default_rng(seed)
    t=np.arange(fs*duration)/fs
    x=np.sin(2*np.pi*7*t)+.3*np.sin(2*np.pi*13*t+.4)+rng.normal(0,.13,len(t))
    events=[]
    for sec in (16,35,58,79,103):
        p=int(sec*fs); width=int(.28*fs)
        # deliberately injected disappearance of a high-frequency component
        x[p:p+width]-=.3*np.sin(2*np.pi*13*t[p:p+width]+.4)
        events.append({"sample":p,"type":"injected_component_dropout"})
    return x,fs,events

def descriptors(x,fs,window=720,hop=180):
    x=np.asarray(x,float)
    if x.ndim!=1 or len(x)<window or not np.isfinite(x).all():
        raise ValueError("Need a finite mono recording at least one window long")
    centers=[]; rows=[]
    for start in range(0,len(x)-window+1,hop):
        w=x[start:start+window]
        # Two-band analytic phase relation: operational proxy, not new physics.
        lo=signal.sosfiltfilt(signal.butter(3,[5,9],btype="bandpass",fs=fs,output="sos"),w)
        hi=signal.sosfiltfilt(signal.butter(3,[11,15],btype="bandpass",fs=fs,output="sos"),w)
        p1=np.angle(signal.hilbert(lo))
        p2=np.angle(signal.hilbert(hi))
        # Local phase concentration of relative phase (not cross-frequency PLV).
        phase_rel=np.exp(1j*(p2-p1))
        phase_consistency=float(abs(np.mean(phase_rel)))
        rms=float(np.sqrt(np.mean(w*w)))
        hi_power=float(np.mean(hi*hi))
        # Energy independent, dimensionless relation-change proxy.
        sub=np.array_split(phase_rel,4)
        local=np.array([abs(np.mean(z)) for z in sub])
        relation_instability=float(np.std(local))
        centers.append(start+window//2)
        rows.append([rms,hi_power,phase_consistency,relation_instability])
    return np.asarray(centers),np.asarray(rows)

def robust_outliers(values):
    median=np.median(values,axis=0)
    scale=1.4826*np.median(abs(values-median),axis=0)
    z=(values-median)/np.maximum(scale,1e-8)
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",choices=["synthetic","ecg"],default="synthetic")
    ap.add_argument("--output",type=Path,default=Path("event_discovery_report.json"))
    args=ap.parse_args()
    if args.source=="synthetic":
        x,fs,known=make_synthetic()
    else:
        x=np.asarray(datasets.electrocardiogram(),float)
        fs=360;known=[]
    centers,features=descriptors(x,fs)
    z=robust_outliers(features)
    names=["rms","high_band_energy","phase_concentration","relation_instability"]
    # Candidate discoveries are ranked; no labels or p-values are inferred.
    candidates={}
    for k,name in enumerate(names):
        order=np.argsort(-abs(z[:,k]))[:10]
        candidates[name]=[{"time_seconds":round(float(centers[j]/fs),3),
                            "robust_z":round(float(z[j,k]),3)} for j in order]
    report={"source":args.source,"sampling_hz":fs,"n_samples":len(x),
            "n_windows":len(centers),"feature_names":names,
            "candidate_events":candidates,"injected_events":known,
            "status":"exploratory_not_novelty_proof",
            "caveats":["Synthetic events are deliberately injected, not discovered in nature.",
                       "ECG is unlabelled; candidate events are not clinical findings.",
                       "Phase concentration is an existing-style statistic; test alternative phase and spectral controls.",
                       "Overlapping windows are dependent; do not treat peaks as independent discoveries.",
                       "Filter edges and band choices can generate artifacts; verify on independent recordings."]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"source":args.source,"n_windows":len(centers),"report":str(args.output)}))
if __name__=="__main__": main()
