#!/usr/bin/env python3
"""Dynamic trajectory pilot, standard library only.

Tests whether temporal ordering helps distinguish ramp versus step changes.
This is a temporal baseline, NOT a full TIMDR implementation.
"""
import math, random, statistics

WINDOW=64
WINDOWS=16
TRAIN=range(1000,1100)
TEST=range(9000,9050)
LABELS=("STEP","RAMP","RECOVERY")

def trajectory(seed,label):
    rng=random.Random(seed)
    x=[0.0]*(WINDOW*WINDOWS)
    for i in range(1,len(x)):
        w=i//WINDOW
        if label=="STEP":
            a=0.35 if w<4 else 0.80
        elif label=="RAMP":
            a=0.35 if w<4 else (0.35+0.45*min((w-4)/7,1))
        else:
            a=0.35 if w<4 or w>=12 else 0.80
        x[i]=a*x[i-1]+math.sqrt(1-a*a)*rng.gauss(0,1)
    return x

def lag1(x):
    m=sum(x)/len(x)
    den=sum((v-m)**2 for v in x)
    return sum((x[i]-m)*(x[i-1]-m) for i in range(1,len(x)))/den if den else 0.0

def features(x,mode):
    z=[lag1(x[i:i+WINDOW]) for i in range(0,len(x),WINDOW)]
    if mode=="DYNAMIC":
        return z
    if mode=="STATIC":
        return [statistics.mean(z),statistics.pstdev(z),min(z),max(z)]
    if mode=="SHUFFLED":
        rng=random.Random(123456)
        rng.shuffle(z)
        return z
    raise ValueError(mode)

def model(mode):
    rows={label:[features(trajectory(seed,label),mode) for seed in TRAIN]
          for label in LABELS}
    d=len(next(iter(rows.values()))[0])
    mu=[statistics.mean(v[j] for values in rows.values() for v in values) for j in range(d)]
    sd=[statistics.pstdev(v[j] for values in rows.values() for v in values) or 1 for j in range(d)]
    centroids={label:[statistics.mean((v[j]-mu[j])/sd[j] for v in values)
                      for j in range(d)] for label,values in rows.items()}
    return mu,sd,centroids

def predict(x,m):
    mu,sd,centroids=m
    z=[(v-a)/b for v,a,b in zip(x,mu,sd)]
    return min(LABELS,key=lambda label:sum((v-w)**2 for v,w in zip(z,centroids[label])))

def main():
    print("mode,accuracy")
    for mode in ("STATIC","SHUFFLED","DYNAMIC"):
        m=model(mode)
        ok=0
        for seed in TEST:
            for label in LABELS:
                pred=predict(features(trajectory(seed,label),mode),m)
                ok+=(pred==label)
        print(f"{mode},{ok/(len(TEST)*len(LABELS)):.4f}")

if __name__=="__main__":
    main()
