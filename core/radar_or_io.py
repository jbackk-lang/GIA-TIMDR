"""Open Radar Initiative (Gusland i in. 2021), zbior 'moving target': podzial i cache.

Podzial ustalony PRZED jakimikolwiek cechami: w kazdej klasie slady sortowane po czasie
pierwszej klatki; pierwsze 60% -> dev, reszta -> eval (inne przeloty/sesje, jak w tescie turbiny).
Z kazdego sladu zapisujemy do 5 ciaglych kawalkow po 40 klatek (2 s), rowno rozlozonych
(cap 200 klatek), plus kinematyke trackera (|v|, zasieg, SNR) dla kontroli akwizycji.
"""
import json, os, sys
import numpy as np

DATA = os.path.join(os.path.dirname(__file__), '..', '..', 'DATA', 'open_radar')
CLASSES = ['person', 'bicycle', 'uav', 'vehicle']
DEV_FRAC = 0.6
CHUNK, NCHUNK = 40, 5   # v0.1-dev: zmienione z 10x20 (kadencja chodu wymaga >= 2 s)


def chunk_starts(n):
    if n < CHUNK:
        return [0] if n > 0 else []
    k = min(NCHUNK, n // CHUNK)
    return sorted(set(np.linspace(0, n - CHUNK, k).round().astype(int).tolist()))


def build(force=False):
    sys.path.insert(0, DATA)
    from load_safe import load
    S = load(os.path.join(DATA, 'moving_target_dataset.npy'))
    split = {'rule': 'per klasa, sort po ts[0], pierwsze 60% dev', 'dev': [], 'eval': []}
    for c in CLASSES:
        idx = sorted([i for i, x in enumerate(S) if x['class_name'] == c], key=lambda i: S[i]['ts'][0])
        nd = int(round(DEV_FRAC * len(idx)))
        split['dev'] += idx[:nd]; split['eval'] += idx[nd:]
    for part in ('dev', 'eval'):
        os.makedirs(os.path.join(DATA, part), exist_ok=True)
        for i in split[part]:
            fn = os.path.join(DATA, part, f'track_{i:03d}.npz')
            try:
                if force: raise ValueError
                np.load(fn)['cls']; continue          # juz poprawnie zapisany
            except Exception:
                pass
            x = S[i]; n = x['signature'].shape[0]
            st = chunk_starts(n)
            fr = np.concatenate([np.arange(s, min(s + CHUNK, n)) for s in st])
            rp = x['radar_parameters']
            np.savez(fn,
                     spec=x['signature'][fr].astype(np.complex64), frames=fr, chunk_starts=np.array(st),
                     ts=x['ts'][fr], velocity=x['velocity'][fr], range=x['range'][fr], snr_db=x['snr_db'][fr],
                     n_frames=n, cls=x['class_name'], prf=rp['prf'], bw=rp['bw'], fc=rp['fc'])
    split['counts'] = {p: {c: int(sum(S[i]['class_name'] == c for i in split[p])) for c in CLASSES} for p in ('dev', 'eval')}
    json.dump(split, open(os.path.join(DATA, 'split_v0_1.json'), 'w'), indent=1)
    print(split['counts'])


def tracks(part):
    d = os.path.join(DATA, part)
    for f in sorted(os.listdir(d)):
        if f.endswith('.npz'):
            z = np.load(os.path.join(d, f))
            yield f[:-4], {k: z[k] for k in z.files}


if __name__ == '__main__':
    build(force='--force' in sys.argv)
