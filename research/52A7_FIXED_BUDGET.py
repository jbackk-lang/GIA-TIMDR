"""52A.7: fixed sample budget, weak signal and correlated nuisance features."""
import random,math,json
from pathlib import Path
SEED=5207
REPS=300
TOTALS=(40,100,200)
MS=(8,32)
FRACTIONS=(0,.25,.5)

def make(rng,n,m):
    out=[]
    for _ in range(n):
        s=int(rng.random()<.5)
        y=s if rng.random()<.65 else 1-s
        x=[s]+[s if rng.random()<.75 else 1-s for _ in range(m-1)]
        out.append((x,y))
    return out

def fit(rows,j):
    c=[[.5,.5],[.5,.5]]
    for x,y in rows:c[x[j]][y]+=1
    return [r[1]/sum(r) for r in c]

def score(rows,j,p):
    return sum(-math.log2(p[x[j]] if y else 1-p[x[j]]) for x,y in rows)/len(rows)

def true_loss(j,p):
    if j==0:q0,q1=.35,.65
    else:q0,q1=.425,.575
    return .5*sum(-q*math.log2(v)-(1-q)*math.log2(1-v) for q,v in ((q0,p[0]),(q1,p[1])))

def run():
    rows=[]
    for total in TOTALS:
        for m in MS:
            for fraction in FRACTIONS:
                val_n=round(total*fraction);train_n=total-val_n
                assert train_n>=20
                wrong=0;loss=0;oracle=0
                for trial in range(REPS):
                    rng=random.Random(SEED+total*1000000+m*10000+int(fraction*100)*1000+trial)
                    train=make(rng,train_n,m)
                    val=make(rng,val_n,m) if val_n else train
                    pars=[fit(train,j) for j in range(m)]
                    chosen=min(range(m),key=lambda j:score(val,j,pars[j]))
                    wrong+=chosen!=0
                    loss+=true_loss(chosen,pars[chosen])
                    oracle+=true_loss(0,pars[0])
                rows.append(dict(total_n=total,candidates=m,validation_fraction=fraction,train_n=train_n,validation_n=val_n,wrong_rate=wrong/REPS,population_logloss_bits=loss/REPS,oracle_loss_bits=oracle/REPS))
    return dict(status='FIXED_BUDGET_PASS',seed=SEED,repeats=REPS,rows=rows,limitations='Synthetic balanced binary signal with 65% label accuracy, nuisance features 75% correlated with signal; separate train/validation from same distribution; no real data; no GIAFilter; model parameter cost excluded.')

if __name__=='__main__':
    result=run()
    Path(__file__).with_name('52A7_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
