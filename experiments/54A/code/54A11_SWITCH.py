import gzip,json,random
N=32768; LAGS=(1,3,64)
def sets():
 r=random.Random(5411)
 yield 'random',bytes(r.randrange(256) for _ in range(N))
 yield 'periodic',bytes((i%3*43+(i//3)%64)%256 for i in range(N))
 yield 'regime_512',bytes(((i//512)%2*73+(i//3 if (i//512)%2 else i//64))%256 for i in range(N))
 yield 'regime_128',bytes(((i//128)%2*73+(i//3 if (i//128)%2 else i//64))%256 for i in range(N))
 yield 'mixed',bytes(((i//1024)*7+(i%3)*11+(i//64)%5)%256 for i in range(N))
def process(data,mode,decode=False,track=False):
 hist=bytearray();out=bytearray();scores=[0]*3;recent=[[0]*16 for _ in range(3)];sums=[0]*3;prev=0;switches=0;choices=[]
 for i,v in enumerate(data):
  preds=[hist[-lag] if i>=lag else 0 for lag in LAGS]
  if mode=='raw':k=None
  elif mode=='static':k=2
  elif mode=='adaptive':k=min(range(3),key=lambda j:(scores[j],j))
  elif mode=='switch':k=min(range(3),key=lambda j:(sums[j]+(8 if j!=prev else 0),j))
  else:raise ValueError(mode)
  if k is not None:
   if i and k!=prev:switches+=1
   prev=k
  p=preds[k] if k is not None else 0
  x=(v+p)%256 if decode else v
  out.append(x if decode else (x-p)%256)
  for j in range(3):
   d=(x-preds[j])%256;d=min(d,256-d)
   scores[j]=scores[j]*15//16+d
   idx=i%16;sums[j]+=d-recent[j][idx];recent[j][idx]=d
  hist.append(x)
  if track:choices.append(k)
 return (bytes(out),switches,choices) if track else bytes(out)
def main():
 rows=[]
 for name,data in sets():
  row={'dataset':name,'input_bytes':len(data)}
  for mode in ('raw','static','adaptive','switch'):
   transformed,sw,choices=process(data,mode,track=True)
   assert process(transformed,mode,decode=True)==data
   row[mode+'_bytes']=len(gzip.compress(transformed,compresslevel=9,mtime=0))
   row[mode+'_switches']=sw
  rows.append(row)
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
