import numpy as np
from scipy.signal import hilbert,find_peaks
rng=np.random.default_rng(202611140807)
fs=200.;t=np.arange(0,10,1/fs);f=7.
for phi in [0,np.pi/3,2*np.pi/3,np.pi]:
 x=np.sin(2*np.pi*f*t)+np.sin(2*np.pi*f*t+phi)
 print('interference',phi/np.pi,np.sqrt(np.mean(x*x)),2*abs(np.cos(phi/2)))
for df in [.5,1.,2.]:
 x=np.sin(2*np.pi*7*t)+np.sin(2*np.pi*(7+df)*t)
 env=abs(hilbert(x))
 p,_=find_peaks(env,distance=int(fs/df*.75),prominence=.5)
 interior=t[p];interior=interior[(interior>.5/df)&(interior<10-.5/df)]
 print('beating',df,'expected',1/df,'observed',np.median(np.diff(interior)))
print('dispersion_phase_velocities',10/2,13/2.5,'group_velocity',(13-10)/(2.5-2))
for decay in [0.,.1,.3]:
 for sigma in [0.,.15]:
  err=[]
  for _ in range(300):
   phi=rng.uniform(-np.pi,np.pi)
   x=np.exp(-decay*t)*np.sin(2*np.pi*f*t+phi)+rng.normal(0,sigma,len(t))
   sl=t<2
   c=np.sum(x[sl]*np.cos(2*np.pi*f*t[sl]));s=np.sum(x[sl]*np.sin(2*np.pi*f*t[sl]))
   est=np.arctan2(c,s)
   err.append(abs(np.angle(np.exp(1j*(est-phi)))))
  print('phase_mae',decay,sigma,np.mean(err))
width=.16;center=4.
for delta in [0,1/(4*f),1/(2*f),1/f]:
 x1=np.exp(-.5*((t-center)/width)**2)*np.cos(2*np.pi*f*(t-center))
 x2=np.exp(-.5*((t-center-delta)/width)**2)*np.cos(2*np.pi*f*(t-center-delta))
 ratio=np.sum((x1+x2)**2)/(np.sum(x1*x1)+np.sum(x2*x2))
 print('packet_delay_cycles',delta*f,'energy_ratio',ratio)
