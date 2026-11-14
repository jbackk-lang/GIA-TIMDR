import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score,mean_squared_error
A=np.array([0,1,4,10,12,17]); B=np.array([0,1,8,11,13,17]);N=96
rng=np.random.default_rng(20261114)
def dynamics(x,alpha=.88):
    z=np.zeros(len(x)+1)
    for t in range(len(x)):z[t+1]=alpha*z[t]+x[t]
    return z
def make(n,reset=False,noise=.05):
    hist=[]; states=[]; futures=[]; labels=[]; triples=[]; gaps=[]; powers=[]
    for k in range(n):
        label=k%2; start=N-18; a=float(rng.uniform(.8,1.2))
        x=np.zeros(N); ix=start+(A if label==0 else B);x[ix]=a
        z=dynamics(x); state=z[-1]
        if reset:state=0.
        future=state*.88**np.arange(1,17)+rng.normal(0,noise,16)
        hist.append(x);states.append(state);futures.append(future);labels.append(label)
        triples.append([x.min(),x.max(),x.argmax()-x.argmin()]);gaps.append(np.diff(ix));powers.append(abs(np.fft.rfft(x))**2)
    return tuple(map(np.array,(hist,states,futures,labels,triples,gaps,powers)))
train=make(4000);test=make(2000);reset=make(2000,reset=True)
print('exact homometry',np.max(abs(abs(np.fft.rfft(np.bincount(N-18+A,minlength=N)))**2-abs(np.fft.rfft(np.bincount(N-18+B,minlength=N)))**2)))
print('gaps',np.diff(A),np.diff(B))
for name,idx in [('train',train),('test',test),('reset',reset)]:
 x,z,f,y,tr,g,p=idx
 print(name,'n',len(y),'mean_state_A',z[y==0].mean(),'mean_state_B',z[y==1].mean(),'future_mean_A',f[y==0,0].mean(),'future_mean_B',f[y==1,0].mean())
for feat,ix in [('global_triple',4),('fft_power',6),('local_gaps',5),('raw_waveform',0),('state_oracle',1)]:
 F=train[ix].reshape(len(train[3]),-1);G=test[ix].reshape(len(test[3]),-1)
 model=Ridge(alpha=1).fit(F,train[2][:,0]);pred=model.predict(G)
 print('predict',feat,'r2',r2_score(test[2][:,0],pred),'rmse',np.sqrt(mean_squared_error(test[2][:,0],pred)))
x=np.zeros(N);x[N-18+A]=1; y=np.zeros(N);y[N-18+B]=1
za=dynamics(x)[-1];zb=dynamics(y)[-1]
print('paired state A,B',za,zb,'difference',zb-za)
print('paired future difference no reset',.88*(zb-za),'reset',0)
print('paired global triples', [x.min(),x.max(),x.argmax()-x.argmin()],[y.min(),y.max(),y.argmax()-y.argmin()])
for name,fi in [('triple_plus_gaps',(4,5)),('power_plus_gaps',(6,5))]:
 F=np.column_stack([train[i].reshape(len(train[3]),-1) for i in fi]);G=np.column_stack([test[i].reshape(len(test[3]),-1) for i in fi]);pred=Ridge(alpha=1).fit(F,train[2][:,0]).predict(G)
 print('predict',name,'r2',r2_score(test[2][:,0],pred),'rmse',np.sqrt(mean_squared_error(test[2][:,0],pred)))
