import gzip,json,random
N=32768
def data_sets():
 r=random.Random(5410)
 yield 'random',bytes(r.randrange(256) for _ in range(N))
 yield 'periodic',bytes((i%3*43+(i//3)%64)%256 for i in range(N))
 yield 'drift',bytes(((i//256)*3+(i%256)//4)%256 for i in range(N))
 yield 'regime',bytes(((i//512)%2*73+(i//3 if (i//512)%2 else i//64))%256 for i in range(N))
 yield 'mixed',bytes(((i//1024)*7+(i%3)*11+(i//64)%5)%256 for i in range(N))
def process(data,mode,decode=False):
 hist=bytearray();out=bytearray();scores=[0,0,0];errors=[[],[],[]]
 for i,v in enumerate(data):
  pred=[hist[-1] if i else 0,hist[-3] if i>=3 else 0,hist[-64] if i>=64 else 0]
  if mode=='raw':k=None
  elif mode=='static':k=2
  elif mode=='adaptive':k=min(range(3),key=lambda j:(scores[j],j))
  elif mode=='multiscale':
   metrics=[sum(errors[j][-16:])*4+sum(errors[j][-64:])+sum(errors[j][-256:])//4 for j in range(3)]
   k=min(range(3),key=lambda j:(metrics[j],j))
  else:raise ValueError(mode)
  p=0 if k is None else pred[k]
  x=(v+p)%256 if decode else v
  out.append(x if decode else (x-p)%256)
  for j in range(3):
   d=(x-pred[j])%256;d=min(d,256-d)
   scores[j]=scores[j]*15//16+d
   errors[j].append(d)
  hist.append(x)
 return bytes(out)
def run():
 results=[]
 for name,data in data_sets():
  row={'dataset':name,'input_bytes':len(data)}
  for mode in ('raw','static','adaptive','multiscale'):
   transformed=process(data,mode)
   assert process(transformed,mode,True)==data
   row[mode]=len(gzip.compress(transformed,compresslevel=9,mtime=0))
  results.append(row)
 return results
if __name__=='__main__':
 print(json.dumps(run(),indent=2))
