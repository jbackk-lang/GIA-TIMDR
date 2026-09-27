"""Cechy rury per slad -> DATA/open_radar/feat_tube_v0_1_<part>/ (grupa 'tube')."""
import os, sys, json, numpy as np
import radar_or_io as io, radar_or_tube as rt

def run(part):
    wp = np.load(os.path.join(io.DATA, 'window_profile_dev.npy'))
    od = os.path.join(io.DATA, f'feat_tube_v0_1_{part}'); os.makedirs(od, exist_ok=True)
    for name, t in io.tracks(part):
        json.dump({'cls': str(t['cls']), 'tube': rt.track_tube(t, wp)}, open(os.path.join(od, name + '.json'), 'w'))
    print(part, len(os.listdir(od)))

if __name__ == '__main__':
    run(sys.argv[1])
