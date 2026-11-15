#!/usr/bin/env python3
"""Two-receiver common-source simulation; standard library only.

Run: python docs/research/info_geometry/two_receivers.py
Exploratory demonstration, NOT causal proof.
"""
import math
import random
import statistics

N = 8192
CUT = N // 2

def generate(seed, source_change=False):
    rng = random.Random(seed)
    x = [0.0] * N
    for t in range(1, N):
        a = 0.82 if source_change and t >= CUT else 0.35
        x[t] = a*x[t-1] + math.sqrt(1-a*a)*rng.gauss(0,1)
    return x

def lowpass(x):
    return [x[0]] + [(x[i]+x[i-1])/2 for i in range(1,len(x))]

def observe(s, scenario, seed):
    rng = random.Random(seed)
    a = s[:]
    b = s[:]
    # A common-channel change affects both receivers.
    if scenario == "COMMON_CHANNEL":
        post = lowpass(s[CUT:])
        a[CUT:] = post
        b[CUT:] = post
    # Receiver-specific changes affect one branch only.
    if scenario == "RECEIVER_A":
        a[CUT:] = [max(-0.65,min(0.65,v)) for v in a[CUT:]]
    if scenario == "RECEIVER_B":
        b[CUT:] = [max(-0.65,min(0.65,v)) for v in b[CUT:]]
    # Independent sensor noise in both branches.
    a = [v + 0.08*rng.gauss(0,1) for v in a]
    b = [v + 0.08*rng.gauss(0,1) for v in b]
    return a,b

def lag1(x):
    m = statistics.mean(x)
    z = [v-m for v in x]
    den = sum(v*v for v in z)
    return sum(z[i]*z[i-1] for i in range(1,len(z)))/den if den else 0

def stats(x):
    return (statistics.pstdev(x),lag1(x))

def delta(x):
    before = stats(x[:CUT])
    after = stats(x[CUT:])
    return tuple(q-p for p,q in zip(before,after))

def run():
    print("scenario,delta_std_A,delta_lag1_A,delta_std_B,delta_lag1_B")
    for scenario in ("NONE","SOURCE","COMMON_CHANNEL","RECEIVER_A","RECEIVER_B"):
        s = generate(20261114, source_change=scenario=="SOURCE")
        a,b = observe(s,scenario,seed=20261115)
        da,db = delta(a),delta(b)
        print(f"{scenario},{da[0]:.6f},{da[1]:.6f},{db[0]:.6f},{db[1]:.6f}")

if __name__ == "__main__":
    run()
