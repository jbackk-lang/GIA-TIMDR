"""51B.19 exact fixed-budget comparison (no dependencies).

Run from repository root: python research/51B19_EXACT_BUDGET.py
Analytic synthetic baseline; NOT the operational GIAFilter.
"""
import itertools
import json
import math

P_C, P_D = 0.05, 0.5
P_F1_C, P_F1_NOT_C = 0.99, 0.01
DISTANCE = {"signal": 1.0, "distractor": 0.0}
STATES = list(itertools.product((0, 1), repeat=2))

def h(p):
    return -p*math.log(p)-(1-p)*math.log(1-p)

def kl(p,q):
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))

def weight(c,d):
    return (P_C if c else 1-P_C)*(P_D if d else 1-P_D)

def future(c,d):
    return P_F1_C if c else P_F1_NOT_C

def code(c,d,selected):
    return tuple((name,c if name=="signal" else d) for name in sorted(selected))

def delta(selected):
    mass, positive = {}, {}
    for c,d in STATES:
        z, w = code(c,d,selected), weight(c,d)
        mass[z] = mass.get(z,0)+w
        positive[z] = positive.get(z,0)+w*future(c,d)
    return sum(weight(c,d)*kl(future(c,d),
               positive[code(c,d,selected)]/mass[code(c,d,selected)])
               for c,d in STATES)

def run():
    # Fixed one-event budget, same node IDs, times and coding conventions.
    # Selection is fixed before observing a history; no future leakage.
    rows = [{"selection":name,"events":1,
             "geometry_cost":DISTANCE[name],
             "delta_nats":delta((name,))} for name in DISTANCE]
    g = min(rows,key=lambda x:x["geometry_cost"])
    p = min(rows,key=lambda x:x["delta_nats"])
    q = P_C*P_F1_C+(1-P_C)*P_F1_NOT_C
    analytic = h(q)-P_C*h(P_F1_C)-(1-P_C)*h(P_F1_NOT_C)
    assert abs(g["delta_nats"]-analytic)<1e-12
    assert abs(p["delta_nats"])<1e-12
    hybrids = []
    for penalty in (0.0,0.05,0.15,0.17,0.20,0.30):
        z = min(rows,key=lambda x:(x["delta_nats"]+
                  penalty*x["geometry_cost"],x["delta_nats"]))
        assert z["delta_nats"]>=p["delta_nats"]-1e-12
        hybrids.append({"penalty":penalty,**z})
    return {"status":"EXACT_ENUMERATION_PASS",
            "budget_events":1,"G":g,"P_exact_optimum":p,
            "H":hybrids,"switch_penalty":analytic,
            "limitations":"Synthetic exhaustive benchmark; no fitted PCA, no real-data transfer, no operational GIAFilter."}

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
