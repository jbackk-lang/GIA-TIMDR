import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
rng=np.random.default_rng(202611140803)
N=6000; L=92
order=rng.integers(0,2,N); z0=rng.normal(.5,.07,N); a=rng.uniform(.82,.94,N)
b=.965
h=np.zeros(N); x=np.zeros((N,L)); gaps=np.zeros((N,2)); tri=np.tile([-1.,1.,3.],(N,3))
for i,c in enumerate(order):
    g=(18,38) if c==0 else (38,18);gaps[i]=g
    for t in (8,8+g[0],64):x[i,t]=-1;x[i,t+3]=1
    for v in x[i]:h[i]=b*h[i]+max(v,0)
probe=np.c_[z0+rng.normal(0,.018,N),a*z0+rng.normal(0,.018,N)]
y=.6*z0+.8*h+rng.normal(0,.035,N)
yreset=.6*z0+rng.normal(0,.035,N)
tr=np.arange(3500);te=np.arange(4500,N)
features={'probe':probe,'triples':tri,'unordered_gaps':np.sort(gaps,axis=1),'ordered_gaps':gaps,'probe_plus_gaps':np.c_[probe,gaps],'probe_plus_triples_gaps':np.c_[probe,tri,gaps],'raw':x,'probe_plus_raw':np.c_[probe,x]}
print('N',N,'test',len(te),'hidden_means',*[round(h[order==c].mean(),6) for c in (0,1)])
for name,target in [('natural',y),('reset_hidden',yreset)]:
 for key,F in features.items():
  m=Ridge(alpha=.01).fit(F[tr],target[tr]);print(name,key,round(r2_score(target[te],m.predict(F[te])),5))
print('paired_mean_effect',round(np.mean(y-yreset),6),'paired_class_effect_difference',round(.8*(h[order==0].mean()-h[order==1].mean()),6))
