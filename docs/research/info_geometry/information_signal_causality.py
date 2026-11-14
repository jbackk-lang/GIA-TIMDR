import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
rng=np.random.default_rng(341);n=6000;T=128
base=np.zeros(T)
base[20]=-2;base[30]=2;base[70]=-1;base[86]=1
base=np.convolve(base,[.2,.6,.2],mode='same');base[0]=base[-1]=0
histories=np.array([base,base[::-1]])
assert np.allclose(abs(np.fft.rfft(histories[0]))**2,abs(np.fft.rfft(histories[1]))**2)
label=rng.integers(0,2,n);override=rng.integers(0,2,n);intervene=rng.random(n)<.5
memory=np.where(intervene,override,label)
X=histories[label]+rng.normal(0,.035,(n,T));X[:,-1]=0
y=(2*memory-1)*.6+rng.normal(0,.35,n);future=(y>0).astype(int)
train,test=train_test_split(np.arange(n),test_size=.3,random_state=13,stratify=future)
features={'instantaneous':X[:,-1:],
'global_triplet':np.column_stack([X.min(axis=1),X.max(axis=1),X.argmax(axis=1)-X.argmin(axis=1)]),
'power_spectrum':np.log1p(abs(np.fft.rfft(X,axis=1))**2),
'ordered_history':np.column_stack([X[:,20],X[:,30],X[:,70],X[:,86],X[:,T-21],X[:,T-31],X[:,T-71],X[:,T-87]]),
'true_memory':memory[:,None]}
print('exact_base_power_diff',np.max(abs(abs(np.fft.rfft(histories[0]))**2-abs(np.fft.rfft(histories[1]))**2)))
print('same_present',histories[:,-1].tolist())
for subset,name in [(np.ones(n,dtype=bool),'all'),(~intervene,'natural'),(intervene,'intervened')]:
 ids=test[subset[test]]
 print('subset',name,'count',len(ids),'history_memory_agreement',np.mean(label[ids]==memory[ids]))
 for key,F in features.items():
  clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1500))
  clf.fit(F[train],future[train]);p=clf.predict_proba(F[ids])[:,1]
  print(key,'acc',round(accuracy_score(future[ids],p>=.5),4),'auc',round(roc_auc_score(future[ids],p),4))
for h in (0,1):
 for m in (0,1):
  sel=intervene&(label==h)&(override==m)
  print('do_history',h,'do_memory',m,'n',sel.sum(),'mean_future',round(y[sel].mean(),4))
print('future_effect_do_memory',round(y[intervene&(override==1)].mean()-y[intervene&(override==0)].mean(),4))
