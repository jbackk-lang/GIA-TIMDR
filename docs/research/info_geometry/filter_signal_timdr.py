import numpy as np
from scipy.signal import butter,sosfilt,sosfreqz,find_peaks
fs=200.; t=np.arange(0,4,1/fs)
rng=np.random.default_rng(202611140814)
x=np.sin(2*np.pi*4*t)+.65*np.sin(2*np.pi*28*t+.7)+.13*rng.normal(size=len(t))
filters={'lowpass_8Hz':butter(4,8,fs=fs,output='sos'),'highpass_15Hz':butter(4,15,fs=fs,btype='highpass',output='sos'),'bandpass_25_31Hz':butter(4,[25,31],fs=fs,btype='bandpass',output='sos')}
def triple_stats(a):
 peaks,_=find_peaks(a,prominence=.25,distance=3)
 troughs,_=find_peaks(-a,prominence=.25,distance=3)
 triples=[]
 for p in peaks:
  previous=troughs[troughs<p]
  if len(previous):
   q=previous[-1];triples.append((a[q],a[p],(p-q)/fs))
 return len(peaks),len(troughs),np.median([v[2] for v in triples]) if triples else float('nan'),triples
print('input rms',np.sqrt(np.mean(x**2)),'peaks troughs median_dt',triple_stats(x)[:3])
for name,sos in filters.items():
 y=sosfilt(sos,x)
 _,H=sosfreqz(sos,worN=2*np.pi*np.array([4.,28.])/fs)
 print(name,'rms',round(np.sqrt(np.mean(y**2)),5),'gain_4_28',np.round(abs(H),5),'phase_4_28_rad',np.round(np.angle(H),5),'peaks troughs median_dt',triple_stats(y)[:3])
np.savez('/mnt/data/timdr_experiment/filter_signal_timdr.npz',t=t,input=x,**{k:sosfilt(v,x) for k,v in filters.items()})
