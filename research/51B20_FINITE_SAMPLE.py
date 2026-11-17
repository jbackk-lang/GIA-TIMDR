"""51B.20 finite-sample geometry prior versus predictive selection.

Run: python research/51B20_FINITE_SAMPLE.py
Synthetic binary feature selection, known population loss; not operational GIAFilter.
"""
import json
import math
import random

P_SIGNAL = 0.05
P_Y1_SIGNAL = 0.99
P_Y1_NO_SIGNAL = 0.01
SIZES = (20, 50, 200, 1000)
REPEATS = 1000
PENALTY = 0.02

def entropy(p):
    return 0.0 if p in (0.0, 1.0) else -p * math.log(p) - (1-p) * math.log(1-p)

def draw(rng):
    s = int(rng.random() < P_SIGNAL)
    d = int(rng.random() < 0.5)
    y = int(rng.random() < (P_Y1_SIGNAL if s else P_Y1_NO_SIGNAL))
    return s, d, y

def estimated_mi(samples, index):
    # Jeffreys smoothing of the 2x2 empirical joint table.
    table = [[0.5, 0.5], [0.5, 0.5]]
    for row in samples:
        table[row[index]][row[2]] += 1
    total = sum(map(sum, table))
    joint = [[v/total for v in row] for row in table]
    px = [sum(row) for row in joint]
    py = [sum(joint[i][j] for i in range(2)) for j in range(2)]
    return sum(joint[i][j]*math.log(joint[i][j]/(px[i]*py[j]))
               for i in range(2) for j in range(2))

def run():
    q = P_SIGNAL*P_Y1_SIGNAL+(1-P_SIGNAL)*P_Y1_NO_SIGNAL
    lost = entropy(q) - P_SIGNAL*entropy(P_Y1_SIGNAL) - (1-P_SIGNAL)*entropy(P_Y1_NO_SIGNAL)
    rows = []
    for geometry in ('aligned', 'misleading'):
        costs = (0.0, 1.0) if geometry == 'aligned' else (1.0, 0.0)
        for n in SIZES:
            wins = {'P':0, 'H':0, 'G':0}
            for trial in range(REPEATS):
                rng = random.Random(20261117 + 100000*n + trial)
                train = [draw(rng) for _ in range(n)]
                mi = [estimated_mi(train,i) for i in (0,1)]
                p = max((0,1), key=lambda i:(mi[i],i))
                h = max((0,1), key=lambda i:(mi[i]-PENALTY*costs[i],i))
                g = min((0,1), key=lambda i:(costs[i],-i))
                for label, choice in [('P',p),('H',h),('G',g)]:
                    wins[label] += choice == 0
            row = {'geometry':geometry,'train_n':n,'repeats':REPEATS,
                   'penalty':PENALTY,'delta_opt_nats':0.0,
                   'delta_if_distractor_nats':lost}
            for label in ('G','P','H'):
                row[label+'_signal_selection_rate'] = wins[label]/REPEATS
                row[label+'_mean_delta_nats'] = (1-wins[label]/REPEATS)*lost
            rows.append(row)
    assert all(r['H_mean_delta_nats'] <= r['P_mean_delta_nats']+1e-14
               for r in rows if r['geometry']=='aligned')
    assert all(r['H_mean_delta_nats'] >= r['P_mean_delta_nats']-1e-14
               for r in rows if r['geometry']=='misleading')
    return {'status':'FINITE_SAMPLE_PASS','seed':20261117,'rows':rows,
            'limitations':'Synthetic binary features, fixed penalty, known population loss; no operational GIAFilter.'}

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
