#!/usr/bin/env python3
"""Pilot G/H/R: rozróżnianie źródła, kanału i odbiornika.

Wymaga numpy. Uruchom: python docs/research/info_geometry/pilot_ghr.py
Nie zastępuje prerejestrowanego testu; wyniki eksploracyjne.
"""
import numpy as np

N = 4096
SEED = 20261114

def source(rng, a=0.6, n=N):
    e = rng.normal(size=n + 256)
    x = np.zeros(n + 256)
    for i in range(1, len(x)):
        x[i] = a * x[i-1] + np.sqrt(1-a*a) * e[i]
    return x[256:]

def channel(x, mode):
    if mode == "lowpass":
        return np.convolve(x, [0.25, 0.5, 0.25], mode="same")
    return x.copy()

def receiver(x, mode):
    if mode == "clip":
        return np.clip(x, -0.8, 0.8)
    return x.copy()

def features(x):
    """Cechy opisowe obserwacji; nie przypisują przyczyny."""
    x = np.asarray(x)
    lag = np.corrcoef(x[:-1], x[1:])[0, 1]
    # Opóźnieniowa krzywa 3D, różnice skończone.
    X = np.column_stack((x[4:], x[2:-2], x[:-4]))
    v = np.gradient(X, axis=0)
    a = np.gradient(v, axis=0)
    cross = np.cross(v, a)
    speed = np.linalg.norm(v, axis=1)
    valid = speed > 1e-6
    k = np.full(len(speed), np.nan)
    k[valid] = np.linalg.norm(cross[valid], axis=1) / speed[valid]**3
    return dict(std=float(x.std()), lag1=float(lag),
                curvature_median=float(np.nanmedian(k)),
                masked_fraction=float(np.mean(~valid)))

def run():
    rng = np.random.default_rng(SEED)
    # To samo losowanie innowacji dla porównań, dzięki czemu
    # różnice nie wynikają wyłącznie z innego szumu losowego.
    base = source(rng, a=0.6)
    changed_generator = source(np.random.default_rng(SEED), a=0.85)
    variants = {
        "BASE": (base, "identity", "identity"),
        "G": (changed_generator, "identity", "identity"),
        "H": (base, "lowpass", "identity"),
        "R": (base, "identity", "clip"),
        "GH": (changed_generator, "lowpass", "identity"),
        "GR": (changed_generator, "identity", "clip"),
        "ALL": (changed_generator, "lowpass", "clip"),
    }
    print("variant,std,lag1,curvature_median,masked_fraction")
    for name, (s, h, r) in variants.items():
        obs = receiver(channel(s, h), r)
        f = features(obs)
        print(f"{name},{f['std']:.6f},{f['lag1']:.6f},"
              f"{f['curvature_median']:.6f},{f['masked_fraction']:.6f}")

if __name__ == "__main__":
    run()
