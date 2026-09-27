"""Ekstrakcja cech per slad (cache w DATA/open_radar/feat_<part>/)."""
import os, sys, json, numpy as np
import radar_or_io as io, radar_or_features as rf

MIN_CHUNK = 16   # klatek (0,8 s) -- krotsze kawalki nie daja cech rytmu


def track_features(t):
    spec = t['spec']; prf = float(t['prf'])
    fr = t['frames']; st = list(t['chunk_starts'])
    # kawalki w cache sa kolejno po sobie; granice z chunk_starts
    bounds, pos = [], 0
    for s in st:
        n = int(np.sum((fr >= s) & (fr < s + io.CHUNK)))
        bounds.append((pos, pos + n)); pos += n
    sv, ch, cv = [], [], []
    for a, b in bounds:
        if b - a < MIN_CHUNK:
            continue
        A, f = rf.body_align(spec[a:b], prf)
        sv.append(rf.chunk_sieve(A, f)); ch.append(rf.chunk_character(A, f)); cv.append(rf.chunk_cvd(A))
    med = lambda L, k: float(np.median([d[k] for d in L])) if L else float('nan')
    jem = rf.jem_cepstrum(spec, prf)
    sd, sent, bw = rf.doppler_stats(spec, prf)
    q = lambda v: [float(np.median(v)), float(np.percentile(v, 90))]
    return {
        'cls': str(t['cls']), 'bw': float(t['bw']), 'n_frames': int(t['n_frames']), 'n_chunks': len(sv),
        'sieve': [med(sv, 'Q'), med(sv, 'mesh'), med(sv, 'alpha'), med(sv, 'mesh_off')],
        'char': [med(ch, 'L'), med(ch, 'P'), med(ch, 'M')],
        'cvd': [med(cv, 'cvd_peak'), med(cv, 'cvd_alpha')],
        'jem': q(jem),
        'dopp': q(sd) + q(sent) + q(bw),
        'kin': [float(np.median(np.abs(t['velocity']))), float(np.median(t['range'])), float(np.median(t['snr_db']))],
    }


def run(part, budget=165, tag='v0_1'):
    import time
    t0 = time.time()
    od = os.path.join(io.DATA, f'feat_{tag}_{part}'); os.makedirs(od, exist_ok=True)
    done = 0
    for name, t in io.tracks(part):
        fn = os.path.join(od, name + '.json')
        if os.path.exists(fn):
            continue
        json.dump(track_features(t), open(fn, 'w'))
        done += 1
        if time.time() - t0 > budget:
            break
    left = sum(1 for f in os.listdir(os.path.join(io.DATA, part)) if f.endswith('.npz')) - len(os.listdir(od))
    print(part, 'zrobione', done, 'zostalo', left)


if __name__ == '__main__':
    run(sys.argv[1], tag=sys.argv[2] if len(sys.argv) > 2 else 'v0_1')
