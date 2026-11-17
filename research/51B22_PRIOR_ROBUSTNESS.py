"""51B.22: sensitivity of sample complexity to noisy geometric priors.

Geometry is an independent, task-level hint, correct with probability q.
No GIAFilter, no learned geometry. Paired synthetic Monte Carlo, exact loss.
"""
import json, math, random

NS=(10,20,40,80,160,320)
QS=(0.5,0.6,0.75,0.9,1.0)
REGIMES=((0.05,0.99,0.01),(0.1,0.9,0.1),(0.2,0.8,0.2))
REPEATS=600
LAMBDA=0.02
EPS=(0.001,0.005)
SEED=51222026

def entropy(p):
    return 0 if p in (0,1) else -p*math.log(p)-(1-p)*math.log(1-p)

def upper(k,n):
    z=1.95996398454
    p=k/n
    return (p+z*z/(2*n)+z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)))/(1+z*z/n)

def mi(t):
    total=sum(map(sum,t))
    px=[sum(r) for r in t]
    py=[t[0][j]+t[1][j] for j in (0,1)]
    return sum(t[i][j]/total*math.log(t[i][j]*total/px[i]/py[j]) for i in (0,1) for j in (0,1))

def run():
    out=[]
    for regime,(prev,p1,p0) in enumerate(REGIMES):
        qf=prev*p1+(1-prev)*p0
        loss=entropy(qf)-prev*entropy(p1)-(1-prev)*entropy(p0)
        for n in NS:
            ep=0
            eh={str(q):0 for q in QS}
            for trial in range(REPEATS):
                rng=random.Random(SEED+regime*10000000+n*10000+trial)
                a=[[0.5,0.5],[0.5,0.5]]
                b=[[0.5,0.5],[0.5,0.5]]
                for _ in range(n):
                    s=int(rng.random()<prev)
                    d=int(rng.random()<0.5)
                    y=int(rng.random()<(p1 if s else p0))
                    a[s][y]+=1
                    b[d][y]+=1
                diff=mi(a)-mi(b)
                ep+=diff<0
                for q in QS:
                    correct=rng.random()<q
                    eh[str(q)]+=diff < (-LAMBDA if correct else LAMBDA)
            out.append({'regime':regime,'prevalence':prev,'p_y1_signal':p1,'p_y1_no_signal':p0,
                        'n':n,'loss_if_wrong':loss,
                        'P':{'errors':ep,'mean_delta':loss*ep/REPEATS,'upper95':loss*upper(ep,REPEATS)},
                        'H':{str(q):{'errors':eh[str(q)],'mean_delta':loss*eh[str(q)]/REPEATS,
                                      'upper95':loss*upper(eh[str(q)],REPEATS)} for q in QS}})
    thresholds=[]
    for regime in range(len(REGIMES)):
        rr=[r for r in out if r['regime']==regime]
        for eps in EPS:
            def first(key):
                return next((r['n'] for r in rr if key(r)<=eps),None)
            pn=first(lambda r:r['P']['upper95'])
            for q in QS:
                hn=first(lambda r:r['H'][str(q)]['upper95'])
                thresholds.append({'regime':regime,'epsilon':eps,'prior_correctness':q,
                                   'n_P':pn,'n_H':hn,'ratio_P_over_H':pn/hn if pn and hn else None})
    return {'status':'ROBUSTNESS_SIMULATION_COMPLETE','seed':SEED,'repeats':REPEATS,
            'lambda':LAMBDA,'n_grid':NS,'q_grid':QS,'regimes':REGIMES,
            'thresholds':thresholds,'rows':out,
            'limitations':'Prior correctness q imposed externally; fixed lambda; Wilson pointwise upper bounds; finite n grid; no operational GIAFilter.'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
