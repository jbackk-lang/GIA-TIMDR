import argparse, json, random, struct, time, zlib
R=struct.Struct('<IhhhB')
def make(n,kind):
 r=random.Random(5420);o=bytearray();x=y=z=0
 for i in range(n):
  mode=kind if kind!='mixed' else ('stable' if (i//2048)%2==0 else 'random')
  if mode=='stable':
   x+=1 if i%64<32 else -1;y+=1 if i%128<64 else -1;z+=1 if i%256<128 else -1;e=(i//32)%256
  else:x=r.randrange(-30000,30000);y=r.randrange(-30000,30000);z=r.randrange(-30000,30000);e=r.randrange(256)
  o+=R.pack(i,x,y,z,e)
 return bytes(o)
def shuffle(b):return b''.join(b[j::11] for j in range(11))
def unshuffle(b):
 n=len(b)//11;o=bytearray(len(b))
 for j in range(11):o[j::11]=b[j*n:(j+1)*n]
 return bytes(o)
def next_size(block,prior,kind):
 if kind=='fixed':return prior
 # decisions use only previous completed block; two different causal features
 if kind=='variance':
  coords=[v[1] for v in R.iter_unpack(block)];score=sum(abs(b-a) for a,b in zip(coords,coords[1:]))/max(1,len(coords)-1)
  stable=score<5
 else:
  vals=list(R.iter_unpack(block));dx=[abs(vals[i][1]-vals[i-1][1]) for i in range(1,len(vals))];dy=[abs(vals[i][2]-vals[i-1][2]) for i in range(1,len(vals))];dz=[abs(vals[i][3]-vals[i-1][3]) for i in range(1,len(vals))]
  # completed-window proxy for local geometry alignment J, and temporal activity tau
  tau=sum(dx)+sum(dy)+sum(dz);J=sum(a>=b and a>=c for a,b,c in zip(dx,dy,dz))/max(1,len(dx));stable=tau/max(1,len(dx))<12 and J>=0.2
 return min(4096,prior*2) if stable else max(64,prior//2)
def encode(data,kind,initial=256):
 out=bytearray(b'G20A'+struct.pack('<I',len(data)));pos=0;blocksize=initial;counts={};chunks=[]
 while pos<len(data):
  b=data[pos:pos+blocksize*11];c=zlib.compress(shuffle(b),1);out+=struct.pack('<HI',len(b)//11,len(c))+c;counts[len(b)//11]=counts.get(len(b)//11,0)+1;chunks.append(len(b)//11);pos+=len(b)
  blocksize=next_size(b,blocksize,kind)
 return bytes(out),counts,chunks
def decode(blob):
 assert blob[:4]==b'G20A';total=struct.unpack_from('<I',blob,4)[0];pos=8;out=bytearray()
 while pos<len(blob):
  count,n=struct.unpack_from('<HI',blob,pos);pos+=6;c=blob[pos:pos+n];pos+=n
  d=zlib.decompress(c);assert len(d)==count*11;out+=unshuffle(d)
 assert len(out)==total
 return bytes(out)
def run(n):
 rows=[]
 for dataset in ('stable','mixed','random'):
  data=make(n,dataset)
  for method,initial in [('fixed64',64),('fixed256',256),('fixed1024',1024),('fixed4096',4096),('variance',256),('timdr_proxy',256)]:
   kind='fixed' if method.startswith('fixed') else method
   start=time.perf_counter();blob,counts,chunks=encode(data,kind,initial);elapsed=time.perf_counter()-start
   assert decode(blob)==data
   rows.append(dict(dataset=dataset,method=method,bytes=len(blob),ratio=round(len(blob)/len(data),5),MiB_s=round(len(data)/1048576/elapsed,2),blocks=len(chunks),block_histogram=counts,roundtrip=True))
 return {'records':n,'record_bytes':11,'description':'synthetic, deterministic, in-memory single run; completed-block causal adaptation; no full formal TIMDR state','rows':rows}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--records',type=int,default=32768);p.add_argument('--output',default='/mnt/data/54A20_RESULTS.json');a=p.parse_args();res=run(a.records);open(a.output,'w').write(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
