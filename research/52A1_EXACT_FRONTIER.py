"""52A.1: exact deterministic predictive compression frontier, H=(S,D)."""
import itertools, math, json
P_S=.05
P_F={0:.01,1:.99}
STATES=[(s,d) for s in (0,1) for d in (0,1)]
WEIGHTS=[(P_S if s else 1-P_S)*.5 for s,d in STATES]

def entropy(probs):
    return -sum(p*math.log2(p) for p in probs if p>0)

def partition_labels(n):
    def rec(prefix, maxlabel):
        if len(prefix)==n:
            yield tuple(prefix);return
        for label in range(maxlabel+2):
            yield from rec(prefix+[label],max(maxlabel,label))
    yield from rec([0],0)

def evaluate(labels):
    k=max(labels)+1
    pz=[sum(WEIGHTS[i] for i in range(4) if labels[i]==j) for j in range(k)]
    hz=entropy(pz)
    fixed_bits=math.ceil(math.log2(k))
    conditional=0
    for j,p in enumerate(pz):
        pf=sum(WEIGHTS[i]*P_F[STATES[i][0]] for i in range(4) if labels[i]==j)/p
        conditional+=p*entropy((pf,1-pf))
    base=sum(WEIGHTS[i]*entropy((P_F[STATES[i][0]],1-P_F[STATES[i][0]])) for i in range(4))
    return {'labels':list(labels),'symbols':k,'fixed_bits_per_history':fixed_bits,'entropy_bits_per_history':hz,'delta_bits':conditional-base}

def main():
    rows=[evaluate(x) for x in partition_labels(4)]
    assert len(rows)==15
    names={'constant':(0,0,0,0),'signal':(0,0,1,1),'distractor':(0,1,0,1),'identity':(0,1,2,3)}
    named={name:next(r for r in rows if tuple(r['labels'])==lab) for name,lab in names.items()}
    assert abs(named['signal']['delta_bits'])<1e-12
    assert abs(named['distractor']['delta_bits']-named['constant']['delta_bits'])<1e-12
    assert named['signal']['entropy_bits_per_history']<named['identity']['entropy_bits_per_history']
    frontier=[]
    for r in sorted(rows,key=lambda x:(x['entropy_bits_per_history'],x['delta_bits'])):
        if not any(x['entropy_bits_per_history']<=r['entropy_bits_per_history']+1e-12 and x['delta_bits']<=r['delta_bits']+1e-12 and (x['entropy_bits_per_history']<r['entropy_bits_per_history']-1e-12 or x['delta_bits']<r['delta_bits']-1e-12) for x in rows):
            frontier.append(r)
    unique=[]
    for r in frontier:
        if not any(abs(r['entropy_bits_per_history']-u['entropy_bits_per_history'])<1e-12 and abs(r['delta_bits']-u['delta_bits'])<1e-12 for u in unique):unique.append(r)
    return {'status':'EXACT_ENUMERATION_PASS','states':STATES,'probabilities':WEIGHTS,'partitions_checked':len(rows),'units':'bits per history; ideal Shannon entropy is lower bound, not actual coded length','named':named,'pareto_entropy':unique,'all_partitions':rows,'limitations':'Known synthetic generator; no real data, no actual compressor, no decoder/model metadata; fixed-length cost excludes codebook; entropy is asymptotic ideal lower bound.'}

if __name__=='__main__':print(json.dumps(main(),indent=2))
