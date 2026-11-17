"""53E.3: coupled memory reuse and energy buffer, illustrative Joule accounting."""
import json
from pathlib import Path
COMPUTE=.01;WRITE=.003;READ=.0002;RETAIN=.00001
CHARGE_EFF=.8;DISCHARGE_EFF=.7;LEAK=.01
def scenario(uses,captured_j_per_use):
    baseline=uses*COMPUTE
    memory=COMPUTE+WRITE+(uses-1)*READ+uses*RETAIN
    avoided=baseline-memory
    stored=captured=leaked=conversion_loss=0.
    for _ in range(uses):
        lost=stored*LEAK
        stored-=lost;leaked+=lost
        captured+=captured_j_per_use
        stored+=captured_j_per_use*CHARGE_EFF
        conversion_loss+=captured_j_per_use*(1-CHARGE_EFF)
    recovered=stored*DISCHARGE_EFF
    conversion_loss+=stored*(1-DISCHARGE_EFF)
    assert abs(captured-recovered-leaked-conversion_loss)<1e-12
    return dict(uses=uses,captured_waste_per_use_j=captured_j_per_use,
        baseline_compute_j=round(baseline,9),memory_compute_j=round(memory,9),
        avoided_compute_j=round(avoided,9),captured_waste_j=round(captured,9),
        recovered_work_j=round(recovered,9),combined_benefit_j=round(avoided+recovered,9),
        storage_balance_error_j=round(captured-recovered-leaked-conversion_loss,12))
def main():
    rows=[scenario(n,w) for n in (1,2,5,10,50,100) for w in (0,.001,.005)]
    assert len(rows)==18 and all(abs(r['storage_balance_error_j'])<1e-10 for r in rows)
    return dict(status='COUPLED_ACCOUNTING_PASS',rows=rows,
        assumptions=dict(compute_j=COMPUTE,write_j=WRITE,read_j=READ,retention_per_use_j=RETAIN,
            charge_efficiency=CHARGE_EFF,discharge_efficiency=DISCHARGE_EFF,leakage_per_cycle=LEAK),
        caveats=['Illustrative Joule costs, not measured','Waste energy independent of computation savings; avoid double counting',
                 'Capture hardware and opportunity costs excluded','No claim that information itself stores recoverable energy'])
if __name__=='__main__':
    result=main()
    Path(__file__).with_name('53E3_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    for row in result['rows']:
        if row['captured_waste_per_use_j']==.001:print(row)
    print(result['status'],len(result['rows']))
