import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
A=np.array([0,1,4,10,12,17]); B=np.array([0,1,8,11,13,17]); N=96
assert sorted(j-i for q in [A] for i in q for j in q if j>i)==sorted(j-i for q in [B] for i in q for j in q if j>i)
r=np.random.default_rng(405)
def sample(n, intervene=False):
    y=np.tile([0,1],n//2);r.shuffle(y)
    starts=r.integers(10,65,n);lo=r.uniform(-1.5,-.5,n);hi=r.uniform(.5,1.5,n)
    X=np.tile(lo[:,None],(1,N));gaps=[];tri=[]
    for k in range(n):
        ix=starts[k]+(A if y[k]==0 else B)
        X[k,ix]=hi[k]
        gaps.append(np.diff(ix));tri.append([X[k].min(),X[k].max(),X[k].argmax()-X[k].argmin()])
    M=r.integers(0,2,n) if intervene else y.copy()
    future=.8*(2*M-1)+r.normal(0,.45,n)
    return X,np.array(gaps),np.array(tri),y,M,future
tr=sample(3000);te=sample(1500);it=sample(1500,True)
def features(d):
 X,g,t,y,m,f=d
 return {'global_triple':t,'power':np.log1p(np.abs(np.fft.rfft(X,axis=1))**2),'ordered_gaps':g,'full_signal':X,'actual_memory':m[:,None]}
for name,F in features(tr).items():
 model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)).fit(F,(tr[-1]>0).astype(int))
 for label,d in [('observational',te),('intervention',it)]:
  idx=(d[-1]>0).astype(int)
  print(name,label,round(accuracy_score(idx,model.predict(features(d)[name])),4))
for label,d in [('observational',te),('intervention',it)]:
 print(label,'history_memory_agreement',round(np.mean(d[3]==d[4]),4),'mean_future_M1',round(d[-1][d[4]==1].mean(),4),'mean_future_M0',round(d[-1][d[4]==0].mean(),4))
X,g,t,y,m,f=sample(1000)
print('max_global_triplet_pair_difference',np.max(abs(t[y==0].mean(axis=0)-t[y==1].mean(axis=0))))
s=np.full(N,-1.);q=np.full(N,-1.);s[10+A]=1;q[10+B]=1
print('exact_pair_power_difference',np.max(abs(abs(np.fft.rfft(s))**2-abs(np.fft.rfft(q))**2)))
print('exact_pair_triplets', [s.min(),s.max(),s.argmax()-s.argmin()], [q.min(),q.max(),q.argmax()-q.argmin()])
print('gaps',np.diff(A).tolist(),np.diff(B).tolist())
noise=r.normal(0,.45,2000)
follow_A=-.8+noise;follow_B=.8+noise
fixed_A=-.8+noise;fixed_B=-.8+noise
print('paired_effect_memory_follows_relation',round(np.mean(follow_B-follow_A),4))
print('paired_effect_memory_held_fixed',round(np.mean(fixed_B-fixed_A),4))
