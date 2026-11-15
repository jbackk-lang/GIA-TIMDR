import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def generate(n,seed):
 r=np.random.default_rng(seed); X=[];Y=[]
 for i in range(n):
  label=i%2
  x=np.zeros(128)
  x[16]=-5; x[112]=5
  loc=(35,48) if label==0 else (68,81)
  x[loc[0]]=1.5; x[loc[1]]=-1.5
  x+=r.uniform(-.05,.05,128)
  x[16]=-5; x[112]=5
  alpha=.15 if label==0 else .85
  y=np.empty(128);y[0]=r.normal()
  for j in range(1,128):
   y[j]=alpha*y[j-1]+np.sqrt(1-alpha**2)*r.normal()
  future_label=int(np.corrcoef(y[:-1],y[1:])[0,1]>.5)
  X.append(x);Y.append(future_label)
 return np.array(X),np.array(Y)

def features(x):
 return np.column_stack([x.min(axis=1),x.max(axis=1),np.abs(x.argmax(axis=1)-x.argmin(axis=1))/127])

def evaluate():
 train,ytrain=generate(2000,51);test,ytest=generate(1000,52)
 for name,a,b in [('MIN_MAX_TIME',features(train),features(test)),('FULL_WAVEFORM',train,test),('INTERIOR_EVENT_TIME',np.column_stack([train[:,35],train[:,68]]),np.column_stack([test[:,35],test[:,68]]))]:
  model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000))
  model.fit(a,ytrain)
  print(name,round(accuracy_score(ytest,model.predict(b)),4),'features',a.shape[1])
 print('unique_3D_features_train',np.unique(features(train),axis=0).shape[0])
 print('future_label_agreement_with_generator',round(np.mean(ytest==np.arange(len(ytest))%2),4))
 print('example_3D',features(test[:2]).tolist())
if __name__=='__main__':evaluate()
