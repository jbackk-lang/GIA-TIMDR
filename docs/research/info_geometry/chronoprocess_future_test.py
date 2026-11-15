#!/usr/bin/env python3
"""Synthetic prediction test: extrema timing vs a later, separately generated AR regime."""
import random, math, statistics
N=64
TRAIN=range(1000,1300)
TEST=range(9000,9100)
LABELS=(0,1)

def session(seed,label):
    rng=random.Random(seed*19+label*1000003)
    a,b=sorted(rng.sample(range(6,N-6),2))
    x=[rng.uniform(-.6,.6) for _ in range(N)]
    order=label if rng.random()<.85 else 1-label
    if order==0: x[a],x[b]=1.,-1.
    else: x[a],x[b]=-1.,1.
    alpha=.15 if label==0 else .85
    y=[rng.gauss(0,1)]
    for _ in range(127):
        y.append(alpha*y[-1]+math.sqrt(1-alpha**2)*rng.gauss(0,1))
    return x,y

def feat(x,mode,seed):
    base=[min(x),max(x),N-1]
    if mode=='VALUES': return base
    tmin=x.index(min(x));tmax=x.index(max(x))
    if mode=='EVENT': return base+[tmax-tmin]
    if mode=='SHUFFLE':
        sign=1 if random.Random(seed+9917).random()<.5 else -1
        return base+[sign*abs(tmax-tmin)]
    raise ValueError(mode)

def fit(mode):
    rows={label:[feat(session(s,label)[0],mode,s) for s in TRAIN] for label in LABELS}
    d=len(rows[0][0])
    mu=[statistics.mean(v[j] for label in LABELS for v in rows[label]) for j in range(d)]
    sd=[statistics.pstdev(v[j] for label in LABELS for v in rows[label]) or 1 for j in range(d)]
    cent={label:[statistics.mean((v[j]-mu[j])/sd[j] for v in rows[label]) for j in range(d)] for label in LABELS}
    return mu,sd,cent

def predict(v,m):
    mu,sd,cent=m
    z=[(a-b)/c for a,b,c in zip(v,mu,sd)]
    return min(LABELS,key=lambda l:sum((a-b)**2 for a,b in zip(z,cent[l])))

def lag1(y):
    avg=statistics.mean(y)
    return sum((y[i]-avg)*(y[i-1]-avg) for i in range(1,len(y)))/sum((v-avg)**2 for v in y)

def main():
    print('mode,correct,total,accuracy')
    for mode in ('VALUES','SHUFFLE','EVENT'):
        m=fit(mode);correct=0;total=0
        for s in TEST:
            for label in LABELS:
                x,y=session(s,label)
                assert min(x)==-1 and max(x)==1
                correct+=predict(feat(x,mode,s),m)==label
                total+=1
        print(f'{mode},{correct},{total},{correct/total:.4f}')
    print('future_lag1_mean_by_label',*[round(statistics.mean(lag1(session(s,l)[1]) for s in TEST),3) for l in LABELS])
if __name__=='__main__': main()
