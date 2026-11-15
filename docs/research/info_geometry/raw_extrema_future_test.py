import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
N=101

def batch(seed,n,noise):
 r=np.random.default_rng(seed); X=[]; Y=[]; quality=[]
 for i in range(n):
  regime=i%2
  gap=int(r.integers(12,33) if regime==0 else r.integers(58,79))
  a=int(r.integers(5,96-gap)); b=a+gap
  if r.random()<.5:a,b=b,a
  t=np.arange(N); clean=np.exp(-.5*((t-b)/2.2)**2)-np.exp(-.5*((t-a)/2.2)**2)
  if a>b: clean=-clean
  x=clean+r.normal(0,noise,N)
  smooth=np.convolve(np.pad(x,(2,2),mode='edge'),np.ones(5)/5,mode='valid')
  imn=int(np.argmin(smooth)); imx=int(np.argmax(smooth))
  d=abs(imx-imn)/100
  X.append([float(x.min()),float(x.max()),d])
  alpha=.2 if regime==0 else .8
  future=np.empty(128);future[0]=r.normal()
  for j in range(1,128):future[j]=alpha*future[j-1]+np.sqrt(1-alpha**2)*r.normal()
  corr=np.corrcoef(future[:-1],future[1:])[0,1]
  Y.append(int(corr>.5))
  quality.append(abs(imx-imn-gap))
 return np.array(X),np.array(Y),np.array(quality)

print('noise,baseline_accuracy,three_feature_accuracy,median_gap_error,unknown_rate,covered_accuracy')
for noise in [0,.05,.15,.3,.5]:
 tr,ytr,_=batch(1000,1600,noise);te,yte,err=batch(9000,800,noise)
 base=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)).fit(tr[:,:2],ytr)
 model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)).fit(tr,ytr)
 proba=model.predict_proba(te)[:,1];pred=(proba>=.5).astype(int)
 uncertain=np.abs(proba-.5)<.2
 covered=~uncertain
 print(f'{noise},{accuracy_score(yte,base.predict(te[:,:2])):.4f},{accuracy_score(yte,pred):.4f},{np.median(err):.1f},{uncertain.mean():.4f},{accuracy_score(yte[covered],pred[covered]) if covered.any() else float("nan"):.4f}')
