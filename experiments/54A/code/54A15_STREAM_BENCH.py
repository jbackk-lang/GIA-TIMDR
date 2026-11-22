#!/usr/bin/env python3
"""54A.15: streaming time/space transform, full-file roundtrip and throughput."""
import argparse, gzip, json, random, struct, time, zlib
from pathlib import Path

MAGIC=b'G15S'
RECORD=struct.Struct('<IhhhB') # time, x,y,z, energy = 11 bytes
BLOCK=4096 # records
def generate(n,kind):
    rng=random.Random(5415); out=bytearray()
    x=y=z=0
    for i in range(n):
        if kind=='trajectory':
            x+=1 if i%128<64 else -1
            y+=1 if i%256<128 else -1
            z+=1 if i%512<256 else -1
            e=(i//64)%256
        elif kind=='regime':
            s=(i//8192)%3
            x+= (1 if s==0 else -1 if s==1 else 0)
            y+= (1 if s==1 else -1 if s==2 else 0)
            z+= (1 if s==2 else -1 if s==0 else 0)
            if max(abs(x),abs(y),abs(z))>30000:x=y=z=0
            e=(i//32+s*37)%256
        else:
            x=rng.randrange(-30000,30000);y=rng.randrange(-30000,30000);z=rng.randrange(-30000,30000);e=rng.randrange(256)
        out+=RECORD.pack(i,x,y,z,e)
    return bytes(out)
def delta_encode(chunk):
    out=bytearray();prev=[0]*5
    for t,x,y,z,e in RECORD.iter_unpack(chunk):
        vals=[t,x,y,z,e]
        for j,v in enumerate(vals):
            if j==0:out+=struct.pack('<I',(v-prev[j])&0xffffffff)
            elif j==4:out.append((v-prev[j])&255)
            else:out+=struct.pack('<H',(v-prev[j])&65535)
            prev[j]=v
    return bytes(out)
def delta_decode(chunk):
    out=bytearray();prev=[0]*5
    for i in range(0,len(chunk),11):
        d=[struct.unpack_from('<I',chunk,i)[0]]+[struct.unpack_from('<H',chunk,i+j)[0] for j in (4,6,8)]+[chunk[i+10]]
        vals=[(prev[0]+d[0])&0xffffffff]
        for j in (1,2,3):
            u=(prev[j]+d[j])&65535
            vals.append(u-65536 if u>=32768 else u)
        vals.append((prev[4]+d[4])&255)
        out+=RECORD.pack(*vals);prev=vals
    return bytes(out)
def compress_stream(data, transform=False, level=1):
    out=bytearray(MAGIC+bytes([int(transform),level])+struct.pack('<I',len(data)//11))
    for start in range(0,len(data),BLOCK*11):
        raw=data[start:start+BLOCK*11]
        payload=zlib.compress(delta_encode(raw) if transform else raw,level)
        out+=struct.pack('<I',len(payload))+payload
    return bytes(out)
def decompress_stream(blob):
    assert blob[:4]==MAGIC
    transform,level=blob[4:6];count=struct.unpack_from('<I',blob,6)[0]
    out=bytearray();p=10
    while p<len(blob):
        size=struct.unpack_from('<I',blob,p)[0];p+=4
        chunk=zlib.decompress(blob[p:p+size]);p+=size
        out+=delta_decode(chunk) if transform else chunk
    assert len(out)==count*11
    return bytes(out)
def bench(data, fn, repeats):
    sizes=[];durations=[];encoded=None
    for _ in range(repeats):
        start=time.perf_counter();encoded=fn(data);durations.append(time.perf_counter()-start);sizes.append(len(encoded))
    assert len(set(sizes))==1
    return encoded, sorted(durations)[len(durations)//2]
def run(n,repeats):
    rows=[]
    for kind in ('trajectory','regime','random'):
        data=generate(n,kind)
        for method,fn,decode in [
            ('gzip_1',lambda d:gzip.compress(d,compresslevel=1,mtime=0),gzip.decompress),
            ('gzip_6',lambda d:gzip.compress(d,compresslevel=6,mtime=0),gzip.decompress),
            ('zlib_blocks_1',lambda d:compress_stream(d,False,1),decompress_stream),
            ('delta_zlib_blocks_1',lambda d:compress_stream(d,True,1),decompress_stream)]:
            blob,sec=bench(data,fn,repeats)
            st=time.perf_counter();restored=decode(blob);decsec=time.perf_counter()-st
            assert restored==data,(kind,method)
            rows.append(dict(dataset=kind,method=method,input_bytes=len(data),compressed_bytes=len(blob),ratio=round(len(blob)/len(data),6),compress_seconds=round(sec,6),compress_MiB_s=round(len(data)/1048576/sec,2),decompress_seconds=round(decsec,6),roundtrip=True))
    return {'records':n,'repeats':repeats,'block_records':BLOCK,'method':'median compression time, one decompression time; no external dependencies','rows':rows}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--records',type=int,default=262144);ap.add_argument('--repeats',type=int,default=3);ap.add_argument('--output');a=ap.parse_args()
    result=run(a.records,a.repeats)
    text=json.dumps(result,indent=2)
    if a.output:Path(a.output).write_text(text)
    print(text)
