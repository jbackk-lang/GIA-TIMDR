# timdr_torus_map.py
# TIMDR – TORUS-MAP
# Analiza radialna widma -> wykrywanie torusa energii

from PIL import Image
import numpy as np

def _to_float(img):
    return np.asarray(img.convert("L"), dtype=np.float32) / 255.0

def _fft_mag(gray):
    F = np.fft.fft2(gray)
    Fshift = np.fft.fftshift(F)
    mag = np.log1p(np.abs(Fshift))
    mag /= mag.max() + 1e-8
    return mag

def timdr_torus_map(img):
    gray = _to_float(img)
    mag = _fft_mag(gray)

    h, w = mag.shape
    cy, cx = h//2, w//2

    # odległość od środka (promień)
    Y, X = np.ogrid[:h, :w]
    R = np.sqrt((Y-cy)**2 + (X-cx)**2)

    # normalizacja promienia
    Rn = R / R.max()

    # torus = widmo * promień
    torus = mag * Rn
    torus /= torus.max() + 1e-8

    torus_rgb = np.stack([torus, torus, torus], axis=-1)
    torus_rgb = (torus_rgb * 255).astype(np.uint8)

    return Image.fromarray(torus_rgb)
