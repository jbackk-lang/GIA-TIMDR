import numpy as np
from itertools import combinations

def trial(n,seed):
 r=np.random.default_rng(seed); records=[]
 for i in range(n):
  y=i%2; t0=r.uniform(25,65); true=np.array([t0,t0+(30 if y==0 else 60),t0+90]);p=np.exp(r.uniform(-1.6,1.6));f=lambda t:255*(t/255)**p
  ref=np.linspace(5,250,12);m=f(ref)+r.normal(0,1.5,12);m=np.maximum.accumulate(m+np.arange(12)*1e-5)
  observed=f(true)+r.normal(0,1.5,3)
  distract=f(r.uniform(15,210,5));cand=np.sort(np.r_[observed,distract]); source=np.interp(cand,m,ref)
  hyps=[]
  for ids in combinations(range(len(cand)),3):
   ts=source[list(ids)];d=np.diff(ts)
   if np.min(d)<6:continue
   score=abs(d.sum()-90)/14+min(np.sum(abs(d-[30,60])),np.sum(abs(d-[60,30])))/12
   label=int(d[0]>d[1]);correct=all(np.min(abs(cand-observed[j]))<4 for j in range(3)) and np.max(abs(np.sort(cand[list(ids)])-np.sort(observed)))<4
   hyps.append((score,label,correct))
  hyps.sort(key=lambda x:x[0]); hyps=hyps[:8]
  if not hyps:continue
  weights=np.exp(-np.array([h[0] for h in hyps])/1.5);weights/=sum(weights)
  p1=sum(w*h[1] for w,h in zip(weights,hyps))
  records.append((y,hyps[0][1],int(p1>=.5),max(p1,1-p1),any(h[2] for h in hyps),hyps[0][2],p1))
 return np.array(records)

def main():
 v=trial(3000,777);t=trial(5000,778)
 print('validation',len(v),'test',len(t))
 print('top1_accuracy',np.mean(t[:,0]==t[:,1]))
 print('top8_vote_accuracy',np.mean(t[:,0]==t[:,2]))
 print('true_in_top1',np.mean(t[:,5]),'true_in_top8',np.mean(t[:,4]))
 for target in [.75,.8,.85,.9]:
  choices=[]
  for threshold in np.linspace(.5,1,101):
   accept=v[:,3]>=threshold
   if accept.sum()<100:continue
   acc=np.mean(v[accept,0]==v[accept,2])
   if acc>=target:choices.append((accept.mean(),threshold,acc))
  if not choices:print('target',target,'no_valid_threshold');continue
  coverage,threshold,valacc=max(choices)
  accept=t[:,3]>=threshold
  print('target',target,'threshold',round(threshold,3),'validation_coverage',round(coverage,4),'validation_acc',round(valacc,4),'test_coverage',round(accept.mean(),4),'test_acc',round(np.mean(t[accept,0]==t[accept,2]),4))
 for a,b in [(.5,.6),(.6,.7),(.7,.8),(.8,.9),(.9,1.01)]:
  ix=(t[:,3]>=a)&(t[:,3]<b)
  if ix.any():print('confidence_bin',a,b,'n',ix.sum(),'mean_confidence',round(t[ix,3].mean(),3),'accuracy',round(np.mean(t[ix,0]==t[ix,2]),3))
if __name__=='__main__':main()
