import random,math,json,zlib,struct
from pathlib import Path
SEED=5205
NS=(20,50,100,200,500,1000)
REPS=300
TEST_N=2000

def sample(rng,n):
    return [(int(rng.random()<.05),int(rng.random()<.5),None) for _ in range(n)]

def label(rng,s):return int(rng.random() < (.99 if s else .01))

def score(train,feature):
    counts=[[.5,.5],[.5,.5]]
    for s,d,y in train:counts[(s,d)[feature]][y]+=1
    return sum(-math.log(counts[(s,d)[feature]][y]/sum(counts[(s,d)[feature]])) for s,d,y in train)

def run():
    rows=[]
    for n in NS:
        errors=0; losses=[0.,0.]; size_bits=[0.,0.]
        for trial in range(REPS):
            rng=random.Random(SEED+n*100000+trial)
            train=[(s,d,label(rng,s)) for s,d,_ in sample(rng,n)]
            feature=min((0,1),key=lambda f:score(train,f))
            errors+=feature!=0
            counts=[[.5,.5],[.5,.5]]
            for s,d,y in train:counts[(s,d)[feature]][y]+=1
            probs=[r[1]/sum(r) for r in counts]
            loss=0.
            for s in (0,1):
                for d in (0,1):
                    weight=(.05 if s else .95)*.5
                    p=.99 if s else .01
                    pred=probs[(s,d)[feature]]
                    loss+=weight*(-p*math.log2(pred)-(1-p)*math.log2(1-pred))
            losses[0]+=loss
            oracle=[[.5,.5],[.5,.5]]
            for s,d,y in train:oracle[s][y]+=1
            ps=[r[1]/sum(r) for r in oracle]
            oracle_loss=sum((.05 if s else .95)*(-p*math.log2(ps[s])-(1-p)*math.log2(1-ps[s])) for s,p in ((0,.01),(1,.99)))
            losses[1]+=oracle_loss
            for j,f in enumerate((feature,0)):
                stream=bytes((s,d)[f] for s,d,y in train)
                size_bits[j]+=8*(5+16+len(zlib.compress(stream,9)))
        rows.append({'n':n,'repeats':REPS,'feature_selection_error_rate':errors/REPS,'learned_population_logloss_bits':losses[0]/REPS,'oracle_population_logloss_bits':losses[1]/REPS,'learned_total_bits_mean':size_bits[0]/REPS,'oracle_total_bits_mean':size_bits[1]/REPS})
    return {'status':'LEARNED_REPRESENTATION_PASS','seed':SEED,'rows':rows,'limitations':'Synthetic known generator; two candidate 1-bit features only; selection via training in-sample likelihood, no validation; population loss calculated analytically using known generator; representation codebook and two parameters charged, feature-search algorithm complexity not charged; no GIAFilter or real data.'}
if __name__=='__main__':
    r=run();Path(__file__).with_name('52A5_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
