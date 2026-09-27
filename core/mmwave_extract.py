"""mmWave (AWR1642, Data in Brief 2020): adc_Data.mat (tabela MATLAB, 4 Rx x 26 214 400 probek zespolonych)
-> widmo Dopplera klatek: 400 klatek x 128 chirpow x 512 probek; FFT zasiegu, usuniecie tla statycznego (srednia po
chirpach w klatce), FFT Dopplera (Hann), suma mocy po zasiegu 0,25-10 m i po 4 Rx. Wynik: P[klatka, 128 binow], RD
zasiegu (profil) do kontroli. Strumieniowo -- VM ma 3 GB RAM."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from mmwave_matstream import Raw, walk_stream

NF, NC, NS = 400, 128, 512
R_LO, R_HI = 5, 205                     # zasieg w binach (~0,05 m/bin); cel lezy w ujemnej polowce FFT


def extract(path, out):
    tmp = os.path.expanduser('~/mm/_re.f32')
    acc = {'P': np.zeros((NF, NC)), 'R': np.zeros((NF, NS)), 'M': np.zeros((NF, NS)), 'k': 0}
    def on_array(s, dims, cplx, n):
        if acc['k'] % 2 == 0:                     # czesc rzeczywista -> dysk (float32)
            mm = np.memmap(tmp, np.float32, 'w+', shape=(n // 8,)); pos = 0
            while pos < n // 8:
                k = min(1 << 20, n // 8 - pos); mm[pos:pos + k] = np.frombuffer(s.read(8 * k), '<f8'); pos += k
            mm.flush(); del mm
        else:                                     # czesc urojona -> klatka po klatce
            re = np.memmap(tmp, np.float32, 'r', shape=(n // 8,)); fl = NC * NS
            win_d = np.hanning(NC)[:, None]
            for i in range(NF):
                im = np.frombuffer(s.read(8 * fl), '<f8').astype(np.float32)
                z = (re[i * fl:(i + 1) * fl] + 1j * im).reshape(NC, NS)
                Rg = np.fft.fft(z * np.hanning(NS)[None, :], axis=1)
                acc['R'][i] += (np.abs(Rg) ** 2).mean(0)
                Rg = Rg - Rg.mean(0, keepdims=True)                   # tlo statyczne
                acc['M'][i] += (np.abs(Rg) ** 2).mean(0)
                D = np.fft.fftshift(np.fft.fft(Rg * win_d, axis=0), axes=0)
                acc['P'][i] += (np.abs(D[:, NS - R_HI:NS - R_LO]) ** 2).sum(1)   # cel w ujemnej polowce (zasieg = 512 - bin)
            del re
        acc['k'] += 1
    if isinstance(path, str):
        with open(path, 'rb') as f:
            f.read(128); walk_stream(Raw(f), on_array)
    else:
        path.read(128); walk_stream(path, on_array)
    os.remove(tmp)
    np.savez(out, P=acc['P'].astype(np.float32), R=acc['R'].astype(np.float32), M=acc['M'].astype(np.float32), n_arrays=acc['k'])

if __name__ == '__main__':
    extract(sys.argv[1], sys.argv[2])


class BlockStream:
    """Czytanie z blokow libarchive (wpis w RAR) jak z pliku -- bez wypakowywania na dysk."""
    def __init__(self, blocks):
        self.it = iter(blocks); self.buf = bytearray()
    def read(self, n):
        while len(self.buf) < n:
            try:
                self.buf += next(self.it)
            except StopIteration:
                raise EOFError
        out = bytes(self.buf[:n]); del self.buf[:n]
        return out


def extract_rar(rar, outdir, only=None, limit_s=160):
    """Przetwarza kolejne adc_Data.mat prosto z archiwum RAR; pomija juz zrobione; konczy przed limitem czasu."""
    import libarchive, time
    t0 = time.time(); cls = os.path.basename(rar).split('.')[0]
    with libarchive.file_reader(rar) as arc:
        for e in arc:
            if not e.pathname.endswith('adc_Data.mat'):
                continue
            idx = e.pathname.split('/')[-2]; out = os.path.join(outdir, f'{cls}_{int(idx):02d}.npz')
            if os.path.exists(out) or (only and idx not in only):
                continue
            if time.time() - t0 > limit_s:
                print('limit czasu'); return
            extract(BlockStream(e.get_blocks()), out); print('zrobione', out, round(time.time() - t0), 's', flush=True)
