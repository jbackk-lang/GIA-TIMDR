"""Strict local MIN/MAX/delta-time test. Requires numpy and scikit-learn."""
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
WINDOWS=[(10,23),(27,56),(60,90),(102,121)]

def generate(n,seed,shift=0):
    r=np.random.default_rng(seed); X=[]; Y=[]
    for i in range(n):
        z=i%2
        x=r.normal(0,.12,128)
        x[16]=-5; x[112]=5
        for c,a in zip(([35,48] if z==0 else [68,81]),[1.5,-1.5]):
            c+=shift
            for k in range(-2,3):
                j=c+k
                if 0<=j<128 and j not in (16,112):
                    x[j]+=a*np.exp(-.5*(k/1.1)**2)
        x[16]=-5; x[112]=5
        alpha=.15 if z==0 else .85
        y=np.empty(128); y[0]=r.normal()
        for j in range(1,128):
            y[j]=alpha*y[j-1]+np.sqrt(1-alpha**2)*r.normal()
        Y.append(int(np.corrcoef(y[:-1],y[1:])[0,1]>.5))
        X.append(x)
    return np.asarray(X),np.asarray(Y)

def features(X,kind):
    out=[]
    for x in X:
        if kind=='global':
            out.append([x.min(),x.max(),abs(x.argmax()-x.argmin())/127])
            continue
        if kind=='full':
            out.append(x)
            continue
        triples=[]
        for a,b in WINDOWS:
            w=x[a:b]; lo=int(w.argmin()); hi=int(w.argmax())
            triples.append([w[lo],w[hi],(hi-lo)/(b-a-1)])
        if kind=='unordered':
            triples=sorted(triples,key=lambda t:(t[0],t[1],t[2]))
        if kind=='triples_plus_position':
            out.append(np.asarray(triples).ravel().tolist()+[(a+b)/254 for a,b in WINDOWS])
        else:
            out.append(np.asarray(triples).ravel())
    return np.asarray(out)

if __name__=='__main__':
    train,yt=generate(2000,61)
    for shift in (0,4,10,18):
        test,ye=generate(1000,62,shift)
        print('SHIFT',shift,'future-label-match',np.mean(ye==np.arange(len(ye))%2))
        for kind in ('global','triples','unordered','triples_plus_position','full'):
            a=features(train,kind); b=features(test,kind)
            model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000))
            model.fit(a,yt)
            print(kind,a.shape[1],round(accuracy_score(ye,model.predict(b)),4))
