import numpy as np
from scipy.signal import find_peaks
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score
rng=np.random.default_rng(202611140800)
N=6000;L=96;K=8
raw=np.zeros((N,L));tri=np.zeros((N,9));gaps=np.zeros((N,2));probe=np.zeros((N,K));y=np.zeros(N);alpha=np.zeros(N);ok=np.zeros(N,bool)
for i in range(N):
 a=rng.uniform(.82,.94);alpha[i]=a
 g=(18,38) if rng.integers(2)==0 else (38,18)
 s=int(rng.integers(5,13));amp=rng.uniform(.8,1.2);clean=np.zeros(L)
 for t in [s,s+g[0],s+sum(g)]:clean[t]=-amp;clean[t+3]=amp
 z=0.
 for v in clean:z=a*z+max(v,0)
 raw[i]=clean+rng.normal(0,.12,L)
 probe[i]=z*a**np.arange(K)+rng.normal(0,.018,K)
 y[i]=z*a**K+rng.normal(0,.015)
 peaks,_=find_peaks(raw[i],height=.55,distance=9,prominence=.45)
 peaks=np.sort(peaks[np.argsort(raw[i,peaks])[-3:]])
 if len(peaks)==3:
  ok[i]=True;gaps[i]=np.diff(peaks)
  for j,p in enumerate(peaks):
   q=max(0,p-6)+np.argmin(raw[i,max(0,p-6):p]);tri[i,3*j:3*j+3]=[raw[i,q],raw[i,p],p-q]
train=np.arange(3500);test=np.arange(4500,N)
print('n_train',len(train),'n_test',len(test),'detected',ok[test].mean(),'target_std',y[test].std(),flush=True)
for k in [1,2,4,8]:
 p=probe[:,:k]
 reps={'probe':p,'probe_ordered_gaps':np.c_[p,gaps],'probe_triplets_gaps':np.c_[p,tri,gaps],'probe_raw':np.c_[p,raw]}
 for name,X in reps.items():
  model=Ridge(alpha=1.).fit(X[train],y[train]);r=r2_score(y[test],model.predict(X[test]))
  print('ridge',k,name,round(r,5),flush=True)
 for name in ['probe','probe_ordered_gaps','probe_triplets_gaps']:
  X=reps[name]
  model=HistGradientBoostingRegressor(max_iter=90,max_leaf_nodes=10,l2_regularization=5,random_state=0).fit(X[train],y[train]);r=r2_score(y[test],model.predict(X[test]))
  print('hgb',k,name,round(r,5),flush=True)
# Negative control: shuffle gaps between examples, leaving probes intact.
for k in [1,2]:
 perm=rng.permutation(N);X=np.c_[probe[:,:k],gaps[perm]]
 model=Ridge(alpha=1.).fit(X[train],y[train]);print('negative_shuffled_gaps',k,round(r2_score(y[test],model.predict(X[test])),5),flush=True)
