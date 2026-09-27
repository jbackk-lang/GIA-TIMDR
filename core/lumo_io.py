"""LUMO (wieza kratowa, Leibniz Univ. Hannover, CC-BY 3.0): bloki 10-min z paczek przykladowych -> widma drgan.
Na blok: srednie znormalizowane (mediana) widmo Welcha 18 kanalow przyspieszen (nperseg 2^15, ~0,05 Hz, 0-120 Hz),
widmo kazdego kanalu przy <= 120 Hz (do samokorekty kotwic), srednia temperatura stali temp01, etykieta z folderu."""
import glob, io, json, os, zipfile
import numpy as np
import scipy.io as sio
from scipy.signal import welch

LUMO = os.path.join(os.path.dirname(__file__), '..', '..', 'DATA', 'lumo')
FMAX = 120.0


def blocks():
    for zp in sorted(glob.glob(os.path.join(LUMO, 'exemplary_datasets_*.zip'))):
        z = zipfile.ZipFile(zp)
        for m in z.namelist():
            if m.endswith('.mat'):
                yield zp, z, m


def build(limit=None):
    out = os.path.join(LUMO, 'lumo_spectra.npz'); done = {}
    if os.path.exists(out):
        d = np.load(out, allow_pickle=False); done = {k: i for i, k in enumerate(d['keys'])}
        acc = {k: list(d[k]) for k in d.files}
    else:
        acc = {'keys': [], 'S': [], 'temp': [], 'state': [], 'time': []}
    n = 0
    for zp, z, m in blocks():
        key = os.path.basename(zp)[:-4] + '/' + m
        if key in done:
            continue
        D = sio.loadmat(io.BytesIO(z.read(m)), squeeze_me=True, struct_as_record=False)['Dat']
        names = list(D.ChannelNames); X = D.Data; fs = float(D.Fs)
        acc_idx = [i for i, c in enumerate(names) if c.startswith('accel')]
        f, P = welch(X[:, acc_idx].T.astype(float), fs, nperseg=2 ** 15)
        k = f <= FMAX; P = P[:, k]
        acc['keys'].append(key); acc['S'].append((P / np.median(P, 1, keepdims=True)).astype(np.float32))
        acc['temp'].append(float(np.nanmean(X[:, names.index('temp01')])))
        acc['state'].append(m.split('/')[0]); acc['time'].append(m.split('_')[-1][:-4])
        n += 1
        if limit and n >= limit:
            break
    np.savez(out, keys=np.array(acc['keys']), S=np.array(acc['S']), temp=np.array(acc['temp']), state=np.array(acc['state']),
             time=np.array(acc['time']), f=f[k])
    return len(acc['keys'])


if __name__ == '__main__':
    import sys
    print(build(int(sys.argv[1]) if len(sys.argv) > 1 else None))
