import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
N=128

def dataset(n,seed):
 r=np.random.default_rng(seed); X=[]; Y=[]
 for i in range(n):
  z=i%2; t=np.arange(N); a=r.uniform(0.8,1.4); b=r.uniform(.8,1.4)
  c=int(r.integers(25,45)); gap=int(r.integers(15,28)); w=r.uniform(1.5,3)
  x=-a*np.exp(-.5*((t-c)/w)**2)+b*np.exp(-.5*((t-c-gap)/w)**2)
  x+=r.normal(0,.10,N)
  if z:x=x[::-1].copy()
  X.append(x);Y.append(z)
 return np.array(X),np.array(Y)

def extract(X):
 out={}
 out['power']=np.log1p(abs(np.fft.rfft(X,axis=1))**2)
 out['autocorr']=np.array([[np.dot(x[:-k],x[k:])/np.dot(x,x) for k in range(1,33)] for x in X])
 F=np.fft.rfft(X,axis=1)
 out['complex_fft']=np.column_stack([F.real,F.imag])
 out['ordered_extrema']=np.column_stack([X.min(axis=1),X.max(axis=1),(X.argmax(axis=1)-X.argmin(axis=1))/N])
 out['unordered_extrema']=np.column_stack([X.min(axis=1),X.max(axis=1),abs(X.argmax(axis=1)-X.argmin(axis=1))/N])
 windows=np.lib.stride_tricks.sliding_window_view(X,32,axis=1)[:,::16,:]
 out['stft_time']=np.log1p(abs(np.fft.rfft(windows*np.hanning(32),axis=2))**2).reshape(len(X),-1)
 out['raw']=X
 return out

def main():
 A,y=dataset(2400,71);B,z=dataset(1200,72)
 fa=extract(A);fb=extract(B)
 for name in fa:
  model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,C=1)).fit(fa[name],y)
  print(name,round(accuracy_score(z,model.predict(fb[name])),4))
 x=A[0];reverse=x[::-1]
 print('exact_power_reversal_error',np.max(abs(abs(np.fft.rfft(x))**2-abs(np.fft.rfft(reverse))**2)))
 print('exact_autocorr_reversal_error',np.max(abs(extract(x[None,:])['autocorr']-extract(reverse[None,:])['autocorr'])))
 r=np.random.default_rng(73); base=[]
 for j in range(500):
  t=np.arange(N);c=int(r.integers(25,45));g=int(r.integers(15,28));w=r.uniform(1.5,3)
  x=-r.uniform(.8,1.4)*np.exp(-.5*((t-c)/w)**2)+r.uniform(.8,1.4)*np.exp(-.5*((t-c-g)/w)**2)+r.normal(0,.1,N)
  base.append(x)
 P=np.array(base);Q=P[:,::-1]
 print('paired_power_max_abs',np.max(abs(extract(P)['power']-extract(Q)['power'])))
 print('paired_autocorr_max_abs',np.max(abs(extract(P)['autocorr']-extract(Q)['autocorr'])))
if __name__=='__main__':main()
