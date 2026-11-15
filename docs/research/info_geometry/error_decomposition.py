import numpy as np
from scipy.signal import find_peaks
from sklearn.isotonic import IsotonicRegression
from itertools import combinations

def run(n,seed,noise_clock=1.5):
 r=np.random.default_rng(seed);stats=np.zeros((4,2),int);detok=0;usable=0
 for i in range(n):
  z=i%2;gaps=[30,60] if z==0 else [60,30]
  t0=r.uniform(35,95);truth=np.array([t0,t0+gaps[0],t0+90])
  p=np.exp(r.uniform(-1.6,1.6));f=lambda t:255*(t/255)**p
  obs=f(truth);x=r.normal(0,.18,256)
  for center in obs:
   for k,amp in [(0,-2),(8,2)]:
    x+=amp*np.exp(-.5*((np.arange(256)-(center+k))/1.7)**2)
  for _ in range(3):
   center=r.uniform(15,220);a=r.uniform(1.6,2.3)
   for k,amp in [(0,-a),(8,a)]:
    x+=amp*np.exp(-.5*((np.arange(256)-(center+k))/1.7)**2)
  start=int(r.integers(5,230));length=int(r.integers(10,25))
  x[start:start+length]=np.nan
  good=np.isfinite(x)
  x=np.interp(np.arange(256),np.where(good)[0],x[good])
  smooth=np.convolve(x,[.25,.5,.25],mode='same')
  mins,_=find_peaks(-smooth,height=.8,distance=11)
  maxs,_=find_peaks(smooth,height=.8,distance=8)
  candidates=[]
  for a in mins:
   b=maxs[(maxs>=a+5)&(maxs<=a+12)]
   if len(b):candidates.append(a)
  candidates=np.array(sorted(set(candidates)))
  ref=np.linspace(5,250,12)
  meas=f(ref)+r.normal(0,noise_clock,len(ref))
  meas=IsotonicRegression(increasing=True,out_of_bounds='clip').fit_transform(ref,meas)
  meas=np.maximum.accumulate(meas+np.arange(len(meas))*1e-6)
  def correct(v):return np.interp(v,meas,ref)
  def pred(v):return int((v[1]-v[0])>(v[2]-v[1]))
  for j,v in enumerate([obs,correct(obs)]):
   stats[j,0]+=1;stats[j,1]+=int(pred(v)==z)
  if len(candidates)>=3:
   best=None;score=1e9
   for comb in combinations(candidates,3):
    v=correct(np.array(comb));d=np.diff(v)
    s=abs(d.sum()-90)+.3*min(abs(d[0]-30)+abs(d[1]-60),abs(d[0]-60)+abs(d[1]-30))
    if s<score:score=s;best=np.array(comb)
   detok+=int(np.max(abs(best-obs))<=3);usable+=1
   for j,v in enumerate([best,correct(best)],2):
    stats[j,0]+=1;stats[j,1]+=int(pred(v)==z)
 return stats,detok,usable

if __name__=='__main__':
 for sigma in [0,1.5,4]:
  stats,detok,usable=run(1000,2026,sigma)
  print('clock_noise',sigma,'usable',usable,'detected_all_three_within3',detok,'detection_precision',round(detok/usable,4))
  for name,(total,correct) in zip(['oracle_raw','oracle_calibrated','detected_raw','detected_calibrated'],stats):
   print(name,total,correct,round(correct/total,4) if total else None)
