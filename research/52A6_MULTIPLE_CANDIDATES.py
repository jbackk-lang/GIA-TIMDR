"""52A.6: independent validation versus training selection with many nuisance features."""
import json, math, random
from pathlib import Path
SEED=5206
NS=(20,50,100)
MS=(2,8,32,128)
REPS=300
VALIDATION_N=100

def sample(rng,n,m):
    rows=[]
    for _ in range(n):
        s=int(rng.random()<.05)
        xs=[s]+[int(rng.random()<.5) for _ in range(m-1)]
        y=int(rng.random()<(.99 if s else .01))
        rows.append((xs,y))
    return rows

def fit(train,j):
    c=[[.5,.5],[.5,.5]]
    for x,y in train:c[x[j]][y]+=1
    return [r[1]/sum(r) for r in c]

def logloss(data,j,p):
    return sum(-math.log2(p[x[j]] if y else 1-p[x[j]]) for x,y in data)/len(data)

def population_loss(j,p):
    if j==0:
        return sum(w*(-q*math.log2(p[s])-(1-q)*math.log2(1-p[s])) for s,w,q in ((0,.95,.01),(1,.05,.99)))
    q=.05*.99+.95*.01
    return sum(.5*(-q*math.log2(v)-(1-q)*math.log2(1-v)) for v in p)

def run():
    rows=[]
    for n in NS:
        for m in MS:
            errs={'train':0,'validation':0}
            losses={'train':0.,'validation':0.,'oracle':0.}
            for trial in range(REPS):
                rng=random.Random(SEED+n*10000000+m*10000+trial)
                train=sample(rng,n,m)
                val=sample(rng,VALIDATION_N,m)
                params=[fit(train,j) for j in range(m)]
                train_scores=[logloss(train,j,params[j]) for j in range(m)]
                val_scores=[logloss(val,j,params[j]) for j in range(m)]
                picks={'train':min(range(m),key=lambda j:train_scores[j]),
                       'validation':min(range(m),key=lambda j:val_scores[j])}
                for method,j in picks.items():
                    errs[method]+=j!=0
                    losses[method]+=population_loss(j,params[j])
                losses['oracle']+=population_loss(0,params[0])
            rows.append({'train_n':n,'candidates':m,'validation_n':VALIDATION_N,'repeats':REPS,
                         'train_wrong_rate':errs['train']/REPS,'validation_wrong_rate':errs['validation']/REPS,
                         'train_population_logloss_bits':losses['train']/REPS,
                         'validation_population_logloss_bits':losses['validation']/REPS,
                         'oracle_population_logloss_bits':losses['oracle']/REPS})
    assert len(rows)==len(NS)*len(MS)
    assert all(r['oracle_population_logloss_bits']<=r['train_population_logloss_bits']+1e-10 for r in rows)
    assert all(r['oracle_population_logloss_bits']<=r['validation_population_logloss_bits']+1e-10 for r in rows)
    return {'status':'MULTIPLE_CANDIDATES_PASS','seed':SEED,'rows':rows,
            'limitations':'Synthetic generator; signal feature is index 0, nuisance features independent; 300 trials, one validation size; selection comparisons reuse trained probabilities, no refitting; population loss uses known generator; no real data or GIAFilter.'}

if __name__=='__main__':
    out=run()
    Path(__file__).with_name('52A6_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
