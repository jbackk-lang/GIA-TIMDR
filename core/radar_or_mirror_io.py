"""Open Radar v0.3 (lustro): cache calych sladow (do CAP klatek) w ukladzie linii ciala.

Podzial bez zmian (split_v0_1.json, per klasa po czasie, 60% dev). Dla kazdej klatki: moc |widmo|^2, linia ciala =
szczyt widma bez binu zerowego (+-2), czestotliwosc wzgledna f - f_ciala zawinieta modulo PRF (Doppler jest okresowy),
zsumowana do stalej siatki 100 Hz w +-8 kHz. Zapis: full_{dev,eval}/track_XXX.npz (P[klatki, 160], ts, f_body, cls, bw, prf).
"""
import json, os, sys, time
import numpy as np

DATA = os.path.join(os.path.dirname(__file__), '..', '..', 'DATA', 'open_radar')
CAP = 600                          # klatek (~30 s)
EDGES = np.arange(-8000, 8001, 100.0)


def body_frame(spec, prf):
    F, N = spec.shape
    P = np.abs(spec.astype(np.complex64)) ** 2
    f = (np.arange(N) - N // 2) * prf / N
    Pm = P.copy(); Pm[:, N // 2 - 2: N // 2 + 3] = 0
    fb = f[np.argmax(Pm, 1)]
    rel = ((f[None, :] - fb[:, None] + prf / 2) % prf) - prf / 2
    idx = np.digitize(rel, EDGES) - 1
    ok = (idx >= 0) & (idx < len(EDGES) - 1)
    G = np.zeros((F, len(EDGES) - 1))
    rows = np.repeat(np.arange(F)[:, None], N, 1)
    np.add.at(G, (rows[ok], idx[ok]), P[ok])
    return G.astype(np.float32), fb.astype(np.float32)


def build(parts=('dev', 'eval'), start=0, stop=None):
    sys.path.insert(0, DATA)
    from load_safe import load
    t0 = time.time(); S = load(os.path.join(DATA, 'moving_target_dataset.npy')); print('load', round(time.time() - t0, 1), 's')
    split = json.load(open(os.path.join(DATA, 'split_v0_1.json')))
    for part in parts:
        d = os.path.join(DATA, f'full_{part}'); os.makedirs(d, exist_ok=True)
        for i in split[part][start:stop]:
            fn = os.path.join(d, f'track_{i:03d}.npz')
            if os.path.exists(fn):
                try:
                    np.load(fn)['cls']; continue
                except Exception:
                    pass
            x = S[i]; n = min(CAP, x['signature'].shape[0]); rp = x['radar_parameters']
            G, fb = body_frame(x['signature'][:n], rp['prf'])
            np.savez(fn, P=G, f_body=fb, ts=x['ts'][:n], cls=x['class_name'], bw=rp['bw'], prf=rp['prf'],
                     n_total=x['signature'].shape[0])
        print(part, 'ok', round(time.time() - t0, 1), 's')


if __name__ == '__main__':
    build()
