import gzip, json, random, struct
N=32768
LAGS=(1,3,64)
HEADER=b'GIA54A14\x01\x00\x00\x00'

def sources():
    rng=random.Random(5414)
    yield 'random',bytes(rng.randrange(256) for _ in range(N))
    for block in (256,512,1024):
        out=bytearray()
        for i in range(N):
            lag=LAGS[(i//block)%3]
            if i%block<lag or rng.randrange(100)<2:
                out.append(rng.randrange(256))
            else:
                out.append(out[i-lag])
        yield f'lag_switch_{block}',bytes(out)
    yield 'constant',bytes((i//512)%256 for i in range(N))

def predictors(hist):
    return [hist[-lag] if len(hist)>=lag else 0 for lag in LAGS]

def adaptive(data, decode=False):
    hist=bytearray(); out=bytearray();scores=[0]*3
    for v in data:
        preds=predictors(hist); k=min(range(3),key=lambda j:(scores[j],j));p=preds[k]
        x=(v+p)%256 if decode else v
        out.append(x if decode else (x-p)%256)
        for j in range(3):
            d=(x-preds[j])%256;scores[j]=scores[j]*15//16+min(d,256-d)
        hist.append(x)
    return bytes(out)

def best_selector(data,start,end):
    costs=[0]*3
    for i in range(start,end):
        for j,lag in enumerate(LAGS):
            p=data[i-lag] if i>=lag else 0
            d=(data[i]-p)%256
            costs[j]+=min(d,256-d)
    return min(range(3),key=lambda j:(costs[j],j))

def transform(data, block, selectors, decode=False):
    hist=bytearray();out=bytearray()
    for i,v in enumerate(data):
        lag=LAGS[selectors[i//block]]
        p=hist[-lag] if len(hist)>=lag else 0
        x=(v+p)%256 if decode else v
        out.append(x if decode else (x-p)%256)
        hist.append(x)
    return bytes(out)

def pack(selectors):
    b=bytearray((len(selectors)+3)//4)
    for i,k in enumerate(selectors):b[i//4]|=k<<((i%4)*2)
    return bytes(b)

def unpack(data,count):
    return [(data[i//4]>>((i%4)*2))&3 for i in range(count)]

def coded(data,block,method):
    count=(len(data)+block-1)//block
    if method=='oracle':
        selectors=[best_selector(data,i*block,min(len(data),(i+1)*block)) for i in range(count)]
    elif method=='causal':
        selectors=[0]+[best_selector(data,(i-1)*block,i*block) for i in range(1,count)]
    else:raise ValueError(method)
    raw_side=pack(selectors)
    side=gzip.compress(raw_side,compresslevel=9,mtime=0)
    residual=transform(data,block,selectors)
    compressed=gzip.compress(residual,compresslevel=9,mtime=0)
    blob=HEADER+struct.pack('<II',block,len(side))+side+compressed
    assert blob[:12]==HEADER
    b,side_len=struct.unpack('<II',blob[12:20]); side2=blob[20:20+side_len]
    sel2=unpack(gzip.decompress(side2),(len(data)+b-1)//b)
    assert all(k<3 for k in sel2)
    assert transform(gzip.decompress(blob[20+side_len:]),b,sel2,True)==data
    return {'total_bytes':len(blob),'residual_gzip_bytes':len(compressed),'selector_gzip_bytes':len(side),'selector_count':count,'selector_changes':sum(a!=b for a,b in zip(selectors,selectors[1:]))}

def main():
    rows=[]
    for name,data in sources():
        assert adaptive(adaptive(data),True)==data
        baseline=len(HEADER)+len(gzip.compress(data,compresslevel=9,mtime=0))
        ad=len(HEADER)+len(gzip.compress(adaptive(data),compresslevel=9,mtime=0))
        row={'dataset':name,'input_bytes':len(data),'gzip_total_bytes':baseline,'adaptive_total_bytes':ad}
        for block in (256,512,1024):
            for mode in ('causal','oracle'):
                row[f'{mode}_{block}']=coded(data,block,mode)
        rows.append(row)
    return {'format':'gzip raw and adaptive include 12-byte header; switched include 20-byte header + compressed selector stream','rows':rows}
if __name__=='__main__':print(json.dumps(main(),indent=2))
