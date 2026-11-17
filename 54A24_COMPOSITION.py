import json,random,struct,zlib
def run(n=8192):
 rng=random.Random(5424);out=[]
 for kind in ('shared','independent','switching','random'):
  triples=[]
  for t in range(n):
   base=(t//4)%1000
   if kind=='shared':v=[base+j*10+(t%4) for j in range(3)]
   elif kind=='independent':v=[(t*(j+1)*(j+2)//7)%30000 for j in range(3)]
   elif kind=='switching':v=[base+j*10+(t%4) if t//256%2==0 else (t*(j+1)*(j+2)//7)%30000 for j in range(3)]
   else:v=[rng.randrange(30000) for j in range(3)]
   triples.append(v)
  raw=b''.join(struct.pack('<HHH',*v) for v in triples)
  # Independent nodes: per-node temporal delta.
  cols=[[v[j] for v in triples] for j in range(3)]
  def temporal(col):
   prev=0;buf=bytearray()
   for v in col:buf+=struct.pack('<H',(v-prev)&65535);prev=v
   return bytes(buf)
  independent=b''.join(temporal(c) for c in cols)
  # Hierarchical: node0 temporal; node1/2 encoded as spatial offsets from node0,
  # then temporal delta on offsets. No graph edge information assumed.
  hier=temporal(cols[0])+temporal([(b-a)&65535 for a,b in zip(cols[0],cols[1])])+temporal([(c-a)&65535 for a,c in zip(cols[0],cols[2])])
  # decode from transformed bytes, then compare all original values
  def undo(buf):
   v=[];p=0
   for (d,) in struct.iter_unpack('<H',buf):
    p=(p+d)&65535;v.append(p)
   return v
  a=undo(hier[:2*n]);d1=undo(hier[2*n:4*n]);d2=undo(hier[4*n:])
  assert all((a[i],(a[i]+d1[i])&65535,(a[i]+d2[i])&65535)==tuple(triples[i]) for i in range(n))
  # equal zlib wrapper, explicit 3-node topology known to both; schema cost omitted equally
  sizes={'raw':len(zlib.compress(raw,6)),'independent':len(zlib.compress(independent,6)),'hierarchical':len(zlib.compress(hier,6))}
  out.append({'dataset':kind,'compressed_bytes':sizes,'hierarchical_vs_independent_pct':round(100*(sizes['hierarchical']/sizes['independent']-1),2),'roundtrip':True})
 return {'experiment':'54A.24','n':n,'record_bytes':6,'compressor':'zlib level 6','assumptions':'three 16-bit nodes per timestamp, fixed known star topology, no metadata for topology; synthetic','rows':out}
if __name__=='__main__':print(json.dumps(run(),indent=2))
