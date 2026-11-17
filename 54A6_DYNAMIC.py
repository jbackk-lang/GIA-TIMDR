import gzip,json,random
N=32768
def datasets():
 r=random.Random(546)
 yield 'random',bytes(r.randrange(256) for _ in range(N))
 yield 'periodic',bytes((i%3*43+(i//3)%64)%256 for i in range(N))
 yield 'drift',bytes(((i//256)*3+(i%256)//4)%256 for i in range(N))
 yield 'correlated',bytes(((i//3)*7+(i%3)*5+r.randrange(2))%256 for i in range(N))
def transform(src,mode,decode=False):
 hist=bytearray();out=bytearray();err=[0,0,0]
 for i,v in enumerate(src):
  p=[hist[-1] if len(hist)>0 else 0,hist[-3] if len(hist)>2 else 0,hist[-256] if len(hist)>255 else 0]
  if mode=='static':k=2
  elif mode=='adaptive':k=min(range(3),key=lambda j:(err[j],j))
  elif mode=='coupled':
   lam=2
   s=[err[1]-lam*err[2],-lam*err[0]+err[2],err[0]-lam*err[1]]
   k=min(range(3),key=lambda j:(err[j]+max(-1024,min(1024,s[j]))//8,j))
  else:k=0
  x=(v+p[k])%256 if decode else v
  out.append(x if decode else (x-p[k])%256)
  for j in range(3):
   d=(x-p[j])%256;d=min(d,256-d)
   err[j]=(15*err[j])//16+d
  hist.append(x)
 return bytes(out)
def main():
 rows=[]
 for name,src in datasets():
  row={'data':name,'input_bytes':len(src)}
  for mode in ('raw','static','adaptive','coupled'):
   enc=transform(src,mode)
   assert transform(enc,mode,True)==src
   row[mode]=len(gzip.compress(enc,compresslevel=9,mtime=0))
  rows.append(row)
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
