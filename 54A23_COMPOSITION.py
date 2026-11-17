"""54A.23: Composition of three-node predictors. Reproducible algebra and compression ablation."""
import json,random,struct,zlib,statistics
def compose(a,b):
 # affine predictor f(x)=a0*x+a1; f_a after f_b
 return (a[0]*b[0],a[0]*b[1]+a[1])
def apply(f,x):return f[0]*x+f[1]
def algebra():
 r=random.Random(5423)
 for _ in range(1000):
  a,b,c=[(r.randrange(-3,4),r.randrange(-5,6)) for i in range(3)]
  x=r.randrange(-20,21)
  assert compose(compose(a,b),c)==compose(a,compose(b,c))
  assert apply(compose(a,b),x)==apply(a,apply(b,x))
 return True
def pack_residuals(data,model):
 out=bytearray()
 for i,v in enumerate(data):
  if model=='raw':p=0
  elif model=='lag1':p=data[i-1] if i else 0
  elif model=='lag2':p=2*data[i-1]-data[i-2] if i>=2 else (data[i-1] if i else 0)
  else:
   # three-node composition: A=lag1, B=lag2, C=lag1 of B error.
   # equivalent to third difference: 3*x_(i-1)-3*x_(i-2)+x_(i-3)
   p=3*data[i-1]-3*data[i-2]+data[i-3] if i>=3 else (2*data[i-1]-data[i-2] if i>=2 else (data[i-1] if i else 0))
  out+=struct.pack('<H',(v-p)&65535)
 return bytes(out)
def run(n=65536):
 assert algebra()
 rng=random.Random(5423);results=[]
 for name in ('linear','quadratic','piecewise','random'):
  values=[]
  for i in range(n):
   if name=='linear':v=i//4
   elif name=='quadratic':v=(i//64)**2
   elif name=='piecewise':v=(i//1024)*700+(i%1024)//4 if i%2048<1024 else (i//1024)*700-(i%1024)//4
   else:v=rng.randrange(65536)
   values.append(v&65535)
  for method in ('raw','lag1','lag2','composed3'):
   b=pack_residuals(values,method)
   compressed=zlib.compress(b,1)
   # independent decoder reconstructs sequentially
   restored=[]
   for i in range(0,len(b),2):
    j=i//2;d=struct.unpack_from('<H',b,i)[0]
    if method=='raw':p=0
    elif method=='lag1':p=restored[-1] if j else 0
    elif method=='lag2':p=2*restored[-1]-restored[-2] if j>=2 else (restored[-1] if j else 0)
    else:p=3*restored[-1]-3*restored[-2]+restored[-3] if j>=3 else (2*restored[-1]-restored[-2] if j>=2 else (restored[-1] if j else 0))
    restored.append((p+d)&65535)
   assert restored==values
   results.append({'dataset':name,'method':method,'bytes':len(compressed),'ratio':round(len(compressed)/(n*2),6),'roundtrip':True})
 return {'experiment':'54A.23','records':n,'algebra_associative':True,'composition':'third finite difference is a composed 3-stage linear predictor; NOT a proven TIMDR trinode','rows':results}
if __name__=='__main__':
 result=run();print(json.dumps(result,indent=2))
