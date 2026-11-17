import gzip,random,json
from pathlib import Path
N=131072; B=256
rng=random.Random(5405)
def datasets():
 r=random.Random(11)
 yield 'random',bytes(r.randrange(256) for _ in range(N))
 base=bytes((i*13+i//7)%256 for i in range(B))
 yield 'repeated', (base*(N//B+1))[:N]
 out=bytearray(); prev=bytearray(base)
 for t in range((N+B-1)//B):
  if t%7==0: prev[(t*17)%B]=(prev[(t*17)%B]+1)%256
  out.extend(prev)
 yield 'slow_changes',bytes(out[:N])
 out=bytearray()
 for i in range(N):
  t=i//3; ch=i%3; v=(t*7+t//17)%256
  out.append((v+(0 if ch==0 else 3 if ch==1 else 6)+ (r.randrange(3)==0))%256)
 yield 'three_correlated',bytes(out)

def encode(data,mode):
 # all predictors causal and fully decoder-synchronizable; choose by past residual score only
 history=bytearray(); residual=bytearray(); scores=[0,0,0]
 for i,x in enumerate(data):
  cand=[history[-1] if len(history)>=1 else 0,history[-3] if len(history)>=3 else 0,history[-B] if len(history)>=B else 0]
  if mode=='static': p=cand[2]
  elif mode=='adaptive': p=cand[min(range(3),key=lambda k:(scores[k],k))]
  elif mode=='tri_loop':
   # channel phase changes which of 3 candidate forecasts is preferred on tied scores
   k=min(range(3),key=lambda k:(scores[k],(k-i%3)%3));p=cand[k]
  else: p=0
  residual.append((x-p)%256)
  # rolling scores based on observed prediction error; integer deterministic decay
  for k in range(3):
   e=(x-cand[k])%256; e=min(e,256-e)
   scores[k]=(scores[k]*15)//16+e
  history.append(x)
 return bytes(residual)

def decode(res,mode):
 history=bytearray();scores=[0,0,0]
 for i,d in enumerate(res):
  cand=[history[-1] if len(history)>=1 else 0,history[-3] if len(history)>=3 else 0,history[-B] if len(history)>=B else 0]
  if mode=='static':p=cand[2]
  elif mode=='adaptive':p=cand[min(range(3),key=lambda k:(scores[k],k))]
  elif mode=='tri_loop':p=cand[min(range(3),key=lambda k:(scores[k],(k-i%3)%3))]
  else:p=0
  x=(d+p)%256
  for k in range(3):
   e=(x-cand[k])%256;e=min(e,256-e)
   scores[k]=(scores[k]*15)//16+e
  history.append(x)
 return bytes(history)

rows=[]
for name,data in datasets():
 row={'dataset':name,'raw':len(data)}
 for mode in ['raw','static','adaptive','tri_loop']:
  encoded=encode(data,mode)
  assert decode(encoded,mode)==data
  row[mode]=len(gzip.compress(encoded,compresslevel=9,mtime=0))
 rows.append(row)
print(json.dumps(rows,indent=2))
Path('/mnt/data/54A5_RESULTS.json').write_text(json.dumps({'method':'Causal byte predictors; gzip level 9; no side information; prototype tri_loop is phase-aware tie-breaking, NOT original TIMDR J(Lambda)','results':rows},indent=2))
