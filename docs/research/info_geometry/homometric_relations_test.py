import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
A=np.array([1,-2,-1,2,-1,0,0]);B=np.array([1,-1,1,-1,2,2,-2]);X=np.convolve(A,B);Y=np.convolve(A,B[::-1]);N=64
assert X.min()==Y.min() and X.max()==Y.max() and X.argmax()-X.argmin()==Y.argmax()-Y.argmin()
assert np.allclose(abs(np.fft.rfft(X,N))**2,abs(np.fft.rfft(Y,N))**2)
def make(n,seed):
 r=np.random.default_rng(seed);data=[];labels=[]
 for i in range(n):
  z=i%2;scale=r.uniform(.5,2.);shift=int(r.integers(8,40));v=np.zeros(N);v[shift:shift+len(X)]=scale*(Y if z else X)
  data.append(v);labels.append(z)
 return np.array(data),np.array(labels)
def feat(D):
 f=np.fft.rfft(D,axis=1);power=np.log1p(abs(f)**2)
 ac=np.array([[np.dot(x[:-k],x[k:]) for k in range(1,24)] for x in D])
 tri=np.column_stack([D.min(axis=1),D.max(axis=1),(D.argmax(axis=1)-D.argmin(axis=1))/N])
 centers=D.argmin(axis=1)
 rel=np.array([[x[c+j] if 0<=c+j<N else 0 for j in range(-5,7)] for x,c in zip(D,centers)])
 return {'global3':tri,'power':power,'autocorr':ac,'relative_local_sequence':rel,'complex_fft':np.column_stack([f.real,f.imag]),'full_signal':D}
tr,yt=make(2000,20);te,ye=make(1000,21);ft=feat(tr);fe=feat(te)
for key in ft:
 m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000)).fit(ft[key],yt)
 print(key,accuracy_score(ye,m.predict(fe[key])))
print('global_triple_X',X.min(),X.max(),X.argmax()-X.argmin())
print('global_triple_Y',Y.min(),Y.max(),Y.argmax()-Y.argmin())
print('max_power_difference',np.max(abs(abs(np.fft.rfft(X,N))**2-abs(np.fft.rfft(Y,N))**2)))
print('templates',X.tolist(),Y.tolist())
