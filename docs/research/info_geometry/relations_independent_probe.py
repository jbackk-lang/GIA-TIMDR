import numpy as np
from scipy.signal import find_peaks
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score
rng=np.random.default_rng(202611140758)
N=6000; L=96; K=8
raw=np.zeros((N,L)); triples=np.zeros((N,9)); gaps=np.zeros((N,2)); probes=np.zeros((N,K)); y=np.zeros(N); atrue=np.zeros(N); complete=np.zeros(N,bool)
for i in range(N):
 a=rng.uniform(.82,.94);atrue[i]=a
 g=(18,38) if rng.integers(2)==0 else (38,18)
 s=int(rng.integers(5,13)); amp=rng.uniform(.8,1.2)
 clean=np.zeros(L)
 for t in [s,s+g[0],s+sum(g)]:clean[t]=-amp;clean[t+3]=amp
 z=0.
 for v in clean:z=a*z+max(v,0)
 raw[i]=clean+rng.normal(0,.12,L)
 probes[i]=z*a**np.arange(K)+rng.normal(0,.018,K)
 y[i]=z*a**K+rng.normal(0,.015)
 pk,_=find_peaks(raw[i],height=.55,distance=9,prominence=.45)
 pk=np.sort(pk[np.argsort(raw[i,pk])[-3:]])
 if len(pk)==3:
  complete[i]=True;gaps[i]=np.diff(pk)
  for j,p in enumerate(pk):
   q=max(0,p-6)+np.argmin(raw[i,max(0,p-6):p]);triples[i,3*j:3*j+3]=[raw[i,q],raw[i,p],p-q]
train=np.arange(3500);test=np.arange(4500,N)
shuffled=probes.copy();shuffled[test]=probes[test][rng.permutation(len(test))]
F={'triples':triples,'ordered_relations':gaps,'triples_relations':np.c_[triples,gaps],'probe_only':probes,'relations_probe':np.c_[triples,gaps,probes],'raw_only':raw,'raw_probe':np.c_[raw,probes],'shuffled_probe_negative':shuffled,'oracle_alpha_relations':np.c_[triples,gaps,atrue]}
print('N',N,'test',len(test),'detection_coverage',round(complete[test].mean(),5),'target_sd',round(y[test].std(),5))
for name,x in F.items():
 for model_name,model in [('ridge',Ridge(alpha=1.0)),('hgb',HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=12,l2_regularization=5,random_state=0))]:
  model.fit(x[train],y[train]);p=model.predict(x[test]);print(name,model_name,'R2',round(r2_score(y[test],p),5))
