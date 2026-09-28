"""Krzywe uczenia (PREREG_PADERBORN_LEARNING_CURVES_v0_1): dane wejsciowe dla dwoch ramion tej samej sieci z uwaga.
Na pomiar (2 s, decymacja do 32 kHz, jak w sicie rezonansowym):
  raw -- surowy przebieg 64000 probek (float32), bez zadnej obrobki poza usunieciem sredniej;
  tok -- pole TIMDR: 15 pasm nosnych (tokeny) x widmo obwiedni znormalizowane mediana (odniesienie, tlo = 1),
         os modulacji przeliczona na rzedy obrotu (kotwica z kinematyki: alfa / f_obr), 0,5-12 rzedow co 0,05, max w binie.
Zapis: DATA/paderborn_lc_v0_1/<lozysko>.npz."""
import sys
from io import BytesIO
from pathlib import Path
import numpy as np
from scipy.signal import decimate
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.real_paderborn_real_damage import BEARINGS, CONDS, RAW, rpm  # noqa: E402
from core.real_paderborn_resonance_sieve import resonance_map, N2  # noqa: E402

OUT = Path(__file__).resolve().parent.parent.parent / "DATA" / "paderborn_lc_v0_1"
ORD = np.arange(0.5, 12.0 + 1e-9, 0.05)


def tokens(x, r):
    Rz, al = resonance_map(x); o = al / (r / 60.0); idx = np.digitize(o, ORD) - 1
    T = np.zeros((Rz.shape[0], len(ORD) - 1), np.float32)
    for k in range(len(ORD) - 1):
        m = idx == k
        if m.any():
            T[:, k] = Rz[:, m].max(1)
    return np.log(T + 1e-6)


def bearing(b):
    from unrar.cffi import rarfile
    from scipy.io import loadmat
    OUT.mkdir(parents=True, exist_ok=True); rf = rarfile.RarFile(str(RAW / f"{b}.rar"))
    raw, tok, cond, meas = [], [], [], []
    for cd in CONDS:
        for n in range(1, 21):
            mat = loadmat(BytesIO(rf.read(f"{b}/{cd}_{b}_{n}.mat")), squeeze_me=True, struct_as_record=False)
            s = mat[[x for x in mat if not x.startswith("__")][0]]
            v = np.asarray({e.Name: e.Data for e in s.Y}["vibration_1"], float)
            x2 = decimate(v, 2, ftype="fir", zero_phase=True)[:N2]; x2 = x2 - x2.mean()
            raw.append(x2.astype(np.float32)); tok.append(tokens(x2, rpm(cd))); cond.append(cd); meas.append(n)
    np.savez(OUT / f"{b}.npz", raw=np.array(raw), tok=np.array(tok), cond=np.array(cond), meas=np.array(meas))


if __name__ == "__main__":
    import time
    t0 = time.time()
    for b in sys.argv[1:]:
        if (OUT / f"{b}.npz").exists():
            continue
        bearing(b); print(b, round(time.time() - t0), flush=True)
