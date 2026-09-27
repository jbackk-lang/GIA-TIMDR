"""wind_lbf_io.py -- odczyt nagran Fraunhofer LBF (turbina 750 W) i podzial rozwoj/ocena.
Tachometr sluzy WYLACZNIE do oceny i do wyboru linii odniesienia w fazie rozwoju -- nigdy jako wejscie metody."""
from __future__ import annotations
import io, zipfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import decimate

DATA = Path(__file__).resolve().parent.parent.parent / "DATA" / "wind_lbf"
CLASSES = {"Healthy": ("Healthy.zip", "Healthy/"), "InnerRace": ("Bearing.zip", "Bearing/InnerRace/"),
           "OuterRace": ("Bearing.zip", "Bearing/OutterRace/"), "RollerElement": ("Bearing.zip", "Bearing/RollerElement/"),
           "InnerRace_MassImbalance": ("Bearing.zip", "Bearing/InnerRace_MassImbalance/"), "MassImbalance": ("Imbalance_Mid.zip", "Mid/")}
MULT = {"BPFO": 4.593, "BPFI": 6.407, "BSF": 5.995, "FTF": 0.417}   # lozysko 6007 2Z, 11 kulek (publikacja zbioru)
TACH_PPR = 108


def files(cls):
    z, pre = CLASSES[cls]
    names = sorted(n for n in zipfile.ZipFile(DATA / z).namelist() if n.startswith(pre) and n.endswith(".mat"))
    return z, names


def split(cls):
    """Rozwoj = pierwsza trzecia nagran klasy (zaokraglona w gore), ocena = reszta (kolejnosc czasowa)."""
    _, names = files(cls); k = -(-len(names) // 3)
    return names[:k], names[k:]


def load(cls, name, channels=("brng_f_y",)):
    z, _ = files(cls)
    b = zipfile.ZipFile(DATA / z).read(name)
    m = loadmat(io.BytesIO(b), squeeze_me=True, variable_names=list(channels) + ["tach", "Sample_rate"])
    fs = float(m["Sample_rate"])
    return fs, {c: np.asarray(m[c], float) for c in channels}, np.asarray(m["tach"], float), fs / 25


def tach_speed(tach, ft, thr=2.0):
    """Predkosc z tachometru [obr/s] w chwilach impulsow (tylko do oceny)."""
    up = np.where((tach[1:] >= thr) & (tach[:-1] < thr))[0]
    tt = up[1:] / ft; fr = 1 / (TACH_PPR * np.diff(up) / ft)
    return tt, fr


def dec(x, q):
    y = x
    while q > 1:
        s = min(q, 8)
        while q % s:
            s -= 1
        y = decimate(y, s, ftype="fir", zero_phase=True); q //= s
    return y
