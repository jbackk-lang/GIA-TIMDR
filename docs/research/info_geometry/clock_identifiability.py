#!/usr/bin/env python3
"""Exact observational equivalence of source chirp and clock warp; independent reference resolves it."""
import math
N=1001
T=[i/1000 for i in range(N)]
f0=8.0
beta=0.30
psi=lambda t:t+beta*t*t/2
source_a=lambda t:math.sin(2*math.pi*f0*psi(t))
source_b=lambda tau:math.sin(2*math.pi*f0*tau)
a=[source_a(t) for t in T]
b=[source_b(psi(t)) for t in T]
maxerr=max(abs(x-y) for x,y in zip(a,b))
ref_a=T[:]
ref_b=[psi(t) for t in T]
rate_a=[(ref_a[i+1]-ref_a[i])/(T[i+1]-T[i]) for i in range(N-1)]
rate_b=[(ref_b[i+1]-ref_b[i])/(T[i+1]-T[i]) for i in range(N-1)]
threshold=0.1
pred_a='SOURCE_CHIRP' if max(abs(r-1) for r in rate_a)>threshold else 'CLOCK_IDENTITY'
pred_b='CLOCK_WARP' if max(abs(r-1) for r in rate_b)>threshold else 'CLOCK_IDENTITY'
print('N',N)
print('signal_max_abs_difference',format(maxerr,'.3g'))
print('minmax_A',min(a),max(a))
print('minmax_B',min(b),max(b))
print('reference_rate_A_first_last',rate_a[0],rate_a[-1])
print('reference_rate_B_first_last',rate_b[0],rate_b[-1])
print('reference_based_A',pred_a,'reference_based_B',pred_b)
assert maxerr<1e-12
assert pred_a=='CLOCK_IDENTITY' and pred_b=='CLOCK_WARP'
print('PASS: observational equivalence; independent clock distinguishes clock warp')
