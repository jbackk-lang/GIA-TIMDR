import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def make(n,seed):
 r=np.random.default_rng(seed); X=[]; Y=[]
 for i in range(n):
  z=i%2; x=r.normal(0,.12,128)
  x[16]=-5;x[112]=5
  centers=[35,48] if z==0 else [68,81]
  for center,amp in zip(centers,[1.5,-1.5]):
   for k in range(-2,3):
    t=center+k
    x[t]+=amp*np.exp(-.5*(k/1.1)**2)
  x[16]=-5;x[112]=5
  alpha=.15 if z==0 else .85
  y=np.empty(128);y[0]=r.normal()
  for j in range(1,128):y[j]=alpha*y[j-1]+np.sqrt(1-alpha**2)*r.normal()
  Y.append(int(np.corrcoef(y[:-1],y[1:])[0,1]>.5));X.append(x)
 return np.asarray(X),np.asarray(Y)

def global3(x):
 return np.column_stack([x.min(axis=1),x.max(axis=1),np.abs(x.argmax(axis=1)-x.argmin(axis=1))/127])

def relational(x):
 # Predeclared windows; four values per window, not three.
 windows=[(10,23),(27,56),(60,90),(102,121)]
 out=[]
 for s in x:
  features=[]
  for a,b in windows:
   w=s[a:b]; mn=int(w.argmin());mx=int(w.argmax())
   features.extend([float(w[mn]),float(w[mx]),(a+mn)/127,(a+mx)/127])
  out.append(features)
 return np.asarray(out)

def run():
 tr,yt=make(2000,61);te,ye=make(1000,62)
 print('train/test',len(tr),len(te),'future_label_balance',ye.mean())
 for name,f in [('global3',global3),('relational16',relational),('full128',lambda a:a)]:
  model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000))
  model.fit(f(tr),yt)
  print(name,'features',f(tr).shape[1],'accuracy',round(accuracy_score(ye,model.predict(f(te))),4))
 print('global_unique',len(np.unique(global3(te),axis=0)))
if __name__=='__main__':run()
