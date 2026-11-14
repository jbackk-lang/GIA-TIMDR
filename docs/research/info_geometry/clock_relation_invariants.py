import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def make(n,seed,warp='identity'):
 r=np.random.default_rng(seed); X=[]; y=[]; flips=0
 for i in range(n):
  z=i%2
  gaps=np.array([24.,48.]) if z==0 else np.array([48.,24.])
  t0=r.uniform(15,65); ts=np.r_[t0,t0+gaps[0],t0+gaps.sum()]
  if warp=='identity':f=lambda t:t
  elif warp=='affine':
   a=r.uniform(.4,2.5);b=r.uniform(-80,80);f=lambda t:a*t+b
  elif warp=='mild':
   p=np.exp(r.uniform(-.45,.45));f=lambda t:200*(t/200)**p
  elif warp=='strong':
   p=np.exp(r.uniform(-2.2,2.2));f=lambda t:200*(t/200)**p
  elif warp=='adversarial':
   k=r.choice([.025,.1,10.,40.]);f=lambda t:200*(t/200)**k
  s=f(ts);d=np.diff(s); ratio=d[0]/sum(d)
  flips+=int((ratio<.5)!=(z==0))
  X.append([ratio,d[0],d[1],np.sign(d[1]-d[0]),float(s[0]<s[1]<s[2])]);y.append(z)
 return np.array(X),np.array(y),flips/n

def main():
 train,y,_=make(6000,12,'identity')
 for condition in ['identity','affine','mild','strong','adversarial']:
  test,z,flip=make(3000,42,condition)
  print('TEST',condition,'fraction_gap_order_reversed_vs_source',round(flip,4))
  for name,cols in [('ratio',[0]),('raw_gaps',[1,2]),('gap_order',[3]),('event_order',[4])]:
   m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)).fit(train[:,cols],y)
   print(name,round(accuracy_score(z,m.predict(test[:,cols])),4))
 obs=np.array([0.,1.,2.]);src0=np.array([0.,1.,3.]);src1=np.array([0.,2.,3.])
 print('NONIDENTIFIABILITY','source_A',src0.tolist(),'source_B',src1.tolist(),'observed_both',obs.tolist())
 print('AFFINE_INVARIANCE_EXAMPLE',48/(24+48),2.7*48/(2.7*24+2.7*48))
if __name__=='__main__':main()
