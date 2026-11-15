import numpy as np
from scipy.signal import find_peaks
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
rng=np.random.default_rng(202611140813)
N=2400;fs=80;L=160;hs=[2,10,30];t=np.arange(L+max(hs)+1)/fs
X=np.zeros((N,L));Y=np.zeros((N,3));T=np.zeros((N,18));P=np.zeros((N,16));D=np.zeros((N,6));count=[]
for i in range(N):
 f1=rng.uniform(4,8);f2=f1+rng.uniform(.4,1.5)
 a1,a2=rng.uniform(.65,1.2,2);p1,p2=rng.uniform(-np.pi,np.pi,2);d1,d2=rng.uniform(.03,.25,2)
 clean=a1*np.exp(-d1*t)*np.sin(2*np.pi*f1*t+p1)+a2*np.exp(-d2*t)*np.sin(2*np.pi*f2*t+p2)
 x=clean[:L]+rng.normal(0,.12,L);X[i]=x;Y[i]=clean[[L+h-1 for h in hs]]+rng.normal(0,.12,3)
 peaks,_=find_peaks(x,distance=5,prominence=.25)
 peaks=np.sort(peaks[np.argsort(x[peaks])[-6:]]);count.append(len(peaks))
 for j,p in enumerate(peaks):
  lo=max(0,p-9);q=lo+np.argmin(x[lo:p]) if p>lo else p
  T[i,3*j:3*j+3]=[x[q],x[p],(p-q)/fs]
 if len(peaks)>1:D[i,:len(peaks)-1]=np.diff(peaks)/fs
 for j,f in enumerate(np.linspace(4,10,8)):
  z=np.dot(x[-100:],np.exp(-2j*np.pi*f*np.arange(100)/fs))/100
  P[i,2*j:2*j+2]=[z.real,z.imag]
train=np.arange(1500);test=np.arange(1900,N)
features={'triples':T,'triples_relations':np.c_[T,D],'phase_quadratures':P,'triples_relations_phase':np.c_[T,D,P],'raw':X,'raw_phase':np.c_[X,P]}
print('N',N,'train',len(train),'test',len(test),'peaks6_fraction',np.mean(np.array(count)==6))
for name,F in features.items():
 for hidx,h in enumerate(hs):
  m=make_pipeline(StandardScaler(),Ridge(alpha=100)).fit(F[train],Y[train,hidx])
  print(name,h,round(r2_score(Y[test,hidx],m.predict(F[test])),5))
