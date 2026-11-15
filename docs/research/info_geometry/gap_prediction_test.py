import random, math
N=101

def run(mode,negative=False,n=2000):
    rng=random.Random(20261114+{'identity':0,'affine':1,'nonlinear':2}[mode]+100*negative)
    counts={k:0 for k in ['SIGN','RAW_DELTA','NORMALIZED_DELTA']}
    for i in range(n):
        label=i%2
        gap=rng.randint(12,32) if label==0 else rng.randint(58,78)
        a=rng.randint(5,95-gap);b=a+gap
        if rng.random()<.5: a,b=b,a
        offset=rng.uniform(-1000,1000)
        scale=math.exp(rng.uniform(-1,1))
        power=math.exp(rng.uniform(-.8,.8))
        def f(t):
            if mode=='identity':return t
            if mode=='affine':return offset+scale*t
            return offset+100*scale*(t/100)**power
        delta=f(b)-f(a)
        raw=abs(delta)
        norm=raw/(f(100)-f(0))
        future=rng.randrange(2) if negative else label
        preds={'SIGN':int(delta>0),'RAW_DELTA':int(raw>45),'NORMALIZED_DELTA':int(norm>.45)}
        for k in counts:counts[k]+=preds[k]==future
    return {k:round(v/n,4) for k,v in counts.items()}

if __name__=='__main__':
    for mode in ['identity','affine','nonlinear']:
        print(mode,'signal',run(mode),'negative',run(mode,True))
