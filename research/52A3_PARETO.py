"""52A.3: measured three-objective Pareto frontier on synthetic S,D histories."""
import json,random,struct,zlib,time,statistics,math
from pathlib import Path
MAPS={'constant':(0,0,0,0),'signal':(0,0,1,1),'distractor':(0,1,0,1),'identity':(0,1,2,3)}
N=100000; REPEATS=7; SEED=5203

def h(p):
    return -sum(x*math.log2(x) for x in (p,1-p) if x)

def delta(m):
    w=(.475,.475,.025,.025)
    base=.95*h(.01)+.05*h(.99)
    result=0
    for label in set(m):
        ids=[i for i in range(4) if m[i]==label]
        mass=sum(w[i] for i in ids)
        pf=sum(w[i]*(.99 if i//2 else .01) for i in ids)/mass
        result+=mass*h(pf)
    return result-base

def main():
    rng=random.Random(SEED)
    states=bytes(2*int(rng.random()<.05)+int(rng.random()<.5) for _ in range(N))
    rows=[]
    for name,mapping in MAPS.items():
        mapping_table=bytes(mapping)
        stream=states.translate(mapping_table+bytes(range(4,256)))
        assert all(stream[i]==mapping[states[i]] for i in (0,1,999,N-1))
        enc_times=[];dec_times=[];payloads=[]
        for _ in range(REPEATS):
            t0=time.perf_counter_ns()
            payload=struct.pack('>I',N)+mapping_table+zlib.compress(stream,9)
            t1=time.perf_counter_ns()
            decoded=zlib.decompress(payload[8:])
            t2=time.perf_counter_ns()
            assert decoded==stream and payload[4:8]==mapping_table
            payloads.append(len(payload));enc_times.append((t1-t0)/1e6);dec_times.append((t2-t1)/1e6)
        assert len(set(payloads))==1
        rows.append({'representation':name,'n':N,'total_bytes':payloads[0], 'bits_per_history':8*payloads[0]/N,'delta_bits':delta(mapping),'encode_median_ms':statistics.median(enc_times),'decode_median_ms':statistics.median(dec_times),'encode_runs_ms':enc_times,'decode_runs_ms':dec_times})
    for a in rows:
        a['pareto_3d']=not any(all(b[k]<=a[k]+1e-12 for k in ('bits_per_history','delta_bits','encode_median_ms')) and any(b[k]<a[k]-1e-12 for k in ('bits_per_history','delta_bits','encode_median_ms')) for b in rows if b is not a)
        a['pareto_2d']=not any(all(b[k]<=a[k]+1e-12 for k in ('bits_per_history','delta_bits')) and any(b[k]<a[k]-1e-12 for k in ('bits_per_history','delta_bits')) for b in rows if b is not a)
    assert next(x for x in rows if x['representation']=='signal')['delta_bits']<1e-12
    assert next(x for x in rows if x['representation']=='identity')['delta_bits']<1e-12
    return {'status':'MEASURED_PARETO_PASS','seed':SEED,'n':N,'repeats':REPEATS,'codec':'zlib level 9','header_bytes':8,'timing':'perf_counter_ns, sequential runs, median, machine-specific; encoding time excludes mapping transform and predictor cost','rows':rows,'limitations':'One synthetic dataset, four fixed representations, 7 sequential timing repetitions, no cross-machine inference; timings sensitive to scheduler/cache; codebook/model training cost omitted; Pareto limited to tested choices.'}
if __name__=='__main__':
    result=main();p=Path(__file__).with_name('52A3_RESULTS.json');p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'rows':[{k:v for k,v in r.items() if not k.endswith('_runs_ms')} for r in result['rows']]},indent=2))
