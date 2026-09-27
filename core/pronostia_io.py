"""PRONOSTIA (IEEE PHM 2012, FEMTO-ST): lozyska do zniszczenia. Rozwoj = Learning_set (6), ocena = Full_Test_Set (11).
Pobrane co drugie nagranie (acc_ nieparzyste) -> migawka 0,1 s co 20 s. 25,6 kHz, kolumny: h, m, s, us, poziom, pion.
Lozysko: Z = 13, d = 3,5 mm, Dm = 25,6 mm (dokument wyzwania, zal. A.1), kat styku 0."""
from __future__ import annotations
import os
from pathlib import Path
import numpy as np

DATA = Path(__file__).resolve().parent.parent.parent / "DATA" / "pronostia"
FS = 25600.0
RPM = {"1": 1800.0, "2": 1650.0, "3": 1500.0}
_Z, _d, _Dm = 13, 3.5, 25.6
MULT = {"BPFO": _Z / 2 * (1 - _d / _Dm), "BPFI": _Z / 2 * (1 + _d / _Dm),
        "BSF": _Dm / (2 * _d) * (1 - (_d / _Dm) ** 2), "FTF": 0.5 * (1 - _d / _Dm)}
DEV = ["Bearing1_1", "Bearing1_2", "Bearing2_1", "Bearing2_2", "Bearing3_1", "Bearing3_2"]
EVAL = ["Bearing1_3", "Bearing1_4", "Bearing1_5", "Bearing1_6", "Bearing1_7", "Bearing2_3", "Bearing2_4",
        "Bearing2_5", "Bearing2_6", "Bearing2_7", "Bearing3_3"]


def folder(b):
    return DATA / ("Learning_set" if b in DEV else "Full_Test_Set") / b


def snapshots(b):
    fs = sorted(f for f in os.listdir(folder(b)) if f.startswith("acc_"))
    return fs


def read(b, f):
    p = folder(b) / f
    txt = p.read_text()
    sep = ";" if ";" in txt.splitlines()[0] else ","
    a = np.array([[float(v) for v in l.split(sep)] for l in txt.splitlines() if l.strip()])
    return a[:, 4], a[:, 5]


def fr(b):
    return RPM[b[7]] / 60.0
