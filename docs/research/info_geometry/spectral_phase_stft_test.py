"""Fair-budget spectral phase / STFT comparison on synthetic TIMDR signals."""
import numpy as np
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,roc_auc_score
from spectral_relational_comparison import batch,autocorr

def features(x,t):
 x=x-x.mean(axis=1,keepdims=True)
 fft=np.fft.rfft(x,axis=1)[:,1:]
 mag=np.log1p(abs(fft)**2)
 # Cartesian complex FFT: retains phase, but is not translation invariant.
 complex_fft=np.column_stack((fft.real,fft.imag))
 # STFT magnitude (local time-frequency energy) with overlapping 32-point Hann windows.
 windows=np.lib.stride_tricks.sliding_window_view(x,32,axis=1)[:,::16,:]
 stft=np.log1p(abs(np.fft.rfft(windows*np.hanning(32),axis=2))**2).reshape(len(x),-1)
 return {'temporal':t[:,:3], 'fft_power':mag,'fft_complex_phase':complex_fft,
         'stft_power':stft,'autocorrelation':autocorr(x),
         'temporal+stft':np.column_stack((t[:,:3],stft))}

def run():
 datasets={'train':batch(2400,510),'validation':batch(800,511,True),'test_hard':batch(1200,512,True),'test_easy':batch(1200,513),'negative':batch(1200,514,True,True)}
 feats={k:features(v[0],v[1]) for k,v in datasets.items()}
 names=list(feats['train']); budgets=[3,8,16]
 results=[]
 for budget in budgets:
  for name in names:
   # Dimensionality reduction is learned ONLY on training data, never validation/test.
   prep=make_pipeline(StandardScaler(),PCA(n_components=budget,random_state=0)) if feats['train'][name].shape[1]>budget else StandardScaler()
   train=prep.fit_transform(feats['train'][name]); val=prep.transform(feats['validation'][name]);
   # Tune C on validation; hard test is untouched during selection.
   opts=[]
   for c in [.01,.1,1,10]:
    m=LogisticRegression(C=c,max_iter=1000).fit(train,datasets['train'][2]);p=m.predict_proba(val)[:,1]
    opts.append((accuracy_score(datasets['validation'][2],p>=.5),c,m))
   _,c,m=max(opts,key=lambda z:(z[0],-z[1]))
   line={'budget':budget,'feature':name,'C':c}
   for ds in ['validation','test_hard','test_easy','negative']:
    p=m.predict_proba(prep.transform(feats[ds][name]))[:,1]; y=datasets[ds][2]
    line[ds]=round(accuracy_score(y,p>=.5),4)
   results.append(line)
   print('RESULT',line,flush=True)
 print('SELECTED_BEST_VALIDATION')
 for budget in budgets:
  winner=max((r for r in results if r['budget']==budget),key=lambda z:z['validation'])
  print(budget,winner,flush=True)
if __name__=='__main__':run()
