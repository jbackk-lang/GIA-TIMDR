#!/usr/bin/env python3
"""Three-feature relational-time pilot under unknown clock origin."""
import random, math
N=64
TRIALS=1000

def trial(i, negative=False):
    rng=random.Random(20261114+i)
    label=rng.randrange(2)
    a,b=sorted(rng.sample(range(5,N-5),2))
    x=[rng.uniform(-.6,.6) for _ in range(N)]
    event_label=label if rng.random()<.85 else 1-label
    x[a],x[b]=((-1.,1.) if event_label==1 else (1.,-1.))
    tmin=x.index(-1.);tmax=x.index(1.)
    origin=rng.uniform(-1e4,1e4)
    future_label=rng.randrange(2) if negative else label
    alpha=.15 if future_label==0 else .85
    y=[rng.gauss(0,1)]
    for _ in range(127):
        y.append(alpha*y[-1]+math.sqrt(1-alpha*alpha)*rng.gauss(0,1))
    return future_label,(min(x),max(x),tmax-tmin),(min(x),max(x),origin+tmin)

def main():
    for neg in (False,True):
        correct={'VALUES':0,'RELATIVE_TIME':0,'ABSOLUTE_TIME':0}
        for i in range(TRIALS):
            target,rel,absolute=trial(i,neg)
            predictions={'VALUES':0,'RELATIVE_TIME':int(rel[2]>0),'ABSOLUTE_TIME':int(absolute[2]>0)}
            for key,p in predictions.items():correct[key]+=p==target
            assert abs(rel[2]-((absolute[2]+12345)-(absolute[2]+12345-rel[2])))<1e-8
        print('NEGATIVE_CONTROL' if neg else 'CORRELATED_FUTURE',correct,'total',TRIALS)
if __name__=='__main__':main()
