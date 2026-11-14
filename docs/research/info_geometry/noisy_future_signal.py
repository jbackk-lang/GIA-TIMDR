import random,math,statistics
N=101

def run(noise,seed):
 r=random.Random(seed); label=seed%2
 gap=r.randint(12,32) if label==0 else r.randint(58,78)
 a=r.randint(5,95-gap);b=a+gap
 if r.random()<.5:a,b=b,a
 power=math.exp(r.uniform(-.8,.8));scale=math.exp(r.uniform(-1,1))
 def f(t):return 100*scale*(t/100)**power
 am=max(0,min(100,a+r.gauss(0,noise)));bm=max(0,min(100,b+r.gauss(0,noise)))
 raw=abs(f(bm)-f(am)); norm=raw/(f(100)-f(0))
 sign=int(bm>am)
 alpha=.15 if label==0 else .85
 y=[r.gauss(0,1)]
 for _ in range(127):y.append(alpha*y[-1]+math.sqrt(1-alpha*alpha)*r.gauss(0,1))
 avg=sum(y)/len(y)
 autocorr=sum((y[i]-avg)*(y[i-1]-avg) for i in range(1,len(y)))/sum((v-avg)**2 for v in y)
 target=int(autocorr>.5)
 return target, {'BASE':0,'SIGN':sign,'RAW':int(raw>45),'NORMALIZED':int(norm>.45)},label

for noise in (0,2,5,10,20):
 counts={k:0 for k in ['BASE','SIGN','RAW','NORMALIZED']}; total=4000;labelmatch=0
 for i in range(total):
  target,pred,label=run(noise,100000+i)
  labelmatch+=target==label
  for k,v in pred.items():counts[k]+=v==target
 print(noise,'future_matches_regime',round(labelmatch/total,4),{k:round(v/total,4) for k,v in counts.items()})
