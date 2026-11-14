import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def make(n,seed,shift=0,noise=.12):
 r=np.random.default_rng(seed); X=[]; Y=[]
 for i in range(n):
  z=i%2; x=r.normal(0,noise,128)
  x[16]=-5;x[112]=5
  for c,a in zip(([35,48] if z==0 else [68,81]),[1.5,-1.5]):
   c+=shift
   for k in range(-2,3):
    j=c+k
    if 0<=j<128 and j not in (16,112):x[j]+=a*np.exp(-.5*(k/1.1)**2)
  x[16]=-5;x[112]=5
  alpha=.15 if z==0 else .85
  y=np.empty(128);y[0]=r.normal()
  for j in range(1,128):y[j]=alpha*y[j-1]+np.sqrt(1-alpha**2)*r.normal()
  Y.append(int(np.corrcoef(y[:-1],y[1:])[0,1]>.5));X.append(x)
 return np.array(X),np.array(Y)

def extract(x):
 # Unsupervised local-peak detection, without predefined event windows.
 cand=[i for i in range(2,len(x)-2) if .7<abs(x[i])<3 and abs(x[i])>=max(abs(x[i-2:i])) and abs(x[i])>=max(abs(x[i+1:i+3]))]
 cand.sort(key=lambda i:-abs(x[i])); chosen=[]
 for i in cand:
  if all(abs(i-j)>5 for j in chosen):chosen.append(i)
 chosen.sort()
 triples=[]
 for i in chosen[:2]:
  a=max(0,i-2);b=min(128,i+3);w=x[a:b]
  triples.append([float(w.min()),float(w.max()),float(w.argmax()-w.argmin())/127])
 while len(triples)<2:triples.append([0,0,0])
 edge=(chosen[1]-chosen[0])/127 if len(chosen)>=2 else 0
 center=(chosen[0]+chosen[1])/254 if len(chosen)>=2 else 0
 return np.array(triples).ravel().tolist()+[edge,center],len(chosen)

def main():
 tr,yt=make(2000,61)
 ftr=np.array([extract(x)[0] for x in tr])
 for shift in [0,4,10,18]:
  te,ye=make(1000,62,shift)
  extracted=[extract(x) for x in te]
  fte=np.array([v[0] for v in extracted])
  print('SHIFT',shift,'detection_2_events',round(np.mean([v[1]>=2 for v in extracted]),3))
  for name,cols in [('triples_only',slice(0,6)),('triples_plus_gap',slice(0,7)),('triples_plus_gap_and_center',slice(0,8)),('full128',None)]:
   a=tr if cols is None else ftr[:,cols];b=te if cols is None else fte[:,cols]
   model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000)).fit(a,yt)
   print(name,round(accuracy_score(ye,model.predict(b)),4))
if __name__=='__main__':main()
