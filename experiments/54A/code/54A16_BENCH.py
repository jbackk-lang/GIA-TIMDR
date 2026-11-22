import argparse,gzip,json,random,struct,time,zlib,statistics
R=struct.Struct('<IhhhB')
def make(n,kind):
 rng=random.Random(5416);out=bytearray();x=y=z=0
 for i in range(n):
  if kind=='trajectory':
   x+=1 if i%128<64 else -1;y+=1 if i%256<128 else -1;z+=1 if i%512<256 else -1;e=(i//64)%256
  elif kind=='regime':
   s=(i//8192)%3;x+=(1 if s==0 else -1 if s==1 else 0);y+=(1 if s==1 else -1 if s==2 else 0);z+=(1 if s==2 else -1 if s==0 else 0);e=(i//32+s*37)%256
   if max(abs(x),abs(y),abs(z))>30000:x=y=z=0
  else:x=rng.randrange(-30000,30000);y=rng.randrange(-30000,30000);z=rng.randrange(-30000,30000);e=rng.randrange(256)
  out.extend(R.pack(i,x,y,z,e))
 return bytes(out)
def shuffle(b):
 n=len(b)//11;return b''.join(b[j::11] for j in range(11))
def unshuffle(b):
 n=len(b)//11;out=bytearray(len(b))
 for j in range(11):out[j::11]=b[j*n:(j+1)*n]
 return bytes(out)
def delta(b):
 out=bytearray();p=[0]*5
 for vals in R.iter_unpack(b):
  t,x,y,z,e=vals;out.extend(struct.pack('<IHHHB',(t-p[0])&0xffffffff,(x-p[1])&65535,(y-p[2])&65535,(z-p[3])&65535,(e-p[4])&255));p=list(vals)
 return bytes(out)
def undelta(b):
 out=bytearray();p=[0]*5
 for dt,dx,dy,dz,de in R.iter_unpack(b):
  t=(p[0]+dt)&0xffffffff;vs=[(p[k]+d)&65535 for k,d in enumerate((dx,dy,dz),1)];vs=[v-65536 if v>=32768 else v for v in vs];e=(p[4]+de)&255
  vals=(t,*vs,e);out.extend(R.pack(*vals));p=list(vals)
 return bytes(out)
def comp(raw,method):
 if method=='gzip1':return gzip.compress(raw,compresslevel=1,mtime=0)
 if method=='gzip6':return gzip.compress(raw,compresslevel=6,mtime=0)
 if method=='shuffle_z1':return zlib.compress(shuffle(raw),1)
 if method=='shuffle_z6':return zlib.compress(shuffle(raw),6)
 if method=='delta_z1':return zlib.compress(delta(raw),1)
 if method=='delta_shuffle_z1':return zlib.compress(shuffle(delta(raw)),1)
 if method=='delta_shuffle_z6':return zlib.compress(shuffle(delta(raw)),6)
 raise ValueError(method)
def decomp(blob,method):
 if method.startswith('gzip'):return gzip.decompress(blob)
 b=zlib.decompress(blob)
 if 'shuffle' in method:b=unshuffle(b)
 if 'delta' in method:b=undelta(b)
 return b
def bench(n,reps):
 rows=[]
 for kind in ('trajectory','regime','random'):
  raw=make(n,kind)
  for method in ('gzip1','gzip6','shuffle_z1','shuffle_z6','delta_z1','delta_shuffle_z1','delta_shuffle_z6'):
   ts=[];ds=[]
   for _ in range(reps):
    t=time.perf_counter();blob=comp(raw,method);ts.append(time.perf_counter()-t)
    t=time.perf_counter();check=decomp(blob,method);ds.append(time.perf_counter()-t)
    assert check==raw,(kind,method)
   c=statistics.median(ts);d=statistics.median(ds)
   rows.append(dict(dataset=kind,method=method,raw_bytes=len(raw),compressed_bytes=len(blob),ratio=round(len(blob)/len(raw),6),compress_seconds=round(c,6),compress_MiB_s=round(len(raw)/1048576/c,2),decompress_MiB_s=round(len(raw)/1048576/d,2),roundtrip=True))
 return dict(records=n,repeats=reps,python='stdlib',note='Synthetic records; median wall-clock; no file I/O; zlib and gzip headers differ',rows=rows)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--records',type=int,default=131072);p.add_argument('--repeats',type=int,default=3);p.add_argument('--output');a=p.parse_args();res=bench(a.records,a.repeats);s=json.dumps(res,indent=2);print(s)
 if a.output:open(a.output,'w').write(s+'\n')
