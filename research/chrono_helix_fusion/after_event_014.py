"""After-event exploratory test. Requires CWRU_CHF.zip and scipy/numpy.
Source dataset must be supplied separately; no data bundled.
"""
import io,zipfile,json,argparse
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import hilbert

def run(source,seed=20261119,permutations=2000):
 rng=np.random.default_rng(seed); rows=[]
 with zipfile.ZipFile(source) as z:
  for name in sorted(z.namelist()):
   mat=loadmat(io.BytesIO(z.read(name)))
   x=np.asarray(mat[next(k for k in mat if k.endswith('_DE_time'))]).ravel().astype(float)
   w=x[:50*2048].reshape(50,2048)
   rms=np.sqrt(np.mean(w*w,axis=1))
   crest=np.max(abs(w),axis=1)/(rms+1e-12)
   rec=[]
   for a in w:
    env=abs(hilbert(a));env-=env.mean();den=np.dot(env,env)+1e-12
    rec.append(max(np.dot(env[:-lag],env[lag:])/den for lag in range(30,401)))
   rec=np.array(rec)
   event=np.zeros(49,dtype=bool);event[np.argsort(crest[:49])[-5:]]=True
   for label,y in [('recurrence',rec[1:]),('rms',rms[1:])]:
    v=(y-y.mean())/(y.std()+1e-12)
    obs=float(v[event].mean()-v[~event].mean())
    null=[]
    for _ in range(permutations):
     ev=np.roll(event,int(rng.integers(1,49)))
     null.append(float(v[ev].mean()-v[~ev].mean()))
    rows.append({'file':name,'outcome':label,'effect_sd':obs,'null_effects':null,
                 'event_windows':np.flatnonzero(event).tolist()})
 results={}
 for label in ('recurrence','rms'):
  data=[r for r in rows if r['outcome']==label]
  obs=float(np.mean([r['effect_sd'] for r in data]))
  null=np.mean(np.array([r['null_effects'] for r in data]),axis=0)
  results[label]={'mean_effect_sd':obs,
    'two_sided_shift_p':float((1+np.sum(abs(null)>=abs(obs)))/(len(null)+1)),
    'null_95_interval':np.quantile(null,[.025,.975]).tolist(),
    'positive_recordings':int(sum(r['effect_sd']>0 for r in data)),
    'per_file_effects':{r['file']:r['effect_sd'] for r in data}}
 return {'seed':seed,'permutations':permutations,'results':results,
         'limitations':['Exploratory post-selected hypothesis','No causal inference',
                        'No CHF/helix features','Circular shift null imperfect for nonstationary data',
                        'Two outcomes examined without multiplicity adjustment']}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('zip_file');parser.add_argument('--output',default='CHF_AFTER_EVENT_014.json')
 args=parser.parse_args()
 report=run(args.zip_file)
 Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report['results'],indent=2))
