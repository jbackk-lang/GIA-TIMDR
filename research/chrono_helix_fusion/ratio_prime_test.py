"""Prime-indexed helix turn concentration versus random turn subsets.
Exploratory arithmetic control, not real signal decoding.
"""
import json
from pathlib import Path
import numpy as np

def run(seed=20261119):
    rng=np.random.default_rng(seed);N=10000
    sieve=np.ones(N+1,dtype=bool);sieve[:2]=False
    for p in range(2,int(N**.5)+1):
        if sieve[p]:sieve[p*p::p]=False
    n=np.arange(2,N+1);prime=sieve[2:]
    ratios={'pi_over_sqrt2_plus_sqrt3':np.pi/(np.sqrt(2)+np.sqrt(3)),
            'inverse':(np.sqrt(2)+np.sqrt(3))/np.pi,
            'pi_over_sqrt2_plus_sqrt5':np.pi/(np.sqrt(2)+np.sqrt(5)),
            'sqrt2':np.sqrt(2),'golden_ratio':(1+np.sqrt(5))/2}
    results={}
    for name,r in ratios.items():
        rows=[]
        for upper in [1000,3000,10000]:
            idx=n<=upper;ph=np.exp(2j*np.pi*np.remainder(n[idx]*r,1))
            p=prime[idx];obs=float(abs(ph[p].mean()));m=p.sum()
            null=np.array([abs(ph[rng.choice(len(ph),m,replace=False)].mean()) for _ in range(999)])
            rows.append({'turns':upper,'primes':int(m),'prime_phase_concentration':obs,
                         'null_mean':float(null.mean()),'null_q95':float(np.quantile(null,.95)),
                         'permutation_p_one_sided':float((1+np.sum(null>=obs))/1000)})
        results[name]=rows
    return {'method':'Circular concentration of prime-indexed turns versus random subsets',
            'seed':seed,'results':results,
            'limitations':['No measured signal or CHF decoder.',
                           'Exploratory unadjusted tests across five ratios and three horizons.',
                           'Random subsets do not preserve prime spacing or density variation.',
                           'Near-unity ratios induce long beat periods and finite-window drift.']}

if __name__=='__main__':
    report=run()
    output=Path(__file__).with_name('ratio_prime_results.json')
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
