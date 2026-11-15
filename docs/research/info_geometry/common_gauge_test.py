#!/usr/bin/env python3
"""Common clock drift is a gauge ambiguity for internal pairwise measurements."""
import random, statistics
N=101
T=[i/(N-1) for i in range(N)]
SIGMA=.004
BETA=.3
TRIALS=500

def slope_diff(t,y):
    k=len(t)//2
    def slope(xx,yy):
        mx=statistics.mean(xx);my=statistics.mean(yy)
        return sum((a-mx)*(b-my) for a,b in zip(xx,yy))/sum((a-mx)**2 for a in xx)
    return slope(t[k:],y[k:])-slope(t[:k],y[:k])

def session(seed,drift):
    rng=random.Random(seed)
    common=[(BETA/2)*t*t if drift else 0 for t in T]
    clocks=[[t+common[i]+offset+rng.gauss(0,SIGMA) for i,t in enumerate(T)]
            for offset in (0,.1,-.15,.23)]
    internal=[slope_diff(T,[a-b for a,b in zip(clocks[i],clocks[j])])
              for i in range(4) for j in range(i+1,4)]
    external=slope_diff(T,[statistics.mean(c[i]-off for c,off in zip(clocks,(0,.1,-.15,.23)))-T[i]
                           for i in range(N)])
    return max(abs(v) for v in internal),external

def main():
    cal=[session(100000+i,False) for i in range(2000)]
    thresh_int=sorted(x[0] for x in cal)[1979]
    thresh_ext=sorted(abs(x[1]) for x in cal)[1979]
    print('threshold_internal',round(thresh_int,6),'threshold_external',round(thresh_ext,6))
    print('scenario,internal_detect,external_detect,total')
    for label,drift in [('STABLE',False),('COMMON_DRIFT',True)]:
        vals=[session(200000+i,drift) for i in range(TRIALS)]
        internal=sum(x>thresh_int for x,y in vals)
        external=sum(abs(y)>thresh_ext for x,y in vals)
        print(f'{label},{internal},{external},{TRIALS}')
    rng=random.Random(43)
    clocks=[[t+offset+rng.gauss(0,SIGMA) for t in T] for offset in (0,.1,-.15,.23)]
    warped=[[v+.15*t*t for v,t in zip(c,T)] for c in clocks]
    max_pairwise_error=max(abs((clocks[i][k]-clocks[j][k])-(warped[i][k]-warped[j][k]))
                           for i in range(4) for j in range(i+1,4) for k in range(N))
    print('max_pairwise_gauge_error',f'{max_pairwise_error:.3g}')
    assert max_pairwise_error<1e-14
if __name__=='__main__':main()
