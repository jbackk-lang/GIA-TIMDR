"""Lagged decoding of previous CWRU crest-factor events. Reproduces stage 017.
Requires CWRU_CHF.zip, numpy, scipy, scikit-learn, and stage 016 module.
Run: python research/chrono_helix_fusion/chf_stage_017.py CWRU_CHF.zip
"""
import sys,io,zipfile,json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import hilbert
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score
LAGS=(1,2,3,5,8)
def features(w):
 w=w-w.mean();n=len(w);rms=np.sqrt(np.mean(w*w))+1e-12
 F=np.fft.rfft(w*np.hanning(n));power=abs(F)**2
 bands=np.array([np.log1p(power[i:j].sum()) for i,j in [(1,32),(32,128),(128,512),(512,1025)]])
 env=abs(hilbert(w));env-=env.mean();den=np.dot(env,env)+1e-12
 ac=np.array([np.dot(env[:-k],env[k:])/den for k in (32,64,128,256)])
 phase=np.angle(F);ph=[]
 for a in (8,16,32,64):
  d=phase[2*a]-2*phase[a];ph.extend([np.cos(d),np.sin(d)])
 time=np.array([np.log(rms),np.max(abs(w))/rms,np.mean((np.diff(w)/rms)**3),np.mean((w/rms)**4)])
 return np.concatenate([time,bands,ac,ph])
def run(source):
 files=[]
 with zipfile.ZipFile(source) as z:
  for f in sorted(k for k in z.namelist() if k.endswith('.mat')):
   m=loadmat(io.BytesIO(z.read(f)));x=np.asarray(m[next(k for k in m if k.endswith('_DE_time'))]).ravel()
   w=x[:50*2048].reshape(50,2048)
   crest=np.max(abs(w),axis=1)/(np.sqrt(np.mean(w*w,axis=1))+1e-12)
   ft=np.array([features(v) for v in w]);ft=(ft-ft.mean(axis=0))/(ft.std(axis=0)+1e-8)
   files.append((f,crest,ft))
 results={}
 for lag in LAGS:
  X=[];y=[];ids=[]
  for f,crest,ft in files:
   count=50-lag;labels=np.zeros(count,dtype=int);labels[np.argsort(crest[:count])[-5:]]=1
   X.extend(ft[lag:].tolist());y.extend(labels.tolist());ids.extend([f]*count)
  X=np.asarray(X);y=np.asarray(y);ids=np.asarray(ids);scores={}
  for method,sel in {'rms':[0],'fft':list(range(4,8)),'envelope':list(range(8,12)),
                     'phase':list(range(12,20)),'all':list(range(20))}.items():
   pred=np.zeros(len(y))
   for f in np.unique(ids):
    tr=ids!=f;te=~tr
    model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,C=.1,class_weight='balanced'))
    model.fit(X[tr][:,sel],y[tr]);pred[te]=model.predict_proba(X[te][:,sel])[:,1]
   scores[method]={'mean_auroc':float(np.mean([roc_auc_score(y[ids==f],pred[ids==f]) for f in np.unique(ids)])),
                   'pooled_auroc':float(roc_auc_score(y,pred))}
  results[str(lag)]={'pairs':len(y),'positives':int(y.sum()),'scores':scores}
 return {'stage':'017','lags':LAGS,'results':results,'limitations':['Exploratory lag/feature scan',
  'Events selected separately for each lag','Transductive per-recording normalization',
  'No CHF helix descriptors, surrogates or external validation']}
if __name__=='__main__':
 result=run(sys.argv[1]);Path('CHF_AFTER_EVENT_017.json').write_text(json.dumps(result,indent=2)+'\n')
 for lag,data in result['results'].items():print(lag,{k:round(v['mean_auroc'],4) for k,v in data['scores'].items()})
