"""53E.1: deterministic accounting model for amortized predictive memory.
Operation units are NOT joules. Physical energy storage is not modeled.
"""
import json
from pathlib import Path

COMPUTE=100
READ=2
WRITE=25
RETAIN=0.05

def simulate(unique,reuse):
    queries=[k for _ in range(reuse) for k in range(unique)]
    cached=set()
    baseline=0.0; memory=0.0
    for key in queries:
        baseline+=COMPUTE
        memory+=RETAIN*len(cached)
        memory+=READ
        if key not in cached:
            memory+=COMPUTE+WRITE
            cached.add(key)
    return {'unique_keys':unique,'reuse_per_key':reuse,'queries':len(queries),
            'baseline_units':round(baseline,5),'memory_units':round(memory,5),
            'savings_units':round(baseline-memory,5),
            'savings_fraction':round((baseline-memory)/baseline,8),
            'cache_entries':len(cached)}

def main():
    rows=[simulate(unique,reuse) for unique in (1,10,100) for reuse in (1,2,5,10,50)]
    assert len(rows)==15
    assert all(r['savings_units']<0 for r in rows if r['reuse_per_key']==1)
    assert any(r['savings_units']>0 for r in rows)
    assert any(r['savings_units']<0 for r in rows)
    return {'status':'ACCOUNTING_MODEL_PASS','units':'arbitrary operation-equivalent units, NOT joules',
            'parameters':{'compute':COMPUTE,'read':READ,'write':WRITE,'retention_per_entry_per_step':RETAIN},
            'rows':rows,'limitations':'Deterministic assumed costs; no hardware measurements, no thermodynamic energy measurements, no physical energy accumulation. Memory retains reusable answers, not energy. Identical prediction quality is assumed by exact caching.'}

if __name__=='__main__':
    result=main()
    Path(__file__).with_name('53E1_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
