"""Post-impulse fading phase memory: honest FFT-vs-phase negative control.

Run: python research/chrono_helix_fusion/afterglow_probe.py
Requires numpy scipy scikit-learn.
"""
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def run():
    rng=np.random.default_rng(204)
    fs=200
    t=np.arange(fs*8)/fs
    rows=[]
    for group in range(100):
        phi=rng.uniform(0,2*np.pi)
        noise=rng.normal(0,.06,len(t))
        amp=rng.uniform(.8,1.2)
        for bit in (0,1):
            # Known synthetic memory state: phase shift decays after t=2s.
            memory=(.55 if bit else 0)*np.exp(-np.maximum(t-2,0)/2)*(t>=2)
            x=amp*np.sin(2*np.pi*9*t+phi+memory)+.35*np.sin(2*np.pi*18*t+2*phi)+noise
            w=x[(t>=2.5)&(t<4.5)]
            f=np.fft.rfft(w)
            freqs=np.fft.rfftfreq(len(w),1/fs)
            c9=f[np.argmin(abs(freqs-9))]
            c18=f[np.argmin(abs(freqs-18))]
            rel=np.angle(c18*np.conj(c9)**2)
            rows.append((group,bit,float(np.sqrt(np.mean(w*w))),float(np.sin(rel)),float(np.cos(rel)),np.abs(f)))
    y=np.array([r[1] for r in rows])
    groups=np.array([r[0] for r in rows])
    sets={'rms':np.array([[r[2]] for r in rows]),
          'fft_magnitude':np.array([r[5] for r in rows]),
          'relative_phase':np.array([[r[3],r[4]] for r in rows])}
    result={}
    splits=list(GroupShuffleSplit(n_splits=20,test_size=.3,random_state=7).split(sets['rms'],y,groups))
    for name,X in sets.items():
        scores=[]
        for train,test in splits:
            model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))
            model.fit(X[train],y[train])
            scores.append(float(roc_auc_score(y[test],model.predict_proba(X[test])[:,1])))
        result[name]={'auroc_mean':float(np.mean(scores)),
                      'auroc_std':float(np.std(scores)),
                      'split_aurocs':scores}
    return {'source':'synthetic_fading_phase_state','seed':204,
            'pairs':100,'splits':20,'sample_rate_hz':fs,
            'impulse_time_seconds':2,'observed_interval_seconds':[2.5,4.5],
            'phase_memory_time_constant_seconds':2,
            'results':result,
            'interpretation':'RMS misses the constructed fading state, but FFT magnitude and harmonic phase both decode it. No CHF-specific advantage.',
            'limitations':['Memory dynamics are imposed in a toy model, not observed in nature.',
                           'This is a negative control for novelty; full CHF is not tested.',
                           'Overlapping samples within pairs share noise; split by pair.',
                           'No independent physical validation or statistical novelty claim.']}

if __name__=='__main__':
    report=run()
    out=Path(__file__).with_name('afterglow_probe_results.json')
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
