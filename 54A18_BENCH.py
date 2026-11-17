import os, sys, time, json, gzip, subprocess, tempfile, hashlib
from pathlib import Path
import lz4.frame
from importlib.machinery import SourceFileLoader
codec=SourceFileLoader('gia17','54A17_STREAM.py').load_module()
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def zstd(src,dst,decode=False):
 cmd=['zstd','-q','-f','-T1','-1']+(['-d'] if decode else [])+['-o',dst,src]
 subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def lz4_file(src,dst,decode=False):
 with open(src,'rb') as f,open(dst,'wb') as o:
  if decode:
   with lz4.frame.open(f,'rb') as d:
    for b in iter(lambda:d.read(1<<20),b''):o.write(b)
  else:
   with lz4.frame.open(o,'wb',compression_level=0) as c:
    for b in iter(lambda:f.read(1<<20),b''):c.write(b)
def gz(src,dst,decode=False):
 with open(src,'rb') as f,open(dst,'wb') as o:
  if decode:
   with gzip.GzipFile(fileobj=f,mode='rb') as g:
    for b in iter(lambda:g.read(1<<20),b''):o.write(b)
  else:
   with gzip.GzipFile(fileobj=o,mode='wb',compresslevel=1,mtime=0) as g:
    for b in iter(lambda:f.read(1<<20),b''):g.write(b)
def build_large(src,dst,repeat=10):
 with open(src,'rb') as f:seed=f.read()
 with open(dst,'wb') as f:
  for _ in range(repeat):f.write(seed)
def run():
 rows=[]
 with tempfile.TemporaryDirectory() as d:
  for kind in ('trajectory','regime','random'):
   seed=f'{d}/seed';inp=f'{d}/input';out=f'{d}/out';rest=f'{d}/rest'
   codec.generate(seed,1048576,kind)
   build_large(seed,inp,10)
   digest=sha(inp);size=os.path.getsize(inp)
   methods={'gzip1':gz,'zstd1':zstd,'lz4':lz4_file,'gia17':lambda a,b,decode=False:codec.decode(a,b) if decode else codec.encode(a,b)}
   for name,fn in methods.items():
    t=time.perf_counter();fn(inp,out);ct=time.perf_counter()-t
    packed=os.path.getsize(out)
    t=time.perf_counter();fn(out,rest,True);dt=time.perf_counter()-t
    assert sha(rest)==digest,(kind,name)
    rows.append({'dataset':kind,'method':name,'input_bytes':size,'compressed_bytes':packed,'compression_seconds':round(ct,4),'compression_MiBs':round(size/1048576/ct,2),'decompression_seconds':round(dt,4),'decompression_MiBs':round(size/1048576/dt,2),'sha256_equal':True})
    print(kind,name,packed,round(size/1048576/ct,2),flush=True)
 return {'data':'synthetic 11MiB seed repeated 10 times (110MiB); repeated patterns may inflate gains','environment':'local file I/O, one pass, no warmup, not randomized','rows':rows}
if __name__=='__main__':
 result=run();Path('54A18_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
