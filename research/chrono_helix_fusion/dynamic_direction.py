"""Time-reversal dynamic direction control: same global FFT magnitudes."""
import json
from pathlib import Path
import numpy as np
from scipy.signal import chirp, stft
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

def run():
    rng=np.random.default_rng(20261119);fs=256;n=1024;t=np.arange(n)/fs
    xfft=[];xdyn=[];labels=[];groups=[];errors=[]
    for g in range(80):
        f0=rng.uniform(6,13);f1=rng.uniform(27,52)
        x=chirp(t,f0=f0,f1=f1,t1=t[-1],method='linear',phi=rng.uniform(0,360))
        x=x+.04*rng.normal(size=n)
        a=x;b=x[::-1].copy()
        errors.append(float(np.max(abs(abs(np.fft.rfft(a))-abs(np.fft.rfft(b))))))
        for bit,w in enumerate([a,b]):
            xfft.append(abs(np.fft.rfft(w)))
            freq,tt,z=stft(w,fs=fs,nperseg=128,noverlap=96,boundary=None)
            cent=(freq[:,None]*abs(z)**2).sum(axis=0)/(abs(z)**2).sum(axis=0)
            xdyn.append([float(np.polyfit(tt,cent,1)[0])])
            labels.append(bit);groups.append(g)
    y=np.array(labels);groups=np.array(groups)
    results={}
    for name,features in [('global_fft_magnitude',np.array(xfft)),
                          ('spectral_centroid_drift',np.array(xdyn))]:
        auc=[]
        for tr,te in GroupShuffleSplit(n_splits=20,test_size=.25,random_state=42).split(features,y,groups):
            model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000))
            model.fit(features[tr],y[tr])
            auc.append(float(roc_auc_score(y[te],model.predict_proba(features[te])[:,1])))
        results[name]={'mean_auroc':float(np.mean(auc)),'std_auroc':float(np.std(auc))}
    return {'experiment':'time_reversal_dynamic_direction','pairs':80,
            'max_fft_magnitude_difference':max(errors),'results':results,
            'caveats':['Known STFT time-frequency direction; not a new signal feature.',
                       'Time reversal preserves FFT magnitudes by construction.',
                       'Full CHF helix/trinode/bridges not yet evaluated.',
                       'Synthetic chirps, not natural physical recordings.']}
if __name__=='__main__':
    result=run()
    path=Path(__file__).with_name('dynamic_direction_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
