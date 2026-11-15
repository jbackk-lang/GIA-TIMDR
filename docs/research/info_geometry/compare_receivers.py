#!/usr/bin/env python3
"""Ablation of one vs two receivers using the frozen synthetic generator.

Run from repo root:
python docs/research/info_geometry/compare_receivers.py
"""
from collections import Counter
import multibranch_receiver_test as base

def vectors(a,b,branches,receiver):
    if receiver=="A":
        return base.vector(a,b,branches)[:0] + sum((base.feature(a,k) for k in branches),[])
    if receiver=="B":
        return sum((base.feature(b,k) for k in branches),[])
    return base.vector(a,b,branches)

def score(branches,receiver):
    train=[]
    for seed in base.TRAIN_SEEDS:
        for label in base.LABELS:
            a,b=base.measure(seed,label)
            train.append((vectors(a,b,branches,receiver),label))
    model=base.fit(train)
    counts=Counter()
    for seed in base.TEST_SEEDS:
        for label in base.LABELS:
            a,b=base.measure(seed,label)
            pred=base.predict(vectors(a,b,branches,receiver),model)
            counts[(label,pred)]+=1
    f1=[]
    for label in base.LABELS:
        tp=counts[(label,label)]
        fp=sum(counts[(actual,label)] for actual in base.LABELS if actual!=label)
        fn=sum(counts[(label,pred)] for pred in base.LABELS if pred!=label)
        f1.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0)
    acc=sum(counts[(l,l)] for l in base.LABELS)/(len(base.TEST_SEEDS)*len(base.LABELS))
    return acc,sum(f1)/len(f1),counts

def main():
    print("receiver,features,accuracy,macro_f1,source_as_common,common_as_source")
    for receiver in ("A","B","AB"):
        for name,branches in (("MS",("MS",)),("ALL",("MS","K_PROXY","G_PROXY"))):
            acc,f1,c=score(branches,receiver)
            print(f"{receiver},{name},{acc:.4f},{f1:.4f},"
                  f"{c[('SOURCE','COMMON_CHANNEL')]},"
                  f"{c[('COMMON_CHANNEL','SOURCE')]}")

if __name__=="__main__":
    main()
