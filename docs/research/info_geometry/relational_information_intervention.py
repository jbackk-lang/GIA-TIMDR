import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
rng=np.random.default_rng(20261114)
# Same three local MIN/MAX/delta-time triples, distinct event-gap order.
# Explicit causal model: a state variable stores a weighted temporal trace of the events.
N=6000; n=90; alpha=.97; t0=8
orders=np.tile([0,1],N//2);rng.shuffle(orders)
X=np.zeros((N,n)); gaps=np.zeros((N,2)); memories=np.zeros(N)
for i,c in enumerate(orders):
    g=(18,38) if c==0 else (38,18)
    times=np.array([t0,t0+g[0],t0+sum(g)])
    gaps[i]=g
    for t in times:
        X[i,t]=-1;X[i,t+3]=1
    z=0.
    for x in X[i]:z=alpha*z+max(x,0)
    memories[i]=z
y=memories+rng.normal(0,.025,N)
yreset=rng.normal(0,.025,N)
train=np.arange(4000);test=np.arange(4000,N)
triples=np.tile(np.array([-1,1,3]*3),(N,1))
features={'triples_only':triples,'ordered_gaps':gaps,'unordered_gaps':np.sort(gaps,axis=1),'triples_plus_gaps':np.column_stack([triples,gaps])}
print('N',N,'train',len(train),'test',len(test),'alpha',alpha)
print('unique_triplets',np.unique(triples,axis=0).shape[0]);print('gap_patterns',np.unique(gaps,axis=0))
print('memory_means',[(c,memories[orders==c].mean()) for c in (0,1)])
for label,target in [('natural',y),('memory_reset',yreset)]:
 for name,F in features.items():
    model=Ridge(alpha=.01).fit(F[train],target[train]);pred=model.predict(F[test]);print(label,name,'r2',round(r2_score(target[test],pred),5),'rmse',round(np.mean((pred-target[test])**2)**.5,5))
print('paired_causal_effect_mean',round(np.mean(y-yreset),6),'mean_abs_memory',round(np.mean(np.abs(memories)),6))
print('future_by_order',[(c,round(y[orders==c].mean(),6),round(yreset[orders==c].mean(),6)) for c in (0,1)])
