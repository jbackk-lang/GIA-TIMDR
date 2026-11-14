#!/usr/bin/env python3
"""Independent clock-reference noise sensitivity; no source attribution without source model."""
import random, math
N=101
TRIALS=300
BETA=.30

def slope(t,y):
    mt=sum(t)/len(t);my=sum(y)/len(y)
    return sum((a-mt)*(b-my) for a,b in zip(t,y))/sum((a-mt)**2 for a in t)

def measure(sigma,seed,kind):
    rng=random.Random(seed+100000*(kind=='WARP'))
    t=[i/(N-1) for i in range(N)]
    tau=[v+(BETA*v*v/2 if kind=='WARP' else 0)+rng.gauss(0,sigma) for v in t]
    mid=N//2
    return slope(t[mid:],tau[mid:])-slope(t[:mid],tau[:mid])

def main():
    print('sigma,threshold,false_alarms_300,warp_detected_300,warp_unknown_300')
    for sigma in (0,.002,.01,.03,.1):
        cal=[measure(sigma,10000+i,'STABLE') for i in range(TRIALS)]
        threshold=sorted(abs(v) for v in cal)[math.ceil(.99*TRIALS)-1]+1e-12
        fp=sum(measure(sigma,20000+i,'STABLE')>threshold for i in range(TRIALS))
        detected=sum(measure(sigma,20000+i,'WARP')>threshold for i in range(TRIALS))
        print(f'{sigma:g},{threshold:.5f},{fp},{detected},{TRIALS-detected}')
if __name__=='__main__':
    main()
