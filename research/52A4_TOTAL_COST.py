"""52A.4: synthetic total coding cost and held-out predictive log-loss."""
import json,random,math,zlib,struct,time
from pathlib import Path
MAPS={'constant':(0,0,0,0),'signal':(0,0,1,1),'distractor':(0,1,0,1),'identity':(0,1,2,3)}
SEED=5204

def sample(rng,n):
    out=[]
    for _ in range(n):
        s=int(rng.random()<.05);d=int(rng.random()<.5);y=int(rng.random() < (.99 if s else .01))
        out.append((2*s+d,y))
    return out

def run():
    rng=random.Random(SEED)
    test=sample(rng,20000)
    rows=[]
    for n in (20,100,1000,10000):
        train=sample(rng,n)
        for name,mapping in MAPS.items():
            start=time.perf_counter_ns()
            counts=[[.5,.5] for _ in range(max(mapping)+1)]
            for state,y in train: counts[mapping[state]][y]+=1
            params=[r[1]/sum(r) for r in counts]
            train_ms=(time.perf_counter_ns()-start)/1e6
            ll=-sum(math.log2(params[mapping[state]] if y else 1-params[mapping[state]]) for state,y in test)/len(test)
            stream=bytes(mapping[state] for state,_ in train)
            encoded=struct.pack('>I',n)+bytes(mapping)+zlib.compress(stream,9)
            model_bits=64*len(params)
            total_bits=8*len(encoded)+model_bits
            rows.append({'train_n':n,'representation':name,'test_logloss_bits':ll,'encoded_bytes':len(encoded),'representation_bits':8*len(encoded),'model_bits':model_bits,'total_bits':total_bits,'total_bits_per_training_history':total_bits/n,'train_fit_ms':train_ms,'symbols':len(params)})
    h=lambda p: -p*math.log2(p)-(1-p)*math.log2(1-p)
    oracle=.95*h(.01)+.05*h(.99)
    assert all(r['total_bits']==r['representation_bits']+r['model_bits'] for r in rows)
    assert all(r['test_logloss_bits']>=0 for r in rows)
    return {'status':'TOTAL_COST_TEST_PASS','seed':SEED,'test_n':len(test),'oracle_logloss_bits':oracle,'model_budget':'64 bits per conditional Bernoulli parameter, fixed convention (not serialized fitted floats)','rows':rows,'limitations':'Synthetic generator; training stream compressed but not independently encoded target labels; representation mapping assumed known and charged 4 bytes; model bits are explicit accounting convention, not measured model file; no cost of learning representation, no real dataset; timing excludes feature extraction and codec.'}

if __name__=='__main__':
    result=run();Path(__file__).with_name('52A4_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'oracle_logloss_bits':result['oracle_logloss_bits'],'rows':result['rows']},indent=2))
