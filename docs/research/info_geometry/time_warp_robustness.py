#!/usr/bin/env python3
"""Invariance of three time features under offset, affine and nonlinear clocks."""
import random,math,statistics
rng=random.Random(20261114)
N=101; trials=3000
for mode in ['offset','affine','nonlinear']:
    errors={k:[] for k in ['delta','sign','normalized']}
    for _ in range(trials):
        a,b=sorted(rng.sample(range(5,96)))
        direction=rng.choice([-1,1])
        imin,imax=(a,b) if direction==1 else (b,a)
        scale=math.exp(rng.uniform(-1.2,1.2))
        offset=rng.uniform(-100,100)
        power=math.exp(rng.uniform(-1.2,1.2))
        def f(t):
            u=t/(N-1)
            if mode=='offset': return offset+t
            if mode=='affine': return offset+scale*t
            return offset+scale*(N-1)*u**power
        d0=imax-imin
        d=f(imax)-f(imin)
        nd0=d0/(N-1)
        nd=d/(f(N-1)-f(0))
        errors['delta'].append(abs(d-d0)/(N-1))
        errors['sign'].append(int((d>0)!=(d0>0)))
        errors['normalized'].append(abs(nd-nd0))
    print(mode,'mean_abs_delta_error_window_units',round(statistics.mean(errors['delta']),4),'sign_flips',sum(errors['sign']),'mean_abs_normalized_error',round(statistics.mean(errors['normalized']),4))
