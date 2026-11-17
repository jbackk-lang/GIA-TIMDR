"""52A.2: actual zlib byte sizes including codebook and stream header."""
import json, random, struct, zlib, math
SEED=5202
P_SIGNAL=.05
P_F={0:.01,1:.99}
MAPS={'constant':(0,0,0,0),'signal':(0,0,1,1),'distractor':(0,1,0,1),'identity':(0,1,2,3)}

def h(p):
    return -sum(v*math.log2(v) for v in (p,1-p) if v>0)

def exact_delta(labels):
    weights=[.475,.475,.025,.025]
    pz={v:sum(w for w,x in zip(weights,labels) if x==v) for v in set(labels)}
    hf=0
    for v,p in pz.items():
        pf=sum(w*P_F[i//2] for i,(w,x) in enumerate(zip(weights,labels)) if x==v)/p
        hf+=p*h(pf)
    return hf-(.95*h(.01)+.05*h(.99))

def main():
    results=[]
    for n in (100,1000,10000,100000):
        rng=random.Random(SEED+n)
        states=[2*int(rng.random()<P_SIGNAL)+int(rng.random()<.5) for _ in range(n)]
        for name,mapping in MAPS.items():
            stream=bytes(mapping[s] for s in states)
            # Four mapping bytes and a four-byte stream length are charged.
            payload=struct.pack('>I',n)+bytes(mapping)+zlib.compress(stream,level=9)
            decoded=zlib.decompress(payload[8:])
            assert decoded==stream and len(decoded)==n
            assert payload[4:8]==bytes(mapping)
            results.append({'n':n,'representation':name,'symbols':len(set(mapping)),
                            'total_bytes':len(payload),'bits_per_history':8*len(payload)/n,
                            'delta_bits':exact_delta(mapping)})
    return {'status':'ACTUAL_CODING_PASS','seed':SEED,'codec':'zlib DEFLATE level 9',
            'header':'4-byte big-endian n + 4-byte mapping + zlib payload','rows':results,
            'limitations':'Codebook mapping is fixed/known and charged 4 bytes; no model training or decoding of original H; single seeded stream per n; DEFLATE is not an optimal entropy coder; cost is encoding Z, not predictive decoder parameters.'}

if __name__=='__main__':print(json.dumps(main(),indent=2))
