import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score,mean_squared_error
rng=np.random.default_rng(2026111409)
N=10000; K=8; alpha=rng.uniform(.82,.94,N); z0=rng.uniform(.12,.55,N); forcing=rng.normal(0,.045,N); noise=.012
z=np.zeros((N,K+2));z[:,0]=z0
for k in range(K+1): z[:,k+1]=alpha*z[:,k]+forcing
obs=z[:,:K]+rng.normal(0,noise,(N,K));target=z[:,K+1]+rng.normal(0,.018,N)
tr=np.arange(0,6000);va=np.arange(6000,8000);te=np.arange(8000,10000)
def evaluate(F):
 model=Ridge(alpha=1e-3).fit(F[tr],target[tr]);pred=model.predict(F[te]);return r2_score(target[te],pred),np.sqrt(mean_squared_error(target[te],pred))
estimated=[]
for x in obs:
 X=np.column_stack((x[:-1],np.ones(K-1))); a,u=np.linalg.lstsq(X,x[1:],rcond=None)[0];estimated.append((np.clip(a,.5,1.1),u))
est=np.array(estimated)
print('test',len(te),'forcing_std',np.std(forcing[te]),'target_std',np.std(target[te]))
for name,F in [('initial_state',z0[:,None]),('initial_state_alpha',np.column_stack((z0,alpha))),('probe_1',obs[:,:1]),('probe_2',obs[:,:2]),('probe_4',obs[:,:4]),('probe_8',obs),('probe_8_alpha',np.column_stack((obs,alpha))),('probe_8_est_alpha_u',np.column_stack((obs,est))),('oracle_state_alpha',np.column_stack((z[:,K],alpha))),('oracle_state_alpha_forcing',np.column_stack((z[:,K],alpha,forcing)))]:
 r,rm=evaluate(F);print(name,'R2',round(r,5),'RMSE',round(rm,5))
print('alpha_est_mae',np.mean(abs(est[te,0]-alpha[te])),'u_est_mae',np.mean(abs(est[te,1]-forcing[te])))
x0=.25;x1=.26
for a in [.82,.94]:
 u=x1-a*x0
 print('same_first_two',x0,x1,'alpha',a,'forcing',u,'next',a*x1+u)
x=.25;a=.88
for u in [-.04,0,.04]:
 zz=x
 for _ in range(9):zz=a*zz+u
 print('do_u',u,'z9',zz)
