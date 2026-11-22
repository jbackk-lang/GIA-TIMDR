import gzip,json,random
N=32768;SEG=512;LAGS=(1,3,64)
def dataset():
 r=random.Random(5412);out=bytearray();boundaries=[];targets=[]
 for seg in range(N//SEG):
  lag=LAGS[seg%3];boundaries.append(len(out));targets.append(seg%3)
  for j in range(SEG):
   i=len(out)
   x=r.randrange(256) if j<lag or r.randrange(100)>=98 else out[i-lag]
   out.append(x)
 return bytes(out),boundaries,targets
def process(data,mode,decode=False,trace=False):
 h=bytearray();out=bytearray();ew=[0]*3;recent=[[0]*32 for _ in range(3)];sums=[0]*3;prev=0;choices=[]
 for i,v in enumerate(data):
  pred=[h[-lag] if i>=lag else 0 for lag in LAGS]
  if mode=='raw':k=None
  elif mode=='static':k=2
  elif mode=='adaptive':k=min(range(3),key=lambda j:(ew[j],j))
  elif mode=='fast':k=min(range(3),key=lambda j:(sums[j]+(6 if j!=prev else 0),j))
  else:raise ValueError(mode)
  p=pred[k] if k is not None else 0
  x=(v+p)%256 if decode else v
  out.append(x if decode else (x-p)%256)
  for j in range(3):
   d=(x-pred[j])%256;d=min(d,256-d)
   ew[j]=ew[j]*15//16+d
   idx=i%32;sums[j]+=d-recent[j][idx];recent[j][idx]=d
  h.append(x)
  if k is not None:prev=k
  if trace:choices.append(k)
 return (bytes(out),choices) if trace else bytes(out)
def run():
 data,boundaries,targets=dataset();results={}
 for mode in ('raw','static','adaptive','fast'):
  residual,choices=process(data,mode,trace=True)
  assert process(residual,mode,decode=True)==data
  delays=[];correct=[]
  if mode in ('adaptive','fast'):
   for start,target in zip(boundaries[1:],targets[1:]):
    window=choices[start:start+SEG]
    delays.append(next((j for j in range(len(window)-7) if all(k==target for k in window[j:j+8])),None))
    correct.append(sum(k==target for k in window)/len(window))
  results[mode]={'compressed_bytes':len(gzip.compress(residual,compresslevel=9,mtime=0)),'switches':sum(a!=b for a,b in zip(choices,choices[1:])), 'detection_delays':delays,'mean_accuracy_after_boundary':sum(correct)/len(correct) if correct else None}
 return {'input_bytes':len(data),'segment_bytes':SEG,'lags':LAGS,'results':results}
if __name__=='__main__':print(json.dumps(run(),indent=2))
