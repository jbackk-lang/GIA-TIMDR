#!/usr/bin/env python3
"""Predefined counterexample: extrema values alone cannot identify event order."""
import random, statistics
N=64
TRAIN=range(1000,1100)
TEST=range(9000,9050)

def sample(seed, label):
    rng=random.Random(seed)
    x=[rng.uniform(-.6,.6) for _ in range(N)]
    a,b=sorted(rng.sample(range(4,N-4),2))
    if label=='MAX_FIRST': x[a],x[b]=1.,-1.
    else: x[a],x[b]=-1.,1.
    return x

def features(x,mode):
    mn=min(x); mx=max(x)
    if mode=='VALUES': return (mn,mx,N-1)
    if mode=='EVENT_TIME': return (mn,mx,x.index(mn),x.index(mx),N-1)
    if mode=='RELATIVE_TIME': return (mn,mx,x.index(mx)-x.index(mn),N-1)
    raise ValueError(mode)

def fit(mode):
    return {label:tuple(statistics.mean(features(sample(s,label),mode)[j] for s in TRAIN) for j in range(len(features(sample(1000,label),mode)))) for label in ('MAX_FIRST','MIN_FIRST')}

def predict(f,centroids):
    return min(centroids,key=lambda l:sum((a-b)**2 for a,b in zip(f,centroids[l])))

def main():
    print('representation,correct,total,accuracy')
    for mode in ('VALUES','EVENT_TIME','RELATIVE_TIME'):
        model=fit(mode); correct=0; total=0
        for seed in TEST:
            for label in ('MAX_FIRST','MIN_FIRST'):
                correct+=predict(features(sample(seed,label),mode),model)==label
                total+=1
        print(f'{mode},{correct},{total},{correct/total:.3f}')
    assert all(features(sample(s,'MAX_FIRST'),'VALUES')==features(sample(s,'MIN_FIRST'),'VALUES') for s in TEST)
    assert all(features(sample(s,'MAX_FIRST'),'RELATIVE_TIME')!=features(sample(s,'MIN_FIRST'),'RELATIVE_TIME') for s in TEST)
if __name__=='__main__': main()
