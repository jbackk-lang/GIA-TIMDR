"""Controlled phase-memory benchmark: same FFT magnitudes, different phase code.

This demonstrates known phase information, NOT an unknown physical memory
or a validated CHF advantage. Reproduce: python phase_memory_probe.py
Dependencies: numpy scipy scikit-learn.
"""
import json
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

def run():
    rng=np.random.default_rng(20261119)
    fs=256; n=512
    spectra=[];phase_features=[];labels=[];groups=[]
    pair_errors=[]
    for group in range(80):
        base=rng.uniform(-np.pi,np.pi)
        amplitude=rng.uniform(.28,.52)
        pair=[]
        for bit in (0,1):
            t=np.arange(n)/fs
            x=np.sin(2*np.pi*8*t+base)+amplitude*np.sin(
                2*np.pi*16*t+2*base+(np.pi/2 if bit else -np.pi/2))
            fft=np.fft.rfft(x)
            mag=np.abs(fft)
            spectra.append(mag)
            # Relative harmonic phase is invariant to a shared time shift.
            relation=np.angle(fft[32]*np.conj(fft[16])**2)
            phase_features.append([np.sin(relation),np.cos(relation)])
            labels.append(bit);groups.append(group);pair.append(mag)
        pair_errors.append(float(np.max(np.abs(pair[0]-pair[1]))))
    y=np.array(labels);groups=np.array(groups)
    scores={}
    splitter=GroupShuffleSplit(n_splits=10,test_size=.25,random_state=42)
    for name,features in [('fft_magnitude',np.array(spectra)),
                          ('harmonic_relative_phase',np.array(phase_features))]:
        auc=[]
        for train,test in splitter.split(features,y,groups):
            model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))
            model.fit(features[train],y[train])
            auc.append(float(roc_auc_score(y[test],model.predict_proba(features[test])[:,1])))
        scores[name]={'mean_auroc':float(np.mean(auc)),'std_auroc':float(np.std(auc)),
                      'split_aurocs':auc}
    return {'source':'synthetic_known_phase_code','n_pairs':80,
            'sampling_hz':fs,'window_samples':n,'max_pair_fft_magnitude_difference':max(pair_errors),
            'scores':scores,
            'interpretation':'A known constructed phase code is not visible in FFT magnitude; phase relations decode it.',
            'caveats':['No real physical system or natural memory mechanism was tested.',
                       'Not a CHF helix/trinode/bridge evaluation.',
                       'FFT phase and higher-order spectra can capture this known effect.',
                       'The phase code is imposed by construction, not discovered.']}

if __name__=='__main__':
    result=run()
    path=Path(__file__).with_name('phase_memory_probe_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
