"""Temporal information beyond FFT magnitude: exact-spectrum phase surrogates."""
import argparse,json
from pathlib import Path
import numpy as np

def generate(seed,n=8192):
    rng=np.random.default_rng(seed)
    pulses=(rng.random(n)<.015)*rng.lognormal(0,.45,n)
    k=np.exp(-np.arange(70)/11)*(1-np.exp(-np.arange(70)/3))
    x=np.convolve(pulses,k,'full')[:n]+rng.normal(0,.045,n)
    return (x-x.mean())/x.std()

def surrogate(x,rng):
    f=np.fft.rfft(x)
    p=rng.uniform(-np.pi,np.pi,len(f))
    p[0]=np.angle(f[0]);p[-1]=np.angle(f[-1])
    return np.fft.irfft(abs(f)*np.exp(1j*p),n=len(x))

def h(counts):
    p=np.asarray(counts,float);p=p[p>0]/p.sum()
    return float(-np.sum(p*np.log2(p)))

def metrics(x,lag=8):
    z=np.digitize(x,np.quantile(x,[1/3,2/3]))
    a,b,c=z[:-2*lag],z[lag:-lag],z[2*lag:]
    mi=h(np.bincount(a,minlength=3))+h(np.bincount(c,minlength=3))-h(np.bincount(3*a+c,minlength=9))
    cmi=h(np.bincount(3*a+b,minlength=9))+h(np.bincount(3*b+c,minlength=9))-h(np.bincount(b,minlength=3))-h(np.bincount(9*a+3*b+c,minlength=27))
    d=np.diff(x)
    asym=float(np.mean(d**3)/(np.mean(d*d)**1.5+1e-12))
    return {'predictive_mi_bits':mi,'conditional_memory_bits':cmi,'increment_asymmetry':asym}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--replicates',type=int,default=24)
    p.add_argument('--surrogates',type=int,default=79)
    p.add_argument('--output',type=Path,default=Path('information_probe.json'))
    args=p.parse_args()
    rng=np.random.default_rng(773);rows=[]
    for rep in range(args.replicates):
        x=generate(1000+rep);actual=metrics(x)
        null=[metrics(surrogate(x,rng)) for _ in range(args.surrogates)]
        err=float(np.max(abs(abs(np.fft.rfft(x))-abs(np.fft.rfft(surrogate(x,rng))))))
        row={'replicate':rep,'actual':actual,'null_mean':{},'p_two_sided':{},'max_fft_magnitude_error':err}
        for key in actual:
            vals=np.array([z[key] for z in null]);center=np.median(vals)
            row['null_mean'][key]=float(vals.mean())
            row['p_two_sided'][key]=float((1+sum(abs(vals-center)>=abs(actual[key]-center)))/(len(vals)+1))
        rows.append(row)
    summary={key:{'actual_mean':float(np.mean([r['actual'][key] for r in rows])),
                  'null_mean':float(np.mean([r['null_mean'][key] for r in rows])),
                  'replicates_p_le_0_05':sum(r['p_two_sided'][key]<=.05 for r in rows)}
             for key in rows[0]['actual']}
    report={'source':'synthetic_shot_noise','replicates':args.replicates,
            'surrogates_per_replicate':args.surrogates,'summary':summary,
            'max_fft_magnitude_error':max(r['max_fft_magnitude_error'] for r in rows),
            'results':rows,'caveats':['Synthetic known pulse process, no novel physical discovery.',
            'Surrogates preserve FFT magnitude and linear autocorrelation but not sample amplitude distribution.',
            'Quantized predictive mutual information is not encoded message content or channel capacity.',
            'Fixed lag and exploratory multiple metrics; no multiple-testing correction.',
            'This is a control experiment, not yet a CHF helix/bridge validation.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
if __name__=='__main__':main()
