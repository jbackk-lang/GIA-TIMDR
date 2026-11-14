#!/usr/bin/env python3
"""Exploratory multibranch receiver test, standard library only.

Compares M/S, K, delay-curve geometry proxy and combined features for
SOURCE vs RECEIVER_A vs RECEIVER_B vs COMMON_CHANNEL vs NONE.
Not a validated TIMDR G surface operator or K resonance operator.
"""
import math, random, statistics
from collections import Counter

N=1024
LABELS=("NONE","SOURCE","COMMON_CHANNEL","RECEIVER_A","RECEIVER_B")
TRAIN_SEEDS=range(1000,1100)
TEST_SEEDS=range(9000,9050)

def signal(seed, label):
    rng=random.Random(seed)
    x=[0.0]*N
    for i in range(1,N):
        a=0.80 if label=="SOURCE" and i>=N//2 else 0.35
        x[i]=a*x[i-1]+math.sqrt(1-a*a)*rng.gauss(0,1)
    return x

def measure(seed,label):
    s=signal(seed,label)
    a=s[:]; b=s[:]
    if label=="COMMON_CHANNEL":
        for z in (a,b):
            for i in range(N-1,N//2-1,-1):
                z[i]=(s[i]+s[i-1])*0.5
    if label=="RECEIVER_A":
        a[N//2:]=[max(-0.65,min(0.65,v)) for v in a[N//2:]]
    if label=="RECEIVER_B":
        b[N//2:]=[max(-0.65,min(0.65,v)) for v in b[N//2:]]
    ra=random.Random(seed+500000)
    rb=random.Random(seed+700000)
    return ([v+0.08*ra.gauss(0,1) for v in a],
            [v+0.08*rb.gauss(0,1) for v in b])

def lag1(x):
    m=sum(x)/len(x)
    d=sum((v-m)**2 for v in x)
    return sum((x[i]-m)*(x[i-1]-m) for i in range(1,len(x)))/d if d else 0.0

def ms(x):
    return [statistics.pstdev(x),lag1(x)]

def modal_proxy(x):
    # Relative high-frequency energy from first differences; not TIMDR K resonance.
    d=sum((x[i]-x[i-1])**2 for i in range(1,len(x)))
    p=sum(v*v for v in x)
    return [d/(p+1e-12)]

def geometry_proxy(x):
    # Turning angle of 2D delay curve; NOT surface geometry operator G.
    pts=[(x[i],x[i-2]) for i in range(2,len(x))]
    angles=[]
    for i in range(1,len(pts)-1):
        u=(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1])
        v=(pts[i+1][0]-pts[i][0],pts[i+1][1]-pts[i][1])
        nu=math.hypot(*u); nv=math.hypot(*v)
        if nu>1e-8 and nv>1e-8:
            cos=max(-1,min(1,(u[0]*v[0]+u[1]*v[1])/(nu*nv)))
            angles.append(math.acos(cos))
    return [statistics.median(angles) if angles else 0.0]

def feature(x,branch):
    f={"MS":ms,"K_PROXY":modal_proxy,"G_PROXY":geometry_proxy}[branch]
    p=f(x[:N//2]); q=f(x[N//2:])
    return [b-a for a,b in zip(p,q)]

def vector(a,b,branches):
    out=[]
    for branch in branches:
        out+=feature(a,branch)+feature(b,branch)
    return out

def fit(train):
    dims=len(train[0][0])
    means=[statistics.mean(row[0][j] for row in train) for j in range(dims)]
    sds=[statistics.pstdev(row[0][j] for row in train) or 1.0 for j in range(dims)]
    centroids={}
    for label in LABELS:
        rows=[[ (v[j]-means[j])/sds[j] for j in range(dims)]
              for v,y in train if y==label]
        centroids[label]=[statistics.mean(row[j] for row in rows) for j in range(dims)]
    return means,sds,centroids

def predict(x,model):
    means,sds,centroids=model
    z=[(v-m)/s for v,m,s in zip(x,means,sds)]
    return min(LABELS,key=lambda label:sum((a-b)**2 for a,b in zip(z,centroids[label])))

def evaluate(branches):
    train=[]
    for seed in TRAIN_SEEDS:
        for label in LABELS:
            a,b=measure(seed,label)
            train.append((vector(a,b,branches),label))
    model=fit(train)
    counts=Counter()
    for seed in TEST_SEEDS:
        for label in LABELS:
            a,b=measure(seed,label)
            pred=predict(vector(a,b,branches),model)
            counts[(label,pred)]+=1
    f1=[]
    for label in LABELS:
        tp=counts[(label,label)]
        fp=sum(counts[(actual,label)] for actual in LABELS if actual!=label)
        fn=sum(counts[(label,pred)] for pred in LABELS if pred!=label)
        f1.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0)
    accuracy=sum(counts[(l,l)] for l in LABELS)/(len(TEST_SEEDS)*len(LABELS))
    return accuracy,sum(f1)/len(f1),counts

def main():
    print("variant,accuracy,macro_f1")
    for name,branches in (
        ("MS",("MS",)),
        ("MS_K",("MS","K_PROXY")),
        ("MS_G",("MS","G_PROXY")),
        ("ALL",("MS","K_PROXY","G_PROXY"))):
        acc,f1,counts=evaluate(branches)
        print(f"{name},{acc:.4f},{f1:.4f}")
        if name=="ALL":
            print("confusion_actual,predicted,count")
            for actual in LABELS:
                for predicted in LABELS:
                    print(f"{actual},{predicted},{counts[(actual,predicted)]}")

if __name__=="__main__":
    main()
