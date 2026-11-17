"""53E.2 — energy balance of hypothetical storage vs reuse of computed memory.
Assumed Joule values are NOT empirical measurements.
"""
import json
from pathlib import Path

def storage(n, input_j=1.0, eta_charge=.8, leak=.01, eta_discharge=.7):
    stored=0.; heat=0.; history=[]
    for _ in range(n):
        leakage=leak*stored
        heat+=leakage+(1-eta_charge)*input_j
        stored=stored-leakage+eta_charge*input_j
        history.append(stored)
    work=eta_discharge*stored
    heat+=(1-eta_discharge)*stored
    return {'cycles':n,'input_j':n*input_j,'stored_before_discharge_j':stored,
            'recoverable_work_j':work,'heat_total_j':heat,
            'balance_error_j':n*input_j-work-heat,'history_j':history}

def computation(reuses,compute_j=.01,read_j=.0002,write_j=.003,retain_j_per_step=.00001):
    baseline=reuses*compute_j
    cached=compute_j+write_j+(reuses-1)*read_j+reuses*retain_j_per_step
    return {'uses':reuses,'baseline_j':baseline,'cached_j':cached,
            'saved_j':baseline-cached,'saving_fraction':(baseline-cached)/baseline}

def main():
    s=[storage(n) for n in (1,5,10,50,100)]
    c=[computation(n) for n in (1,2,5,10,50,100)]
    assert all(abs(x['balance_error_j'])<1e-10 for x in s)
    assert c[0]['saved_j']<0 and c[-1]['saved_j']>0
    return {'status':'ENERGY_BALANCE_PASS','storage':s,'computation':c,
            'assumptions':'Illustrative Joule-denominated parameters, not measured hardware or validated physical medium. Memory storage and computational reuse are separate systems.',
            'conclusion':'Stored energy and saved computation are not interchangeable; energy conservation alone does not prove storage capacity or recoverability.'}

if __name__=='__main__':
    result=main()
    Path(__file__).with_name('53E2_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
