import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from false_events_clock_test import N

def generate(n,seed,hard=False,negative=False):
 r=np.random.default_rng(seed); records=[]
 for i in range(n):
  z=i%2; gap=int(r.integers(16,25) if z==0 else r.integers(43,52)); start=int(r.integers(12,90)); centers=[start,start+gap]
  t=np.arange(N); x=r.normal(0,.10 if not hard else .20,N)
  for c,a in zip(centers,[2,-2]):x+=a*np.exp(-.5*((t-c)/2.0)**2)
  nf=int(r.integers(0,3) if not hard else r.integers(2,8))
  for _ in range(nf):
   c=int(r.integers(7,N-7));a=float(r.choice([-1,1])*r.uniform(.5,1.2 if not hard else 2.4))
   x+=a*np.exp(-.5*((t-c)/r.uniform(1.0,2.7))**2)
  keep=r.random(N)>(.05 if not hard else .22);keep[0]=keep[-1]=True
  x=np.interp(t,t[keep],x[keep]);sm=np.convolve(np.pad(x,(2,2),mode='edge'),np.ones(5)/5,'valid')
  peaks=[j for j in range(3,N-3) if sm[j]>sm[j-1] and sm[j]>=sm[j+1] and sm[j]>.35]
  troughs=[j for j in range(3,N-3) if sm[j]<sm[j-1] and sm[j]<=sm[j+1] and sm[j]<-.35]
  power=float(np.exp(r.uniform(-.12,.12) if not hard else r.uniform(-.65,.65)))
  f=lambda v:(v/(N-1))**power
  pairs=[]
  for p in peaks:
   for m in troughs:
    d=abs(f(p)-f(m)); amp=float(sm[p]-sm[m])
    pairs.append((p,m,d,amp))
  pairs.sort(key=lambda q:-q[3]);pairs=pairs[:30]
  alpha=.2 if z==0 else .8
  future=np.empty(128);future[0]=r.normal()
  for j in range(1,128):future[j]=alpha*future[j-1]+np.sqrt(1-alpha**2)*r.normal()
  y=int(np.corrcoef(future[:-1],future[1:])[0,1]>.5)
  if negative:y=int(r.integers(2))
  records.append((pairs,centers,y))
 return records

def vector(pairs,method):
 if not pairs:return [0,0,0]
 if method=='strongest':
  q=pairs[0];return [q[2],q[3],1]
 selected=pairs[:8]
 weights=np.exp(2*(np.array([q[3] for q in selected])-selected[0][3]))
 weights/=weights.sum()
 ds=np.array([q[2] for q in selected])
 return [float(np.dot(weights,ds)),float(np.dot(weights,ds*ds)),float(max(weights))]

def main():
 train=generate(3000,101);val=generate(1000,201,True);test=generate(1500,300,True);negative=generate(1500,301,True,True)
 print('sets',len(train),len(val),len(test))
 for method in ['strongest','multipair']:
  a=np.array([vector(q[0],method) for q in train]);y=np.array([q[2] for q in train])
  model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)).fit(a,y)
  vp=model.predict_proba(np.array([vector(q[0],method) for q in val]))[:,1];vy=np.array([q[2] for q in val])
  choices=[]
  for threshold in np.linspace(0,.49,50):
   mask=np.abs(vp-.5)>=threshold
   if mask.any():
    acc=accuracy_score(vy[mask],vp[mask]>=.5)
    if acc>=.9:choices.append((mask.mean(),threshold))
  threshold=max(choices)[1] if choices else .49
  print(method,'validation_threshold',round(threshold,3),'validation_90pct_feasible',bool(choices))
  for name,ds in [('shifted',test),('negative',negative)]:
   xx=np.array([vector(q[0],method) for q in ds]); yy=np.array([q[2] for q in ds]);prob=model.predict_proba(xx)[:,1];pred=prob>=.5;mask=np.abs(prob-.5)>=threshold
   topk=1 if method=='strongest' else 8
   pair_found=np.mean([any(abs(p-centers[0])<=4 and abs(m-centers[1])<=4 for p,m,*_ in pairs[:topk]) for pairs,centers,_ in ds])
   print(name,'accuracy',round(accuracy_score(yy,pred),4),'coverage',round(mask.mean(),4),'covered_accuracy',round(accuracy_score(yy[mask],pred[mask]),4) if mask.any() else None,'correct_pair_in_topk',round(pair_found,4))
if __name__=='__main__':main()
