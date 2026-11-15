import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def generate(n,seed,noise=0,markers=0,adversarial=False):
 r=np.random.default_rng(seed);out=[];y=[];err=[]
 for i in range(n):
  z=i%2;a,b=(24,48) if z==0 else (48,24)
  t0=r.uniform(20,60);ts=np.array([t0,t0+a,t0+a+b])
  p=np.exp(r.uniform(-2.2,2.2)) if adversarial else np.exp(r.uniform(-.45,.45))
  f=lambda t:200*(t/200)**p
  observed=f(ts);ratio=np.diff(observed)[0]/(observed[-1]-observed[0])
  if markers:
   reference=np.linspace(10,170,markers)
   readings=f(reference)+r.normal(0,noise,markers)
   readings=np.maximum.accumulate(readings+np.arange(markers)*1e-8)
   corrected=np.interp(observed,readings,reference)
   corrected_ratio=(corrected[1]-corrected[0])/(corrected[-1]-corrected[0]) if corrected[-1]>corrected[0] else .5
  else:corrected_ratio=ratio
  out.append([ratio,corrected_ratio]);y.append(z)
  err.append(abs(corrected_ratio-(1/3 if z==0 else 2/3)))
 return np.array(out),np.array(y),np.array(err)

def main():
 train,yt,_=generate(6000,101)
 model=make_pipeline(StandardScaler(),LogisticRegression()).fit(train[:,[0]],yt)
 for markers in [0,4,8,16,32,64]:
  for noise in [0,1,4]:
   X,y,e=generate(3000,200+markers*10+noise,noise,markers,True)
   for label,col in [('raw',0),('corrected',1)]:
    pred=model.predict(X[:,[col]])
    print(markers,noise,label,round(accuracy_score(y,pred),4),round(float(np.median(e)),4),flush=True)
if __name__=='__main__':main()
