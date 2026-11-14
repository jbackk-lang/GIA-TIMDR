import numpy as np
from scipy.signal import find_peaks
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score
rng=np.random.default_rng(202611140801)
N=6000; L=100
raw=np.zeros((N,L)); tri=np.zeros((N,9)); gaps=np.zeros((N,2)); probe=np.zeros((N,2)); y=np.zeros(N); cls=np.zeros(N,int); good=np.zeros(N,bool)
for i in range(N):
 c=int(rng.integers(2));cls[i]=c
 g=(18,38) if c==0 else (38,18)
 s=int(rng.integers(8,15)); amp=rng.uniform(.85,1.15)
 clean=np.zeros(L)
 for t in [s,s+g[0],s+sum(g)]:clean[t]=-amp;clean[t+3]=amp
 raw[i]=clean+rng.normal(0,.10,L)
 # Observable state is independent of relational history.
 z=rng.normal(.5,.08); a=rng.uniform(.82,.94)
 probe[i]=[z+rng.normal(0,.018),z*a+rng.normal(0,.018)]
 # Hidden state is explicitly assigned by relational class (synthetic mechanism).
 h=.12 if c==0 else -.12
 y[i]=.6*z+.8*h+rng.normal(0,.035)
 pk,_=find_peaks(raw[i],height=.55,prominence=.45,distance=9)
 pk=np.sort(pk[np.argsort(raw[i,pk])[-3:]])
 if len(pk)==3:
  good[i]=True;gaps[i]=np.diff(pk)
  for j,p in enumerate(pk):
   lo=max(0,p-6);q=lo+np.argmin(raw[i,lo:p]);tri[i,3*j:3*j+3]=[raw[i,q],raw[i,p],p-q]
train=np.arange(3500);test=np.arange(4500,N)
features={'probe':probe,'triples':tri,'ordered_gaps':gaps,'unordered_gaps':np.sort(gaps,axis=1),'probe_gaps':np.c_[probe,gaps],'probe_triples_gaps':np.c_[probe,tri,gaps],'raw':raw,'probe_raw':np.c_[probe,raw]}
print('N',N,'train',len(train),'test',len(test),'detected',good[test].mean(),'class_means',*[round(y[test][cls[test]==c].mean(),5) for c in [0,1]])
for name,x in features.items():
 for label,m in [('ridge',Ridge(alpha=1)),('hgb',HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=12,l2_regularization=5,random_state=0))]:
  m.fit(x[train],y[train]); print(name,label,round(r2_score(y[test],m.predict(x[test])),5))
perm=rng.permutation(N);xp=np.c_[probe,gaps[perm]]
m=Ridge(alpha=1).fit(xp[train],y[train]);print('shuffled_relations_ridge',round(r2_score(y[test],m.predict(xp[test])),5))
print('paired_effect_by_class',.8*.12,-.8*.12,'difference',.8*.24)
