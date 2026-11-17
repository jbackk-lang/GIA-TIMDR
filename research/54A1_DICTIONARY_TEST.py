import zlib,random,json,struct
from pathlib import Path
rng=random.Random(5401)
base=[bytes(rng.randrange(256) for _ in range(1024)) for _ in range(8)]
sets={'repeated':[base[i%8] for i in range(128)],'random':[bytes(rng.randrange(256) for _ in range(1024)) for _ in range(128)]}
def independent(xs):
    return b''.join(struct.pack('>I',len(zlib.compress(x,9)))+zlib.compress(x,9) for x in xs)
def shared(xs):
    return zlib.compress(b''.join(xs),9)
def adaptive(xs):
    seen={};out=bytearray()
    for x in xs:
        if x in seen:out+=b'R'+struct.pack('>I',seen[x])
        else:
            packed=zlib.compress(x,9);out+=b'L'+struct.pack('>I',len(packed))+packed
            seen[x]=len(seen)
    return bytes(out)
def decode_adaptive(payload):
    i=0;dictionary=[];out=[]
    while i<len(payload):
        tag=payload[i:i+1];i+=1
        n=struct.unpack('>I',payload[i:i+4])[0];i+=4
        if tag==b'R':out.append(dictionary[n])
        elif tag==b'L':
            block=zlib.decompress(payload[i:i+n]);i+=n;dictionary.append(block);out.append(block)
        else:raise ValueError('invalid tag')
    return out
rows=[]
for name,xs in sets.items():
    a=independent(xs);b=shared(xs);c=adaptive(xs)
    assert decode_adaptive(c)==xs
    assert zlib.decompress(b)==b''.join(xs)
    rows.append({'dataset':name,'raw_bytes':sum(map(len,xs)),'independent_bytes':len(a),'whole_stream_bytes':len(b),'adaptive_bytes':len(c),'adaptive_vs_whole_ratio':round(len(c)/len(b),4)})
result={'status':'ROUNDTRIP_PASS','rows':rows,'note':'Synthetic 1 KiB blocks; adaptive is exact-block memoization, not novel; independent block compressor is an intentionally weak baseline; whole-stream zlib is stronger baseline.'}
Path('/mnt/data/54A/54A1_RESULTS.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
