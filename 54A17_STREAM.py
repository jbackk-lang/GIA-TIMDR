import argparse, os, struct, zlib, gzip, time, json, hashlib, tempfile, tracemalloc
from pathlib import Path
MAGIC=b'GIA17\x01\x00\x00'; HDR=struct.Struct('<8sIQ'); CH=struct.Struct('<II'); RECORD=11

def shuffle(b):
    return b''.join(b[i::RECORD] for i in range(RECORD))
def unshuffle(b):
    n=len(b)//RECORD; out=bytearray(len(b))
    for i in range(RECORD):out[i::RECORD]=b[i*n:(i+1)*n]
    return out

def encode(src,dst,block_records=65536):
    length=os.path.getsize(src)
    if length%RECORD:raise ValueError('input length not divisible by 11')
    with open(src,'rb') as f,open(dst,'wb') as o:
        o.write(HDR.pack(MAGIC,block_records,length))
        while True:
            b=f.read(block_records*RECORD)
            if not b:break
            c=zlib.compress(shuffle(b),1)
            o.write(CH.pack(len(b),len(c)));o.write(c)

def decode(src,dst):
    with open(src,'rb') as f,open(dst,'wb') as o:
        header=f.read(HDR.size)
        if len(header)!=HDR.size:raise ValueError('truncated header')
        magic,block_records,total=HDR.unpack(header)
        if magic!=MAGIC or not block_records or total%RECORD:raise ValueError('invalid header')
        written=0
        while written<total:
            h=f.read(CH.size)
            if len(h)!=CH.size:raise ValueError('truncated block header')
            raw_n,comp_n=CH.unpack(h)
            if not 0<raw_n<=block_records*RECORD or raw_n%RECORD or comp_n>raw_n+1024:raise ValueError('invalid block size')
            payload=f.read(comp_n)
            if len(payload)!=comp_n:raise ValueError('truncated payload')
            dec=zlib.decompressobj();b=dec.decompress(payload,raw_n+1)
            if not dec.eof or dec.unused_data or dec.unconsumed_tail or len(b)!=raw_n:raise ValueError('invalid payload')
            o.write(unshuffle(b));written+=raw_n
        if written!=total or f.read(1):raise ValueError('length or trailing bytes')

def generate(path,records,kind):
    pack=struct.Struct('<IhhhB').pack
    with open(path,'wb') as f:
        buf=bytearray();x=y=z=0
        for i in range(records):
            if kind=='trajectory':
                x+=1 if i%128<64 else -1;y+=1 if i%256<128 else -1;z+=1 if i%512<256 else -1;e=(i//64)%256
            elif kind=='regime':
                s=(i//8192)%3;x+=1 if s==0 else -1 if s==1 else 0;y+=1 if s==1 else -1 if s==2 else 0;z+=1 if s==2 else -1 if s==0 else 0
                if max(abs(x),abs(y),abs(z))>30000:x=y=z=0
                e=(i//32+s*37)%256
            else:
                import random
                if i==0:rng=random.Random(5417)
                x=rng.randrange(-30000,30000);y=rng.randrange(-30000,30000);z=rng.randrange(-30000,30000);e=rng.randrange(256)
            buf.extend(pack(i,x,y,z,e))
            if len(buf)>=1024*1024:f.write(buf);buf.clear()
        f.write(buf)

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def gzip_file(src,dst):
    with open(src,'rb') as f,open(dst,'wb') as o:
        with gzip.GzipFile(fileobj=o,mode='wb',compresslevel=1,mtime=0) as g:
            for b in iter(lambda:f.read(1024*1024),b''):g.write(b)

def run(records,block_records):
    rows=[]
    with tempfile.TemporaryDirectory() as d:
        for kind in ('trajectory','regime','random'):
            src=f'{d}/in';encoded=f'{d}/encoded';restored=f'{d}/restored';gz=f'{d}/gzip'
            generate(src,records,kind); size=os.path.getsize(src)
            t=time.perf_counter();gzip_file(src,gz);gt=time.perf_counter()-t
            tracemalloc.start();t=time.perf_counter();encode(src,encoded,block_records);ct=time.perf_counter()-t;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            t=time.perf_counter();decode(encoded,restored);dt=time.perf_counter()-t
            assert sha(src)==sha(restored)
            rows.append({'dataset':kind,'input_bytes':size,'gzip1_bytes':os.path.getsize(gz),'stream_bytes':os.path.getsize(encoded),'gzip1_seconds':round(gt,4),'stream_compress_seconds':round(ct,4),'stream_decompress_seconds':round(dt,4),'gzip1_MiBs':round(size/1048576/gt,2),'stream_MiBs':round(size/1048576/ct,2),'stream_decode_MiBs':round(size/1048576/dt,2),'peak_tracemalloc_bytes':peak,'sha256_equal':True})
    return {'records':records,'block_records':block_records,'format':'GIA17 v1, 20 byte header, 8 byte per-block header','rows':rows}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--records',type=int,default=1048576);p.add_argument('--block-records',type=int,default=65536);p.add_argument('--output');a=p.parse_args()
    result=run(a.records,a.block_records);s=json.dumps(result,indent=2);print(s)
    if a.output:Path(a.output).write_text(s+'\n')
