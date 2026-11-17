"""54A.19: causal block hybrid (shuffle+zlib1 vs raw LZ4). Python >=3.8, lz4."""
import argparse, hashlib, json, os, random, struct, tempfile, time, zlib, gzip, subprocess
from pathlib import Path
import lz4.frame
REC=struct.Struct('<IhhhB'); HDR=struct.Struct('<4sIIQ'); BH=struct.Struct('<BII')
BLOCK=32768
def source(path,kind,n):
 r=random.Random(5419);x=y=z=0
 with open(path,'wb') as f:
  buf=bytearray()
  for i in range(n):
   segment=i//BLOCK
   mode=kind if kind!='mixed' else ('trajectory','random','regime','random')[segment%4]
   if mode=='trajectory':
    x+=1 if i%128<64 else -1;y+=1 if i%256<128 else -1;z+=1 if i%512<256 else -1;e=(i//64+segment*7)%256
   elif mode=='regime':
    s=(i//8192)%3;x+=1 if s==0 else -1 if s==1 else 0;y+=1 if s==1 else -1 if s==2 else 0;z+=1 if s==2 else -1 if s==0 else 0
    if max(abs(x),abs(y),abs(z))>30000:x=y=z=0
    e=(i//32+s*37+segment*3)%256
   else:
    x=r.randrange(-30000,30000);y=r.randrange(-30000,30000);z=r.randrange(-30000,30000);e=r.randrange(256)
   buf.extend(REC.pack(i,x,y,z,e))
   if len(buf)>=1<<20:f.write(buf);buf.clear()
  f.write(buf)
def shuffle(b):return b''.join(b[j::11] for j in range(11))
def unshuffle(b):
 n=len(b)//11;out=bytearray(len(b))
 for j in range(11):out[j::11]=b[j*n:(j+1)*n]
 return bytes(out)
def encode(src,dst,mode='hybrid'):
 size=os.path.getsize(src)
 if size%11:raise ValueError('expected 11-byte records')
 counts=[0,0,0]
 with open(src,'rb') as f,open(dst,'wb') as o:
  o.write(HDR.pack(b'G19H',BLOCK,11,size))
  while True:
   b=f.read(BLOCK*11)
   if not b:break
   if mode=='gia':kind=1
   else:
    sample=b[:min(len(b),4096*11)]
    kind=1 if len(zlib.compress(shuffle(sample),1))<len(sample)*0.20 else 2
   payload=zlib.compress(shuffle(b),1) if kind==1 else lz4.frame.compress(b,compression_level=0,block_linked=False)
   counts[kind]+=1;o.write(BH.pack(kind,len(b),len(payload)));o.write(payload)
 return counts
def decode(src,dst):
 with open(src,'rb') as f,open(dst,'wb') as o:
  h=f.read(HDR.size)
  if len(h)!=HDR.size:raise ValueError('header')
  magic,block,rec,size=HDR.unpack(h)
  if magic!=b'G19H' or rec!=11 or not 0<block<=1048576 or size%11:raise ValueError('bad header')
  done=0
  while done<size:
   h=f.read(BH.size)
   if len(h)!=BH.size:raise ValueError('truncated')
   kind,rawlen,clen=BH.unpack(h)
   if not 0<rawlen<=min(block*11,size-done) or rawlen%11 or clen>rawlen+100000:raise ValueError('bad sizes')
   p=f.read(clen)
   if len(p)!=clen:raise ValueError('truncated payload')
   if kind==1:
    d=zlib.decompressobj();data=d.decompress(p,rawlen+1)
    if not d.eof or d.unused_data or d.unconsumed_tail:raise ValueError('bad zlib')
    b=unshuffle(data)
   elif kind==2:b=lz4.frame.decompress(p)
   else:raise ValueError('bad kind')
   if len(b)!=rawlen:raise ValueError('wrong block size')
   o.write(b);done+=len(b)
  if f.read(1):raise ValueError('trailing bytes')
def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def gzip_file(src,dst,reverse=False):
 with open(src,'rb') as f,open(dst,'wb') as o:
  if reverse:
   with gzip.GzipFile(fileobj=f,mode='rb') as g:
    for b in iter(lambda:g.read(1<<20),b''):o.write(b)
  else:
   with gzip.GzipFile(fileobj=o,mode='wb',compresslevel=1,mtime=0) as g:
    for b in iter(lambda:f.read(1<<20),b''):g.write(b)
def lz4_file(src,dst,reverse=False):
 with open(src,'rb') as f,open(dst,'wb') as o:
  if reverse:
   with lz4.frame.open(f,'rb') as d:
    for b in iter(lambda:d.read(1<<20),b''):o.write(b)
  else:
   with lz4.frame.open(o,'wb',compression_level=0) as c:
    for b in iter(lambda:f.read(1<<20),b''):c.write(b)
def zstd_file(src,dst,reverse=False):
 subprocess.run(['zstd','-q','-f','-T1','-1']+(['-d'] if reverse else [])+['-o',dst,src],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def benchmark(records=1048576):
 rows=[]
 with tempfile.TemporaryDirectory() as tmp:
  for kind in ('trajectory','regime','random','mixed'):
   src=f'{tmp}/src';dst=f'{tmp}/encoded';rest=f'{tmp}/decoded'
   source(src,kind,records);original=digest(src);size=os.path.getsize(src)
   methods=[('gzip1',gzip_file),('zstd1',zstd_file),('lz4',lz4_file),('gia_shuffle',lambda a,b,reverse=False:decode(a,b) if reverse else encode(a,b,'gia')),('hybrid',lambda a,b,reverse=False:decode(a,b) if reverse else encode(a,b,'hybrid'))]
   for name,fn in methods:
    start=time.perf_counter();counts=fn(src,dst);ct=time.perf_counter()-start;csize=os.path.getsize(dst)
    start=time.perf_counter();fn(dst,rest,True);dt=time.perf_counter()-start
    assert digest(rest)==original,(kind,name)
    rows.append(dict(dataset=kind,method=name,raw_bytes=size,compressed_bytes=csize,compression_seconds=round(ct,5),compression_MiBs=round(size/1048576/ct,2),decompression_MiBs=round(size/1048576/dt,2),block_method_counts=counts if name in ('gia_shuffle','hybrid') else None,sha256_equal=True))
    print(kind,name,csize,round(size/1048576/ct,2),flush=True)
 return dict(records=records,block_records=BLOCK,benchmark='single run, file IO, synthetic nonrepeated, no warmup',rows=rows)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--records',type=int,default=1048576);p.add_argument('--output',default='54A19_RESULTS.json');a=p.parse_args()
 result=benchmark(a.records);Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
