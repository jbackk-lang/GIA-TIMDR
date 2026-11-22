import gzip, json, random
N=16384
W=64

def datasets():
    r=random.Random(549)
    for name in ('aligned','rotating','switching','random'):
        sig=bytearray()
        geom=bytearray()
        for i in range(N):
            w=i//W
            if name=='aligned':
                orient=1
                x=(i//3)%256
            elif name=='rotating':
                orient=(w//4)%2
                x=((i//3)*7+(w//4)*13)%256
            elif name=='switching':
                orient=(w//3)%2
                x=(i*3 if orient else (i//3)*7)%256
            else:
                orient=r.randrange(2)
                x=r.randrange(256)
            geom.append(orient)
            sig.append(x)
        yield name,bytes(sig),bytes(geom)

def encode(src,geom,mode,inverse=False):
    out=bytearray()
    hist=bytearray()
    scores=[0,0,0]
    aligned=0
    count=0
    for i,v in enumerate(src):
        if i%W==0 and i:
            aligned=sum(geom[i-W:i])
            count=W
        j_prev=aligned*256//count if count else 128
        pred=[hist[-1] if i else 0,
              hist[-3] if i>=3 else 0,
              hist[-W] if i>=W else 0]
        if mode=='raw':
            p=0
        elif mode=='static':
            p=pred[2]
        elif mode=='adaptive':
            p=pred[min(range(3),key=lambda k:(scores[k],k))]
        elif mode=='geometry':
            penalty=[(255-j_prev)//4,0,j_prev//4]
            p=pred[min(range(3),key=lambda k:(scores[k]+penalty[k],k))]
        else:
            raise ValueError(mode)
        x=(v+p)%256 if inverse else v
        out.append(x if inverse else (x-p)%256)
        for k in range(3):
            d=(x-pred[k])%256
            d=min(d,256-d)
            scores[k]=(15*scores[k])//16+d
        hist.append(x)
    return bytes(out)

def run():
    rows=[]
    for name,sig,geom in datasets():
        side=len(gzip.compress(geom,compresslevel=9,mtime=0))
        row={'dataset':name,'bytes':len(sig),'geometry_side_bytes':side}
        for mode in ('raw','static','adaptive','geometry'):
            transformed=encode(sig,geom,mode)
            assert encode(transformed,geom,mode,True)==sig
            size=len(gzip.compress(transformed,compresslevel=9,mtime=0))
            row[mode]=size
            row[mode+'_total']=size+side
        rows.append(row)
    return rows

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
