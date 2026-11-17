"""51B.23: actual reference gia_select as geometric prior (not operational GIAFilter)."""
import json, math, random
from core.trm_gia_projections import Event, EventGraph, fit_line_reference, gia_select

SEED=51232026
N_GRID=(10,20,40,80,160)
QS=(0.5,0.75,0.9,1.0)
REPEATS=300
PENALTY=0.02
EPS=0.005

def h(p):
    return 0 if p in (0,1) else -p*math.log(p)-(1-p)*math.log(1-p)

def mi(t):
    z=sum(map(sum,t))
    a=[sum(r) for r in t]
    b=[t[0][j]+t[1][j] for j in (0,1)]
    return sum(t[i][j]/z*math.log(t[i][j]*z/a[i]/b[j]) for i in (0,1) for j in (0,1))

def ucb(k,n):
    z=1.95996398454
    p=k/n
    return (p+z*z/(2*n)+z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)))/(1+z*z/n)

def main():
    ref=fit_line_reference([(-2,0,0),(-1,0,0),(0,0,0),(1,0,0),(2,0,0)],0.2)
    p1,p0,prev=0.99,0.01,0.05
    qf=prev*p1+(1-prev)*p0
    loss=h(qf)-prev*h(p1)-(1-prev)*h(p0)
    rows=[]
    for n in N_GRID:
        errors={str(q):{'P':0,'H':0,'G':0} for q in QS}
        for trial in range(REPEATS):
            rng=random.Random(SEED+n*10000+trial)
            a=[[0.5,0.5],[0.5,0.5]]
            b=[[0.5,0.5],[0.5,0.5]]
            for _ in range(n):
                s=int(rng.random()<prev)
                d=int(rng.random()<0.5)
                y=int(rng.random()<(p1 if s else p0))
                a[s][y]+=1
                b[d][y]+=1
            diff=mi(a)-mi(b)
            for q in QS:
                aligned=rng.random()<q
                # Geometry alone determines which event the real gia_select retains.
                signal_pos=(0,0,0) if aligned else (0,1,0)
                distractor_pos=(0,1,0) if aligned else (0,0,0)
                graph=EventGraph((Event('signal',1.0,0,signal_pos),
                                  Event('distractor',1.0,1,distractor_pos)))
                kept=gia_select(graph,ref)
                assert len(kept.events)==1
                geometric=kept.events[0].id
                errors[str(q)]['G']+=geometric!='signal'
                errors[str(q)]['P']+=diff<0
                errors[str(q)]['H']+=diff<(-PENALTY if geometric=='signal' else PENALTY)
        for q in QS:
            row={'n':n,'q':q,'budget_events':1,'repeats':REPEATS}
            for method in ('G','P','H'):
                k=errors[str(q)][method]
                row[method]={'wrong':k,'wrong_rate':k/REPEATS,
                             'mean_delta_nats':loss*k/REPEATS,
                             'upper95_delta_nats':loss*ucb(k,REPEATS)}
            rows.append(row)
    thresholds=[]
    for q in QS:
        subset=[r for r in rows if r['q']==q]
        threshold={'q':q,'epsilon':EPS}
        for method in ('G','P','H'):
            threshold['n_'+method]=next((r['n'] for r in subset
                         if r[method]['upper95_delta_nats']<=EPS),None)
        pn,hn=threshold['n_P'],threshold['n_H']
        threshold['ratio_P_over_H']=pn/hn if pn and hn else None
        thresholds.append(threshold)
    return {'status':'REFERENCE_GIA_SELECT_PASS','seed':SEED,'loss_if_wrong_nats':loss,
            'calibration':'PCA fitted once on x-axis calibration points; no labels',
            'radius':ref.radius,'penalty':PENALTY,'rows':rows,'thresholds':thresholds,
            'limitations':'Real reference gia_select invoked, but event positions are synthetically assigned to achieve target q; not operational GIAFilter; Wilson pointwise; fixed n grid.'}

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
